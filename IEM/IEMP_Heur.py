import argparse
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

def load_social_network(file_path):
    global G, vertices
    with open(file_path, 'r') as f:
        G = nx.DiGraph()
        n, m = map(int, f.readline().split())
        vertices = n
        for i in range(m):
            u, v, p1, p2 = map(float, f.readline().split())
            G.add_edge(int(u), int(v), p1=p1, p2=p2)


def load_seed_set(file_path):
    global c1, c2
    with open(file_path, 'r') as f:
        k1, k2 = map(int, f.readline().strip().split())
        c1 = [int(f.readline().strip()) for _ in range(k1)]
        c2 = [int(f.readline().strip()) for _ in range(k2)]


def initial_diffusion_model(initial_seed, type):
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

    return active_nodes, touch_nodes


def expenditure_diffusion_model(activate_seed, occupied_seed, test_seed, type):
    newly_active_nodes = set(test_seed)
    while newly_active_nodes:
        next_newly_active_nodes = set()
        for u in newly_active_nodes:
            if u >= 0:
                for v in G.successors(u):
                    if v not in activate_seed and v not in occupied_seed:
                        occupied_seed.add(v)
                        p = G[u][v]['p1'] if type == 1 else G[u][v]['p2']
                        if np.random.rand() <= p:
                            next_newly_active_nodes.add(v)
        activate_seed.update(next_newly_active_nodes)
        newly_active_nodes = next_newly_active_nodes

    return occupied_seed


def good_reached_nodes(other_touch_nodes, activate_seed, touch_nodes, test_seed, type):
    new_occupied_seed = expenditure_diffusion_model(activate_seed, touch_nodes, test_seed, type)
    satisfied_nodes = len(other_touch_nodes.intersection(new_occupied_seed)) + vertices - len(
        other_touch_nodes.union(new_occupied_seed))
    return satisfied_nodes


def heuristic_algorithm(budget, monte_carlo):
    balanced_seed1 = []
    balanced_seed2 = []
    active_nodes1 = set(c1)
    active_nodes2 = set(c2)

    budget_remaining = budget
    fitness_history = []  # 记录每次迭代的fitness
    while budget_remaining > 0:

        h1_list = np.zeros(len(G.nodes))
        h2_list = np.zeros(len(G.nodes))

        for _ in range(monte_carlo):

            new_active_nodes1, touch_nodes1 = initial_diffusion_model(active_nodes1, 1)
            new_active_nodes2, touch_nodes2 = initial_diffusion_model(active_nodes2, 2)

            satisfied_nodes = len(touch_nodes1.intersection(touch_nodes2)) + vertices - len(
                touch_nodes1.union(touch_nodes2))

            for node in range(vertices):

                if node not in new_active_nodes1:
                    o_touch_nodes1 = set(touch_nodes1)
                    total_activate_seed1 = set(new_active_nodes1)
                    expected1 = good_reached_nodes(touch_nodes2, total_activate_seed1, o_touch_nodes1, [node],
                                                   1)
                    h1 = expected1 - satisfied_nodes
                    h1_list[node] += h1 / monte_carlo

                if node not in new_active_nodes2:
                    o_touch_nodes2 = set(touch_nodes2)
                    total_activate_seed2 = set(new_active_nodes2)
                    expected2 = good_reached_nodes(touch_nodes1, total_activate_seed2, o_touch_nodes2, [node],
                                                   2)
                    h2 = expected2 - satisfied_nodes
                    h2_list[node] += h2 / monte_carlo

        h1_max_avg = np.argmax(h1_list)
        h2_max_avg = np.argmax(h2_list)

        if h1_list[h1_max_avg] > h2_list[h2_max_avg]:
            active_nodes1.add(h1_max_avg)
            balanced_seed1.append(h1_max_avg)
        else:
            active_nodes2.add(h2_max_avg)
            balanced_seed2.append(h2_max_avg)

        budget_remaining -= 1

    # 可视化fitness变化
    plt.plot(fitness_history)
    plt.title('Fitness Over Iterations')
    plt.xlabel('Iteration')
    plt.ylabel('Fitness')
    plt.grid()
    plt.savefig('fitness_plot.png')  # 保存图像
    plt.show()  # 显示图像

    return balanced_seed1, balanced_seed2


G = nx.DiGraph()
vertices = 0
c1 = []
c2 = []

# 直接使用绝对路径
SOCIAL_NETWORK_PATH = 'D:/学习/第五学期/artificial_intelligence/project/Testcase/Heuristic/map2/dataset2'
INITIAL_SEED_SET_PATH = 'D:/学习/第五学期/artificial_intelligence/project/Testcase/Heuristic/map2/seed'
BALANCED_SEED_SET_PATH = 'D:/学习/第五学期/artificial_intelligence/project/Testcase/Heuristic/balanced_set.txt'

def main():
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-n', required=True, help='Path to the social network file')
    # parser.add_argument('-i', required=True, help='Path to the initial seed set file')
    # parser.add_argument('-b', required=True, help='Path to the balanced seed set file')
    # parser.add_argument('-k', type=int, required=True, help='Budget')
    #
    # args = parser.parse_args()
    # load_social_network(args.n)
    # load_seed_set(args.i)
    # budget = args.k
    # 直接使用绝对路径
    load_social_network(SOCIAL_NETWORK_PATH)
    load_seed_set(INITIAL_SEED_SET_PATH)
    budget = 14  # 设置预算，或根据需求修改

    balanced_seed1, balanced_seed2 = heuristic_algorithm(budget, 2)

    with open(BALANCED_SEED_SET_PATH, 'w') as f:
        f.write(f"{len(balanced_seed1)} {len(balanced_seed2)}\n")
        for node in balanced_seed1:
            f.write(f"{node}\n")
        for node in balanced_seed2:
            f.write(f"{node}\n")


if __name__ == "__main__":
    main()
