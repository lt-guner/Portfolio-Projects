# Course: CS261 - Data Structures
# Author: Timur Guner
# Assignment: 6
# Description: This portion of the assignment implements an undirected graph using an adjacency list

import heapq
from collections import deque

class UndirectedGraph:
    """
    Class to implement undirected graph
    - duplicate edges not allowed
    - loops not allowed
    - no edge weights
    - vertex names are strings
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.adj_list = dict()

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            for u, v in start_edges:
                self.add_edge(u, v)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = [f'{v}: {self.adj_list[v]}' for v in self.adj_list]
        out = '\n  '.join(out)
        if len(out) < 70:
            out = out.replace('\n  ', ', ')
            return f'GRAPH: {{{out}}}'
        return f'GRAPH: {{\n  {out}}}'

    # ------------------------------ Helper Functions ---------------------------------------- #

    def cycle_helper(self, visited_list, visited_vertex, visited_parent):
        """
        This is a helper function that helps the has_cycle function. This is done using a modified version of the DFS
        which also keeps track of the parent vertex as to prevent a the visited vertex from associating the parent
        vertex as a cycle.
        """

        # first append the visited vertex to the visited_list
        visited_list.append(visited_vertex)

        # iterate through the list of adjacent vertexes attached to the visited vertex
        for u in self.adj_list[visited_vertex]:

            # call the cycle_helper if the node was not already visited
            if u not in visited_list:
                cycle = self.cycle_helper(visited_list,u,visited_vertex)
                if cycle == True:
                    return True

            # return true if the adjacent vertex is already visited and is not the parent of the current vertex then we
            # have a cycle
            elif u != visited_parent:
                return True

        # return false if iterations and recursions end with no detected cycle
        return False

    # ---------------------------- Assignment Functions -------------------------------------- #

    def add_vertex(self, v: str) -> None:
        """
        Add new vertex to the graph
        """

        # a for loop iterates through v and adds the key with a blank list if it does not exist
        for letter in v:
            if letter in self.adj_list:
                pass
            else:
                self.adj_list[letter] = []

        return
        
    def add_edge(self, u: str, v: str) -> None:
        """
        Add edge to the graph
        """

        # if the vertices match, do nothing
        if u == v:
            return

        # note: below code does contain extra if statements that may not be necessary but are in place just for extra
        # safety precautions

        # if the vertices are not in the list then add them, and the edges connections to the list
        if u not in self.adj_list:
            self.add_vertex(u)
            self.adj_list[u] = [v]

        if v not in self.adj_list:
            self.add_vertex(v)
            self.adj_list[v] = [u]

        # else add the edges to the list keys list if the edges do not exist yet
        # adds v to u's list
        list_u = self.adj_list[u]
        if v not in list_u:
            list_u.append(v)
            list_u.sort()
        else:
            pass

        # adds u to v's list
        list_v = self.adj_list[v]
        if u not in list_v:
            list_v.append(u)
            list_v.sort()
        else:
            pass

        return

    def remove_edge(self, v: str, u: str) -> None:
        """
        Remove edge from the graph
        """

        # remove u from v's list if u exists
        if v in self.adj_list:
            list_v = self.adj_list[v]
            if u in list_v:
                list_v.remove(u)

        # remove v from u's list if v exists
        if u in self.adj_list:
            list_u = self.adj_list[u]
            if v in list_u:
                list_u.remove(v)

        return

    def remove_vertex(self, v: str) -> None:
        """
        Remove vertex and all connected edges
        """

        # The nested ifs and for loop, first saves the list from the vertex being deleted and the vertex is delete.
        # After the deletion of the vertex, list is iterated through to find the edges that were previously attached to
        # to deleted vertex and removes them
        if v in self.adj_list:
            d_list = self.adj_list[v]
            del self.adj_list[v]
            for u in d_list:
                if u in self.adj_list:
                    x_list = self.adj_list[u]
                    x_list.remove(v)

        return

    def get_vertices(self) -> []:
        """
        returns a list of vertices from the graph
        """

        # declare a blank list of vertices
        vertices = []

        # for every vertex (key) append it to vertices
        for v in self.adj_list:
            vertices.append(v)

        # return vertices
        return vertices

    def get_edges(self) -> []:
        """
        Return list of edges in the graph (any order)
        """

        # declare a blank list of edges
        edges = []

        # the nested for loop and single if statement iterate through each vertex (key) and edges (key's list) and adds
        # the edges as tuples to the edges list
        for v in self.adj_list:
            for u in self.adj_list[v]:
                edge_tuple = (v, u)
                edge_tuple_reverse = (u, v)
                if edge_tuple not in edges and edge_tuple_reverse not in edges:
                    edges.append(edge_tuple)

        # return list of edges
        return edges

    def is_valid_path(self, path: []) -> bool:
        """
        Return true if provided path is valid, False otherwise
        """

        # if path is empty, then true
        if not path:
            return True

        # if path one vertex is passed, then true if vertex exists else return false
        if len(path) == 1:
            if path[0] in self.adj_list:
                return True
            else:
                return False

        # The for loop iterates through path (list) and checks to see if the vertex exists and if its connected to the
        # next element. Returns false an invalid edge or vertex was passed
        for v in range(0, len(path)-1):
            if path[v] not in self.adj_list:
                return False
            elif path[v+1] not in self.adj_list[path[v]]:
                return False
            else:
                pass

        # returns true if no issues in the for loop above
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
        if v_start not in self.adj_list:
            return dfs_list

        # append v_start to the list
        dfs_list.append(v_start)

        # if v_end is the v_start then return dfs_list because there will be no other vertices to search
        if v_start == v_end:
            return dfs_list

        # once v_start is appended to dfs_list, pull the edges from graph and push them to the stack in reverse
        # alphabetical order
        u_list = []
        for u in self.adj_list[v_start]:
            u_list.append(u)
        u_list.sort(reverse=True)
        for v in u_list:
            dfs_stack.append(v)

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
                for u in self.adj_list[v]:
                    u_list.append(u)
                u_list.sort(reverse=True)
                for v in u_list:
                    dfs_stack.append(v)

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
        if v_start not in self.adj_list:
            return bfs_list

        # append v_start to the list
        bfs_list.append(v_start)

        # if v_end is  v_start then return bfs_list because there will be no other vertices to search
        if v_start == v_end:
            return bfs_list

        # once v_start is appended to bfs_list, pull the edges from graph and enqueues them to the queue in alphabetical
        # order
        for u in self.adj_list[v_start]:
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
                for u in self.adj_list[v]:
                    bfs_queue.append(u)

        # return bfs_list
        return bfs_list

    def count_connected_components(self):
        """
        Return number of connected componets in the graph
        """

        # create a blank connected components list
        cc_list = []

        # we pull each individual vertex (key) from the graph
        for v in self.adj_list:

            # set in_cc to false and iterate through each sublist of cc_list to see if it was pulled part of an existing
            # DFS search
            in_cc = False
            for i in range(0,len(cc_list)):
                if v in cc_list[i]:
                    in_cc = True
                    break

            # if it was not part of a previous dfs search then it is a new connected component and append the new dfs
            # search to the connected components
            if in_cc == False:
                t_list = self.dfs(v)
                cc_list.append(t_list)

        # return the length of the cc_list which is the number of connected unique dfs searches
        return len(cc_list)

    def has_cycle(self):
        """
        Return True if graph contains a cycle, False otherwise
        """

        # iterate through each vertex of the graph to pass to the cycle_helper function
        for v in self.adj_list:

            # create an empty list to store visited vertexes for each used in cycle_helper
            visited_list = []

            # if vertex has no adjacent vertices, then do nothing
            if not self.adj_list[v]:
                pass

            # append the v to the visited_list and send v and its first adjacent vertex to the cycle_helper
            else:
                visited_list.append(v)
                visited = self.adj_list[v]
                cycle = self.cycle_helper(visited_list,visited[0],v)

                # if cycle_helper returned true then return true
                if cycle == True:
                    return True

        # return false if a cycle exists between no vertex dfs calls
        return False

if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = UndirectedGraph()
    print(g)

    for v in 'ABCDE':
        g.add_vertex(v)
    print(g)

    g.add_vertex('A')
    print(g)

    for u, v in ['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE', ('B', 'C')]:
        g.add_edge(u, v)
    print(g)


    print("\nPDF - method remove_edge() / remove_vertex example 1")
    print("----------------------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE','DE'])
    g.remove_vertex('DOES NOT EXIST')
    g.remove_edge('A', 'B')
    g.remove_edge('X', 'B')
    print(g)
    g.remove_vertex('D')
    print(g)


    print("\nPDF - method get_vertices() / get_edges() example 1")
    print("---------------------------------------------------")
    g = UndirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE'])
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    test_cases = ['ABC', 'ADE', 'ECABDCBE', 'ACDECB', '', 'D', 'Z']
    for path in test_cases:
        print(list(path), g.is_valid_path(list(path)))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = ['AB', 'BC', 'CD', 'DE', 'DG', 'FG', 'FH', 'HI', 'GI', 'IJ']
    g = UndirectedGraph(edges)
    test_cases = 'A'
    for case in test_cases:
        print(f'{case} DFS:{g.dfs(case)} BFS:{g.bfs(case)}')
    print('-----')
    for i in range(1, len(test_cases)):
        v1, v2 = test_cases[i], test_cases[-1 - i]
        print(f'{v1}-{v2} DFS:{g.dfs(v1, v2)} BFS:{g.bfs(v1, v2)}')


    print("\nPDF - method count_connected_components() example 1")
    print("---------------------------------------------------")
    edges = ['AB', 'BC', 'CD', 'DE', 'DG', 'FG', 'FH', 'HI', 'GI', 'IJ']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print(g.count_connected_components(), end=' ')
    print()


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG',
        'add FG', 'remove GE')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print('{:<10}'.format(case), g.has_cycle())