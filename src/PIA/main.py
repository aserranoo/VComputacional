#PIA Deteccion de rugosidad de la corteza de un arbol
#Materia: Vision Computacional

import cv2
import Tkinter 
import tkFileDialog
import numpy as np
from matplotlib import pyplot as plt


def Rugosidad():
    images = []
    for item in Org_img:        
        blur = cv2.medianBlur(item,5)
        ret, otsu = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        images = [blur, otsu]
    return images  
#Inicia programa
print "\n[---- Rugosidad Arbol ----] \n\n (i) - Vamos a procesar una imagen primero escoje un archivo de imagen valido "

#Seleccion de imagen
Tkinter.Tk().withdraw()
ruta = tkFileDialog.askopenfilenames(filetypes=(("Archivos JPG", "*.jpg"),
											("Archivos JPEG", "*.jpeg"),
											("Archivos PNG", "*.png"),
                                            ("Todo los archivos", "*.*")))
#Se lee la imagen
try:
    Org_img = []
    count = 0    
    for item in ruta:
        Org_img.append(cv2.imread(item, 0))
    try:
        bordes = 0
        rug = 0
        total = 0
        images = Rugosidad()                            
        titles = ['Filtro Mediana','Histograma',"Umbral Otsu"]
        
        edges = cv2.Canny(images[1],600,50)
        prop = edges.shape
        height = prop[0]
        width = prop[1]
        for y in range(height):
            total +=  1
            for x in range(width):
                total +=  1
                if edges[y,x] > 0:                    
                    bordes += 1             
        rug =  total/bordes
        plt.subplot(2,4,1),plt.imshow(images[0],cmap = 'gray')
        plt.title('Imagen Original'), plt.xticks([]), plt.yticks([])        
        plt.subplot(2,4,2), plt.hist(images[0].ravel(),256)
        plt.title('Histogramas'), plt.xticks([], plt.yticks([]))
        plt.subplot(2,4,3),plt.imshow(edges,cmap = 'gray')
        plt.title('Bordes'), plt.xticks([]), plt.yticks([])
        plt.subplot(2,4,4),plt.imshow(images[1],cmap = 'gray')
        plt.title('Umbral'), plt.xticks([]), plt.yticks([])              
        plt.subplot(2,4,5), plt.axis('off')
        plt.title('Rugosidad = ' + str(100-rug) + '\n'), plt.xticks([]), plt.yticks([]), plt.axis('off')   
        plt.show()        
    except Exception as e:
        print e
        print("\n\n(X) - Esa opcion no es valida")

except:
	print "\n\n(X) - NO SELECCIONASTE UN ARCHIVO VALIDO!\a"
	print "\n\n 	 Saliendo del programa...\a"

cv2.waitKey(0)
cv2.destroyAllWindows()

