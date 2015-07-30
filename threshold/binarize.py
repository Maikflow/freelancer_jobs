import cv2
import numpy as np
import wave
import os
import threading
import subprocess
from time import sleep,time

def binarize_image(src):
    """
    Recibe una imagen (como matriz), y le aplica 
    el metodo del umbral (la transforma en una imagen en blanco y negro)
    """

    #Convertimos la imagen a escala de grises
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

    #Aplicamos el metodo del umbral, primero para obtener el umbral promedio
    (thresh, threshed_image) = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    #Aplicamos el metodo ahora con el umbral promedio para obtener mejores resultados
    (thresh, threshed_image) = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    #threshed_image = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    #Mostramos la imagen 
    cv2.imshow('preview',threshed_image)
    cv2.waitKey(2)

    #la guardamos en el actual directorio como 'muestra.jpg'
    cv2.imwrite('muestra.jpg',threshed_image) 
    check_contours(threshed_image, src)

def check_contours(threshed_image, img):
    """
    Dada alguna imagen y su umbral, traza el contorno de los objetos
    (en este caso la mano) y sus puntos caracteristicos
    """

    #Obtenemos el contorno de la imagen img
    x, contours,hierarchy = cv2.findContours(threshed_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #Creamos una base para dibujar el contorno y demas puntos importantes
    #como las yemas de los dedos y el punto mas bajo entre dedos
    drawing = np.zeros(img.shape,np.uint8)
    max_area=0

    #Calculamos el area de todos los objetos vistos en la imagen
    #para quedarnos con el objeto mas grande
    for i in range(len(contours)):
        cnt=contours[i] 
        area = cv2.contourArea(cnt)
        if(area>max_area):
            max_area=area
            ci=i

    cnt = contours[ci]
    #Obtenemos los puntos convexos (el punto mas bajo entre los dedos
    hull = cv2.convexHull(cnt)
    moments = cv2.moments(cnt)

    #Si el area es diferente de cero, entramos y trazamos el contorno y demas
    #puntos sobre la imagen
    if moments['m00']!=0:
        cx = int(moments['m10']/moments['m00']) # cx = M10/M00
        cy = int(moments['m01']/moments['m00']) # cy = M01/M00
        centr=(cx,cy)
        cv2.circle(img,centr,5,[0,0,255],2)
        cv2.drawContours(drawing,[cnt],0,(0,255,0),2)
        cv2.drawContours(drawing,[hull],0,(0,0,255),2)
        cnt = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
        hull = cv2.convexHull(cnt,returnPoints = False)
        if(1):

            #Estos son los puntos entre dedos, aqui llamados defectos
            defects = cv2.convexityDefects(cnt,hull)
            #print 'center', centr
            mind = 0
            maxd = 0
            song = 0
            for i in range(defects.shape[0]):
                s,e,f,d = defects[i,0]
                start = tuple(cnt[s][0])
                end = tuple(cnt[e][0])
                far = tuple(cnt[f][0])
                print far, centr
                print 'i: ',i,'depth: ', d
                dist = cv2.pointPolygonTest(cnt,centr,True)
                cv2.line(img,start,end,[0,255,0],2)
                cv2.circle(img,far,5,[0,0,255],-1)
                if far[1] <= centr[1]: song+=1
                print 'cancion', song

            #Mostramos las imagenes trazadas
            cv2.imshow('output',drawing)
            cv2.imshow('input',img)
            cv2.waitKey(2)
            choose_song(song)


def detect_motion(t0, t1, t2):
    """
    Calcula la diferencia absoluta entre dos pares de imagenes y
    retorna la matriz resultante
    """
    d1 = cv2.absdiff(t2, t1)
    d2 = cv2.absdiff(t1, t0)
    return cv2.bitwise_and(d1, d2)

def choose_song(value):
    """
    Elige la cancion de acuerdo al gesto obtenido en la imagen
    """
    if value == 0:
        if os.name == 'nt':
            os.startfile('Juanes.wav')
        elif os.name == 'posix':
            subprocess.call(('xdg-open', 'Juanes.wav'))
    elif value == 1:
        if os.name == 'nt':
            os.startfile('Aterciopelados.wav')
        elif os.name == 'posix':
            subprocess.call(('xdg-open','Aterciopelados.wav'))
    elif value == 2:
        if os.name == 'nt':
            os.startfile('CHOCQUIBTOWN.wav')
        elif os.name == 'posix':
            subprocess.call(('xdg-open', 'CHOCQUIBTOWN.wav'))
    sleep(2)

def get_webcam():
    """
    Activa la camara y toma una foto al detectar movimiento 
    en la imagen actual
    """

    #Inicializamos la camara
    vc = cv2.VideoCapture(0)
    reloj = int(time())

    #Validamos si la camara se inicializo con exito:
    if vc.isOpened(): 
        #si no hubo error al iniciar, comienza a leer imagenes de la camara
        rval, frame = vc.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        (thresh, threshed_image) = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

        #Aqui declaramos tres imagenes de referencia
        t_minus = cv2.cvtColor(vc.read()[1], cv2.COLOR_RGB2GRAY)
        t = cv2.cvtColor(vc.read()[1], cv2.COLOR_RGB2GRAY)
        t_plus = cv2.cvtColor(vc.read()[1], cv2.COLOR_RGB2GRAY)
        #Suavizamos la imagen del movimiento y calculamos el promedio 
        #del color de los pixeles
        mean = cv2.GaussianBlur(detect_motion(t_minus, t, t_plus), (5, 5), 0).mean()
    else:
        print "No se encontro una camara web funcional"
        rval = False


    #Mientras la camara este activa:
    while rval:
        t2 = reloj+4
        gray = cv2.cvtColor(vc.read()[1], cv2.COLOR_BGR2GRAY)
        (thresh, threshed_image) = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
        (thresh, threshed_image) = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

        img = detect_motion(t_minus, t, t_plus)
       # img = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        img = cv2.GaussianBlur(img, (5, 5), 0)

        #Mostrar lo que se esta observando
        cv2.imshow("preview", threshed_image)

        #Si en la matriz se observa movimiento, entonces el valor promedio de los pixeles
        #sera mayor al valor promedio del color en los pixeles en la base
        if img.mean()>mean:

            #Pasamos a obtener el umbral de la imagen actual
            if int(time()) >= (t2):  
                binarize_image(vc.read()[1])
                reloj = int(time())

            #Retomamos las imagenes de referencia del movimiento
            t_minus = cv2.cvtColor(vc.read()[1], cv2.COLOR_RGB2GRAY)
            t = cv2.cvtColor(vc.read()[1], cv2.COLOR_RGB2GRAY)
            t_plus = cv2.cvtColor(vc.read()[1], cv2.COLOR_RGB2GRAY)
        else:
            t_minus = t
            t = t_plus
            t_plus = cv2.cvtColor(vc.read()[1], cv2.COLOR_RGB2GRAY)

        rval, frame = vc.read()
        key = cv2.waitKey(20)

        #Podemos salir de nuestro ciclo presionando cualquier tecla
        if key != -1:
            break
    cv2.destroyWindow("preview")

if __name__ == "__main__":
    get_webcam()
