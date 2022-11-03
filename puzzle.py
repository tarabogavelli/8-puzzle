from __future__ import division
from __future__ import print_function

import sys
import math
import time
import queue as Q
import resource
from queue import PriorityQueue

class frontier():
    
    def __init__(self):
        self.list = []
        self.my_set = set()
        self.config_set = set()
        
    def add_config(self, item):
        self.config_set.add(item)
        return self
    def remove_config(self, item):
        self.config_set.add(item)
        return self
        
        
    def push(self, item):
        self.list.append(item)
        self.my_set.add(item)
        self.config_set.add(item)
        return self
    
    def pop(self):
        item = self.list.pop()
        self.my_set.remove(item)
        self.config_set.remove(item)
        return item
        
    def enqueue(self, item):
        self.list.append(item)
        self.my_set.add(item)
        self.config_set.add(item)
        return self
    
    def dequeue(self):
        item = self.list.pop(0)
        self.my_set.remove(item)
        self.config_set.remove(item)
        return item
    
    def contains(self, item):
        if item in self.config_set:
            return True
        else:
            return False
        
    def is_empty(self):
        if self.list:
            return False
        else:
            return True
#### SKELETON CODE ####
## The Class that Represents the Puzzle
class PuzzleState(object):
    """
        The PuzzleState stores a board configuration and implements
        movement instructions to generate valid children.
    """
    def __init__(self, config, n, parent=None, action="Initial", cost=0):
        """
        :param config->List : Represents the n*n board, for e.g. [0,1,2,3,4,5,6,7,8] represents the goal state.
        :param n->int : Size of the board
        :param parent->PuzzleState
        :param action->string
        :param cost->int
        """
        if n*n != len(config) or n < 2:
            raise Exception("The length of config is not correct!")
        if set(config) != set(range(n*n)):
            raise Exception("Config contains invalid/duplicate entries : ", config)

        self.n        = n
        self.cost     = cost
        self.parent   = parent
        self.action   = action
        self.config   = config
        self.children = []

        # Get the index and (row, col) of empty block
        self.blank_index = self.config.index(0)
        
    def __lt__(self, other):
        # self left other up
        "UDLR"
        if self.action == "Up":
            return self.action < other.action
        elif self.action == "Down" and other.action != "Up":
            return self.action < other.action
        elif self.action == "Left" and other.action !="Up" and other.action != "Down":
            return self.action < other.action
        else:
            return self.action > other.action
            
    def display(self):
        """ Display this Puzzle state as a n*n board """
        for i in range(self.n):
            print(self.config[3*i : 3*(i+1)])

    def move_up(self):
        """ 
        Moves the blank tile one row up.
        :return a PuzzleState with the new configuration
        """
        
        my_list = self.config[:]
        zero_index = self.config.index(0)
        up_pos = zero_index-3
        if zero_index!=0 and zero_index!=1 and zero_index!=2:
            temp = self.config[up_pos]
            my_list[up_pos] = 0
            my_list[zero_index] = temp
            new = PuzzleState(my_list,self.n,self,"Up")
            new.cost = self.cost+1
            #print("up")
            return new
        else:
            return None
        
      
    def move_down(self):
        """
        Moves the blank tile one row down.
        :return a PuzzleState with the new configuration
        """
        # make list then at the end create new object
        my_list = self.config[:] 
        zero_index = self.config.index(0)
        down_pos = zero_index+3
        if zero_index!=6 and zero_index!=7 and zero_index!=8:
            temp = self.config[down_pos]
            my_list[down_pos] = 0
            my_list[zero_index] = temp
            new = PuzzleState(my_list,self.n,self,"Down")
            new.cost = self.cost+1
            return new
        else:
            return None
      
    def move_left(self):
        """
        Moves the blank tile one column to the left.
        :return a PuzzleState with the new configuration
        """
        my_list = self.config[:]
        zero_index = self.config.index(0)
        left_pos = zero_index-1
        if zero_index!=0 and zero_index!=3 and zero_index!=6:
            temp = self.config[left_pos]
            my_list[left_pos] = 0
            my_list[zero_index] = temp
            new = PuzzleState(my_list, self.n, self, "Left")
            new.cost = self.cost+1
            return new
        else:
            return None

    def move_right(self):
        """
        Moves the blank tile one column to the right.
        :return a PuzzleState with the new configuration
        """
        my_list = self.config[:]
        zero_index = self.config.index(0)
        right_pos = zero_index+1
        if zero_index!=2 and zero_index!=5 and zero_index!=8:
            temp = self.config[right_pos]
            my_list[right_pos] = 0
            my_list[zero_index] = temp
            new = PuzzleState(my_list, self.n, self, "Right")
            new.cost = self.cost+1
            return new
        else:
            return None
      
    def expand(self):
        """ Generate the child nodes of this node """
        
        # Node has already been expanded
        if len(self.children) != 0:
            return self.children
        
        # Add child nodes in order of UDLR
        children = [
            self.move_up(),
            self.move_down(),
            self.move_left(),
            self.move_right()]

        # Compose self.children of all non-None children states
        self.children = [state for state in children if state is not None]
        return self.children

# Function that Writes to output.txt

### Students need to change the method to have the corresponding parameters        
    
def writeOutput(initial_state,final_state,nodes_expanded,ram, max_search_depth, time):
    ### Student Code Goes here
    # path_to_goal
    cur_state = final_state
    path_to_goal = []
    while cur_state.config != initial_state.config:
        path_to_goal.insert(0, cur_state.action)
        cur_state = cur_state.parent
    f = open("output.txt", "w")
    f.write("path_to_goal: " + str(path_to_goal) + "\n")
    f.write("cost_of_path: " + str(len(path_to_goal))+ "\n")
    f.write("nodes_expanded: " + str(nodes_expanded)+ "\n")
    f.write("search_depth: "+ str(len(path_to_goal))+ "\n")
    f.write("max_search_depth: "+ str(max_search_depth)+ "\n")
    f.write("running_time: " + str(round(time, 8))+ "\n")
    f.write("max_ram_usage: " + str(ram)+ "\n")
    f.close()

    

def bfs_search(initial_state):
    """BFS search"""
    ### STUDENT CODE GOES HERE ###
    start_time  = time.time()
    start_ram = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    my_frontier = frontier()
    my_frontier = my_frontier.enqueue(initial_state)
    my_frontier.add_config(tuple(initial_state.config))
    explored = set()
    cost_set = set()
    
    while not my_frontier.is_empty():
        state = my_frontier.dequeue()
        my_frontier.remove_config(tuple(state.config))
        neighbors = state.expand()
        
        if test_goal(state):
            ram = (resource.getrusage(resource .RUSAGE_SELF).ru_maxrss-start_ram)/(2**20)
            end_time = time.time()
            writeOutput(initial_state, state, len(explored), ram,list(cost_set).pop(), end_time-start_time)
            return state
        explored.add(tuple(state.config))
        for neighbor in neighbors:
            if not my_frontier.contains(tuple(neighbor.config)) and tuple(neighbor.config) not in explored:
                my_frontier.enqueue(neighbor)
                cost_set.add(neighbor.cost)
                my_frontier.add_config(tuple(neighbor.config))
    return None
    

def dfs_search(initial_state):
    """DFS search"""
    start_time  = time.time()
    start_ram = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    my_frontier = frontier()
    my_frontier.push(initial_state)
    my_frontier.add_config(tuple(initial_state.config))
    explored = set()
    cost_set = set()
    
    while not my_frontier.is_empty():
        state = my_frontier.pop()
        my_frontier.remove_config(tuple(state.config))
        neighbors = state.expand()
        
        if test_goal(state):
            ram = (resource.getrusage(resource .RUSAGE_SELF).ru_maxrss-start_ram)/(2**20)
            end_time = time.time()
            writeOutput(initial_state, state, len(explored), ram, list(cost_set).pop(), end_time-start_time)
            return state
        explored.add(tuple(state.config))
        counter = len(neighbors)-1
        while counter >= 0:
            if not my_frontier.contains(tuple(neighbors[counter].config)) and tuple(neighbors[counter].config) not in explored:
                my_frontier.push(neighbors[counter])
                cost_set.add(neighbors[counter].cost)
                my_frontier.add_config(tuple(neighbors[counter].config))
            counter -= 1
    return None
            
    
    

def A_star_search(initial_state):
    """A * search"""
    ### STUDENT CODE GOES HERE ###
    start_time  = time.time()
    start_ram = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    frontier = PriorityQueue()
    explored = set()
    frontier.put((0,initial_state))
    cost_set = set()
    
    while frontier:
        state = frontier.get()[1]
        explored.add(tuple(state.config))
        neighbors = state.expand()
        
        if test_goal(state):
            ram = (resource.getrusage(resource .RUSAGE_SELF).ru_maxrss-start_ram)/(2**20)
            end_time = time.time()
            writeOutput(initial_state, state, len(explored)-1, ram, list(cost_set).pop(), end_time-start_time)
            return state
        
        for neighbor in neighbors:
            if tuple(neighbor.config) not in explored:
                frontier.put((calculate_total_cost(neighbor),neighbor))
                cost_set.add(neighbor.cost)
         
    return None
    

def calculate_total_cost(state):
    """calculate the total estimated cost of a state"""
    ### STUDENT CODE GOES HERE ###
    # total cost = number of moves made
    cost = state.cost
    config = state.config
    n = state.n
    total_man_cost = 0
    for i in range(n**2):
        man_cost = calculate_manhattan_dist(i, config[i], n)
        total_man_cost += man_cost
    return total_man_cost + cost
    
    

def calculate_manhattan_dist(idx, value, n):
    """calculate the manhattan distance of a tile"""
    ### STUDENT CODE GOES HERE ###

    goal_idx = value
    if idx == goal_idx or value==0:
        return 0
    
    else:
        goal_idx_row = math.floor(goal_idx/3)
        goal_idx_col = goal_idx%3
        
        idx_row = math.floor(idx/3)
        idx_col = idx%3
        
        distance = abs(goal_idx_row - idx_row) + abs(goal_idx_col - idx_col)
        return distance
    
    
    

def test_goal(puzzle_state):
    """test the state is the goal state or not"""
    ### STUDENT CODE GOES HERE ###
    if puzzle_state.config == [0,1,2,3,4,5,6,7,8]:
        return True

# Main Function that reads in Input and Runs corresponding Algorithm
def main():
    
    # ORIGINAL CODE
    
    search_mode = sys.argv[1].lower()
    begin_state = sys.argv[2].split(",")
    begin_state = list(map(int, begin_state))
    board_size  = int(math.sqrt(len(begin_state)))
    hard_state  = PuzzleState(begin_state, board_size)
    start_time  = time.time()
    
    if   search_mode == "bfs": bfs_search(hard_state)
    elif search_mode == "dfs": dfs_search(hard_state)
    elif search_mode == "ast": A_star_search(hard_state)
    else: 
        print("Enter valid command arguments !")
        
    end_time = time.time()
    print("Program completed in %.3f second(s)"%(end_time-start_time))
    

if __name__ == '__main__':
    main()
