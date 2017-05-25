#PIA Deteccion de rugosidad de la corteza de un arbol
#Materia: Vision Computacional

import cv2
import Tkinter 
import tkFileDialog
from matplotlib import pyplot as plt

def Rugosidad():
    blur = cv2.GaussianBlur(Pr_img , (5,5), 0)
    ret, otsu = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    images = [blur, otsu]
    return images

#Inicia programa
print "\n[---- Rugosidad Arbol ----] \n\n (i) - Vamos a procesar una imagen primero escoje un archivo de imagen valido "

#Seleccion de imagen
Tkinter.Tk().withdraw() 
ruta = tkFileDialog.askopenfilename(filetypes=(("Archivos JPG", "*.jpg"),
											("Archivos JPEG", "*.jpeg"),
											("Archivos PNG", "*.png"),
                                            ("Todo los archivos", "*.*")))                
#Se lee la imagen
try:

    Or_img 	= cv2.imread(ruta,0) #Imagen original
    Pr_img	= cv2.imread(ruta,0) #Imagen procesada
    prop 	= Or_img.shape   #obtiene propiedades de la imagen
    height 	= prop[0] - 1 #obtiene filas
    width 	= prop[1] - 1 #obtiene cols	
    print "\n\n (i) - Imagen leida exitosamente.\n       Detalles:\n       -Ancho  -> " + str(width) + "px\n       -Altura -> " + str(height) + "px\n       -Ruta   -> " + ruta 

    #Se realiza la opcion seleccionada
    try:	                                        
        images = Rugosidad()        
        titles = ['Filtro Gaussiano','Histograma',"Umbral Otsu"]        

        plt.subplot(3,3,1),plt.imshow(images[0],'gray')
        plt.title(titles[0]), plt.xticks([]), plt.yticks([])
        plt.subplot(3,3,2),plt.hist(images[0].ravel(),256)
        plt.title(titles[1]), plt.xticks([]), plt.yticks([])
        plt.subplot(3,3,3),plt.imshow(images[1],'gray')
        plt.title(titles[2]), plt.xticks([]), plt.yticks([])
        plt.show() 
        # Guardar()
    except Exception as e:        
        print e
        print("\n\n(X) - Esa opcion no es valida")

except:
	print "\n\n(X) - NO SELECCIONASTE UN ARCHIVO VALIDO!\a"
	print "\n\n 	 Saliendo del programa...\a"

cv2.waitKey(0)
cv2.destroyAllWindows()


