"""
File: Animation_a.py
Description: Simple line plotting animation.
"""
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
matplotlib.use("TkAgg")

# Create a figure and axes and line plot
fig, ax = plt.subplots()
plt.grid()
xdata, ydata = [],[]
line, = plt.plot(xdata, ydata, 'ro') # Returns a tuple of line2d objects


def init():
    """ Initializing an empty plot """
    ax.set_xlim(0, 2*np.pi)
    ax.set_ylim(-1, 1)
    line.set_data([],[])
    return line,
# Define an update function which func_animation will call repeatedly
def update(frame):
    xdata.append(frame)
    ydata.append(np.sin(frame))
    line.set_data(xdata, ydata)
    return line,

# Create the animation then run it
anim = FuncAnimation(fig,
                          update,
                          frames = np.linspace(0, 2*np.pi, 180),
                          init_func = init,
                          blit = True,
                          interval = 50
                          )
plt.show()