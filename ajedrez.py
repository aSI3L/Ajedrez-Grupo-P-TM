#Inicialización


# ========== JUEGO ==========

class Juega:
	#Funcion donde se instancia el talero y los movimientos
    def __init__(self, FEN=''):
        self.tablero = TABLERO_INICIO
        self.mueve_prim = BLANCO
        self.ep_casill = 0
        self.enroque_reglas = FULL_ENROQUE_REGLAS
        self.halfmove_clock = 0
        self.fullmove_number = 1

        self.posicion_historial = []
        if FEN != '':
            self.load_FEN(FEN)
            self.posicion_historial.append(FEN)
        else:
            self.posicion_historial.append(INICIAL_FEN)
            
        self.movimientos_historial = []

   #Funcion que retorna los movimientos
    def get_mov_list(self):
        return ' '.join(self.movimientos_historial)

    #Funcion que trabaja con el rango de movimientos de las fichas (zona vertical del tablero)
    def to_FEN(self):
        FEN_str = ''

        for i in range(len(RANGOS)):
            primer = len(self.tablero) - 8*(i+1)
            vacio_casill = 0
            for fille in range(len(FILAS)):
                pieza = self.tablero[primer+fille]
                if pieza&PIEZA_MASK == VACIO:
                    vacio_casill += 1
                else:
                    if vacio_casill > 0:
                        FEN_str += '{}'.format(vacio_casill)
                    FEN_str += '{}'.format(pieza_str(pieza))
                    vacio_casill = 0
            if vacio_casill > 0:
                FEN_str += '{}'.format(vacio_casill)
            FEN_str += '/'
        FEN_str = FEN_str[:-1] + ' '

        if self.mueve_prim == BLANCO:
            FEN_str += 'b '
        if self.mueve_prim == NEGRO:
            FEN_str += 'n '

        if self.enroque_reglas & ENROCAR_KINGSIDE_BLANCO:
            FEN_str += 'K'
        if self.enroque_reglas & ENROCAR_QUEENSIDE_BLANCO:
            FEN_str += 'Q'
        if self.enroque_reglas & ENROCAR_KINGSIDE_NEGRO:
            FEN_str += 'k'
        if self.enroque_reglas & ENROCAR_QUEENSIDE_NEGRO:
            FEN_str += 'q'
        if self.enroque_reglas == 0:
            FEN_str += '-'
        FEN_str += ' '

        if self.ep_casill == 0:
            FEN_str += '-'
        else:
            FEN_str += bb2str(self.ep_casill)

        FEN_str += ' {}'.format(self.halfmove_clock)
        FEN_str += ' {}'.format(self.fullmove_number)
        return FEN_str

    #Funcion que separa y ordena las piezas del tablero (Blancas y Negras) en una especie de lista o cadena separadas
    #una de otra instanciado los objetos que seran invocados para utilizar el metodo
    def load_FEN(self, FEN_str):
        FEN_list = FEN_str.split(' ')
        
        tablero_str = FEN_list[0]
        rango_list = tablero_str.split('/')
        rango_list.reverse()
        self.tablero = []

        for rango in rango_list:
            rango_piezas = []
            for p in rango:
                if p.isdigit():
                    for _ in range(int(p)):
                        rango_piezas.append(VACIO)
                else:
                    rango_piezas.append(pieza_str(p))
            self.tablero.extend(rango_piezas)

        mueve_prim_str = FEN_list[1].lower()
        if mueve_prim_str == 'b':
            self.mueve_prim = BLANCO
        if mueve_prim_str == 'n':
            self.mueve_prim = NEGRO

        enroque_reglas_str = FEN_list[2]
        self.enroque_reglas = 0
        if enroque_reglas_str.find('K') >= 0:
            self.enroque_reglas |= ENROCAR_KINGSIDE_BLANCO
        if enroque_reglas_str.find('Q') >= 0:
            self.enroque_reglas |= ENROCAR_QUEENSIDE_BLANCO
        if enroque_reglas_str.find('k') >= 0:
            self.enroque_reglas |= ENROCAR_KINGSIDE_NEGRO
        if enroque_reglas_str.find('q') >= 0:
            self.enroque_reglas |= ENROCAR_QUEENSIDE_NEGRO

        ep_str = FEN_list[3]
        if ep_str == '-':
            self.ep_casill = 0
        else:
            self.ep_casill = str2bb(ep_str)
        
        self.halfmove_clock = int(FEN_list[4])
        self.fullmove_number = int(FEN_list[5])

# ========== FUNCIONES ==========

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

# ==================== PIEZAS ====================

# ========== PEON ==========

def get_peones_total(tablero):
    return list2int([ i&PIEZA_MASK == PEON for i in tablero ])

def get_peones(tablero, color):
    return list2int([ i == color|PEON for i in tablero ])

def peon_movimientos(moviendo_pieza, juega, color):
    return peon_avance(moviendo_pieza, juega.tablero, color) | peon_capturas(moviendo_pieza, juega, color)

def peon_capturas(moviendo_pieza, juega, color):
    return peon_simple_capturas(moviendo_pieza, juega, color) | peon_ep_capturas(moviendo_pieza, juega, color)

def peon_avance(moviendo_pieza, tablero, color):
    return peon_simple_avance(moviendo_pieza, tablero, color) | peon_doble_avance(moviendo_pieza, tablero, color)

def peon_simple_capturas(atacando_pieza, juega, color):
    return peon_ataca(atacando_pieza, juega.tablero, color) & get_piezas_color(juega.tablero, opuesto_color(color))

def peon_ep_capturas(atacando_pieza, juega, color):
    if color == BLANCO:
        ep_casilleros = juega.ep_casill & RANGO_6
    if color == NEGRO:
        ep_casilleros = juega.ep_casill & RANGO_3
    return peon_ataca(atacando_pieza, juega.tablero, color) & ep_casilleros

def peon_ataca(atacando_pieza, tablero, color):
    return peon_este_ataca(atacando_pieza, tablero, color) | peon_oeste_ataca(atacando_pieza, tablero, color)

def peon_simple_avance(moviendo_pieza, tablero, color):
    if color == BLANCO:
        return lado_norte(moviendo_pieza) & vacio_casilleros(tablero)
    if color == NEGRO:
        return lado_sur(moviendo_pieza) & vacio_casilleros(tablero)

def peon_doble_avance(moviendo_pieza, tablero, color):
    if color == BLANCO:
        return lado_norte(peon_simple_avance(moviendo_pieza, tablero, color)) & (vacio_casilleros(tablero) & RANGO_4)
    if color == NEGRO:
        return lado_sur(peon_simple_avance(moviendo_pieza, tablero, color)) & (vacio_casilleros(tablero) & RANGO_5)

def peon_este_ataca(atacando_pieza, tablero, color):
    if color == BLANCO:
        return lado_NE(atacando_pieza & get_piezas_color(tablero, color))
    if color == NEGRO:
        return lado_SE(atacando_pieza & get_piezas_color(tablero, color))

def peon_oeste_ataca(atacando_pieza, tablero, color):
    if color == BLANCO:
        return lado_NO(atacando_pieza & get_piezas_color(tablero, color))
    if color == NEGRO:
        return lado_SO(atacando_pieza & get_piezas_color(tablero, color))

def peon_doble_ataca(atacando_pieza, tablero, color):
    return peon_este_ataca(atacando_pieza, tablero, color) & peon_este_ataca(atacando_pieza, tablero, color)

def doble_avance(abandona_casillero, destino_casillero):
    return (abandona_casillero&RANGO_2 and destino_casillero&RANGO_4) or \
           (abandona_casillero&RANGO_7 and destino_casillero&RANGO_5)

def new_ep_casill(abandona_casillero):
    if abandona_casillero&RANGO_2:
        return lado_norte(abandona_casillero)
    if abandona_casillero&RANGO_7:
        return lado_sur(abandona_casillero)

def remueve_ep_capturado(juega):
    new_tablero = deepcopy(juega.tablero)
    if juega.ep_casill & RANGO_3:
        new_tablero[bb2index(lado_norte(juega.ep_casill))] = VACIO
    if juega.ep_casill & RANGO_6:
        new_tablero[bb2index(lado_sur(juega.ep_casill))] = VACIO
    return new_tablero

# ========== CABALLO ==========

def get_caballos(tablero, color):
    return list2int([ i == color|CABALLO for i in tablero ])

def caballo_movimientos(moviendo_pieza, tablero, color):
    return caballo_ataca(moviendo_pieza) & nnot(get_piezas_color(tablero, color))

def caballo_ataca(moviendo_pieza):
    return caballo_NNE(moviendo_pieza) | \
           caballo_ENE(moviendo_pieza) | \
           caballo_NNO(moviendo_pieza) | \
           caballo_ONO(moviendo_pieza) | \
           caballo_SSE(moviendo_pieza) | \
           caballo_ESE(moviendo_pieza) | \
           caballo_SSO(moviendo_pieza) | \
           caballo_OSO(moviendo_pieza)

def caballo_ONO(moviendo_pieza):
    return moviendo_pieza << 6 & nnot(FILA_G | FILA_H)

def caballo_ENE(moviendo_pieza):
    return moviendo_pieza << 10 & nnot(FILA_A | FILA_B)

def caballo_NNO(moviendo_pieza):
    return moviendo_pieza << 15 & nnot(FILA_H)

def caballo_NNE(moviendo_pieza):
    return moviendo_pieza << 17 & nnot(FILA_A)

def caballo_ESE(moviendo_pieza):
    return moviendo_pieza >> 6 & nnot(FILA_A | FILA_B)

def caballo_OSO(moviendo_pieza):
    return moviendo_pieza >> 10 & nnot(FILA_G | FILA_H)

def caballo_SSE(moviendo_pieza):
    return moviendo_pieza >> 15 & nnot(FILA_A)

def caballo_SSO(moviendo_pieza):
    return moviendo_pieza >> 17 & nnot(FILA_H)

def caballo_llena(moviendo_pieza, n):
    llena = moviendo_pieza
    for _ in range(n):
        llena |= caballo_ataca(llena)
    return llena

def caballo_distancia(pos1, pos2):
    init_bitboard = str2bb(pos1)
    end_bitboard = str2bb(pos2)
    llena = init_bitboard
    dist = 0
    while llena & end_bitboard == 0:
        dist += 1
        llena = caballo_llena(init_bitboard, dist)
    return dist

# ========== REY ==========

def get_king(tablero, color):
    return list2int([ i == color|KING for i in tablero ])

def king_movimientos(moviendo_pieza, tablero, color):
    return king_ataca(moviendo_pieza) & nnot(get_piezas_color(tablero, color))

def king_ataca(moviendo_pieza):
    king_atq = moviendo_pieza | lado_este(moviendo_pieza) | lado_oeste(moviendo_pieza)
    king_atq |= lado_norte(king_atq) | lado_sur(king_atq)
    return king_atq & nnot(moviendo_pieza)

def puede_enrocar_kingside(juega, color):
    if color == BLANCO:
        return (juega.enroque_reglas & ENROCAR_KINGSIDE_BLANCO) and \
                juega.tablero[str2index('f1')] == VACIO and \
                juega.tablero[str2index('g1')] == VACIO and \
                (not bajo_ataque(str2bb('e1'), juega.tablero, opuesto_color(color))) and \
                (not bajo_ataque(str2bb('f1'), juega.tablero, opuesto_color(color))) and \
                (not bajo_ataque(str2bb('g1'), juega.tablero, opuesto_color(color)))
    if color == NEGRO:
        return (juega.enroque_reglas & ENROCAR_KINGSIDE_NEGRO) and \
                juega.tablero[str2index('f8')] == VACIO and \
                juega.tablero[str2index('g8')] == VACIO and \
                (not bajo_ataque(str2bb('e8'), juega.tablero, opuesto_color(color))) and \
                (not bajo_ataque(str2bb('f8'), juega.tablero, opuesto_color(color))) and \
                (not bajo_ataque(str2bb('g8'), juega.tablero, opuesto_color(color)))

def puede_enrocar_queenside(juega, color):
    if color == BLANCO:
        return (juega.enroque_reglas & ENROCAR_QUEENSIDE_BLANCO) and \
                juega.tablero[str2index('b1')] == VACIO and \
                juega.tablero[str2index('c1')] == VACIO and \
                juega.tablero[str2index('d1')] == VACIO and \
                (not bajo_ataque(str2bb('c1'), juega.tablero, opuesto_color(color))) and \
                (not bajo_ataque(str2bb('d1'), juega.tablero, opuesto_color(color))) and \
                (not bajo_ataque(str2bb('e1'), juega.tablero, opuesto_color(color)))
    if color == NEGRO:
        return (juega.enroque_reglas & ENROCAR_QUEENSIDE_NEGRO) and \
                juega.tablero[str2index('b8')] == VACIO and \
                juega.tablero[str2index('c8')] == VACIO and \
                juega.tablero[str2index('d8')] == VACIO and \
                (not bajo_ataque(str2bb('c8'), juega.tablero, opuesto_color(color))) and \
                (not bajo_ataque(str2bb('d8'), juega.tablero, opuesto_color(color))) and \
                (not bajo_ataque(str2bb('e8'), juega.tablero, opuesto_color(color)))

def enrocar_kingside_movim(juega):
    if juega.mueve_prim == BLANCO:
        return (str2bb('e1'), str2bb('g1'))
    if juega.mueve_prim == NEGRO:
        return (str2bb('e8'), str2bb('g8'))

def enrocar_queenside_movim(juega):
    if juega.mueve_prim == BLANCO:
        return (str2bb('e1'), str2bb('c1'))
    if juega.mueve_prim == NEGRO:
        return (str2bb('e8'), str2bb('c8'))

def remueve_enroque_reglas(juega, removidas_reglas):
    return juega.enroque_reglas & ~removidas_reglas

# ========== ALFIL ==========

def get_alfiles(tablero, color):
    return list2int([ i == color|ALFIL for i in tablero ])

def alfil_linea(moviendo_pieza):
    return linea_diag(moviendo_pieza) | linea_anti_diag(moviendo_pieza)
           
def linea_diag(moviendo_pieza):
    return NE_linea(moviendo_pieza) | SO_linea(moviendo_pieza)

def linea_anti_diag(moviendo_pieza):
    return NO_linea(moviendo_pieza) | SE_linea(moviendo_pieza)

def linea_NE(moviendo_pieza):
    linea_atq = lado_NE(moviendo_pieza)
    for _ in range(6):
        linea_atq |= lado_NE(linea_atq)
    return linea_atq & CASILLEROS

def linea_SE(moviendo_pieza):
    linea_atq = lado_SE(moviendo_pieza)
    for _ in range(6):
        linea_atq |= lado_SE(linea_atq)
    return linea_atq & CASILLEROS

def linea_NO(moviendo_pieza):
    linea_atq = lado_NO(moviendo_pieza)
    for _ in range(6):
        linea_atq |= lado_NO(linea_atq)
    return linea_atq & CASILLEROS

def linea_SO(moviendo_pieza):
    linea_atq = lado_SO(moviendo_pieza)
    for _ in range(6):
        linea_atq |= lado_SO(linea_atq)
    return linea_atq & CASILLEROS

def ataca_NE(pieza_indiv, tablero, color):
    bloq = lsb(linea_NE(pieza_indiv) & ocupado_casilleros(tablero))
    if bloq:
        return linea_NE(pieza_indiv) ^ linea_NE(bloq)
    else:
        return linea_NE(pieza_indiv)
    
def ataca_NO(pieza_indiv, tablero, color):
    bloq = lsb(linea_NO(pieza_indiv) & ocupado_casilleros(tablero))
    if bloq:
        return linea_NO(pieza_indiv) ^ linea_NO(bloq)
    else:
        return linea_NO(pieza_indiv)

def ataca_SE(pieza_indiv, tablero, color):
    bloq = msb(linea_SE(pieza_indiv) & ocupado_casilleros(tablero))
    if bloq:
        return linea_SE(pieza_indiv) ^ linea_SE(bloq)
    else:
        return linea_SE(pieza_indiv)

def ataca_SO(pieza_indiv, tablero, color):
    bloq = msb(linea_SO(pieza_indiv) & ocupado_casilleros(tablero))
    if bloq:
        return linea_SO(pieza_indiv) ^ linea_SO(bloq)
    else:
        return linea_SO(pieza_indiv)

def diagonal_ataca(pieza_indiv, tablero, color):
    return ataca_NE(pieza_indiv, tablero, color) | ataca_SO(pieza_indiv, tablero, color)

def anti_diagonal_ataca(pieza_indiv, tablero, color):
    return ataca_NO(pieza_indiv, tablero, color) | ataca_SE(pieza_indiv, tablero, color)

def alfil_ataca(moviendo_pieza, tablero, color):
    atq = 0
    for pieza in indiv_gen(moviendo_pieza):
        atq |= diagonal_ataca(pieza, tablero, color) | anti_diagonal_ataca(pieza, tablero, color)
    return atq

def alfil_movimientos(moviendo_pieza, tablero, color):
    return alfil_ataca(moviendo_pieza, tablero, color) & nnot(get_piezas_color(tablero, color))

#========== TORRE ==========

def get_torres(board, color):
    return list2int([ i == color|TORRE for i in tablero ])

def torre_lineas(moviendo_pieza):
    return rango_lineas(moviendo_pieza) | fila_lineas(moviendo_pieza)

def rango_lineas(moviendo_pieza):
    return linea_este(moviendo_pieza) | linea_oeste(moviendo_pieza)

def fila_lineas(moviendo_pieza):
    return linea_norte(moviendo_pieza) | linea_sur(moviendo_pieza)

def linea_este(moviendo_pieza):
    linea_atq = lado_este(moviendo_pieza)
    for _ in range(6):
        linea_atq |= lado_este(linea_atq)
    return linea_atq & CASILLEROS

def linea_oeste(moviendo_pieza):
    linea_atq = lado_oeste(moviendo_pieza)
    for _ in range(6):
        linea_atq |= lado_oeste(linea_atq)
    return linea_atq & CASILLEROS

def linea_norte(moviendo_pieza):
    linea_atq = lado_norte(moviendo_pieza)
    for _ in range(6):
        linea_atq |= lado_norte(linea_atq)
    return linea_atq & CASILLEROS

def linea_sur(moviendo_pieza):
    linea_atq = lado_sur(moviendo_pieza)
    for _ in range(6):
        linea_atq |= lado_sur(linea_atq)
    return linea_atq & CASILLEROS

def ataca_este(pieza_indiv, tablero, color):
    bloq = lsb(linea_este(pieza_indiv) & ocupado_casilleros(tablero))
    if bloq:
        return linea_este(pieza_indiv) ^ linea_este(bloq)
    else:
        return linea_este(pieza_indiv)
    
def ataca_oeste(pieza_indiv, tablero, color):
    bloq = msb(linea_oeste(pieza_indiv) & ocupado_casilleros(tablero))
    if bloq:
        return linea_oeste(pieza_indiv) ^ linea_oeste(bloq)
    else:
        return linea_oeste(pieza_indiv)

def rango_ataca(pieza_indiv, tablero, color):
    return ataca_este(pieza_indiv, tablero, color) | ataca_oeste(pieza_indiv, tablero, color)

def ataca_norte(pieza_indiv, tablero, color):
    bloq = lsb(linea_norte(pieza_indiv) & ocupado_casilleros(tablero))
    if bloq:
        return linea_norte(pieza_indiv) ^ linea_norte(bloq)
    else:
        return linea_norte(pieza_indiv)
    
def ataca_sur(pieza_indiv, tablero, color):
    bloq = msb(linea_sur(pieza_indiv) & ocupado_casilleros(tablero))
    if bloq:
        return linea_sur(pieza_indiv) ^ linea_sur(bloq)
    else:
        return linea_sur(pieza_indiv)

def fila_ataca(pieza_indiv, tablero, color):
    return ataca_norte(pieza_indiv, tablero, color) | ataca_sur(pieza_indiv, tablero, color)

def torre_ataca(moviendo_pieza, tablero, color):
    atq = 0
    for pieza_indiv in indiv_gen(moviendo_pieza):
        atq |= rango_ataca(pieza_indiv, tablero, color) | fila_ataca(pieza_indiv, tablero, color)
    return atq

def torre_movimientos(moviendo_pieza, tablero, color):
    return torre_ataca(moviendo_pieza, tablero, color) & nnot(get_piezas_color(tablero, color))

# ========== REINA ==========

def get_queen(tablero, color):
    return list2int([ i == color|QUEEN for i in tablero ])

def queen_lineas(moviendo_pieza):
    return torre_lineas(moviendo_pieza) | alfil_linea(moviendo_pieza)

def queen_ataca(moviendo_pieza, tablero, color):
    return alfil_ataca(moviendo_pieza, tablero, color) | torre_ataca(moviendo_pieza, tablero, color)

def queen_movimientos(moviendo_pieza, tablero, color):
    return alfil_movimientos(moviendo_pieza, tablero, color) | torre_movimientos(moviendo_pieza, tablero, color)

# ========== FUNCIONES, ATAQUES, EVALUACIONES ==========

#Define situacion de ataque segun color c/contador
def bajo_ataque(objetivo, tablero, atacando_color):
    return cuenta_ataques(objetivo, tablero, atacando_color) > 0

#Define situacion de jaque cuando rey esta bajo ataque
def jaque(tablero, color):
    return bajo_ataque(get_king(tablero, color), tablero, opuesto_color(color))

#Retorna la pieza y color que ataca
def get_ataques(moviendo_pieza, tablero, color):
    pieza = tablero[bb2index(moviendo_pieza)]

    if pieza&PIEZA_MASK == PEON:
        return peon_ataca(moviendo_pieza, tablero, color)
    elif pieza&PIEZA_MASK == CABALLO:
        return caballo_ataca(moviendo_pieza)
    elif pieza&PIEZA_MASK == ALFIL:
        return alfil_ataca(moviendo_pieza, tablero, color)
    elif pieza&PIEZA_MASK == TORRE:
        return torre_ataca(moviendo_pieza, tablero, color)
    elif pieza&PIEZA_MASK == QUEEN:
        return queen_ataca(moviendo_pieza, tablero, color)
    elif pieza&PIEZA_MASK == KING:
        return king_ataca(moviendo_pieza)

#Define el movimiento de piezas con el tipo de pieza
def get_movimientos(moviendo_pieza, juega, color):
    pieza = juega.tablero[bb2index(moviendo_pieza)]

    if pieza&PIEZA_MASK == PEON:
        return peon_movimientos(moviendo_pieza, juega, color)
    elif pieza&PIEZA_MASK == CABALLO:
        return caballo_movimientos(moviendo_pieza, juega.tablero, color)
    elif pieza&PIEZA_MASK == ALFIL:
        return alfil_movimientos(moviendo_pieza, juega.tablero, color)
    elif pieza&PIEZA_MASK == TORRE:
        return torre_movimientos(moviendo_pieza, juega.tablero, color)
    elif pieza&PIEZA_MASK == QUEEN:
        return queen_movimientos(moviendo_pieza, juega.tablero, color)
    elif pieza&PIEZA_MASK == KING:
        return king_movimientos(moviendo_pieza, juega.tablero, color)

#Contador de ataques segun el color
def cuenta_ataques(objetivo, tablero, atacando_color):
    ataque_contador = 0

    for index in range(64):
        pieza = tablero[index]
        if pieza != VACIO and pieza&COLOR_MASK == atacando_color:
            pos = 0b1 << index
            
            if get_ataques(pos, tablero, atacando_color) & objetivo:
                ataque_contador += 1
                      
    return ataque_contador

#Cuenta el material en tablero
def material_sumat(tablero, color):
    material = 0
    for pieza in tablero:
        if pieza&COLOR_MASK == color:
            material += PIEZA_VALOR[pieza&PIEZA_MASK]
    return material

#Evalua diferencia de material entre jugadores
def material_saldo(tablero):
    return material_sumat(tablero, BLANCO) - material_sumat(tablero, NEGRO)

#Evalua diferenccia de movimientos entre jugadores
def movimientos_saldo(juega):
    return cont_movim_legales(juega, BLANCO) - cont_movim_legales(juega, NEGRO)

#Evalua estado del juego
def evalua_juego(juega):
    if finaliza_juego(juega):
        return evalua_final(juega)
    else:
        return material_saldo(juega.tablero) + saldo_posicion(juega)

#Evalua condicion de finalizacion
def evalua_final(juega):
    if jaquemate(juega, juega.mueve_prim):
        return puntaje(juega.mueve_prim)
    elif juego_ahogado(juega) or \
         material_insuficiente(juega) or \
         menos_75_movim_regla(juega):
        return 0

# ========== PUNTAJES ==========

def saldo_posicion(juega):
    return bonus_posicion(juega, BLANCO) - bonus_posicion(juega, NEGRO) 

def bonus_posicion(juega, color):
    bonus = 0
    
    if color == BLANCO:
        tablero = juega.tablero
    elif color == NEGRO:
        tablero = inv_tablero_v(juega.tablero)
        
    for index in range(64):
        pieza = tablero[index]
        
        if pieza != VACIO and pieza&COLOR_MASK == color:
            pieza_tipo = pieza&PIEZA_MASK
            
            if pieza_tipo == PEON:
                bonus += PEON_BONUS[index]
            elif pieza_tipo == CABALLO:
                bonus += CABALLO_BONUS[index]
            elif pieza_tipo == ALFIL:
                bonus += ALFIL_BONUS[index]
             
            elif pieza_tipo == TORRE:
                posicion = 0b1 << index
                 
                if is_open_file(posicion, tablero):
                    bonus += TORRE_OPEN_FILE_BONUS
                elif is_semi_open_file(posicion, tablero):
                    bonus += TORRE_SEMI_OPEN_FILE_BONUS
                     
                if posicion & RANGO_7:
                    bonus += TORRE_EN_SEPTIMA_BONUS
                 
            elif pieza_tipo == KING:
                if fin_del_juego(tablero):
                    bonus += KING_FINJUEG_BONUS[index]
                else:
                    bonus += KING_BONUS[index]
    
    return bonus

def fin_del_juego(tablero):
    return cuenta_piezas(ocupado_casilleros(tablero)) <= FINJUEG_PIEZA_RESUL

#Open file: fila sin peones
def is_open_file(bitboard, tablero):
    for f in FILAS:
        rango_filtro = get_fila(f)
        if bitboard & rango_filtro:
            return cuenta_piezas(get_peones_total(tablero)&rango_filtro) == 0

#Semi open file: fila con peones de un solo color
def is_semi_open_file(bitboard, tablero):
    for f in FILAS:
        rango_filtro = get_fila(f)
        if bitboard & rango_filtro:
            return cuenta_piezas(get_peones_total(tablero)&rango_filtro) == 1

#Cuenta espacios ocupados en el tablero de bits
def cuenta_piezas(bitboard):
    return bin(bitboard).count("1")

#Evalua puntaje por color
def puntaje(color):
    if color == BLANCO:
        return -10*PIEZA_VALOR[KING]
    if color == NEGRO:
        return 10*PIEZA_VALOR[KING]

#Movimientos que no tienen en cuenta las demas piezas
def movim_pseudo_legales(juega, color):
    for index in range(64):
        pieza = juega.tablero[index]

        if pieza != VACIO and pieza&COLOR_MASK == color:
            pieza_pos = 0b1 << index
            
            for objetivo in indiv_gen(get_movimientos(pieza_pos, juega, color)):
                yield (pieza_pos, objetivo)

    if puede_enrocar_kingside(juega, color):
        yield (get_king(juega.tablero, color), lado_este(lado_este(get_king(juega.tablero, color))))
    if puede_enrocar_queenside(juega, color):
        yield (get_king(juega.tablero, color), lado_oeste(lado_oeste(get_king(juega.tablero, color))))

#Movimientos permitidos
def movimientos_legales(juega, color):
    for movim in movim_pseudo_legales(juega, color):
        if movim_legal(juega, movim):
            yield movim

#Movimientos que no dejan al propio rey en jaque
def movim_legal(juega, movim):
    new_juega = mueve(juega, movim)
    return not jaque(new_juega.tablero, juega.mueve_prim)

#Contador de movimientos permitidos
def cont_movim_legales(juega, color):
    cuenta_movim = 0
    for _ in movimientos_legales(juega, color):
        cuenta_movim += 1
    return cuenta_movim

def juego_ahogado(juega):
    for _ in movimientos_legales(juega, juega.mueve_prim):
        return False
    return not jaque(juega.tablero, juega.mueve_prim)
  
def jaquemate(juega, color):
    for _ in movimientos_legales(juega, juega.mueve_prim):
        return False
    return jaque(juega.tablero, color)  

def misma_posicion(FEN_a, FEN_b):
    FEN_a_list = FEN_a.split(' ')
    FEN_b_list = FEN_b.split(' ')
    return FEN_a_list[0] == FEN_b_list[0] and \
           FEN_a_list[1] == FEN_b_list[1] and \
           FEN_a_list[2] == FEN_b_list[2] and \
           FEN_a_list[3] == FEN_b_list[3]

#Reglas

#Si la misma posicion ocurre 3 veces -> tablas
def triple_repeticion(juega):
    posicion_actual = juega.posicion_historial[-1]
    cuenta_posicion = 0
    for posicion in juega.posicion_historial:
        if misma_posicion(posicion_actual, posicion):
            cuenta_posicion += 1
    return cuenta_posicion >= 3
#si luego de 50 movimientos no se producen capturas -> tablas
def menos_50_movim_regla(juega):
    return juega.halfmove_clock >= 100
#si no hay capturas en 75 movimientos -> tablas
def menos_75_movim_regla(juega):
    return juega.halfmove_clock >= 150
#EVALUA LAS 4 COMBINACIONES PARA QUE SE DE UN EMPATE POR MATERIAL INSUFICIENTE (MATERIALES SON LAS PIEZAS 
#EN EL TABLERO), LA REGLA TIENE EN CUENTA ALFILES, CABALLOS Y REY
def material_insuficiente(juega):
    if material_sumat(juega.tablero, BLANCO) + material_sumat(juega.tablero, NEGRO) == 2*PIEZA_VALOR[KING]:
        return True
    if material_sumat(juega.tablero, BLANCO) == PIEZA_VALOR[KING]:
        if material_sumat(juega.tablero, NEGRO) == PIEZA_VALOR[KING] + PIEZA_VALOR[CABALLO] and \
        (get_caballos(juega.tablero, NEGRO) != 0 or get_alfiles(game.tablero, NEGRO) != 0):
            return True
    if material_sumat(juega.tablero, NEGRO) == PIEZA_VALOR[KING]:
        if material_sumat(juega.tablero, BLANCO) == PIEZA_VALOR[KING] + PIEZA_VALOR[CABALLO] and \
        (get_caballos(juega.tablero, BLANCO) != 0 or get_alfiles(juega.tablero, BLANCO) != 0):
            return True
    return False #DEVUELVE FALSO SI NO SE DA LA CONDICION

#devuelve la condicion del juego terminado
def finaliza_juego(juega):
    return jaquemate(juega, BLANCO) or \
           jaquemate(juega, NEGRO) or \
           juego_ahogado(juega) or \
           material_insuficiente(juega) or \
           menos_75_movim_regla(juega)

def movim_aleat(juega, color):
    return choice(movim_legal(juega, color))
#evalua puntajes y guarda los mayores
def movim_evaluado(juega, color):
    mejor_puntaje = puntaje(color)
    mejor_movimientos = []
    
    for movim in movimientos_legales(juega, color):
        evalua = evalua_juego(mueve(juega, movim))
        
        if jaquemate(mueve(juega, movim), opuesto_color(juega.mueve_prim)):
            return [movim, evalua]
        
        if (color == BLANCO and evalua > mejor_puntaje) or \
           (color == NEGRO  and evalua < mejor_puntaje):
            mejor_puntaje = evalua
            mejor_movimientos = [movim]
        elif evalua == mejor_puntaje:
            mejor_movimientos.append(movim)
                
    return [choice(mejor_movimientos), mejor_puntaje]

#Evaluaciones de Movimientos / Árbol Binario
#genera arbol binario de movimientos optimos 
def minimax(juega, color, profund=1):
    if finaliza_juego(juega):
        return [None, evalua_juego(juega)]
    
    [movim_simple, evaluacion_simple] = movim_evaluado(juega, color)
    
    if profund == 1 or \
       evaluacion_simple == puntaje(opuesto_color(color)):
        return [movim_simple, evaluacion_simple]
    
    mejor_puntaje = puntaje(color)
    mejor_movimientos = []
    
    for movim in movim_legal(juega, color):
        su_juego = mueve(juega, movim)
        
        if jaquemate(su_juego, su_juego.mueve_prim):
            return [movim, puntaje(su_juego.mueve_prim)]
            
        [_, evalua] = minimax(su_juego, opuesto_color(color), profund-1)
        
        if evalua == puntaje(opuesto_color(color)):
            return [movim, evalua]
        
        if (color == BLANCO and evalua > mejor_puntaje) or \
           (color == NEGRO and evalua < mejor_puntaje):
            mejor_puntaje = evalua
            mejor_movimientos = [movim]
        elif evalua == mejor_puntaje:
            mejor_movimientos.append(movim)
        
    return [choice(mejor_movimientos), mejor_puntaje]
#"poda" los subarboles de minimax que considera que NO seran seleccionados
def alpha_beta(juega, color, profund, alpha=-float('inf'), beta=float('inf')):
    if finaliza_juego(juega):
        return [None, evalua_juego(juega)]
    
    [movim_simple, evaluacion_simple] = movim_evaluado(juega, color)
    
    if profund == 1 or \
       evaluacion_simple == puntaje(opuesto_color(color)):
        return [movim_simple, evaluacion_simple]

    mejor_movimientos = []
        
    if color == BLANCO:
        for movim in movimientos_legales(juega, color):
            if verbose:
                print('\t'*profund + str(profund) + '. evaluando ' + PIEZA_CODIG[get_pieza(juega.tablero, movim[0])] + movim2str(movim))
                
            new_juega = mueve(juega, movim)
            [_, puntos] = alpha_beta(new_juega, opuesto_color(color), profund-1, alpha, beta)
            
            if verbose:
                print('\t'*profund + str(profund) + '. ' + str(puntos) + ' [{},{}]'.format(alpha, beta))
            
            if puntos == puntaje(opuesto_color(color)):
                return [movim, puntos]
            
            if puntos == alpha:
                mejor_movimientos.append(movim)
            if puntos > alpha: # blanco maximiza puntaje
                alpha = puntos
                mejor_movimientos = [movim]
                if alpha > beta: # poda alpha-beta 
                    if verbose:
                        print('\t'*profund + 'poda')
                    break
        if mejor_movimientos:
            return [choice(mejor_movimientos), alpha]
        else:
            return [None, alpha]
    
    if color == NEGRO:
        for movim in movimientos_legales(juega, color):
            if verbose:
                print('\t'*profund + str(profund) + '. evaluando ' + PIEZA_CODIG[get_pieza(juega.tablero, movim[0])] + movim2str(movim))
                
            new_juega = mueve(juega, movim)
            [_, puntos] = alpha_beta(new_juega, opuesto_color(color), profund-1, alpha, beta)
            
            if verbose:
                print('\t'*profund + str(profund) + '. ' + str(puntos) + ' [{},{}]'.format(alpha, beta))
            
            if puntos == puntaje(opuesto_color(color)):
                return [movim, puntos]
            
            if puntos == beta:
                mejor_movimientos.append(movim)
            if puntos < beta: # negro minimiza puntaje
                beta = puntos
                mejor_movimientos = [movim]
                if alpha > beta: # poda alpha-beta
                    if verbose:
                        print('\t'*profund + 'poda')
                    break
        if mejor_movimientos:
            return [choice(mejor_movimientos), beta]
        else:
            return [None, beta]
#evalua condiciones para hacer el movimiento
def analiza_codig_movim(juega, movim_codigo):
    movim_codigo = movim_codigo.replace(" ","")
    movim_codigo = movim_codigo.replace("x","")

    if movim_codigo.upper() == 'O-O' or movim_codigo == '0-0':
        if puede_enrocar_kingside(juega, juega.mueve_prim):
            return enrocar_kingside_movim(juega)
        
    if movim_codigo.upper() == 'O-O-O' or movim_codigo == '0-0-0':
        if puede_enrocar_queenside(juega, juega.mueve_prim):
            return enrocar_queenside_movim(juega)

    if len(movim_codigo) < 2 or len(movim_codigo) > 4:
        return False
    
    if len(movim_codigo) == 4:
        filtra_casilleros = get_filtro(movim_codigo[1])
    else:
        filtra_casilleros = CASILLEROS

    destino_str = movim_codigo[-2:]
    if destino_str[0] in FILAS and destino_str[1] in RANGOS:
        casill_objetivo = str2bb(destino_str)
    else:
        return False

    if len(movim_codigo) == 2:
        pieza = PEON
    else:
        pieza_codig = movim_codigo[0]
        if pieza_codig in FILAS:
            pieza = PEON
            filtra_casilleros = get_filtro(pieza_codig)
        elif pieza_codig in PIEZA_CODIG:
            pieza = PIEZA_CODIG[pieza_codig]&PIEZA_MASK
        else:
            return False

    movim_validos = []
    for movim in movim_legal(juega, juega.mueve_prim):
        if movim[1] & casill_objetivo and \
           movim[0] & filtra_casilleros and \
           get_pieza(juega.tablero, movim[0])&PIEZA_MASK == pieza:
            movim_validos.append(movim) 

    if len(movim_validos) == 1:
        return movim_validos[0]
    else:
        return False
#obtiene y evalua el movimiento del usuario
def get_movim_usuario(juega):
    movim = None
    while not movim:
        movim = analiza_codig_movim(juega, input())
        if not movim:
            print('Movimiento No Váido!!!')
    return movim
#obtiene y evalua el movimiento de la AI
def get_AI_movim(juega, profund=2):
    if verbose:
        print('Blanco analizando mejor jugada...' if juega.mueve_prim == BLANCO else 'Negro analizando mejor jugada...')
    start_time = time()

    if busca_en_libro(juega):
        movim = get_movim_libro(juega)  #movimiento de libro ("book.txt")
    else:
        movim = alpha_beta(juega, juega.mueve_prim, profund)[0]

    end_time = time()
    if verbose:
        print('Movimiento encontrado ' + PIEZA_CODIG[get_pieza(juega.tablero, movim[0])] + ' desde ' + str(bb2str(movim[0])) + ' hasta ' + str(bb2str(movim[1])) + ' en {:.3f} segundos'.format(end_time-start_time) + ' ({},{})'.format(evalua_juego(juega), evalua_juego(mueve(juega, movim))))
    return movim    #retorna el movimiento y detiene el reloj
#imprime salida por pantalla
def print_salida(juega):
    print(get_salida(juega))

#obtiene salida
def get_salida(juega):
    if juego_ahogado(juega):
        return 'Empate por Juego Ahogado'
    if jaquemate(juega, BLANCO):
        return '=== NEGRAS GANAN!!!! ==='
    if jaquemate(juega, NEGRO):
        return '=== BLANCAS GANAN!!!! ==='
    if material_insuficiente(juega):
        return 'Empate por piezas insuficientes!!!'
    if menos_75_movim_regla(juega):
        return 'Empate por regla de los 75 movimientos!!!'

# ========== MODOS DE JUEGO ==========

def juega_con_blancas(juega=Juega()):
    print('Jugador: BLANCAS!')
    while True:
        print_tablero(juega.tablero)
        if finaliza_juego(juega):
            break

        juega = mueve_prim(juega, get_movim_usuario(juega))
        
        print_tablero(juega.tablero)
        if finaliza_juego(juega):
            break
        
        juega = mueve_prim(juega, get_AI_movim(juega))
    print_salida(juega)

def juega_con_negras(juega=Juega()):
    print('Jugador: NEGRAS!')
    while True:
        print_rotar_tablero(juega.tablero)
        if finaliza_juego(juega):
            break

        juega = mueve(juega, get_AI_movim(juega))
        
        print_rotar_tablero(juega.tablero)
        if finaliza_juego(juega):
            break
        
        juega = mueve(juega, get_movim_usuario(juega))
    print_salida(juega)


def juega_con(color):
    if color == BLANCO:
        juega_con_blancas()
    if color == NEGRO:
        juega_con_negras()

def juega_con_aleatorio():
    color = choice([BLANCO, NEGRO])
    juega_con(color)

# ========== FICHERO ==========

def busca_en_libro(juega):
    if juega.posicion_historial[0] != INICIAL_FEN:
        return False

    fichero = []
    fichero_libro = open("libro.txt")
    for line in fichero_libro:
        if line.startswith(juega.get_mov_list()) and line.rstrip() > juega.get_mov_list():
            fichero.append(line.rstrip())
    fichero_libro.close()
    return fichero

def get_movim_libro(juega):
    fichero = busca_en_libro(juega)
    opc_fichero = choice(fichero)
    movim_siguientes = opc_fichero.replace(juega.get_mov_list(), '').lstrip()
    movim_str = movim_siguientes.split(' ')[0]
    movim = [str2bb(movim_str[:2]), str2bb(movim_str[-2:])]
    return movim