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
zombies = []

#Crear el personaje enemigo
        
class zombie(pilasengine.actores.Actor):    
    def iniciar(self):
        self.imagen = "superzombi.png"
        self.x =0
        self.y = 0
        self.escala = 0.1
        self.radio_de_colision=16
pilas.actores.vincular(zombie)

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
def zombie_destruido(enemigo,disparo):
    global zombies    
    disparo.eliminar()
    enemigo.eliminar()
    #zombies.remove(enemigo)
    puntos.aumentar()
    puntos.escala = 1

def crear_zombie():
    if not fin_de_juego:
        # Crear un enemigo nuevo
        enemigo = pilas.actores.zombie()
        # Hacer que se aparición sea con un efecto bonito
        ##la escala varíe entre 0,25 y 0,75 (Ojo con el radio de colisión)
        enemigo.escala = 0.3
        enemigo.aprender(pilas.habilidades.SeguirAOtro, sobreviviente, 1)
        enemigo.aprender(pilas.habilidades.MirarAlActor, sobreviviente)

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
        zombies.append(enemigo)
        # Permitir la creación de enemigos mientras el juego esté en activo
    
        return True
    else:
        return False


# Crear al jugador

class sobreviviente(pilasengine.actores.Actor):    
    def iniciar(self):
        self.imagen = "sobreviviente.png"
        self.x =0
        self.y = 0
        self.escala = 0.1
        self.radio_de_colision=10
        
pilas.actores.vincular(sobreviviente)

sobreviviente = pilas.actores.sobreviviente()
sobreviviente.escala = 0.6
sobreviviente.aprender("MoverseConElTeclado")
sobreviviente.aprender("RotarConMouse")
sobreviviente.aprender("DispararConClick",grupo_enemigos=zombies,cuando_elimina_enemigo=zombie_destruido, angulo_salida_disparo= 90, frecuencia_de_disparo= 2, municion= "Misil")

tcz = pilas.tareas.agregar(0.5, crear_zombie)
#pilas.mundo.agregar_tarea(1, crear_mono) <-- sintaxis vieja

def perder(sobreviviente,enemigo):
    global fin_de_juego, tcz, zombies
    fin_del_juego= True    
    #tcz.terminar()
    for zombie in zombies:
        zombie.eliminar()
    tcz.terminar()
    sobreviviente.eliminar()
    avisar = pilas.actores.Texto("PERDISTEEE, conseguiste %d puntos" % (puntos.obtener()))
    avisar.escala = [1,0,2,1,0,2,1,0,2,1,0,2,1]

    
pilas.colisiones.agregar(sobreviviente, zombies, perder)

# Arrancar el juego

pilas.ejecutar()
