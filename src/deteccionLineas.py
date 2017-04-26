from PIL import Image
import sys 
import math
from math import sqrt,fabs,sin,cos,floor,atan, ceil
import numpy as np
import Tkinter
import tkFileDialog

def escalaDeGrises(im):
    imGris = im.copy()
    w,h = imGris.size
    pixeles = imGris.load()

    for x in range(w):
        for y in range(h):
            promedio = sum(pixeles[x,y])/3
            pixeles[x,y] = (promedio, promedio,promedio)
    imGris.save('grises.png')
    return imGris
    
def difuminar(im):
    pixeles = im.load()
    w,h = im.size
    imDif = Image.new('RGB',(w,h))
    difPix = imDif.load()

    for x in range(w):
        for y in range(h):
            pix = []
            pix.append(list(pixeles[x,y]))

            if x > 0:
                pix.append(list(pixeles[x-1, y]))
            if y > 0:
                pix.append(list(pixeles[x, y-1]))
            if x < w-1:
                pix.append(list(pixeles[x+1, y]))
            if y < h-1:
                pix.append(list(pixeles[x, y+1]))
            
            filtro = [sum(i) for i in zip(*pix)]
            total = len(pix)
            difPix[x,y] = filtro[0]/total, filtro[1]/total, filtro[2]/total
    imDif.save('difuminada.png')
    return imDif

def binarizar(im):
    imBinaria = im.copy()
    w,h = im.size
    pixeles = imBinaria.load()

    for x in range(w):
        for y in range(h):
            if pixeles[x,y][0] >= 30:
                    pixeles[x,y] = (255,255,255)
            else:
                    pixeles[x,y] = (0,0,0)
    imBinaria.save('binaria.png')
    return imBinaria

def convolucion(im, g):
  w, h = im.size
  pix = im.load()
  out_im = Image.new("RGB", (w, h))
  out = out_im.load()
  for i in xrange(w):
    for j in xrange(h):
      suma = 0
      for n in xrange(i-1, i+2):
        for m in xrange(j-1, j+2):
            if n >= 0 and m >= 0 and n < w and m < h:
              suma += g[n - (i - 1)][ m - (j - 1)] * pix[n, m][1]
      out[i, j] = suma, suma, suma
  out_im.save("output.png", "png")
  return out_im

def euclides(gx,gy):
    w, h = gx.size
    g = Image.new('RGB', (w,h))
    pixeles = g.load()
    dx = gx.load()
    dy = gy.load()
    for x in range(w):
        for y in range(h):
            c = int(sqrt( (dx[x,y][0])**2 + (dy[x,y][0])**2 ))
            pixeles[x,y] = (c,c,c)
    return g

def normalizar(im):
    w,h = im.size
    imNorm = im.copy()
    pixeles = imNorm.load()
    maximo = 0
    minimo = 0
    for x in range(w):
        for y in range(h):
            if pixeles[x,y] > maximo:
                maximo = pixeles[x,y][0]
            if pixeles[x,y] < minimo:
                minimo = pixeles[x,y][0]
    prop = 256.0/(maximo - minimo)
    for x in range(w):
        for y in range(h):
            n = int(floor((pixeles[x,y][0] - minimo)* prop))
            pixeles[x,y] = (n,n,n)
    imNorm.save('normalizada.png')
    return imNorm


def frecuentes(histo, cantidad):
    frec = list()
    for valor in histo:
        if valor is None:
            continue
        frecuencia = histo[valor]
        acepta = False
        if len(frec) <= cantidad:
            acepta = True
        if not acepta:
            for (v, f) in frec:
                if frecuencia > f:
                    acepta = True
                    break
        if acepta:
            frec.append((valor, frecuencia))
            frec = sorted(frec, key = lambda tupla: tupla[1])
            if len(frec) > cantidad:
                frec.pop(0)
    incluidos = list()
    for (valor, frecuencia) in frec:
        incluidos.append(valor)
        #print frecuencia
    return incluidos
def sort_dictionary(d):
  return sorted(d.items(), key=lambda x: x[1], reverse = True)

def deteccionDeLineas(im,u):
    maskx = [[-1, -1, -1], [2, 2, 2], [-1, -1, -1]]
    masky = [[-1, 2, -1], [-1, 2, -1], [-1, 2, -1]]
    gradx = convolucion(im, maskx)
    grady = convolucion(im, masky)
    gx = gradx.load()
    gy = grady.load()
    matriz = []
    comb = {}
    ang = []
    x, y = im.size
    for i in range(x):
        lista = []
        for j in range(y):
            gx = gradx.getpixel((i,j))[0]					#Se cargan las mascaras
            gy = grady.getpixel((i,j))[0]
            theta = 0.0								#Las condiciones deben de cumplirse
            if abs(gx) + abs(gy) <= 0.0:					#al no ser asi, theta sigue siendo 0
                theta = None
            elif gx == 0 and gy == 255:
                theta = 90
            if theta is not None:
                rho = abs((i) * math.cos(theta) + (j) * math.sin(theta))	#Se calcula RHO para cada pixel con un theta diferente
                if not theta in ang:  						#de None
                    ang.append(theta)
                if i > 0 and i < x-1 and j > 0 and j < y - 1: 			#Cada vez que hay un par roh, theta igual, se aumenta 1
                    if (rho, theta) in comb:					#el valor del diccionario, cada valor identico pertenece a 
                        comb[(rho, theta)] += 1					#una linea ya sea horizontal o vertical
                    else:
                        comb[(rho, theta)] = 1
                lista.append((rho, theta))
            else:
                lista.append((None, None))
        matriz.append(lista)
    comb = sorted(comb.items(), key=lambda k: k[1], reverse = True)
    frec = {}
    n = int(math.ceil(len(comb) * u))
    for i in range(n):								#Se ordena el diccionario y se crea un histograma de 
        (rho, theta) = comb[i][0]						#frecuencias
        frec[(rho, theta)] = comb[1]
    for i in range(x):
        for j in range(y):							#Se pintan los pixeles en base al vaor del diccionario
            if i > 0 and j > 0 and i < x and j < y:
                rho, theta = matriz[i][j]
                if (rho, theta) in frec:
                    if theta == 0:
                        im.putpixel((i,j),(255,0,0))
                    elif theta == 90:
                        im.putpixel((i,j),(0,255,0))
    im.save("output.jpg","jpg")

if __name__=="__main__":
    Tkinter.Tk().withdraw() 
    ruta = tkFileDialog.askopenfilename(filetypes=(("Archivos JPG", "*.jpg"),
											("Archivos JPEG", "*.jpeg"),
											("Archivos PNG", "*.png"),
                                            ("Todo los archivos", "*.*")))     
    im = Image.open(ruta)
    gris = escalaDeGrises(im)
    dif = difuminar(gris)
    binaria = normalizar(binarizar(dif))
    lineas = deteccionDeLineas(binaria,10)