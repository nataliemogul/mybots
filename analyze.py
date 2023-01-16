import numpy
import matplotlib.pyplot

data = numpy.load('data/backLegSensorValues.npy')
data1 = numpy.load('data/frontLegSensorValues.npy')
print(data)
matplotlib.pyplot.plot(data, linewidth = 4)
matplotlib.pyplot.plot(data1)
matplotlib.pyplot.legend((data, data1), ('label1', 'label2'))
matplotlib.pyplot.legend()
matplotlib.pyplot.show()