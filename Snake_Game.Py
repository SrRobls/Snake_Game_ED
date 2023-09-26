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

# fruta_posicion = [random.randrange(1, (ventana[0] // 32))*32,
#                   random.randrange(1, (ventana[1] // 32))*32]

fruta_spawn = True

# Dirección inicial de la serpiente
direccion = "UP"
cambiar_direccion = direccion

#Puntaje Inicial 
puntos = 0


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
            if event.key == pygame.K_UP:
                cambiar_direccion = "UP"
            if event.key == pygame.K_DOWN:
                cambiar_direccion = "DOWN"
            if event.key == pygame.K_LEFT:
                cambiar_direccion = "LEFT"
            if event.key == pygame.K_RIGHT:
                cambiar_direccion = "RIGHT"
    
    # Actualizar la dirección directamente sin necesidad de comparaciones
    direccion = cambiar_direccion

    # Esto es muy importante: se hacen las verificaciones claramente si la serpiente va hacia arriba
    # No puede ir hacia ya que moririria, lo mismo pasa si se dirige a la izquierda y luego a la derecha, etc.

    # PROBLEMON: esto no esta funcionando jajaja. no se cumplen la ideas de arriba. compruebenlo por uds mismos
    if cambiar_direccion == "UP" and direccion == "DOWN":
        direccion = "DOWN"
    elif cambiar_direccion == "DOWN" and direccion == "UP":
        direccion = "UP"
    elif cambiar_direccion == "LEFT" and direccion == "RIGHT":
        direccion = "RIGHT"
    elif cambiar_direccion == "RIGHT" and direccion == "LEFT":
        direccion = "LEFT"
    



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
        fruta_spawn = False
    else:
        posiciones_cuerpo.pop()

    if not fruta_spawn:
        fruta_posicion = [random.randrange(1, (ventana_tamano[0] // 32))*32,
                        random.randrange(1, (ventana_tamano[1] // 32))*32]

    fruta_spawn = True

    # Contruimos los cuerpos en la pantalla
    # Limpiar la pantalla
    ventana.fill(blanco)

    # Crear el cuerpo y cara de la serpienge
    for pos in range(len(posiciones_cuerpo)):
        # si pos es 0, significa que es la cabeza de la serpiente
        if pos == 0:
            # Lo pintamos de gris ocuro
            pygame.draw.rect(ventana, gris_oscuro, pygame.Rect(posiciones_cuerpo[pos][0], posiciones_cuerpo[pos][1], 32, 32))
            continue
        # pintamos el cuerpo de gris claro
        pygame.draw.rect(ventana, gris_clarito, pygame.Rect(posiciones_cuerpo[pos][0], posiciones_cuerpo[pos][1], 32, 32))

    # Crear el cuerpo de la manzana
    pygame.draw.rect(ventana, negro, pygame.Rect(fruta_posicion[0], fruta_posicion[1], 32, 32))


    # Mostrar puntaje
    #
    #
    #
    #


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

