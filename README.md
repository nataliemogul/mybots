# mybots

**Methods**

I was really struggling with my code up until 3 days before the project was due, when I changed a line in my generate_brain function and I was finally able to evolve. Unfortunately due to my inability to fix this bug sooner, even though my robot does not follow a presupposed size and shape or number and shape of limbs, it does not follow the laws of physics since I did not perfect the connections of the joints and cubes. My code is mainly in the solution.py. I begin by initializing a dictionary of cubes and joints. I need to make a dictionary to store these items so that I don’t “forget” the parent, or re-randomize even if the parent is more fit than the child. For the brain, motor and sensor neurons are assigned randomly. Links with a sensor are green and those without are blue. My mutations are adding a new limb to either the positive x, negative x, or z directions, code for this can be found in new_limb. A figure for this can be seen here:

<img width="573" alt="Screenshot 2023-02-23 at 6 14 40 PM" src="https://user-images.githubusercontent.com/114442449/221060451-4109c0ea-9a85-4185-9de9-cda1e17ad9b7.png">

The figure shows randomized direction and shape. I mutate 25 percent of the time. My parallel hill climber works by picking the robot that moves the most in the x direction. You can run it by calling python search.py. You can get a plot by running python plot.py. You can get any of the final 10 evolved creatures by running python simulate.py GUI <5000-5009>. 

**Results**

Clearly my results were doing what I wanted them to based on the graph seen in Figure 1. I find it interesting that most of the evolution happened in the first 50 generations (out of 500). I think that if my joints were properly made the evolution would be much more insightful and easier to analyze. I think that since there were possible robots that started below ground and shot up, this affected their fitness. I also find it interesting that the final 10 robots were so different (see video). Certain lineages barely evolved after the 100 generation point (see light green, pink, and red lines in Figure 1). 

<img width="642" alt="FINAL PROJECT" src="https://user-images.githubusercontent.com/114442449/225150777-919212f6-398d-4228-ae5b-aba8f6bda524.png">

**GIF**

https://user-images.githubusercontent.com/114442449/225151925-f711b34f-27a3-49fc-b1d2-a7e3eb9a2a7a.mov

**2 minute video link**

https://youtu.be/egaZslYeyEA

**Sources:**
Evolving Virtual Creatures by Karl Sims (https://www.karlsims.com/papers/siggraph94.pdf)
Ludobots MOOC on Reddit (https://www.reddit.com/r/ludobots/)
