import numpy as np
from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2

# Construya el analizador ( parser ) de
# argumentos y analice los argumentos
ap = argparse . ArgumentParser ()
# Camino ( path ) al archivo de video
ap.add_argument( "-v", "--video" )
# Tamaño mınimo y maximo de la región a considerar
ap.add_argument( "-a" , "--min-area", type=int, default=100)
ap.add_argument( "-b" , "--max-area", type=int, default=1000)
args = vars(ap.parse_args ())

# Si el argumento del video en None ,
# estamos reciviendo de la webcam
if args.get("video", None) is None:
    vs = VideoStream(src=0).start()
    time.sleep(2.0)
else :
    vs = cv2.VideoCapture (args["video"])

# Para guardar la trayectoria
Out = open("trajectory.dat","w")


#Determinar los límites para el color que se desea detectar
boundaries = ([80, 20, 20], [255, 70, 70]) #B, G, R
lower = np.array(boundaries[0], dtype = "uint8")
upper = np.array(boundaries[1], dtype = "uint8")


# Ciclo sobre los frames del video
frameNo = 0
while True :
    # Tomar el siguiente frame del video
    frame = vs.read()
    frame = frame if args.get("video", None) is None else frame[1]
    
    # Si no hay mas frames ...
    if frame is None :
        frameNo += 1
        break
    # Ajustar tamaño del frame
    frame = imutils.resize(frame, width =500)

    # Encontrar las regiones con color dentro de los límites lower y upper
    # y aplicar una máscara
    mask = cv2.inRange(frame, lower, upper)
    output = cv2.bitwise_and(frame, frame, mask = mask)
    
    # Convertir a escala de grises para medir intensidad
    gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY )
    # Promediar sobre un area 21 x21 para suavisar imagen
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    
    # Umbral
    thresh = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations =2)

    # Definir los contornos
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # Ciclo sobre los contornos
    for c in cnts:
        # Filtrar las regiones muy pequeñas o muy grandes
        if cv2.contourArea(c) < args["min_area"] and cv2.contourArea(c) < args["max_area"]:
            continue

        # Calcular la caja que enmarca el contorno
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
        
        # Calcular el centro del marco
        dcolor = [255 ,0 ,0]
        cordx = x + int(w/2)
        cordy = y + int(h/2)
        # Imprimimos la trayectoria
        Out.write("{0} {1} {2}\n".format(frameNo,cordx,cordy))
        
        for i in range (cordx-5, cordx+5):
            for j in range(cordy-5, cordy+5):
                if j < frame.shape[0] and i < frame.shape[1]:
                    frame[j, i] = dcolor
        

    # Mostrar el frame
    cv2.imshow("Security Feed", frame)
    # Detenemos el video si se oprime la letra q
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    
    frameNo += 1
    # Para ajustar la velocidad del video
    time.sleep(0.100)
        

        
# Parar los procesos y cerrar las ventanas
Out.close()
vs.stop() if args.get("video", None) is None else vs.release()
cv2.destroyAllWindows()
