# coding: utf-8
#echo # mass_death-juego_de_zombies- >> README.md
#git init
#git add README.md
#git commit -m "first commit"
#git remote add origin https://github.com/marcossavid/mass_death-juego_de_zombies-.git
#git push -u origin master
import pilasengine
import time,random
pilas = pilasengine.iniciar()

TIEMPO = 6
fin_de_juego = False
balas_simples = pilas.actores.Bala()
monos = []
class inicio(pilasengine.escenas.Escena):
    def iniciar(self):
        self.fondo= pilas.fondos.Fondo("data/309471.png")
        pass
pilas.escenas.vincular(inicio)
pilas.escenas.inicio()
                                                
def juego1():
    
    class juegoactivo(pilasengine.escenas.Escena):

        def iniciar(self):
            menu.eliminar()
            pilas.fisica.definir_gravedad(0,0)
            fondo= pilas.fondos.Fondo("data/mapazombi.png") 
            puntos = pilas.actores.Puntaje(x=230, y=200, color=pilas.colores.blanco)
            puntos.magnitud = 1000
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
                    enemigo = pilas.actores.Mono()
                    enemigo.imagen="data/superzombi.png"
                    enemigo. escala=0.3
                    enemigo.radio_de_colision=25
                    enemigo.velocidad=10
                    enemigo.aprender(pilas.habilidades.SeguirAOtro, torreta, 1)
                    enemigo.aprender(pilas.habilidades.PuedeExplotarConHumo)
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


# Añadir la torreta del jugador

            torreta = pilas.actores.Torreta(enemigos=monos,municion_bala_simple="bala", cuando_elimina_enemigo=mono_destruido,frecuencia_de_disparo=1)
            torreta.aprender("MoverseConElTeclado")
            torreta.imagen="data/sobreviviente.png"
            torreta.escala=0.5
            torreta.x=-100
            tcm = pilas.tareas.agregar(1, crear_mono)
            def mover_camara(evento):
                pilas.camara.x = torreta.x
                pilas.camara.y=torreta.y
            pilas.eventos.actualizar.conectar(mover_camara)
    

            def perder(torreta,enemigo):
                global fin_de_juego, tcm, monos
                tcm = pilas.tareas.agregar(1, crear_mono)
                fin_del_juego= True   
                for mono in monos:
                    mono.eliminar()
                tcm.terminar()    
                torreta.eliminar()   
                avisar = pilas.actores.Texto("PERDISTEEE, conseguiste %d puntos" % (puntos.obtener()))
                avisar.escala = [1,2,1,2,1,2,1,2,1]
                
                
            pilas.colisiones.agregar(torreta, monos, perder)
            
      
    
            pass
        def ejecutar(self):
            pass
    pilas.escenas.vincular(juegoactivo)
    pilas.escenas.juegoactivo()
    
#def juego2():    
  #  class pedo(pilasengine.escenas.Escena):

    #    def iniciar(self):
          
      #      pass

       # def ejecutar(self):
         #   pass
   # pilas.escenas.vincular(pedo)
    #pilas.escenas.pedo()
def salir_del_juego():
    pilas.terminar()
menu=pilas.actores.Menu(
        [
            ('jugar', juego1),
            ('salir', salir_del_juego),
            ])

pilas.ejecutar()