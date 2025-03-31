"""

alife.py: An animated Artificial Life Simulation

Key concepts:
- Modeling and simulation as a way of understanding complex systems
- Artificial Life: Life as it could be
- Numpy array processing!
- Animation using the matplotlib.animation library

Key life lesson: Let curiosity be your guide.

"""
import matplotlib
import random as rnd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import copy
matplotlib.use("TkAgg")

SIZE = 500  # The dimensions of the field
OFFSPRING = 2  # Max offspring when a rabbit reproduces
GRASS_RATE = 0.02  # Probability that grass grows back at any location in the next season.
POPULATION_SIZE = 25
SPEED = 2
WRAP = False

class Rabbit:
    """ A furry creature roaming a field in search of grass to eat.
    Mr. Rabbit must eat enough to reproduce, otherwise he will starve. """

    def __init__(self):
        self.x = rnd.randrange(0, SIZE)
        self.y = rnd.randrange(0, SIZE)
        self.eaten = 0

    def reproduce(self):
        """ Make a new rabbit at the same location.
         Reproduction is hard work! Each reproducing
         rabbit's eaten level is reset to zero. """
        self.eaten = 0
        return copy.deepcopy(self)

    def eat(self, amount):
        """ Feed the rabbit some grass """
        self.eaten += amount

    def move(self):
        """ Move up, down, left, right randomly """
        if WRAP:
            self.x = self.x + rnd.choice([-1, 0, 1]) % 500
            self.y = self.y + rnd.choice([-1, 0, 1]) % 500
        else:
            self.x = min(SIZE - 1, max(0, (self.x + rnd.choice([-1, 0, 1]))))
            self.y = min(SIZE - 1, max(0, (self.y + rnd.choice([-1, 0, 1]))))

class Field:
    """ A field is a patch of grass with 0 or more rabbits hopping around
    in search of grass """

    def __init__(self):
        """ Create a patch of grass with dimensions SIZE x SIZE
        and initially no rabbits """
        self.rabbits = []
        self.field = np.ones((SIZE, SIZE), dtype = int)

    def add_rabbit(self, rabbit):
        """ A new rabbit is added to the field """
        self.rabbits.append(rabbit)

    def move(self):
        """ Rabbits move """
        for r in self.rabbits:
            r.move()

    def eat(self):
        """ Rabbits eat (if they find grass where they are) """
        for r in self.rabbits:
            r.eat(self.field[r.x, r.y])
            self.field[r.x, r.y] = 0

    def survive(self):
        """ Rabbits who eat some grass live to eat another day """
        self.rabbits = [r for r in self.rabbits if r.eaten > 0]

    def reproduce(self):
        """ Rabbits reproduce like rabbits. """
        born = []
        for r in self.rabbits:
            for _ in range(rnd.randint(1,OFFSPRING)):
                born.append(r.reproduce())
            self.rabbits+=born
    def grow(self):
        """ Grass grows back with some probability """
        #growloc = (np.random.rand(SIZE, SIZE)<GRASS_RATE * 1)
        pass


    def generation(self):
        """ Run one generation of rabbits """
        self.move()
        self.eat()
        self.survive()
        self.reproduce()
        self.grow()

def animate(i, field, im):
    for _ in range(SPEED):
        field.generation()
    im.set_array(field.field())
    return im,

def main():

    # Create a field
    field = Field()

    # Then God created rabbits....
    for _ in range(25):
        field.add_rabbit(Rabbit())

    # Animate the world!
    array = np.ones(shape=(SIZE, SIZE), dtype = int)
    fig = plt.figure(figsize = (8,8))
    im = plt.imshow(array, cmap = 'PiYG', interpolation = 'hamming', vmin = 0, vmax = 1)
    anim = animation.FuncAnimation(fig, animate, fargs = (field,im), frames = 10*10, interval = 1000)
    plt.show()


if __name__ == '__main__':
    main()
