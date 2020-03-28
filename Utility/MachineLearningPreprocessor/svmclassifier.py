import os
import pandas
import numpy
from sklearn import datasets, svm, metrics
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import pickle
from joblib import dump, load

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
    partialMatrix = matrix[500:1000]
    
    return [matrix.to_numpy(), numpy.asarray(labels, dtype=numpy.int8)]#[500:1000]]

def trainSVM(path):
    outputPath = os.path.join(path, 'classifier.joblib')
    matrix, labels = getData(path)
    pca = PCA(n_components=5)
    print ('Old matrix samples: {}\nOld matrix components: {}\nOld labels lenght: {}\n'.format(len(matrix),len(matrix[0]),len(labels)))
    newMatrix = pca.fit_transform(matrix)

    #sottocampiona ogni 10 campioni
    i = 0
    deleteIndex = []
    while (i+10 < len(labels)):
        k = 1
        if (labels[i] == 0):
            while (labels[i+k] == 0) and (k <= 10):
                deleteIndex.append(i+k)
                k += 1
        i += k
    
    deleteIndex = numpy.asarray(deleteIndex, dtype=numpy.int32)
    labels = numpy.delete(labels, deleteIndex, 0)
    newMatrix = numpy.delete(newMatrix, deleteIndex, 0)

    print ('New matrix samples: {}\nNew matrix components: {}\nNew labels lenght: {}\n'.format(len(newMatrix),len(newMatrix[0]),len(labels)))
    classifier = svm.LinearSVC(class_weight='balanced', verbose=True, max_iter=10000)
    classifier.fit(newMatrix, labels)
    
    dump(classifier, outputPath) 

def testSVM(path, trainingPath):
    outputPath = os.path.join(trainingPath, 'classifier.joblib')
    matrix, expected = getData(path)
    pca = PCA(n_components=5)
    print ('Old matrix samples: {}\nOld matrix components: {}\nOld labels lenght: {}\n'.format(len(matrix),len(matrix[0]),len(expected)))
    newMatrix = pca.fit_transform(matrix)
    print ('New matrix samples: {}\nNew matrix components: {}\nNew labels lenght: {}\n'.format(len(newMatrix),len(newMatrix[0]),len(expected)))
    
    classifier = load(outputPath) 
    predicted = classifier.predict(newMatrix)
    
    print("Classification report for classifier {}:\n{}\n".format(classifier, metrics.classification_report(expected, predicted)))
    print("Confusion matrix:\n{}".format(metrics.confusion_matrix(expected, predicted)))



if __name__ == "__main__":
    datasetPath = 'dataset/training/Match_2019_08_30_#001'
    testPath = 'dataset/testing/Match_2019_08_30_#001'
    #testSVM(testPath, datasetPath)
    trainSVM(datasetPath)

