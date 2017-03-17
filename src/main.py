#PIA Deteccion de rugosidad de la corteza de un arbol
#Materia: Vision Computacional

import cv2
import numpy
import Tkinter 
import tkFileDialog
import random
import math

#Funciones principales
def Guardar():
    print '\n(i) - Guardar imagen resultante? \a'
    print '\n      [ S / N ]   \a'
    
    Opcion = raw_input('\t->')

    if(Opcion == 'S' or Opcion == 's'):
        try:
            print '\n(i) - Que nombre le damos a la imagen?\a'
            NombreArchivo = raw_input('      ->')
            NombreArchivo = NombreArchivo+'.png'
            cv2.imwrite(NombreArchivo,Pr_img)
            print '\n(i) - Listo!\a'
        except:
            print '\n(X) - No se pudo!\a'

    return 0
#Funciones
def Grises(): #Imagen se convierte a escala de grises
    #Explicacion
    print "\n\n|------------------- A Escala de grises ------------------|"
    print "|    (i) - Se convertira la imagen a escala de grises     |"
    print "|          Formula:                                       |"
    print "|            Gris = R*.299 + G*.587 + B*114               |"
    print "|           Por cada pixel                                |"
    print "|            Pixel[x,y] = Gris                            |"
    print "|           Donde:                                        |"
    print "|           R,G,B = Tonos de los colores primarios (0-255)|"
    print "|---------------------------------------------------------|"

    #Proceso
    print '\n(i) - Cargando...'
    for y in range(height):
        for x in range(width):
            gris = (Or_img[y,x,0]*.114) + (Or_img[y,x,1]*.587) + (Or_img[y,x,2]*.299) #se obtiene el tono de gris del pixel
            Pr_img[y,x,0] = gris; 	#azul	
            Pr_img[y,x,1] = gris; 	#verde
            Pr_img[y,x,2] = gris; 	#rojo
    print '\n(i) - Listo!\a'
    return Pr_img
def Binario():
    #Explicacion
    print "\n\n|-------------------- Umbral Binario ---------------------|"
    print "|    (i) - Aplicando filtro de umbral binario             |"
    print "|          Formula:                                       |"
    print "|          Por cada Pixel[x,y]                            |"
    print "|           Si Pixel[x,y] > U :                           |"
    print "|             Pixel[x,y] = 255                            |"
    print "|           Si Pixel[x,y] <= U :                          |"
    print "|             Pixel[x,y] = 0                              |"
    print "|          Donde: U = Umbral                              |"
    print "|---------------------------------------------------------|"

    #Proceso
    print '\n(i) - Cargando...'

    Umbral = raw_input('\n\n(?) - Nivel de umbral a trabajar? (1-255)\n      ->')
    Umbral = int(Umbral)	
    Pr_img = GrisesOpenCV();
    Or_img = GrisesOpenCV();
    try:        
        for y in range(height):
            for x in range(width):
                if Or_img[y,x] > Umbral:
                    Pr_img[y,x] = 255

                if Or_img[y,x] <= Umbral:
                    Pr_img[y,x] = 0

        print '\n(i) - Listo!\a'
        return Pr_img
    except Exception as e:
        print e
def GrisesOpenCV():
    Pr_img = cv2.imread(ruta,0)
    return Pr_img   
def slicing(l, n):
    return [l[a:a+n] for a in range(0, len(l), n)]     
def grayscale(pixels, lmin=0, lmax=255):
    for a, pixel in enumerate(pixels): 
        color = sum(pixel)/3
        color = 255 if(color >= lmax) else color
        color = 0 if(color <= lmin) else color
        pixels[a] = (color, color, color)
    return pixels    
def convolution2D(f,h):                              # Convolucion discreta usando numpy
    fS, hS = f.shape, h.shape                        # Obtenemos el tamano de la mascara y la imagen
    F = numpy.zeros(shape=fS)                        # Creamos el arreglo donde se guardaran los calculos
    for x in range(fS[0]):                           # Recorremos la imagen a lo alto
        #print str(round(float(x*100.0/fS[0]),2))     # Imprimimos el progreso de la rutina
        for y in range(fS[1]):                       # Recorremos la imagen a lo ancho
            mSum = numpy.array([0.0, 0.0, 0.0])      # Inicializamos la sumatoria en cero   
            for i in range(hS[0]):                   # Recorremos la mascara a lo alto
                i1 = i-(hS[0]/2)                     # Centramos la mascara a lo alto
                for j in range(hS[1]):               # Recorremos la mascara a lo ancho
                    j2 = j-(hS[0]/2)                 # Centramos la mascara a lo ancho  
                    try:                             # Realizamos la sumatoria de los valores
                        mSum += f[x+i1,y+j2]*h[i,j]  # Los bloques try, catch ayudan en a evitar errores
                    except IndexError: pass          # cuando estamos en los pixeles de las orillas
            F[x,y] = mSum                            # Agregamos el nuevo valor al arreglo de la gradiente
    return F      # Regresamos los valores de la gradiente calculados
def borderDetection(): # Rutina para deteccion de     
    pixels = grayscale(Or_img.size)      # Convertir la imagen a escala de grises
    print pixels
    pixels = slicing(pixels, width) # Pasar los pixeles a un arreglo compatible con numpy
    pixels = numpy.array(pixels)    # Pasar los pixeles a un arreglo numpy

    newPixels = list() # Lista que almacenara los nuevos pixeles de la nueva imagen
    iS = pixels.shape  # Obtenermos el tamano del arreglo (tamano de la imagen)

    n = 1.0/1.0        # Multiplicador de las mascaras
    # Usaremos 4 mascaras de Prewitt
    mask1 = numpy.array([[-1,0,1],[-1,0,1],[-1,0,1]]) * n # Prewitt simetrica vertical
    mask2 = numpy.array([[1,1,1],[0,0,0],[-1,-1,-1]]) * n # Prewitt simetrica horizontal
    mask3 = numpy.array([[-1,1,1],[-1,-2,1],[-1,1,1]])* n # Prewitt 0 grados
    mask4 = numpy.array([[1,1,1],[-1,-2,1],[-1,-1,1]])* n # Prewitt 45 grados

    g1 = convolution2D(pixels, mask1) # Llamamos a la rutina de convolucion discreta
    g2 = convolution2D(pixels, mask2) # para aplicar las mascaras
    g3 = convolution2D(pixels, mask3) # una por una
    g4 = convolution2D(pixels, mask4)

    for x in range(iS[0]):            # Recorremos los gradientes que hemos obtenido de aplicar
        for y in range(iS[1]):        # las mascaras a la imagen
            pixel = (g1[x,y]**2) + (g2[x,y]**2) + (g3[x,y]**2) + (g4[x,y]**2) # Buscamos los cambios de direcciones
            pixel = tuple([int(math.floor(math.sqrt(p))) for p in pixel])               # aplicando un acoplamiento
            newPixels.append(pixel)   # Agregamos el nuevo pixel a la lista para armar la nueva imagen

    newPixels = grayscale(newPixels)  # Binarizamos la imagen aplicando umbrales    
    return newPixels                  # Regresamos la lista de nuevos pixeles

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

    Or_img 	= cv2.imread(ruta) #Imagen original
    Pr_img	= cv2.imread(ruta) #Imagen procesada
    prop 	= Or_img.shape   #obtiene propiedades de la imagen
    height 	= prop[0] - 1 #obtiene filas
    width 	= prop[1] - 1 #obtiene cols	
    print "\n\n (i) - Imagen leida exitosamente.\n       Detalles:\n       -Ancho  -> " + str(width) + "px\n       -Altura -> " + str(height) + "px\n       -Ruta   -> " + ruta

    #Se muestra el menu

    listaFunciones = { '1': Grises, '2': GrisesOpenCV, '3' : Binario, '4' : borderDetection}

    print("\n\n (?) - Que deseas hacer con la imagen? Escribe uno de los siguientes comandos \n\t(Respetar las mayusculas y minusculas): \n\t-> "
    "1 : Convierte la imagen a escala de grises\n\t-> "
    "2 : Convierte la imagen a escala de grises con OpenCV\n\t-> "
    "3 : Convierte la imagen de grises a binario para obtener bordes\n\t-> "
    "4 : Deteccion de borde de la imagen")

    #El usuario escoje una opcion

    opcion = raw_input('\t-> ')

    #Se realiza la opcion seleccionada
    try:	
        Pr_img = listaFunciones[opcion]()    
        cv2.imshow("PIA",Pr_img)
        # Guardar()
    except Exception as e:        
        print e
        print("\n\n(X) - Esa opcion no es valida")

except:
	print "\n\n(X) - NO SELECCIONASTE UN ARCHIVO VALIDO!\a"
	print "\n\n 	 Saliendo del programa...\a"

cv2.waitKey(0)
cv2.destroyAllWindows()


