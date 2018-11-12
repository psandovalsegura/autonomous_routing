#!/usr/bin/python

# this script visualizes the results in this folder

from matplotlib import pyplot as plt
import os
import numpy as np

data = dict()
for f in os.listdir('results/'):
    if not '.npy' in f:
        continue
    stat, measure, alg, time = f[:-4].split('_')
    key = '%s_%s' % (stat, measure)
    if not key in data:
        data[key] = []
    data[key].append({'alg': alg, 'time': time, 'data': np.load('results/%s' % f)})


for key, value in data.iteritems():
    plt.figure()
    for item in value:
        label = '%s_%s' % (item['alg'], item['time'])
        plt.plot(item['data'], label = label,\
                               linestyle = 'dashed' if item['alg'] == 'dijkstra' else 'solid')
    plt.title(key)


for key, value in data.iteritems():
    plt.figure()
    new_data = dict()
    for item in value:
        if not item['alg'] in new_data:
            new_data[item['alg']] = []
        new_data[item['alg']].append(item['data'])
    for alg in new_data:
        plt.plot(np.mean(np.array(new_data[alg]), axis = 0), label = alg)
        plt.title(key)
        plt.legend()


plt.show()
