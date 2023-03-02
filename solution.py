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

        # self.numLimbs = random.randint(2,constants.maxLinks)
        # self.prev_length = random.randint(1,2)
        # self.prev_width = random.randint(1,2)
        # self.prev_height = random.randint(1,2)
        # self.directions = [1]
        # self.prev_dir = [0.5, 0, 0]

    def Start_Simulation(self, directOrGUI):
        # self.Create_Robot()
        # self.Create_Limbs(self.numLimbs)
        # self.Create_Body()
        self.Create_Dict()
        self.Create_Body()
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
        # numSensors = self.links.count(1)
        # row = random.randint(0,numSensors-1)
        # col = random.randint(0,len(self.joints)-1)
        prob = random.randint(1,4)
        if prob == 1:
            print("MUTATED")
            # self.Create_One_Limb(self.numLimbs+1, self.prev_dir, self.prev_length, self.prev_width, self.prev_height)
            self.New_Limb(self.numLinks)
            self.Create_Body()
            self.Generate_Brain()
        # self.weights[row][col] = random.random()*2-1

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
                
    # def Create_Robot(self):
    #     # pyrosim.Start_URDF("body.urdf")

    #     length=random.randint(1,2)
    #     width=random.randint(1,2)
    #     height=random.randint(1,2)

    #     prev_length = length
    #     prev_width = width
    #     prev_height = height
                
    # def Create_Limbs(self, randLinks):
    #     pyrosim.Start_URDF('body' + str(self.myID) + '.urdf')

    #     self.directions= [0 for x in range(randLinks)]
    #     self.directions[0] = 1
    #     prev_dir = [0.5, 0, 0]
    #     for i in range(1,randLinks):
    #         self.directions[i]= random.randint(1,3)
    #     self.links= [random.randint(0,1) for x in range (randLinks)]

    #     length=random.randint(1,2)
    #     width=random.randint(1,2)
    #     height=random.randint(1,2)

    #     prev_length = length
    #     prev_width = width
    #     prev_height = height

    #     ######## handling colors
    #     if self.links[0]==0:
    #         color="Blue"
    #         rgb=[0,0,1]
    #     else:
    #         color="Green"
    #         rgb=[0,1,0]
    #     ##########

    #     pyrosim.Send_Cube(name="Link0", pos=[0,0,height], size=[length, width, height], color=color, rgb=rgb)
    #     pyrosim.Send_Joint(name="Link0_Link1", parent="Link0", child="Link1", type="revolute", position=[length/2,0,height/2], jointAxis= "1 0 0")		

    #     self.joints.append("Link0_Link1")
        
    #     for i in range(1,randLinks):
    #         parentName="Link"+str(i)
    #         childName="Link"+str(i+1)
    #         length=random.uniform(1,3)
    #         width=random.uniform(1,2)
    #         height=random.uniform(1,2)

    #         if self.links[i]==0:
    #             color_name="Blue"
    #             rgb=[0,0,1]
    #         else:
    #             color_name="Green"
    #             rgb=[0,1,0]

    #         ######## handling direction
    #         if self.directions[i] == 1:
    #             #joint_position = [(prev_dir[0]+0.5)*length, prev_dir[1]*width, prev_dir[2]*height]
    #             joint_position = [length, 0, 0]
    #             cube_position = [length/2, 0, 0]
    #             prev_dir = [0.5, 0, 0]
    #             joint_direction='1 0 0'
                
    #         elif self.directions[i] == 3:
    #             # joint_position = [prev_dir[0]*width, (prev_dir[1]+0.5)*width, prev_dir[2]*width]
    #             joint_position = [(length-prev_length)/2, (prev_width+width)/2, 0]
    #             cube_position = [0, (prev_width+width)/2, 0]
    #             prev_dir = [0, 0.5, 0]
    #             joint_direction='0 1 0'

    #         elif self.directions[i] == 2:
    #             #joint_position = [prev_dir[0]*prev_height, prev_dir[1]*prev_height, (prev_dir[0]+0.5)*height]
    #             joint_position = [(length-prev_length)/2, 0, (prev_height+height)/2]
    #             cube_position = [0, 0, (prev_height+height)/2]
    #             prev_dir = [0, 0, 0.5]
    #             joint_direction='0 1 0'

    #         prev_length = length
    #         prev_width = width
    #         prev_height = height

    #         pyrosim.Send_Cube(name=parentName, pos=cube_position, size=[length, width, height], color=color_name, rgb=rgb)

    #         if i<randLinks-1: #should this be randLinks-1 or randLinks
    #             jointName= parentName+'_'+childName
    #             pyrosim.Send_Joint(name=jointName, parent=parentName, child=childName, type="revolute", position=joint_position, jointAxis= joint_direction)
    #             self.joints.append(jointName)

    #     pyrosim.End()

    # def Create_Body(self):
    #     pyrosim.Start_URDF('body' + str(self.myID) + '.urdf')
    #     height = random.uniform(1,2)
    #     pyrosim.Send_Cube(name="Link0", pos=[0,0,height], size=[random.uniform(1,2), random.uniform(1,2), height], color="Green", rgb=[0,1,0])
    #     pyrosim.Send_Joint(name="Link0_Link1", parent="Link0", child="Link1", type="revolute", position=[length/2,0,height/2], jointAxis= "1 0 0")		

    #     self.joints.append("Link0_Link1")

    #     for i in range(1,self.numLimbs):
    #         self.Create_One_Limb(i, self.prev_dir, self.prev_length, self.prev_width, self.prev_height)

    #     pyrosim.End()
    
    # def Create_One_Limb(self, parent, prev_dir, prev_length, prev_width, prev_height):
    #     parentName="Link"+str(parent)
    #     childName="Link"+str(parent+1)

    #     length=random.uniform(1,3)
    #     width=random.uniform(1,2)
    #     height=random.uniform(1,2)
    #     new_link= random.randint(0,1)
    #     self.links.append(new_link)
    #     new_dir = random.randint(1,3)
    #     self.directions.append(new_dir)

    #     if new_link==0:
    #         color_name="Blue"
    #         rgb=[0,0,1]
    #     else:
    #         color_name="Green"
    #         rgb=[0,1,0]

    #     ######## handling direction
    #     if self.directions[i] == 1:
    #         joint_position = [length, 0, 0]
    #         cube_position = [length/2, 0, 0]
    #         self.prev_dir = [0.5, 0, 0]
    #         joint_direction='1 0 0'
            
    #     elif self.directions[i] == 3:
    #         joint_position = [(length-prev_length)/2, (prev_width+width)/2, 0]
    #         cube_position = [0, (prev_width+width)/2, 0]
    #         self.prev_dir = [0, 0.5, 0]
    #         joint_direction='0 1 0'

    #     elif self.directions[i] == 2:
    #         joint_position = [(length-prev_length)/2, 0, (prev_height+height)/2]
    #         cube_position = [0, 0, (prev_height+height)/2]
    #         self.prev_dir = [0, 0, 0.5]
    #         joint_direction='0 1 0'

    #     jointName= parentName+'_'+childName
    #     pyrosim.Send_Joint(name=jointName, parent=parentName, child=childName, type="revolute", position=joint_position, jointAxis= joint_direction)
    #     self.joints.append(jointName)

    #     self.prev_length = length
    #     self.prev_width = width
    #     self.prev_height = height

    #     pyrosim.Send_Cube(name=parentName, pos=cube_position, size=[length, width, height], color=color_name, rgb=rgb)

    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")
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
