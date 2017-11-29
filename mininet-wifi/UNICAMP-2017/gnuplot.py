#!/usr/bin/env python

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import glob

#Caminho dos arquivos de Path a serem lidos
myPath="./"
#Contador da quantidade de arquivos de Path
pttPathCounter = len(glob.glob1(myPath,"data.txt"))
#Armazena em Array o nome dos arquivos de Path
files=glob.glob1(myPath,"data.txt")

f2 = open(myPath+'data.txt', 'r')
newlines = f2.readlines()
f2.close()

# initialize some variable to be lists:
rss = []
dist = []
bw = []

# scan the rows of the file stored in lines, and put the values into some variables:
for newline in newlines:
    p = newline.split()
    rss.append(float(p[0]))
    dist.append(float(p[1]))
    bw.append(float(p[2]))

fig, ax1 = plt.subplots()
ax2 = ax1.twinx()

ax1.plot(dist, rss, color='green', marker='+', markevery=1, linewidth=2, label="Sinal")
ax2.plot(dist, bw, color='black', marker='.', markevery=1, linewidth=2, label="Largura de Banda")

ax1.set_ylabel("Sinal (dBm)")
ax1.set_xlabel("Distancia (m)")
ax2.set_ylabel("Largura de Banda (Mbps)")

ax2.legend(loc=1, borderaxespad=0.)
ax1.legend(loc=2, borderaxespad=0.)

#plt.ylim([-10,100])
plt.margins(0.02, 0.0)
plt.savefig("graph1.eps")
plt.clf()
