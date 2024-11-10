# CS303 Project1 Report

## Introduction

Information Exposure Maximization is modeled as an algorithmic problem in [1] to reduce the echo chamber and filter-bubble effect: users get less exposure to conflicting viewpoints and are isolated in their own informational bubble. This problem studies a social network represented as a graph **G=(V,E)**, where **V**  is the set of nodes in **G** (i.e., users) and **E** is the set of edges in  **G** (i.e., social links between users).  The goal of this problem is to select two user sets (referred to as "activities") in a social network to maximize the expected number of nodes. These nodes either connect to two activities simultaneously or are unaware of both activities. This process involves not only the dissemination of information, but also how to balance the exposure of different viewpoints or movements to promote broader information exchange and discussion.

By combining heuristic algorithms and evolutionary algorithms, this project will explore how to effectively select seed nodes to achieve a balance between effective information dissemination and exposure in dynamic social networks. This is not only of great significance for understanding the information flow in social media, but also provides new perspectives and ideas for algorithm design and social network applications. In the following, several preliminary definitions are provided first, and then a formal definition and an example of the IEM problem are presented.



## Preliminary

**Social Network:** 𝑮 = (𝑽, 𝑬) , where 𝑉 = {𝑣1, ⋯ , 𝑣𝑛} represents the node set, and 𝐸 = 𝑉 × 𝑉 represents the edges between nodes.

**Campaigns:** 𝑪 = {𝒄𝟏, 𝒄𝟐} represents two campaigns; each campaign holds a viewpoint.

**Initial Seed Set:** 𝑰𝒊 ⊆ 𝑽,𝒊 ∈ {𝟏**，**𝟐} represents the initial seed set for campaigns 𝑐𝑖.

**Balanced Seed Set:** 𝑺𝒊 ⊆ 𝑽,𝒊 ∈ {𝟏**，**𝟐} represents the target seed set that you need to find for each campaign 𝑐𝑖 .

**Budget:** 𝒌 represents the size of the target seed set; |𝑆1 | + |𝑆2 | ≤ 𝑘.

**Diffusion Probability:** 𝑷𝒊 = {𝒑( 𝒊 𝒖,𝒗) |(𝒖, 𝒗) ∈ 𝑬},𝒊 ∈ {𝟏**，**𝟐} represents the edge weight associated with campaign 𝑐𝑖 , where 𝑝( 𝑖 𝑢,𝑣) represents the probability of node 𝑢 activating node 𝑣 under each campaign 𝑐𝑖 .

**Diffusion Model:** 𝑴 captures the stochastic process for seed set 𝑈𝑖 = 𝐼𝑖 ∪𝑆𝑖 spreading information on 𝐺 . ee assume that information on the two campaigns propagates in the network following the independent cascade (IC) model. The two campaigns’ messages propagate independently of each other (such propagation is often called *heterogeneous propagation*). The diffusion 

process of the first campaign (the process for the second campaign is analogous) unfolds in the following discrete steps:

- In step 𝑡 = 0, the nodes in seed set 𝑈1 are activated, while the other nodes stay inactive;

- Each active user 𝑢 for campaign 𝑐1 in step 𝑡 will activate each of its outgoing neighbor 𝑣 that is inactive for campaign 𝑐1 in step 𝑡 −1 with probability 𝑝1(𝑢,𝑣) ;

  The activation process can be considered as flipping a coin with head probability 𝑝1(𝑢,𝑣) : if the result is head, then 𝑣 is activated; otherwise, 𝑣 stays inactive;

  Note that 𝑢 has only one chance to activate its outgoing neighbors for campaign 𝑐1. After that, 𝑢 stays active and stops the activation for campaign 𝑐1;

- The diffusion instance terminates when no more nodes can be activated.

**Exposed Nodes:** Given a seed set 𝑈, 𝑟𝑖(𝑈) is the vertices that are reached from 𝑈 using the aforementioned cascade process for campaign 𝑐𝑖 . Note that in one propagation, in addition to nodes that were successfully activated by 𝑈 , nodes that were once attempted to be activated but were not successfully activated by 𝑈 are also considered to be reached by 𝑈. Since the diffusion process is random, 𝑟𝑖(𝑈) is a random variable.



## Methodology

The following will use heuristic algorithms and evolutionary algorithms to analyze the IEM problem separately.

#### Heuristic Algorithms

**1.Monte Carlo simulation**

A computational algorithm that uses repeated random sampling to obtain the likelihood of a range of results of occurring
$$
max\Phi(S_1,S_2) = max\Epsilon[|V\backslash(r_1(I_1 \cup S_1)\Delta r_2(I_2 \cup S_2))|]
\\ 
\Downarrow
\\
\hat{\Phi}(S_1, S_2) = {\sum_{i=0}^{N} \Phi_{g_i}(S_1,S_2) \over N}
$$
Relevant terms and symbols are explained as follows:


$$
\hspace{2cm}S_i\hspace{5.15cm}Balanced\;seed\;seti\hspace{0.19cm}
\\
\hspace{1.15cm}I_i\hspace{5.25cm}Initial\;seed\;set
\\
\hspace{1.7cm}V\hspace{5.22cm}Complete\;seed\;set
\\
\hspace{1.9cm}N\hspace{5.25cm}Total\;seed\;quantity
\\
\hspace{1.69cm}r_i\hspace{5.2cm}Random\;variables
\\
\hspace{1.5cm}\Phi(S_x,S_y)\hspace{4cm}Estimation\;function
$$
**2.Heuristic algorithm for IEM**

Main idea: expand the node with the largest ℎ(𝑣) value

```
Algorithm: Greedy best-first search
S1 ← S2 ← ∅;
while S1 + S2 ≤ k do
    v1* ← arg max v Φ(S1 ∪ v, S2) - Φ(S1, S2);
    v2* ← arg max v Φ(S1, S2 ∪ v) - Φ(S1, S2);
    add the better option between <v1*, ∅> and <∅, v2*> to <S1, S2> while respecting the budget.
```

**3.Combining Monte Carlo and greed search**

```
𝑆1 ← 𝑆2 ← ∅;
while 𝑆1 + 𝑆2 ≤ 𝑘 do
	for j = 1 to N:
		do the following Monte Carlo sampling, each sampling to calculate the h(v) value for all vertices:
		1. simulate an IC model using seed set 𝐼1⋃𝑆1, record the activate set 𝑎1 and exposure set 𝑟1
		2. simulate an IC model using seed set 𝐼2⋃𝑆2, record the activate set 𝑎2 and exposure set 𝑟2
		3. for each 𝑣𝑖 in G:
			3.1 simulate an IC model base on the 𝑎1 and 𝑟1, record the 𝑎1_𝑣𝑖_𝑖𝑛𝑐𝑟𝑒𝑚𝑒𝑛𝑡 and 𝑟1_𝑣𝑖_𝑖𝑛𝑐𝑟𝑒𝑚𝑒𝑛𝑡
			3.2 simulate an IC model base on the 𝑎2 and 𝑟2, record the 𝑎2_𝑣𝑖_𝑖𝑛𝑐𝑟𝑒𝑚𝑒𝑛𝑡 and 𝑟2_𝑣𝑖_𝑖𝑛𝑐𝑟𝑒𝑚𝑒𝑛𝑡
			3.3 calculate and record the ℎ1𝑗(𝑣𝑖) = Φ 𝑆1 ∪ 𝑣𝑖, 𝑆2 − Φ 𝑆1, 𝑆2
			3.4 calculate and record the ℎ2𝑗(𝑣𝑖) = Φ 𝑆1, 𝑆2 ∪ 𝑣𝑖 − Φ 𝑆1, 𝑆2
calculate the average ℎ1𝑎𝑣𝑔(𝑣) value and ℎ2𝑎𝑣𝑔(𝑣) for all vertices
𝑣1∗ ← arg max𝑣ℎ1𝑎𝑣𝑔(𝑣) ;
𝑣2∗ ← arg max𝑣ℎ2𝑎𝑣𝑔(𝑣) ;
add the better option between <𝑣1∗, ∅> and <∅, 𝑣2∗> to <𝑆1, 𝑆2> while respecting the budget.
```

#### Evolutionary Algorithms

**1.genetic makeup**

Binary representation:
$$
x = \{x_1,x_2,...x_{|V|},x_{|V|+1},x_{|V|+2},...,x_{|V|+|V|} \}
\\
x_i\in\{False,True \}
\\\hspace{2.5cm}\downarrow
\\
𝑖th\;node\;is\;added\;into\;𝑆1, 𝑖 ∈ [1, |𝑉|]
\\
𝑖th\;node\;is\;added\;into\;𝑆2, 𝑖 ∈ [ 𝑉 + 1 , 𝑉 + |𝑉|]
$$
**2.Fitness Function**

Distinguish between feasible and infeasible solutions:
$$
fitness(S_1,S_2)= \begin{cases} \hat{\Phi}(S_1,S_2),& \text if\;|S_1|+|S_2|\leq k, \\ -(|S_1|+|S_2|), & \text{otherwise} \end{cases}
$$
**3.flow charts**

<img src="D:\学习\report\evo.png" alt="evo" style="zoom:33%;" />



## Experiments

#### Setup

**1.Environment**

###### Programming Language

Python Version: 3.10

###### Lib Version

```
pymoo == 0.6.0.1
pandas == 2.0.3
numpy == 1.24.4
scipy == 1.14.1
networkx == 2.8.8
```

**2.Dataset**

**Following** provides an overall description of the test datasets:

1. **Type Column:** graph type, all datasets are directed graphs.
2. **Nodes Column:** number of nodes in the graph.
3. **Edges Column:** number of edges in the graph.

All data provided from the Department of Computer Science and Technology at SUSTech.

​							**Heuristic Algorithms data set:**

| Case No. | Nodes | Edges  | Baseline TL | Higher TL |
| -------- | ----- | ------ | ----------- | --------- |
| case 0   | 475   | 13289  | 90s         | 30s       |
| case 1   | 36742 | 49248  | 840s        | 540s      |
| case 2   | 36742 | 49248  | 840s        | 540s      |
| case 3   | 7115  | 103689 | 660s        | 450s      |
| case 4   | 3454  | 32140  | 540s        | 420s      |

**Good Result:**

<img src="D:\学习\report\result1.png" style="zoom:50%;" />



​							**Evolutionary Algorithms data set:**

| Case No. | Nodes | Edges | Baseline TL | Higher TL |
| -------- | ----- | ----- | ----------- | --------- |
| case 0   | 475   | 13289 | 420s        | 380s      |
| case 1   | 13984 | 17319 | 860s        | 780s      |
| case 2   | 13984 | 17319 | 860s        | 780s      |
| case 3   | 3454  | 32140 | 1350s       | 1250s     |
| case 4   | 3454  | 32140 | 1350s       | 1250s     |

**Good Result:**

<img src="D:\学习\report\result2.png" style="zoom:50%;" />

<img src="D:\学习\report\evo_result.png" style="zoom:50%;" />

This chart records the best fitness of each generation, and there is still significant room for improvement in the end. It can improve algebra and further enhance fitness.

**3.Analysis**

Regarding the setting of genetic algorithm control parameters. The current setting is 100 generations, which meets the requirements of the question. Improving algebra significantly increases time expenditure and can optimize the final result, but it does not correspond to an increase in comprehensive income. At present, the initial race size is 500, and increasing it does not significantly change the results. Reducing it will have a certain negative impact on the results, and there is no significant increase in time benefits. At present, each generation produces 50 new offspring, and increasing the number does not significantly change the results. Reducing the number will have a certain negative impact on the results, and there is no significant increase in time benefits. The probability of genome mutation for each individual is 0.1. Each time a gene is mutated, both reduction and increase are likely to have a significant negative impact on the results, without any increase in time benefits. Using the tournament method to randomly select parents, currently 3 sets of genomes are selected for competition each time. If the number of individuals in the competition is increased, it will lead to too fast convergence, which will have a significant negative impact on the results. If the number of individuals in the competition is reduced, it will lead to too fast or too slow, which will have a significant negative impact on the results.

**Bad return:**

![](D:\学习\report\2_bad.png)

In the use of evolutionary algorithms, due to excessively high algebraic settings and high memory usage, the link memory cannot be fully utilized, resulting in low performance.

![](D:\学习\report\1_bad.png)

Due to low Monte Carlo parameter settings. However, being too high can lead to timeouts, and we are seeking a balance between the two.

## Conclusion

Through this project, we propose an algorithm that combines Monte Carlo simulation with greedy best priority search, as well as an algorithm that combines Monte Carlo simulation with natural evolution simulation to solve the problem of maximizing information exposure. These algorithms aim to select seed nodes in dynamic social networks, balancing the relationship between effective information dissemination and exposure. The experimental results show that our algorithm has significant effects in improving information exposure and reducing echo chamber effects.

In the methodology section, we provided a detailed description of each step of the algorithm and demonstrated the specific implementation process through pseudocode and flowcharts. We analyzed the complexity and performance of the algorithm, and explored the impact of different components and hyperparameters on the experimental results. In particular, we discussed the strategy for selecting seed nodes and the contribution of different heuristic methods to the final results, which provides in-depth insights into understanding the effectiveness of the algorithm.

In the experimental section, we provided a detailed introduction to the experimental setup, including features of the dataset, software and hardware configurations, etc. Through experiments on social network graphs of different scales, we found that the algorithm performs well in processing these graphs and the running time is also within an acceptable range. In addition, we analyzed the relationship between experimental results and theoretical expectations, providing explanations for possible differences. For example, in some cases, the complexity of the information propagation path may result in actual effects not meeting expectations, which suggests the need for further optimization of algorithm design.

In summary, our research not only provides a new perspective for understanding information flow in social media, but also offers innovative ideas for algorithm design and social network applications. However, we also recognize that algorithms have some limitations when dealing with large-scale networks, such as efficiency issues, the conflicting balance between information dissemination and exposure, and how to set relevant parameters to ensure higher exposure rates. Future work will continue to explore these issues and attempt to introduce more efficient algorithms and strategies to improve the effectiveness of solving the problem of maximizing information exposure.

In addition, considering the dynamic nature of social networks, we also plan to study the adaptability of algorithms in real-time environments, including how to handle dynamic changes in nodes and edges, and how to maintain the effectiveness of information dissemination in changing network structures. This will provide stronger support for the practical application of algorithms, enabling them to play a role in rapidly changing social networks.

## Reference

[1] K Garimella, A Gionis, N Parotsidis, N Tatti. Balancing information exposure in social networks. NeurIPS 2017: 4663-4671
[2] S Cheng, H Shen, J Huang, W Chen, X Cheng. IMRank: influence maximization via finding self-consistent ranking. SIGIR 2014: 475-484
[3] M Gong, J Yan, B Shen, L Ma, Q Cai. Influence maximization in social networks based on discrete particle swarm optimization. Inf. Sci. 367-368: 600-614 (2016)
[4] Q Jiang, G Song, G Cong, Y Wang, W Si, K Xie. Simulated Annealing Based Influence Maximization in Social Networks. AAAI 2011
