# Importación de biblotecas:
# Descargar bibliotecas serial y matplotlib.

#import serial
from multiprocessing import Process, Queue
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import datetime as dt
from random import randrange
import numpy as np
import time 

#import cv2
#import depthai as dai
import os

# Importar parámetros:
from parametros import LARGO, ANCHO, DISTANCIA, D_PESO, OBJETOS, DATA
from parametros import centro_masa

# escritura_total es una función auxiliar de recepcion_datos()
# que se encarga de escribir la info de los pesos en el archivo principal:

def escritura_total(lista_pesos):
    # Se abre el archivo correspondiente:
    archivo = open("info_pesos.txt", "a+")

    # Se obtiene el valor de la fecha y hora actual:
    hora = dt.datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    # Se escribe el valor de peso total:
    archivo.write(f"{hora} => {lista_pesos[0]}\t{lista_pesos[1]}\t{lista_pesos[2]}\t{lista_pesos[3]}\t{sum(lista_pesos)}\n")
    archivo.close()

def obtencion_peso(decoded_message):
    try:
        # Si el valor es negativo o 0, se asume 0:
        if int(decoded_message[21:]) <= 0:
            return 0

        # Si el valor es positivo, se añade el valor:
        else:
            return int(decoded_message[21:])

    # Si ocurre algún error con la información recepcionada, se asume peso 0:
    except ValueError as error:
        return 0

    # Se retorna el valor de peso medido:
    return peso

# recepcion_datos() recepciona la info del puerto Serial de Arduino
# y la guarda en los archivos correspondientes con escritura_total():

def recepcion_datos():

    # Conexión al Serial. Ojo con el baudrate y el puerto.
    arduino = serial.Serial('COM4', 115200, timeout=0.1)
    lista_pesos = []

    while True:

        # Se obtiene la información del Serial.
        decoded_message = arduino.readline().decode('utf-8').rstrip()
        print(decoded_message)

        # Se verifica que haya info:
        if len(decoded_message)>1:

            # Segundo if revisa de qué celda es la info2
            if decoded_message[10] in ["1", "2", "3"]:
                lista_pesos.append(obtencion_peso(decoded_message))
                
            elif decoded_message[10] == "4" and len(lista_pesos) == 3:
                lista_pesos.append(obtencion_peso(decoded_message))
                escritura_total(lista_pesos)
                lista_pesos = []
            
            else:
                lista_pesos = []
                print("Load cell data lost")

def recepcion_datos_fake():
    """Simulates data input from load cells without needing Arduino."""
    while True:
        pesos = [randrange(10, 100) for _ in range(4)]
        total = sum(pesos)
        hora = dt.datetime.now().strftime("%Y/%m/%d %H:%M:%S")

        with open("info_pesos.txt", "a+") as archivo:
            archivo.write(f"{hora} => {pesos[0]}\t{pesos[1]}\t{pesos[2]}\t{pesos[3]}\t{total}\n")

        time.sleep(1)

def chequeo(cm, pt, pabcd, data=DATA, distancia=DISTANCIA, d_peso=D_PESO):
    #print(cm, pt, pabcd)
    best_i = None
    best = 100
    for i in range(len(data)):
        pt_i = data[i][0]
        if abs(pt_i - pt)<= d_peso:
            pabcd_i = data[i][1]
            if abs(pabcd_i[0] - pabcd[0]) <= d_peso and \
               abs(pabcd_i[1] - pabcd[1]) <= d_peso and \
               abs(pabcd_i[2] - pabcd[2]) <= d_peso and \
               abs(pabcd_i[3] - pabcd[3]) <= d_peso:
                cm_i = data[i][2]
                dist = np.sqrt((cm[0] - cm_i[0])**2 + (cm[1] - cm_i[1])**2)
                if dist <= distancia:
                    #print(cm_i, pt_i, pabcd_i)
                    score = dist + \
                            1.5 * abs(pt_i - pt) / (pt_i + 0.001) + \
                            1.5 * abs(pabcd_i[0] - pabcd[0]) / (pabcd_i[0] + 0.001) + \
                            1.5 * abs(pabcd_i[1] - pabcd[1]) / (pabcd_i[1] + 0.001) + \
                            1.5 * abs(pabcd_i[2] - pabcd[2]) / (pabcd_i[2] + 0.001) + \
                            1.5 * abs(pabcd_i[3] - pabcd[3]) / (pabcd_i[3] + 0.001)
                            
                    if score < best:
                        best_i = i
                        best = score
        elif pt_i > pt + d_peso:
            break
    if best_i != None:
        return data[best_i][2], data[best_i][3]
    else:
        return None, None

def grafico_celda(num):
    fig = plt.figure(figsize=(8, 8))
    ax1 = fig.add_subplot(1, 1, 1)
    x = []
    y = []

    def update_grafico_celda(frame, x, y, num):
        f = open("info_pesos.txt", "r").read().split('\n')
        lineas = f[:-1]
        x.append(dt.datetime.now().strftime('%H:%M:%S'))
        peso = lineas[-1].split("=> ")[1].split("\t")[num - 1]
        y.append(peso)
        if len(x) > 7:
            x = x[1:]
            y = y[1:]
        ax1.clear()
        ax1.plot(x, y)
        plt.title("Peso celda " + str(num))
        plt.xlabel("Tiempo")
        plt.ylabel("Peso")
        plt.tight_layout()

    animations = animation.FuncAnimation(fig, update_grafico_celda, fargs=(x, y, num,), interval=1000, cache_frame_data=False)
    plt.show()

def grafico_tot():
    fig = plt.figure(figsize=(8, 8))
    ax1 = fig.add_subplot(1,1,1)
    ax1.set_ylim(bottom=0,top=150, auto=False)
    x = []
    y = []
    
    def update(i,x,y):
        f = open("info_pesos.txt","r").read().split("\n")
        lineas = f[:-1]
        peso = lineas[-1].split("=> ")[1].split("\t")[-1]
                
        x.append(dt.datetime.now().strftime('%H:%M:%S'))
        y.append(peso)
        if len(x)>7:
            x = x[-100:]
            y = y[-100:]
        ax1.clear()
        ax1.plot(x,y)
        plt.title('Peso Total')
        plt.xlabel('Tiempo')
        plt.ylabel('Peso')
        plt.tight_layout()
    
    animations = animation.FuncAnimation(fig, update, fargs=(x,y), interval=1000, cache_frame_data=False)
    plt.show()
    
def coordenada(data=DATA, objetos=OBJETOS, distancia=DISTANCIA, d_peso=D_PESO, ancho=ANCHO, largo=LARGO):

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(0, ancho)
    ax.set_ylim(0, largo)
    ax.set_title("Ubicación")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")

    x = [0, 0]
    y = [0, 0]
    sizes = [10, 10]
    colors = [1, 100]
    sc = ax.scatter(x, y, s=sizes, c=colors, cmap="viridis", alpha=0.7)

    def update(frames, x, y):
        
        # Para visualizar las conexiones que se deben hacer para que
        # funcionen las ecuaciones, se presenta el siguiente diagrama:
        #---ancho
        #l-------
        #a--a---b
        #r-------
        #g--c---d
        #o-------
        archivo = open(f"info_pesos.txt", "r").read().split("\n")
        lineas = archivo[:-1]
        lista_pesos = lineas[-1].split("=> ")[1].split("\t")
        lista_pesos[0] = int(lista_pesos[0])
        lista_pesos[1] = int(lista_pesos[1])
        lista_pesos[2] = int(lista_pesos[2])
        lista_pesos[3] = int(lista_pesos[3])
        lista_pesos.pop(4)
        cm = centro_masa(lista_pesos, sum(lista_pesos), ancho, largo)
        cm_i, llaves = chequeo(cm, sum(lista_pesos), lista_pesos)
        

        plt.axis([0, ancho, 0, largo])
        plt.title("Ubicacion")
        plt.xlabel("X")
        plt.ylabel("Y")

        x = []
        y = []
        sizes = []
        colors = []
        if llaves != None:
            for llave in llaves:
                datos = objetos[llave]
                x.append(datos[0][0])
                y.append(datos[0][1])
                sizes.append(20)
                colors.append(1)
            x.append(cm_i[0])
            y.append(cm_i[1])
            sizes.append(20)
            colors.append(100)
        x.append(cm[0])
        y.append(cm[1])
        sizes.append(40)
        colors.append(50)

        sc.set_offsets(np.c_[x, y])
        sc.set_sizes(sizes)
        sc.set_array(colors)
        return sc,

    # Displaying plot
    animations = animation.FuncAnimation(fig, update, fargs=(x, y), interval=500, cache_frame_data=False)
    plt.show()

def camara():
    #### PARAMS
    video_size = (500, 500)
    folder = "video_frames"

    # Create pipeline
    pipeline = dai.Pipeline()

    # Define source and output
    # Nodo de entrada
    camRgb = pipeline.create(dai.node.ColorCamera)
    # Nodo de salida
    xoutRgb = pipeline.create(dai.node.XLinkOut)
    xoutRgb.setStreamName("rgb")

    # Properties
    # Qué camara usar
    camRgb.setPreviewSize(video_size[0], video_size[1])
    camRgb.setInterleaved(False)
    camRgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)
    
    # Linking
    camRgb.preview.link(xoutRgb.input)

    # Define the folder to save the images
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Connect to device and start pipeline
    with dai.Device(pipeline) as device:
        qRgb = device.getOutputQueue(name="rgb", maxSize=4, blocking=False)
        while True:
            inRgb = qRgb.get()  # blocking call, will wait until new data has arrived
            frame = inRgb.getCvFrame()
            frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

            # Get current timestamp
            timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")

            # Save the frame as an image with the timestamp as filename
            filename = os.path.join(folder, f"{timestamp}.png")
            cv2.imwrite(filename, frame)
            #print(f"Saved {filename}")

            # Visualizing the frame
            cv2.imshow("rgb", frame)
            if cv2.waitKey(1) == ord('q'):
                break

    # Release everything when job is finished
    cv2.destroyAllWindows()

### Inicialización del programa:

if __name__== '__main__':

    # Obtención de fecha y hora actual para sobreescribir los archivos:
    hora = dt.datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    # Sobreescritura de los archivos anteriores:
    archivo = open("info_pesos.txt", "w+")
    archivo.write(f"{hora} => 0\t0\t0\t0\t0\n")
    archivo.close()
    
    ### Instanciación de procesos:

    # Proceso encargado de obtener la informacion desde el Arduino:
    datos = Process(target=recepcion_datos_fake)

    # Procesos encargados de graficar los pesos vistos en cada celda:
    celda_1 = Process(target=grafico_celda, args=(1,))
    celda_2 = Process(target=grafico_celda, args=(2,))
    celda_3 = Process(target=grafico_celda, args=(3,))
    celda_4 = Process(target=grafico_celda, args=(4,))

    # Proceso encargado de graficar la coordenada del peso total promedio:
    pos = Process(target=coordenada)

    # Procesos encargado de graficar el peso total:
    total = Process(target=grafico_tot)

    cam = Process(target=camara)

    ### Inicialización de los procesos:

    datos.start()
    #celda_1.start()
    #celda_2.start()
    #celda_3.start()
    #celda_4.start()
    #total.start()
    pos.start()
    #cam.start()

    ### 

    datos.join()
    #celda_1.join()
    #celda_2.join()
    #celda_3.join()
    #celda_4.join()
    #total.join()
    pos.join()
    #cam.join()
