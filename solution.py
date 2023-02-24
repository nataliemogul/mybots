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

        prev_length = length
        prev_width = width
        prev_height = height
        
        randLinks= random.randint(2,constants.maxLinks)
        
        self.directions= [0 for x in range(randLinks)]
        self.directions[0] = 1
        prev_dir = [0.5, 0, 0]
        for i in range(1,randLinks):
            # while self.directions[i] == 0 or (self.directions[i] == 1 and self.directions[i-1] == 2) or \
            # (self.directions[i] == 2 and self.directions[i-1] == 1) or (self.directions[i] == 3 and self.directions[i-1] == 4) or \
            # (self.directions[i] == 4 and self.directions[i-1] == 3) or (self.directions[i] == 5 and self.directions[i-1] == 6) or \
            # (self.directions[i] == 6 and self.directions[i-1] == 5):
            self.directions[i]= random.randint(1,3)
            #self.directions[i]= 1
        print(self.directions)
        self.links= [random.randint(0,1) for x in range (randLinks)]
        
        ######## handling colors
        if self.links[0]==0:
            color="Blue"
            rgb=[0,0,1]
        else:
            color="Green"
            rgb=[0,1,0]
        ##########

        pyrosim.Send_Cube(name="Link0", pos=[0,0,height], size=[length, width, height], color=color, rgb=rgb)
        pyrosim.Send_Joint(name="Link0_Link1", parent="Link0", child="Link1", type="revolute", position=[length/2,0,height/2], jointAxis= "1 0 0")		
        
        print("first cube position:", [0,0,height/2], "first joint position:", [length/2,0,height/2])
        print("first cube size:", [length, width, height])

        self.joints.append("Link0_Link1")
        
        for i in range(1,randLinks):
            parentName="Link"+str(i)
            childName="Link"+str(i+1)
            length=random.uniform(1,3)
            width=random.uniform(1,2)
            height=random.uniform(1,2)

            if self.links[i]==0:
                color_name="Blue"
                rgb=[0,0,1]
            else:
                color_name="Green"
                rgb=[0,1,0]

            ######## handling direction
            # if self.directions[i] == 1: #x, pos
            #     cube_position=[length/2, 0, 0]
            #     if prev_dir == 1 or prev_dir == 2:
            #         joint_position=[length,0, 0]
            #     elif prev_dir == 3: #y, pos
            #         joint_position = [prev_length/2, prev_width/2, 0]
            #     elif prev_dir == 4: #y, neg
            #         joint_position = [prev_length/2, -prev_width/2, 0]
            #     elif prev_dir == 5: #z, pos
            #         joint_position = [prev_length/2, 0, prev_height/2]
            #     else: #z, neg
            #         joint_position = [prev_length/2, 0, -prev_height/2]

            #     prev_dir = 1
            #     joint_direction='1 0 0'

            # elif self.directions[i] == 2: #x, neg
            #     cube_position=[-length/2, 0, 0]
            #     if prev_dir == 1 or prev_dir == 2:
            #         joint_position=[-length,0, 0]
            #     elif prev_dir == 3: #y, pos
            #         joint_position = [-prev_length/2, prev_width/2, 0]
            #     elif prev_dir == 4: #y, neg
            #         joint_position = [-prev_length/2, -prev_width/2, 0]
            #     elif prev_dir == 5: #z, pos
            #         joint_position = [-prev_length/2, 0, prev_height/2]
            #     else: #z, neg
            #         joint_position = [-prev_length/2, 0, -prev_height/2]
            #     prev_dir = 2
            #     joint_direction='1 0 0'

            # elif self.directions[i] == 3: #y, pos
            #     cube_position=[0, width/2,0]

            #     if prev_dir == 3 or prev_dir == 4:
            #         joint_position=[0,width, 0]
            #     elif prev_dir == 1: #x, pos
            #         joint_position = [prev_length/2, prev_width/2, 0]
            #     elif prev_dir == 2: #x, neg
            #         joint_position = [-prev_length/2, prev_width/2, 0]
            #     elif prev_dir == 5: #z, pos
            #         joint_position = [0, prev_width/2, prev_height/2]
            #     else: #z, neg
            #         joint_position = [0, prev_width/2, -prev_height/2]
            #     prev_dir = 3
            #     joint_direction='0 1 0'

            # elif self.directions[i] == 4: #y, neg
            #     cube_position=[0, -width/2,0]
            #     if prev_dir == 3 or prev_dir == 4:
            #         joint_position=[0,-width, 0]
            #     elif prev_dir == 1: #x, pos
            #         joint_position = [-prev_length/2, prev_width/2, 0]
            #     elif prev_dir == 2: #x, neg
            #         joint_position = [-prev_length/2, -prev_width/2, 0]
            #     elif prev_dir == 5: #z, pos
            #         joint_position = [0, prev_width/2, prev_height/2]
            #     else: #z, neg
            #         joint_position = [0, -prev_width/2, prev_height/2]
                
            #     prev_dir = 4
            #     joint_direction='0 1 0'
            # elif self.directions[i] == 5: #z, pos
            #     cube_position=[0, 0, height/2]
                
            #     if prev_dir == 5 or prev_dir == 6:
            #         joint_position=[0,0, height]
            #     elif prev_dir == 1: #x, pos
            #         joint_position = [prev_length/2, 0, prev_height/2]
            #     elif prev_dir == 2: #x, neg
            #         joint_position = [-prev_length, 0, prev_height/2]
            #     elif prev_dir == 3: #y, pos
            #         joint_position = [0, prev_width/2, prev_height/2]
            #     else: #y, neg
            #         joint_position = [0, -prev_width/2, prev_height/2]

            #     prev_dir = 5
            #     joint_direction='1 0 0'

            # # else:
                
            # #     cube_position=[0, 0, -height/2]
                
            # #     if prev_dir == 5 or prev_dir == 6:
            # #         joint_position=[0,0, -height]
            # #     elif prev_dir == 1: #x, pos
            # #         joint_position = [prev_length/2, 0, -prev_height/2]
            # #     elif prev_dir == 2: #x, neg
            # #         joint_position = [-prev_length, 0, -prev_height/2]
            # #     elif prev_dir == 3: #y, pos
            # #         joint_position = [0, -prev_width/2, -prev_height/2]
            # #     else: #y, neg
            # #         joint_position = [0, prev_width/2, -prev_height/2]

            # #     prev_dir = 6
            # #     joint_direction='1 0 0'

            if self.directions[i] == 1:
                #joint_position = [(prev_dir[0]+0.5)*length, prev_dir[1]*width, prev_dir[2]*height]
                joint_position = [length, 0, 0]
                cube_position = [length/2, 0, 0]
                prev_dir = [0.5, 0, 0]
                joint_direction='1 0 0'
                
            elif self.directions[i] == 3:
                # joint_position = [prev_dir[0]*width, (prev_dir[1]+0.5)*width, prev_dir[2]*width]
                joint_position = [(length-prev_length)/2, (prev_width+width)/2, 0]
                cube_position = [0, (prev_width+width)/2, 0]
                prev_dir = [0, 0.5, 0]
                joint_direction='0 1 0'

            elif self.directions[i] == 2:
                #joint_position = [prev_dir[0]*prev_height, prev_dir[1]*prev_height, (prev_dir[0]+0.5)*height]
                joint_position = [(length-prev_length)/2, 0, (prev_height+height)/2]
                cube_position = [0, 0, (prev_height+height)/2]
                prev_dir = [0, 0, 0.5]
                joint_direction='0 1 0'

            
            if i < 3:
                print("cube position", cube_position, "joint", joint_position)
                print("cube size", [length, width, height])
                #print(prev_length, prev_width, prev_height)

            prev_length = length
            prev_width = width
            prev_height = height

            pyrosim.Send_Cube(name=parentName, pos=cube_position, size=[length, width, height], color=color_name, rgb=rgb)
                

            if i<randLinks-1:
                jointName= parentName+'_'+childName
                pyrosim.Send_Joint(name=jointName, parent=parentName, child=childName, type="revolute", position=joint_position, jointAxis= joint_direction)
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
