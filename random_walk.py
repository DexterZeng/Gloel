# coding:utf-8
import numpy as np

class Node:
    def __init__(self, mention_id, mention_name, entity_name, local_score, ground_truth):
        self.mention_id = mention_id
        self.mention_name = mention_name
        self.entity_name = entity_name
        self.local_score = local_score
        self.ground_truth = ground_truth
        self.id = -1

    def set_matrix_id(self, id):
        self.id = id

def p_pagerank(E_d, M, index2node):
    alpha = 0.85
    if len(E_d) == 0:
        v = np.zeros(n)
        for i in index2node:
            v[i] = index2node[i].local_score
    else:
        v = np.zeros(n)
        for d_note in E_d:
            v[d_note.id] = 1
    P_n = v
    P_n1 = np.zeros(n)
    e = 100000
    k = 0
    while e > 0.0001:
        P_n1 = alpha * np.dot(M, P_n) + (1 - alpha)* v
        e = P_n1 - P_n
        e = max(map(abs, e))
        P_n = P_n1
        k += 1
    return P_n1/sum(P_n1)

def simKL(vec1, vec2):
    assert len(vec1) == len(vec2)
    sum = 0
    for j in range(len(vec1)):
        if vec2[j] != 0:
            if vec1[j] != 0:
                sum = sum + vec1[j]* np.log(vec1[j]/vec2[j])
            else:
                sum = sum
        else:
            sum = sum + vec1[j]* 20
    return 1/float(sum)

# load the file containing mention and its corresponding candidates with local scores
# format: docid \t mentionid \t mentionName \t trueEntityName \t candidateEntityname@itsLocalScore \t.....
inf = open('toy.txt')
doc2mentions = dict()
for iline in inf:
    strs = iline.strip().split('\t')
    docid = strs[0]
    menid = strs[1]
    men = strs[2]
    truen = strs[3]
    nodes = []
    for i in range(4, len(strs)):
        enname = strs[i].split('@')[0]
        scoree = strs[i].split('@')[1]
        n = Node(menid, men, enname,scoree,truen)
        nodes.append(n)
    if docid in doc2mentions:
        mentions = doc2mentions[docid]
    else:
        mentions = dict()
    #### mentions are recorded by its ids
    mentions[menid] = nodes
    doc2mentions[docid] = mentions

# load relations and the corresponding relation scores
# in the toy example, we merely provide the relations and all of their local scores are considered as 1
# the format docid \t startEntity \t endEntity

doc2realtions = dict()
inf = open('toy_relation.txt')
for iline in inf:
    strs = iline.strip().split('\t')
    if strs[0] not in doc2realtions:
        relations = []
    else:
        relations = doc2realtions[strs[0]]
    relations.append((strs[1], strs[2]))
    doc2realtions[strs[0]] = relations

# start to disambiguate
overall = 0
overall_true = 0
for doc in doc2mentions:
    if doc in doc2realtions:
        relations = doc2realtions[doc]
    else:
        relations = []
    # create edges
    edges = []
    allnodes = []
    mens = doc2mentions[doc]
    for men in mens:
        nodes = mens[men]
        allnodes.extend(nodes)
        for othermen in mens:
            if othermen != men:
                othernodes = mens[othermen]
                for node in nodes:
                    for onode in othernodes:
                        # if two entitie shave a relation, add it to edges; if there is a score between them, change this to include score
                        if node.entity_name == onode.entity_name or (node.entity_name, onode.entity_name) in relations:
                            edges.append([node, onode])
                            edges.append([onode, node])

    assert len(allnodes) == len(set(allnodes))

    # create the graph
    index2node = dict()
    n = len(allnodes) # num of nodes
    for i in range(n): # id2node node2id
        index2node[i] = allnodes[i]
        allnodes[i].set_matrix_id(i)
    #################################################################### pagerank process
    n = len(index2node)
    R = np.zeros([n, n])  # generate adjacency matrix M, shape of (n,n)
    # print R
    for node1 in allnodes:
        for node2 in allnodes:
            if [node1, node2] in edges:
                R[node2.id, node1.id] = float(1)  # change 1 to relation score !!!
    # M is the probability matrix !!! after normalization
    M = np.zeros([n, n])
    for j in range(n):
        sum_of_col = sum(R[:, j])
        if sum_of_col != 0:
            for i in range(n):
                M[i, j] = R[i, j] / float(sum_of_col)
    ####################### update the document signature after disambiguation of a entity
    E_d = [] # unambiguous entities
    for men in mens:
        if len(mens[men]) == 1:
            E_d.append(mens[men][0]) # assume those mentions merely containing one candidate entity is unambiguous
    ### compure signature score of the documentS
    ss_d = p_pagerank(E_d, M, index2node)
    # sort mens by the number of candidate entities it has from low to high
    sort_mens = sorted(mens.items(), key=lambda item: len(item[1]), reverse=False)
    for men in sort_mens:
        men_id = men[0]
        men_nodes = men[1]
        if len(men_nodes) != 1: # filter out those only containing one mentions
            canen2finalscore = dict()
            for men_node in men_nodes:
                ss_e = p_pagerank([men_node], M, index2node) # generate entity signature
                sim = simKL(ss_e, ss_d) # calculate the similarity between the vectors, we choose KL divergence here, could be changed to cosine similarity
                canen2finalscore[men_node.id] = sim * float(men_node.local_score) # we use multiplication here, could be summation
            sort_canen = sorted(canen2finalscore.items(), key=lambda item: item[1], reverse=True)
            E_d.append(index2node[sort_canen[0][0]])
            # update document signature with newly added entity
            ss_d = p_pagerank(E_d, M, index2node)
    assert len(E_d) == len(mens)
    ### E_d contains all disambiguated nodes, should equal to the number of mentions!

    true_counter = 0
    for en in E_d:
        if en.entity_name == en.ground_truth:
            true_counter += 1

    overall += len(E_d)
    overall_true += true_counter
    print(doc + ' : '+ str(true_counter) + ' / ' + str(len(E_d)))

print('overall' + ' : '+ str(overall_true) + ' / ' + str(overall) + ' = ' + str(float(overall_true)/float(overall)))