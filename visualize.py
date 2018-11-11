#!/usr/bin/python

# this script visualizes the results in this folder

from matplotlib import pyplot as plt
import os
import numpy as np

data = dict()
for f in os.listdir('results/'):
    print f
    if not '.npy' in f:
        continue
    stat, measure, alg, time = f[:-4].split('_')
    key = '%s_%s' % (stat, measure)
    if not key in data:
        data[key] = []
    data[key].append({'alg': alg, 'time': time, 'data': np.load('results/%s' % f)})

print data

for key, value in data.iteritems():
    plt.figure()
    for item in value:
        label = '%s_%s' % (item['alg'], item['time'])
        plt.plot(item['data'], label = label)
    plt.legend()
    plt.title(key)

plt.show()
