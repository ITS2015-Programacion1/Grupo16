# coding: utf-8
import pilasengine
from pilasengine.habilidades import Habilidad

pilas = pilasengine.iniciar()

pilas.fondos.Cesped()

class pepe(pilasengine.actores.Actor):
    def iniciar(self):
        grilla = pilas.imagenes.cargar_grilla ("maton1.png", 5)
        pepe = pilas.actores.Animacion(grilla)
    def actualizar(self):
        if pilas.control.izquierda:
            self.imagen.avanzar()
            self.x -= 1
            self.rotacion=180
            self.espejado=True 
            
pilas.actores.vincular(pepe)
actor=pilas.actores.pepe()          


pilas.ejecutar()