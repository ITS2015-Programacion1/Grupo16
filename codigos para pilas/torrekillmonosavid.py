#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pilasengine
import random, time

TIEMPO = 6
fin_de_juego = False

pilas = pilasengine.iniciar()
  
            
# Usar un fondo estándar
fondo= pilas.fondos.Fondo("data/zonadejuego.png")
# Añadir un marcador
puntos = pilas.actores.Puntaje(x=230, y=200, color=pilas.colores.blanco)
puntos.magnitud = 40
# Añadir el conmutador de Sonido
pilas.actores.Sonido()

# Variables y Constantes
balas_simples = pilas.actores.Bala
monos = []

# Funciones
def mono_destruido(enemigo,disparo):
    disparo.eliminar()
    enemigo.eliminar()
    puntos.aumentar()
    puntos.escala=[0,1,3,1]



def crear_mono():
    # Crear un enemigo nuevo
    enemigo = pilas.actores.Mono()
    enemigo.imagen="mutante.png"
    enemigo.radio_de_colision=20
    # Hacer que se aparición sea con un efecto bonito
    ##la escala varíe entre 0,25 y 0,75 (Ojo con el radio de colisión)
    enemigo.escala = .5
    # Dotarle de la habilidad de que explote al ser alcanzado por un disparo
    enemigo.aprender(pilas.habilidades.PuedeExplotar)
    # Situarlo en una posición al azar, no demasiado cerca del jugador
    x = random.randrange(-320, 320)
    y = random.randrange(-240, 240)
    if x >= 0 and x <= 100:
        x = 180
    elif x <= 0 and x >= -100:
        x = -180
    if y >= 0 and y <= 100:
        y = 180
    elif y <= 0 and y >= -100:
        y = -180
    enemigo.x = x
    enemigo.y = y
    # Dotarlo de un movimiento irregular más impredecible
    tipo_interpolacion = ['lineal',
                            'aceleracion_gradual',
                            'desaceleracion_gradual',
                            'rebote_inicial',
                            'rebote_final']
    
    duracion = 1 +random.random()*4
    
    pilas.utils.interpolar(enemigo, 'x', 0, duracion)
    pilas.utils.interpolar(enemigo, 'y', 0, duracion)
    #enemigo.x = pilas.interpolar(0,tiempo,tipo=random.choice(tipo_interpolacion))
    #enemigo.y = pilas.interpolar(0, tiempo,tipo=random.choice(tipo_interpolacion))
    # Añadirlo a la lista de enemigos
    monos.append(enemigo)
    # Permitir la creación de enemigos mientras el juego esté en activo
    if fin_de_juego:
        return False
    else:
        return True


# Añadir la torreta del jugador

torreta = pilas.actores.Torreta(enemigos=monos, cuando_elimina_enemigo=mono_destruido)

pdf=pilas.tareas.agregar(1, crear_mono)
#pilas.mundo.agregar_tarea(1, crear_mono) <-- sintaxis vieja
def terminar_juego(torreta,enemigos):
    global fin_del_juego
    pdf.terminar()
    torreta.eliminar()
    texto=pilas.actores.Texto("fin del juego")
    texto.escala=3
    enemigos.eliminar()
   
pilas.colisiones.agregar(torreta,monos,terminar_juego) 



# Arrancar el juego
pilas.ejecutar()
