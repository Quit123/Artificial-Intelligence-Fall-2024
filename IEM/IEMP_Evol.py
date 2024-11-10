import argparse
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


def load_social_network(file_path):
    with open(file_path, 'r') as f:
        G = nx.DiGraph()
        n, m = map(int, f.readline().split())
        vertices = n
        for i in range(m):
            u, v, p1, p2 = map(float, f.readline().split())
            G.add_edge(int(u), int(v), p1=p1, p2=p2)
    return G, vertices


def load_seed_set(file_path):
    global ini_fa
    global ini_ma
    with open(file_path, 'r') as f:
        k1, k2 = map(int, f.readline().strip().split())
        c1 = [int(f.readline().strip()) for _ in range(k1)]
        c2 = [int(f.readline().strip()) for _ in range(k2)]
        ini_fa = np.array(c1)
        ini_ma = np.array(c2)


def diffusion_model(initial_seed, type):
    active_nodes = set(initial_seed)
    newly_active_nodes = set(active_nodes)
    touch_nodes = set(active_nodes)

    while newly_active_nodes:
        next_newly_active_nodes = set()
        for u in newly_active_nodes:
            if u >= 0:
                for v in G.successors(u):
                    if v not in active_nodes and v not in touch_nodes:
                        touch_nodes.add(v)
                        p = G[u][v]['p1'] if type == 1 else G[u][v]['p2']
                        if np.random.rand() <= p:
                            next_newly_active_nodes.add(v)
        active_nodes.update(next_newly_active_nodes)
        newly_active_nodes = next_newly_active_nodes

    return touch_nodes


def gene_diffusion(gene):
    h_gene = gene[:vertices]
    e_gene = gene[vertices:]
    h_gene[ini_fa] = 1
    e_gene[ini_ma] = 1
    father_gene = np.where(h_gene == 1)[0]
    mother_gene = np.where(e_gene == 1)[0]
    satisfied_nodes = 0
    for _ in range(10):
        touch_nodes_f = diffusion_model(father_gene, 1)
        touch_nodes_m = diffusion_model(mother_gene, 2)
        satisfied_nodes += len(touch_nodes_f.intersection(touch_nodes_m)) + vertices - len(
            touch_nodes_f.union(touch_nodes_m))
    satisfied_nodes = satisfied_nodes / 10
    return satisfied_nodes


def Crossover(parents):
    children = []
    np.random.shuffle(parents)
    for i in range(int(len(parents) / 2)):
        father = parents[2 * i]
        mother = parents[2 * i + 1]

        crossover_point1, crossover_point2, crossover_point3, crossover_point4 = np.random.choice(
            range(0, len(father) - 1), 4, replace=False)
        crossover_point1, crossover_point2, crossover_point3, crossover_point4 = np.sort(
            [crossover_point1, crossover_point2, crossover_point3, crossover_point4])

        child1 = np.concatenate(
            (father[:crossover_point1], mother[crossover_point1:crossover_point2],
             father[crossover_point2:crossover_point3], mother[crossover_point3:crossover_point4],
             father[crossover_point4:]))
        child2 = np.concatenate(
            (mother[:crossover_point1], father[crossover_point1:crossover_point2],
             mother[crossover_point2:crossover_point3], father[crossover_point3:crossover_point4],
             mother[crossover_point4:]))

        children.append(child1)
        children.append(child2)

    return children


def Mutation(children, mutation_rate):
    for child in children:
        if np.random.random() <= mutation_rate:
            mutate_point = np.random.randint(0, 2 * vertices)
            child[mutate_point] = 1 - child[mutate_point]
    return children


def Genetic_crossover_mutation(selected_indices, gene_bank, mutation_rate):
    parents = []
    for index in selected_indices:
        parents.append(gene_bank[index])
    children = Crossover(parents)
    children = Mutation(children, mutation_rate=mutation_rate)

    return children


def check_best_gene(checked_gene, fitness, max_reached_node, gene_set):
    checked_gene_back = np.copy(checked_gene)
    satisfied_nodes = gene_diffusion(checked_gene_back)
    fitness.append(satisfied_nodes)
    if max_reached_node < satisfied_nodes:
        max_reached_node = satisfied_nodes
        gene_set = checked_gene
    return max_reached_node, gene_set


def GeneticAlgorithm(generation, initial_size, offspring_size, competitor_size, mutation_rate):
    global fitness_history
    fitness_history = []  # 用于记录每代的适应度
    # 初始化
    gene_set = []
    max_reached_node = -1
    gene_bank = []
    fitness = []
    ini_set = np.concatenate((ini_fa, ini_ma))
    vertices_array = np.arange(vertices)
    zero_indices = np.setdiff1d(vertices_array, ini_set)
    for i in range(initial_size):
        gene_back = np.zeros(vertices * 2)
        selected_indices = np.random.choice(zero_indices, size=budget, replace=False)
        gene_back[selected_indices] = 1
        max_reached_node, gene_set = check_best_gene(gene_back, fitness, max_reached_node, gene_set)
        gene_bank.append(gene_back)

    # 遗传开始
    for i in range(generation):
        selected_indices = tournament_selection(fitness, offspring_size, competitor_size)

        children = Genetic_crossover_mutation(selected_indices, gene_bank, mutation_rate)

        for child in children:
            check = 0
            for j in child:
                if j == 1:
                    check += 1
            if check <= budget:
                max_reached_node, gene_set = check_best_gene(child, fitness, max_reached_node, gene_set)
                gene_bank.append(child)
            else:
                gene_bank.append(child)
                p = np.random.uniform(0.94, 0.96)
                fitness.append(max_reached_node * p)
        fitness_history.append(np.mean(fitness))  # 记录每代的适应度
        if len(gene_bank) > 1000:
            prune_gene_bank(gene_bank, fitness, remove_size=offspring_size)
    return gene_set


G = nx.DiGraph()
vertices = 0
budget = 0
ini_fa = []
ini_ma = []


def tournament_selection(fitness, offspring_size, competitor_size):
    index = []
    for i in range(offspring_size):
        competitors = np.random.choice(len(fitness), size=competitor_size, replace=False)
        competitor_fitness = np.array(fitness)[competitors]
        sel = np.argmax(competitor_fitness)
        index.append(competitors[sel])
    return index


def prune_gene_bank(gene_bank, fitness, remove_size=50):
    if len(fitness) > remove_size:
        worst_indices = np.argsort(fitness)[:remove_size]
        worst_set = set(worst_indices)
        gene_bank[:] = [gene_bank[i] for i in range(len(gene_bank)) if i not in worst_set]
        fitness[:] = [fitness[i] for i in range(len(fitness)) if i not in worst_set]


def plot_fitness_over_generations(fitness_history):
    plt.figure(figsize=(10, 6))
    plt.plot(fitness_history, marker='o')
    plt.title('Fitness over Generations')
    plt.xlabel('Generation')
    plt.ylabel('Average Fitness')
    plt.grid()
    plt.tight_layout()
    plt.show()


def plot_final_result(gene_set):
    h_gene = gene_set[:vertices]
    e_gene = gene_set[vertices:]

    plt.figure(figsize=(10, 6))
    plt.scatter(np.where(h_gene == 1)[0], np.zeros(np.sum(h_gene)), color='blue', label='Seed 1 Nodes')
    plt.scatter(np.where(e_gene == 1)[0], np.ones(np.sum(e_gene)), color='orange', label='Seed 2 Nodes')
    plt.title('Final Seed Sets')
    plt.yticks([0, 1], ['Seed 1', 'Seed 2'])
    plt.xlabel('Node Index')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()


# 直接使用绝对路径
SOCIAL_NETWORK_PATH = 'D:/学习/第五学期/artificial_intelligence/project/Testcase/Evolutionary/map2/dataset2'
INITIAL_SEED_SET_PATH = 'D:/学习/第五学期/artificial_intelligence/project/Testcase/Evolutionary/map2/seed'
BALANCED_SEED_SET_PATH = 'D:/学习/第五学期/artificial_intelligence/project/Testcase/Evolutionary/balanced_set.txt'


def main():
    global budget, G, vertices
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-n', required=True, help='Path to the social network file')
    # parser.add_argument('-i', required=True, help='Path to the initial seed set file')
    # parser.add_argument('-b', required=True, help='Path to the balanced seed set file')
    # parser.add_argument('-k', type=int, required=True, help='Budget')
    # args = parser.parse_args()
    # G, vertices = load_social_network(args.n)
    # load_seed_set(args.i)
    # budget = args.k
    G, vertices = load_social_network(SOCIAL_NETWORK_PATH)
    load_seed_set(INITIAL_SEED_SET_PATH)
    budget = 14  # 设置预算，或根据需求修改
    gene_set = GeneticAlgorithm(100, 500, 50, 3, 0.1)
    # gene_set = GeneticAlgorithm(100, 500, 50, 3, 0.05)

    # 生成图像
    plot_fitness_over_generations(fitness_history)
    plot_final_result(gene_set)

    h_gene = gene_set[:vertices]
    e_gene = gene_set[vertices:]
    balanced_seed1 = np.where(h_gene == 1)[0]
    balanced_seed2 = np.where(e_gene == 1)[0]

    with open(BALANCED_SEED_SET_PATH, 'w') as f:
        f.write(f"{len(balanced_seed1)} {len(balanced_seed2)}\n")
        for node in balanced_seed1:
            f.write(f"{node}\n")
        for node in balanced_seed2:
            f.write(f"{node}\n")


if __name__ == "__main__":
    main()