import pybullet as p
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy
import random
import constants as c
from simulation import SIMULATION
from world import WORLD
from robot import ROBOT
import sys

directOrGUI = sys.argv[1]
solutionID = sys.argv[2]

print("simulation.py -> ", solutionID)
simulation = SIMULATION(directOrGUI, solutionID)
simulation.Run()
simulation.Get_Fitness()