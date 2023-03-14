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
        self.links = [1]
        self.joints = []

        self.cube = {}
        self.joint = {}
        self.numLinks = random.randint(2,constants.maxLinks)

    def Start_Simulation(self, directOrGUI):
        self.Create_Dict()
        self.Create_Body()
        self.Generate_Brain()
        systemCommand = "python3 simulate.py " + directOrGUI + " " + str(self.myID) + " 2&>1 &"
        os.system(systemCommand)

    def Wait_For_Simulation_To_End(self):
        fitnessFile = "fitness" + str(self.myID) + ".txt"
        while not os.path.exists(fitnessFile):
            time.sleep(0.1)

        file = open(fitnessFile, "r")
        self.fitness = float(file.read())
        file.close()

    def Set_ID(self, newID):
        self.myID = newID

    def Get_Fitness(self):
        return self.fitness  

    def Mutate(self):
        os.system('rm brain*.nndf')
        os.system('rm body*.urdf')
        os.system('rm fitness*.txt')
        prob = random.randint(1,4)
        if prob == 1:
            self.New_Limb(self.numLinks)
            self.Create_Body()
            self.Generate_Brain()

    def Create_World():
        pyrosim.Start_SDF("world.sdf")
        pyrosim.End()

    def Create_Dict(self):
        height = random.randint(1,2)
        self.cube[0] = ["Link0", [0,0,height], [random.randint(1,2), random.randint(1,2), height], "Green", [0,1,0], [0.5, 0, 0]]
        for i in range(1, self.numLinks):
            length=random.randint(1,2)
            width=random.randint(1,2)
            height=random.randint(1,2)

            newLink = random.randint(0,1)
            self.links.append(newLink)

            ######## handling colors
            if newLink==0:
                color="Blue"
                rgb=[0,0,1]
            else:
                color="Green"
                rgb=[0,1,0]
            ##########

            ######## handling direction
            new_dir = random.randint(1,3)

            prev_length = self.cube[i-1][1][0]
            prev_width = self.cube[i-1][1][1]
            prev_height = self.cube[i-1][1][2]

            if new_dir == 1:
                joint_position = [length, 0, 0]
                cube_position = [length/2, 0, 0]
                prev_dir = [0.5, 0, 0]
                joint_direction='1 0 0'
                
            elif new_dir == 3:
                joint_position = [(length-prev_length)/2, (prev_width+width)/2, 0]
                cube_position = [0, (prev_width+width)/2, 0]
                prev_dir = [0, 0.5, 0]
                joint_direction='0 1 0'

            elif new_dir == 2:
                joint_position = [(length-prev_length)/2, 0, (prev_height+height)/2]
                cube_position = [0, 0, (prev_height+height)/2]
                prev_dir = [0, 0, 0.5]
                joint_direction='0 1 0'
            ##########
            self.cube[i] = ["Link"+ str(i), cube_position, [length, width, height], color, rgb]
            self.joint[i] = ["Link"+ str(i-1)+'_'+"Link"+ str(i), "Link"+ str(i-1), "Link"+ str(i), joint_position, joint_direction]

    def Create_Body(self):
        pyrosim.Start_URDF('body' + str(self.myID) + '.urdf')
        for i in range(self.numLinks):
            pyrosim.Send_Cube(name=self.cube[i][0], pos=self.cube[i][1], size=self.cube[i][2], color=self.cube[i][3], rgb=self.cube[i][4])
            if i+1<self.numLinks:
                pyrosim.Send_Joint(name=self.joint[i+1][0], parent=self.joint[i+1][1], child=self.joint[i+1][2], type="revolute", position=self.joint[i+1][3], jointAxis= self.joint[i+1][4])
        pyrosim.End()
        
    def New_Limb(self,i):
        length=random.randint(1,2)
        width=random.randint(1,2)
        height=random.randint(1,2)

        newLink = random.randint(0,1)

        ######## handling colors
        if newLink==0:
            color="Blue"
            rgb=[0,0,1]
        else:
            color="Green"
            rgb=[0,1,0]
        ##########

        ######## handling direction
        new_dir = random.randint(1,3)

        prev_length = self.cube[i-1][1][0]
        prev_width = self.cube[i-1][1][1]
        prev_height = self.cube[i-1][1][2]

        if new_dir == 1:
            joint_position = [length, 0, 0]
            cube_position = [length/2, 0, 0]
            prev_dir = [0.5, 0, 0]
            joint_direction='1 0 0'
            
        elif new_dir == 3:
            joint_position = [(length-prev_length)/2, (prev_width+width)/2, 0]
            cube_position = [0, (prev_width+width)/2, 0]
            prev_dir = [0, 0.5, 0]
            joint_direction='0 1 0'

        elif new_dir == 2:
            joint_position = [(length-prev_length)/2, 0, (prev_height+height)/2]
            cube_position = [0, 0, (prev_height+height)/2]
            prev_dir = [0, 0, 0.5]
            joint_direction='0 1 0'
        ##########

        self.cube[i] = ["Link"+ str(i), cube_position, [length, width, height], color, rgb]
        self.joint[i] = ["Link"+ str(i-1)+'_'+"Link"+ str(i), "Link"+ str(i-1), "Link"+ str(i), joint_position, joint_direction]
        
        self.numLinks += 1

    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")
        self.weights = numpy.random.rand(len(self.links),len(self.joints)) * 2 - 1

        i = 0 
        while i < len(self.links):
            pyrosim.Send_Sensor_Neuron(name = i, linkName = "Link" + str(self.links[i]))
            i += 1
        
        while i < len(self.joints):
            pyrosim.Send_Motor_Neuron(name = motorcount, jointName = self.joints[i])
            i += 1

        for currentRow in range(len(self.links)):        
            for currentColumn in range(len(self.joints)):
                pyrosim.Send_Synapse(sourceNeuronName = currentRow, targetNeuronName = currentColumn + len(self.links), weight = self.weights[currentRow][currentColumn])

        pyrosim.End()