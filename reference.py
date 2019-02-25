import argparse
import imutils
import cv2


def onmouse(event, x, y, flags, param):
    global position
    if event == cv2.EVENT_LBUTTONDOWN:
        position = x, y
        print(position)


# Construya el analizador ( parser ) de
# argumentos y analice los argumentos
ap = argparse.ArgumentParser()
# Camino ( path ) al archivo de video
ap.add_argument("-v", "--video" )
args = vars(ap.parse_args())

# Cargar el primer frame el video
vs = cv2.VideoCapture(args["video"])
frame = vs.read()
frame = frame if args.get("video", None) is None else frame[1]
frame = imutils.resize(frame, width=500)

cv2.imshow("image", frame)

#Mostrar la posición en donde se hace click
cv2.setMouseCallback("image", onmouse)

cv2.waitKey(0)
