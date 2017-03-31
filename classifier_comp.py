#!/usr/bin/env python

"""Train classifiers to predict HASY data."""

import numpy as np
import time
import os

# Classifiers
# from sklearn.neighbors import KNeighborsClassifier
# from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
# from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
# from sklearn.ensemble import GradientBoostingClassifier
# from sklearn.naive_bayes import GaussianNB
# from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
# from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
# from sklearn.neural_network import BernoulliRBM
# from sklearn.pipeline import Pipeline
# from sklearn.linear_model import LogisticRegression
# from sklearn import cross_validation


def main():
    """Run experiment with multiple classifiers."""
    # Get classifiers
    classifiers = [
        ('Decision Tree', DecisionTreeClassifier(max_depth=5)),
        # ('Random Forest', RandomForestClassifier(n_estimators=50,
        #                                          n_jobs=10,
        #                                          max_features=50)),
        # ('AdaBoost', AdaBoostClassifier()),
        # ('Naive Bayes', GaussianNB()),
        # ('LDA', LinearDiscriminantAnalysis()),
        # ('QDA', QuadraticDiscriminantAnalysis()),
        # ('Random Forest 2', RandomForestClassifier(max_depth=5,
        #                                            n_estimators=10,
        #                                            max_features=1,
        #                                            n_jobs=10)),
        # ('Logistic Regression (C=1)', LogisticRegression(C=1)),
        # #('Logistic Regression (C=1000)', LogisticRegression(C=10000)),
        # ('RBM 200, n_iter=40, LR=0.01, Reg: C=1',
        #  Pipeline(steps=[('rbm', BernoulliRBM(n_components=200,
        #                                       n_iter=40,
        #                                       learning_rate=0.01,
        #                                       verbose=True)),
        #                  ('logistic', LogisticRegression(C=1))])),
        # ('RBM 200, n_iter=40, LR=0.01, Reg: C=10000',
        #  Pipeline(steps=[('rbm', BernoulliRBM(n_components=200,
        #                                       n_iter=40,
        #                                       learning_rate=0.01,
        #                                       verbose=True)),
        #                  ('logistic', LogisticRegression(C=10000))])),
        # ('RBM 100', Pipeline(steps=[('rbm', BernoulliRBM(n_components=100)),
        #                             ('logistic', LogisticRegression(C=1))])),
        # ('RBM 100, n_iter=20',
        #  Pipeline(steps=[('rbm', BernoulliRBM(n_components=100, n_iter=20)),
        #                  ('logistic', LogisticRegression(C=1))])),
        # ('RBM 256', Pipeline(steps=[('rbm', BernoulliRBM(n_components=256)),
        #                             ('logistic', LogisticRegression(C=1))])),
        # ('RBM 512, n_iter=100',
        #  Pipeline(steps=[('rbm', BernoulliRBM(n_components=512, n_iter=10)),
        #                  ('logistic', LogisticRegression(C=1))])),
        # ('NN 20:5', skflow.TensorFlowDNNClassifier(hidden_units=[20, 5],
        #                                            n_classes=data['n_classes'],
        #                                            steps=500)),
        # ('NN 500:200 dropout',
        # ('CNN', skflow.TensorFlowEstimator(model_fn=conv_model,
        #                                    n_classes=10,
        #                                    batch_size=100,
        #                                    steps=20000,
        #                                    learning_rate=0.001)),
        # ('SVM, adj.', SVC(probability=False,
        #                   kernel="rbf",
        #                   C=2.8,
        #                   gamma=.0073,
        #                   cache_size=200)),
        # ('SVM, linear', SVC(kernel="linear", C=0.025, cache_size=200)),
        # ('k nn', KNeighborsClassifier(3)),
        # ('Gradient Boosting', GradientBoostingClassifier())
    ]

    print("Start getting data.")
    data = get_data('hasy')
    print("Got data. Start.")

    # Fit them all
    classifier_data = {}
    with open('classifier-comp.md', 'w') as f:
        for clf_name, clf in classifiers:
            print(clf_name)
            classifier_data[clf_name] = []
            f.write("#" * 80)
            f.write("\n")
            f.write("Start fitting '%s' classifier.\n" % clf_name)
            for fold in data:
                print("Got %i training samples and %i test samples." %
                      (len(fold['train']['X']),
                       len(fold['test']['X'])))
                t0 = time.time()
                examples = 10**9
                clf.fit(fold['train']['X'][:examples],
                        fold['train']['y'][:examples])
                t1 = time.time()
                an_data = analyze(clf,
                                  fold,
                                  t1 - t0, clf_name=clf_name, handle=f)
                classifier_data[clf_name].append({'training_time': t1 - t0,
                                                  'testing_time':
                                                      an_data['testing_time'],
                                                  'accuracy':
                                                      an_data['accuracy']})

    pretty_print(classifier_data)


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


def analyze(clf, data, fit_time, clf_name='', handle=None):
    """
    Analyze how well a classifier performs on data.

    Parameters
    ----------
    clf : classifier object
    data : dict
    fit_time : float
    clf_name : str
    handle : write to file

    Returns
    -------
    dict
        accuracy and testing_time
    """
    results = {}

    # Get confusion matrix
    from sklearn import metrics
    t0 = time.time()
    predicted = np.array([])
    for i in range(0, len(data['test']['X']), 128):  # go in chunks of size 128
        predicted_single = clf.predict(data['test']['X'][i:(i + 128)])
        predicted = np.append(predicted, predicted_single)
    t1 = time.time()
    results['testing_time'] = t1 - t0
    results['fit_time'] = fit_time
    results['accuracy'] = metrics.accuracy_score(data['test']['y'], predicted)
    cm = (metrics.confusion_matrix(data['test']['y'], predicted)).tolist()
    write_analyzation_results(handle, clf_name, results, cm)
    return results


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


def view_image(image, label=""):
    """
    View a single image.

    Parameters
    ----------
    image : numpy array
        Make sure this is of the shape you want.
    label : str
    """
    from matplotlib.pyplot import show, imshow, cm
    print("Label: %s" % label)
    imshow(image, cmap=cm.gray)
    show()


def get_data(dataset='iris'):
    """
    Get data ready to learn with.

    Parameters
    ----------
    dataset : str
        'iris'

    Returns
    -------
    dict
    """
    if dataset == 'iris':
        import sklearn
        from sklearn.datasets import fetch_mldata
        from sklearn.utils import shuffle
        mnist = fetch_mldata('iris')

        x = mnist.data
        y = mnist.target

        le = sklearn.preprocessing.LabelEncoder()
        le.fit(y)
        y = le.transform(y)

        x, y = shuffle(x, y, random_state=0)

        from sklearn.cross_validation import train_test_split
        x_train, x_test, y_train, y_test = train_test_split(x, y,
                                                            test_size=0.33,
                                                            random_state=42)
        data = {'train': {'X': x_train,
                          'y': y_train},
                'test': {'X': x_test,
                         'y': y_test},
                'n_classes': len(np.unique(y_train))}
        scaler = sklearn.preprocessing.StandardScaler().fit(data['train']['X'])
        data['train']['X'] = scaler.transform(data['train']['X'])
        data['test']['X'] = scaler.transform(data['test']['X'])
    elif dataset == 'mnist_simple':
        # Load the simple, but similar digits dataset
        from sklearn.datasets import load_digits
        from sklearn.utils import shuffle
        digits = load_digits()
        x = [np.array(el).flatten() for el in digits.images]
        y = digits.target

        # Scale data to [-1, 1] - This is of mayor importance!!!
        x = x / 255.0 * 2 - 1

        x, y = shuffle(x, y, random_state=0)

        from sklearn.cross_validation import train_test_split
        x_train, x_test, y_train, y_test = train_test_split(x, y,
                                                            test_size=0.33,
                                                            random_state=42)
        data = {'train': {'X': x_train,
                          'y': y_train},
                'test': {'X': x_test,
                         'y': y_test}}
    elif dataset == 'mnist':  # Load the original dataset
        from sklearn.datasets import fetch_mldata
        from sklearn.utils import shuffle
        mnist = fetch_mldata('MNIST original')

        x = mnist.data
        y = mnist.target

        # Scale data to [-1, 1] - This is of mayor importance!!!
        x = x / 255.0 * 2 - 1

        x, y = shuffle(x, y, random_state=0)

        from sklearn.cross_validation import train_test_split
        x_train, x_test, y_train, y_test = train_test_split(x, y,
                                                            test_size=1 / 7.,
                                                            random_state=42)
        data = {'train': {'X': x_train,
                          'y': y_train},
                'test': {'X': x_test,
                         'y': y_test}}
    elif dataset == 'hasy':
        import hasy_tools as ht
        dataset_path = os.path.join(os.path.expanduser("~"), 'hasy')
        data_complete = []

        symbol_id2index = ht.generate_index("%s/symbols.csv" % dataset_path)
        base_ = "%s/classification-task/fold" % dataset_path
        for fold in range(1, 11):
            print("Fold %i" % fold)
            one_hot = False  # Only True for CNN
            x_train, y_train, s_train = ht.load_images('%s-%i/train.csv' %
                                                       (base_, fold),
                                                       symbol_id2index,
                                                       one_hot=one_hot,
                                                       flatten=True,
                                                       shuffle=True)
            x_test, y_test, s_test = ht.load_images('%s-%i/test.csv' %
                                                    (base_, fold),
                                                    symbol_id2index,
                                                    one_hot=one_hot,
                                                    flatten=True,
                                                    shuffle=True)
            data = {'train': {'X': x_train,
                              'y': y_train},
                    'test': {'X': x_test,
                             'y': y_test},
                    'n_classes': 369}
            data_complete.append(data)
        data = data_complete
    else:
        raise NotImplemented()
    return data


if __name__ == '__main__':
    main()
