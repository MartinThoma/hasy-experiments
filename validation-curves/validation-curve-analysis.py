#!/usr/bin/env python

"""Visualize how the accuracy increases over epochs."""

import glob
import natsort
import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

base = '/home/moose/GitHub/HASY/scripts/experiments/'
csv_files = natsort.natsorted(glob.glob('%stf-cnn-weight-decay/*.csv' % base))
csv_filename = csv_files[0]


def file_len(fname):
    """Count the number of lines of fname."""
    i = 0
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

MAX_DATA_LINES = file_len(csv_filename)

xs_all, y_test_all, y_train_all = [], [], []
epoch_sum_train = [0 for _ in range(MAX_DATA_LINES)]
epoch_sum_test = [0 for _ in range(MAX_DATA_LINES)]
series = 0

# Get the data
experiments = [('tf-cnn-updated', 'updated', ('ro-', 'g^-')),
               ('tf-cnn-updated-prelu', 'updated prelu', ('bD-', 'cH-'))]
for folder, name, colors in experiments:
    csv_files = glob.glob(('{base}/{folder}/*.csv').format(base=base,
                                                           folder=folder))
    csv_files = natsort.natsorted(csv_files)
    curves_train = []
    curves_test = []
    for filename in csv_files:
        series += 1
        with open(filename, 'rb') as f:
            reader = csv.reader(f, delimiter=";")
            validation_data = list(reader)

        # Crop data
        validation_data = validation_data[:MAX_DATA_LINES]

        xs = [el[0] for el in validation_data]
        ys_train = [1 - float(el[1]) for el in validation_data]
        ys_test = [1 - float(el[2]) for el in validation_data]
        curves_train.append(np.array(ys_train))
        curves_test.append(np.array(ys_test))

        for i, y_train in enumerate(ys_train):
            epoch_sum_train[i] += y_train
        for i, y_test in enumerate(ys_test):
            epoch_sum_test[i] += y_test

        xs_all += xs
        y_train_all += ys_train
        y_test_all += ys_test
    plt.plot(xs, sum(curves_train) / 10.0, colors[0], label="Training set (%s)" % name)
    plt.plot(xs, ys_test, colors[1], label="Test set (%s)" % name)

# Print mean
# train_means = [el / float(series) for el in epoch_sum_train]
# test_means = [el / float(series) for el in epoch_sum_test]
# plt.plot(xs, train_means, 'b-')
# plt.plot(xs, test_means, 'b-')

plt.axhline(y=0.20)  # 0.175
plt.axhline(y=0.01)
# x = np.linspace(0, MAX_DATA_LINES * 100, 100)  # 100 linearly spaced numbers
# plt.plot(x, (-10 * 10**-7) * x + 0.17, color="red")  # sin(x)/x

# This is added to the SO post
plt.ylim(0.0, 0.5)
plt.title(u"Epoch-Accuracy Validation Curve", fontweight='bold', fontsize=20)
plt.xlabel(r"""Training step""", fontsize=20)
plt.ylabel(r"""1 - Accuracy""", fontsize=20)
plt.legend(fontsize=20)
plt.show()

# I'm not sure if this makes sense
d = {'train': pd.Series(y_train_all, index=xs_all),
     'test': pd.Series(y_test_all, index=xs_all),
     'epoch': pd.Series(xs_all, index=xs_all)}
df = pd.DataFrame(d)
df.index.name = 'epoch'

plt.show()
