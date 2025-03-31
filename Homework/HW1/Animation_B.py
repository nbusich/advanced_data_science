"""
File: Animation_a.py
Description: Image animation example.
"""
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
matplotlib.use("TkAgg")

FIGSIZE = 8 # The size of the image 8 inches by 8 inches
SIZE = 10 # Array is of size 10x10

def animate_func(i, *fargs):
    im = fargs[0]
    im.set_array(np.random.rand(SIZE,SIZE))
    return im,


def main():

    # Initialize the first frame
    fig = plt.figure(figsize= (FIGSIZE, FIGSIZE), )
    arr = np.random.rand(SIZE,SIZE)
    im = plt.imshow(arr, interpolation = 'none')

    # Configure the animation
    anim = animation.FuncAnimation(
        fig,
        animate_func,
        fargs = (im,),
        frames = 10 ** 100,
        interval = 1000,
        repeat = True
    )
    plt.show()

if __name__ == '__main__':
    main()


