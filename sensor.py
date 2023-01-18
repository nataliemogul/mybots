import numpy

class SENSOR:
    def __init__(self, linkName):
        self.linkName = linkName
        self.values = numpy.zeros(1000)

    def Get_Value(self, i):
        values[i] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)
        print(values)