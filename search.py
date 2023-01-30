import os
from hillclimber import HILL_CLIMBER

#os.system("python3 generate.py")
#os.system("python3 simulate.py")

hc = HILL_CLIMBER()
hc.Evolve()
hc.Show_Best()