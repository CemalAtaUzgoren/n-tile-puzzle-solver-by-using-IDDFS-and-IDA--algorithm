import numpy as np
import random
import copy
import csv
import time
import os
####################################################################
########################### RESULTS  ######(python 3.11.6)##########
####################################################################
'''
Seed,Case_id,start_state,solution,moves,nodes,time(sec)
97,1,"[0, 1, [[7, 0, 3], [4, 8, 6], [1, 2, 5]]]",1,21,[1239],0.063
97,2,"[1, 2, [[2, 1, 7], [5, 3, 0], [6, 4, 8]]]",0,30,[116523],3.51
97,3,"[0, 0, [[0, 8, 4], [1, 2, 7], [6, 5, 3]]]",0,30,[395369],11.631
97,4,"[0, 1, [[5, 0, 8], [2, 3, 4], [1, 7, 6]]]",0,30,[198912],5.875
97,5,"[2, 1, [[1, 5, 3], [8, 6, 2], [4, 0, 7]]]",0,30,[239101],7.173
97,6,"[1, 2, [[4, 5, 6], [8, 3, 0], [2, 7, 1]]]",1,21,[145],0.005
97,7,"[2, 2, [[1, 2, 3], [7, 4, 8], [6, 5, 0]]]",0,30,[634096],18.908
97,8,"[1, 2, [[7, 1, 3], [2, 4, 0], [5, 6, 8]]]",1,17,[213],0.007
97,9,"[2, 2, [[7, 2, 6], [4, 8, 5], [3, 1, 0]]]",1,26,[2704],0.091
97,10,"[0, 2, [[2, 7, 0], [6, 3, 1], [4, 5, 8]]]",1,22,[613],0.019
'''
####################################################################
##################  SETTING UP THE INITIAL STATES  #################
####################################################################

class initialStates():

    def __init__(self) :

        self.tile_num=8# assuming that all different sizes are squire of a number. (16x16 , 9x9 , 5x5, ...)
        self.initial_state = list(reversed(range(self.tile_num+1)))# template_state from given in the CW_1 brief.
        self.states = []#all random initial states will be in this array.
        self.seed=97#106#97#755
        random.seed(self.seed)
    def random_init_states(self):
        self.mem_init =copy.deepcopy(self.initial_state)
        self.stored = self.mem_init
        for _ in range(10):#creating 10 initial state with the same seed value.
            print(f'template list for random initial state {_+1}',self.initial_state)
            random.shuffle(self.initial_state)
            a=True
            num=2
            while a :
                state_rows=[]#contains row information
                if num*num == len(self.initial_state):
                    rest_of_initial_state=self.initial_state
                    #spliting the initial state in to row lists
                    for i in range(int(len(self.initial_state)/num)):
                        state_rows.append((rest_of_initial_state[:num]))
                        rest_of_initial_state = rest_of_initial_state[num:]
                    #searching for the blank tile's position
                    for j in range(len(state_rows)):#i index of the blank tile
                        for k in range(num): # j index of the blank tile 
                            if state_rows[j][k] ==0:
                               init_state_row=[j,k,(state_rows)]
                               break
                    self.states.append((init_state_row))#
                    a=False  
                num=num+1
            self.mem_init2 =copy.deepcopy(self.stored)
            self.stored2 = self.mem_init2
            self.initial_state=self.stored2
                
        return(self.states)
    
    def print_init_states(self):#function to print the initial cases
        print('\n *INITIAL STATES* \n')
        for v in range(len(self.states)):
            print(self.states[v])

##########################################################################
##################  SEARCHİNG FOR THE GOAL STATE  ########################
##########################################################################

class searching(initialStates):
    def __init__(self) :
        self.visited=[]
       
    def move_blank(self,i,j,n): # creating generator for calculate the possible moves.
        if i+1 < n:
            yield (i+1,j)
        if i-1 >= 0:
            yield (i-1,j)
        if j+1 < n:
            yield (i,j+1)
        if j-1 >= 0:
            yield (i,j-1)
        
    def move(self,state):# making  the calculated moves.
        #print(state)
        [i, j, grid] =state
        n = len(grid)
      
        for pos in self.move_blank(i,j,n):
            i1,j1 = pos
            grid[i][j], grid[i1][j1] = grid[i1][j1], grid[i][j]#swap the blank tile
            yield [i1,j1,grid]
            grid[i][j], grid[i1][j1] = grid[i1][j1], grid[i][j] #restore the grid

    def manhattan_dist(self,init_pos , goal_pos):
        # tried to don't use any loop for high performance.

        init_pos = np.array(init_pos[-1])#taking only the grid part
        goal_pos = np.array(goal_pos[-1])#taking only the grid part

        indexes_of_differences = np.where((init_pos != goal_pos) & (init_pos!=0))#findind the coordinates of the misplaced tiles in the current state
        different_positions = np.array(list(zip(*indexes_of_differences)))#merging the x and y coordinates and creating a numpy array.
        init_values = init_pos[indexes_of_differences]#getting the values of the misplaced tiles in the initial grid.
        sorted_indices_init = np.argsort(init_values)#sorting the values of misplacesd tiles to make sure that we will compare the right tiles with the goal grid.
        sorted_coordinates_init = different_positions[sorted_indices_init]#sorting the coordinate array as well.

        indexes_of_goal = np.where(np.isin(goal_pos , init_values))#findind the coordinates of the misplaced tiles in the final state
        goal_positions = np.array(list(zip(indexes_of_goal[0], indexes_of_goal[1])))#merging the x and y coordinates and creating a numpy array.
        goal_values = goal_pos[indexes_of_goal]#getting the values
        sorted_indices_goal = np.argsort(goal_values)#sort the tiles that are compared with the misplaced tiles in the initial grid.
        sorted_coordinates_goal = goal_positions[sorted_indices_goal]#sort the coordinates as well
        #calculate the manhatton distance 
        substract = abs(sorted_coordinates_goal - sorted_coordinates_init)
        manhattan_dist = np.sum(substract)

        return manhattan_dist
    
    def solve_puzzle(self,start_state, goal_state):
        threshold = self.manhattan_dist(start_state,goal_state)#defining the threshold as manhatton distance
        self.visited.append(start_state)#initialize the visited list with root value.
        init_time = time.time()#start timer
        def IDA_star(visited , goal_state , layer , threshold ,nodes):
            current_node = visited[-1]#get the current grid
            cost = layer +self.manhattan_dist(current_node,goal_state)#calculate cost
            if layer==30:#check if the current depth is 30. 
                return 0 ,layer #If it is terminate the execution.
            
            if threshold<cost:#if cost,exceeds the threshold ,return cost to make it new threshold for further iterations.
                return cost,layer
            
            if current_node == (goal_state):#if the goal has achieved, return result.
                return 1,layer
            
            minimum_cost = float('inf')#minimim value will be our smallest cost  
            c=copy.deepcopy(current_node)#deep copy to don't lose the previous nodes because of the referential characteristic of the lists.
            for neighbour in self.move(c):#change the tiles positions
                if (neighbour not in visited):
                    visited.append(neighbour)#add to path
                    nodes[0] += 1#node counter
                    solution,sol_layer = IDA_star(visited, goal_state, layer + 1, threshold ,nodes)#recursion
                    #terminate the function for suspended nodes.(below)
                    if solution == 1:
                      return 1,sol_layer
                    if solution == 0:
                      return 0,sol_layer
                    if solution < minimum_cost:
                        minimum_cost = solution
                    visited.remove(neighbour)#after ever search, clear the path.    
            return minimum_cost,layer#return for update to threshold.
        nodes=[0]#node counter
        while True:
            sol,moves=IDA_star(self.visited , goal_state , 0 ,threshold, nodes)
            if sol==1:
                end_time =time.time()#stop timer
                total_time=round(end_time-init_time , 3)#calculate time
                return start_state , sol , moves , nodes , total_time 
            elif sol==0:
                end_time =time.time()
                total_time=round(end_time-init_time,3) 
                return start_state , sol , moves , nodes , total_time
            else :
                threshold=sol#update threshold.
            
if __name__ == "__main__":
    obj=initialStates()
    a=obj.random_init_states()
    obj.print_init_states()

    goal_state=[1, 1, [[1, 2, 3], [8, 0, 4], [7, 6, 5]]]#defining the goal state
    csv_file_headers = ['Seed' , 'Case_id' , 'start_state' , 'solution' , 'moves' , 'nodes' , 'time(sec)'] #cvs file's headers
    print('\n *RESULTS* \n') 
    for init_grid in range (len(a)):#running the IDDFS for each of the initial states
        obj3 = searching()
        sol=list(obj3.solve_puzzle(a[init_grid],goal_state))#call solve function 
        sol.insert(0,obj.seed)#add seed to csv file data
        sol.insert(1,init_grid+1)#add case number to csv file data
        csv_data=sol
        file_path= os.path.abspath('IDAstar_output.csv')
        
        with open(file_path , 'a' , newline='') as csvFile:#creating csv file in append mode.
            writer = csv.writer(csvFile)
            if init_grid==0:
                csvFile.truncate(0)#clear the csv file beafore adding the new lines
                writer.writerow(csv_file_headers)
            writer = csv.writer(csvFile)
            writer.writerow(csv_data)
           
        print(f'Solution for state{init_grid+1}==>',list(sol))