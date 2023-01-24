import numpy

class SOLUTION:
    def __init__(self):
        self.weights = numpy.random.rand(3,2)*2-1

    def Evaluate(self):
        pass

    def Create_World(self):
        pass

    def Create_Robot(self):
        pass
    
    def Generate_Brain(self):
        for currentRow in range(3):
            for currentColumn in range(2):
                self.weights[currentRow][currentColumn]