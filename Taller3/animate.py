import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

colors = ['k','r','b','g','c','y','m']

N = 2

Lx = 10
Ly = 10


infile = open("trajectory.dat","r")
xd, yd = [], []
for n in range(N):
    xd.append([])
    yd.append([])

for line in infile:
    v = list(map(float, line.split()))
    for n in range(N):
        xd[n].append(v[2*n])
        yd[n].append(v[2*n+1])
infile.close()

#print(xd)
fig, ax = plt.subplots()

xdata, ydata = [], []
for n in range(N):
    xdata.append([])
    ydata.append([])

lnt = []
for n in range(N):
    ln, = plt.plot([], [], 'ro', linestyle='-',color=colors[n])
    lnt.append(ln)

def init():
    ax.set_xlim(-Lx/2, Lx/2)
    ax.set_ylim(-Ly/2, Ly/2)
    return lnt[0],

def updateAll(frame):
    for n in range(N):
        xdata[n].append(xd[n][frame])
        ydata[n].append(yd[n][frame])
        lnt[n].set_data(xdata[n], ydata[n])

    lntot = ()
    for n in range(N):
        lntot += lnt[n],
    return lntot


ani = FuncAnimation(fig, updateAll, frames=range(len(xd[0])), repeat=False,
                    init_func=init, blit=True)



plt.show()
