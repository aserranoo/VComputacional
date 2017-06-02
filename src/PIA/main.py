#PIA Deteccion de rugosidad de la corteza de un arbol
#Materia: Vision Computacional

import cv2
import Tkinter 
import tkFileDialog
import numpy as np
from matplotlib import pyplot as plt


def Rugosidad():
    images = []  
    # gray = []  
    for item in Org_img:
        # gray = cv2.cvtColor(item, cv2.COLOR_BGR2GRAY)
        blur = cv2.medianBlur(item,1)
        # blur = cv2.GaussianBlur(item,(5,5),.1)
        ret, otsu = cv2.threshold(blur,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
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
        Org_img.append(cv2.imread(item,0))
    try:
        bordes = 0
        bordes2 = 0
        rug = 0
        rug2= 0
        total = 0
        images = Rugosidad()
        titles = ['Filtro Mediana','Histograma',"Umbral Otsu"]        
        edges = cv2.Canny(images[1],10,200)
        prop = images[1].shape
        height = prop[0]
        width = prop[1]
        for y in range(height):            
            for x in range(width):
                total +=  1
                if images[1][y,x] > 0:
                    bordes += 1
                if images[1][y,x] == 0:
                    bordes2 += 1
        rug = round((bordes * 100) / total)
        rug2 = round((bordes2 * 100) / total)
        print rug
        print rug2
        rugosidadfinal = rug
        tiporugosidad =  " "
        if rugosidadfinal < 30:
          	tiporugosidad = 'NO es una imagen rugosa'
        else:
            tiporugosidad = 'SI es una imagen rugosa'
        plt.subplot(2,4,1),plt.imshow(images[0],cmap = 'gray')
        plt.title('Imagen Original'), plt.xticks([]), plt.yticks([])
        plt.subplot(2,4,2), plt.hist(images[0].ravel(),256)
        plt.title('Histogramas')   , plt.xticks([], plt.yticks([]))
        plt.subplot(2,4,3),plt.imshow(edges,cmap = 'gray')
        plt.title('Bordes'), plt.xticks([]), plt.yticks([])
        plt.subplot(2,4,4),plt.imshow(images[1],cmap = 'gray')
        plt.title('Umbral'), plt.xticks([]), plt.yticks([])              
        plt.subplot(2,4,5), plt.axis('off')
        plt.title('Rugosidad = ' + str(rugosidadfinal) + '\n' + 'Tipo de rugosidad = ' + str(tiporugosidad)), plt.xticks([]), plt.yticks([]), plt.axis('off')
        plt.show()        
    except Exception as e:
        print e
        print("\n\n(X) - Esa opcion no es valida")

except:
	print "\n\n(X) - NO SELECCIONASTE UN ARCHIVO VALIDO!\a"
	print "\n\n 	 Saliendo del programa...\a"

cv2.waitKey(0)
cv2.destroyAllWindows()