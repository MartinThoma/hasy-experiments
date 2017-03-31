#!/usr/bin/env python

import numpy as np


def write_analyzation_results(handle, clf_name, results, cm):
    """
    Write classifier results to open file handle.

    Parameters
    ----------
    handle : opened file
    clf_name : str
    results : dict
        keys: 'fit_time', 'testing_time', 'accuracy'
    """
    handle.write("Classifier: %s\n" % clf_name)
    handle.write("Accuracy: %0.4f\n" % (results['accuracy'] * 100))
    handle.write("Testing time: %0.4fs\n" % results['testing_time'])
    handle.write("Training time: %0.4fs\n" % results['fit_time'])
    handle.write("Confusion matrix:\n")
    for row in cm:
        handle.write("%s\n" % row)
    handle.write("#" * 80)
    handle.write("\n")


def pretty_print(classifier_data):
    """Pretty print classifier data."""
    for clf_name, clf_data in classifier_data.items():
        print("%s:" % clf_name)
        train_times = np.array([el['training_time'] for el in clf_data])
        test_times = np.array([el['testing_time'] for el in clf_data])
        accuracy = np.array([el['accuracy'] for el in clf_data])
        print("\tRuns:\t%i" % len(train_times))
        print("\ttrain_time:\t%0.1f (min=%0.2f, max=%0.2f)" %
              (train_times.mean(), train_times.min(), train_times.max()))
        print("\ttest_time:\t%0.1f (min=%0.2f, max=%0.2f)" %
              (test_times.mean(), test_times.min(), test_times.max()))
        print("\tacc:\t\t%0.1f (min=%0.1f, max=%0.1f)" %
              (accuracy.mean() * 100,
               accuracy.min() * 100,
               accuracy.max() * 100))
    print(classifier_data)
