import sys

sys.path.append("/usr/lib/python3/dist-packages/aima-python")

from search import Problem, best_first_graph_search

class TicTac(Problem):
    """
    Definición del problema TicTac, modelando el juego de Tic-Tac en un tablero cuadrado.
    Permite definir el estado inicial, obtener acciones válidas, y verificar si se ha alcanzado el objetivo del juego.
    """

    def __init__(self, initial):
        """
        Inicializa el estado inicial del problema TicTac, tamaño del tablero y la definición de los símbolos.
        
        Args:
            initial: estado inicial del problema representando el tablero.

        Returns:
            None
        """
        self.size_matrix = len(initial)
        self.initial = initial 
        self.x = 'x'
        self.o = 'o'
        self.empty = '_'

    def actions(self, state):
        """
        Define las posibles acciones en cada estado. Se recorre el tablero, y si la posición es vacía se añade
        en las acciones la posición (fila, columna) y el valor del símbolo.

        Args:
            state: el estado actual del tablero.

        Returns:
            list: lista de acciones posibles en el estado actual.
        """
        actions = []
        for i in range(self.size_matrix):
            for j in range(self.size_matrix):
                if state[i][j] == self.empty:
                    actions.append((i, j, self.o))  
                    actions.append((i, j, self.x))  
        return actions

    def result(self, state, action):

        """
        Genera el resultado de aplicar un acción en el estado actual, creando un nuevo estado con la accion que se ha aplicado. 

        Args:
            state: estado actual del tablero
            action: accion que se quiere aplicar, representada como (fila, columna, simbolo). 

        Returns:
            tuple: nuevo estado del tablero despues de aplicar dicha accion.
        """
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
        """
        Verifica si el estado actual cumple con las condiciones/restricciones en el problema Tic-Tac. Cada fila y columna del tablero debe tener 
        el mismo número de 'o', no debe haber más de dos símbolos consecutivos iguales.

        Args: 
            state: estado actual del tablero

        Returns:
            bool: True si el estado cumple todas las condiciones, False en caso contrario.
        """
        size = self.size_matrix
        total_o = 0

        #--Calcular el número total de 'o' en el tablero
        for row in state:
            total_o += row.count(self.o)

        #--Calcular el número esperado de 'o' en filas y columnas
        expected_o_count = total_o // size

        for i in range(size):
            #--Verificar si el conteo de 'o' en la fila es correcto
            row_o_count = state[i].count(self.o)
            if row_o_count != expected_o_count:
                return False

            #--Verificar si el conteo de 'o' en la columna es correcto
            col_o_count = sum(1 for j in range(size) if state[j][i] == self.o)
            if col_o_count != expected_o_count:
                return False


            #--Comprobar que no haya más de dos símbolos consecutivos en filas
            for j in range(size - 2):
                if (state[i][j] != self.empty and state[i][j] == state[i][j + 1] and state[i][j] == state[i][j + 2]):
                    return False

            #--Comprobar que no haya más de dos símbolos consecutivos en columnas
            for j in range(size - 2):
                if (state[i][j] != self.empty and state[i][j] == state[j + 1][i] and state[i][j] == state[j + 2][i]):
                    return False

            #--Verificar posiciones vacias
            for row in state:
                if self.empty in row:
                    return False

        return True

    def function_evaluation(self, node):
        """
        La función de evaluación devuelve un valor constante de 1, lo que significa que no se está aplicando ninguna 
        función heurística para la priorización de estados, ya que estamos utilizando un algoritmo de búsqueda no informada (BFS).
        """
        return 1 

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
    """
    Se utiliza una busqueda no informada aplicando el algoritmo de Busqueda por Anchura (BFS) ya que se trata de un problema relativamente sencillo en 
    el que se busca encontrar una solucion rapidamente en tableros de tamaño pequeño. BFS permite explorar todas las configuraciones posibles
    de manera exhaustiva, asegurando que se consideren todas las jugadas antes de avanzar a niveles más profundos. Ademas, su implementacion es sencilla 
    lo que facilita el diseño del problema. 

    Sin embargo, si el espacio de estados incrementa, como en tableros más grandes, sería interesante considerar el uso de busquedas informadas. Estas 
    busquedas pueden utilizar funciones heuristicas para dirigir la busqueda de manera mas eficiente, reducindo el numero de estados explorados 
    y optimizando el proceso de encontrar la solución. 

    Adicionalmente, tambien se podria utilizar busquedas locales ya que en estos casos no siempre se busca la mejor combinacion de movimientos, sino 
    llegar a una solucion. 
    """

    initial_state = read_input()
    tictac = TicTac(initial_state)

    solution = best_first_graph_search(tictac, tictac.function_evaluation)

    if solution:
        final_state = solution.state 
        for row in final_state:
            print(''.join(row))
    else:
        print('No hay solución')

if __name__ == "__main__":
    main()
