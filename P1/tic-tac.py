import sys

sys.path.append("/home/bvillalb/miniconda3/envs/IA/lib/python3.10/site-packages/aima")

from aima.search import Problem, best_first_graph_search,astar_search

class TicTac(Problem):
    def __init__(self, initial):
        self.size_matrix = len(initial)
        # Convertir el estado inicial a tupla de tuplas
        self.initial = initial 
        self.x = 'x'
        self.o = 'o'
        super().__init__(self.initial)

    def actions(self, state):
        actions = []
        for i in range(self.size_matrix):
            for j in range(self.size_matrix):
                if state[i][j] == '_':
                    actions.append((i, j, 'o'))
                    actions.append((i, j, 'x'))
        return actions

    def result(self, state, action):
        row, col, value = action

        next_state = []
        final_state = []

        for r in state:
            new_row = list(r)  
            next_state.append(new_row)  

       
        next_state[row][col] = value

       
        final_state = []
        for new_row in next_state:
            final_state.append(tuple(new_row))

        
        return tuple(final_state)


    def goal_test(self, state):
        size = self.size_matrix
        
        # Para verificar el mismo número de 'o' en cada fila y columna
        expected_o_count = sum(row.count(self.o) for row in state) // size

        for i in range(size):
            # Verificar si el conteo de 'o' en la fila es correcto
            row_o_count = sum(1 for cell in state[i] if cell == self.o)
            if row_o_count != expected_o_count:
                return False

            # Verificar si el conteo de 'o' en la columna es correcto
            col_o_count = sum(1 for j in range(size) if state[j][i] == self.o)
            if col_o_count != expected_o_count:
                return False

            # Comprobar que no haya más de dos 'x' o 'o' consecutivos en filas
            for j in range(size - 2):
                if state[i][j] == state[i][j + 1] == state[i][j + 2] != '_':
                    return False

            # Comprobar que no haya más de dos 'x' o 'o' consecutivos en columnas
            for j in range(size - 2):
                if state[j][i] == state[j + 1][i] == state[j + 2][i] != '_':
                    return False

            for row in state:
                if '_' in row:
                    return False


        return True


    def function_evaluation(self, node):
        score = 1

        return score
    
    def heuristic(self, node):
        state = node.state  # Extrae el estado del nodo
        score = 0
        
        # Contar espacios vacíos
        empty_spaces = sum(1 for row in state for cell in row if cell == '_')
        score -= empty_spaces  # Penaliza por espacios vacíos


        return score




def read_input():
    matrix = []
    n_elements = 0

    # Lee todas las líneas de entrada hasta que se complete la matriz
    for line in sys.stdin:
        line = line.strip()  # Quitar posibles espacios en blanco al inicio y final
        if line:  # Evitar líneas vacías
            n_elements += len(line)
            matrix.append(tuple(line))  # Convierte cada línea en una tupla de caracteres

            # Si la cantidad de elementos leídos es igual a la longitud de la línea al cuadrado, finaliza
            if n_elements >= len(line) ** 2:
                break

    return tuple(matrix)  # Devuelve la matriz como una tupla de tuplas

def main():
    initial_state = read_input()
    tictac = TicTac(initial_state)

    solution = astar_search(tictac,tictac.heuristic)

    #solution = best_first_graph_search(tictac, tictac.function_evaluation)

    if solution:
        final_state = solution.state  # Estado final de la solución
        for row in final_state:
            print(''.join(row))
        
    else:

        print('No hay solucion')

if __name__ == "__main__":
    main()
