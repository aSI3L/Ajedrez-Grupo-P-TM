#Inicialización


#Juego


#==========FUNCIONES==========

#Se asigna un índice a los bits disponibles para el tablero
def get_pieza(tablero, bitboard):
    return tablero[bb2index(bitboard)]

#Espacios disponibles en el tablero para realizar la jugada
def bb2index(bitboard):
    for i in range(64):
        if bitboard & (0b1 << i):
            return i

#Distribucion de filas y rangos en el tablero con matriz de 8x8
def str2index(posicion_str):
    fille = FILAS.index(posicion_str[0].lower())
    rango = RANGOS.index(posicion_str[1])
    return 8 * rango + fille

#Se realiza la division de los espacios (64) y se distribuyen equitativamente entre filas y rangos
def bb2str(bitboard):
    for i in range(64):
        if bitboard & (0b1 << i):
            fille = i%8
            rango = int(i/8)
            return '{}{}'.format(FILAS[fille], RANGOS[rango])

#Se encadenan letras y rangos uno por uno dentro de los bits correspondientes al tablero
def str2bb(posicion_str):
    return 0b1 << str2index(posicion_str)

def movim2str(movim):
    return bb2str(movim[0]) + bb2str(movim[1])

#Se dsitribuyen rangos y letras dentro del tablero respetando el rango de 64 (Espacios=Matriz de 8X8)
def indiv_gen(bitboard):
    for i in range(64):
        bit = 0b1 << i
        if bitboard & bit:
            yield bit

#Se distribuyen las piezas en el tablero (utilizando su codigo o id)  dentro del rango del tablero (64)
def pieza_gen(tablero, pieza_codig):
    for i in range(64):
        if tablero[i]&PIEZA_MASK == pieza_codig:
            yield 0b1 << i

#Se ordenan las piezas por su codigo y color dentro del rango del tablero (64)
def pieza_color_gen(tablero, pieza_codig, color):
    for i in range(64):
        if tablero[i] == pieza_codig|color:
            yield 0b1 << i

#Devuelve color opuesto al ordenado
def opuesto_color(color):
    if color == BLANCO:
        return NEGRO
    if color == NEGRO:
        return BLANCO

#Retorna el codigo de cada pieza
def pieza_str(pieza):
    return PIEZA_CODIG[pieza]

#Retorna cada pieza a través de su codigo en cada posicion del arreglo
def str2pieza(string):
    return PIEZA_CODIG[string]

#Imprime el orden del tablero de un lado y distribucion de los cuadrados de cada pieza (8 Letras)
def print_tablero(tablero):
    print('')
    for i in range(len(RANGOS)):
        rango_str = str(8-i) + ' '
        primer = len(tablero) - 8*(i+1)
        for fille in range(len(FILAS)):
            rango_str += '{} '.format(pieza_str(tablero[primer+fille]))
        print(rango_str)
    print('  a b c d e f g h')

#Imprime el orden del tablero del lado opuesto y distribucion de los cuadrados de cada pieza (8 Letras) utilizando la tecnica espejo
def print_rotar_tablero(tablero):
    r_tablero = rota_tablero(tablero)
    print('')
    for i in range(len(RANGOS)):
        rango_str = str(i+1) + ' '
        primer = len(r_tablero) - 8*(i+1)
        for fille in range(len(FILAS)):
            rango_str += '{} '.format(pieza_str(r_tablero[primer+fille]))
        print(rango_str)
    print('  h g f e d c b a')

#Devuelve la distribucion del tablero comprobando si son numeros o caracteres para ordenarlos segun corresponda
def print_bitboard(bitboard):
    print('')
    for rango in range(len(RANGOS)):
        rango_str = str(8-rango) + ' '
        for fille in range(len(FILAS)):
            if (bitboard >> (fille + (7-rango)*8)) & 0b1:
                rango_str += '# '
            else:
                rango_str += '. '
        print(rango_str)
    print('  a b c d e f g h')

#Retorna los bits correspondiente dentro del rango de tablero (64)
def lsb(bitboard):
    for i in range(64):
        bit = (0b1 << i) 
        if bit & bitboard:
            return bit

#Retorna los bits correspondientes. A medida que se recorre el arreglo de bits se lo va restando al total del tablero
def msb(bitboard):
    for i in range(64):
        bit = (0b1 << (63-i)) 
        if bit & bitboard:
            return bit

#Obtiene el color de cada pieza del tablero avanzando a través de un arreglo
def get_piezas_color(tablero, color):
    return list2int([ (i != VACIO and i&COLOR_MASK == color) for i in tablero ])

#Obtiene color de los cuadros vacios avanzando atraves de un arreglo
def vacio_casilleros(tablero):
    return list2int([ i == VACIO for i in tablero ])

#Permite identificar los cuadrados ocupados en el tablero devolviendo los que no cumplen la condicion de vacios
def ocupado_casilleros(tablero):
    return nnot(vacio_casilleros(tablero))

#Invierte la lista de las piezas
def list2int(lst):
    rev_list = lst[:]
    rev_list.reverse()
    return int('0b' + ''.join(['1' if i else '0' for i in rev_list]), 2)

def nnot(bitboard):
    return ~bitboard & CASILLEROS

#Recibe el tablero y lo rota
def rota_tablero(tablero):
    rotar_tablero = deepcopy(tablero)
    rotar_tablero.reverse()
    return rotar_tablero
#Copia el tablero invertido dentro del rango del tablero (64)
def inv_tablero_v(tablero):
    inv =  [56,  57,  58,  59,  60,  61,  62,  63,
            48,  49,  50,  51,  52,  53,  54,  55,
            40,  41,  42,  43,  44,  45,  46,  47,
            32,  33,  34,  35,  36,  37,  38,  39,
            24,  25,  26,  27,  28,  29,  30,  31,
            16,  17,  18,  19,  20,  21,  22,  23,
             8,   9,  10,  11,  12,  13,  14,  15,
             0,   1,   2,   3,   4,   5,   6,   7]
    return deepcopy([tablero[inv[i]] for i in range(64)])

#Retorna  opuesto de Fila A 
def lado_este(bitboard):
    return (bitboard << 1) & nnot(FILA_A)

#Retorna opuesto Fila H del lado contrario del tablero
def lado_oeste(bitboard):
    return (bitboard >> 1) & nnot(FILA_H)

#Retorna los rangos para el usuario desde 8 a 1
def lado_norte(bitboard):
    return (bitboard << 8) & nnot(RANGO_1)

#Retorna los rangos del lado opuesto desde 1 a 8
def lado_sur(bitboard):
    return (bitboard >> 8) & nnot(RANGO_8)

#Retorna primer bit NorEste
def lado_NE(bitboard):
    return lado_norte(lado_este(bitboard))

#Retorna primer bit NorOeste
def lado_NO(bitboard):
    return lado_norte(lado_oeste(bitboard))

#Retorna primer bit SurEste
def lado_SE(bitboard):
    return lado_sur(lado_este(bitboard))

#Retrona primer bit SurOeste
def lado_SO(bitboard):
    return lado_sur(lado_oeste(bitboard))

#Retorna espacio libre luego de un movimiento
def mueve_pieza(tablero, movim):
    new_tablero = deepcopy(tablero)
    new_tablero[bb2index(movim[1])] = new_tablero[bb2index(movim[0])] 
    new_tablero[bb2index(movim[0])] = VACIO
    return new_tablero

#Nueva posicion adquirida en el tablero
def mueve(juega, movim):
    new_juega = deepcopy(juega)
    abandona_posicion = movim[0]
    nueva_posicion = movim[1]

    #Actualiza reloj
    new_juega.halfmove_clock += 1
    if new_juega.mueve_prim == NEGRO:
        new_juega.fullmove_number += 1

    #Resetea el reloj con captura
    if get_pieza(new_juega.tablero, nueva_posicion) != VACIO:
        new_juega.halfmove_clock = 0

    #Peones: resetea reloj, remueve ep capturado, establece nuevo ep
    if get_pieza(new_juega.tablero, abandona_posicion)&PIEZA_MASK == PEON:
        new_juega.halfmove_clock = 0
        
        if nueva_posicion == juega.ep_casill:
            new_juega.tablero = remueve_ep_capturado(new_juega)
    
        if doble_avance(abandona_posicion, nueva_posicion):
            new_juega.ep_casill = new_ep_casill(abandona_posicion)
            
        if nueva_posicion&(RANGO_1|RANGO_8):
            new_juega.tablero[bb2index(abandona_posicion)] = new_juega.mueve_prim|QUEEN

    #Resetea ep_casill si no fue actualizado
    if new_juega.ep_casill == juega.ep_casill:
        new_juega.ep_casill = 0

    #Actualiza reglas de enroque para la torre
    if abandona_posicion == str2bb('a1'):
        new_juega.enroque_reglas = remueve_enroque_reglas(new_juega, ENROCAR_QUEENSIDE_BLANCO)
    if abandona_posicion == str2bb('h1'):
        new_juega.enroque_reglas = remueve_enroque_reglas(new_juega, ENROCAR_KINGSIDE_BLANCO)
    if abandona_posicion == str2bb('a8'):
        new_juega.enroque_reglas = remueve_enroque_reglas(new_juega, ENROCAR_QUEENSIDE_NEGRO)
    if abandona_posicion == str2bb('h8'):
        new_juega.enroque_reglas = remueve_enroque_reglas(new_juega, ENROCAR_KINGSIDE_NEGRO)

    #Enroque
    if get_pieza(new_juega.tablero, abandona_posicion) == BLANCO|KING:
        new_juega.enroque_reglas = remueve_enroque_reglas(new_juega, ENROCAR_KINGSIDE_BLANCO|ENROCAR_QUEENSIDE_BLANCO)
        if abandona_posicion == str2bb('e1'):
            if nueva_posicion == str2bb('g1'):
                new_juega.tablero = mueve_pieza(new_juega.tablero, [str2bb('h1'), str2bb('f1')])
            if nueva_posicion == str2bb('c1'):
                new_juega.tablero = mueve_pieza(new_juega.tablero, [str2bb('a1'), str2bb('d1')])

    if get_pieza(new_juega.tablero, abandona_posicion) == NEGRO|KING:
        new_juega.enroque_reglas = remueve_enroque_reglas(new_juega, ENROCAR_KINGSIDE_NEGRO|ENROCAR_QUEENSIDE_NEGRO)
        if abandona_posicion == str2bb('e8'):
            if nueva_posicion == str2bb('g8'):
                new_juega.tablero = mueve_pieza(new_juega.tablero, [str2bb('h8'), str2bb('f8')])
            if nueva_posicion == str2bb('c8'):
                new_juega.tablero = mueve_pieza(new_juega.tablero, [str2bb('a8'), str2bb('d8')])

    #Actualiza posiciones y siguiente movimiento
    new_juega.tablero = mueve_pieza(new_juega.tablero, (abandona_posicion, nueva_posicion))
    new_juega.mueve_prim = opuesto_color(new_juega.mueve_prim)
    
    #Actualiza historial
    new_juega.movimientos_historial.append(movim2str(movim))
    new_juega.posicion_historial.append(new_juega.to_FEN())
    return new_juega

#Retorna el historial de nuevos movimientos
def deshace_movim(juega):
    if len(juega.posicion_historial) < 2:
        return deepcopy(juega)
    
    new_juega = Juega(juega.posicion_historial[-2])
    new_juega.movimientos_historial = deepcopy(juega.movimientos_historial)[:-1]
    new_juega.posicion_historial = deepcopy(juega.posicion_historial)[:-1]
    return new_juega

#Retorna el nuevo enmascarado dentro de los rangos 
def get_rango(rango_num):
    rango_num = int(rango_num)
    return RANGO_MASKS[rango_num]

#Retorna el numero de la posicion correspondiente a cada fila dentro de la cadena
def get_fila(fila_str):
    fila_str = fila_str.lower()
    fila_num = FILAS.index(fila_str)
    return FILA_MASK[fila_num]

#Filtra cadenas o rangos segun donde se encuentre 
def get_filtro(filtro_str):
    if filtro_str in FILAS:
        return get_fila(filtro_str)
    if filtro_str in RANGOS:
        return get_rango(filtro_str)

#Peon


#Caballo


#Rey


#Alfil


#Torre


#Reina


#Funciones, Ataques, Evaluaciones


#Puntajes


#Reglas


#Evaluaciones de Movimientos / Árbol Binario


#Modos de Juego