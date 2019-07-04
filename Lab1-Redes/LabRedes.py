from matplotlib import pyplot
import scipy.io.wavfile as waves
from scipy.fftpack import fft, fftfreq
import numpy as np


###############################Funciones###############################


def errorCuadraticoMedio(x,y):
    return np.sqrt(((x-y)**2).mean())

'''
########################################################################################################################

Entradas: DeltaT: corresponde al espacio entre los intervalos del eje x.
          Sonido: Es la amplitud de entrada del archivo de audio (en el tiempo).
Descripción: La función retorna el valor de la variable x (duración del audio) para el gráfico de la función en el
             tiempo.
'''

def funcionTiempo(deltaT,sonido):
    duracion = len(sonido) /muestreo
    x = np.linspace(duracion,deltaT,num=len(sonido))
    return x


'''
########################################################################################################################

Entradas: deltaT: corresponde al espacio entre los intervalos del eje x.
          Sonido: Es la amplitud de entrada del archivo de audio (en el tiempo).
Descripción: fft devuelve la transformada discreta de fourier, fftfreq devuelve la frecuencia que corresponde cada
             punto de la transformada discreta, en base a n (siendo n el tamaño que tiene el array de la transformada)
             y el diferencial (espacio entre los intervalos).

'''

def transformada(deltaT,sonido):
    transformada = fft(sonido)
    n= transformada.size
    frecuencia = fftfreq(n,deltaT)
    return frecuencia,transformada

'''
########################################################################################################################
Entradas: transformada: corresponde a los valores de la transformada de Fourier
Descripción: eliminarRuido genera una lista en donde los valores menores a 0.45*10**7 se reemplazan por cero para poder
             eliminar el ruido generado.
'''

def eliminarRuido(transformada):
    sinRuido = []
    for x in transformada:
        if x <= 4.3*10**6:
            sinRuido.append(0)
        else:
            sinRuido.append(x)

    return sinRuido

'''
########################################################################################################################
Entrada:  transformada: corresponde a los valores de la transformada de Fourier
Descripción: La función retorna el valor de la inversa de Fourier (pasa del dominio de la frecuencia al dominio del
             tiempo).

'''
def inversa(transformada):
    return np.fft.ifft(transformada)



###############################MAIN###############################


    
archivoEntrada = ('handel.wav')
#Muestreo indica la cantidad de muestras que hay en un segundo
muestreo,sonido = waves.read(archivoEntrada)
deltaT = float(1/muestreo)
x = funcionTiempo(deltaT,sonido)

#Parámetros de entrada:
#print('Duración audio:',float(1/muestreo), '\nMuestreo: ',muestreo,'\nSonido (Amplitud): ',len(sonido) )


#Gráfico de tiempo (s) en función de la amplitud
#pyplot.subplots(2,1,1)
pyplot.title('Gráfico función de audio en el tiempo')
pyplot.xlabel('Tiempo (s)')
pyplot.ylabel('Amplitud')
pyplot.plot(x,sonido,'c')
pyplot.show()



frecuencia,transformada = transformada(deltaT,sonido)


#Gráfico en el dominio de la frecuencia (transformada)

pyplot.title('Gráfico en el dominio de la frecuencia')
pyplot.xlabel('Frecuencia (Hz)')
pyplot.ylabel('Amplitud')
pyplot.plot(frecuencia,abs(transformada),'b')
pyplot.show()


#transformada inversa
tInversa = inversa(transformada).real

#Gráfico de la transformada inversa

pyplot.title('Gráfico función de audio en el tiempo (transformada inversa de Fourier)')
pyplot.xlabel('Tiempo (s)')
pyplot.ylabel('Amplitud')
pyplot.plot(x,tInversa,'g')
pyplot.show()

#Se calcula el error cuadrático medio entre la señal original y la inversa obtenida
#para ver como varía luego de la transformación
print('El error cuadrático medio entre la función original y la inversa de la transformada es: ',errorCuadraticoMedio(sonido,tInversa.real))


#Gráfico en el dominio de la frecuencia sin ruido

sinRuido = np.asarray(eliminarRuido(transformada)).real

pyplot.title('Gráfico en el dominio de la frecuencia sin ruido')
pyplot.xlabel('Frecuencia (Hz)')
pyplot.ylabel('Amplitud')
pyplot.plot(frecuencia,sinRuido,'r')
pyplot.show()



#Gráfico de tiempo (s) en función de la amplitud luego de eliminar el ruido


pyplot.title('Gráfico función de audio en el tiempo (luego de eliminar el ruido)')
pyplot.xlabel('Tiempo (s)')
pyplot.ylabel('Amplitud')
pyplot.plot(x,inversa(sinRuido).real,'c')
pyplot.show()




#Se genera una nueva señal de audio sin ruido
waves.write('sinRuido.wav',muestreo,tInversa)

print('El progama finalizó con éxito')
