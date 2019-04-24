#--------------------------------------
#Hard-sphere event driven MD simulation
#
#Mass and diameter of the particles is 1
#--------------------------------------
import numpy as np
import random

TIMBIG = 1.e10

class Particle:
    def __init__(self, inipos, inivel, label):
        self.pos = inipos
        self.vel = inivel
        self.label = label
    def getPos(self):
        return self.pos
    def getVel(self):
        return self.vel
    def getLabel(self):
        return self.label
    def setPos(self,newpos):
        self.pos = newpos
    def setVel(self,newvel):
        self.vel = newvel
    def move(self,time):
        newposx = (self.getVel())[0]*time+(self.getPos())[0]
        newposy = (self.getVel())[1]*time+(self.getPos())[1]
        self.setPos([newposx,newposy])

def calc_time(part1, part2, sigma):
    Rij = [(part1.getPos())[0]-(part2.getPos())[0],(part1.getPos())[1]-(part2.getPos())[1]]
    Vij = [(part1.getVel())[0]-(part2.getVel())[0],(part1.getVel())[1]-(part2.getVel())[1]]
    RV = Rij[0]*Vij[0]+Rij[1]*Vij[1]
    V = (Vij[0]**2)+(Vij[1]**2)
    R = (Rij[0]**2)+(Rij[1]**2)
    det = (RV**2)-V*R+V*sigma**2
    if (det > 0):
        sqt = np.sqrt(det)
        a1 = (-1*RV+sqt)/V
        a2 = (-1*RV-sqt)/V
        return min(a1,a2)
    return TIMBIG

def times(part, Lx, Ly):
    sigma = 1. #diámetro de las partículas
    sigsq = sigma**2
    t = []      #tiempos de colisión
    partnr = [] #compañera de collision (negativo si es contra un muro)
    for i in part:
        t.append(TIMBIG)
        partnr.append(i.getLabel())

    for i in part[:len(part)-1]:
        for j in part[i.getLabel()+1:]:
            time = calc_time(i,j,sigma)
            if (t[i.getLabel()] > time):
                t[i.getLabel()] = time
                partnr[i.getLabel()] = j.getLabel()


    for i in part:
        Vx = i.getVel()[0]
        Vy = i.getVel()[1]
        Rx = i.getPos()[0]
        Ry = i.getPos()[1]
        if (Vx < 0):
            timex = (-1*Rx)/Vx
            wallx = -1
        elif (Vx > 0):
            timex = (Lx-Rx)/Vx
            wallx = -2
        else:
            timex = TIMBIG
            wallx = -5
        if (Vy < 0):
            timey = (-1*Ry)/Vy
            wally = -4
        elif (Vy > 0):
            timex = (Ly-Ry)/Vy
            wally = -3
        else:
            timey = TIMBIG
            wally = -5
        time = min(timex,timey)
        if (time == timex):
            wall = wallx
        else:
            wall = wally
        if (t[i.getLabel()] > time):
            t[i.getLabel()] = time
            partnr[i.getLabel()] = wall


    return (t, partnr)

def changeVel(part1, part2):
    #Cambia la velocidad de las partículas i y j
    # en caso que hayan colisionado
    sigma = 1.
    sigsq = sigma**2
    Rij = [(part1.getPos())[0]-(part2.getPos())[0],(part1.getPos())[1]-(part2.getPos())[1]]
    Vij = [(part1.getVel())[0]-(part2.getVel())[0],(part1.getVel())[1]-(part2.getVel())[1]]
    R = [Rij[0]/sigma,Rij[1]/sigma]
    esc = -1*(Vij[0]*R[0]+Vij[1]*R[1])
    D_V = [esc*R[0],esc*R[1]]
    part1.setVel([part1.getVel()[0]+D_V[0],part1.getVel()[1]+D_V[1]])
    part2.setVel([part2.getVel()[0]-D_V[0],part2.getVel()[1]-D_V[1]])

def main():
    #No. de partículas
    N = 2
    #Tamaño de la caja de simulación en X
    Lx = 10
    #Tamaño de la caja en simulación en Y
    Ly = 10
    #Numero de pasos de simulación
    steps = 20
    #Condiciones iniciales de las partículas (pos y vel)
    X = [0., 3., 2., 4.]
    Y = [0., 1., 0., 2.]
    VX = [0.5, 0.3, -0.2, 0]
    VY = [0, -0.5, 0.6, -0.1]

    #Initializar las partículas
    part = []
    for i in range(N):
        part.append(Particle([X[i], Y[i]], [VX[i], VY[i]],i))

    #Para guardar las trayectorias
    traject = []
    posit = []
    for i in range(N):
        r = part[i].getPos()
        posit.append(r[0])
        posit.append(r[1])
    traject.append(posit)


    #Ciclo principal de la simulación
    for n in range(steps):
        tim, partnr = times(part, Lx, Ly)

        #tiempo de la próxima colisión y compañeras de colisión
        nextt = TIMBIG #tiempo de la siguiente colisión
        p1 = 0 #índices de las partículas (o muro) implicadas
        p2 = 0
        for i in range(len(tim)):
            if tim[i] < nextt:
                nextt = tim[i]
                p1 = i
                p2 = partnr[i]

        for i in part:
            i.move(nextt)
            if (p1 == i.getLabel()):
                part1 = i
            if (p2 == i.getLabel()):
                part2 = i

        if (p2 >= 0):
            changeVel(part1,part2)
        else:
            if (p2 == -1 or p2 == -3):
                part1.setVel([-1*part1.getVel()[0],part1.getVel()[1]])
            elif (p2 == -2 or p2 == -4):
                part1.setVel([part1.getVel()[0],-1*part1.getVel()[1]])
        #Guardar las trayectorias
        posit = []
        for i in range(N):
            r = part[i].getPos()
            posit.append(r[0])
            posit.append(r[1])
        traject.append(posit)



    #imprimir trayectorias
    output = open("trajectory.dat","w")
    for n in range(len(traject)):
        for i in range(len(traject[n])):
            output.write("{0:.6f} ".format(traject[n][i]))
        output.write("\n")
    output.close()

##Ejecución...
main()
