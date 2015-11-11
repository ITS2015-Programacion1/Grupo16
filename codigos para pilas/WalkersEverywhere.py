 #! /usr/bin/env python
# -*- coding: utf-8 -*-
import pilasengine
import random

TIEMPO = 6
fin_de_juego = False

pilas = pilasengine.iniciar()
# Usar un fondo estándar
pilas.fondos.Pasto()
# Añadir un marcador
puntos = pilas.actores.Puntaje(x=230, y=200, color=pilas.colores.blanco)
puntos.magnitud = 40
# Añadir el conmutador de Sonido
pilas.actores.Sonido()

# Variables y Constantes
balas_simples = pilas.actores.Bala
monos = []

#Crear el personaje enemigo
        
class Fantasma_1(pilasengine.actores.Actor):    
    def iniciar(self):
        self.imagen = "fantasma1.png"
        self.x =0
        self.y = 0
        self.escala = 0.1
        
pilas.actores.vincular(Fantasma_1)

 #Hacer que el enemigo siga al jugador  
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
def mono_destruido(enemigo,disparo):
    global monos    
    disparo.eliminar()
    enemigo.eliminar()
    #monos.remove(enemigo)
    puntos.aumentar()
    puntos.escala = 1

def crear_mono():
    if not fin_de_juego:
        # Crear un enemigo nuevo
        enemigo = pilas.actores.Fantasma_1()
        # Hacer que se aparición sea con un efecto bonito
        ##la escala varíe entre 0,25 y 0,75 (Ojo con el radio de colisión)
        enemigo.escala = .1
        enemigo.aprender(pilas.habilidades.SeguirAOtro, torreta, 1)
        enemigo.aprender(pilas.habilidades.MirarAlActor, torreta)

        # Dotarle de la habilidad de que explote al ser alcanzado por un disparo
        enemigo.aprender(pilas.habilidades.PuedeExplotarConHumo)

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
        monos.append(enemigo)
        # Permitir la creación de enemigos mientras el juego esté en activo
    
        return True
    else:
        return False


# Crear al jugador

torreta = pilas.actores.Torreta(enemigos=monos,municion_bala_simple="misil", cuando_elimina_enemigo=mono_destruido)
torreta.aprender("MoverseConElTeclado")
torreta.aprender("LimitadoABordesDePantalla")
#torreta.imagen = "vacio.png"
tcm = pilas.tareas.agregar(1, crear_mono)
#pilas.mundo.agregar_tarea(1, crear_mono) <-- sintaxis vieja

def perder(torreta,enemigo):
    global fin_de_juego, tcm, monos
    fin_del_juego= True    
    #tcm.terminar()
    for mono in monos:
        mono.eliminar()
    tcm.terminar()
    torreta.eliminar()
    avisar = pilas.actores.Texto("PERDISTEEE, conseguiste %d puntos" % (puntos.obtener()))
    avisar.escala = [1,0,2,1,0,2,1,0,2,1,0,2,1]

    
pilas.colisiones.agregar(torreta, monos, perder)

# Arrancar el juego

pilas.ejecutar()
