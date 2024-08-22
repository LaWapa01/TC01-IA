import heapq
import time
#import matplotlib.pyplot as plt

class BoardState:
    def __init__(self, board, g=0, parent=None):
        self.board = board
        self.g = g  # Costo desde el inicio hasta este nodo
        self.parent = parent  # Nodo padre para reconstruir el camino

    def __eq__(self, other):
        return self.board == other.board

    def __hash__(self):
        return hash(str(self.board))

    def __lt__(self, other):
        return (self.g + heuristic(self)) < (other.g + heuristic(other))

    def is_goal(self):
        # Comprueba si el tablero está en el estado objetivo
        return self.board[3][3] == '*' and sum(row.count('*') for row in self.board) == 1

def get_legal_moves(state):
    directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
    legal_moves = []
    
    for r in range(7):
        for c in range(7):
            if state.board[r][c] == '*':
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    mr, mc = r + dr // 2, c + dc // 2
                    if 0 <= nr < 7 and 0 <= nc < 7 and state.board[nr][nc] == 'o' and state.board[mr][mc] == '*':
                        new_board = [row[:] for row in state.board]
                        new_board[r][c] = 'o'
                        new_board[mr][mc] = 'o'
                        new_board[nr][nc] = '*'
                        legal_moves.append(BoardState(new_board, state.g + 1, state))
    return legal_moves

def heuristic(state):
    # Heurística: Número de piezas restantes - 1
    return sum(row.count('*') for row in state.board) - 1

def a_star(initial_state):
    open_list = []
    closed_set = set()

    heapq.heappush(open_list, (heuristic(initial_state), initial_state))

    while open_list:
        _, current_state = heapq.heappop(open_list)

        if current_state.is_goal():
            return current_state

        closed_set.add(current_state)

        for move in get_legal_moves(current_state):
            if move not in closed_set:
                closed_set.add(move)  # Añadir el movimiento a closed_set para evitar ciclos
                heapq.heappush(open_list, (move.g + heuristic(move), move))
    
    return None

def reconstruct_path(state):
    path = []
    while state:
        path.append(state)
        state = state.parent
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

    # Añadir etiquetas para los puntos
    for i, label in enumerate(labels):
        ax1.annotate(f"{times[i]:.2f}", (labels[i], times[i]), textcoords="offset points", xytext=(0,5), ha='center', color='tab:green')
        ax2.annotate(f"{moves[i] if moves[i] is not None else 'No Solution'}", (labels[i], moves[i] if moves[i] is not None else 0), textcoords="offset points", xytext=(0,-15), ha='center', color='tab:blue')

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
        [
            [None, None, '*', '*', '*', None, None],
            [None, None, '*', 'o', '*', None, None],
            ['*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*'],
            [None, None, '*', 'o', '*', None, None],
            [None, None, '*', '*', '*', None, None]
        ],
        [
            [None, None, '*', '*', '*', None, None],
            [None, None, '*', '*', '*', None, None],
            ['*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', 'o', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*'],
            [None, None, '*', '*', '*', None, None],
            [None, None, '*', '*', '*', None, None]
        ],
    ]

    execution_times = []
    move_counts = []
    labels = []

    for idx, initial_board in enumerate(test_cases):
        print(f"\n----------------------------------")
        print(f"\nTesting case {idx + 1}...")
        initial_state = BoardState(initial_board)

        print("Initial board state:")
        print_board(initial_board)  # Imprimir el tablero inicial

        start_time = time.time()
        goal_state = a_star(initial_state)
        end_time = time.time()

        if goal_state:
            path = reconstruct_path(goal_state)
            num_moves = len(path) - 1
            print(f"Number of moves: {num_moves}")
            move_counts.append(num_moves)
            print("Final board state:")
            print_board(goal_state.board)  # Imprimir el tablero final
        else:
            print("No solution found")
            move_counts.append(None)  # No hay solución

        execution_time = end_time - start_time
        print(f"Execution time for test case {idx + 1}: {execution_time:.2f} seconds")
        execution_times.append(execution_time)
        labels.append(f"Case {idx + 1}")

    # Graficar el desempeño
#    plot_performance(execution_times, move_counts, labels)
