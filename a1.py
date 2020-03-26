#!/usr/bin/env python
# coding: utf-8

# In[1]:


# a1.py

from search import *
import random
import time


# In[2]:


# https://realpython.com/python-super/
# https://www.tutorialspoint.com/python3/number_shuffle.htm

def make_rand_8puzzle():
    tmp_list = [1,2,3,4,5,6,7,8,0]
    random.shuffle(tmp_list)
    ex = EightPuzzle(tuple(tmp_list))
    while ex.check_solvability(ex.initial) == False:
        random.shuffle(tmp_list)
        ex = EightPuzzle(tuple(tmp_list))
    return ex


# In[3]:


def display(state):
    tmp = state.initial
    tmp = list(tmp)
    for i in range(9):
        if tmp[i] == 0:
            tmp[i] = '*'
    print(*tmp[:3])
    print(*tmp[3:6])
    print(*tmp[6:])


# In[4]:


def manhattan_8(node):
    state = node.state
    index_goal = {0:[2,2], 1:[0,0], 2:[0,1], 3:[0,2], 4:[1,0], 5:[1,1], 6:[1,2], 7:[2,0], 8:[2,1]}
    index_state = {}
    index = [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2]]
    
    for i in range(len(state)):
        index_state[state[i]] = index[i]
    
    mhd = 0
    
    for i in range(8):
        for j in range(2):
            mhd = abs(index_goal[i+1][j] - index_state[i+1][j]) + mhd
    return mhd


# In[5]:


def max_manhattan(node):
    state = EightPuzzle(node.state)
    return max(manhattan_8(node), state.h(node))


# In[6]:


def best_first_graph_search(problem, f, display=False):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    pop_number = 0
    while frontier:
        node = frontier.pop()
        pop_number = pop_number + 1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return node, pop_number
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None, pop_number


def astar_search(problem, h=None):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n))


# In[7]:


def test_8puzzle():
    for i in range(10):
        print('Records for test',i+1, ': ')
        
        new = make_rand_8puzzle()
        display(new)
        print(new.initial)

        time_start = time.time()
        a, b = astar_search(new)
        running_time = time.time() - time_start
        
        print('Misplaced tile heuristic:')
        print('Total running time in seconds:', running_time)
        print('Length of solution:', len(a.solution()))
        print('Total number of nodes that removed:', b)

        time_start = time.time()
        a, b = astar_search(new, h = manhattan_8)
        running_time = time.time() - time_start
        print('Manhattan distance heuristic:')
        print('Total running time in seconds:', running_time)
        print('Length of solution:', len(a.solution()))
        print('Total number of nodes that removed:', b)

        time_start = time.time()
        a, b = astar_search(new, h = max_manhattan)
        running_time = time.time() - time_start
        print('Max of the misplaced tile and Manhattan distance:')
        print('Total running time in seconds:', running_time)
        print('Length of solution:', len(a.solution()))
        print('Total number of nodes that removed:', b)
        print()


# In[8]:


class HousePuzzle(Problem):
    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        """ Define goal state and initialize a problem """
       
        self.goal = goal
        super().__init__(initial, goal)
       
    def find_blank_square(self, state):
        """Return the index of the blank square in a given state"""
       
        return state.index(0)
   
    def actions(self, state):
       
        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']      
        index_blank_square = self.find_blank_square(state)

        if index_blank_square == 0:
            possible_actions.remove('UP')
            possible_actions.remove('LEFT')
            possible_actions.remove('RIGHT')

        if index_blank_square == 1:
            possible_actions.remove('UP')
            possible_actions.remove('LEFT')
       
        if index_blank_square == 3:
            possible_actions.remove('UP')
           
        if index_blank_square == 4:
            possible_actions.remove('UP')
            possible_actions.remove('RIGHT')
           
        if index_blank_square == 5:
            possible_actions.remove('LEFT')
            possible_actions.remove('DOWN')
           
        if index_blank_square == 6:
            possible_actions.remove('DOWN')
           
        if index_blank_square == 7:
            possible_actions.remove('DOWN')
       
        if index_blank_square == 8:
            possible_actions.remove('RIGHT')
            possible_actions.remove('DOWN')
           
        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)
       
        if blank == 0:
            delta = {'UP':-3, 'DOWN':2, 'LEFT':-1, 'RIGHT':1}
            neighbor = blank + delta[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
       
        if blank == 1:
            delta = {'UP':-3, 'DOWN':4, 'LEFT':-1, 'RIGHT':1}
            neighbor = blank + delta[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
       
        if blank == 2:
            delta = {'UP':-2, 'DOWN':4, 'LEFT':-1, 'RIGHT':1}
            neighbor = blank + delta[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
           
        if blank == 3:
            delta = {'UP':-3, 'DOWN':4, 'LEFT':-1, 'RIGHT':1}
            neighbor = blank + delta[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
           
        if blank == 4:
            delta = {'UP':-3, 'DOWN':4, 'LEFT':-1, 'RIGHT':1}
            neighbor = blank + delta[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
           
        if blank == 5:
            delta = {'UP':-4, 'DOWN':3, 'LEFT':-1, 'RIGHT':1}
            neighbor = blank + delta[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
           
        if blank == 6:
            delta = {'UP':-4, 'DOWN':3, 'LEFT':-1, 'RIGHT':1}
            neighbor = blank + delta[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
           
        if blank == 7:
            delta = {'UP':-4, 'DOWN':3, 'LEFT':-1, 'RIGHT':1}
            neighbor = blank + delta[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
           
        if blank == 8:
            delta = {'UP':-4, 'DOWN':3, 'LEFT':-1, 'RIGHT':1}
            neighbor = blank + delta[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
           
        return tuple(new_state)
   
    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal
       
#     def check_solvability(self, state):
#         """ Checks if the given state is solvable """
#         blank = state.index(0)
#         if state[0] != 1 and state[0] != 0:
#             return False
#         elif state[0] == 0 and state[2] != 1:
#             return False
#         inversion = 0
#         for i in range(1, len(state)):
#             for j in range(i+1, len(state)):
#                 if (state[i] > state[j]) and state[i] != 0 and state[j]!= 0:
#                     inversion += 1
#         return inversion % 2 == 0


# The following function is discussed with another classmate Eric Sun :

    def check_solvability(self, state):
        inversion = 0
        if state[0] == 1:
            for i in range(1,9):
                for j in range(i+1, 9):
                    if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                        inversion +=1
            if state.index(0) <= 4:
                inversion +=1
            return inversion%2 == 0
        
        elif state[0] == 0 and state[2] == 1:
            for i in range(1,9):
                for j in range(i+1, 9):
                    if (state[i] > state[j]) and state[i] != 1 and state[j] != 1:
                        inversion +=1
            return inversion % 2 == 1
        else:
            return False

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))


# In[9]:


def make_rand_housepuzzle():
    tmp_list = [1,2,3,4,5,6,7,8,0]
    random.shuffle(tmp_list)
    ex = HousePuzzle(tuple(tmp_list))
    while ex.check_solvability(ex.initial) == False:
        random.shuffle(tmp_list)
        ex = HousePuzzle(tuple(tmp_list))
    return ex


# In[10]:


def house_display(state):
    tmp = state.initial
    tmp = list(tmp)
    for i in range(9):
        if tmp[i] == 0:
            tmp[i] = '*'
    print('  ', *tmp[:1], sep = '')
    print(*tmp[1:5])
    print(*tmp[5:])


# In[11]:


def manhattan_house(node):
    state = node.state
    index_goal = {0:[2,3], 1:[0,1], 2:[1,0], 3:[1,1], 4:[1,2], 5:[1,3], 6:[2,0], 7:[2,1], 8:[2,2]}
    index_state = {}
    index = [[0,1], [1,0], [1,1], [1,2], [1,3], [2,0], [2,1], [2,2], [2,3]]
    x, y = 0, 0
   
    for i in range(len(state)):
        index_state[state[i]] = index[i]
   
    mhd = 0

    # Don't include zero. The heuristic function never ever overestimate the true cost
    # but the default one does
    for i in range(1,9):
        for j in range(2):
            mhd = abs(index_goal[i][j] - index_state[i][j]) + mhd
   
    return mhd


# In[12]:


def max_manhattan_house(node):
    state = HousePuzzle(node.state)
    return max(manhattan_house(node), state.h(node))


# In[13]:


def test_housepuzzle():
    for i in range(10):
        print('Records for test',i+1, ': ')
        
        new = make_rand_housepuzzle()
        house_display(new)
        print(new.initial)

        time_start = time.time()
        a, b = astar_search(new)
        running_time = time.time() - time_start
        
        print('Misplaced tile heuristic:')
        print('Total running time in seconds:', running_time)
        print('Length of solution:', len(a.solution()))
        print('Total number of nodes that removed:', b)

        time_start = time.time()
        a, b = astar_search(new, h = manhattan_house)
        running_time = time.time() - time_start
        print('Manhattan distance heuristic:')
        print('Total running time in seconds:', running_time)
        print('Length of solution:', len(a.solution()))
        print('Total number of nodes that removed:', b)

        time_start = time.time()
        a, b = astar_search(new, h = max_manhattan_house)
        running_time = time.time() - time_start
        print('Max of the misplaced tile and Manhattan distance:')
        print('Total running time in seconds:', running_time)
        print('Length of solution:', len(a.solution()))
        print('Total number of nodes that removed:', b)
        print()


# In[14]:


print('Test result for 8_Puzzle: ')
test_8puzzle()
print('Test result for House_Puzzle:')
test_housepuzzle()

