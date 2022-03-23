# Course: CS261 - Data Structures
# Author: Timur Guner
# Assignment: 6
# Description: The portion of this assignment deals with implementation of directed graphs using adjacency matrix

import heapq
from collections import deque

class DirectedGraph:
    """
    Class to implement directed weighted graph
    - duplicate edges not allowed
    - loops not allowed
    - only positive edge weights
    - vertex names are integers
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency matrix
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.v_count = 0
        self.adj_matrix = []

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            v_count = 0
            for u, v, _ in start_edges:
                v_count = max(v_count, u, v)
            for _ in range(v_count + 1):
                self.add_vertex()
            for u, v, weight in start_edges:
                self.add_edge(u, v, weight)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if self.v_count == 0:
            return 'EMPTY GRAPH\n'
        out = '   |'
        out += ' '.join(['{:2}'.format(i) for i in range(self.v_count)]) + '\n'
        out += '-' * (self.v_count * 3 + 3) + '\n'
        for i in range(self.v_count):
            row = self.adj_matrix[i]
            out += '{:2} |'.format(i)
            out += ' '.join(['{:2}'.format(w) for w in row]) + '\n'
        out = f"GRAPH ({self.v_count} vertices):\n{out}"
        return out

    # ------------------------------ Helper Functions ---------------------------------------- #

    def cycle_helper(self, v_vertex, v_stack):
        """
        This is a helper function that helps the has_cycle function. This is done using a modified version of the DFS
        which uses a stack to determine if a vertex was previous visited. Its not a true stack as this method does
        search through it like a list but only push and pop are used to maintain it.
        """

        # first append the visited vertex to the v_stack
        v_stack.append(v_vertex)

        # for the current vertex, iterate through DFS by examining its adjacent nodes first
        for v in range(0, self.v_count):

            # only proceed if the current vertex can connect to another vertex
            if self.adj_matrix[v_vertex][v] != 0:

                # if the vertex was already in the stack, then we have a cycle
                if v in v_stack:
                    return True

                # call the cycle_helper function and return true if it returns true
                cycle = self.cycle_helper(v, v_stack)
                if cycle == True:
                    return True

        # pop the top of the v_stack, so so the comparisons don't produce an incorrect cycle
        v_stack.pop()

        # return false if iterations and recursions end with no detected cycle
        return False

    # -------------------------------- Assignment Functions ---------------------------------- #

    def add_vertex(self) -> int:
        """
        Add new vertex to the graph
        """

        # us a blank list to add a new row with the current amount of vertices + 1
        u_list = []
        for v in range(0,self.v_count+1):
            u_list.append(0)

        # append an additional column to the existing matrix rows
        for u in range(0,self.v_count):
            self.adj_matrix[u].append(0)

        # add the new vertex rows to the matrix
        self.adj_matrix.append(u_list)

        # increment the v_count
        self.v_count+=1

        return self.v_count

    def add_edge(self, src: int, dst: int, weight=1) -> None:
        """
        Add edge to the graph
        """

        # if the src vertex is not in matrix, then do nothing
        if src >= self.v_count or src < 0 or type(src) != int:
            return

        # if dst vertex is not in the matrix, then do nothing
        if dst >= self.v_count or dst < 0 or type(src) != int:
            return

        # if weight is not positive
        if weight < 1 or type(weight) != int:
            return

        # if src and dst are the same, do nothing
        if src == dst:
            return

        # add edge to graph
        self.adj_matrix[src][dst] = weight

        return

    def remove_edge(self, src: int, dst: int) -> None:
        """
        Remove edge from the graph
        """

        # if the src vertex is not in matrix, then do nothing
        if src >= self.v_count or src < 0 or type(src) != int:
            return

        # if dst vertex is not in the matrix, then do nothing
        if dst >= self.v_count or dst < 0 or type(src) != int:
            return

        # if no edge exists, do nothing
        if self.adj_matrix[src][dst] == 0:
            return

        # remove edge by setting weight to 0
        self.adj_matrix[src][dst] = 0

        return

    def get_vertices(self) -> []:
        """
        returns a list of vertices from the graph
        """

        # empty list that will be used to store thge vertices
        v_list = []

        # assign the vertices to the list
        for u in range(0,self.v_count):
            v_list.append(u)

        # return the list
        return v_list

    def get_edges(self) -> []:
        """
        Return list of edges in the graph (any order)
        """

        # create an empty of edges
        edges = []

        # append the vertex, its destination, and weight as a tuple to the edges
        for v in range(0,self.v_count):
            for u in range(0,self.v_count):
                if self.adj_matrix[v][u] != 0:
                    edges.append((v,u,self.adj_matrix[v][u]))

        # return edges
        return edges

    def is_valid_path(self, path: []) -> bool:
        """
        Return true if provided path is valid, False otherwise
        """

        # if path is empty, then return true
        if not path:
            return True

        # if path is one vertex and valid, return true else false
        if len(path) == 1:
            if path[0] >= 0 and path[0] < self.v_count:
                return True
            else:
                return False

        # iterate through path and determine if the path is valid, and if at any point in the iteration there is no edge
        # then return false
        for v in range(0, len(path)-1):
            if path[v] >= self.v_count or path[v] < 0:
                return False
            elif path[v+1] >= self.v_count or path[v+1] < 0:
                return False
            elif self.adj_matrix[path[v]][path[v+1]] == 0:
                return False
            else:
                pass

        # return true is the iteration passes
        return True

    def dfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during DFS search
        Vertices are picked in alphabetical order
        """

        # initialize blank lists dfs and stack
        dfs_list = []
        dfs_stack = []

        # if the starting vertex is not is list return dfs_list
        if v_start >= self.v_count or v_start < 0 or type(v_start) != int:
            return dfs_list

        # append v_start to the list
        dfs_list.append(v_start)

        # if v_end is the v_start then return dfs_list because there will be no other vertices to search
        if v_start == v_end:
            return dfs_list

        # once v_start is appended to dfs_list, pull the edges from graph and push them to the stack in reverse
        # alphabetical order
        u_list = []
        for u in range(0, self.v_count):
            if self.adj_matrix[v_start][u] != 0:
                u_list.append(u)
        u_list.sort(reverse=True)
        for v in range(0, len(u_list)):
            dfs_stack.append(u_list[v])

        # the while loop will pop vertices from the stack until the stack is empty
        while len(dfs_stack) > 0:

            # pop the top of the stack
            v = dfs_stack.pop()

            # if v is not already in the dfs list then do the following
            if v not in dfs_list:

                # append v to the dfs list and return the dfs if v is equal to v_end
                dfs_list.append(v)
                if v == v_end:
                    return dfs_list

                # pull the vertices that have edges with v and push them to the stack in reverse alphabetical order
                u_list = []
                for u in range(0,self.v_count):
                    if self.adj_matrix[v][u] != 0:
                        u_list.append(u)
                u_list.sort(reverse=True)
                for v in range(0,len(u_list)):
                    dfs_stack.append(u_list[v])

        # return dfs_list
        return dfs_list

    def bfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during BFS search
        Vertices are picked in alphabetical order
        """

        # initialize blank lists bfs and queue
        bfs_list = []
        bfs_queue = []

        # if the starting vertex is not is list return bfs_list
        if v_start >= self.v_count or v_start < 0 or type(v_start) != int:
            return bfs_list

        # append v_start to the list
        bfs_list.append(v_start)

        # if v_end is the v_start then return dfs_list because there will be no other vertices to search
        if v_start == v_end:
            return bfs_list

        # once v_start is appended to bfs_list, pull the edges from graph and enqueues them to the queue in alphabetical
        # order
        for u in range(0, self.v_count):
            if self.adj_matrix[v_start][u] != 0:
                bfs_queue.append(u)

        # while queue is not empty, do the following
        while len(bfs_queue) > 0:

            # dequeue the queue
            v = bfs_queue.pop(0)

            # if v is not already in the bfs list then do the following
            if v not in bfs_list:

                # append v to the bfs list and return the bfs if v is equal to v_end
                bfs_list.append(v)
                if v == v_end:
                    return bfs_list

                # enqueue u (adjacent vertices) to the queue
                for u in range(0,self.v_count):
                    if self.adj_matrix[v][u]:
                        bfs_queue.append(u)

        # return bfs_list
        return bfs_list

    def has_cycle(self):
        """
        Return True if graph contains a cycle, False otherwise
        """

        # iterate through each vertex to find a cycle and return True if found, else return False
        for v in range(0, self.v_count):

            # declare an empty stack to store visited nodes
            visited_stack = []

            # call the cycle helper to determine if the current current is in a cycle and return true
            cycle = self.cycle_helper(v,visited_stack)
            if cycle == True:
                return True

        return False

    def dijkstra(self, src: int) -> []:
        """
        Returns a list of shortest paths to all vertices
        """

        # create a list to store shortest path and set everything to inf, then set the index matching src to 0, and
        # finally declare a dictionary with src and distance 0 appended to it
        dijkstra = [float('inf')] * self.v_count
        dijkstra[src] = 0
        dist_pque = {src: 0}

        # while dist_pque is not empty
        while dist_pque:

            # set the short_weight to 0
            s = float('inf')
            weight = float('inf')

            # iterate through the dist_pque dictionary finding the closest distance, delete it from the dictionary, and
            # save the key (vertex) in short_weight
            for v in dist_pque:
                if dist_pque[v] < weight:
                    s = v
                    weight = dist_pque[v]
            del dist_pque[s]

            # iterate through the row index 'short_weight' to pull all edges
            for v in range(0, self.v_count):

                # if distance is 0 then there is no directed connection in the adjacency matrix
                if self.adj_matrix[s][v] != 0:

                    # if the distance of the vertex (v) is greater than the distance of vertex s + distance in the
                    # adjacency matrix, then update dijkstra with the new weight at index v and add v plus its weight to
                    # the dist_pque
                    # https://en.wikipedia.org/wiki/Dijkstra's_algorithm
                    if dijkstra[s] + self.adj_matrix[s][v] < dijkstra[v]:
                        dijkstra[v] = dijkstra[s] + self.adj_matrix[s][v]
                        dist_pque[v] = dijkstra[v]

        # return the dijkstra list
        return dijkstra

if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = DirectedGraph()
    print(g)
    for _ in range(5):
        g.add_vertex()
    print(g)

    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    for src, dst, weight in edges:
        g.add_edge(src, dst, weight)
    print(g)


    print("\nPDF - method get_edges() example 1")
    print("----------------------------------")
    g = DirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method get_edges() example 1")
    print("----------------------------------")
    g = DirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    test_cases = [[0, 1, 4, 3], [1, 3, 2, 1], [0, 4], [4, 0], [], [2]]
    for path in test_cases:
        print(path, g.is_valid_path(path))


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = [(0, 1, 18), (0,3,13),(0,12,17),
             (2, 0, 1), (2, 6, 16),
             (3, 9, 1),
             (4, 9, 15),
             (6, 7, 7), (6, 9, 18),
             (7, 4, 9),
             (8, 9, 6),
             (9, 10, 3),
             (12, 4, 4),
             ]
    g = DirectedGraph(edges)
    print(g)
    print(g.get_edges())
    print(g.has_cycle())

    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    edges_to_remove = [(3, 1), (4, 0), (3, 2)]
    for src, dst in edges_to_remove:
        g.remove_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')
    edges_to_add = [(4, 3), (2, 3), (1, 3), (4, 0, 99)]
    for src, dst, *weight in edges_to_add:
        g.add_edge(src, dst, *weight)
        print(g.get_edges(), g.has_cycle(), sep='\n')
    print('\n', g)


    print("\nPDF - dijkstra() example 1")
    print("--------------------------")
    edges = [(0, 1, -10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
    g.remove_edge(4, 3)
    print('\n', g)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
