import random
import ast
import copy
import pandas as pd
import time
import timeit
####################################################################
##################  SETTING UP THE INITIAL STATES  #################
####################################################################

class initialStates():

    def __init__(self) :

        self.tile_num=8# assuming that all different sizes are squire of a number. (16x16 , 9x9 , 5x5, ...)
        self.initial_state = list(reversed(range(self.tile_num+1)))# template _state from given in the CW_1 brief.
        self.states = []#all random initial states will be in this array.

    def random_init_states(self):

        random.seed(97)# my students ID's last 3 three digits are 097. That's why I used 97 only.
        for _ in range(10):#creating 10 initial state with the same seed value.
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
        return(self.states)
    
    def print_init_states(self):
        print('\n *INITIAL STATES* \n')
        for v in range(len(self.states)):
            print(self.states[v])
            
##########################################################################
##################  SETTING UP THE GRAPH DATA STRUCTURE  #################
##########################################################################
class graph():

    def __init__(self , is_directed=True):
        self.graph = {}#the graph will be constructed in this dict.
        self.graph_type = is_directed#the type of the graph(directed or undirected)

    def add_node(self,node):#add node to the graph
        if str(node) not in self.graph:
            self.graph[str(node)] = []
            
    def connect_nodes(self,node1,node2):#connects the nodes by taking the graph_type in to consideration.
        if str(node2) not in self.graph[str(node1)]:
            self.graph[str(node1)].append(str(node2))
        
        if not self.graph_type:
            self.graph[str(node2)].append(str(node1))
    
    def graph_print(self):#prints the graph in the dict form(left side=the node     and      right side=neighabours of that node)
        print('\n *GRAPH* \n')
        for i in self.graph:
            print('{',i,'} ===> ' , self.graph[i])

##########################################################################
##################  SEARCHİNG FOR THE GOAL STATE  ########################
##########################################################################
 
class searching(graph , initialStates):
    #this code block has been taken from the lecture slides.
     
    def move_blank(self,i,j,n):
        if i+1 < n:
            yield (i+1,j)
        if i-1 >= 0:
            yield (i-1,j)
        if j+1 < n:
            yield (i,j+1)
        if j-1 >= 0:
            yield (i,j-1)
        
    def move(self,state):
        [i,j,grid]=state
        n = len(grid)
        list_grid=list(grid)

        for pos in self.move_blank(i,j,n):
            i1,j1 = pos
            list_grid[i][j], list_grid[i1][j1] = list_grid[i1][j1], list_grid[i][j]#swap the blank tile
            
            yield [i1,j1,list_grid]

            list_grid[i][j], list_grid[i1][j1] = list_grid[i1][j1], list_grid[i][j] #restore the grid
    
    def dfs(self, graph, root , goal) :
        
            # visited.add(str(root)) 
                    
            for self.neighbour in graph[str(root)]: 
                
                if self.neighbour == goal:
                    
                    return self.neighbour
                else:
                    result = self.dfs( graph, self.neighbour, goal)
                    if result is not None:
                       return result# terminate the suspended node search

    
    def solve_puzzle(self , start_state , goal_state):
        self.add_node(start_state) #adding the root to the graph.
        layer =[]
        layer.append(start_state)
        
        max_layer=30
        counter =0
        while max_layer>0:  
            
            for a in range(counter,len(layer)):
                
                copied_L = copy.deepcopy(layer[a])
               
                for next_state in self.move(layer[a]):
                    
                    self.add_node(next_state)

                    if  next_state not in layer:

                        self.connect_nodes(copied_L, next_state)
                        layer.append(copy.deepcopy(next_state))
                counter+=1
                    
            #end of layer
            solution=self.dfs( self.graph, start_state , goal_state)
            
            print(max_layer)
            if [1, 1, [[1, 2, 3], [8, 0, 4], [7, 6, 5]]] in layer:
               print(True)  
            if solution is not None:
                return (start_state,solution)
              
            max_layer=max_layer-1
        #self.graph_print()
           
if __name__ == "__main__":
   
    
    obj=initialStates()
    a=obj.random_init_states()
    obj.print_init_states()

    obj3 = searching()
    sol=obj3.solve_puzzle(a[4],'[1, 1, [[1, 2, 3], [8, 0, 4], [7, 6, 5]]]')
    print(sol)
    
    

