import pyrosim.pyrosim as pyrosim
import random

length = 1
width = 1
height = 1
x = 0
y = 0
z = 0.5

def Create_World():
    pyrosim.Start_SDF("world.sdf")
    pyrosim.Send_Cube(name="Box", pos=[x,y,z] , size=[length, width, height])
    pyrosim.End()

def Create_Robot():
    pyrosim.Start_URDF("body.urdf")
    y_orientation=0
    shape_length=0
    randLinks= random.randint(2, 10)
    
    pyrosim.Send_Cube(name="Head" , pos=[0.5,0,0.5] , size=[0.02,0.5,0.2], rgb=[1,0,1])
    pyrosim.End()

def Generate_Brain():
    pyrosim.Start_NeuralNetwork("brain.nndf")
    pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
    pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "BackLeg")
    pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "FrontLeg")
    pyrosim.Send_Motor_Neuron( name = 3 , jointName = 'Torso_BackLeg')
    pyrosim.Send_Motor_Neuron( name = 4 , jointName = "Torso_FrontLeg")

    for neuron in range(3):
        for motor in range(3, 5):
            pyrosim.Send_Synapse( sourceNeuronName = neuron , targetNeuronName = motor , weight = (random.random()*2-1) )
    pyrosim.End()

Create_World()
Create_Robot()
#Generate_Brain()