import numpy
import matplotlib.pyplot as plt

In = open("trajectory.dat")
lista = []

for line in In:
    V = list(map(int, line.split()))
    lista.append(V)

m_max = lista[len(lista)-1][2]
t_max = lista[0][0]

ext = []
con = input("Enter the convertion parameter\n> ")
con = float(con)

fps = 24.0

for listo in lista:
	if(True):
	    tmp = [0, listo[1], 0]
	    var = listo[2]
	    var = (m_max-var)/con
	    tmp[2] = var
	    var = listo[0]
	    var = (var-t_max)/fps
	    tmp[0] = var
	    ext.append(tmp)
In.close()

Out = open("trajm.dat", "w")
for listo in ext[0:6]:
    #if (listo[0] < 0.4):
    Out.write("{0} {1} {2}\n".format(listo[0], listo[1], listo[2]))
Out.close()

deto = open("trajm.dat", "r")
list_t = []
list_m = []
for line in deto:
    Vam = list(map(float, line.split()))
    list_t.append(Vam[0])
    list_m.append(Vam[2])

fit = numpy.polyfit(list_t, list_m, 2)

print ("g = {}".format(-2*fit[0]))
plt.plot(list_t, list_m, linestyle="", marker="o")

list_m2 = []
for i in list_t:
        list_m2.append((fit[0]*i*i)+(fit[1]*i)+fit[2])
plt.plot(list_t, list_m2)
plt.show()

deto.close()


