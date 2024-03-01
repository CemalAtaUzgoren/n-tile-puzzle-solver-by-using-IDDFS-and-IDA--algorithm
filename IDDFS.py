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
97,1,"[0, 1, [[7, 0, 3], [4, 8, 6], [1, 2, 5]]]",1,21,[1090243],3.542250871658325
97,2,"[1, 2, [[2, 1, 7], [5, 3, 0], [6, 4, 8]]]",0,30,[221230850],715.1047222614288
97,3,"[0, 0, [[0, 8, 4], [1, 2, 7], [6, 5, 3]]]",0,30,[154866570],497.6049599647522
97,4,"[0, 1, [[5, 0, 8], [2, 3, 4], [1, 7, 6]]]",0,30,[221230850],714.9736349582672
97,5,"[2, 1, [[1, 5, 3], [8, 6, 2], [4, 0, 7]]]",0,30,[221230850],712.9818658828735
97,6,"[1, 2, [[4, 5, 6], [8, 3, 0], [2, 7, 1]]]",1,21,[1324774],4.279350996017456
97,7,"[2, 2, [[1, 2, 3], [7, 4, 8], [6, 5, 0]]]",0,30,[154866570],497.1300401687622
97,8,"[1, 2, [[7, 1, 3], [2, 4, 0], [5, 6, 8]]]",1,17,[123098],0.400728702545166
97,9,"[2, 2, [[7, 2, 6], [4, 8, 5], [3, 1, 0]]]",1,26,[10995156],35.46028208732605
97,10,"[0, 2, [[2, 7, 0], [6, 3, 1], [4, 5, 8]]]",1,22,[1369408],4.476354122161865
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
        self.mem_init =copy.deepcopy(self.initial_state)#making sure that every random initial state is the shuffled version of list[8,7,6,5,4,3,2,1,0] (for self.initial_state)
        self.stored = self.mem_init
        for _ in range(10):#creating 10 initial state with the same seed value.
            print(f'template list for random initial state {_+1}',self.initial_state)# showing that every template state is going to be shuffled are same. (list[8,7,6,5,4,3,2,1,0] )
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
            self.mem_init2 =copy.deepcopy(self.stored)#making sure that every random initial state is the shuffled version of list[8,7,6,5,4,3,2,1,0] (for the rest 9 state)
            self.stored2 = self.mem_init2
            self.initial_state=self.stored2
                
        return(self.states)
    
    def print_init_states(self):#function to print the initial cases
        print('\n *INITIAL STATES* \n')
        for v in range(len(self.states)):
            print(self.states[v])

##########################################################################
##################  SEARCHING FOR THE GOAL STATE  ########################
##########################################################################

class searching(initialStates):
    def __init__(self) :
        self.visited=set()
       
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
        [i, j, grid] =state
        n = len(grid)
      
        for pos in self.move_blank(i,j,n):
            i1,j1 = pos
            grid[i][j], grid[i1][j1] = grid[i1][j1], grid[i][j]#swap the blank tile
            yield [i1,j1,grid]
            grid[i][j], grid[i1][j1] = grid[i1][j1], grid[i][j] #restore the grid

    
    def solve_puzzle(self,start_state, goal_state): #def solve_puzzle(start_state, goal_state): same as brief.
        start_state2=copy.deepcopy(start_state)
        visited=self.visited#create a set object to control nodes in the previous case
        start_time = time.time()#initialize the time
        def iddfs(start_state, goal_state ,depth,allowed_depth,path,node_count):#search algorithm
            
            if (goal_state)==(start_state):
                return start_state
              
            elif depth < allowed_depth:#maximum depth control 
                #c=copy.deepcopy(start_state)  #deep copy to reserve the previus state
                for neighbour in self.move(start_state):  #for loop for suspending mechanisim (dfs goes as deep as it can without looking the neighabours, so we have to create a mechanism to check the neighbour nodes after the algorithm goes to deepest layer allowed.) 
                    if (str(neighbour) not in visited):
                        visited.add(str(neighbour))  
                        node_count[0] += 1 #counter for total visited nodes.
                        new_path = path + [neighbour]  # stores the successfull path.
                        
                        sol=iddfs(neighbour,goal_state,depth+1,allowed_depth,new_path,node_count)#recursion
                        if sol != None:#terminated the seaches for suspended  nodes after a solution is found.
                            return sol
                          
                        visited.remove(str(neighbour))         
            return None
        nodes=[0]
        max_depth=30
    
        for moves in range(1,max_depth+1):#increase the depth of the graph if a solution couldn't be found. 
            depth=0
            visited=self.visited
            start_time_for_layers = time.time()#start timer only for printing purposes.
            solution=iddfs(start_state,goal_state,depth,moves,[start_state],nodes)
            end_time_for_layers = time.time()#end timer only for printing purposes.
            print('layer:',moves,f'(took:{round(end_time_for_layers-start_time_for_layers , 2)} sec)')#printing the new max allowed layer number and the spent time. 
            if solution is not None:#result handling
                end_time = time.time()
                elapsed_time = (end_time - start_time)#calculated the time has spent.
                return start_state2,1,moves,nodes,elapsed_time
            elif solution==None and moves==30:
                end_time = time.time()
                elapsed_time = (end_time - start_time)#calculated the time has spent.
                return start_state2,0,moves,nodes,elapsed_time #return the desired values (return (start_state,solution,moves,nodes,time)) same as brief.
                

if __name__ == "__main__":
    obj=initialStates()
    a=obj.random_init_states()
    obj.print_init_states()

    goal_state=[1, 1, [[1, 2, 3], [8, 0, 4], [7, 6, 5]]]#defining the goal state
    csv_file_headers = ['Seed' , 'Case_id' , 'start_state' , 'solution' , 'moves' , 'nodes' , 'time(sec)'] #cvs file's headers

    for init_grid in range (len(a)):#running the IDDFS for each of the initial states
        obj3 = searching()
        print(f'SOLVING FOR ==>{a[init_grid]}')
        sol=list(obj3.solve_puzzle(a[init_grid],goal_state))#call solve function
        sol.insert(0,obj.seed)#add seed to csv file data
        sol.insert(1,init_grid+1)#add case number to csv file data
        csv_data=sol
        file_path= os.path.abspath('IDDFS_output.csv')
        with open(file_path , 'a' , newline='') as csvFile:#creating csv file.
            writer = csv.writer(csvFile)
            if init_grid==0:
                csvFile.truncate(0)
                writer.writerow(csv_file_headers)
            writer = csv.writer(csvFile)
            writer.writerow(csv_data)
             
        print('Solution==>',list(sol))
    
