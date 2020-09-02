# ParsaMazaheri 
import pygame 
import pandas as pd

pygame.init()
SIZE = (640, 480)
screen = pygame.display.set_mode(SIZE, pygame.RESIZABLE)
screen.fill((255,255,255))
pygame.display.set_caption("NFA to DFA")
font = pygame.font.SysFont("courier new", 18, bold=True)
pygame.display.update()

# --- Global constants --- #
coordinate = []
final_states = []
radius = 18
n, t = 4, 2 

# SAMPLE DATA 
# nfa = {'A': {'a': ['A', 'B'], 'b': ['A']}, 'B': {'a': ['C'], 'b': ['C']}, 'C': {'a': ['D'], 'b': ['D']}, 'D': {'a': [], 'b': []}}

# OUTPUT
# dfa ={} {'A': {'a': 'AB', 'b': 'A'}, 
        #'AB': {'a': 'ABC', 'b': 'AC'}, 
        #'ABC': {'a': 'ABCD', 'b': 'ACD'}, 
        #'AC': {'a': 'ABD', 'b': 'AD'}, 
        #'ABCD': {'a': 'ABCD', 'b': 'ACD'}, 
        #'ACD': {'a': 'ABD', 'b': 'AD'}, 
        #'ABD': {'a': 'ABC', 'b': 'AC'}, 
        #'AD': {'a': 'AB', 'b': 'A'}}

def NFAtoDFA():
    option = int(input("0: sample data    1: input\n")) 
    if option == 0:
        n, t = 4, 2 
        nfa = {'A': {'a': ['A', 'B'], 'b': ['A']}, 'B': {'a': ['C'], 'b': ['C']}, 'C': {'a': ['D'], 'b': ['D']}, 'D': {'a': [], 'b': []}}
    else:                             
        n = int(input("No. of states : "))            #Enter total no. of states
        t = int(input("No. of transitions : "))       #Enter total no. of transitions/paths eg: a,b so input 2 for a,b,c input 3
        for i in range(n):  
            state = input("state name : ")            #Enter state name eg: A, B, C, q1, q2 ..etc
            nfa[state] = {}                           #Creating a nested dictionary
            for j in range(t):
                path = input("path : ")               #Enter path eg : a or b in {a,b} 0 or 1 in {0,1}
                print("Enter end state from state {} travelling through path {} : ".format(state,path))
                reaching_state = [x for x in input().split()]  #Enter all the end states that 
                nfa[state][path] = reaching_state     #Assigning the end states to the paths in dictionary
    
    print("\nPrinting NFA table : ")
    print(pd.DataFrame(nfa).transpose())

    print("Enter final state of NFA : ")
    nfa_final_state = [x for x in input().split()]      # Enter final state/states of NFA
    ###################################################                 
        
    new_states_list = []                          #holds all the new states created in dfa
    dfa = {}                                      #dfa dictionary/table or the output structure we needed
    keys_list = list(list(nfa.keys())[0])         #conatins all the states in nfa plus the states created in dfa are also appended further
    path_list = list(nfa[keys_list[0]].keys())    #list of all the paths eg: [a,b] or [0,1]

    ###################################################

    # Computing first row of DFA transition table

    dfa[keys_list[0]] = {}                        #creating a nested dictionary in dfa 
    for y in range(t):
        var = "".join(nfa[keys_list[0]][path_list[y]])   #creating a single string from all the elements of the list which is a new state
        dfa[keys_list[0]][path_list[y]] = var            #assigning the state in DFA table
        if var not in keys_list:                         #if the state is newly created 
            new_states_list.append(var)                  #then append it to the new_states_list
            keys_list.append(var)                        #as well as to the keys_list which contains all the states
            
    ###################################################
    
    # Computing the other rows of DFA transition table

    while len(new_states_list) != 0:                     #consition is true only if the new_states_list is not empty
        dfa[new_states_list[0]] = {}                     #taking the first element of the new_states_list and examining it
        for _ in range(len(new_states_list[0])):
            for i in range(len(path_list)):
                temp = []                                #creating a temporay list
                for j in range(len(new_states_list[0])):
                    temp += nfa[new_states_list[0][j]][path_list[i]]  #taking the union of the states
                s = ""
                s = s.join(temp)                         #creating a single string(new state) from all the elements of the list
                if s not in keys_list:                   #if the state is newly created
                    new_states_list.append(s)            #then append it to the new_states_list
                    keys_list.append(s)                  #as well as to the keys_list which contains all the states
                dfa[new_states_list[0]][path_list[i]] = s   #assigning the new state in the DFA table
            
        new_states_list.remove(new_states_list[0])       #Removing the first element in the new_states_list

    print("\nPrinting DFA table :- ")
    print(pd.DataFrame(dfa).transpose())

    dfa_states_list = list(dfa.keys())
    dfa_final_states = []
    for x in dfa_states_list:
        for i in x:
            if i in nfa_final_state:
                dfa_final_states.append(x)
                break
            
    print("\nFinal states of the DFA : ",dfa_final_states)       #Printing Final states of DFA
    
    return dfa, dfa_final_states


def DrawDFA(coord, dfa, final):   
    getPos(dfa)                         # node positions
    states = list(list(dfa.keys()))     # assign a number to each state
    for i in range(len(states)):
        drawNode(i, states, final)      # draw node    
        drawEdges(i, states, dfa)       # draw transactions
        pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

# darw node (state) 
def drawNode(i, states, final):
    pos = coordinate[i]
    if (isFinalState(i, states, final)):
        pygame.draw.circle(screen, pygame.Color('blue'), pos, radius, 1)
    else:
        pygame.draw.circle(screen, pygame.Color('red'), pos, radius, 1)

    word = font.render(states[i], 0, pygame.Color('black'))
    screen.blit(word, (pos[0]- 7, pos[1] - 7))

# darwing edges (transactions)
def drawEdges(i, states, dfa):
    s1 = states[i]

    for tran in dfa[s1]:
        s2 = dfa[s1][tran]
        j = getIndex(s2, states)
        pygame.draw.line(screen, pygame.Color('gray'), coordinate[i], coordinate[j], 1)
        # neveshtn a ,b roye felesh ha
        pos = ((coordinate[i][0] + coordinate[j][0])/2 , (coordinate[i][1] + coordinate[j][1])/2)
        word = font.render(tran, 0, pygame.Color('black'))
        screen.blit(word, (pos[0]- 7, pos[1] - 7))

# get node positions 
def getPos(dfa):
    print('Select {} points to place the nodes'.format(len(dfa)))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or len(coordinate) == len(dfa):
                return 
            if event.type == pygame.MOUSEBUTTONDOWN: 
                coordinate.append(event.pos)
                pygame.draw.circle(screen, pygame.Color('red'), event.pos, radius, 1)
                pygame.display.update()

def isFinalState(i, states, final):
    for s in final:
        if(states[i] == s):
            return True
    return False 

def getIndex(s2, states):
    for i in range(len(states)):
        if states[i] == s2:
            return i

if __name__ == "__main__":
    DFA, final = NFAtoDFA()
    DrawDFA(coordinate, DFA, final)
    

