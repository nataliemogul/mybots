# mybots

This program generates a 3D snake with a random amount of links each with random dimensions. Links with sensors are green and links without sensors are blue. Each link is randomly in either the x, y, or z direction. A visual can be seen here:

<img width="573" alt="Screenshot 2023-02-23 at 6 14 40 PM" src="https://user-images.githubusercontent.com/114442449/221060451-4109c0ea-9a85-4185-9de9-cda1e17ad9b7.png">

For the brain, motor and sensor neurons are assigned randomly

There were mutations added for this assignment. With a probability of 0.25, another link would be added to the child. This was made possible by creating a dictionary that saved all values for cubes and joints of a parent. If a mutation in the parent increased the fitness in the child, the child would replace the parent.

Run search.py to generate a random snake.

Run plot.py to generate a fitness plot.
