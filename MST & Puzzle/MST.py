# Author: Timur Guner
# Class: CS325
# Assignment 8: MST

import heapq

def Prims(G):
    # create an empty set to store the pq of the minimum spanning tree
    mst = set()

    # creating a starting vertex by selecting the first key as cur_node
    cur_node = list(G.keys())[0]

    # mark the the cur_node as visited
    visited = set([cur_node])

    # blank priority queue
    pq = []

    # heap push tuples of cost, cur_node, node_next to the pq
    for node_next, cost in G[cur_node].items():
        heapq.heappush(pq, (cost, cur_node, node_next))

    # iterate while visited is less than the number of vertices
    while len(visited) < len(G):

        # heappop the cost of the cost, cur_node, and node_next
        cost, cur_node, node_next = heapq.heappop(pq)

        # check if the node_next (the neighbor of cur_node) has not already been processed, else skipp
        if node_next not in visited:

            # add node_next to visited set and tuple of cur_node, node_next, and cost to mst
            visited.add(node_next)
            mst.add((cur_node, node_next, cost))

            # iterate through the node_next dictionary of items and push the next_nodes neighbor data to the heap
            for node_next_next, cost in G[node_next].items():
                heapq.heappush(pq, (cost, node_next, node_next_next))

    return mst

if __name__ == '__main__':

    G = {
        'A': {'C': 1, 'D': 6},
        'B': {'D': 15},
        'C': {'A': 1, 'D': 4},
        'D': {'A': 6, 'B': 15, 'C': 4, 'E': 20},
        'E': {'D': 20}
    }

    # {('A', 'B', 2), ('C', 'E', 1), ('B', 'D', 3), ('B', 'C', 1)}

    print(Prims(G))