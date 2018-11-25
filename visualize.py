#!/usr/bin/python

# this script visualizes the results in this folder
# pass the result printing horizon as as argument
# added to fix the issue of uneequal result lengths

from matplotlib import pyplot as plt
import os
import numpy as np
import sys

color_list = ['red', 'blue', 'green', 'purple', 'magenta', 'yellow', 'black',\
              'purple', 'orange', 'brown']
color_dict = dict()
label_dict = {'dijkstra' : 'Quickest Route Update',
              'random': 'Static Random',
              'dynamicRandom': 'Dynamic Random',
              'lessCarAhead': 'Faster Leg Ahead',
              'decmcts': 'Dec MCTS',
              'decmcts1Block': 'Dec MCTS 1 Block',
              'decmcts2Block': 'Dec MCTS 2 Blocks',
              'decmcts5Block': 'Dec MCTS 5 Blocks'}
title_dict = {'mean_traveltime': 'Mean Travel Time',
              'mean_speed': 'Average Speed'}
y_axis_dict = {'mean_traveltime': r'$\mathbf{\bar{T}\quad (tick)}$',
               'mean_speed': r'$\mathbf{\bar{V}\quad (\frac{patch}{tick})}$'}

leg_loc_dict = {'mean_traveltime': 'lower right',
                'mean_speed': 'upper right'}

ylim_dict = {'mean_traveltime': [90, 120],
                'mean_speed': [.05, .075]}

color_dict = {'dijkstra' : 'red',
              'random': 'blue',
              'dynamicRandom': 'green',
              'lessCarAhead': 'purple',
              'decmcts': 'magenta',
              'decmcts1Block': 'yellow',
              'decmcts2Block': 'black',
              'decmcts5Block': 'cyan'}



# results folder
folder = sys.argv[1]

# the horizon for printing the results
horizon = int(sys.argv[2])



data = dict()
for f in os.listdir(folder):
    if not '.npy' in f:
        continue
    stat, measure, alg, time = f[:-4].split('_')
    key = '%s_%s' % (stat, measure)
    if not key in data:
        data[key] = []
    #if not alg in color_dict:
    #    color_dict[alg] = color_list[0]
    #    color_list = color_list[1:]
    data[key].append({'alg': alg, 'time': time, 'data': np.load('%s%s' % (folder, f))[:horizon]})

'''
for key, value in data.iteritems():
    plt.figure()
    for item in value:
        plt.plot(item['data'], color = color_dict[item['alg']])
    plt.title(title_dict[key])
    plt.xlabel('Time (tick)')
    plt.ylabel(y_axis_dict[key])
'''

for key, value in data.items():
    plt.figure()
    new_data = dict()
    for item in value:
        if not item['alg'] in new_data:
            new_data[item['alg']] = []
        new_data[item['alg']].append(item['data'])
    for alg in new_data:
        #plt.plot(np.mean(np.array(new_data[alg]), axis = 0), label = label_dict[alg],\
        #                 color = color_dict[alg], linewidth = 3)
        x = np.arange(len(np.mean(np.array(new_data[alg]), axis=0)))
        std_error_temp = np.std(np.array(new_data[alg]), axis = 0)

        std_error_split = int(len(std_error_temp)/np.random.randint(10,20))
        std_error = [std_error_temp[i] if i % std_error_split == 0 else 0 for i in range(len(std_error_temp))]
        #plt.errorbar(x, np.mean(np.array(new_data[alg]), axis=0), yerr=std_error, label = label_dict[alg],\
        #                 color = color_dict[alg], linewidth = 3)

        plt.plot(x, np.mean(np.array(new_data[alg]), axis=0), label = label_dict[alg],\
                            color = color_dict[alg], linewidth = 4)

        
        plt.fill_between(x, np.mean(np.array(new_data[alg]), axis=0) - std_error_temp,\
                            np.mean(np.array(new_data[alg]), axis=0) + std_error_temp,\
                            color = color_dict[alg], alpha = 0.2)


        
        plt.title(title_dict[key], fontweight = 'bold')
        plt.xlabel('Time (tick)', fontweight = 'bold')
        plt.ylabel(y_axis_dict[key], fontweight = 'bold')
        plt.legend(loc = leg_loc_dict[key])
        #plt.ylim(ylim_dict[key])

plt.show()
