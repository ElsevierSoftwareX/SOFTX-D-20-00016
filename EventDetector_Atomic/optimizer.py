#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import math
import argparse
import random
import array
from os import makedirs

import pandas
from time import time
import matplotlib.pyplot as plt
import numpy
import pickle
from Validator.validator import AtomicValidator as AV
from Validator.validator import XML as XMLc
from deap import base, creator, tools, algorithms
from decimal import Decimal, ROUND_HALF_EVEN
from EventDetector_Atomic.detector import Detector as DET
from EventDetector_Atomic.detector import LinePandaParser as PND
from EventDetector_Atomic.detector import XML as XMLa

def calculateFScore(TP,FP,FN):
    try:
        precision = TP/(TP+FP)
    except ZeroDivisionError: 
        precision = 0
    try:
        recall = TP/(TP+FN)
    except ZeroDivisionError: 
        recall = 0
    try:
        fScore = 2*precision*recall/(precision+recall)
    except ZeroDivisionError: 
        fScore = 0
    return precision, recall, fScore

def findBestAndVisualize(outputOriginal, pathOutput):
    kickingTheBall = []
    ballPossession = []
    tackle = []
    ballDeflection = []
    ballOut = []
    average =[]
    output = list(outputOriginal)

    with open('E:/alloutput.txt', 'w') as f:
        f.write('Index KickP KickR KickF PossP PossR PossF TackleP TackleR TackleF DeflP DeflR DeflF OutP OutR OutF\n')
        for index,element in enumerate(output):
            precisions = [output[index]['KickingTheBall']['Precision'], output[index]['BallPossession']['Precision'], output[index]['Tackle']['Precision'], output[index]['BallDeflection']['Precision']]#, output[index]['BallOut']['Precision'], output[index]['Goal']['Precision']]
            recalls = [output[index]['KickingTheBall']['Recall'], output[index]['BallPossession']['Recall'], output[index]['Tackle']['Recall'], output[index]['BallDeflection']['Recall']]#, output[index]['BallOut']['Recall'], output[index]['Goal']['Recall']]
            fScores = [output[index]['KickingTheBall']['F-Score'], output[index]['BallPossession']['F-Score'], output[index]['Tackle']['F-Score'], output[index]['BallDeflection']['F-Score']]#, #output[index]['BallOut']['F-Score'], output[index]['Goal']['F-Score']]
            f.write('{} {:0.2f} {:0.2f} {:0.2f} {:0.2f} {:0.2f} {:0.2f} {:0.2f} {:0.2f} {:0.2f} {:0.2f} {:0.2f} {:0.2f}\n'.format(index, precisions[0], recalls[0], fScores[0], precisions[1], recalls[1], fScores[1], precisions[2], recalls[2], fScores[2], precisions[3], recalls[3], fScores[3]))#, precisions[4], recalls[4], fScores[4], precisions[5], recalls[5], fScores[5]))        


    for i,element in enumerate(output):
        kickingTheBall.append(element['KickingTheBall']['F-Score'])
        ballPossession.append(element['BallPossession']['F-Score'])
        tackle.append(element['Tackle']['F-Score'])
        ballDeflection.append(element['BallDeflection']['F-Score'])
        ballOut.append(element['BallOut']['F-Score'])
        average.append((kickingTheBall[i]+ballPossession[i]+tackle[i]+ballDeflection[i]+ballOut[i])/5)
    
    correspondingIndex = list(range(len(tackle)))
    degenerateNumber = 0
    i = 0
    while (i < len(tackle)):
        if (tackle[i] < 0.2):
            degenerateNumber += 1
            del tackle[i]
            del kickingTheBall[i]
            del ballPossession[i]
            del ballDeflection[i]
            del average[i]
            del output[i]
            del correspondingIndex[i]
        else:
            i += 1
    
    print("\nThere are {} degenerates".format(degenerateNumber))

    bestElements = []
    bestElements.append(kickingTheBall.index(max(kickingTheBall)))
    bestElements.append(ballPossession.index(max(ballPossession)))
    bestElements.append(tackle.index(max(tackle)))
    bestElements.append(ballDeflection.index(max(ballDeflection)))
    bestElements.append(average.index(max(average)))

    with open(pathOutput + '2.txt', 'w') as f:
        f.write('Index KickP KickR KickF PossP PossR PossF TackleP TackleR TackleF DeflP DeflR DeflF OutP OutR OutF\n')
        for index, corrIndex in enumerate(correspondingIndex):
            precisions = [output[index]['KickingTheBall']['Precision'], output[index]['BallPossession']['Precision'], output[index]['Tackle']['Precision'], output[index]['BallDeflection']['Precision']]#, output[index]['BallOut']['Precision'], output[index]['Goal']['Precision']]
            recalls = [output[index]['KickingTheBall']['Recall'], output[index]['BallPossession']['Recall'], output[index]['Tackle']['Recall'], output[index]['BallDeflection']['Recall']]#, output[index]['BallOut']['Recall'], output[index]['Goal']['Recall']]
            fScores = [output[index]['KickingTheBall']['F-Score'], output[index]['BallPossession']['F-Score'], output[index]['Tackle']['F-Score'], output[index]['BallDeflection']['F-Score']]#, #output[index]['BallOut']['F-Score'], output[index]['Goal']['F-Score']]
            f.write('{} {:0.2f} {:0.2f} {:0.2f} {:0.2f} {:0.2f} {:0.2f} {:0.2f} {:0.2f} {:0.2f} {:0.2f} {:0.2f} {:0.2f}\n'.format(corrIndex, precisions[0], recalls[0], fScores[0], precisions[1], recalls[1], fScores[1], precisions[2], recalls[2], fScores[2], precisions[3], recalls[3], fScores[3]))#, precisions[4], recalls[4], fScores[4], precisions[5], recalls[5], fScores[5]))        

    with open(pathOutput, 'w') as f:
        f.write('Index KickP KickR KickF PossP PossR PossF TackleP TackleR TackleF DeflP DeflR DeflF OutP OutR OutF\n')
        eventList = ['KickingTheBall','BallPossession', 'Tackle', 'BallDeflection']
        for index in bestElements:
            precisions = [output[index]['KickingTheBall']['Precision'], output[index]['BallPossession']['Precision'], output[index]['Tackle']['Precision'], output[index]['BallDeflection']['Precision']]#, output[index]['BallOut']['Precision'], output[index]['Goal']['Precision']]
            recalls = [output[index]['KickingTheBall']['Recall'], output[index]['BallPossession']['Recall'], output[index]['Tackle']['Recall'], output[index]['BallDeflection']['Recall']]#, output[index]['BallOut']['Recall'], output[index]['Goal']['Recall']]
            fScores = [output[index]['KickingTheBall']['F-Score'], output[index]['BallPossession']['F-Score'], output[index]['Tackle']['F-Score'], output[index]['BallDeflection']['F-Score']]#, #output[index]['BallOut']['F-Score'], output[index]['Goal']['F-Score']]
            f.write('{} {:0.2f} {:0.2f} {:0.2f} {:0.2f} {:0.2f} {:0.2f} {:0.2f} {:0.2f} {:0.2f} {:0.2f} {:0.2f} {:0.2f}\n'.format(correspondingIndex[index], precisions[0], recalls[0], fScores[0], precisions[1], recalls[1], fScores[1], precisions[2], recalls[2], fScores[2], precisions[3], recalls[3], fScores[3]))#, precisions[4], recalls[4], fScores[4], precisions[5], recalls[5], fScores[5]))        

            visualize(precisions, recalls, fScores, eventList)

def visualize(precision_means, recall_means, fscore_means, eventList):
    ind = numpy.arange(len(precision_means))  # the x locations for the groups
    width = 0.20  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind - width, precision_means, width,
                    color='SkyBlue', label='Precision')
    rects2 = ax.bar(ind, recall_means, width,
                    color='IndianRed', label='Recall')
    rects3 = ax.bar(ind + width, fscore_means, width,
                    color='Green', label='F1 Score')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Percentage')
    ax.set_title('Precision/Recall/F1 score for each event')
    ax.set_yticks(numpy.arange(0, 1.1, 0.1))
    ax.set_xticks(ind)
    ax.set_xticklabels(eventList)
    ax.legend(bbox_to_anchor=(1, 1))

    plt.show()

def autolabel(rects, xpos='center'):
        """
        Attach a text label above each bar in *rects*, displaying its height.

        *xpos* indicates which side to place the text w.r.t. the center of
        the bar. It can be one of the following {'center', 'right', 'left'}.
        """

        xpos = xpos.lower()  # normalize the case of the parameter
        ha = {'center': 'center', 'right': 'left', 'left': 'right'}
        offset = {'center': 0.1, 'right': 0.4, 'left': 0.6}  # x_txt = x + w*off

        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()*offset[xpos], 1.01*height,
                    '{}'.format(height), ha=ha[xpos], va='bottom')

def createDetectorFile(parameterList, outputPath):
    #newParameterList = [int(par) for par in parameterList[:5]]+list(parameterList[5:8])+[parameterList[6]+parameterList[8]]+[parameterList[9]]
    #fileString = "KickingTheBall 1.0 {1} {5:.1f}\nBallPossession 1.0 {2} {6:.1f} {8:.1f}\nTackle 1.0 {2} {6:.1f} {8:.1f}\nBallDeflection 1.0 {3} {7:.1f} {9:.1f}\nBallOut 1.0 {4}".format(*newParameterList)
    newParameterList = [int(par) for par in parameterList[:5]]+list(parameterList[5:9])+[parameterList[6]+parameterList[9],parameterList[7]+parameterList[10]]+list(parameterList[11:])
    fileString = "KickingTheBall 3.0 {1} {5:.01f} {11:.1f}\nBallPossession 3.0 {2} {6:.01f} {9:.01f} {12:.1f}\nTackle 3.0 {3} {7:.01f} {10:.01f} {13:.1f}\nBallDeflection 3.0 {4} {8:.01f} {14:.1f} {15:.1f} 50.0\nBallOut 2.0 50\nGoal 1.0 50".format(*newParameterList)
    with open(outputPath, 'w') as f:
            f.write(fileString)
    return fileString.split('\n')

def createValidatorFile(parameterList, outputPath):
    #newParameterList = [int(par) for par in parameterList[:5]]+list(parameterList[5:])
    #fileString = "KickingTheBall 1.0 {1} {5:.1f}\nBallPossession 1.0 {2} {6:.1f} {8:.1f}\nTackle 1.0 {2} {6:.1f} {8:.1f}\nBallDeflection 1.0 {3} {7:.1f} {9:.1f}\nBallOut 1.0 {4}".format(*newParameterList)
    newParameterList = [int(par) for par in parameterList[:5]]
    fileString = 'KickingTheBall playerId teamId {1}\nBallPossession playerId teamId {2}\nTackle playerId teamId {3}\nBallDeflection playerId teamId {4}\nBallOut 500\nGoal team 100\nFoul 50\nPenalty 50'.format(*newParameterList)
    #fileString = 'KickingTheBall playerId teamId {1}\nBallPossession playerId teamId {2}\nTackle {3}\nBallDeflection playerId teamId {4}\nBallOut 500\nGoal 100\nFoul 50\nPenalty 50'.format(*newParameterList)

    with open(outputPath, 'w') as f:
            f.write(fileString)
    return fileString.split('\n')

def extractAllFeature(datasetPath, xDimension, yDimension, samplingRate, maxSize):
    generalParameters = [xDimension, yDimension, samplingRate, maxSize]
    print('Starting extraction of features')
    startAll = time()
    for subdir, dirs, files in os.walk(datasetPath):
        for directory in dirs:
            if (directory != '1st half') and (directory != '2nd half'):
                print('Starting processing of folder ' + directory)
                start = time()
                extractSingleMatch(generalParameters, datasetPath + directory + '//')
                elapsed = time() - start
                print('All processing in folder ended in {} seconds\n\n'.format(round(elapsed,1)))
    elapsedAll = time() - startAll
    print('All processing ended in {} seconds\n'.format(round(elapsedAll,1)))

def testAllMatch(individuals, datasetPath, xDimension, yDimension, samplingRate, maxSize, finalPath = None, test = False):
    detectorsFilename = 'detectors.txt'
    knowEventsFilename = 'events.txt'
    generalParameters = [xDimension, yDimension, samplingRate, maxSize]
    populationResult = [None for individual in individuals]
    # print('Starting validation of dataset')
    startAll = time()
    for subdir, dirs, files in os.walk(datasetPath):
        for directory in dirs:
            if (directory != '1st half') and (directory != '2nd half'):
                # print('Starting processing of folder ' + directory)
                start = time()
                createDetectorFile(individuals[0], detectorsFilename)
                featurePath = datasetPath + directory + '//' + 'features.log'
                annotationPath = datasetPath + directory + '//' + 'Annotations_AtomicEvents_Manual.xml'
                groundPath = datasetPath + directory + '//' + 'Annotations_AtomicEvents.xml'
                startPars = time()
                detector = DET('position.log', 'events.log', detectorsFilename, xDimension, yDimension, samplingRate, maxSize,
                               annotationFile=annotationPath, featurePath=featurePath)
                detector.extractAndCompact()
                directoryDataset = detector.dataset
                if (test):
                    sample = 1
                else:
                    sample = 3
                groundDictionary = XMLc.createDictionary(groundPath, samples=sample)
                elapsed = time() - start
                print('Parsing of dataset {} ended in {} seconds'.format(directory, round(elapsed,1)))
                for i,individual in enumerate(individuals):
                    start = time()
                    createDetectorFile(individual, detectorsFilename)
                    createValidatorFile(individual, knowEventsFilename)
                    results = testSingleMatch(individual, datasetPath + directory + '//', detectorsFilename, knowEventsFilename, generalParameters, i, directoryDataset, groundDictionary)
                    if (populationResult[i] is None):
                        populationResult[i] = results
                    else:
                        for event in populationResult[i]:
                            if (event != 'windowSize'):
                                populationResult[i][event]['TP'] += results[event]['TP']
                                populationResult[i][event]['FP'] += results[event]['FP']
                                populationResult[i][event]['FN'] += results[event]['FN']
                    elapsed = time() - start
                    #print('Detecting of individual {} ended in {} seconds'.format(i, round(elapsed,1)))
    for result,individual in zip(populationResult, individuals):
        result['KickingTheBall']['Precision'], result['KickingTheBall']['Recall'], result['KickingTheBall']['F-Score'] = calculateFScore(result['KickingTheBall']['TP'], result['KickingTheBall']['FP'], result['KickingTheBall']['FN'])
        result['BallPossession']['Precision'], result['BallPossession']['Recall'], result['BallPossession']['F-Score'] = calculateFScore(result['BallPossession']['TP'], result['BallPossession']['FP'], result['BallPossession']['FN'])
        result['Tackle']['Precision'], result['Tackle']['Recall'], result['Tackle']['F-Score'] = calculateFScore(result['Tackle']['TP'], result['Tackle']['FP'], result['Tackle']['FN'])
        result['BallDeflection']['Precision'], result['BallDeflection']['Recall'], result['BallDeflection']['F-Score'] = calculateFScore(result['BallDeflection']['TP'], result['BallDeflection']['FP'], result['BallDeflection']['FN'])
        result['BallOut']['Precision'], result['BallOut']['Recall'], result['BallOut']['F-Score'] = calculateFScore(result['BallOut']['TP'], result['BallOut']['FP'], result['BallOut']['FN'])
        result['Goal']['Precision'], result['Goal']['Recall'], result['Goal']['F-Score'] = calculateFScore(result['Goal']['TP'], result['Goal']['FP'], result['Goal']['FN'])    
    if (test):
        findBestAndVisualize(populationResult, finalPath)
    else:
        for result,individual in zip(populationResult, individuals):
            individual.fitness.values = (0.25*result['KickingTheBall']['Precision']+0.25*result['BallPossession']['Precision']+0.25*result['Tackle']['Precision']+0.25*result['BallDeflection']['Precision'],
                                         0.25*result['KickingTheBall']['Recall']+0.25*result['BallPossession']['Recall']+0.25*result['Tackle']['Recall']+0.25*result['BallDeflection']['Recall'])
    elapsedAll = time() - startAll
    print('Fitness computation ended in {} seconds\n'.format(round(elapsedAll,1)))


def testSingleMatch(individualList, folderPath, detectorsPath, validatorsPath, parameters, index, dataset, groundDictionary):
    positionPath = folderPath + 'position.log'
    featurePath = folderPath + 'features.log'
    eventStoragePath = folderPath + 'Annotations_AtomicEvents_Detected_{}.xml'.format(index)
    annotationPath = folderPath + 'Annotations_AtomicEvents_Manual.xml'
    groundPath = folderPath + 'Annotations_AtomicEvents.xml'
    outputPath = folderPath + 'Annotations_AtomicEvents_Results_{}.xml'.format(index)

    # print('Processing individual {}'.format(index))
    detector = DET(positionPath, eventStoragePath, detectorsPath, *parameters, annotationFile=annotationPath,
                   permutation=individualList[0], featurePath=featurePath, dataset=dataset)
    detector.startPostDetection()
    
    # print('Starting validation {}'.format(index))
    # start = time()
    detectedDictionary = XMLc.createAtomicDictionaryFromList(detector.eventList)
    currentValidator = AV(validatorsPath, groundDictionary, detectedDictionary, -1)
    currentValidator.validate()
    #XMLc.createOutputFile(currentValidator.output, outputPath)
    # elapsed = time() - start
    # print('Elapsed {} seconds\n'.format(round(elapsed,1)))
    return currentValidator.output['overall']

def compareAllMatchOptimized(individuals, datasetPath, xDimension, yDimension, samplingRate, maxSize, useFiles = True):
    detectorsFilename = 'detectors.txt'
    knowEventsFilename = 'events.txt'
    generalParameters = [xDimension, yDimension, samplingRate, maxSize]
    populationResult = [{'TP':0,'FP':0,'FN':0} for individual in individuals]
    # print('Starting validation of dataset')
    startAll = time()
    for subdir, dirs, files in os.walk(datasetPath):
        for directory in dirs:
            if (directory != '1st half') and (directory != '2nd half'):
                # print('Starting processing of folder ' + directory)
                start = time()
                createDetectorFile(individuals[0], detectorsFilename)
                featurePath = datasetPath + directory + '//' + 'features.log'
                annotationPath = datasetPath + directory + '//' + 'Annotations_AtomicEvents_Manual.xml'
                groundPath = datasetPath + directory + '//' + 'Annotations_AtomicEvents.xml'
                startPars = time()
                detector = DET('position.log', 'events.log', detectorsFilename, xDimension, yDimension, samplingRate, maxSize,
                               annotationFile=annotationPath, featurePath=featurePath)
                detector.extractAndCompact()
                directoryDataset = detector.dataset
                groundDictionary = XMLc.createDictionary(groundPath, samples=3)
                elapsed = time() - start
                print('Parsing of dataset {} ended in {} seconds'.format(directory, round(elapsed,1)))
                for i,individual in enumerate(individuals):
                    start = time()
                    createDetectorFile(individual, detectorsFilename)
                    createValidatorFile(individual, knowEventsFilename)
                    results = compareSingleMatchOptimized(individual, datasetPath + directory + '//', detectorsFilename, knowEventsFilename, generalParameters, i, directoryDataset, groundDictionary)
                    for j,key in zip(range(len(results)),populationResult[i]):
                        populationResult[i][key] += results[j]
                    elapsed = time() - start
                    #print('Detecting of individual {} ended in {} seconds'.format(i, round(elapsed,1)))
    for result,individual in zip(populationResult, individuals):
        precision = 0
        recall = 0
        precisionSum = (result['TP']+result['FP'])
        recallSum = (result['TP']+result['FN'])
        if (precisionSum != 0):
            precision = result['TP']/precisionSum
        if (recallSum != 0):
            recall = result['TP']/recallSum
        individual.fitness.values = (precision, recall)
    elapsedAll = time() - startAll
    print('Fitness computation ended in {} seconds\n'.format(round(elapsedAll,1)))

def compareSingleMatchOptimized(individualList, folderPath, detectorsPath, validatorsPath, parameters, index, dataset, groundDictionary):
    positionPath = folderPath + 'position.log'
    featurePath = folderPath + 'features.log'
    eventStoragePath = folderPath + 'Annotations_AtomicEvents_Detected_{}.xml'.format(index)
    annotationPath = folderPath + 'Annotations_AtomicEvents_Manual.xml'
    groundPath = folderPath + 'Annotations_AtomicEvents.xml'
    outputPath = folderPath + 'Annotations_AtomicEvents_Results_{}.xml'.format(index)

    # print('Processing individual {}'.format(index))
    detector = DET(positionPath, eventStoragePath, detectorsPath, *parameters, annotationFile=annotationPath,
                   permutation=individualList[0], featurePath=featurePath, dataset=dataset)
    detector.startPostDetection()
    
    # print('Starting validation {}'.format(index))
    # start = time()
    detectedDictionary = XMLc.createAtomicDictionaryFromList(detector.eventList)
    currentValidator = AV(validatorsPath, groundDictionary, detectedDictionary, -1)
    currentValidator.validate()
    #XMLc.createOutputFile(currentValidator.output, outputPath)
    # elapsed = time() - start
    # print('Elapsed {} seconds\n'.format(round(elapsed,1)))
    return [currentValidator.totalTruePositive, currentValidator.totalFalsePositive, currentValidator.totalFalseNegative]

def extractSingleMatch(parameters, folderPath):
    positionPath = folderPath + 'positions.log'
    annotationPath = folderPath + 'Annotations_AtomicEvents_Manual.xml'
    featurePath = folderPath + 'features.log'
    detectPath = folderPath + 'detectors.txt'

    extractor = DET(positionPath, None, detectPath, *parameters, annotationFile=annotationPath, featurePath=featurePath)
    extractor.startPreExtraction()

def rebound(ind, elementsRange):
    for i in range(len(ind)):
        if (ind[i] < elementsRange[i][0]):
            ind[i] = elementsRange[i][0]
        elif (ind[i] > elementsRange[i][1]):
            ind[i] = elementsRange[i][1]
        roundDecimal = elementsRange[i][2]
        ind[i] = float(Decimal(ind[i]).quantize(Decimal(roundDecimal), rounding=ROUND_HALF_EVEN))

def initFromRange(indc, elementsRange):
    "Crea gli individui, a partire da una lista di tuple contenente minimo, massimo e discretizzazione per ciascun valore"
    ind = indc(random.uniform(values[0],values[1]) for values in elementsRange)
    rebound(ind, elementsRange)
    return ind

def initFromFile(indc, filename, pop):
    index = [i for i in range(len(pop))]
    random.shuffle(index)
    i = 0
    with open(filename, 'r') as f:
        for line in f:
            j = index[i]
            pop[j] = indc(float(value) for value in line.rstrip('\n').split(" "))
            i += 1

def checkBounds(elementsRange):
    def decorator(func):
        def wrapper(*args, **kargs):
            offspring = func(*args, **kargs)
            for child in offspring:
                rebound(child, elementsRange)
            return offspring
        return wrapper
    return decorator

def checkCondition(individuals):
    for individual in individuals:
        if (individual.fitness.values == (1.0, 1.0)):
            return True
    return False

def logStats(population, archive, index, logbook):
    pop = []
    for ind in population:
        find = False
        for arc in archive:
            if (ind == arc):
                find = True
                break
        if not(find):
            pop.append(ind)
    precisionPopValues = []
    recallPopValues = []
    precisionArcValues = []
    recallArcValues = []
    for ind in pop:
        precisionPopValues.append(ind.fitness.values[0])
        recallPopValues.append(ind.fitness.values[1])  
    for ind in archive:
        precisionArcValues.append(ind.fitness.values[0])
        recallArcValues.append(ind.fitness.values[1]) 
    maximumValue = max(max(precisionArcValues),max(recallArcValues))
    for i in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]:
        if maximumValue < i:
            maximumValue = i
            break
    minimumValue = min(min(precisionArcValues),min(recallArcValues))
    for i in [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]:
        if minimumValue > i:
            minimumValue = i
            break
    plt.clf()
    plt.plot(precisionPopValues, recallPopValues,'ko', markersize=5)
    plt.plot(precisionArcValues, recallArcValues,'ro', markersize=5)
    plt.xlabel('Precision')
    plt.ylabel('Recall')
    plt.axis([minimumValue,maximumValue,minimumValue,maximumValue])
    plt.savefig("Results/ArchiveGen_{}.png".format(index))

    with open('Results/ArchiveGen_{}.txt'.format(index), 'w') as f:
            for element in archive:
                f.write('{:1.0f} {:1.0f} {:1.0f} {:1.0f} {:1.0f} {:.2f} {:.2f} {:.2f} {:.2f} {:.2f} {:.2f} {:.1f} {:.1f} {:.1f} {:.1f} {:.1f}\n'.format(*element))
    
    with open('Results/ArchiveFitnessGen_{}.txt'.format(index), 'w') as f:
            for element in archive:
                f.write('{} {}\n'.format(*element.fitness.values))
    
    with open('Results/PopulationGen_{}.txt'.format(index), 'w') as f:
            for element in population:
                f.write('{:1.0f} {:1.0f} {:1.0f} {:1.0f} {:1.0f} {:.2f} {:.2f} {:.2f} {:.2f} {:.2f} {:.2f} {:.1f} {:.1f} {:.1f} {:.1f} {:.1f}\n'.format(*element))
    
    with open('Results/PopulationFitnessGen_{}.txt'.format(index), 'w') as f:
            for element in population:
                f.write('{} {}\n'.format(*element.fitness.values))
    
    with open("Results/StatisticsGen_{}.txt".format(index),'w') as f:
            f.write("Gen AvgPrecision MaxPrecision AvgRecall MaxRecall StdPrecision StdRecall\n")
            avgVals, maxVals, stdVals = logbook.select('avg', 'max','std')
            i = 0
            for avgV, maxV, stdV in zip(avgVals, maxVals, stdVals):
                f.write("{} {} {} {} {} {} {}\n".format(i, avgV[0], maxV[0], avgV[1], maxV[1], stdV[0], stdV[1]))
                i += 1


def startOptimization(populationSize, archiveSize, nOfGenerations, crossoverProbability, mutationProbability, arguments, finalPath):

    #list of parameters with limit range and discretization
    attributeRange = [(0.0,119.0,'1.'),(3.0,30.0,'1.'),(3.0,30.0,'1.'),(3.0,30.0,'1.'),(3.0,30.0,'1.'),
                      (0.1,2.0,'.01'),(0.1,2.0,'.01'),(0.1,2.0,'.01'),(0.1,2.0,'.01'),
                      (0.1,1.0,'.01'),(0.1,1.0,'.01'),
                      (1.0,15.0,'.1'),(1.0,15.0,'.1'),(1.0,15.0,'.1'),(1.0,15.0,'.1'),
                      (5.0,30.0,'.1'),]
    # variance for each parameter on which the Gaussian mutation acts
    sigma = [1, 1, 1, 1, 1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 1.0, 1.0, 1.0, 1.0, 1.0]
    
    creator.create("FitnessPrecRec", base.Fitness, weights=(0.8, 1.2))
    creator.create("Individual", array.array, typecode='f', fitness=creator.FitnessPrecRec)

    history = tools.History()
    logbook = tools.Logbook()
    stats = tools.Statistics(key=lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean, axis=0)
    stats.register("std", numpy.std, axis=0)
    stats.register("min", numpy.min, axis=0)
    stats.register("max", numpy.max, axis=0)

    toolbox = base.Toolbox()
    toolbox.register("individual", initFromRange, creator.Individual, attributeRange)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("populationFromFile", initFromFile, creator.Individual, "seed.txt")
    toolbox.register("check", checkCondition)
    toolbox.register("evaluate", testAllMatch)
    toolbox.register("selectEnvironment", tools.selSPEA2, k=archiveSize)
    toolbox.register("selectMating", tools.selTournament, k=populationSize, tournsize=2)
    toolbox.register("mate", tools.cxBlend, alpha=0.5)
    toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=sigma, indpb=1.0)
    toolbox.decorate("mate", checkBounds(attributeRange))
    toolbox.decorate("mutate", checkBounds(attributeRange))
    toolbox.decorate("mate", history.decorator)
    toolbox.decorate("mutate", history.decorator)
    toolbox.register("logFront", logStats)

    print('Initializing algorithm')
    startAllTime=time()

    # print('Initializing population')
    # startTime=time()
    population = toolbox.population(n = populationSize)
    toolbox.populationFromFile(population)
    # elapsedTime = time()-startTime
    # print('Elapsed {} s'.format(elapsedTime))
    
    history.update(population)

    output = None
    archive = []
    condition = False
    currentGeneration = 0
    while not(condition):
        print("Generation {}".format(currentGeneration))
        startTime=time()
        
        toolbox.evaluate(population,*arguments, test=False)

        # print('Starting environment selection')
        # startTime=time()
        archive = toolbox.selectEnvironment(population + archive)
        # elapsedTime = time()-startTime
        # print('Elapsed {} s\n'.format(elapsedTime))
        
        # Salva le statistiche e crea un grafico della generazione corrente
        record = stats.compile(archive)
        logbook.record(gen=currentGeneration, **record)
        avgV, maxV, minV, stdV = logbook.select('avg', 'max', 'min', 'std')
        a = currentGeneration
        print("Gen: {}\nAverage precision: {}\nMaximum precision: {}\nAverage recall: {}\nMaximum recall: {}\nStandard precision: {}\nStandard recall: {}\n\n".format(a, avgV[a][0], maxV[a][0], avgV[a][1], maxV[a][1], stdV[a][0], stdV[a][1]))
        toolbox.logFront(population, archive, currentGeneration, logbook)

        condition = toolbox.check(archive)
        if(currentGeneration >= nOfGenerations) or condition: 
            toolbox.evaluate(archive,*arguments, finalPath=finalPath, test=True)
            output = archive
            break
        else:
            # print('Starting mating selection')
            # startTime=time()
            offspring = map(toolbox.clone, toolbox.selectMating(archive))
            # elapsedTime = time()-startTime
            # print('Elapsed {} s\n'.format(elapsedTime))
        
            # print('Starting crossover and mutation')
            # startTime=time()
            offspring = algorithms.varAnd(offspring, toolbox, crossoverProbability, mutationProbability)
            # elapsedTime = time()-startTime
            # print('Elapsed {} s\n'.format(elapsedTime))

            population[:] = offspring

            for ind in population:
                del ind.fitness.values
            currentGeneration += 1
            
            elapsedTime = time()-startTime
            print('Elapsed {} s\n'.format(elapsedTime))
    elapsedAllTime = time()-startAllTime
    print('Algorithm terminated in {} h\n'.format(elapsedAllTime/3600))
    if (output is None):
        raise Exception("Algorithm terminated without returning values!")
    #else:        
    #    plt.clf()
    #    graph = networkx.DiGraph(history.genealogy_tree)
    #    graph = graph.reverse()
    #    networkx.draw(graph)
    #    plt.savefig("Results/GenerationalGraph.png")


def main():
    individuals = []
    individuals.append([0, 25, 25, 25, 50, 0.5, 0.5, 0.5, 1.5, 90.0])
    individuals.append([100, 30, 30, 30, 40, 1.0, 1.0, 1.0, 1.5, 125.0])

    parser = argparse.ArgumentParser()
    parser.add_argument("datasetPath", help="Path to the dataset")
    parser.add_argument("-m", "--maxSize", type=int, default=1024, help="Maximum space taken by the detector (couldn't eccess maximum RAM size)")
    parser.add_argument("-s", "--samplingRate", type=int, default=10, help="Sampling rate at which the positional data were taken")
    parser.add_argument("-x", "--xDimension", type=int, default=110, help="Horizontal size of the pitch")
    parser.add_argument("-y", "--yDimension", type=int, default=60, help="Vertical size of the pitch")
    parser.add_argument("-mo", "--mode", type=str, default='FEATURE', help="Use FEATURE to extract all features from a folder and OPTIMIZE to start optimizing")
    parser.add_argument("-ps", "--populationSize", type=int, default=20, help="Size of the population")
    parser.add_argument("-as", "--archiveSize", type=int, default=10, help="Size of the archive")
    parser.add_argument("-n", "--numberOfGeneration", type=int, default=10, help="Number of generation")
    parser.add_argument("-c", "--crossoverProbability", type=float, default=0.5, help="Probability of crossover")
    parser.add_argument("-mu", "--mutationProbability", type=float, default=0.5, help="Probability of mutation")
    parser.add_argument("-se", "--seed", type=str, default='file', help="Seed for test or genetic algorithm")
    parser.add_argument("-fo", "--finalOutput", type=str, default='Results/FinalResults.txt', help="Seed for test or genetic algorithm")
    args = parser.parse_args()
    datasetPath = args.datasetPath
    maxSize = args.maxSize
    samplingRate = args.samplingRate
    xDimension = args.xDimension
    yDimension = args.yDimension
    populationSize = args.populationSize
    archiveSize = args.archiveSize
    nOfGeneration = args.numberOfGeneration
    crossProbability = args.crossoverProbability
    mutProbability = args.mutationProbability
    seed = args.seed
    finalOutput = args.finalOutput
    if os.path.exists("Result"):
        makedirs("Result")
    if not(os.path.isdir(datasetPath)):
        raise Exception("No directory with such name found!")
    if (args.mode == 'FEATURE'):
        extractAllFeature(datasetPath,xDimension,yDimension,samplingRate,maxSize)
    elif (args.mode == 'TEST'):
        population = []
        with open(seed,'r') as f:
            for line in f:
                population.append([float(value) for value in line.rstrip('\n').split(" ")])
        testAllMatch(population, datasetPath, xDimension,yDimension,samplingRate,maxSize, finalPath=finalOutput, test=True)
    elif (args.mode == 'OPTIMIZE'):
        startOptimization(populationSize,archiveSize, nOfGeneration, crossProbability, mutProbability, [datasetPath, xDimension,yDimension,samplingRate,maxSize], finalPath=finalOutput)  
    else:
        raise Exception("Mode {} isn't a valid parameter".format(args.mode))

def main2():
    #startOptimization(1,1,1,1)
    print('a')

if __name__ == '__main__':
    main()

