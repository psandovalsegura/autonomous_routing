#!/usr/bin/python

# this script visualizes the results in this folder

from matplotlib import pyplot as plt
import os
import numpy as np

color_list = ['red', 'blue', 'green', 'purple', 'magenta', 'yellow', 'black',\
              'purple', 'orange', 'brown']
color_dict = dict()
label_dict = {'dijkstra' : 'Quickest Route Update',
              'random': 'Static Random',
              'dynamicRandom': 'Dynamic Random',
              'lessCarAhead': 'Faster Leg Ahead'}
title_dict = {'mean_traveltime': 'Mean Travel Time',
              'mean_speed': 'Average Speed'}
y_axis_dict = {'mean_traveltime': r'$\mathbf{\bar{T}\quad (tick)}$',
               'mean_speed': r'$\mathbf{\bar{V}\quad (\frac{patch}{tick})}$'}

leg_loc_dict = {'mean_traveltime': 'lower right',
                'mean_speed': 'upper right'}

ylim_dict = {'mean_traveltime': None,
                'mean_speed': [.035, .055]}

data = dict()
for f in os.listdir('results/'):
    if not '.npy' in f:
        continue
    stat, measure, alg, time = f[:-4].split('_')
    key = '%s_%s' % (stat, measure)
    if not key in data:
        data[key] = []
    if not alg in color_dict:
        color_dict[alg] = color_list[0]
        color_list = color_list[1:]
    data[key].append({'alg': alg, 'time': time, 'data': np.load('results/%s' % f)})

'''
for key, value in data.iteritems():
    plt.figure()
    for item in value:
        plt.plot(item['data'], color = color_dict[item['alg']])
    plt.title(title_dict[key])
    plt.xlabel('Time (tick)')
    plt.ylabel(y_axis_dict[key])
'''


for key, value in data.iteritems():
    plt.figure()
    new_data = dict()
    for item in value:
        if not item['alg'] in new_data:
            new_data[item['alg']] = []
        new_data[item['alg']].append(item['data'])
    for alg in new_data:
        plt.plot(np.mean(np.array(new_data[alg]), axis = 0), label = label_dict[alg],\
                         color = color_dict[alg], linewidth = 3)
        plt.title(title_dict[key], fontweight = 'bold')
        plt.xlabel('Time (tick)', fontweight = 'bold')
        plt.ylabel(y_axis_dict[key], fontweight = 'bold')
        plt.legend(loc = leg_loc_dict[key])
        plt.ylim(ylim_dict[key])

plt.show()
