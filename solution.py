import numpy
import os
import pyrosim.pyrosim as pyrosim
import random
import time
import constants

class SOLUTION:
    def __init__(self, nextAvailableID = 0):
        self.weights = 0
        self.myID = nextAvailableID
        self.links = []
        self.joints = []

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
        numSensors = self.links.count(1)
        row = random.randint(0,numSensors-1)
        col = random.randint(0,len(self.joints)-1)
        self.weights[row][col] = random.random()*2-1

    def Create_World():
        pyrosim.Start_SDF("world.sdf")
        pyrosim.End()
                
    def Create_Robot(self):
        pyrosim.Start_URDF("body.urdf")
		
        length=random.randint(1,2)
        width=random.randint(1,2)
        height=random.randint(1,2)
        
        randLinks= random.randint(2,constants.maxLinks)
        
        self.links= [random.randint(0,1) for x in range (randLinks)]
        
        if self.links[0]==0:
            color="Blue"
            rgb=[0,0,1]
        else:
            color="Green"
            rgb=[0,1,0]

        pyrosim.Send_Cube(name="Link0", pos=[0,0,height/2], size=[length, width, height], color=color, rgb=rgb)

        pyrosim.Send_Joint(name="Link0_Link1", parent="Link0", child="Link1", type="revolute", position=[0,width/-2,0.5], jointAxis= "1 0 0")		
        
        self.joints.append("Link0_Link1")
        
        for i in range(1,randLinks):
            parentName="Link"+str(i)
            childName="Link"+str(i+1)
            length=random.randint(1,3)
            width=random.randint(1,2)
            height=random.randint(1,2)

            if self.links[i]==0:
                color_name="Blue"
                rgb=[0,0,1]
            else:
                color_name="Green"
                rgb=[0,1,0]

            pyrosim.Send_Cube(name=parentName, pos=[0,0,height/2], size=[length, width, height], color=color, rgb=rgb)
            
            if i<randLinks-1:
                jointName= parentName+'_'+childName
                pyrosim.Send_Joint(name=jointName, parent=parentName, child=childName, type="revolute", position=[0,width/-1,0.5], jointAxis= "1 0 0")
                self.joints.append(jointName)
                
        pyrosim.End()

    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")
        numSensors = self.links.count(1)
        self.weights = numpy.random.rand(numSensors,len(self.joints)) * 2 - 1

        i=0
        for link in self.links:
            if link == 1: #has sensor
                pyrosim.Send_Sensor_Neuron(name = i, linkName = "Link"+str(i))
                i +=1

        for joint in self.joints:
            pyrosim.Send_Motor_Neuron(name = i, jointName = joint)
            i += 1

        for currRow in range(numSensors):
            for currColumn in range(len(self.joints)):
                pyrosim.Send_Synapse(sourceNeuronName = currRow, 
					targetNeuronName = currColumn + numSensors, 
					weight = self.weights[currRow][currColumn] )
                    
        pyrosim.End()
