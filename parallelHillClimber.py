from solution import SOLUTION
import copy
import constants
import pyrosim.pyrosim as pyrosim
import os

class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        os.system("rm brain*.nndf")
        os.system("rm fitness*.txt")

        self.parents = {}
        self.nextAvailableID = 0

        SOLUTION.Create_World()
        SOLUTION.Create_Robot()

        for i in range(constants.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1

    def Evolve(self):
        self.Evaluate(self.parents)

        for currentGeneration in range(constants.numberOfGenerations):
            self.Evolve_For_One_Generation()

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        self.Print()
        self.Select()
    
    def Evaluate(self, solutions):
        for solution in solutions:
            solutions[solution].Start_Simulation("DIRECT")

        for solution in solutions:
            solutions[solution].Wait_For_Simulation_To_End()

    def Spawn(self):
        self.children = {}
        for parent in self.parents:
            self.children[parent] = copy.deepcopy(self.parents[parent])
            self.children[parent].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1

    def Mutate(self):
        for child in self.children:
            self.children[child].Mutate()

    def Select(self):
        for child in self.children:
            if self.parents[child].Get_Fitness() > self.children[child].Get_Fitness():
                self.parents[child] = self.children[child]

    def Print(self):
        print()
        for parent in self.parents:
            print("Parent: ", self.parents[parent].Get_Fitness(), " Child: ", self.children[parent].Get_Fitness())
        print()

    def Show_Best(self):
        best_parent_key = "None"
        best_fitness = 1000000
        for parent in self.parents:
            parent_fitness = self.parents[parent].Get_Fitness()
            if parent_fitness < best_fitness:
                best_fitness = parent_fitness
                best_parent = parent

        self.parents[best_parent].Start_Simulation("GUI")
        print("Best fitness: ", best_fitness)

