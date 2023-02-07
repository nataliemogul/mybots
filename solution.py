import numpy
import os
import pyrosim.pyrosim as pyrosim
import random
import time
import constants

class SOLUTION:
    def __init__(self, nextAvailableID):
        self.weights = numpy.random.rand(3,2)*2-1
        self.myID = nextAvailableID

    def Start_Simulation(self, directOrGUI):
        self.Create_Robot()
        self.Generate_Brain()
        systemCommand = "python3 simulate.py " + directOrGUI + " " + str(self.myID) + " 2&>1 &"
        os.system(systemCommand)

    def Wait_For_Simulation_To_End(self):
        fitnessFile = "fitness" + str(self.myID) + ".txt"
        while not os.path.exists(fitnessFile):
            time.sleep(0.01)

        file = open(fitnessFile, "r")
        self.fitness = float(file.read())
        file.close()
        # print(self.fitness)
        os.system("rm " + fitnessFile)

    def Set_ID(self, newID):
        self.myID = newID

    def Get_Fitness(self):
        return self.fitness  

    def Mutate(self):
        row = random.randint(0,constants.numSensorNeurons-1)
        col = random.randint(0,constants.numMotorNeurons-1)
        self.weights[row, col] = random.random()*2-1

    @staticmethod
    def Create_World():
        pyrosim.Start_SDF("world.sdf")
        #pyrosim.Send_Cube(name="Box", pos=[2, 2, 0.5] , size=[1, 1, 1])
        pyrosim.End()

    @staticmethod
    def Create_Robot():
        pyrosim.Start_URDF("body.urdf")
        pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1] , size=[2, 1, 0.2])

        pyrosim.Send_Joint(name = "Torso_Neck", parent= "Torso", child = "Neck", type = "revolute", position = [0, -0.5, 1], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="Neck", pos=[1, 0.5, 0.5] , size=[0.2, 0.2, 1])
        pyrosim.Send_Joint(name = "Neck_Head", parent= "Neck", child = "Head", type = "revolute", position = [0, -1, 0], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="Head", pos=[1.2, 1.5, 1.2] , size=[0.5, 0.5, 0.5])
        
        pyrosim.Send_Joint(name = "Torso_BackLeg", parent= "Torso", child = "BackLeg", type = "revolute", position = [0, -0.5, 1], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="BackLeg", pos=[0, -0.5, 0] , size=[0.2, 1, 0.2])
        pyrosim.Send_Joint(name = "BackLeg_LowerBackLeg", parent= "BackLeg", child = "LowerBackLeg", type = "revolute", position = [0, -1, 0], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="LowerBackLeg", pos=[0, 0, -0.5] , size=[0.2, 0.2, 1])

        pyrosim.Send_Joint(name = "Torso_FrontLeg", parent= "Torso", child = "FrontLeg", type = "revolute", position = [0, 0.5, 1], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="FrontLeg", pos=[0, 0.5, 0] , size=[0.2, 1, 0.2])
        pyrosim.Send_Joint(name = "FrontLeg_LowerFrontLeg", parent= "FrontLeg", child = "LowerFrontLeg", type = "revolute", position = [0, 1, 0], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="LowerFrontLeg", pos=[0, 0, -0.5] , size=[0.2, 0.2, 1])

        pyrosim.Send_Joint(name = "Torso_LeftLeg", parent= "Torso", child = "LeftLeg", type = "revolute", position = [-0.5, 0, 1], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="LeftLeg", pos=[-0.5, 0, 0] , size=[1, 0.2, 0.2])
        pyrosim.Send_Joint(name = "LeftLeg_LowerLeftLeg", parent= "LeftLeg", child = "LowerLeftLeg", type = "revolute", position = [-1, 0, 0], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="LowerLeftLeg", pos=[0, 0, -0.5] , size=[0.2, 0.2, 1])

        pyrosim.Send_Joint(name = "Torso_RightLeg", parent= "Torso", child = "RightLeg", type = "revolute", position = [0.5, 0, 1], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="RightLeg", pos=[0.5, 0, 0] , size=[1, 0.2, 0.2])
        pyrosim.Send_Joint(name = "RightLeg_LowerRightLeg", parent= "RightLeg", child = "LowerRightLeg", type = "revolute", position = [1, 0, 0], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="LowerRightLeg", pos=[0, 0, -0.5] , size=[0.2, 0.2, 1])

        pyrosim.End()
    
    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")

        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
        pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "BackLeg")
        pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "FrontLeg")

        sensorLinkNames = ["LowerBackLeg", "LowerFrontLeg", "LowerLeftLeg", "LowerRightLeg"]
        motorJointNames = ["Torso_BackLeg", "Torso_FrontLeg", "Torso_LeftLeg", "Torso_RightLeg", "BackLeg_LowerBackLeg", "FrontLeg_LowerFrontLeg", "LeftLeg_LowerLeftLeg", "RightLeg_LowerRightLeg"]
        
        for i in range(constants.numSensorNeurons):
            pyrosim.Send_Sensor_Neuron(name = i , linkName = sensorLinkNames[i])

        for j in range(constants.numMotorNeurons):
            pyrosim.Send_Motor_Neuron(name = j+constants.numSensorNeurons, jointName = motorJointNames[j])

        for currentRow in range(constants.numSensorNeurons):
            for currentColumn in range(constants.numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName = currentRow,
                                    targetNeuronName = currentColumn+3, 
                                    weight = self.weights[currentRow][currentColumn])

        pyrosim.End()