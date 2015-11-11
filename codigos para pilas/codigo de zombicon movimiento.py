# coding: utf-8
import pilasengine

pilas = pilasengine.iniciar()


class Zombie(pilasengine.actores.Actor):

    def iniciar(self):
        self.imagen = "data/zombie/2.png"
        self.escala = 1
        self.x = -250

    def actualizar(self):
        if pilas.control.izquierda:
             self.x -= 5
             self.imagen = "data/zombie/5.png"


        elif pilas.control.derecha:
             self.x += 5
             self.imagen = "data/zombie/8.png"

        elif pilas.control.arriba:
             self.y += 5
             self.imagen = "data/zombie/11.png"

        elif pilas.control.abajo:
            self.y -= 5
            self.imagen = "zombie/2.png"
pilas.actores.vincular(Zombie) 
torreta=pilas.actores.Zombie()
def mover_camara(evento):
    pilas.camara.x = torreta.x
    pilas.camara.y=torreta.y
pilas.eventos.actualizar.conectar(mover_camara)
 
pilas.ejecutar()