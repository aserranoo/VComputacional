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
        blur = cv2.bilateralFilter(item,9,75,75)
        ret, otsu = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        images.append([blur, otsu])
    return images
    
#Inicia programa
print "\n[---- Rugosidad Arbol ----] \n\n (i) - Vamos a procesar una imagen primero escoje un archivo de imagen valido "

#Seleccion de imagen
# Tkinter.Tk().withdraw() 
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
    # print Org_img
    # Or_img 	= cv2.imread(ruta,0) #Imagen original
    # Pr_img	= cv2.imread(ruta,0) #Imagen procesada
    # prop 	= Or_img.shape   #obtiene propiedades de la imagen
    # height 	= prop[0] - 1 #obtiene filas
    # width 	= prop[1] - 1 #obtiene cols	
    # print "\n\n (i) - Imagen leida exitosamente.\n       Detalles:\n       -Ancho  -> " + str(width) + "px\n       -Altura -> " + str(height) + "px\n       -Ruta   -> " + ruta 

    #Se realiza la opcion seleccionada
    try:	                      
        images = Rugosidad()
        hists = []
        res = []        
        for item in images:
            count = 0    
            for i in item:                
                if count == 0:
                    hist = cv2.calcHist([i.ravel()],[0],None,[256],[0,256])
                    hists.append(hist)
                count+=1
        for i in range(1, len(hists)):
            res.append(cv2.compareHist(hists[0], hists[i], cv2.HISTCMP_BHATTACHARYYA))
        
        # titles = ['Filtro Bilateral','Histograma',"Umbral Otsu"]            
        # for i in range(0, len(images)):            
        #     plt.subplot(1,3,1),plt.imshow(images[0],'gray')
        #     plt.title(titles[0]), plt.xticks([]), plt.yticks([])
        #     plt.subplot(1,3,2),plt.hist(images[0].ravel(), 256)
        #     plt.title(titles[1]), plt.xticks([]), plt.yticks([])
        #     plt.subplot(1,3,3),plt.imshow(images[1],'gray')
        #     plt.title(titles[2]), plt.xticks([]), plt.yticks([])
        # plt.show() 
        # Guardar()
    except Exception as e:        
        print e
        print("\n\n(X) - Esa opcion no es valida")

except:
	print "\n\n(X) - NO SELECCIONASTE UN ARCHIVO VALIDO!\a"
	print "\n\n 	 Saliendo del programa...\a"

cv2.waitKey(0)
cv2.destroyAllWindows()

