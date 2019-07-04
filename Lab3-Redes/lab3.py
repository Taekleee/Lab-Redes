import numpy
from PIL import Image
from matplotlib import pyplot as plt

'''
########################################################################################################################

Entrada: Nombre de la imagen junto con su extensión
Descripción: La función se encarga de abrir la imagen que se encuentra en la misma carpeta que el programa y la transforma
             por medio de numpy a matriz


'''

def generarMatriz(imagen):
    abrirImagen= Image.open(imagen)
    matriz= numpy.array(abrirImagen)
    abrirImagen.close()
    return matriz

'''
########################################################################################################################

Entrada: Nombre de la imagen junto a su extensión
Descripción: Retorna la imagen.
'''
def abrirImagen(nombre):
    abrirImagen= Image.open(nombre)
    return abrirImagen



'''
########################################################################################################################


Entrada: -
Descripción: La función kernel multiplica la matriz por 1/256, para luego ser aplicado en la imagen

'''

def kernel():
    matriz = [[1,4,6,4,1],[ 4, 16, 24, 16, 4],[ 6, 24, 36, 24, 6],[ 4, 16, 24, 16, 4],[ 1, 4, 6, 4, 1]]
    i = 0;
    j = 0;
    while i < len(matriz):
        while j < len(matriz[i]):
            matriz[i][j] = matriz[i][j]*(1/256)
            j = j+1
        i = i+1
        j = 0
    return matriz
     
'''
########################################################################################################################

Entrada: Imagen: Matriz con los valores de la imagen.
         Kernel: Matriz con los valores del kernel
Descripción: Convolución crea una nueva matriz de ceros en donde son agregados la convolución entre el kernel y la imagen,
             es decir, la suma de las multiplicaciones entre el kernel y una serie de elementos de la imagen.             

'''
def convolucion(imagen,kernel,dim):
    medidas=  list(imagen.shape)
    a= medidas[0]
    b= medidas[1]
    dim = len(medidas)
    if(dim == 3):
        c= medidas[2]
        nuevaImagen= numpy.zeros((a,b,c))
    else:
        nuevaImagen = numpy.zeros((a,b))
    i = 2
    j = 2
    k = 0
    l = 0
    cantI = 0
    cantJ = 0
    suma = 0
    while i < (len(imagen)-2):
        while j < (len(imagen[0])-2):
            while k < len(kernel):
                while l < len(kernel[k]):
                    suma = suma + kernel[k][l]*imagen[i-2][j-2]
                    l = l + 1
                    j = j + 1
                    cantJ = cantJ + 1
                j = j - cantJ
                cantJ = 0
                l = 0
                k = k + 1
                i = i + 1
                cantI = cantI + 1
            i = i -cantI
            nuevaImagen[i-2][j-2] = suma
            suma = 0
            cantI = 0
            k = 0
            j = j + 1
        j = 0
        i = i + 1
    return nuevaImagen



'''
########################################################################################################################

Entrada: Imagen y títulos para los gráficos que serán generados
Descripción: La función primero convierte la imagen a escala de grises, para luego realizar la transformada en dos
             dimensiones. La magnitud se trabaja con logaritmo para lograr comparar los valores.
             Con fftshift se centra el resultado de la transformada, por lo cual el punto 0 se encuentra en el medio
             de la imagen.

'''

################## El código fue obtenido de https://unipython.com/transformada-de-fourier/ ############################
def transformada2D(imagen,titulo1,titulo2,dim):
    transformada = numpy.fft.fft2(imagen) 
    fshift = numpy.fft.fftshift(transformada) 
    magnitudFFT = 20*numpy.log(numpy.abs(fshift))
    plt.subplot(121),plt.imshow(imagen, cmap = 'gray')
    plt.title(titulo1), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(magnitudFFT)
    plt.colorbar().set_label('Intensidad (dB)')
    plt.xlabel('Frecuencia [Hz]')
    plt.ylabel('Frecuencia [Hz]')

    plt.title(titulo2), plt.xticks([]), plt.yticks([])
    plt.show()

#########################################################################################################################

    

#Se abre la imagen, se crea el kernel 2 y se llama a la convolución
nombreImagen = 'leena512.bmp'
matrizImagen= generarMatriz(nombreImagen)
medidas=  list(matrizImagen.shape)
dim = len(medidas)
imagen = abrirImagen(nombreImagen)
kernel2 = [[ 1, 2, 0, -2, -1],[ 1, 2, 0, -2, -1],[ 1, 2, 0, -2, -1],[ 1, 2, 0, -2, -1],[ 1, 2, 0, -2, -1]]
print("Procesando la imagen")


salida1 = convolucion(matrizImagen,kernel(),dim)
salida2 = convolucion(matrizImagen,kernel2,dim)


print("Terminó con éxito")

if(dim == 3):

#Se genera una nueva imagen, en donde los valores deben ir entre 0 y 255 en formato RBG
    imagenSalida1 = Image.fromarray(salida1.clip(0,255).astype('uint8'), 'RGB')
    imagenSalida2 = Image.fromarray(salida2.clip(0,255).astype('uint8'), 'RGB')
    imagenSalida1.save("Salida11.png")
    imagenSalida2.save("Salida22.png")

else:

    imagenSalida1 = Image.fromarray(salida1.clip(0,255).astype('uint8'))
    imagenSalida2 = Image.fromarray(salida2.clip(0,255).astype('uint8'))
    imagenSalida1.save("Salida1.bmp")
    imagenSalida2.save("Salida2.bmp")
    #Se calcula la transformada de la imagen y se genera el gráfico.
    transformada2D(imagen,"Imagen Original", "Transformada de Fourier Original",dim)
    transformada2D(imagenSalida1,"Imagen con filtro suavizado Gaussiano","Transformada de Fourier (Suavizado Gaussiano)",dim)
    transformada2D(imagenSalida2,"Imagen con filtro detector de bordes","Transformada de Fourier (Detector de bordes)",dim)



#Se cierra la imagen
imagen.close()


