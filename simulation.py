from world import WORLD
from robot import ROBOT
from sensor import SENSOR
import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy
import time


class SIMULATION:
    def __init__(self):
        self.physicsClient = p.connect(p.GUI)
        self.world = WORLD()
        self.robot = ROBOT()
        p.setGravity(0,0,-9.8)

    def Run(self):
        for i in range(1000):
            p.stepSimulation()
            self.robot.Sense(i)
        #     pyrosim.Set_Motor_For_Joint(
        #         bodyIndex = robotId, 
        #         jointName = b"Torso_BackLeg", 
        #         controlMode = p.POSITION_CONTROL, 
        #         targetPosition = c.targetAngles_back[i], 
        #         maxForce = 50)
        #     pyrosim.Set_Motor_For_Joint(
        #         bodyIndex = robotId, 
        #         jointName = b"Torso_FrontLeg", 
        #         controlMode = p.POSITION_CONTROL, 
        #         targetPosition = c.targetAngles_front[i], 
        #         maxForce = 50)
            time.sleep(0.01)

    def __del__(self):
        p.disconnect()