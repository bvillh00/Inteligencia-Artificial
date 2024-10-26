import sys

sys.path.append("/home/bvillalb/aima-python")

from search import Problem

class TicTac(Problem):

    def __init__(self,initial):
        self.size_matrix = len(initial)
        self.goal = None

    def actions(self,state):
        actions = []
        for i in self.size_matrix:
            for j in self.size_matrix:
                if state[i][j] == '_':
                    actions.append((i,j),'x')
                    actions.append((i,j),'o')


        return actions

    def result(self,state,action):
        row,colum,value = action

        state[row][colum] = value
        return state

    def is_goal(self, state):
        
       pass
def read_input():

    matrix = []
    print("Introduzca la matriz de entrada (se supone que esta bien formada y es cuadrada):")
    n_elements = 0
    line=''

    while True:

        line = input()
        n_elements += len(line)
        matrix.append(line)

        if not(n_elements < len(line) ** 2):
            break

    return tuple(matrix)

    
def main():
    initial_state = read_input()




if __name__ == "__main__":
    main()

