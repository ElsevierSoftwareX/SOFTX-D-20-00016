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

# Grid Search 
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.svm import SVC

from random import sample


# Numero di componenti per la PCA
NUM_FEATURES = 48

# Attivare o meno il downsampling
DOWNSAMPLE = True
NUM_CLASS_0 = 500
NUM_CLASS_1 = 107

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
    matrix = numpy.delete(matrix, deleteIndex, 0)

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

    return matrix, labels


def trainSVM(path):
    outputPath = os.path.join(path, 'classifier.joblib')
    matrix, labels = getData(path)
    pca = PCA(n_components=NUM_FEATURES)
    print ('Old matrix samples: {}\nOld matrix components: {}\nOld labels lenght: {}\n'.format(len(matrix),len(matrix[0]),len(labels)))
    matrix = pca.fit_transform(matrix)

    # Downsampling sulla classe 0 (che non ci interessa)
    if (DOWNSAMPLE):
        matrix, labels = downsample(matrix, labels, NUM_CLASS_0, NUM_CLASS_1)
    print('New matrix samples: {}\nNew matrix components: {}\nNew labels lenght: {}\n'.format(len(matrix),len(matrix[0]),len(labels)))
    
    ########################
    ###### EDIT HERE #######
    #classifier = svm.OneClassSVM()
    #classifier = linear_model.SGDClassifier(verbose=DEBUG, alpha=0.0001, n_jobs=4, class_weight={1: 2000}, validation_fraction=0.3, n_iter_no_change=5)     #-> acc=0.73
    #classifier = linear_model.SGDClassifier(verbose=DEBUG, max_iter=10000, n_jobs=4)
    #classifier = linear_model.SGDClassifier(verbose=DEBUG, max_iter=10000, n_jobs=4, tol=0.0000000001, alpha=0.0001)                                #-> acc=0.72
    #classifier = svm.LinearSVC(verbose=DEBUG, max_iter=10000, multi_class='ovr', random_state=0, tol=1e-6, class_weight={1: 1000})                  #-> acc=0.87
    #classifier = svm.LinearSVC(verbose=DEBUG, max_iter=10000, multi_class='crammer_singer', random_state=0, tol=1e-6, class_weight={1: 400})        #-> p=0.00 r=0.00 acc=1.00
    #classifier = svm.LinearSVC(verbose=DEBUG, max_iter=100000, multi_class='ovr', random_state=0, tol=1e-5, class_weight={1: 500})                  #-> p=0.00 r=0.23 acc=0.94
    #classifier = svm.LinearSVC(verbose=DEBUG, max_iter=100000, multi_class='ovr', random_state=0, tol=1e-5)                                         #-> acc=0.72
    #classifier = svm.SVC(kernel='linear', class_weight={1: 1000}, verbose=DEBUG)
    #classifier = svm.SVC(kernel='rbf', class_weight={1: 500}, verbose=DEBUG, C=1.0, gamma=0.1)                                                      #-> p=0.00 r=0.64 acc=0.92      [72 sec]
    #classifier = svm.SVC(kernel='rbf', verbose=DEBUG, C=1.0, gamma=0.5)                                                                              #-> p=0.00 r=0.91 acc=0.87      [84 sec]
    
    
    #classifier = svm.SVC(kernel='rbf', gamma=1000000000, C=10)
    classifier = svm.SVC(kernel='rbf', gamma=0.1, C=100)
    classifier.fit(matrix, labels)

    dump(classifier, outputPath) 



def testSVM(path, trainingPath):
    outputPath = os.path.join(trainingPath, 'classifier.joblib')
    matrix, expected = getData(path)
    pca = PCA(n_components=NUM_FEATURES)
    print ('Old matrix samples: {}\nOld matrix components: {}\nOld labels lenght: {}\n'.format(len(matrix),len(matrix[0]),len(expected)))
    matrix = pca.fit_transform(matrix)

    # Downsampling
    if (not DOWNSAMPLE):
        matrix, expected = downsample(matrix, expected, NUM_CLASS_0, NUM_CLASS_1)
    print ('New matrix samples: {}\nNew matrix components: {}\nNew labels lenght: {}\n'.format(len(matrix),len(matrix[0]),len(expected)))
    
    
    classifier = load(outputPath) 
    predicted = classifier.predict(matrix)
    
    print("Classification report for classifier {}:\n{}\n".format(classifier, metrics.classification_report(expected, predicted)))
    print("Confusion matrix:\n{}".format(metrics.confusion_matrix(expected, predicted)))



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
    matrix = pca.fit_transform(matrix)

    # Downsample
    if (DOWNSAMPLE):
        matrix, labels = downsample(matrix, labels, NUM_CLASS_0, NUM_CLASS_1)
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
    grid.fit(matrix, labels)

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
            clf.fit(matrix, labels)
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
        plt.scatter(matrix[:, 0], matrix[:, 1], c=labels, cmap=plt.cm.coolwarm_r,
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
    matrix = pca.fit_transform(matrix)

    # Downsample
    if (DOWNSAMPLE):
        matrix, labels = downsample(matrix, labels, NUM_CLASS_0, NUM_CLASS_1)
    print('New matrix samples: {}\nNew matrix components: {}\nNew labels lenght: {}\n'.format(len(matrix),len(matrix[0]),len(labels)))

    label_arr = numpy.asarray(labels)
    matrix_arr = numpy.asarray(matrix)

    #classifier = svm.LinearSVC(C=1, class_weight={1:1000}, verbose=True)
    classifier = svm.LinearSVC(verbose=True, max_iter=10000, multi_class='ovr', random_state=0, tol=1e-5, class_weight={1: 500}) 

    scoring = ['precision_macro', 'recall_macro']
    scoring = {'prec_macro': 'precision_macro', 'rec_macro': make_scorer(recall_score, average='macro')}
    scores = cross_validate(classifier, matrix_arr, label_arr, scoring=scoring, cv=5, return_train_score=True)
    #scores = cross_val_score(classifier, matrix_arr, label_arr, cv=5, scoring='f1_macro')
    
    print("\n\nfit_time:", scores['fit_time'])
    print("score_time:", scores['score_time'])
    print("test_precision_macro:", scores['test_prec_macro'])
    print("test_recall_macro:", scores['test_rec_macro'])
    print("train_precision_macro:", scores['train_prec_macro'])
    print("train_recall_macro:", scores['train_rec_macro'])


def grid_search(path_training, path_testing):
    # Ref: https://scikit-learn.org/stable/auto_examples/model_selection/plot_grid_search_digits.html

    outputPath = os.path.join(path_training, 'classifier.joblib')
    matrix, labels = getData(path_training)
    pca = PCA(n_components=NUM_FEATURES)
    print ('Old matrix samples: {}\nOld matrix components: {}\nOld labels lenght: {}\n'.format(len(matrix),len(matrix[0]),len(labels)))
    matrix = pca.fit_transform(matrix)

    # Downsampling
    if (DOWNSAMPLE):
        matrix, labels = downsample(matrix, labels, NUM_CLASS_0, NUM_CLASS_1)
    print('New matrix samples: {}\nNew matrix components: {}\nNew labels lenght: {}\n'.format(len(matrix),len(matrix[0]),len(labels)))

    X_train = matrix
    y_train = labels

    # Leggo il testing senza fare downsanpling
    X_test, y_test = getData(path_testing)
    X_test = pca.fit_transform(X_test)
    
    # Set the parameters by cross-validation
    tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e0, 1e-1, 1e-2, 1e-3, 1e-4], 'C': [1, 10, 100, 1000], 'class_weight': [{1: 1}, {1: 100}, {1:500}, {1:1000}]},
                        {'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]

    tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-1, 1e-2, 1e-3, 1e-4], 'C': [1, 10, 100]},
                        {'kernel': ['linear'], 'C': [1, 10, 100]}]

    scores = ['precision', 'recall']

    for score in scores:
        print("# Tuning hyper-parameters for %s" % score)
        print()

        clf = GridSearchCV(SVC(), tuned_parameters, cv=5, n_jobs=-1,
                        scoring='%s_macro' % score)
        clf.fit(X_train, y_train)

        print("Best parameters set found on development set:")
        print()
        print(clf.best_params_)
        print()
        print("Grid scores on development set:")
        print()
        means = clf.cv_results_['mean_test_score']
        stds = clf.cv_results_['std_test_score']
        for mean, std, params in zip(means, stds, clf.cv_results_['params']):
            print("%0.3f (+/-%0.03f) for %r"
                % (mean, std * 2, params))
        print()

        print("Detailed classification report:")
        print()
        print("The model is trained on the full development set.")
        print("The scores are computed on the full evaluation set.")
        print()
        y_true, y_pred = y_test, clf.predict(X_test)
        print(classification_report(y_true, y_pred))
        print()
        print("Confusion matrix:\n{}".format(metrics.confusion_matrix(y_true, y_pred)))

    # Note the problem is too easy: the hyperparameter plateau is too flat and the
    # output model is the same for precision and recall with ties in quality.


def custom_grid_search(path, test_path):
    matrix, labels = getData(path)
    pca = PCA(n_components=NUM_FEATURES)
    print ('Old matrix samples: {}\nOld matrix components: {}\nOld labels lenght: {}\n'.format(len(matrix),len(matrix[0]),len(labels)))
    matrix = pca.fit_transform(matrix)

    # Testing
    X_test, expected = getData(test_path)
    pca = PCA(n_components=NUM_FEATURES)
    X_test = pca.fit_transform(X_test)

    # Definizione delle caratteristiche con cui lanciare le varie istanze di RF
    C_list = [1, 5, 10, 20, 100]
    gamma_list = [1000, 100, 1e0, 1e-1, 1e-2, 1e-3, 1e-4]
    samples_class0 = [100, 200, 300, 500, 800, 1000, 1500]

    with open("result_SVM.txt", "w") as f:

        for num_sample_class0 in samples_class0:
            # Downsampling
            if (DOWNSAMPLE):
                X, y = downsample(matrix, labels, num_sample_class0, 107)
                #print('New matrix samples: {}\nNew matrix components: {}\nNew labels lenght: {}\n'.format(len(matrix),len(matrix[0]),len(labels)))

            for C in C_list:
                for gamma in gamma_list:
                    # Addestramento RF
                    rfc = SVC(kernel='rbf', gamma=gamma, C=C)  #, class_weight={0:1, 1:100}) 
                    rfc.fit(X, y)          
                    
                    # Predizione classi
                    predicted = rfc.predict(X_test)

                    f.write("Training set\nClass 0: {}\nClass 1: {}\n".format(str(num_sample_class0), "107"))
                    f.write("Testing  set\nClass 0: {}\nClass 1: {}\n".format("33290", "72"))
                    f.write("Classification report for:\nC={}\ngamma={}\n\n{}".format(str(C), str(gamma), metrics.classification_report(expected, predicted)))
                    f.write("Confusion matrix:\n{}\n\n\n".format(metrics.confusion_matrix(expected, predicted)))



if __name__ == "__main__":
    #datasetPath = 'dataset/training/Match_2019_09_09_#001'
    #datasetPath = 'dataset/training/Total_near_no_norm'
    datasetPath = 'dataset/training/Total_near'
    #testPath = 'dataset/training/Total'
    #testPath = 'dataset/testing/Match_2019_09_15_#002'
    testPath = 'dataset/testing/Total_near'

    start = time.time() 
    
    custom_grid_search(datasetPath, testPath)

    #auto_tune(datasetPath)
    #trainSVM(datasetPath)
    #cross_validation(datasetPath)
    #grid_search(datasetPath, testPath)

    end = time.time()
    elapsed = round(end-start, 1)
    print("\n\n[ETL] Processed data in: " + str(elapsed) + "s.\n")
    
    #testSVM(testPath, datasetPath)
    
