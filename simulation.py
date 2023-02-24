from world import WORLD
from robot import ROBOT
from sensor import SENSOR
import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy
import time
import constants


class SIMULATION:
    def __init__(self, directOrGUI, solutionID):
        self.runType = directOrGUI
        if self.runType == "DIRECT":
            self.physicsClient = p.connect(p.DIRECT)
        else:
            self.physicsClient = p.connect(p.GUI)
            p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
        self.world = WORLD()
        self.robot = ROBOT(solutionID)
        p.setGravity(0,0,-9.8)

    def Run(self):
        for i in range(10000):
            p.stepSimulation()
            self.robot.Sense(i)
            self.robot.Think()
            self.robot.Act()

        if self.runType == "GUI":
                time.sleep(constants.sleep)

    def __del__(self):
        p.disconnect()

    def Get_Fitness(self):
        self.robot.Get_Fitness()