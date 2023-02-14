from solution import SOLUTION
import constants as c
import copy
import os
import pyrosim.pyrosim as pyrosim
import numpy as np
import random

class CHAIN:

    def __init__(self):
        self.chain = SOLUTION()
        self.chain.Create_World()
        self.chain.CreateRandomBot()
        

    def Simulate(self):
        self.chain.Start_Simulation("GUI")