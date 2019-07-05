
from matplotlib import pyplot
from random import randint, uniform,random
import numpy as np
from scipy.signal import butter, filtfilt, freqz

#Modulación ASK

def digitalPlot(s_digital,m_ask,dem_ask):
	pyplot.subplot(3,1,1)
	pyplot.title('Señal Digital entrada')
	pyplot.ylabel('Amplitud')
	'''
	xplot = np.repeat(range(len(s_digital)),2)
	yplot = np.repeat(s_digital,2)
	xplot = xplot[1:]
	yplot = yplot[:-1]
	'''
	pyplot.stem(s_digital)
	pyplot.xlabel('Tiempo')
	pyplot.ylim(-0.5,1.5)
	pyplot.subplot(3,1,2)
	pyplot.plot(m_ask)
	pyplot.title('Señal modulada ask')
	pyplot.xlabel('Tiempo')
	pyplot.ylabel('Amplitud')


	pyplot.subplot(3,1,3)
	pyplot.title('Señal demodulada ask')
	pyplot.xlabel('Tiempo')
	pyplot.ylabel('Amplitud')
	pyplot.stem(dem_ask)
	pyplot.show()

'''
Entradas: s_digital: arreglo de bits a modular con X elementos
		  tasa_de_bits = cantidad de bits por unidad de tiempo
Descripción: Se crea un arreglo de tiempo entre 0 y 1, en donde la cantidad de elementos corresponde
			 a la tasa de bits ingresada. También se generan las funciones portadoras 1 y 2 (coseno), en donde
			 lo que varía es la amplitud (5 y 20), ya que la modulación a generar corresponde a ask. Se evalúa
			 el arreglo de tiempo en cada portadora y a continuación se recorre el arreglo de bits, si se encuentra
			 un 0 se añade a un nuevo arreglo los elementos de la portadora 1 y en caso de ser 1 los elementos de
			 la portadora 2.
Salida: Señal modulada en ask (amplitud)
'''
def modular_ask(s_digital,tasa_de_bits):
	m_ask = []
	tiempo = np.linspace(0,1,tasa_de_bits)
	portadora1 = 5*np.cos(2*np.pi*tiempo)
	portadora2 = 20*np.cos(2*np.pi*tiempo)

	for i in s_digital:
		if i == 0:
			for j in portadora1:
				m_ask.append(j)
		elif i == 1:
			for j in portadora2:
				m_ask.append(j)
	
	return m_ask


'''
Entradas: m_ask = señal modulada en ask
		  tasa_de_bits = cantidad de bits por unidad de tiempo
Descripción: Se recorre el arreglo con la señal modulada, si el valor es igual o similar al de la portadora
			 se vuelve a multiplicar por la misma señal. Por último se vuelve a recorrer el arreglo y si el 
			 valor es mayor a 40 se asigna un bit 1 y si es menor un bit 0. De esta forma es posible retornar
			 la señal digital
Salida: Señal digital demodulada
'''
def demodular_ask(tasa_de_bits, m_ask):
	dem_ask = []
	demodulada = []

	tiempo = np.linspace(0,1,tasa_de_bits)
	portadora1 = 5*np.cos(2*np.pi*tiempo)
	portadora2 = 20*np.cos(2*np.pi*tiempo)
	j = 0
	i = 0
	while i < len(m_ask):
		if abs(m_ask[i]) < portadora1[j] + 2 and abs(m_ask[i]) > portadora1[j] - 2:
			while j < len(portadora1):
				dem_ask.append(m_ask[i]*portadora1[j])
				j = j + 1
				i = i + 1
			j = 0
		elif abs(m_ask[i]) < portadora2[j] + 2 and abs(m_ask[i]) > portadora2[j] - 2:
			while j < len(portadora2):
				dem_ask.append(m_ask[i]*portadora2[j])
				j = j + 1
				i = i + 1
		
			j = 0
	pyplot.plot(dem_ask)
	pyplot.title("modulada*modulada")
	pyplot.show()
	i = 0
	while  i < len(dem_ask):
		if dem_ask[i] >  40:
			demodulada.append(1)
		else:
			demodulada.append(0)
		i = i + 10
	return demodulada


'''
Entradas: m_ask: señal modulada ask
Descripción: la función se encarga de añadir ruido gaussiano a la señal modulada en ask. 
			 El ruido dependerá de la razón de la señal de ruido (SNR). Para esto se utiliza la función
			 normal de numpy, quien recibe como parámetros la media, la desviación estándar y la cantidad de 
			 elementos, por lo que finalmente entrega un arreglo de ruido que es sumado con la señal modulada
			 ask.
Salida: señal ask con ruido
'''
def ruido(m_ask,snr):
	c_elementos = len(m_ask)
	media = 0

	for i in m_ask:
		media = media + i
	media = media/c_elementos

	desviacion = media/snr
	ruido = np.random.normal(0,desviacion,c_elementos)
	s_awgn = m_ask + ruido

	pyplot.plot(ruido)
	pyplot.show()
	pyplot.plot(s_awgn)
	pyplot.title("Señal modulada ask con ruido (awgn)")
	pyplot.show()
	return s_awgn

'''
Entradas: s_digital_e: Señal digital que se envía para la transmisión
		  s_digital_r: Señal digital que se recibe luego de ser aplicado el ruido
Descripción: La función se encarga de calcular la cantidad de bits erroneos luego de ser
			 recibidos. Para esto se recorren los dos arreglos de bits ingresados (señal digital
			 transmitida y recibida), se cuentan aquellos que sean distintos y se dividen por la 
			 cantidad total de bits transmitidos.
'''
def t_errores(s_digital_e, s_digital_r):

	errores = 0
	j = 0
	for i in s_digital_e:
		if s_digital_e[j] == s_digital_r:
			errores = errores + 1
		j = j + 1

	tasa_error = errores/len(s_digital_e)
	return tasa_error



'''
s_digital = Se genera el arreglo de bits a modular con X elementos
tasa_de_bits = cantidad de bits por unidad de tiempo, en este caso corresponde a 10 bits por segundo
'''
s_digital = [1,0,1,1,0,1,0,1,0,0,0,1,0,1,0,1,1,0,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,0,1,0,1,0,1,0,1,0,1]
tasa_de_bits = 10
m_ask = modular_ask(s_digital,tasa_de_bits)


dem_ask = demodular_ask(tasa_de_bits,m_ask)



digitalPlot(s_digital, m_ask,dem_ask)
s_awgn = ruido(m_ask,4)
dem_ask2 = demodular_ask(tasa_de_bits,s_awgn)
pyplot.stem(dem_ask2)
pyplot.title("demodulada con ruido")
pyplot.show()
print(dem_ask)
print(dem_ask2)
print(t_errores(dem_ask,dem_ask2))
