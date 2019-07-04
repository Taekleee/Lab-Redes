from matplotlib import pyplot
from scipy import signal
import scipy.io.wavfile as waves
from scipy.fftpack import fft, fftfreq
import numpy as np
from scipy.signal import butter, filtfilt, freqz


'''
########################################################################################################################
Entradas: Sonido: Es la amplitud de entrada del archivo de audio (en el tiempo).
          Muestreo: indica la cantidad de muestras que hay en un segundo
Descripción: spectrogram permite calcular el espectrograma de una señal con transformadas de Fourier consecutivas
             se utiliza para representar la frecuencia en función del tiempo y su amplitud. (gráfico en 3 dimensiones)
'''


def espectro(sonido,muestreo):
     frecuencias, tiempos, espectrograma = signal.spectrogram(sonido,muestreo)
     return frecuencias, tiempos, espectrograma

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
Entrada:  transformada: corresponde a los valores de la transformada de Fourier
Descripción: La función retorna el valor de la inversa de Fourier (pasa del dominio de la frecuencia al dominio del
             tiempo).

'''
def inversa(transformada):
    return np.fft.ifft(transformada)


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

Entradas: 
     elemento1 = el orden del filtro
     elemento2 = rango de frecuencias críticas. Para una señal análoga está es rad/s, para una
                 digital entre 0 y 1
     elemento3 = tipo de filtro
     elemento4 = analógico o digital
Descripción: La función permite obtener un arreglo con los valores de un audio luego de ser aplicado un tipo específico de filtro
'''
def filtroLow(deltaT,sonido,muestreo):
     b, a = butter(3,1000, btype='low', fs=muestreo)
     resultado = filtfilt(b, a,sonido)
     return resultado


def filtroHigh(deltaT,sonido,muestreo):
     b, a = butter(3,3000, btype='high', fs=muestreo)
     resultado = filtfilt(b, a,sonido)
     return resultado


def filtroBand(deltaT,sonido,muestreo):
     b,a = butter(3,[2000,3000],btype='band',fs=muestreo)
     resultado = filtfilt(b,a,sonido)
     return resultado






#Se abre la señal 
muestreo,sonido = waves.read("handel.wav")
deltaT = 1/muestreo
x = funcionTiempo(deltaT,sonido)

#Se grafica el espectrograma (tiempo en función de la frecuencia)
frecuencias, tiempos, espectrograma = espectro(sonido,muestreo)
imagen = pyplot.pcolormesh(tiempos,frecuencias,np.log10(espectrograma))
pyplot.title('Espectrograma audio original')
pyplot.xlabel('Tiempo [s]')
pyplot.ylabel('Frecuencia [Hz]')
pyplot.colorbar(imagen).set_label('Intensidad (dB)')
pyplot.show()

#Se generan los filtros

filtroLow = filtroLow(deltaT,sonido,muestreo)
filtroHigh= filtroHigh(deltaT,sonido,muestreo)
filtroBand = filtroBand(deltaT,sonido,muestreo)

frecuenciaH, transformadaH = transformada(deltaT,filtroHigh)
frecuenciaL,transformadaL = transformada(deltaT,filtroLow)
frecuenciaB, transformadaB = transformada(deltaT,filtroBand)
frecuencia, transformada = transformada(deltaT,sonido)




#Gráfico en el dominio de la frecuencia (transformada)

pyplot.title('Gráfico en el dominio de la frecuencia (original)')
pyplot.xlabel('Frecuencia (Hz)')
pyplot.ylabel('Amplitud (dB)')
pyplot.plot(frecuencia,abs(transformada),'b')
pyplot.show()


#Gráfico en el dominio de la frecuencia (transformada)

pyplot.title('Gráfico en el dominio de la frecuencia (filtro pasa bajos)')
pyplot.xlabel('Frecuencia (Hz)')
pyplot.ylabel('Amplitud (dB)')
pyplot.plot(frecuenciaL,abs(transformadaL),'g')
pyplot.show()


#Gráfico en el dominio de la frecuencia (transformada)

pyplot.title('Gráfico en el dominio de la frecuencia (filtro pasa altos)')
pyplot.xlabel('Frecuencia (Hz)')
pyplot.ylabel('Amplitud (dB)')
pyplot.plot(frecuenciaH,abs(transformadaH),'r')
pyplot.show()


#Gráfico en el dominio de la frecuencia (transformada)

pyplot.title('Gráfico en el dominio de la frecuencia (filtro pasa medios)')
pyplot.xlabel('Frecuencia (Hz)')
pyplot.ylabel('Amplitud (dB)')
pyplot.plot(frecuenciaB,abs(transformadaB),'m')
pyplot.show()



#Gráfico del audio en el tiempo

pyplot.title('Gráfico función de audio en el tiempo (filtro pasa bajos)')
pyplot.xlabel('Tiempo (s)')
pyplot.ylabel('Amplitud (dB)')
pyplot.plot(x,filtroLow,'g')
pyplot.show()

#Gráfico del audio en el tiempo

pyplot.title('Gráfico función de audio en el tiempo (filtro pasa altos)')
pyplot.xlabel('Tiempo (s)')
pyplot.ylabel('Amplitud (dB)')
pyplot.plot(x,filtroHigh,'r')
pyplot.show()




#Gráfico del audio en el tiempo

pyplot.title('Gráfico función de audio en el tiempo (filtro medio)')
pyplot.xlabel('Tiempo (s)')
pyplot.ylabel('Amplitud (dB)')
pyplot.plot(x,filtroBand,'m')
pyplot.show()

#Se grafica el espectrograma (tiempo en función de la frecuencia y amplitud)
frecuenciasL, tiemposL, espectrogramaL = espectro(filtroLow,muestreo)
imagen = pyplot.pcolormesh(tiemposL,frecuenciasL,np.log10(espectrogramaL))
pyplot.title('Espectrograma audio usando filtro pasa bajos')
pyplot.xlabel('Tiempo [s]')
pyplot.ylabel('Frecuencia [Hz]')
pyplot.colorbar(imagen).set_label('Intensidad (dB)')
pyplot.show()

#Se grafica el espectrograma (tiempo en función de la frecuencia)
frecuenciasH, tiemposH, espectrogramaH = espectro(filtroHigh,muestreo)
imagen = pyplot.pcolormesh(tiemposH,frecuenciasH,np.log10(espectrogramaH))
pyplot.title('Espectrograma audio usando filtro pasa altos')
pyplot.xlabel('Tiempo [s]')
pyplot.ylabel('Frecuencia [Hz]')
pyplot.colorbar(imagen).set_label('Intensidad (dB)')
pyplot.show()


#Se grafica el espectrograma (tiempo en función de la frecuencia)
frecuenciasB, tiemposB, espectrogramaB = espectro(filtroBand,muestreo)
imagen = pyplot.pcolormesh(tiemposB,frecuenciasB,np.log10(espectrogramaB))
pyplot.title('Espectrograma audio usando filtro pasa medios')
pyplot.xlabel('Tiempo [s]')
pyplot.ylabel('Frecuencia [Hz]')
pyplot.colorbar(imagen).set_label('Intensidad (dB)')
pyplot.show()


#Se escriben los archivos de audio

waves.write('filtroL.wav',muestreo,filtroLow)
waves.write('filtroH.wav',muestreo,filtroHigh)
waves.write('filtroB.wav',muestreo,filtroBand)


