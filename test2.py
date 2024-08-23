import heapq
import time
#import matplotlib.pyplot as plt

#En esta clase se calcula el g(n)
class estadoTablero:
    def __init__(actual, tablero, g=0, padre=None):
        actual.tablero = tablero
        actual.g = g  # Costo desde el inicio hasta este nodo
        actual.padre = padre  # Nodo padre para reconstruir el camino

    def __eq__(actual, otro):
        return actual.tablero == otro.tablero

    def __hash__(actual):
        return hash(str(actual.tablero))

    # Comparación de Estados, Esta función calcula f(n)=g(n)+h(n)
    def __lt__(actual, otro):
        return (actual.g + heuristica(actual)) < (otro.g + heuristica(otro))

    def es_deseado(actual):
        # Comprueba si el tablero está en el estado objetivo
        return actual.tablero[3][3] == '*' and sum(fila.count('*') for fila in actual.tablero) == 1

def get_legal_moves(estado):
    direcciones = [(-2, 0), (2, 0), (0, -2), (0, 2)]
    movimientos_permitidos = []
    
    for r in range(7):
        for c in range(7):
            if estado.tablero[r][c] == '*':
                for dr, dc in direcciones:
                    nr, nc = r + dr, c + dc
                    mr, mc = r + dr // 2, c + dc // 2
                    if 0 <= nr < 7 and 0 <= nc < 7 and estado.tablero[nr][nc] == 'o' and estado.tablero[mr][mc] == '*':
                        nuevo_tablero = [fila[:] for fila in estado.tablero]
                        nuevo_tablero[r][c] = 'o'
                        nuevo_tablero[mr][mc] = 'o'
                        nuevo_tablero[nr][nc] = '*'
                        movimientos_permitidos.append(estadoTablero(nuevo_tablero, estado.g + 1, estado))
    return movimientos_permitidos

# Acá se calcula el h(n)
def heuristica(estado):
    # Heurística: Número de piezas restantes - 1
    return sum(fila.count('*') for fila in estado.tablero) - 1

def a_estrella(estado_inicial):
    lista_abierta = []
    lista_cerrada = set()

    heapq.heappush(lista_abierta, (heuristica(estado_inicial), estado_inicial))

    while lista_abierta:
        _, estado_actual = heapq.heappop(lista_abierta)

        if estado_actual.es_deseado():
            return estado_actual

        lista_cerrada.add(estado_actual)

        for movimiento in get_legal_moves(estado_actual):
            if movimiento not in lista_cerrada:
                lista_cerrada.add(movimiento)  # Añadir el movimiento a lista_cerrada para evitar ciclos
                # Inserción en la Cola de Prioridad 
                # Cada vez que se inserta un estado en la cola de prioridad, se calcula 𝑓(𝑛)f(n).
                heapq.heappush(lista_abierta, (movimiento.g + heuristica(movimiento), movimiento))
    
    return None

def recalcular_camino(estado):
    camino = []
    while estado:
        camino.append(estado)
        estado = estado.padre
    return camino[::-1]

def imprimir_tablero(tablero):
    for fila in tablero:
        print(' '.join(c if c else ' ' for c in fila))
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
    casos_prueba = [
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
            [None, None, '*', '*', 'o', None, None],
            [None, None, '*', 'o', '*', None, None],
            ['o', '*', '*', 'o', 'o', 'o', '*'],
            ['*', 'o', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*'],
            [None, None, '*', '*', '*', None, None],
            [None, None, '*', '*', '*', None, None]
        ],
	[ 
            [None, None, 'o', 'o', 'o', None, None],
            [None, None, '*', 'o', 'o', None, None],
            ['o', '*', 'o', 'o', '*', 'o', '*'],
            ['*', 'o', '*', '*', '*', 'o', '*'],
            ['*', '*', 'o', '*', 'o', '*', 'o'],
            [None, None, '*', '*', '*', None, None],
            [None, None, '*', '*', '*', None, None]
        ],
	[ 
            [None, None, 'o', 'o', 'o', None, None],
            [None, None, '*', 'o', 'o', None, None],
            ['o', '*', '*', 'o', '*', 'o', 'o'],
            ['*', 'o', 'o', '*', 'o', 'o', 'o'],
            ['*', 'o', 'o', '*', '*', 'o', 'o'],
            [None, None, 'o', 'o', 'o', None, None],
            [None, None, 'o', 'o', 'o', None, None]
        ],
        # Agrega más configuraciones si es necesario
    ]

    tiempos_ejecucion = []
    movimientos = []
    labels = []

    for idx, tablero_inicial in enumerate(casos_prueba):
        print(f"\n----------------------------------")
        print(f"\nResolviendo caso {idx + 1}...")
        estado_inicial = estadoTablero(tablero_inicial)

        print("Estado inicial del tablero:")
        imprimir_tablero(tablero_inicial)  # Imprimir el tablero inicial

        tiempo_inicial = time.time()
        estado_deseado = a_estrella(estado_inicial)
        tiempo_final = time.time()

        if estado_deseado:
            camino = recalcular_camino(estado_deseado)
            numero_movimientos = len(camino) - 1
            print(f"Numero de movimientos: {numero_movimientos}")
            movimientos.append(numero_movimientos)
            print("Estado final del tablero:")
            imprimir_tablero(estado_deseado.tablero)  # Imprimir el tablero final
        else:
            print("Ninguna solucion encontrada")
            movimientos.append(None)  # No hay solución

        tiempo_ejecucion = tiempo_final - tiempo_inicial
        print(f"Tiempo de ejecucion para el caso de prueba {idx + 1}: {tiempo_ejecucion:.2f} segundos")
        tiempos_ejecucion.append(tiempo_ejecucion)
        labels.append(f"Caso {idx + 1}")

    # Graficar el desempeño
    #plot_performance(tiempos_ejecucion, movimientos, labels)
