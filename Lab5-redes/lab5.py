
from matplotlib import pyplot
from random import randint, uniform,random
import numpy as np
#Modulación ASK

def digitalPlot(s_digital,m_ask,dem_ask):
	pyplot.subplot(3,1,1)
	pyplot.title('Señal Digital')
	'''
	xplot = np.repeat(range(len(s_digital)),2)
	yplot = np.repeat(s_digital,2)
	xplot = xplot[1:]
	yplot = yplot[:-1]
	'''
	pyplot.stem(s_digital)

	pyplot.ylim(-0.5,1.5)
	pyplot.subplot(3,1,2)
	pyplot.plot(m_ask)

	pyplot.subplot(3,1,3)
	pyplot.stem(dem_ask)
	pyplot.show()

def modular_ask():
	s_digital = []
	m_ask = []
	i = 0
	while i < 100:
		s_digital.append(randint(0,1))
		i = i + 1

	tiempo = np.linspace(0,1,10)
	portadora1 = 5*np.cos(2*np.pi*tiempo)
	portadora2 = 20*np.cos(2*np.pi*tiempo)

	for i in s_digital:
		if i == 0:
			for j in portadora1:
				m_ask.append(j)
		elif i == 1:
			for j in portadora2:
				m_ask.append(j)
	
	return m_ask, s_digital
def demodular_ask(portadora1, portadora2, m_ask):
	dem_ask = []
	demodulada = []
	j = 0
	i = 0
	while i < len(m_ask):
		if m_ask[i] == portadora1[j]:
			while j < len(portadora1):
				dem_ask.append(m_ask[i]*portadora1[j])
				j = j + 1
				i = i + 1
			j = 0
		elif m_ask[i] == portadora2[j]:
			while j < len(portadora2):
				dem_ask.append(m_ask[i]*portadora2[j])
				j = j + 1
				i = i + 1
		
			j = 0
	i = 0
	while  i < len(dem_ask):
		if dem_ask[i] >  40:
			demodulada.append(1)
		else:
			demodulada.append(0)
		i = i + 10
	return demodulada


m_ask,s_digital = modular_ask()
tiempo = np.linspace(0,1,10)
portadora1 = 5*np.cos(2*np.pi*tiempo)
portadora2 = 20*np.cos(2*np.pi*tiempo)
dem_ask = demodular_ask(portadora1,portadora2,m_ask)
digitalPlot(s_digital, m_ask,dem_ask)



