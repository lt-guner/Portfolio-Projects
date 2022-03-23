# Author: Timur Guner
# Class: CS325
# Assignment 8: Puzzle

from collections import deque

def solve_puzzle(Board, Source, Destination):

    # check to see if the Source that was passed has
    if Source[0]-1 >= 0:
        if Source[1]-1 >= 0:
            if Board[Source[0]-1][Source[1]-1] == "#":
                return None

    # create a set of visited nodes and add the source
    visited = set()
    visited.add(Source)

    # create a deque from imports and for node moves, count of moves, and the string of directions
    nodes_queue = deque()
    nodes_queue.append([Source])

    move_count = deque()
    move_count.append(0)

    dir_moves = deque()
    dir_moves.append(0)


    # loop through while nodes_queue is not empty
    while nodes_queue:

        # pop the current path that was pushed to the nodes_queue and and use the last node to update the path.
        cur_path = nodes_queue.popleft()
        node = cur_path[-1]
        cur_sum = move_count.popleft()
        cur_moves = dir_moves.popleft()

        # if the last node is the Destination then return cur_path
        if node == Destination:
            return (cur_sum-1,cur_moves)

        # adjust node to the actual indexes of the 2D array for ease use of use when comparing indexes
        fixed_node = tuple((node[0] - 1, node[1] - 1))

        # if the move upwards is in bounds, is a valid move, and is not visited proceed
        # update the path with the new node, the current sum + 1, and add direction to new_moves
        # push all to the queue
        if fixed_node[0]-1 >= 0:
            if Board[fixed_node[0]-1][fixed_node[1]] != '#':
                if tuple((node[0]-1,node[1])) not in visited:
                    
                    updated_path = list(cur_path)
                    updated_path.append(tuple((node[0]-1,node[1])))
                    nodes_queue.append(updated_path)
                    visited.add(tuple((node[0]-1,node[1])))

                    updated_sum = cur_sum+1
                    move_count.append(updated_sum)

                    if cur_moves == 0:
                        dir_moves.append('U')
                    else:
                        new_moves = cur_moves + 'U'
                        dir_moves.append(new_moves)


        # same as above but with downwards move
        if fixed_node[0]+1 < len(Board):
            if Board[fixed_node[0]+1][fixed_node[1]] != '#':
                if tuple((node[0]+1,node[1])) not in visited:
                    
                    updated_path = list(cur_path)
                    updated_path.append(tuple((node[0]+1,node[1])))
                    nodes_queue.append(updated_path)
                    visited.add(tuple((node[0]+1,node[1])))

                    updated_sum = cur_sum+1
                    move_count.append(updated_sum)

                    if cur_moves == 0:
                        dir_moves.append('D')
                    else:
                        new_moves = cur_moves + 'D'
                        dir_moves.append(new_moves)

        # same as above but with leftward move
        if fixed_node[1]-1 >= 0:
            if Board[fixed_node[0]][fixed_node[1]-1] != '#':
                if tuple((node[0],node[1]-1)) not in visited:
                    
                    updated_path = list(cur_path)
                    updated_path.append(tuple((node[0],node[1]-1)))
                    nodes_queue.append(updated_path)
                    visited.add(tuple((node[0],node[1]-1)))

                    updated_sum = cur_sum+1
                    move_count.append(updated_sum)

                    if cur_moves == 0:
                        dir_moves.append('L')
                    else:
                        new_moves = cur_moves + 'L'
                        dir_moves.append(new_moves)

        # same as above but with rightward move
        if fixed_node[1]+1 < len(Board[0]):
            if Board[fixed_node[0]][fixed_node[1]+1] != '#':
                if tuple((node[0],node[1]+1)) not in visited:
                    
                    updated_path = list(cur_path)
                    updated_path.append(tuple((node[0],node[1]+1)))
                    nodes_queue.append(updated_path)
                    visited.add(tuple((node[0],node[1]+1)))

                    updated_sum = cur_sum+1
                    move_count.append(updated_sum)

                    if cur_moves == 0:
                        dir_moves.append('R')
                    else:
                        new_moves = cur_moves + 'R'
                        dir_moves.append(new_moves)

    return (None, None)

if __name__ == '__main__':
    board = [['-', '-', '-', '-', '-'], ['-', '-', '#', '-', '-'], ['-', '-', '-', '-', '-'], ['#', '-', '#', '#', '-'],
             ['-', '#', '-', '-', '-']]
    print(solve_puzzle(board, (1, 3), (3, 3)))
    print(solve_puzzle(board, (1, 1), (5, 5)))
    print(solve_puzzle(board, (1, 1), (5, 1)))