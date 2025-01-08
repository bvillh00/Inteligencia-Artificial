import sys
sys.path.append("/home/bvillalb/aima-python")
from csp import CSP, backtracking_search

class TicTacCSP(CSP):
    def __init__(self, initial):
        self.size_matrix = len(initial)
        self.initial_state = initial
        self.x = 'x'
        self.o = 'o'
        self.empty = '_'

        variables = self.create_variables()

        domains = {var: [self.x, self.o] for var in variables}

        neighbors = self.create_neighbors(variables)

        CSP.__init__(self, variables, domains, neighbors, self.constraints)


    def create_variables(self):
        variables = []
        for i in range(self.size_matrix):
            for j in range(self.size_matrix):
                if self.initial_state[i][j] == self.empty:
                    variables.append((i, j))
        return variables
    
    def create_domains(self,variables):

        domains = {}
        for var in variables:
            domains[var] = [self.x, self.o]

        return domains
    
    def create_neighbors(self,variables):
        neighbors = {}
        for var in variables:
            i, j = var
            neighbors[var] = []
            for k in range(self.size_matrix):
                if k != j:
                    neighbors[var].append((i, k))
                if k != i:
                    neighbors[var].append((k, j))

        return neighbors

    def constraints(self, A, a, B, b):
        current_state = [list(row) for row in self.initial_state]
        current_state[A[0]][A[1]] = a
        current_state[B[0]][B[1]] = b

        def fill_empty_positions(state):
            all_positions = []
            for i in range(self.size_matrix):
                for j in range(self.size_matrix):
                    if state[i][j] == self.empty:
                        all_positions.append((i, j))

            if not all_positions:
                return state

            combinations = []
            def generate_combinations(remaining_positions):
                if not remaining_positions:
                    return [[]]
                current_pos = remaining_positions[0]
                rest_combinations = generate_combinations(remaining_positions[1:])
                return [[self.x] + comb for comb in rest_combinations] + [[self.o] + comb for comb in rest_combinations]

            combinations = generate_combinations(all_positions)
            for combination in combinations:
                temp_state = [row[:] for row in state]
                for idx, pos in enumerate(all_positions):
                    temp_state[pos[0]][pos[1]] = combination[idx]

                if verify_constraints(temp_state):
                    return temp_state

            return False

        def verify_constraints(temp_state):
            expected_o_count = sum(1 for row in temp_state for cell in row if cell == self.o) // self.size_matrix

            for i in range(self.size_matrix):
                row_o_count = 0
                for j in range(self.size_matrix):
                    if temp_state[i][j] == self.o:
                        row_o_count += 1
                if row_o_count != expected_o_count:
                    return False

                col_o_count = 0
                for k in range(self.size_matrix):
                    if temp_state[k][i] == self.o:
                        col_o_count += 1
                if col_o_count != expected_o_count:
                    return False

                for j in range(self.size_matrix - 2):
                    if temp_state[i][j] != self.empty and temp_state[i][j] == temp_state[i][j + 1] == temp_state[i][j + 2]:
                        return False
                    if temp_state[j][i] != self.empty and temp_state[j][i] == temp_state[j + 1][i] == temp_state[j + 2][i]:
                        return False

            return True

        filled_state = fill_empty_positions(current_state)

        if filled_state is False:
            return False

        return True

    def display_solution(self, assignment):
        size = self.size_matrix
        final_state = [[self.initial_state[i][j] for j in range(size)] for i in range(size)]

        for (i, j), val in assignment.items():
            final_state[i][j] = val

        for row in final_state:
            print(''.join(row))

def read_input():
    """
    Se lee de la entrada por terminal, almacenando los valores del tablero. Se termina la lectura si el número de 
    elementos introducidos es mayor o igual al tamaño de la matriz (matriz cuadrada).
    
    Args: 
        None

    Returns:
        tuple: La matriz cuadrada formada para comenzar el problema.
    """
    matrix = []
    n_elements = 0

    for line in sys.stdin:
        #--Eliminación de espacios en blanco
        line = line.strip() 
        if line:
            n_elements += len(line)
            matrix.append(tuple(line)) 

            if n_elements >= len(line) ** 2:
                break

    return tuple(matrix)

def main():
    initial_state = read_input()
    tictac_csp = TicTacCSP(initial_state)

    solution = backtracking_search(tictac_csp)

    if solution:
        print("Solución encontrada:")
        tictac_csp.display_solution(solution)
    else:
        print('No hay solución')

if __name__ == "__main__":
    main()
