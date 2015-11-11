#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pilasengine
import sys
sys.path.append('.')
import time,random

TIEMPO = 6
fin_de_juego = False
    

pilas=pilasengine.iniciar()

        


rectangulo = pilas.fisica.Rectangulo(-61.0, -34.8, 57,100, dinamica=False)
rectangulo = pilas.fisica.Rectangulo(-296.0, -144.0, 50,107, dinamica=False)
rectangulo = pilas.fisica.Rectangulo(-22.0,-214.0,500,40, dinamica=False)    
rectangulo = pilas.fisica.Rectangulo(-445.0,-212.0,250,30, dinamica=False)    
rectangulo = pilas.fisica.Rectangulo(118.0,-101.0,35,216, dinamica=False) 
rectangulo = pilas.fisica.Rectangulo(0,114.0,210,41, dinamica=False) 
rectangulo = pilas.fisica.Rectangulo(105.8,175.0,40,146, dinamica=False) 
rectangulo = pilas.fisica.Rectangulo(-90.0,228.0,365,20, dinamica=False) 
rectangulo = pilas.fisica.Rectangulo(337.0,230.0,400,20, dinamica=False)
rectangulo = pilas.fisica.Rectangulo(-437.0,4.4,65,63, dinamica=False)
rectangulo = pilas.fisica.Rectangulo(-434.0,123.0,58,58, dinamica=False)
rectangulo = pilas.fisica.Rectangulo(-560.4,40.0,40,375, dinamica=False)
rectangulo = pilas.fisica.Rectangulo(-449.8,226.4,300,25, dinamica=False)
rectangulo = pilas.fisica.Rectangulo(324.0,21.0,92,92, dinamica=False)
rectangulo = pilas.fisica.Rectangulo(361.5,-160.0,39,80, dinamica=False)
rectangulo = pilas.fisica.Rectangulo(404.6,-208.0,350,40, dinamica=False)
rectangulo = pilas.fisica.Rectangulo(556.0,142.0,38,220, dinamica=False)
rectangulo = pilas.fisica.Rectangulo(558.0,-98.0,34,200, dinamica=False)
rectangulo = pilas.fisica.Rectangulo(585.0,-13.4,15,200, dinamica=False)
rectangulo = pilas.fisica.Rectangulo(-594.0,-184.5,37,45, dinamica=False)     
        
# Usar un fondo estándar
bala = pilas.actores.Bala( velocidad_maxima=7 )
fondo= pilas.fondos.Fondo("data/zonadejuego.png")    
#zombi
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


    
#fin del zombi    
    
zombie = []
puntos = pilas.actores.Puntaje(x=230, y=200, color=pilas.colores.negro)
puntos.magnitud = 100000




class SeguirAOtro(pilasengine.habilidades.Habilidad):

    def iniciar(self, receptor, actor_perseguido, velocidad):
        self.receptor = receptor
        self.otro = actor_perseguido
        self.velocidad = velocidad
        x_pos=random.randint(0,1)
        y_pos=random.randint(0,1)
        y_delta = random.randrange(200, 300)
        x_delta = random.randrange(200, 300)
        
        if x_pos == 0:
            self.receptor.x = self.otro.x + x_delta
        if x_pos == 1:
            self.receptor.x = self.otro.x - x_delta

        if y_pos == 0:
            self.receptor.y = self.otro.y + y_delta
        if y_pos == 1:
            self.receptor.y = self.otro.y - y_delta
        
        
        
    def actualizar(self):
        if self.receptor:
            if self.receptor.x > self.otro.x:                
                self.receptor.x -= self.velocidad
            else:
                self.receptor.x += self.velocidad

            if self.receptor.y > self.otro.y:
                self.receptor.y -= self.velocidad
            else:
                self.receptor.y += self.velocidad

                        
            
pilas.habilidades.vincular(SeguirAOtro)
# Funciones
def zombie_destruido(enemigo,disparo):
    global zombie   
    disparo.eliminar()
    enemigo.eliminar()
    puntos.aumentar()
    puntos.escala = 1

    
def crear_zombi():
    if not fin_de_juego:
        # Crear un enemigo nuevo
        enemigo = pilas.actores.Zombie()
        # Hacer que se aparición sea con un efecto bonito
        ##la escala varíe entre 0,25 y 0,75 (Ojo con el radio de colisión)
        enemigo.escala = 2
        enemigo.aprender(pilas.habilidades.SeguirAOtro, protagonista, 1)

        # Dotarle de la habilidad de que explote al ser alcanzado por un disparo
        enemigo.aprender(pilas.habilidades.PuedeExplotar)
        # Situarlo en una posición al azar, no demasiado cerca del jugador
        '''
        w=random.uniform(0,2)

        if(w=>1):
           x = random.randrange(-400,400 ) 
        else:
            pass

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
        '''
        # Dotarlo de un movimiento irregular más impredecible
        tipo_interpolacion = ['lineal',
                            'aceleracion_gradual',
                            'desaceleracion_gradual',
                            'rebote_inicial',
                            'rebote_final']
    
        duracion = 1 +random.random()*4
        
        #pilas.utils.interpolar(enemigo, 'x', 0, duracion)
        #pilas.utils.interpolar(enemigo, 'y', 0, duracion)
        #enemigo.x = pilas.interpolar(0,tiempo,tipo=random.choice(tipo_interpolacion))
        #enemigo.y = pilas.interpolar(0, tiempo,tipo=random.choice(tipo_interpolacion))
        # Añadirlo a la lista de enemigos
        zombie.append(enemigo)
        # Permitir la creación de enemigos mientras el juego esté en activo
    
        return True
    else:
        return False


# Añadir la torreta del jugador

protagonista=pilas.actores.Torreta(enemigos=zombie,municion_bala_simple="misil", cuando_elimina_enemigo=zombie_destruido)
tcm = pilas.tareas.agregar(1, crear_zombi)
#pilas.mundo.agregar_tarea(1, crear_mono) <-- sintaxis vieja

          
    
pilas.actores.Sonido()
pilas.fondos.Espacio()


protagonista.escala=0.8
protagonista.velocidad=0.1
caja=pilas.actores.Caja(41.3,175.6)
caja2=pilas.actores.Caja(509.0,-166.0)
#recargas


# Añadir un marcador
puntos = pilas.actores.Puntaje(x=230, y=200, color=pilas.colores.negro)
puntos.magnitud = 100000
protagonista.velocidad=4


pilas.avisar("sobrevive el maximo de rondas")
superficie = pilas.imagenes.cargar_superficie(100, 100)
pilas.fisica.definir_gravedad(0,0)
pilas.fisica.eliminar_paredes()

def mover_camara(evento):
    pilas.camara.x = protagonista.x
pilas.eventos.actualizar.conectar(mover_camara)

    
#fin del zombi

def recargar(protagonista,caja):
    caja.eliminar()
    texto=pilas.actores.Texto("20 balas")
   
   
pilas.colisiones.agregar(protagonista,caja,recargar)


def perder(protagonista,enemigo):
    global fin_de_juego, tcm, zombie
    fin_del_juego= True    
    #tcm.terminar()
    for zombi in zombie:
        zombie.eliminar()
    tcm.terminar()
    protagonista.eliminar()   
    avisar = pilas.actores.Texto("PERDISTEEE, conseguiste %d puntos" % (puntos.obtener()))
    avisar.escala = [1,0,2,1,0,2,1,0,2,1,0,2,1]
pilas.colisiones.agregar(torreta, monos, perder)        



pilas.ejecutar()