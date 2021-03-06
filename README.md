# Gloel

The dataset and code for paper [1].

As is stated in [1], this paper aims to improve List-Only Entity Linking[2] by taking into account global coherence among entities.

## Datasets
We first modified the dataset since, for one thing, each document merely contains a single mention to be disambiguated, which does not fit in with most real-life occasions. For another, the target entity lists are not ambiguous enough, giving rise to the situation that most mentions merely have one candidate entity, and the disambiguation problem is converted to judging whether this sole candidate entity is true or not.

Specifically, the reconstructed target entity lists can be found in **Entity List.txt**. We also provide code in **data_gen.py** as for how to generate the documents. When it comes to how to corrupt the dataset, you can follow the descriptions in the paper.

The generated document follows the format of:
>Article: Houston Mavericks

>target entity name \t mention name \t sentence

and each Article is regarded as a separate document.

## Linking Method
Then regarding the specific linking method, the candidate genration process can be easily re-implemented using *TABLE 1. String matching rules* in [1]. Besides, the random walk process for candidate entities ranking can be found in **random_walk.py**. A toy example is also provided.

We are currently working on organizing the codes for entity information enrichment. You are also welcome to reimplement -- it is not that hard. Let me know if you have any problems.

[1] Weixin Zeng, Xiang Zhao, Jiuyang Tang, Haichuan Shang: Collective List-Only Entity Linking: A Graph-Based Approach. IEEE Access, 2018, 6: 16035-16045. Available at: https://ieeexplore.ieee.org/document/8320777/

[2] Y. Lin, C.-Y. Lin, and H. Ji, List-only entity linking, in Proc. 55th Annu. Meeting Assoc. Comput. Linguistics, Vancouver, BC, Canada, 2017, pp. 536-541. Available at: https://doi.org/10.18653/v1/P17-2085
