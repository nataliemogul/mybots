import constants as c
import numpy
import pyrosim.pyrosim as pyrosim
import pybullet as p

class MOTOR:
    def __init__(self, jointName):
        self.jointName = jointName
        self.Prepare_To_Act()

    def Prepare_To_Act(self):
        self.amplitude = numpy.pi/4
        self.frequency = 10
        self.phaseOffset = 0

        if (self.jointName == b"Torso_FrontLeg"): 
            self.frequency = c.frequency_back/2

        self.targetAngles = numpy.linspace(0, 2*numpy.pi, 1000)
        self.motorValues = self.amplitude/2 * numpy.sin(self.frequency * self.targetAngles + self.phaseOffset)

    def Set_Value(self, i, robotId):
        pyrosim.Set_Motor_For_Joint(
                bodyIndex = robotId, 
                jointName = self.jointName, 
                controlMode = p.POSITION_CONTROL, 
                targetPosition = self.motorValues[i], 
                maxForce = 50)

    def Save_Values(self):
        file = "data/" + self.jointName + "MotorValues.npy"
        numpy.save(file, self.motorValues)
