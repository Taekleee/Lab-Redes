
from matplotlib import pyplot
from random import randint, uniform,random
import numpy as np
#Modulación ASK

def digitalPlot(s_digital,portadora):
	pyplot.subplot(2,1,1)
	pyplot.title('Señal Digital')
	'''
	xplot = np.repeat(range(len(s_digital)),2)
	yplot = np.repeat(s_digital,2)
	xplot = xplot[1:]
	yplot = yplot[:-1]
	'''
	pyplot.stem(s_digital)

	pyplot.ylim(-0.5,1.5)
	pyplot.subplot(2,1,2)
	pyplot.plot(m_ask)
	pyplot.show()


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
	if s_digital[i] == 0:
		for j in portadora1:
			m_ask.append(j)
	elif s_digital[i] == 1:
		for j in portadora2:
			m_ask.append(j)


digitalPlot(s_digital,m_ask)
