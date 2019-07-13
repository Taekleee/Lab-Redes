
from matplotlib import pyplot
from random import randint, uniform,random
import numpy as np
from scipy.signal import butter, filtfilt, freqz
import scipy.integrate as integrate


#Modulación ASK

def digitalPlot(s_digital,m_ask,dem_ask):
	'''
	Entradas: Señal digita, modulación ask y demodulación ask
	Descripción: Se crean tres gráficos de amplitud vs tiempo
	Salida: Gráfico con los tres valores de entrada
	'''
	pyplot.subplot(3,1,1)
	pyplot.title('Señal Digital entrada')
	pyplot.ylabel('Amplitud')

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

#***********************************************************************************************************************
#***********************************************************************************************************************
def modular_ask(s_digital,tasa_de_bits):
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
	m_ask = []
	tiempo = np.linspace(0,1,2*tasa_de_bits)
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

#***********************************************************************************************************************
#***********************************************************************************************************************

def demodular_ask(tasa_de_bits, m_ask):

	'''
	Entradas: m_ask = señal modulada en ask
			  tasa_de_bits = cantidad de bits por unidad de tiempo
	Descripción: Se recorre el arreglo con la señal modulada y se calcula un promedio según la cantidad de muestras de cada bit (tasa de bits),
				 si el valor es igual o mayor al promedio de la portadora con amplitud mayor (portadora 2) se asigna un 1 al nuevo arreglo
				 de salida, en caso contrario un 0.
	Salida: Señal digital demodulada
	'''
	dem_ask = []
	demodulada = []
	muestras = tasa_de_bits*2
	tiempo = np.linspace(0,1,muestras)
	portadora1 = 5*np.cos(2*np.pi*tiempo)
	portadora2 = 20*np.cos(2*np.pi*tiempo)
	prom_portadora = 0

	for i in portadora2:
		prom_portadora  = prom_portadora + i
	prom_portadora = prom_portadora/muestras
	promedio = 0
	i = 0
	
	while  i < len(m_ask):
		j = 0
		while j < muestras:
			promedio = promedio+m_ask[i]
			j = j + 1
			i = i + 1
		promedio = promedio/tasa_de_bits
		if promedio >=  prom_portadora:
			demodulada.append(1)
		else:
			demodulada.append(0)
	return demodulada


#***********************************************************************************************************************
#***********************************************************************************************************************


def ruido(m_ask,snr,energia):
	'''
	Entradas: m_ask: señal modulada ask
			  snr: razón de ruido de la señal
			  Energia: energía que tiene la señal modulada original
	Descripción: la función se encarga de añadir ruido gaussiano a la señal modulada en ask. 
				 El ruido dependerá de la razón de la señal de ruido (SNR). Para esto se utiliza la función
				 normal de numpy, quien recibe como parámetros la media, la desviación estándar y la cantidad de 
				 elementos. Esta función se multiplica con la desviación estandar obtenidas de la relación:
				 Desviación = Energia de la señal/SNR.Por lo que finalmente entrega un arreglo de ruido que es sumado con la señal modulada
				 ask.
	Salida: señal ask con ruido
	'''
	c_elementos = len(m_ask)
	desviacion = np.sqrt(energia/snr)
	ruido = desviacion*np.random.normal(0,1,c_elementos)
	s_awgn = m_ask + ruido
	
	pyplot.show()
	pyplot.plot(s_awgn)
	pyplot.title("Señal modulada ask con ruido (awgn)")
	pyplot.show()
	return s_awgn

#***********************************************************************************************************************
#***********************************************************************************************************************

def t_errores(s_digital_e, s_digital_r):

	'''
	Entradas: s_digital_e: Señal digital que se envía para la transmisión
			  s_digital_r: Señal digital que se recibe luego de ser aplicado el ruido
	Descripción: La función se encarga de calcular la cantidad de bits erroneos luego de ser
				 recibidos. Para esto se recorren los dos arreglos de bits ingresados (señal digital
				 transmitida y recibida), se cuentan aquellos que sean distintos y se dividen por la 
				 cantidad total de bits transmitidos.
	'''
	i = 0
	errores = 0
	while i < len(s_digital_e):
		if(s_digital_e[i] != s_digital_r[i]):
			errores = errores + 1
		i = i+1
	tasa_error = errores/len(s_digital_e)
	return tasa_error

#***********************************************************************************************************************
#***********************************************************************************************************************

def bits_seudoAleatorios(cantidad):
	'''
	Entrada: cantidad: número de elementos a generar
	Descripción: se genera un arreglo de números 0 y 1
	Salida: Arreglo de bits
	'''
	bits = []
	i = 0
	while i < cantidad:
		bits.append(randint(0,1))
		i = i + 1
	return bits

#***********************************************************************************************************************
#***********************************************************************************************************************

def energia(senal):
	'''
	entrada: Señal original
	Descripción: Utilizando simpson se calcula la energía de la señal, la cual corresponde a la 
				 integral.
	Salida: energía de la señal
	'''
	muestras = len(senal)
	dt = 1/muestras
	fin = muestras*dt
	t = np.arange(0,fin,dt)
	cuadrado = np.power(senal, 2)
	energia = integrate.simps(cuadrado,t)
	return energia

#***********************************************************************************************************************
#***********************************************************************************************************************
#***********************************************************************************************************************
#***********************************************************************************************************************
#MAIN
'''
s_digital = Se genera el arreglo de bits a modular con X elementos
tasa_de_bits = cantidad de bits por unidad de tiempo, en este caso corresponde a 10 bits por segundo
'''
s_digital = [1,0,1,1,0,1,0,1,0,0,0,1,0,1,0,1,1,0,0,1,0,1,0,1,0,1,0,1,0,1,0,1]
tasa_de_bits = 10
print("Arreglo de prueba pequeño con ",len(s_digital),"\nTasa de bits: ",tasa_de_bits)

#PARTE 1: Modulador ask para un sistema pequeño
m_ask = modular_ask(s_digital,tasa_de_bits)



#PARTE 2: Demodulador digital
dem_ask = demodular_ask(tasa_de_bits,m_ask)
digitalPlot(s_digital, m_ask,dem_ask)


#PARTE 3: Simulador de canal tipo AWGN. Recibe como parámetro la razón de señal a ruido (SNR) y una señal modulada.
#Retorna la señal de entrada con el nivel de ruido seleccionado. Se calcula también la energía de la señal.
en = energia(m_ask)
s_awgn = ruido(m_ask,4,en)
demodulada = demodular_ask(tasa_de_bits,s_awgn)
error = t_errores(s_digital,demodulada)
print("Energía de la señal: ",en,"\nSnr: 4\nTasa de errores de bits: ",error,"\n\n\n******************************************\n\n")



#PARTE 4 (TASA DE ERROR)
#Generar bits aleatorios 10^5
s_emisor = bits_seudoAleatorios(100000)

#niveles de ruido
n_ruido = [1,2,3,4,8,10]
errores = []
tasa_de_bits2 = [5,10,15]
print("Arreglo aleatorio con 10^5 bits")
for j in tasa_de_bits2:

	for i in n_ruido:
		modulada = modular_ask(s_emisor,tasa_de_bits)
		en = energia(modulada)
		transmitir = ruido(modulada,i,en)
		demodulada = demodular_ask(tasa_de_bits,transmitir)
		error = t_errores(s_emisor,demodulada)
		errores.append(error)
		print("TASA DE BITS: ",j,"\nEnergía de la señal: ",en,"\nSnr: ",i,"\nTasa de errores de bits: ",error,"\n\n\n******************************************\n\n")
	pyplot.title("BER vs SNR")
	pyplot.plot(n_ruido,errores)
	pyplot.xlabel("SNR")
	pyplot.ylabel("Tasa de errores de bit")
	pyplot.show()
	errores = []

