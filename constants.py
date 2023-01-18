import numpy

amplitude_front = numpy.pi/4
frequency_front = 10
phaseOffset_front = 0

amplitude_back = numpy.pi/4
frequency_back = 10
phaseOffset_back = 0

targetAngles = numpy.linspace(0, 2*numpy.pi, 1000)
targetAngles_front = amplitude_front/2 * numpy.sin(100 * targetAngles + phaseOffset_front)
targetAngles_back = amplitude_back * numpy.sin(10 * targetAngles + phaseOffset_back)