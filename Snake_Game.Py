import random # Para la aparicion aleatoria de las manzanas
import time # Aún no se xD
import pygame # Nuestro principal engine para el juego
import sys

# Inicializar Pygame
pygame.init()

# Configurar la ventana
ventana_tamano = (416, 416)  # Tamaño de la ventana en píxeles
ventana = pygame.display.set_mode(ventana_tamano)
pygame.display.set_caption("Snake Game ED") # Nombre de la pantalla

# Colores
blanco = (255, 255, 255)
negro = pygame.Color(0, 0, 0)
gris_oscuro = pygame.Color(41, 41, 41)
gris_clarito = pygame.Color(111, 111, 111)

# Tamaño de la cuadrícula
filas = 13
columnas = 13
ancho_celda = ventana_tamano[0] // columnas
alto_celda = ventana_tamano[1] // filas


FPS = pygame.time.Clock()
# Definimos las posiciones
posicion_serp = [192, 192] # Notemos que cada cuadro es 32 pixeles pues 416 / 12 = 32
#  entonces si lo queremos ubicar en el cuadro 6 en X y 6 en Y, es multiplicar 6*32 para cada coordenada
posiciones_cuerpo = [[192, 224],
                     [192, 256],
                     [192, 288]
                     ]

vel_serp = 5

fruta_posicion = [288, 96] # 9*32 para X, 3*32 para Y
posicion = [0, 0] #Variable auxiliar para verificar que la fruta obtenga posiciones validas

# fruta_posicion = [random.randrange(1, (ventana[0] // 32))*32,
#                   random.randrange(1, (ventana[1] // 32))*32]

fruta_spawn = True

# Dirección inicial de la serpiente
direccion = "UP"
cambiar_direccion = direccion

#Puntaje Inicial 
puntos = 0

movimientos = -1
aparecer_despues = -2 #El numero de movimientos después en los que aparecerá una nueva manzana

def puntaje_final(option, color, font, size):
    puntaje_font = pygame.font.SysFont(font, size)
    puntaje_surfice =  puntaje_font.render('Puntaje: '+ str(puntos), True, color)
    puntaje_rectan = puntaje_surfice.get_rect()

    ventana.blit(puntaje_surfice, puntaje_rectan) 



def Fin_juego():
   puntaje_font = pygame.font.SysFont('Serif', 20)
   Fin_juego_surfice = puntaje_font.render("Tu puntaje fue de: " + str(puntos), True, negro)
   Fin_juego_rectan = Fin_juego_surfice.get_rect()

   Fin_juego_rectan.midtop = (ventana_tamano[0] // 2, ventana_tamano[1] // 2)  # Corregido aquí

   ventana.blit(Fin_juego_surfice, Fin_juego_rectan)

   pygame.display.flip()
   time.sleep(5)
   pygame.quit()

# Bucle principal : Esto donde se ejecuta el juego
ejecutando = True
while ejecutando:
    # Viendo por todos los eventos
    for event in pygame.event.get():
        # Si hay un evento que es de quitar, se cierra la pantalla
        if event.type == pygame.QUIT:
            ejecutando = False

        # Adicionalmente recibimos eventos de teclado
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direccion != "DOWN":
                cambiar_direccion = "UP"
            if event.key == pygame.K_DOWN and direccion != "UP":
                cambiar_direccion = "DOWN"
            if event.key == pygame.K_LEFT and direccion != "RIGHT":
                cambiar_direccion = "LEFT"
            if event.key == pygame.K_RIGHT and direccion != "LEFT":
                cambiar_direccion = "RIGHT"
    
    # Actualizar la dirección directamente sin necesidad de comparaciones
    direccion = cambiar_direccion

    # Esto es muy importante: se hacen las verificaciones claramente si la serpiente va hacia arriba
    # No puede ir hacia ya que moririria, lo mismo pasa si se dirige a la izquierda y luego a la derecha, etc.


    # Controlar el movimiento de la serpiente
    if direccion == "UP":
        posicion_serp[1] -= 32
    if direccion == "DOWN":
        posicion_serp[1] += 32
    if direccion == "LEFT":
        posicion_serp[0] -= 32
    if direccion == "RIGHT":
        posicion_serp[0] += 32



    # Ahora haremos el mecanismo de puntajes y creciemiento de la serpiente
    posiciones_cuerpo.insert(0, list(posicion_serp))

    if posicion_serp[0] == fruta_posicion[0] and posicion_serp[1] == fruta_posicion[1]:
        puntos += 10
        movimientos = 0
        fruta_spawn = False
    else:
        posiciones_cuerpo.pop()

    if not fruta_spawn: 
        # "Escondemos" la fruta mientras el jugador realiza un numero aleatorio de movimientos hasta que esta vuelva a aparecer
        fruta_posicion = [-32,-32]
        aparecer_despues = random.randrange(1, 11)
        fruta_spawn = True

    if movimientos == aparecer_despues:
        # Cuando ya el jugador realizo x numero de movimiento (dictado por el random) la fruta aparece en su nueva posicion
        while True:
            posicion = [random.randrange(1, (ventana_tamano[0] // 32))*32, random.randrange(1, (ventana_tamano[1] // 32))*32]
            if posicion not in posiciones_cuerpo and posicion not in posicion_serp:#Verificar que la fruta no aparezca sobre la serpiente
                break
        fruta_posicion = posicion 

    # Contruimos los cuerpos en la pantalla
    # fondo de la ventana
    ventana.fill(blanco)

    # Crear el cuerpo y cara de la serpienge
    for pos in range(len(posiciones_cuerpo)):
        # si pos es 0, significa que es la cabeza de la serpiente
        if pos == 0:
            # Lo pintamos de gris ocuro
            pygame.draw.rect(ventana, gris_oscuro, pygame.Rect(posiciones_cuerpo[pos][0], posiciones_cuerpo[pos][1], 32, 32))
            movimientos +=1
            # print(movimientos)
            continue
        # pintamos el cuerpo de gris claro
        pygame.draw.rect(ventana, gris_clarito, pygame.Rect(posiciones_cuerpo[pos][0], posiciones_cuerpo[pos][1], 32, 32))
        
    # Crear el cuerpo de la manzana
    pygame.draw.rect(ventana, negro, pygame.Rect(fruta_posicion[0], fruta_posicion[1], 32, 32))
    

    # Mostrar puntaje
    puntaje_final(1, negro, 'Serif', 20)

    #Condiciones de fin de juego
    if posicion_serp[0] < 0 or posicion_serp[0] > ventana_tamano[0]:
        Fin_juego()

    if posicion_serp[1] < 0 or posicion_serp[1] > ventana_tamano[0]:
        Fin_juego()

    for pos in posiciones_cuerpo[1:]:
        if pos[0] == posiciones_cuerpo[0][0] and pos[1] == posiciones_cuerpo[0][1]:
            Fin_juego()


    # Dibujar la cuadrícula: 13x13
    for fila in range(filas):
        for columna in range(columnas):
            # Usamos .draw.rect para dibujar rectangulo
            # el cual recibe lo parametros: la ventana del juego, el color de las lineas de los rectangulos, una tupla con las cordenada 
            # X e Y del rectangulo y el ancho y alto de cada uno, por ultimo recibe un valor para el grosos de las lineas
            pygame.draw.rect(ventana, negro, (columna * ancho_celda, fila * alto_celda, ancho_celda, alto_celda), 1)

    # Actualizar la pantalla: Estos nos ayudara a ver tambien el ancho
    pygame.display.flip()
    pygame.display.update()
    FPS.tick(vel_serp)

# Salir de Pygame
pygame.quit()
sys.exit()


