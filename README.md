# Gloel

The dataset and code for paper [1].

As is stated in [1], this paper aims to improve List-Only Entity Linking[2] by taking into account global coherence among entities.

We first modified the dataset since, for one thing, each document merely contains a single mention to be disambiguated, which does not fit in with most real-life occasions. For another, the target entity lists are not ambiguous enough, giving rise to the situation that most mentions merely have one candidate entity, and the disambiguation problem is converted to judging whether this sole candidate entity is true or not.

Specifically, the reconstructed target entity lists can be found in Entity List.txt. The we also provide code in as for how to generate the documents.


[1] Weixin Zeng, Xiang Zhao, Jiuyang Tang, Haichuan Shang: Collective List-Only Entity Linking: A Graph-Based Approach. IEEE Access, 2018, 6: 16035-16045. Available: https://ieeexplore.ieee.org/document/8320777/

[2] Y. Lin, C.-Y. Lin, and H. Ji, List-only entity linking, in Proc. 55th Annu. Meeting Assoc. Comput. Linguistics, Vancouver, BC, Canada, 2017, pp. 536-541. Available: https://doi.org/10.18653/v1/P17-2085
