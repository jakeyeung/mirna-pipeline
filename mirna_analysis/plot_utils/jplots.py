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


def is_list_of_lists(input_list):
    '''
    Check if list contains list inside
    '''
    return any(isinstance(el, list) for el in input_list)


def frange(x, y, jump):
    '''
    Create range, but jumps are floats.
    '''
    if jump == 0:
        print 'Warning: incrementing by %s results in infinite loop.' % jump
        sys.exit()
    while x <= y:
        yield x
        x += jump


def get_x_values_for_scatter(y_values, xlim_min, xlim_max):
    '''
    We want scatterplot to plot arbitrary number of vectors
    of y-values. The x-values should be assigned such that they
    are evenly spaced amongst the plot.
    '''
    x_values = []

    n_vectors = len(y_values)

    size_yvals = len(y_values[0])

    increment = float((xlim_max - xlim_min)) / (n_vectors + 1.)

    for xval in frange(xlim_min + increment, xlim_max - increment, increment):
        x_values.append([xval] * size_yvals)

    return x_values


def plot_vertical_scatter(y_values,
                          jitter=True,
                          title='Plot title',
                          xlabel='x-label',
                          ylabel='y-label',
                          draw_median=True):
    '''
    Takes as input a list of y-values to be scatterplotted.

    Can be a list of lists or just a single list

    Includes jitter to show values

    Plots a vertical scatter. So they will all have the same x value
    '''
    xlim_min = -1
    xlim_max = 1
    hline_radius = 0.2    # half of horizontal line to be drawn

    # check if list of lists, if it is not, make it a list of list
    if not is_list_of_lists(y_values):
        y_values = [y_values]

    # Create x-values as list of lists based on number of vectors
    # supplied.
    x_values = get_x_values_for_scatter(y_values, xlim_min, xlim_max)

    fig = plt.figure()
    ax = plt.axes()

    for x, y in zip(x_values, y_values):
        # Draw horiznotal line at median
        if draw_median:
            median_y = np.median(y)
            xmin = x[0] - hline_radius
            xmax = x[0] + hline_radius
            plt.hlines(median_y, xmin, xmax)
        # Plot x-y values
        if jitter:
            x = jitter_values(x)
        plt.scatter(x, y)
    # Plot settings
    plt.xlim([xlim_min, xlim_max])
    plt.ylim([-7, 7])
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    # Turn off x axis
    ax.axes.get_xaxis().set_ticks([])
    plt.show()


