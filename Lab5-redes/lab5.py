from matplotlib import pyplot
from random import randint, uniform,random
import numpy as np
#MODULACIÓN ASK

  = []
m_ask = []
i = 0
while i < 100:
	s_digital.append(randint(0,1))
	i = i + 1

#tiempo = arreglo con la cantidad de bits por segundo (0.25)
tiempo = np.linspace(0,1,10)
portadora1 = 5*np.cos(2*np.pi*tiempo)
portadora2 = 20*np.cos(2*np.pi*tiempo)


#Hay 10 muestras por segundo
for i in s_digital:
	if s_digital[i] == 0:
		for j in portadora1:
			m_ask.append(j)
	elif s_digital[i] == 1:
		for j in portadora2:
			m_ask.append(j)



pyplot.plot(m_ask)
pyplot.show()



#DEMODULACIÓN ASK: multiplicar por la portadora para volver a la original

