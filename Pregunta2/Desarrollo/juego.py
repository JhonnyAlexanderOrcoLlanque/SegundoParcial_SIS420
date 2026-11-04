"""Reglas de Puntos y cajas: 3 x 3 puntos y 2 x 2 cajas."""

import random
from copy import deepcopy
from numbers import Integral

VACIO = 0
MODELO = 1
JUGADOR = 2
SIMBOLOS = {VACIO: ' ', MODELO: 'M', JUGADOR: 'J'}
PUNTO = '+'
HORIZONTAL = '-'
VERTICAL = '|'

# Primero seis líneas horizontales, después seis verticales.
EXTREMOS = ((0, 1), (1, 2), (3, 4), (4, 5), (6, 7), (7, 8),
            (0, 3), (1, 4), (2, 5), (3, 6), (4, 7), (5, 8))
CAJAS = ((0, 2, 6, 7), (1, 3, 7, 8),
         (2, 4, 9, 10), (3, 5, 10, 11))


class Juego:
    """Una instancia guarda una partida; no elige las acciones."""

    def __init__(self, jugador_inicial=None):
        # None permite sortear el inicio; un valor explícito permite controlarlo.
        if jugador_inicial is None:
            jugador_inicial = random.choice((MODELO, JUGADOR))
        if (isinstance(jugador_inicial, bool)
                or not isinstance(jugador_inicial, Integral)
                or jugador_inicial not in (MODELO, JUGADOR)):
            raise ValueError('El jugador inicial debe ser MODELO (1) o JUGADOR (2).')
        self._lineas = [False] * 12
        self._cajas = [VACIO] * 4
        self._turno = int(jugador_inicial)

    def obtener_turno(self):
        """Devuelve 1 (M), 2 (J) o None cuando terminó la partida."""
        return self._turno

    def movimientos_validos(self):
        """Los índices de las líneas libres son las acciones disponibles."""
        return [i for i, ocupada in enumerate(self._lineas) if not ocupada]

    def obtener_estado(self):
        """Instantánea inmutable; la entrada final del modelo se definirá después."""
        return (tuple(self._lineas), tuple(self._cajas), self._turno)

    def copiar(self):
        """Copia independiente para ensayar acciones sin alterar la partida."""
        return deepcopy(self)

    def puntajes(self):
        # Derivar los puntos evita guardar contadores que puedan desincronizarse.
        return {MODELO: self._cajas.count(MODELO),
                JUGADOR: self._cajas.count(JUGADOR)}

    def terminado(self):
        return all(self._lineas)

    def ganador(self):
        """None: en curso; 0: empate; 1: gana M; 2: gana J."""
        if not self.terminado():
            return None
        puntos = self.puntajes()
        if puntos[MODELO] == puntos[JUGADOR]:
            return VACIO
        return MODELO if puntos[MODELO] > puntos[JUGADOR] else JUGADOR

    def jugar(self, accion):
        """Aplica una línea al jugador de turno y devuelve lo sucedido."""
        # Todas las validaciones ocurren antes de modificar el estado.
        if self.terminado():
            raise ValueError('La partida ya terminó.')
        if isinstance(accion, bool) or not isinstance(accion, Integral):
            raise ValueError('La acción debe ser un número entero entre 0 y 11.')
        if not 0 <= accion < 12:
            raise ValueError('La acción debe estar entre 0 y 11.')
        if self._lineas[accion]:
            raise ValueError(f'La línea {accion} ya está ocupada.')

        accion = int(accion)
        jugador = self._turno
        self._lineas[accion] = True
        capturadas = []
        for indice, bordes in enumerate(CAJAS):
            if self._cajas[indice] == VACIO and all(self._lineas[b] for b in bordes):
                self._cajas[indice] = jugador
                capturadas.append(indice)

        if self.terminado():
            self._turno = None
        elif not capturadas:
            self._turno = JUGADOR if jugador == MODELO else MODELO
        # Si capturó una o dos cajas, conserva el turno.
        return {'jugador': jugador, 'accion': accion,
                'cajas_capturadas': tuple(capturadas), 'puntajes': self.puntajes(),
                'siguiente_turno': self._turno, 'terminado': self.terminado(),
                'ganador': self.ganador()}

    def representar(self, mostrar_indices=True):
        """Devuelve texto sin imprimirlo. Los números indican líneas libres."""
        # Cada posición vertical ocupa tres caracteres, incluso para 10 y 11.
        def horizontal(i):
            if self._lineas[i]:
                return HORIZONTAL * 7
            return str(i).center(7) if mostrar_indices else ' ' * 7

        def vertical(i):
            if self._lineas[i]:
                return VERTICAL.center(3)
            return str(i).center(3) if mostrar_indices else ' ' * 3

        filas = []
        for fila in range(3):
            filas.append(PUNTO.center(3) + horizontal(2 * fila)
                         + PUNTO.center(3) + horizontal(2 * fila + 1)
                         + PUNTO.center(3))
            if fila < 2:
                base = 6 + fila * 3
                filas.append(vertical(base) + SIMBOLOS[self._cajas[2 * fila]].center(7)
                             + vertical(base + 1)
                             + SIMBOLOS[self._cajas[2 * fila + 1]].center(7)
                             + vertical(base + 2))
        puntos = self.puntajes()
        filas.append(f'M: {puntos[MODELO]} | J: {puntos[JUGADOR]}')
        if self.terminado():
            ganador = self.ganador()
            filas.append('Empate' if ganador == VACIO else f'Ganador: {SIMBOLOS[ganador]}')
        else:
            filas.append(f'Turno: {SIMBOLOS[self._turno]}')
        return '\n'.join(filas)
