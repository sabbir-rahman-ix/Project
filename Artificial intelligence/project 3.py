"""
Project-03
N-Queens and 8-Puzzle using Heuristic Search

Algorithms:
1. Greedy Best First Search
2. A* Search

Level:
Undergraduate Pattern Recognition Lab

Run:
python Project_03_Heuristic_Search.py
"""

import heapq
import time
import copy


# ============================================================
# GENERAL NODE CLASS
# ============================================================

class Node:

    def __init__(self, state, parent=None, g=0, h=0):
        self.state = state
        self.parent = parent
        self.g = g
        self.h = h
        self.f = g + h


    def __lt__(self, other):
        return self.f < other.f



# ============================================================
# ===================== N QUEENS =============================
# ============================================================


def print_board(board):

    n = len(board)

    print()

    for row in range(n):

        line = ""

        for col in range(n):

            if board[row] == col:
                line += " Q "
            else:
                line += " . "

        print(line)

    print()



# ------------------------------------------------------------
# Heuristic:
# Number of attacking queen pairs
# ------------------------------------------------------------

def queen_conflicts(state):

    n = len(state)

    conflicts = 0


    for i in range(n):

        for j in range(i + 1, n):

            # Same column
            if state[i] == state[j]:
                conflicts += 1


            # Same diagonal
            if abs(state[i] - state[j]) == abs(i - j):
                conflicts += 1


    return conflicts



def queen_goal(state):

    return queen_conflicts(state) == 0



# ------------------------------------------------------------
# Generate neighboring states
# ------------------------------------------------------------

def queen_neighbors(state):

    neighbors = []

    n = len(state)


    for row in range(n):

        current_col = state[row]


        for col in range(n):

            if col != current_col:

                new_state = state.copy()

                new_state[row] = col

                neighbors.append(new_state)


    return neighbors



# ------------------------------------------------------------
# Greedy Best First Search for N Queens
# ------------------------------------------------------------

def greedy_nqueen(start):

    start_time = time.time()

    queue = []

    visited = set()


    h = queen_conflicts(start)

    heapq.heappush(queue, Node(start, h=h))


    expanded = 0


    while queue:


        current = heapq.heappop(queue)


        key = tuple(current.state)


        if key in visited:
            continue


        visited.add(key)

        expanded += 1



        if queen_goal(current.state):

            end_time = time.time()

            return (
                current.state,
                expanded,
                end_time-start_time
            )



        for child in queen_neighbors(current.state):

            if tuple(child) not in visited:

                heapq.heappush(
                    queue,
                    Node(
                        child,
                        h=queen_conflicts(child)
                    )
                )


    return None



# ------------------------------------------------------------
# A* Search for N Queens
# ------------------------------------------------------------

def astar_nqueen(start):

    start_time = time.time()


    queue = []

    visited = set()


    heapq.heappush(
        queue,
        Node(
            start,
            g=0,
            h=queen_conflicts(start)
        )
    )


    expanded = 0



    while queue:


        current = heapq.heappop(queue)


        key = tuple(current.state)


        if key in visited:
            continue


        visited.add(key)

        expanded += 1



        if queen_goal(current.state):

            end_time=time.time()

            return(
                current.state,
                expanded,
                end_time-start_time
            )



        for child in queen_neighbors(current.state):


            if tuple(child) not in visited:


                heapq.heappush(
                    queue,
                    Node(
                        child,
                        g=current.g+1,
                        h=queen_conflicts(child)
                    )
                )


    return None



# ------------------------------------------------------------
# Run N Queen Experiment
# ------------------------------------------------------------


def run_nqueen():


    n = int(input("\nEnter number of queens: "))


    start=[]


    for i in range(n):
        start.append(i)



    print("\nInitial State:")
    print_board(start)



    print("Running Greedy Best First Search...")


    result1 = greedy_nqueen(start)



    if result1:


        print("\nGreedy Solution:")
        print_board(result1[0])

        print(
            "Expanded Nodes:",
            result1[1]
        )

        print(
            "Time:",
            result1[2],
            "seconds"
        )



    print("\nRunning A* Search...")


    result2 = astar_nqueen(start)



    if result2:


        print("\nA* Solution:")

        print_board(result2[0])


        print(
            "Expanded Nodes:",
            result2[1]
        )

        print(
            "Time:",
            result2[2],
            "seconds"
        )




# ============================================================
# ===================== 8 PUZZLE =============================
# ============================================================


GOAL_STATE = (
    1,2,3,
    4,5,6,
    7,8,0
)



# ------------------------------------------------------------
# Print Puzzle
# ------------------------------------------------------------

def print_puzzle(state):

    print()

    for i in range(0,9,3):

        row = state[i:i+3]

        print(
            row[0],
            row[1],
            row[2]
        )

    print()



# ------------------------------------------------------------
# Find blank position
# ------------------------------------------------------------

def blank_position(state):

    return state.index(0)



# ------------------------------------------------------------
# Generate puzzle moves
# ------------------------------------------------------------

def puzzle_neighbors(state):

    neighbors=[]


    index = blank_position(state)


    row=index//3
    col=index%3



    moves=[]


    if row>0:
        moves.append(index-3)

    if row<2:
        moves.append(index+3)

    if col>0:
        moves.append(index-1)

    if col<2:
        moves.append(index+1)



    for move in moves:

        new_state=list(state)


        new_state[index],new_state[move]=(
            new_state[move],
            new_state[index]
        )


        neighbors.append(tuple(new_state))


    return neighbors




# ------------------------------------------------------------
# Heuristic 1:
# Misplaced Tiles
# ------------------------------------------------------------

def misplaced_tiles(state):

    count=0


    for i in range(9):

        if (
            state[i]!=0
            and
            state[i]!=GOAL_STATE[i]
        ):

            count+=1


    return count




# ------------------------------------------------------------
# Heuristic 2:
# Manhattan Distance
# ------------------------------------------------------------

def manhattan_distance(state):

    distance=0


    for index,value in enumerate(state):

        if value!=0:


            goal_index=GOAL_STATE.index(value)


            current_row=index//3
            current_col=index%3


            goal_row=goal_index//3
            goal_col=goal_index%3



            distance += (
                abs(current_row-goal_row)
                +
                abs(current_col-goal_col)
            )


    return distance




# ------------------------------------------------------------
# Reconstruct solution path
# ------------------------------------------------------------

def solution_path(node):

    path=[]


    while node:

        path.append(node.state)

        node=node.parent


    return path[::-1]





# ------------------------------------------------------------
# Generic Greedy Best First Search
# ------------------------------------------------------------

def greedy_puzzle(start, heuristic):


    start_time=time.time()


    queue=[]

    visited=set()


    start_node=Node(
        start,
        h=heuristic(start)
    )


    heapq.heappush(queue,start_node)


    expanded=0



    while queue:


        current=heapq.heappop(queue)


        if current.state in visited:
            continue


        visited.add(current.state)


        expanded+=1



        if current.state==GOAL_STATE:


            return(
                solution_path(current),
                expanded,
                time.time()-start_time
            )



        for child in puzzle_neighbors(current.state):


            if child not in visited:


                heapq.heappush(
                    queue,
                    Node(
                        child,
                        parent=current,
                        h=heuristic(child)
                    )
                )



    return None





# ------------------------------------------------------------
# Generic A* Search
# ------------------------------------------------------------

def astar_puzzle(start, heuristic):


    start_time=time.time()


    queue=[]


    visited=set()



    heapq.heappush(
        queue,
        Node(
            start,
            g=0,
            h=heuristic(start)
        )
    )



    expanded=0



    while queue:


        current=heapq.heappop(queue)



        if current.state in visited:
            continue



        visited.add(current.state)


        expanded+=1



        if current.state==GOAL_STATE:


            return(
                solution_path(current),
                expanded,
                time.time()-start_time
            )



        for child in puzzle_neighbors(current.state):


            if child not in visited:


                heapq.heappush(
                    queue,
                    Node(
                        child,
                        parent=current,
                        g=current.g+1,
                        h=heuristic(child)
                    )
                )



    return None





# ------------------------------------------------------------
# Display Puzzle Solution
# ------------------------------------------------------------

def show_solution(path):

    print(
        "\nTotal Moves:",
        len(path)-1
    )


    for step,state in enumerate(path):

        print(
            "\nStep",
            step
        )

        print_puzzle(state)




# ------------------------------------------------------------
# Run 8 Puzzle Experiment
# ------------------------------------------------------------

def run_puzzle():


    start=(1,2,3,
           4,0,6,
           7,5,8)



    print("\nInitial Puzzle:")

    print_puzzle(start)



    print(
        "\nGreedy Best First Search"
        " using Misplaced Tiles"
    )


    result1=greedy_puzzle(
        start,
        misplaced_tiles
    )


    if result1:


        show_solution(result1[0])


        print(
            "Expanded Nodes:",
            result1[1]
        )

        print(
            "Time:",
            result1[2],
            "seconds"
        )




    print(
        "\nGreedy Best First Search"
        " using Manhattan Distance"
    )


    result2=greedy_puzzle(
        start,
        manhattan_distance
    )


    if result2:


        print(
            "Expanded Nodes:",
            result2[1]
        )

        print(
            "Time:",
            result2[2],
            "seconds"
        )




    print(
        "\nA* Search using Manhattan Distance"
    )


    result3=astar_puzzle(
        start,
        manhattan_distance
    )


    if result3:


        show_solution(result3[0])


        print(
            "Expanded Nodes:",
            result3[1]
        )


        print(
            "Time:",
            result3[2],
            "seconds"
        )






# ============================================================
# ===================== MAIN MENU =============================
# ============================================================


def main():


    while True:


        print(
            """
========================================
 Project-03 Heuristic Search
 N-Queens and 8-Puzzle
========================================

1. Solve N-Queens
2. Solve 8-Puzzle
3. Exit

"""
        )



        choice=input(
            "Enter your choice: "
        )



        if choice=="1":

            run_nqueen()



        elif choice=="2":

            run_puzzle()



        elif choice=="3":

            print(
                "Program terminated."
            )

            break



        else:

            print(
                "Invalid choice!"
            )




if __name__=="__main__":

    main()