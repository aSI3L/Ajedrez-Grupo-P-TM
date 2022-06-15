import pygame, ajedrez
from random import choice
from traceback import format_exc
from sys import stderr
from time import strftime
from copy import deepcopy
from tkinter import *

pygame.init()

#Se asigna tamaño para que despues se mutiplique por 8 para que se vea la ventana
CASILLERO_TAM = 65
AI_BUSCA_PROFUND = 2

#Se crean variables que serán colores
JAQUE_ROJO   = (240, 150, 150)
GRIS_CLARO   = (212, 202, 190)
GRIS_OSCURO  = (100,  92,  89)

#Se crea una tupla que es un tipo de arreglo donde se colocarán los colores creados anteriormente
TABLERO_COLORES = [(GRIS_CLARO, GRIS_OSCURO)]

#Con la funcion choice devuelve un color aleatoriamente de la tupla creada
TABLERO_COLOR = choice(TABLERO_COLORES)

#Con la funcion pygame.image.load se carga una imagen en la variable creada (en este caso son las piezas de ajedrez)
NEGRO_KING    = pygame.image.load('Imagenes/rey_negro.png')
NEGRO_QUEEN   = pygame.image.load('Imagenes/reina_negra.png')
NEGRO_TORRE   = pygame.image.load('Imagenes/torre_negra.png')
NEGRO_ALFIL   = pygame.image.load('Imagenes/alfil_negro.png')
NEGRO_CABALLO = pygame.image.load('Imagenes/caballo_negro.png')
NEGRO_PEON    = pygame.image.load('Imagenes/peon_negro.png')

BLANCO_KING    = pygame.image.load('Imagenes/rey_blanco.png')
BLANCO_QUEEN   = pygame.image.load('Imagenes/reina_blanca.png')
BLANCO_TORRE   = pygame.image.load('Imagenes/torre_blanca.png')
BLANCO_ALFIL   = pygame.image.load('Imagenes/alfil_blanco.png')
BLANCO_CABALLO = pygame.image.load('Imagenes/caballo_blanco.png')
BLANCO_PEON    = pygame.image.load('Imagenes/peon_blanco.png')

#Se crea un objeto para poder rastrear el tiempo de juego con la funcion pygame.time.Clock()
RELOJ = pygame.time.Clock()
RELOJ_TICK = 15

#Se le dan las dimesiones al tablero (8x8) para que este parejo
#Se crea una variable string que lleva el titulo de la ventana
VENTANA = pygame.display.set_mode((8*CASILLERO_TAM, 8*CASILLERO_TAM))
TITULO_VENTANA = "AJEDREZ - METODOLOGiA 2022"


#Se coloca el icono del juego para la ventana de visualización con image.load
#Se coloca el título de la ventana actual usando pygame.set_caption()
def mostrarVentana():
    pygame.display.set_icon(pygame.image.load('imagenes/icono.ico'))
    pygame.display.set_caption(TITULO_VENTANA)

#Se imprime el tablero vacio
#Se le da color a las casillas claras y oscuras
def print_tablero_vacio():
    VENTANA.fill(TABLERO_COLOR[0])
    pinta_casill_oscuros(TABLERO_COLOR[1])

#Se pintan las casillas
#Seleciona posicion de las columnas y filas para pintarlas de color claro y/o oscuro
def pinta_casill(casill, casill_color):
    col = ajedrez.FILAS.index(casill[0])
    fil = 7-ajedrez.RANGOS.index(casill[1])
    pygame.draw.rect(VENTANA, casill_color, (CASILLERO_TAM*col,CASILLERO_TAM*fil,CASILLERO_TAM,CASILLERO_TAM), 0)

def pinta_casill_oscuros(casill_color):
    for posicion in ajedrez.indiv_gen(ajedrez.CASILL_OSCUROS):
        pinta_casill(ajedrez.bb2str(posicion), casill_color)

#Retorna las coordenadas del primer cuadro negro tomando como referencia el color blanco
def get_casill_rect(casill):
    col = ajedrez.FILAS.index(casill[0])
    fil = 7-ajedrez.RANGOS.index(casill[1])
    return pygame.Rect((col*CASILLERO_TAM, fil*CASILLERO_TAM), (CASILLERO_TAM,CASILLERO_TAM))

#Retorna coordenadas (cuadro blanco y cuadro negro) tomando como referencia el color blanco
def coord2str(posicion, color=ajedrez.BLANCO):
    if color == ajedrez.BLANCO:
        fila_index = int(posicion[0]/CASILLERO_TAM)
        rango_index = 7 - int(posicion[1]/CASILLERO_TAM)
        return ajedrez.FILAS[fila_index] + ajedrez.RANGOS[rango_index]
    if color == ajedrez.NEGRO:
        fila_index = 7 - int(posicion[0]/CASILLERO_TAM)
        rango_index = int(posicion[1]/CASILLERO_TAM)
        return ajedrez.FILAS[fila_index] + ajedrez.RANGOS[rango_index]

#Retorna la obtencion del tipo y color de la pieza tomando como referencia las coordenadas de cada cuadrado y la ubicacion
#de cada rey (blanco y negro) e imprime el resultado mostrando la pieza ubicada donde corresponde (ambos lados negros y blanco)
#Se asignan las piezas con su tipo y color a una posicion del tablero
def print_tablero(tablero, color=ajedrez.BLANCO):
    if color == ajedrez.BLANCO:
        printed_tablero = tablero
    if color == ajedrez.NEGRO:
        printed_tablero = ajedrez.rota_tablero(tablero)

    print_tablero_vacio() #Funcion para imprimir el tablero vacio

    if ajedrez.jaque(tablero, ajedrez.BLANCO):
        pinta_casill(ajedrez.bb2str(ajedrez.get_king(printed_tablero, ajedrez.BLANCO)), JAQUE_ROJO)
    if ajedrez.jaque(tablero, ajedrez.NEGRO):
        pinta_casill(ajedrez.bb2str(ajedrez.get_king(printed_tablero, ajedrez.NEGRO)), JAQUE_ROJO)

    for posicion in ajedrez.pieza_color_gen(printed_tablero, ajedrez.KING,    ajedrez.NEGRO):
        VENTANA.blit(pygame.transform.scale(NEGRO_KING,    (CASILLERO_TAM,CASILLERO_TAM)), get_casill_rect(ajedrez.bb2str(posicion)))
    for posicion in ajedrez.pieza_color_gen(printed_tablero, ajedrez.QUEEN,   ajedrez.NEGRO):
        VENTANA.blit(pygame.transform.scale(NEGRO_QUEEN,   (CASILLERO_TAM,CASILLERO_TAM)), get_casill_rect(ajedrez.bb2str(posicion)))
    for posicion in ajedrez.pieza_color_gen(printed_tablero, ajedrez.TORRE,   ajedrez.NEGRO):
        VENTANA.blit(pygame.transform.scale(NEGRO_TORRE,   (CASILLERO_TAM,CASILLERO_TAM)), get_casill_rect(ajedrez.bb2str(posicion)))
    for posicion in ajedrez.pieza_color_gen(printed_tablero, ajedrez.ALFIL,   ajedrez.NEGRO):
        VENTANA.blit(pygame.transform.scale(NEGRO_ALFIL,   (CASILLERO_TAM,CASILLERO_TAM)), get_casill_rect(ajedrez.bb2str(posicion)))
    for posicion in ajedrez.pieza_color_gen(printed_tablero, ajedrez.CABALLO, ajedrez.NEGRO):
        VENTANA.blit(pygame.transform.scale(NEGRO_CABALLO, (CASILLERO_TAM,CASILLERO_TAM)), get_casill_rect(ajedrez.bb2str(posicion)))
    for posicion in ajedrez.pieza_color_gen(printed_tablero, ajedrez.PEON,    ajedrez.NEGRO):
        VENTANA.blit(pygame.transform.scale(NEGRO_PEON,    (CASILLERO_TAM,CASILLERO_TAM)), get_casill_rect(ajedrez.bb2str(posicion)))

    for posicion in ajedrez.pieza_color_gen(printed_tablero, ajedrez.KING,    ajedrez.BLANCO):
        VENTANA.blit(pygame.transform.scale(BLANCO_KING,    (CASILLERO_TAM,CASILLERO_TAM)), get_casill_rect(ajedrez.bb2str(posicion)))
    for posicion in ajedrez.pieza_color_gen(printed_tablero, ajedrez.QUEEN,   ajedrez.BLANCO):
        VENTANA.blit(pygame.transform.scale(BLANCO_QUEEN,   (CASILLERO_TAM,CASILLERO_TAM)), get_casill_rect(ajedrez.bb2str(posicion)))
    for posicion in ajedrez.pieza_color_gen(printed_tablero, ajedrez.TORRE,   ajedrez.BLANCO):
        VENTANA.blit(pygame.transform.scale(BLANCO_TORRE,   (CASILLERO_TAM,CASILLERO_TAM)), get_casill_rect(ajedrez.bb2str(posicion)))
    for posicion in ajedrez.pieza_color_gen(printed_tablero, ajedrez.ALFIL,   ajedrez.BLANCO):
        VENTANA.blit(pygame.transform.scale(BLANCO_ALFIL,   (CASILLERO_TAM,CASILLERO_TAM)), get_casill_rect(ajedrez.bb2str(posicion)))
    for posicion in ajedrez.pieza_color_gen(printed_tablero, ajedrez.CABALLO, ajedrez.BLANCO):
        VENTANA.blit(pygame.transform.scale(BLANCO_CABALLO, (CASILLERO_TAM,CASILLERO_TAM)), get_casill_rect(ajedrez.bb2str(posicion)))
    for posicion in ajedrez.pieza_color_gen(printed_tablero, ajedrez.PEON,    ajedrez.BLANCO):
        VENTANA.blit(pygame.transform.scale(BLANCO_PEON,    (CASILLERO_TAM,CASILLERO_TAM)), get_casill_rect(ajedrez.bb2str(posicion)))

    pygame.display.flip() #Actualiza la pantalla completa

#Funcion para establecer el titulo: Obtiene el título de la ventana actual
#Actualiza la pantalla completa: Surface a la pantalla
def set_titulo(titulo):
    pygame.display.set_caption(titulo) #Setea un titulo a la ventana
    pygame.display.flip() #Actualiza el contenido de la ventana

def hacer_AI_movim(juega, color):
    set_titulo(TITULO_VENTANA + ' - Analizando movimiento...') #Al jugar la IA, añade el string a la cabecera de la ventana
    new_juega = ajedrez.mueve(juega, ajedrez.get_AI_movim(juega, AI_BUSCA_PROFUND))
    set_titulo(TITULO_VENTANA)
    print_tablero(new_juega.tablero, color)
    return new_juega

#Identifica si el movimiento de la figura es válido y lo realiza
def intenta_movim(juega, movim_intentado):
    for movim in ajedrez.movimientos_legales(juega, juega.mueve_prim):
        if movim == movim_intentado:
            juega = ajedrez.mueve(juega, movim)
    return juega

#Funcion para arrancar el juego 
def juega_con(juega, color):
    run = True
    ongoing = True

    try:
        while run:
            RELOJ.tick(RELOJ_TICK) #Inicia el conteo del reloj
            print_tablero(juega.tablero, color)

            #Imprime salida de pantalla al finalizar juego y detiene su ejecucion
            if ajedrez.finaliza_juego(juega):
                set_titulo(TITULO_VENTANA + ' - ' + ajedrez.get_salida(juega))
                ongoing = False

            if ongoing and juega.mueve_prim == ajedrez.opuesto_color(color):
                juega = hacer_AI_movim(juega, color)
            
            if ajedrez.finaliza_juego(juega):
                set_titulo(TITULO_VENTANA + ' - ' + ajedrez.get_salida(juega))
                ongoing = False

            for event in pygame.event.get(): #Salir del juego
                if event.type == pygame.QUIT:
                    run = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    abandona_casillero = coord2str(event.pos, color)
                    
                if event.type == pygame.MOUSEBUTTONUP:
                    llegada_casillero = coord2str(event.pos, color)
                    
                    if ongoing and juega.mueve_prim == color:
                        movim = (ajedrez.str2bb(abandona_casillero), ajedrez.str2bb(llegada_casillero))
                        juega = intenta_movim(juega, movim)
                        print_tablero(juega.tablero, color)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == 113:
                        run = False
                    if event.key == 104 and ongoing: 		#Tecla H - IA realiza movimiento
                        juega = hacer_AI_movim(juega, color)
                    if event.key == 100: 					#Tecla D - Deshacer jugada
                        juega = ajedrez.deshace_movim(juega)
                        juega = ajedrez.deshace_movim(juega)
                        set_titulo(TITULO_VENTANA)
                        print_tablero(juega.tablero, color)
                        ongoing = True
                    if event.key == 112: #Tecla P - Historial de Posiciones
                        print(juega.get_mov_list() + '\n')
                        print('\n'.join(juega.posicion_historial))
                    if event.key == 101: 	#Tecla E - Evalua puntaje del juego
                        print('Puntaje actual = ' + str(ajedrez.evalua_juego(juega)/100))

    except:
        print(format_exc(), file=stderr)
        bug_file.write('ERROR!')
        bug_file.write('----- ' + strftime('%x %X') + ' -----\n')
        bug_file.write(format_exc())
        bug_file.write('\nJugando con BLANCO:\n\t' if color == ajedrez.BLANCO else '\nJugando con NEGRO:\n\t')
        bug_file.close()

def juega_con_blancas(juega=ajedrez.Juega()):
    return juega_con(juega, ajedrez.BLANCO)

def juega_con_negras(juega=ajedrez.Juega()):
    return juega_con(juega, ajedrez.NEGRO)

def juega_con_aleatorio(juega=ajedrez.Juega()):
    color = choice([ajedrez.BLANCO, ajedrez.NEGRO])
    juega_con(juega, color)

juega_con_aleatorio()
# Menu
raiz = Tk()
raiz.title("Ajedrez")
raiz.iconbitmap("imagenes/icono.ico")
raiz.config(bg="black")

miFrame = Frame()

# Agrego el frame a la ventana
miFrame.pack()

# Color de fondo
miFrame.config(bg="black")

# Tamaño del frame
miFrame.config(width="650", height="350")

# Borde
miFrame.config(bd=30)
miFrame.config(relief="groove")


# Label
frame2 = Frame(miFrame)
frame2.config(width="220")
frame2.grid(row=1, column=0)
frame3 = Frame(miFrame)
frame3.config(width="220")
frame3.grid(row=1, column=1)
frame4 = Frame(miFrame)
frame4.config(width="220")
frame4.grid(row=1, column=2)
Label(miFrame, text="Bienvenido a ajedrez", fg="white",
      font=(18), bg="black").grid(row=1, column=1)

# Acciones de Botones


def btn_blancas():
    raiz.destroy()
    mostrarVentana()
    juega_con_blancas()


def btn_negras():
    raiz.destroy()
    mostrarVentana()
    juega_con_negras()


def btn_aleatorio():
    raiz.destroy()
    mostrarVentana()
    juega_con_aleatorio()

# Boton
Button(miFrame, text="jugar con blancas",
       command=btn_blancas).grid(row=3, column=1)
negras = Button(miFrame, text="jugar con negras", command=btn_aleatorio)
negras.grid(row=4, column=1)
aleatorio = Button(miFrame, text="jugar con aleatorio", command=btn_aleatorio)
aleatorio.grid(row=5, column=1)

raiz.mainloop()