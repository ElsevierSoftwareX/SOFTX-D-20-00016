import os
import pandas
import numpy
import pickle
import time
import matplotlib.pyplot as plt
from sklearn import datasets, svm, metrics, linear_model
from sklearn.decomposition import PCA
from sklearn.model_selection import StratifiedShuffleSplit
from joblib import dump, load

from sklearn.model_selection import cross_val_score
from sklearn.metrics.scorer import make_scorer
from sklearn.metrics import recall_score
from sklearn.model_selection import cross_validate
from matplotlib.colors import Normalize
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier

# Grid Search 
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.svm import SVC

from scipy.stats import randint as sp_randint

from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV

from random import sample


# Numero di componenti per la PCA
NUM_FEATURES = 48

# Attivare o meno il downsampling
DOWNSAMPLE = True

# Se stampare tutto l'output o no
DEBUG = True


def readLabels(path):
    labels = []
    with open(path, 'r') as f:
        for line in f:
            labels.append(int(line.rstrip('\n')))
    return labels


def getData(path):
    inputMatrixPath = os.path.join(path, 'ballfeatures.log')
    inputLabelsPath = os.path.join(path, 'labels.txt')
    matrix = pandas.read_csv(inputMatrixPath, sep=' ', engine='c', memory_map=True)
    labels = readLabels(inputLabelsPath)
    
    return [matrix.to_numpy(), numpy.asarray(labels, dtype=numpy.int8)]#[500:1000]]


def downsample(matrix, labels, desired_class_0_num, desired_class_1_num):
    i = 0
    size = len(labels)
    deleteIndex = []
    deletable_indexes = []

    for i in range(size):
        if (labels[i] == 0):
            deletable_indexes.append(i)

    labels_to_delete = len(deletable_indexes) - desired_class_0_num

    deleteIndex = sample(deletable_indexes, k=labels_to_delete)

    deleteIndex = numpy.asarray(deleteIndex, dtype=numpy.int32)
    labels = numpy.delete(labels, deleteIndex, 0)
    newMatrix = numpy.delete(matrix, deleteIndex, 0)

    """
    size = len(labels)
    to_add_index = []
    for i in range(size):
        if (labels[i] == 1):
            to_add_index.append(i)
            labels = numpy.append(labels, 1)

    newMatrix = newMatrix.tolist()
    for i in to_add_index:
        newMatrix.append(newMatrix[i])

    newMatrix = numpy.array(newMatrix)
    """

    # Stampa gli elementi dopo il downsampling
    count_class_1 = 0
    count_class_0 = 0
    for i in range(len(labels)):
        if (labels[i] == 1):
            count_class_1 += 1
        else:
            count_class_0 += 1
    
    if (DEBUG):
        print("[DEBUG] Elements count of class 0 after downsampling is {}".format(str(count_class_0)))
        print("[DEBUG] Elements count of class 1 after downsampling is {}\n".format(str(count_class_1)))
            
        print("[DEBUG] Elements count of samples after downsampling is {}".format(str(len(newMatrix))))

    return newMatrix, labels



class MidpointNormalize(Normalize):

    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return numpy.ma.masked_array(numpy.interp(value, x, y))


def auto_tune(path):
    matrix, labels = getData(path)

    ########################################################
    # Set here the wanted PCA
    #
    pca = PCA(n_components=NUM_FEATURES)
    print ('Old matrix samples: {}\nOld matrix components: {}\nOld labels lenght: {}\n'.format(len(matrix),len(matrix[0]),len(labels)))
    newMatrix = pca.fit_transform(matrix)

    # Downsample
    if (DOWNSAMPLE):
        newMatrix, labels = downsample(newMatrix, labels, 50, 44)
    print('New matrix samples: {}\nNew matrix components: {}\nNew labels lenght: {}\n'.format(len(matrix),len(matrix[0]),len(labels)))

    # ######################################################
    # Train classifiers
    #
    # For an initial search, a logarithmic grid with basis
    # 10 is often helpful. Using a basis of 2, a finer
    # tuning can be achieved but at a much higher cost.

    C_range = numpy.logspace(-2, 10, 13)
    gamma_range = numpy.logspace(-9, 3, 13)
    param_grid = dict(gamma=gamma_range, C=C_range)
    cv = StratifiedShuffleSplit(n_splits=5, test_size=0.2, random_state=42)
    grid = GridSearchCV(svm.SVC(), param_grid=param_grid, cv=cv)
    grid.fit(newMatrix, labels)

    print("The best parameters are %s with a score of %0.2f"
        % (grid.best_params_, grid.best_score_))

    # Now we need to fit a classifier for all parameters in the 2d version
    # (we use a smaller set of parameters here because it takes a while to train)

    C_2d_range = [1e-2, 1, 1e2]
    gamma_2d_range = [1e-1, 1, 1e1]
    classifiers = []
    for C in C_2d_range:
        for gamma in gamma_2d_range:
            if (DEBUG):
                print("[DEBUG] Using now gamma={}, C={}".format(str(gamma), str(C)))
            clf = svm.SVC(C=C, gamma=gamma)
            clf.fit(newMatrix, labels)
            classifiers.append((C, gamma, clf))

    # #############################################################################
    # Visualization
    #
    # draw visualization of parameter effects

    plt.figure(figsize=(8, 6))
    xx, yy = numpy.meshgrid(numpy.linspace(-3, 3, 200), numpy.linspace(-3, 3, 200))
    for (k, (C, gamma, clf)) in enumerate(classifiers):
        # evaluate decision function in a grid
        A = numpy.c_[xx.ravel(), yy.ravel(), numpy.repeat(0, xx.ravel().size), numpy.repeat(0, xx.ravel().size), 
                numpy.repeat(0, xx.ravel().size), numpy.repeat(0, xx.ravel().size), 
                numpy.repeat(0, xx.ravel().size), numpy.repeat(0, xx.ravel().size)]

        Z = clf.decision_function(A)
        Z = Z.reshape(xx.shape)

        # visualize decision function for these parameters
        plt.subplot(len(C_2d_range), len(gamma_2d_range), k + 1)
        plt.title("gamma=10^%d, C=10^%d" % (numpy.log10(gamma), numpy.log10(C)),
                size='medium')

        # visualize parameter's effect on decision function
        plt.pcolormesh(xx, yy, -Z, cmap=plt.cm.coolwarm)
        plt.scatter(newMatrix[:, 0], newMatrix[:, 1], c=labels, cmap=plt.cm.coolwarm_r,
                    edgecolors='k')
        plt.xticks(())
        plt.yticks(())
        plt.axis('tight')

    scores = grid.cv_results_['mean_test_score'].reshape(len(C_range),
                                                        len(gamma_range))

    # Draw heatmap of the validation accuracy as a function of gamma and C
    #
    # The score are encoded as colors with the hot colormap which varies from dark
    # red to bright yellow. As the most interesting scores are all located in the
    # 0.92 to 0.97 range we use a custom normalizer to set the mid-point to 0.92 so
    # as to make it easier to visualize the small variations of score values in the
    # interesting range while not brutally collapsing all the low score values to
    # the same color.

    plt.figure(figsize=(8, 6))
    plt.subplots_adjust(left=.2, right=0.95, bottom=0.15, top=0.95)
    plt.imshow(scores, interpolation='nearest', cmap=plt.cm.hot,
            norm=MidpointNormalize(vmin=0.2, midpoint=0.92))
    plt.xlabel('gamma')
    plt.ylabel('C')
    plt.colorbar()
    plt.xticks(numpy.arange(len(gamma_range)), gamma_range, rotation=45)
    plt.yticks(numpy.arange(len(C_range)), C_range)
    plt.title('Validation accuracy')
    plt.show()


def cross_validation(path):
    outputPath = os.path.join(path, 'classifier.joblib')
    matrix, labels = getData(path)
    pca = PCA(n_components=NUM_FEATURES)
    print ('Old matrix samples: {}\nOld matrix components: {}\nOld labels lenght: {}\n'.format(len(matrix),len(matrix[0]),len(labels)))
    newMatrix = pca.fit_transform(matrix)

    # Downsample
    if (DOWNSAMPLE):
        newMatrix, labels = downsample(newMatrix, labels, 50, 44)
    print('New matrix samples: {}\nNew matrix components: {}\nNew labels lenght: {}\n'.format(len(matrix),len(matrix[0]),len(labels)))

    label_arr = numpy.asarray(labels)
    matrix_arr = numpy.asarray(newMatrix)

    #classifier = svm.LinearSVC(C=1, class_weight={1:1000}, verbose=True)
    classifier = svm.LinearSVC(verbose=True, max_iter=10000, multi_class='ovr', random_state=0, tol=1e-5, class_weight={1: 500}) 

    scoring = ['precision_macro', 'recall_macro']
    scoring = {'prec_macro': 'precision_macro', 'rec_macro': make_scorer(recall_score, average='macro')}
    scores = cross_validate(classifier, matrix_arr, label_arr, scoring=scoring, cv=5, return_train_score=True)
    #scores = cross_val_score(classifier, matrix_arr, label_arr, cv=5, scoring='f1_macro')
    
    print("fit_time:", scores['fit_time'])
    print("score_time:", scores['score_time'])
    print("test_precision_macro:", scores['test_prec_macro'])
    print("test_recall_macro:", scores['test_rec_macro'])
    print("train_precision_macro:", scores['train_prec_macro'])
    print("train_recall_macro:", scores['train_rec_macro'])


def grid_search(path):
    # Ref: https://scikit-learn.org/stable/auto_examples/model_selection/plot_grid_search_digits.html

    outputPath = os.path.join(path, 'classifier.joblib')
    matrix, labels = getData(path)
    pca = PCA(n_components=NUM_FEATURES)
    print ('Old matrix samples: {}\nOld matrix components: {}\nOld labels lenght: {}\n'.format(len(matrix),len(matrix[0]),len(labels)))
    matrix = pca.fit_transform(matrix)

    # Downsampling
    if (not DOWNSAMPLE):
        matrix, labels = downsample(matrix, labels, 50, 44)
    print('New matrix samples: {}\nNew matrix components: {}\nNew labels lenght: {}\n'.format(len(matrix),len(matrix[0]),len(labels)))

    X = matrix
    y = labels

    # build a classifier
    clf = RandomForestClassifier(n_estimators=20)


    # Utility function to report best scores
    def report(results, n_top=3):
        for i in range(1, n_top + 1):
            candidates = numpy.flatnonzero(results['rank_test_score'] == i)
            for candidate in candidates:
                print("Model with rank: {0}".format(i))
                print("Mean validation score: {0:.3f} (std: {1:.3f})".format(
                    results['mean_test_score'][candidate],
                    results['std_test_score'][candidate]))
                print("Parameters: {0}".format(results['params'][candidate]))
                print("")


    # specify parameters and distributions to sample from
    param_dist = {"max_depth": [3, None],
                "max_features": sp_randint(1, 11),
                "min_samples_split": sp_randint(2, 11),
                "bootstrap": [True, False],
                "criterion": ["gini", "entropy"]}

    # run randomized search
    n_iter_search = 20
    random_search = RandomizedSearchCV(clf, param_distributions=param_dist,
                                    n_iter=n_iter_search, cv=5, iid=False)

    start = time.time()
    random_search.fit(X, y)
    print("RandomizedSearchCV took %.2f seconds for %d candidates"
        " parameter settings." % ((time.time() - start), n_iter_search))
    report(random_search.cv_results_)

    # use a full grid over all parameters
    param_grid = {"max_depth": [3, None],
                "max_features": [1, 3, 10],
                "min_samples_split": [2, 3, 10],
                "bootstrap": [True, False],
                "criterion": ["gini", "entropy"]}

    # run grid search
    grid_search = GridSearchCV(clf, param_grid=param_grid, cv=5, iid=False)
    start = time.time()
    grid_search.fit(X, y)

    print("GridSearchCV took %.2f seconds for %d candidate parameter settings." % (time.time() - start, len(grid_search.cv_results_['params'])))
    report(grid_search.cv_results_)



def classifierRF(path, test_path):
    outputPath = os.path.join(path, 'classifier.joblib')
    matrix, labels = getData(path)
    pca = PCA(n_components=NUM_FEATURES)
    print ('Old matrix samples: {}\nOld matrix components: {}\nOld labels lenght: {}\n'.format(len(matrix),len(matrix[0]),len(labels)))
    matrix = pca.fit_transform(matrix)

    # Testing
    X_test, expected = getData(test_path)
    pca = PCA(n_components=NUM_FEATURES)
    X_test = pca.fit_transform(X_test)

    # Definizione delle caratteristiche con cui lanciare le varie istanze di RF
    depths = range(3, 30, 5)
    n_estimators = [20, 100, 500]
    samples_class0 = [100, 200, 300, 500, 800, 1000, 1500]

    with open("result.txt", "w") as f:

        for num_sample_class0 in samples_class0:
            # Downsampling
            if (DOWNSAMPLE):
                X, y = downsample(matrix, labels, num_sample_class0, 107)
                #print('New matrix samples: {}\nNew matrix components: {}\nNew labels lenght: {}\n'.format(len(matrix),len(matrix[0]),len(labels)))

            for depth in depths:
                for estimator in n_estimators:
                    # Addestramento RF
                    rfc = RandomForestClassifier(n_jobs=-1, max_features='sqrt', n_estimators=estimator, oob_score=True, verbose=False, max_depth=depth)  #, class_weight={0:1, 1:100}) 
                    rfc.fit(X, y)          
                    
                    # Predizione classi
                    predicted = rfc.predict(X_test)

                    f.write("Training set\nClass 0: {}\nClass 1: {}\n".format(str(num_sample_class0), "107"))
                    f.write("Testing  set\nClass 0: {}\nClass 1: {}\n".format("33290", "72"))
                    f.write("Classification report for:\nEstimators={}\nMaxDepth={}\n\n{}".format(str(estimator), str(depth), metrics.classification_report(expected, predicted)))
                    f.write("Confusion matrix:\n{}\n\n\n".format(metrics.confusion_matrix(expected, predicted)))



def testSVM(path, trainingPath):
    outputPath = os.path.join(trainingPath, 'classifier.joblib')
    matrix, expected = getData(path)
    pca = PCA(n_components=NUM_FEATURES)
    print ('Old matrix samples: {}\nOld matrix components: {}\nOld labels lenght: {}\n'.format(len(matrix),len(matrix[0]),len(expected)))
    matrix = pca.fit_transform(matrix)

    # Downsampling
    if (not DOWNSAMPLE):
        matrix, expected = downsample(matrix, expected, 50, 44)
    print ('New matrix samples: {}\nNew matrix components: {}\nNew labels lenght: {}\n'.format(len(matrix),len(matrix[0]),len(expected)))
    
    
    classifier = load(outputPath) 
    predicted = classifier.predict(matrix)

    print("Classification report for classifier {}:\n{}\n".format(classifier, metrics.classification_report(expected, predicted)))
    print("Confusion matrix:\n{}".format(metrics.confusion_matrix(expected, predicted)))




if __name__ == "__main__":
    datasetPath = 'dataset/training/Total_near'
    testPath = 'dataset/testing/Total_near'
    #testPath = 'dataset/testing/Match_2019_09_09_#001'

    start = time.time() 
    
    #auto_tune(datasetPath)
    #trainSVM(datasetPath)
    #cross_validation(datasetPath)
    #grid_search(testPath)
    classifierRF(datasetPath, testPath)

    end = time.time()
    elapsed = round(end-start, 1)
    print("\n\n[ETL] Processed data in: " + str(elapsed) + "s.\n")
    
    #testSVM(testPath, datasetPath)
    
