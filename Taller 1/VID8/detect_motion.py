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
# Tamaño mınimo de la región a considerar
# como movimiento
ap.add_argument( "-a" , "--min-area", type=int, default=5000)
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
    
# Para guardar el primer frame
firstFrame = None
# Ciclo sobre los frames del video
frameNo = 0
while True :
    # Tomar el siguiente frame del video
    frame = vs . read ()
    frame = frame if args.get("video", None) is None else frame[1]
    text = " No moving bodies detected "
    # Si no hay mas frames ...
    if frame is None :
        break
    # Ajustar tamaño del frame y convertir a
    # escala de grises
    frame = imutils.resize(frame, width =500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY )
    # Promediar sobre un area 21 x21 para suavisar imagen
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # Guardar el primer frame como referencia
    if firstFrame is None :
        firstFrame = gray
        frameNo += 1
        continue

    # Calcula valor absoluto de la diferencia
    # con el frame inicial
    frameDelta = cv2.absdiff(firstFrame, gray)
    # Usa una mascara para definir claramente
    # las regiones que han cambiado
    thresh = cv2.threshold (frameDelta, 50, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations =2)

    # Definir los contornos
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # Ciclo sobre los contornos
    for c in cnts:
        # Filtrar las regiones pequeñas
        if cv2.contourArea(c) < args["min_area"]:
            continue

        # Calcular la caja que enmarca el contorno
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
        text = "Moving bodies detected"
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
            
        # Escribimos el estado del cuarto
        cv2.putText (frame, "{}".format(text),
                        (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 0, 255), 2)

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
