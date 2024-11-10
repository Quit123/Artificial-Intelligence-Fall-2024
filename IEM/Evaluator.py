import argparse
import networkx as nx
import numpy as np


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
    with open(file_path, 'r') as f:
        k1, k2 = map(int, f.readline().strip().split())
        c1 = [int(f.readline().strip()) for _ in range(k1)]
        c2 = [int(f.readline().strip()) for _ in range(k2)]
    return c1, c2


def diffusion_model(G, initial_seed, balanced_seeds, type):
    active_nodes = set(initial_seed) | set(balanced_seeds)
    newly_active_nodes = active_nodes.copy()
    touch_nodes = active_nodes.copy()

    while newly_active_nodes:
        next_newly_active_nodes = set()
        for u in newly_active_nodes:
            for v in G.neighbors(u):
                touch_nodes.add(v)
                if v not in active_nodes:
                    p = G[u][v]['p1'] if type == 1 else G[u][v]['p2']
                    if np.random.rand() <= p:
                        next_newly_active_nodes.add(v)
        active_nodes.update(next_newly_active_nodes)
        newly_active_nodes = next_newly_active_nodes

    return touch_nodes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', required=True, help='Path to the social network file')
    parser.add_argument('-i', required=True, help='Path to the initial seed set file')
    parser.add_argument('-b', required=True, help='Path to the balanced seed set file')
    parser.add_argument('-k', type=int, required=True, help='Budget')
    parser.add_argument('-o', required=True, help='Path for objective value output')

    args = parser.parse_args()

    G, vertices = load_social_network(args.n)
    c1, c2 = load_seed_set(args.i)
    balanced_seed1, balanced_seed2 = load_seed_set(args.b)

    n = 500
    reached_nodes = 0
    for i in range(n):
        reached_node_1 = diffusion_model(G, c1, balanced_seed1, 1)
        reached_node_2 = diffusion_model(G, c2, balanced_seed2, 2)
        reached_nodes += len(reached_node_1.intersection(reached_node_2)) + vertices - len(
            reached_node_1.union(reached_node_2))

    reached_nodes = reached_nodes / n

    with open(args.o, 'w') as f:
        f.write(str(reached_nodes))


if __name__ == "__main__":
    main()
