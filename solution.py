import numpy
import os
import pyrosim.pyrosim as pyrosim

class SOLUTION:
    def __init__(self):
        self.weights = numpy.random.rand(3,2)*2-1

    def Evaluate(self):
        self.Create_World()
        self.Create_Robot()
        self.Generate_Brain()
        os.system("python simulate.py")

    def Create_World(self):
        pass

    def Create_Robot(self):
        pass
    
    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork("brain.nndf")
        for currentRow in range(3):
            for currentColumn in range(2):
                self.weights[currentRow][currentColumn]