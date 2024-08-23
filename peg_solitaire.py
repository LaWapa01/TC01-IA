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

# Genera los movimientos válidos desde un estado dado del tablero.
def obtener_movimientos_correctos(estado):
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
# Calcula la heurística del estado, que es el número de piezas restantes menos una.
# Cuanto menor sea el valor, más cerca está de la solución.
def heuristica(estado):
    # Heurística: Número de piezas restantes - 1
    return sum(fila.count('*') for fila in estado.tablero) - 1

# Funcion para crear el A* donde se tienen las lista abierta y cerrada
def a_estrella(estado_inicial):
    lista_abierta = []
    lista_cerrada = set()

    # agrega cada nuevo movimiento a la lista abierta
    heapq.heappush(lista_abierta, (heuristica(estado_inicial), estado_inicial))

    # Si encuentra el estado objetivo, lo devuelve; de lo contrario, continúa explorando hasta agotar todas las posibilidades.

    while lista_abierta:
        _, estado_actual = heapq.heappop(lista_abierta)

        #print("---- ---- ----")
        #imprimir_tablero(estado_actual.tablero)

        # Verificar si el estado actual es el que se tiene como objetivo
        if estado_actual.es_deseado():
            return estado_actual

        lista_cerrada.add(estado_actual)

        for movimiento in obtener_movimientos_correctos(estado_actual):
            if movimiento not in lista_cerrada:
                lista_cerrada.add(movimiento)  # Añadir el movimiento a lista_cerrada para evitar ciclos
                # Inserción en la Cola de Prioridad 
                # Cada vez que se inserta un estado en la cola de prioridad, se calcula 𝑓(𝑛)f(n).
                heapq.heappush(lista_abierta, (movimiento.g + heuristica(movimiento), movimiento))
    
    return None

# Reconstruye el camino desde el estado inicial hasta el estado objetivo recorriendo los nodos padres
def recalcular_camino(estado):
    camino = []
    while estado:
        camino.append(estado)
        estado = estado.padre
    # Devuelve una lista con los estados en el orden en que se deben recorrer para llegar al estado objetivo
    return camino[::-1]

# Imprime el tablero en la consola
def imprimir_tablero(tablero):
    for fila in tablero:
        print(' '.join(c if c else ' ' for c in fila))
    print()

if __name__ == "__main__":

    # Definir diferentes configuraciones iniciales para pruebas
    casos_prueba = [
        [ # Caso prueba 01
            [None, None, '*', '*', '*', None, None],
            [None, None, '*', '*', '*', None, None],
            ['*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', 'o', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*'],
            [None, None, '*', '*', '*', None, None],
            [None, None, '*', '*', '*', None, None]
        ],
        [  # Caso prueba 02
            [None, None, '*', '*', 'o', None, None],
            [None, None, '*', 'o', '*', None, None],
            ['o', '*', '*', 'o', 'o', 'o', '*'],
            ['*', 'o', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*'],
            [None, None, '*', '*', '*', None, None],
            [None, None, '*', '*', '*', None, None]
        ],
        [  # Caso prueba 03
            [None, None, '*', '*', '*', None, None],
            [None, None, '*', 'o', '*', None, None],
            ['*', '*', 'o', '*', '*', '*', '*'],
            ['*', 'o', '*', '*', '*', '*', '*'],
            ['*', '*', 'o', 'o', '*', '*', '*'],
            [None, None, '*', '*', '*', None, None],
            [None, None, '*', '*', '*', None, None]
        ],
        [ # Caso prueba 04
            [None, None, '*', '*', '*', None, None],
            [None, None, '*', 'o', '*', None, None],
            ['*', '*', 'o', '*', 'o', '*', '*'],
            ['*', '*', 'o', '*', '*', 'o', '*'],
            ['*', '*', '*', '*', '*', '*', '*'],
            [None, None, '*', '*', '*', None, None],
            [None, None, '*', '*', '*', None, None]
        ],
        # Agrega más pruebas si es necesario
    ]
    
    # Variables almacenar tiempos y movimientos relebantes para el análisis
    tiempos_ejecucion = []
    movimientos = []
    nombre = []

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
        nombre.append(f"Caso {idx + 1}")

    # Graficar el desempeño
    #plot_performance(tiempos_ejecucion, movimientos, nombre)
