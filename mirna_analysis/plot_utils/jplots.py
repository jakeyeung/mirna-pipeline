#!/usr/local/bin/python2.7
# encoding: utf-8
'''
Functions for plotting
'''


import random
import matplotlib.pyplot as plt
import numpy as np


def jitter_values(lst, jitter=0.1):
    '''
    Add random noise to reduce overplotting
    Adapted from
    https://www.inkling.com/read/think-stats-allen-downey-1st/chapter-9/making-scatterplots-in-pyplot
    '''
    lst = [l + random.uniform(-jitter, jitter) for l in lst]
    return lst


def plot_vertical_scatter(y_values,
                          jitter=True,
                          title='Plot title',
                          xlabel='x-label',
                          ylabel='y-label',
                          draw_median=True):
    '''
    Takes as input a list of y-values to be scatterplotted.
    Includes jitter to show values

    Plots a vertical scatter. So they will all have the same x value
    '''
    x_values = [0] * len(y_values)


    if jitter:
        x_values = jitter_values(x_values)
    fig = plt.figure()
    ax = plt.axes()
    plt.scatter(x_values, y_values)
    plt.xlim([-1, 1])
    plt.ylim([-7, 7])
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    # Turn off x axis
    ax.axes.get_xaxis().set_ticks([])
    # Draw horiznotal line at median
    if draw_median:
        median_y = np.median(y_values)
        xmin = -0.2
        xmax = 0.2
        plt.hlines(median_y, xmin, xmax)
    plt.show()


