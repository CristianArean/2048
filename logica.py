# Constantes:
from random import randint

ANCHO_TABLERO = 4
ALTO_TABLERO = 4
VACIO = 0
VALOR_GANADOR = 2048
ARRIBA = "W"
DERECHA = "D"
ABAJO = "S"
IZQUIERDA = "A"
LISTA_DE_MOVIMEINTOS = (ARRIBA, DERECHA, ABAJO, IZQUIERDA)
LISTA_DE_MOVIMEINTOS_STR = ('ARRIBA', "DERECHA", "ABAJO", "IZQUIERDA")
CANTIDAD_BARRAS_HORIZONTALES = 15


def inicializar_juego():
    tablero = []
    for i in range(ALTO_TABLERO):
        fila = []
        for j in range(ANCHO_TABLERO):
            fila.append(VACIO)
        tablero.append(fila)
    new_tablero = insertar_nuevo_random(tablero)

    return new_tablero


def mostrar_juego(juego):
    indice = 0
    for i in range(ALTO_TABLERO):
        print("\n", "-" * CANTIDAD_BARRAS_HORIZONTALES)
        for j in range(ANCHO_TABLERO):
            print("|", end=" ")
            if juego[i][j] == VACIO:
                print(" ", end=" ")
            else:
                print(juego[i][j], end=" ")
        print("|")
    print("", "-"*CANTIDAD_BARRAS_HORIZONTALES)

    for movs in LISTA_DE_MOVIMEINTOS:
        print(
            f"Apriete {movs} para moverse hacia {LISTA_DE_MOVIMEINTOS_STR[indice]}")
        indice += 1


def primer_juego(juego):
    for i in range(ALTO_TABLERO):
        for j in range(ANCHO_TABLERO):
            if juego[i][j] != 0:
                return False
    return True


def posicion_vacia(juego, i, j):
    if juego[i][j] == VACIO:
        return True
    return False


def copiador(juego):
    new_juego = []
    for i in range(ALTO_TABLERO):
        fila = []
        for j in range(ANCHO_TABLERO):
            fila.append(juego[i][j])

        new_juego.append(fila)
    return new_juego


def insertar_nuevo_random(juego):
    new_juego = copiador(juego)

    random_pos_i = randint(0, 3)
    random_pos_j = randint(0, 3)

    if primer_juego(juego):
        random_pos_i2 = randint(0, 3)
        random_pos_j2 = randint(0, 3)

        while random_pos_i == random_pos_i2 and random_pos_j == random_pos_j2:
            random_pos_i2 = randint(0, 3)
            random_pos_j2 = randint(0, 3)

        new_juego[random_pos_i][random_pos_j] = 2
        new_juego[random_pos_i2][random_pos_j2] = 2
        return new_juego

    while not posicion_vacia(new_juego, random_pos_i, random_pos_j):
        random_pos_i = randint(0, 3)
        random_pos_j = randint(0, 3)

    new_juego[random_pos_i][random_pos_j] = 2
    return new_juego


def juego_ganado(juego):
    for i in range(ALTO_TABLERO):
        for j in range(ANCHO_TABLERO):
            if juego[i][j] == VALOR_GANADOR:
                return True
    return False


def espacios_libres(juego):
    for i in range(ALTO_TABLERO):
        for j in range(ANCHO_TABLERO):
            if juego[i][j] == 0:
                return True
    return False


def movimientos_disponibles(juego):
    # en j
    for i in range(ALTO_TABLERO):
        for j in range(ANCHO_TABLERO - 1):
            if juego[i][j] == juego[i][j + 1]:
                return True
    # en i
    for i in range(ALTO_TABLERO - 1):
        for j in range(ANCHO_TABLERO):
            if juego[i][j] == juego[i + 1][j]:
                return True

    return False


def juego_perdido(juego):
    if not espacios_libres(juego):
        if not movimientos_disponibles(juego):
            return True
    return False


def transponer(juego):
    new_tablero = []
    for i in range(ALTO_TABLERO):
        fila = []
        for j in range(ANCHO_TABLERO):
            fila.append(juego[j][i])
        new_tablero.append(fila)
    return new_tablero


def invertir(juego):
    new_tablero = []
    for i in range(ALTO_TABLERO):
        fila = []
        for j in range(ANCHO_TABLERO - 1, -1, -1):
            fila.append(juego[i][j])
        new_tablero.append(fila)
    return new_tablero


def sumar_a_la_derecha(juego):
    new_juego = copiador(juego)
    for i in range(ALTO_TABLERO):
        for j in range(ANCHO_TABLERO - 1, 0, -1):  # estamos yendo para la derecha
            indice = 1
            while (j - indice) >= 0 and new_juego[i][j - indice] == VACIO:
                indice += 1
            if (j - indice) >= 0 and new_juego[i][j] == new_juego[i][j - indice]:
                new_juego[i][j] += new_juego[i][j - indice]
                new_juego[i][j - indice] = VACIO

        for x in range(ANCHO_TABLERO - 1, -1, -1):  # corro los ceros
            indice = 1
            while (x + indice) < ANCHO_TABLERO and new_juego[i][x + indice] == VACIO:
                indice += 1
            indice -= 1

            if (x + indice) < ANCHO_TABLERO and new_juego[i][x + indice] == VACIO:
                new_juego[i][x + indice] = new_juego[i][x]
                new_juego[i][x] = VACIO
    return new_juego



def moverse_abajo(juego):
    "transpone la matriz, la mueve a la derecha y la vuelve a transponer"
    new_juego = transponer(juego)
    new_juego = sumar_a_la_derecha(new_juego)
    new_juego = transponer(new_juego)
    return new_juego


def moverse_izquierda(juego):
    "invierte la matriz, la mueve la a derecha y la vuelve a invertir"
    new_juego = invertir(juego)
    new_juego = sumar_a_la_derecha(new_juego)
    new_juego = invertir(new_juego)
    return new_juego


def moverse_arriba(juego):
    """
    Transpone la matriz
    La invierte
    la mueve a la derecha
    la vuelve a invertir
    la transpone de vuelta"""
    new_juego = transponer(juego)
    new_juego = invertir(new_juego)
    new_juego = sumar_a_la_derecha(new_juego)
    new_juego = invertir(new_juego)
    new_juego = transponer(new_juego)
    return new_juego


def pedir_direccion(juego):
    direcciones_soportadas = (ARRIBA, IZQUIERDA, ABAJO, DERECHA)
    dir = input(
        """Ingrese la dir a la que se quiere mover("W", "A", "S", "D")""").upper()
    while not dir in direcciones_soportadas:
        dir = input(
            """No es un movimiento. Ingrese la direccion a la que se quiere mover("W", "A", "S", "D")""").upper()
    return dir


def actualizar_juego(juego, dir):
    """
    - Trasponer el tablero si es necesario
    - Por cada fila:
        - Invertir la fila si es necesario
        - Combinar en nueva fila
        - Invertir la fila resultante si es necesario
    - Trasponer el tablero resultante si es necesario
    """
    if dir == DERECHA:
        return sumar_a_la_derecha(juego)

    elif dir == IZQUIERDA:
        return moverse_izquierda(juego)

    elif dir == ABAJO:
        return moverse_abajo(juego)

    elif dir == ARRIBA:
        return moverse_arriba(juego)
