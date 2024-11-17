import sys
sys.path.append("/home/bvillalb/aima-python")

from games4e import Game, GameState, alpha_beta_search,alpha_beta_cutoff_search,minmax_decision
import time

class BoardGame(Game):
    def __init__(self, n):

        """
        Modelización del problema del juego sin nombre llamado BoardGame 

        Args: 
            n: el tamaño del tablero (n x n)

        Attributes:
            n : tamaño del tablero 
            board: tablero inicial del juego calculando con el metodo initial_state 
            moves: movimientos posibles de cada jugador, comenzando el juego con el jugador 1
            initial (GameState): definicion del estado inicial del juego incluyendo el turno de cada jugador comenzando
                                 con el jugador 1, la utilidad siendo al comienzo 0, el tablero y los movimientos posibles
        """
        self.n = n
        board = self.initial_state()
        moves = self.calculate_moves(board, 'P1')
        self.initial = GameState(to_move='P1', utility=0, board=board, moves=moves)

    def initial_state(self):

        """
        Crear el estado inicial del tablero del juego y posicionar a cada jugador en el tablero. 

        En primer lugar se define el tablero teniendo en cuenta los bordes extras alrededor y se posiciona 
        a los jugadores en cada sitio. El jugador 1 en el borde izquierdo y el jugador 2 en el borde superior
        """

        #--Crear un tablero con borde extra
        size = self.n + 2
        board = []
        for _ in range(size):
            row = [] 
            for _ in range(size):
                row.append(" ")
            board.append(row)

        #--Colocar fichas del jugador 1 en el borde izquierdo
        for i in range(1, self.n + 1):
            board[i][0] = 'P1'
        #--Colocar fichas del jugador 2 en el borde superior
        for j in range(1, self.n + 1):
            board[0][j] = 'P2'
        return board

    def actions(self, state):

        """
        Calcula las acciones/movimientos posibles correspondiente al estado actual en que te encuentres. 

        Si no hay movimientos validos para ese jugador se pasa el turno y sigue el otro jugador

        Args: 
            state: estado actual del juego

        Returns: 
            list: Si hay movimientos validos se devuelve una lista de movimientos para ese jugador si no se retorna 
                  una lista vacia 
        """

        moves = self.calculate_moves(state.board, state.to_move)

        if not moves:
            #--Paso de turno
            return [None]
        else:

            return moves

    def calculate_moves(self, board, player):

        """
        Calcula los movimientos posibles dependiendo del jugador que este jugando, teniendo en cuenta 
        los movimientos simples siendo estos horizontales o verticales y saltos a la ficha del jugador contrario

        Args:
            board: tablero
            player: jugador

        Returns: 
            list: movimientos posibles en el tablero del juego teniendo en cuenta la posicion, la direccion y 
                  el jugador que juega
        """

        moves = []
        directions = []

        if player == 'P1':
            directions.append((0,1))

        else:
            directions.append((1,0))
        
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == player:
                    for direction in directions:
                        moves += self.piece_moves(board, i, j, direction, player)
        return moves

    def piece_moves(self, board, i, j, direction, player):
        """
        Calculo de los movimientos posibles para una ficha dependiendo del jugador en una direccion dada

        En primer lugar, se verifica los movimientos simples, es decir, movimientos horizontales o verticales 

        En segundo lugar, se verifica los movimientos de saltos entre las fichas de los jugadores, es decir, 
        el salto del oponente. Si P1 quiere saltar a P2 o P2 quiere saltar a P1. 

        Args: 
            board: tablero 
            i: posicion de la fila del tablero
            j: posicion de la columna del tablero 
            direction: lista de direcciones horizontales o verticales [(0,1) o (1,0)]
            player: jugador 

        Returns: 
            list: movimientos posibles del jugador
        """
        moves = []

        #--Movimiento simple
        di, dj = direction
        ni, nj = i + di, j + dj
        if self.is_empty_square(board, ni, nj):
            moves.append(((i, j), (ni, nj)))

        #--Salto sobre ficha oponente
        oi, oj = i + di, j + dj
        si, sj = i + 2*di, j + 2*dj
        if self.is_oponent_piece(board, oi, oj, player) and self.is_empty_square(board, si, sj):
            moves.append(((i, j), (si, sj)))
        return moves

    def is_empty_square(self, board, i, j):

        """
        Verifica si la casilla esta libre para poder tener un movimiento valido, teniendo en 
        cuenta los limites del tablero (fila,columna) y la casilla este vacía. 

        En caso contrario devuelve un False

        Args: 
            board: tablero 
            i: posicion de la fila del tablero
            j: posicion de la columna del tablero

        Returns: 
            bool: True si la casilla esta vacía y False cuando no
        """

        if ((0 <= i < len(board) )and (0 <= j < len(board[0])) and (board[i][j] == ' ')):
            return True

        else:
            return False
        

    def is_oponent_piece(self, board, i, j, player):

        """
        Verificar si en esa casilla hay una pieza del jugador contrario, teniendo en cuenta los 
        limites del tablero y si hay una ficha del jugador contrario. 

        En caso contrario devuelve un False

        Args: 
            board: tablero 
            i: posicion de la fila del tablero
            j: posicion de la columna del tablero
            player: jugador 

        Returns: 
            bool: True si la casilla esta ocupada por el jugador contrario y False cuando no 

        """

        opponent = ""

        if player == "P1":
            opponent = "P2"

        else:
            opponent = "P1"
       
        if ((0 <= i < len(board) )and (0 <= j < len(board[0])) and (board[i][j] == opponent)):
            return True

        else:
            return False

    def result(self, state, move):

        """
        Genera el resultado de aplicar una acción en el estado actual después de que un jugador aplique un movimiento 
        o pase de turno. Se verifica el paso de turno del jugador contrario o el resultado de aplicar el movimiento 
        en ese estado actual para ese jugador

        Args: 
            state:estado actual del juego
            move: accion que se quiere aplicar para el estado actual. 

        Returns: 
            GameState: un nuevo estado de juego con el siguiente jugador, la utilidad nueva calculada, el tablero 
                       actualizado y los movimientos posibles para el siguiente jugador

        """

        if move is None:
            # Si el movimiento es None, el jugador pasa su turno
            next_player = ""
            if state.to_move == "P1":
                next_player = "P2"

            else:
                next_player = "P1"

            movimientos = self.calculate_moves(state.board, next_player)
            return GameState(to_move=next_player, utility=state.utility, board=state.board, moves=movimientos)

        else:
            next_player = ""
            from_pos, to_pos = move
            i, j = from_pos
            ni, nj = to_pos

            player = state.to_move

            new_board = []

            for row in state.board:
                new_board.append(row[:])

            new_board[i][j] = " "
            new_board[ni][nj] = player

            utility = self.calculate_utility(new_board, player)

            if player == "P1":
                next_player = "P2"

            else:
                next_player = "P1"

            moves = self.calculate_moves(new_board,next_player)

            return GameState(to_move=next_player,utility=utility,board=new_board,moves=moves)

    def calculate_utility(self, board, player):

        """
        Calculo de la utilidad del tablero para determinar si un jugador ha ganado o no. 

        Se verifica primero si el Jugador 1 ha ganado colocando un valor de utilidad 1 y si ha ganado el Jugador 2 
        su valor de utilidad es -1.

        Si no ha ganado ninguno la utilidad sera de un valor 0

        Args: 
            board: tablero 
            player: jugador

        Returns:
            int: la utilidad indicando si ha ganado el jugador o no.
        """
        n = self.n

        # Verificar si el jugador ha ganado
        if player == 'P1':
            for i in range(1, n + 1):
                if board[i][n + 1] != 'P1':
                    return 0
            return 1 
        else:
            for j in range(1, n + 1):
                if board[n + 1][j] != 'P2':
                    return 0
            return -1

    def utility(self, state, player):

        """
        Evalua la utilidad de un estado del juego dependiendo del jugador que este jugando. 

        Args: 
            state: estado actual del juego
            player: jugador

        Returns:
            int: la utilidad del estado dependiendo del jugador que este jugando 
                 Si es J1 retorna la utilidad tal como esta en el estado 
                 Si es J2 retorna la utilidad negativa ya que es vista desde el jugador contrario

        """

        if player == "P1":
            return state.utility

        else:
            return -state.utility

    def terminal_test(self, state):
        """
        Comprueba si el juego ha terminado. El juego ha terminado cuando un jugador ha ganado u se produce un empate 

        Args: 
            state: el estado actual del juego

        Returns: 
            bool: si el juego ha terminado devuelve un True, en caso contrario un False
        """

        #-- Si un jugador ha ganado
        if state.utility != 0: 
            return True

        #--Si no hay movimientos validos para ambos jugadores
        not_moves_p1 = not self.calculate_moves(state.board,"P1")
        not_moves_p2 = not self.calculate_moves(state.board,"P2")

        if not_moves_p1 and not_moves_p2:
            return True

        return False


    def to_move(self, state):

        """
        Determina a que jugador le toca jugar en el estado actual del juego. 

        Args: 
            state: el estado actual del juego 

        Returns:
            str: el jugador que le toca jugar (P1 o P2)
        """

        return state.to_move

    def display(self, state):
        """
        Muestra el estado actual del tablero de juego, mostrando las posiciones de los jugadires y 
        las posiciones vacias y sus bordes

        Args:
            state: el estado actual del juego
        """

        board = state.board
        size = len(board)

        print("Tablero:")

        for i in range(size):
            row = ''
            for j in range(size):

                square = board[i][j]

                if square == ' ':
                    row += ' . '
                elif square == 'P1':
                    row += ' 1 '
                elif square == 'P2':
                    row += ' 2 '
            print(row)
        print()


def player_alpha_beta_search(game, state):
    return alpha_beta_search(state, game)

def player_alpha_beta_cutoff_search(game, state):
    return alpha_beta_cutoff_search(state, game)


def player_minmax_decision(game, state):
    return minmax_decision(state, game)


def main():
    n = 4
    game = BoardGame(n)

    print("Configuración inicial del tablero:")
    game.display(game.initial)

    initial = time.time()
    actual_state = game.initial

    #--Juega el juego con ambos jugadores utilizando Poda Alfa-Beta
    while not game.terminal_test(actual_state):
        actual_player = game.to_move(actual_state)
        print(f"Turno del jugador {actual_player}")
        move = player_alpha_beta_cutoff_search(game, actual_state)
        actual_state = game.result(actual_state, move)
        game.display(actual_state)

    terminal = time.time()
    print(f"Tiempo de ejecución: {terminal - initial:.4f} segundos")

    #--Determina el resultado
    if actual_state.utility > 0:
        print("¡Gana el Jugador 1!")
    elif actual_state.utility < 0:
        print("¡Gana el Jugador 2!")
    else:
        print("¡Es un empate!")


if __name__ == '__main__':
    main()
    
