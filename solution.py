import numpy
import os
import pyrosim.pyrosim as pyrosim
import random

class SOLUTION:
    def __init__(self):
        self.weights = numpy.random.rand(3,2)*2-1

    def Evaluate(self, directOrGUI):
        self.Create_World()
        self.Create_Robot()
        self.Generate_Brain()
        os.system("python3 simulate.py " + directOrGUI)

        file = open("fitness.txt", "r")
        self.fitness = float(file.read())
        file.close()

    def Mutate(self):
        row = random.randint(0,2)
        col = random.randint(0,1)
        self.weights[row, col] = random.random()*2-1

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[2, 2, 0.5] , size=[1, 1, 1])
        pyrosim.End()

    def Create_Robot(self):
        pyrosim.Start_URDF("body.urdf")
        pyrosim.Send_Cube(name="Torso", pos=[1.5,0,1.5] , size=[1, 1, 1])
        pyrosim.Send_Joint(name = 'Torso_BackLeg', parent= "Torso", child = "BackLeg", type = "revolute", position = [1,0,1])
        pyrosim.Send_Cube(name="BackLeg", pos=[-0.5,0,-0.5] , size=[1, 1, 1])
        pyrosim.Send_Joint(name ="Torso_FrontLeg", parent= "Torso", child = "FrontLeg", type = "revolute", position = [2,0,1])
        pyrosim.Send_Cube(name="FrontLeg", pos=[0.5,0,-0.5] , size=[1, 1, 1])
        pyrosim.End()
    
    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork("brain.nndf")

        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
        pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "BackLeg")
        pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "FrontLeg")

        pyrosim.Send_Motor_Neuron(name = 3 , jointName = "Torso_BackLeg")
        pyrosim.Send_Motor_Neuron(name = 4 , jointName = "Torso_FrontLeg")


        for currentRow in range(3):
            for currentColumn in range(2):
                pyrosim.Send_Synapse(sourceNeuronName = currentRow,
                                    targetNeuronName = currentColumn+3, 
                                    weight = self.weights[currentRow][currentColumn])

        pyrosim.End()