from matplotlib import pyplot
from scipy import signal
import scipy.integrate as integral
import scipy.io.wavfile as waves
from scipy.fftpack import fft, fftfreq
import numpy as np
from scipy.signal import butter, filtfilt, freqz
import math
from scipy import interpolate


def interpolacionAM(sonido,muestreo):
    '''
    Entradas: recibe las amplitudes de la señal junto con el rate de frecuencias
    Salida: la señal interpolada
    Procedimiento: Crea un vector tiempo con Numpy, y se interpola la señal respecto a ese tiempo,
    y finalmente se devuelve la función interpolada evaluada en dicho tiempo
    '''
    duracion = len(sonido)/muestreo
    tiempo=np.linspace(0,duracion, num=len(sonido))
    interpolacion = interpolate.interp1d(tiempo,sonido)
    y2 = interpolacion(tiempo)
    return y2

def modulacionAM(interpolada,sonido,muestreo,k):
    '''
    Entradas: La señal ya interpolada, el sonido y el rate de muestreo del audio original, y el indice de modulacion k
    Salidas: se retorna el tiempo de la señal original, las amplitudes de la señal original, el tiempo de la portadora
    la señal portadora, el tiempo y la señal modulada, además de la frecuencia con la que se modula
    Procedimiento: se forma la portadora con el doble de la frecuencia de muestreo para cumplir el teorema de Nyquist,
    se aplica en un coseno, y esta se multiplica por la señal interpolada.
    '''
    largo_interpolada = len(interpolada)
    fc = 2*muestreo
    tiempo_modulada = np.linspace(0,largo_interpolada/muestreo,num=largo_interpolada)
    tiempo_original = np.linspace(0,len(sonido)/muestreo,num=len(sonido))
    portadora = np.cos(2*np.pi*fc*tiempo_modulada)
    modulada = k*interpolada*portadora
    tiempo_portadora = np.linspace(0,len(portadora)/muestreo, num=len(portadora))
    return tiempo_original,sonido,tiempo_portadora,portadora,tiempo_modulada,modulada,fc


def modulacionFM(interpolada,sonido,muestreo,k):
    '''
    Entradas: La señal ya interpolada, el sonido y el rate de muestreo del audio original, y el indice de modulacion k
    Salida: la señal modulada FM, junto con otros parametros
    Procedimiento: Se calcula la integral que corresponde a la frecuencia instantanea del mensaje, y el resto de lo que corresponde
    al coseno que recibe la señal y la modula
    '''
    largo_interpolada = len(interpolada)
    fc = 3*muestreo
    tiempo_modulada = np.linspace(0,largo_interpolada/muestreo,num=largo_interpolada)
    tiempo_original = np.linspace(0,len(sonido)/muestreo,num=len(sonido))
    modulada = np.cos(2*np.pi*fc*tiempo_modulada + (np.cumsum(interpolada)/muestreo)*k )
    portadora = np.cos(2*np.pi*fc*tiempo_modulada)
    tiempo_portadora = np.linspace(0,len(portadora)/muestreo, num=len(portadora))

    return tiempo_original,sonido,tiempo_portadora,portadora,tiempo_modulada,modulada,fc

def demodulacionAM(modulada,muestreo,interpolada):
    '''
    Entradas: La señal modulada, la señal original interpolada, y el rate de frecuencias de muestreo
    Salida: la señal demodulada y el vector tiempo de esta
    Procedimiento: se crea la misma portadora que en el proceso de modulacion y se multiplica a la señal
    modulada por esta portadora, y luego se aplica un filtro pasabajos para retornar finalmente  la señal
    demodulada
    '''
    largo_interpolada = len(interpolada)
    fc = 2*muestreo
    tiempo_modulada = np.linspace(0,largo_interpolada/muestreo,num=largo_interpolada)
    portadora = np.cos(2*np.pi*fc*tiempo_modulada)
    demodulada = modulada * portadora

    b, a = butter(3,4000,'low',fs=muestreo)
    resultado = filtfilt(b, a,demodulada)



    return tiempo_modulada, resultado



def transformada(deltaT,sonido):
    '''
    Entradas: deltaT: corresponde al espacio entre los intervalos del eje x.
              Sonido: Es la amplitud de entrada del archivo de audio (en el tiempo).
    Salida: La transformada de fourier de una señal
    Descripción: fft devuelve la transformada discreta de fourier, fftfreq devuelve la frecuencia que corresponde cada
                 punto de la transformada discreta, en base a n (siendo n el tamaño que tiene el array de la transformada)
                 y el diferencial (espacio entre los intervalos).
    '''

    transformada = fft(sonido)
    n= transformada.size
    frecuencia = fftfreq(n,deltaT)
    return frecuencia,transformada



def graficar(tipo, x1,x2,y1,y2,z1,z2,w1,w2,i):
    '''
    Entrada: los distintos ejes de los graficos, para la señal original, la portadora, la modulada, la transformada y la demodulada
    Salida: Los distintos graficos por pantalla
    Procedimiento: Se realizan los distintos plots segun el tipo de grafico entregado por parametro, y segun el indice de modulacion i entregado por parametro
    '''
    if tipo==0:
        cantidad = 4
        ejeX = 'Tiempo (s)'
        ejeY = 'Amplitud'
        titulos = ['Señal original en el tiempo', 'Señal portadora en el tiempo','Señal modulada en el tiempo (AM)','Señal demodulada en el tiempo (AM)']
    elif tipo == 1:
        cantidad = 3
        ejeX = 'Tiempo (s)'
        ejeY = 'Amplitud'
        titulos = ['Señal original en el tiempo', 'Señal portadora en el tiempo','Señal modulada en el tiempo (FM)']
    elif tipo == 2:
        cantidad = 4
        ejeX = 'Frecuencia'
        ejeY = 'Amplitud'
        titulos = ['Transformada de Fourier señal de audio','Transformada de Fourier señal portadora','Transformada de Fourier señal modulada (AM)','Transformada de Fourier señal demodulada (AM)']
    elif tipo == 3:
        cantidad = 3
        ejeX = 'Frecuencia'
        ejeY = 'Amplitud'
        titulos = ['Transformada de Fourier señal de audio','Transformada de Fourier señal portadora','Transformada de Fourier señal modulada (FM)']
    if i == 0:
    	k = ' (índice de modulación 15%)'
    elif i == 1:
    	k = ' (índice de modulación 100%)'
    elif i == 2:
    	k = k = ' (índice de modulación 125%)'
    if tipo == 2 or tipo == 3:
        x2 = abs(x2)
        y2 = abs(y2)
        z2 = abs(z2)
        pyplot.subplot(cantidad, 1, 2)
        pyplot.plot(abs(y2),'b')
        pyplot.xlabel(ejeX)
        pyplot.ylabel(ejeY)
        pyplot.title(titulos[1])
        if tipo == 2:
            w2 = abs(w2)

    else:
        pyplot.subplot(cantidad, 1, 2)
        pyplot.plot(y1,y2,'b')
        pyplot.xlabel(ejeX)
        pyplot.ylabel(ejeY)
        pyplot.title(titulos[1])

    pyplot.subplot(cantidad, 1, 1)
    pyplot.plot(x1,x2,'c')
    pyplot.xlabel(ejeX)
    pyplot.ylabel(ejeY)
    pyplot.title(titulos[0])



    pyplot.subplot(cantidad,1,3)
    pyplot.plot(z1,z2,'g')
    pyplot.xlabel(ejeX)
    pyplot.ylabel(ejeY)
    pyplot.title(titulos[2] + k)

    if tipo==0 or tipo == 2:
        pyplot.subplot(cantidad,1,4)
        pyplot.plot(w1,w2,'r')
        pyplot.xlabel(ejeX)
        pyplot.ylabel(ejeY)
        pyplot.title(titulos[3] + k)

    pyplot.show()



#muestreo son la cantidad de frecuencias y sonido las amplitudes
muestreo,sonido = waves.read("handel.wav")
duracion = len(sonido)/muestreo
interpolada= interpolacionAM(sonido,muestreo)
k = [0.15,1,1.25]


i = 0
while i < 3:
	o_tiempo,original,p_tiempo,portadora,m_tiempo,modulada,fcAM = modulacionAM(interpolada,sonido,muestreo,k[i])
	t_demodulada, demodulada = demodulacionAM(modulada,muestreo,interpolada)
	graficar(0,o_tiempo,original,p_tiempo,portadora,m_tiempo,modulada,t_demodulada,demodulada,i)
	if(i == 0):
		waves.write('demodulacionAM_15.wav',muestreo,demodulada)
		print('Se ha creado el archivo demodulacionAM_15.wav')
	elif i == 1:
		waves.write('demodulacionAM_100.wav',muestreo,demodulada)
		print('Se ha creado el archivo demodulacionAM_100.wav')
	elif i == 2:
		waves.write('demodulacionAM_125.wav',muestreo,demodulada)
		print('Se ha creado el archivo demodulacionAM_150.wav')
	o_tiempoFM, originalFM, p_tiempoFM, portadoraFM, m_tiempoFM, moduladaFM,fcFM= modulacionFM(interpolada,sonido,muestreo,k[i])
	graficar(1,o_tiempoFM,originalFM,p_tiempoFM,portadoraFM,m_tiempoFM,moduladaFM,o_tiempoFM,originalFM,i)
	frecuenciaPortadora, transformadaPortadora = transformada(1/muestreo, portadora)
	frecuenciaFM,transformadaFM = transformada(1/fcFM,moduladaFM)
	frecuenciaAM,transformadaAm = transformada(1/fcAM,modulada)
	frecuenciaDemodulada, transformadaDemodulada = transformada(1/muestreo, demodulada)
	frecuenciaOriginal,transformadaOriginal = transformada(1/muestreo,sonido)
	graficar(2,frecuenciaOriginal,transformadaOriginal,frecuenciaPortadora,transformadaPortadora,frecuenciaAM,transformadaAm, frecuenciaDemodulada,transformadaDemodulada,i)
	graficar(3,frecuenciaOriginal,transformadaOriginal,frecuenciaPortadora,transformadaPortadora,frecuenciaFM,transformadaFM, frecuenciaDemodulada,transformadaDemodulada,i)
	i = i + 1
print('El programa ha finalizado con éxito')
