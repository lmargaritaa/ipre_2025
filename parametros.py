# Importación de bibliotecas:
import itertools

# Funciones auxiliares para el calculo de parametros:

# Al conocer las coordenadas x e y de un objeto sobre una
# plataforma de cierto largo y ancho, se pueden obtener las
# fuerzas generadas por este en cada esquina.
# Se asume plataforma rectangular:
def efecto_peso(xy, w):
    ar = xy[1] / LARGO
    ab = 1 - ar
    de = xy[0] / ANCHO
    iz = 1 - de
    pa = round(w * ar * iz, 0)
    pb = round(w * ar * de, 0)
    pc = round(w * ab * iz, 0)
    pd = round(w * ab * de, 0)
    return [pa, pb, pc, pd]

def centro_masa(lista_pesos, w, ancho, largo):
    #---ancho
    #l-------
    #a--a---b
    #r-------
    #g--c---d
    #o-------
    a = float(lista_pesos[0])
    b = float(lista_pesos[1])
    c = float(lista_pesos[2])
    d = float(lista_pesos[3])

    try:
        x = round(ancho * (b + d) / w, 2)
    except ZeroDivisionError:
        x = 0
    try:
        y = round(largo * (a + b) / w, 2)
    except ZeroDivisionError:
        y = 0

    return [x, y]

def combinaciones(dict_obj):
    combinations = []
    llaves = list(dict_obj.keys())
    for i in range(1, len(dict_obj) + 1):
        new_combinations = list(itertools.combinations(llaves, i))
        combinations += new_combinations
    return combinations

def por_peso(lista):
    return lista[0]

def datos_combos(objetos, ancho, largo):
    data = []
    combos = combinaciones(objetos)
    for combo in combos:
        pt = 0
        pabcd = [0, 0, 0, 0]
        for llave in combo:
            pt += sum(objetos[llave][3])
            pabcd = [round(p1 + p2, 1) for p1, p2 in zip(pabcd, objetos[llave][3])]
        cm = centro_masa(pabcd, pt, ancho, largo)
        data.append([pt, pabcd, cm, combo])
    data.sort(key=por_peso)
    return data
        
# Parametros:

# Datos servidor:
BROKER = "broker.emqx.io"
PORT = 1883

# Dimensiones de la plataforma:
LARGO = 2.44 #metros
ANCHO = 2.44 #metros

# Parametros sensores:
CANT = 4

# Parametros de identificacion de los objetos:
DISTANCIA = 0.3 #metros
D_PESO = 2    #kilogramos

# Diccionario objetos formato
# {"obj1": [[x,y], tiempo, [subllaves, ...], [pa,pb,pc,pd]], ...}:

OBJETOS = {
    "Pared 1": [[2.39, 1.24], 0, ["Tabla 1", "Tabla 2"], efecto_peso([2.39, 1.2], 7), "blue"],
    "Pared 2": [[2.39, 2.04], 0, ["Tabla 3", "Tabla 4"], efecto_peso([2.39, 2], 7), "blue"],
    "Pared 3": [[1.35, 2.04], 0, ["Tabla 5", "Tabla 6"], efecto_peso([1.6, 2], 7), "blue"],
    "Pared 3.5": [[1.87, 2.41], 0, ["Tabla 7"], efecto_peso([2, 2.39], 17), "blue"],
    "Tabla 1": [[2.43, 1.24], 0, [], efecto_peso([2.4, 1.2], 10), "green"],
    "Tabla 2": [[2.35, 1.24], 0, [], efecto_peso([2.38, 1.2], 10), "green"],
    "Tabla 3": [[2.43, 2.04], 0, [], efecto_peso([2.4, 2], 10), "green"],
    "Tabla 4": [[2.35, 2.04], 0, [], efecto_peso([2.38, 2], 10), "green"],
    "Tabla 5": [[1.31, 2.04], 0, [], efecto_peso([1.61, 2], 10), "green"],
    "Tabla 6": [[1.39, 2.04], 0, [], efecto_peso([1.59, 2], 10), "green"],
    "Tabla 7": [[1.87, 2.35], 0, [], efecto_peso([2, 2.38], 10), "green"],
    "Tabla 8": [[2.35, 0.4], 0, [], efecto_peso([2.38, 0.4], 10), "green"],
    "Pilar pequeno": [[1.45, 1.67], 0, [], efecto_peso([1.63, 1.6], 1), "black"],
    "Pilar grande": [[2.31, 1.64], 0, [], efecto_peso([2.38, 1.6], 2), "black"]
}

DATA = datos_combos(OBJETOS, ANCHO, LARGO)

# Test efecto_peso:
#print("Ingrese x,y,w: ")
#datos = input().split(",")
#print(efecto_peso([float(datos[0]), float(datos[1])], float(datos[2])))
#input()

# Test combinaciones:
#combinations = combinaciones(OBJETOS)
#print(combinations)
#print(len(combinations))

# Test datos_combo:
#data = datos_combos(OBJETOS, ANCHO, LARGO)
#for ele in data:
#    print(ele)
#print(data[30])

