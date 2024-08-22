import heapq
import time
#import matplotlib.pyplot as plt

#En esta clase se calcula el g(n)
class estadoTablero:
    def __init__(self, board, g=0, parent=None):
        self.board = board
        self.g = g  # Costo desde el inicio hasta este nodo
        self.parent = parent  # Nodo padre para reconstruir el camino

    def __eq__(self, other):
        return self.board == other.board

    def __hash__(self):
        return hash(str(self.board))

    # Comparación de Estados, Esta función calcula f(n)=g(n)+h(n)
    def __lt__(self, other):
        return (self.g + heuristica(self)) < (other.g + heuristica(other))

    def is_goal(self):
        # Comprueba si el tablero está en el estado objetivo
        return self.board[3][3] == '*' and sum(row.count('*') for row in self.board) == 1

def get_legal_moves(estado):
    directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
    movimientos_permitidos = []
    
    for r in range(7):
        for c in range(7):
            if estado.board[r][c] == '*':
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    mr, mc = r + dr // 2, c + dc // 2
                    if 0 <= nr < 7 and 0 <= nc < 7 and estado.board[nr][nc] == 'o' and estado.board[mr][mc] == '*':
                        nuevo_tablero = [row[:] for row in estado.board]
                        nuevo_tablero[r][c] = 'o'
                        nuevo_tablero[mr][mc] = 'o'
                        nuevo_tablero[nr][nc] = '*'
                        movimientos_permitidos.append(estadoTablero(nuevo_tablero, estado.g + 1, estado))
    return movimientos_permitidos

# Acá se calcula el h(n)
def heuristica(estado):
    # Heurística: Número de piezas restantes - 1
    return sum(row.count('*') for row in estado.board) - 1

def a_estrella(estado_inicial):
    open_list = []
    closed_set = set()

    heapq.heappush(open_list, (heuristica(estado_inicial), estado_inicial))

    while open_list:
        _, estado_actual = heapq.heappop(open_list)

        if estado_actual.is_goal():
            return estado_actual

        closed_set.add(estado_actual)

        for movimiento in get_legal_moves(estado_actual):
            if movimiento not in closed_set:
                closed_set.add(movimiento)  # Añadir el movimiento a closed_set para evitar ciclos
                # Inserción en la Cola de Prioridad 
                # Cada vez que se inserta un estado en la cola de prioridad, se calcula 𝑓(𝑛)f(n).
                heapq.heappush(open_list, (movimiento.g + heuristica(movimiento), movimiento))
    
    return None

def reconstruct_path(estado):
    path = []
    while estado:
        path.append(estado)
        estado = estado.parent
    return path[::-1]

def print_board(board):
    for row in board:
        print(' '.join(c if c else ' ' for c in row))
    print()

    """
def plot_performance(times, moves, labels):
    fig, ax1 = plt.subplots()

    # Configuración para el tiempo de ejecución
    color = 'tab:green'
    ax1.set_xlabel('Test Case')
    ax1.set_ylabel('Execution Time (seconds)', color=color)
    ax1.plot(labels, times, color=color, marker='o', label='Execution Time')
    ax1.tick_params(axis='y', labelcolor=color)

    # Configuración para la cantidad de movimientos
    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('Number of Moves', color=color)
    ax2.plot(labels, moves, color=color, marker='x', label='Number of Moves')
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()
    plt.title('Performance of A* Algorithm')
    plt.show()

    """

if __name__ == "__main__":
    # Definir diferentes configuraciones iniciales para pruebas
    test_cases = [
        [
            [None, None, '*', '*', '*', None, None],
            [None, None, '*', '*', '*', None, None],
            ['*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', 'o', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*'],
            [None, None, '*', '*', '*', None, None],
            [None, None, '*', '*', '*', None, None]
        ],
        # Agrega más configuraciones si es necesario
    ]

    execution_times = []
    move_counts = []
    labels = []

    for idx, initial_board in enumerate(test_cases):
        print(f"\n----------------------------------")
        print(f"\nTesting case {idx + 1}...")
        estado_inicial = estadoTablero(initial_board)

        print("Initial board estado:")
        print_board(initial_board)  # Imprimir el tablero inicial

        start_time = time.time()
        goal_state = a_estrella(estado_inicial)
        end_time = time.time()

        if goal_state:
            path = reconstruct_path(goal_state)
            num_moves = len(path) - 1
            print(f"Number of moves: {num_moves}")
            move_counts.append(num_moves)
            print("Final board estado:")
            print_board(goal_state.board)  # Imprimir el tablero final
        else:
            print("No solution found")
            move_counts.append(None)  # No hay solución

        execution_time = end_time - start_time
        print(f"Execution time for test case {idx + 1}: {execution_time:.2f} seconds")
        execution_times.append(execution_time)
        labels.append(f"Case {idx + 1}")

    # Graficar el desempeño
    #plot_performance(execution_times, move_counts, labels)
