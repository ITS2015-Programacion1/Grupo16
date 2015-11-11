# coding: utf-8
import pilasengine
pilas.fondos.Fondo("data/mapazombi.png")

def iniciar_juego():
    print "Tengo que iniciar el juego"

def salir_del_juego():
    print "Tengo que salir..."

pilas.actores.Menu(
        [
            ('iniciar juego', iniciar_juego),
            ('salir', salir_del_juego),
        ])

pilas.ejecutar()