# coding=UTF-8
import os
import numpy as np, time
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import argparse

def visualize(precision_means, recall_means, fscore_means, eventList):

    # Start measuring time
    start = time.time()

    ind = np.arange(len(precision_means))  # the x locations for the groups
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
    ax.set_yticks(np.arange(0, 1.1, 0.1))
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

class XML():
    @staticmethod
    def createValuesictionary(filename):
        dictionary = {}
        
        tree = ET.parse(filename)
        annotations = tree.getroot()
        if (annotations.tag != 'results'):
            raise Exception('No /results found in XML')
        else:
            if (annotations[0].tag != 'overall'):
                raise Exception('No /overall found in XML')
            else:
                overall = annotations[0]
                for event in overall:
                    if (event.tag != 'windowSize') and (event.tag != 'percentage'):
                        dictionary[event.tag] = {}
                        for value in event:
                            dictionary[event.tag][value.tag] = float(value.text)
            
        return dictionary

def searchInThisPath():
    resultDictionary = None    
    for subdir, dirs, files in os.walk('./'):
        for directory in dirs:
            if (directory == 'BestSamples'):
                for subdir1, dirs1, files1 in os.walk(directory):
                    for f in files1:
                        if (resultDictionary is None):
                            resultDictionary = XML.createValuesictionary(os.path.join(directory,f))
                        else:
                            newResultDictionary = XML.createValuesictionary(os.path.join(directory,f))
                            for event, newEvent in zip(resultDictionary, newResultDictionary):
                                if (event != newEvent):
                                    raise Exception('Different XML files!')
                                else:
                                    resultDictionary[event]['TP'] += newResultDictionary[newEvent]['TP']
                                    resultDictionary[event]['FP'] += newResultDictionary[newEvent]['FP']
                                    resultDictionary[event]['FN'] += newResultDictionary[newEvent]['FN']
            else:
                break
    return resultDictionary

def aggregateFromDatasetPath(path, filename):
    if not (os.path.isdir(path)):
        raise Exception('Not a correct path!') 
    resultDictionary = None    
    for subdir, dirs, files in os.walk(path):
        for directory in dirs:
            for subdir1, dirs1, files1 in os.walk(os.path.join(path, directory)):
                for f in files1:
                    if (f == filename):
                        if (resultDictionary is None):
                            resultDictionary = XML.createValuesictionary(os.path.join(path, directory,f))
                        else:
                            newResultDictionary = XML.createValuesictionary(os.path.join(path, directory,f))
                            for event, newEvent in zip(resultDictionary, newResultDictionary):
                                if (event != newEvent):
                                    raise Exception('Different XML files!')
                                else:
                                    resultDictionary[event]['TP'] += newResultDictionary[newEvent]['TP']
                                    resultDictionary[event]['FP'] += newResultDictionary[newEvent]['FP']
                                    resultDictionary[event]['FN'] += newResultDictionary[newEvent]['FN']
    return resultDictionary

def check(resultDictionary): 
    if (resultDictionary is None):
        raise Exception('Dictionary not formed!')
    else:
        resultDictionary['TOTAL'] = {'TP':0, 'FP':0, 'FN':0}
        for event in resultDictionary:
            if (event != 'TOTAL'):
                resultDictionary['TOTAL']['TP'] += resultDictionary[event]['TP']
                resultDictionary['TOTAL']['FP'] += resultDictionary[event]['FP']
                resultDictionary['TOTAL']['FN'] += resultDictionary[event]['FN']
        for event in list(resultDictionary.keys()):
            if (event == 'Goal') or (event == 'Foul') or (event == 'Penalty'):
                del resultDictionary[event]

        precisionScore = []
        recallScore = []
        fscoreScore = []
        for i,event in enumerate(resultDictionary):
            precisionFraction = resultDictionary[event]['TP']+resultDictionary[event]['FP']
            recallFraction = resultDictionary[event]['TP']+resultDictionary[event]['FN']
            if (precisionFraction != 0):
                precisionScore.append(round(resultDictionary[event]['TP']/precisionFraction, 2))
            else:
                precisionScore.append(0)
            
            if (recallFraction != 0):
                recallScore.append(round(resultDictionary[event]['TP']/recallFraction, 2))
            else:
                recallScore.append(0)

            fScoreFraction = recallScore[i]+precisionScore[i]
            if (fScoreFraction != 0): 
                fscoreScore.append( round(2 * recallScore[i]*precisionScore[i]/fScoreFraction,2))
            else:
                fscoreScore.append(0)
            print('{} results:\n\tPrecision: {}\n\tRecall: {}\n\tF1 Score: {}\n\n'.format(event, precisionScore[i],recallScore[i],fscoreScore[i]))
        
        eventList = resultDictionary.keys()
        visualize(tuple(precisionScore),tuple(recallScore),tuple(fscoreScore), eventList)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--datasetPath", help="Path to the dataset")
    parser.add_argument("-f", "--fileName", default="Annotations_AtomicEvents_Results.xml", help="Path to the dataset")
    args = parser.parse_args()
    
    if (args.datasetPath is None):
        resultDictionary =  searchInThisPath()
    else:
        resultDictionary = aggregateFromDatasetPath(args.datasetPath, args.fileName)
    check(resultDictionary)