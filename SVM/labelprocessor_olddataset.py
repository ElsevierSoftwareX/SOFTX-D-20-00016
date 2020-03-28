import os
import os.path as PATH
import argparse
import dicttoxml
import xml.etree.ElementTree as ET
import xml.dom.minidom as DOM
import numpy

WINDOW_SIZE = 30
STRIDE = 1

DEBUG = True

GOALKEEPER0 = 0
GOALKEEPER1 = 18    # Qui non si considera il +128

class XML():    
    @staticmethod
    def createDictionary(filename, samples = 1):
        """
        Crea un dizionario di eventi a partire dal nome del file contenenti gli eventi. Il file degli eventi è un XML così organizzato:
        <annotations>
            <metadata>
                ...
            </metadata>
            <track id=1 label="NomeEvento1">
                <box frame=-frame inizio evento- ...>
                    <attribute name="nomeAttributo1"> -valore attributo 1- </attribute>
                    <attribute name="nomeAttributo2"> -valore attributo 2- </attribute>
                </box>
            </track>
            <track id=2 label="NomeEvento2">
            ...
            
        :param filename: Stringa con il percorso al file XML
        :return: Dizionario con tutti gli eventi nell'XML
        """
        labels = []
        oldAttributes = None
        oldFrame = -1
        frameCount = 0
        trackCounter = 1

        tree = ET.parse(filename)
        annotations = tree.getroot()
        if (annotations.tag != 'annotations'):
            raise Exception('No /annotations found in XML')
        else:
            for track in annotations:
                frameValue = -1
                lengthValue = 0
                eventName = None
                if (track.tag == 'track'):
                    if (track.attrib.get('id') is None):
                         raise Exception('No attribute "id" in /track')
                    else:
                        if (int(track.attrib['id']) != trackCounter):
                           # raise Exception('TrackCounter is {} instead of {}'.format(track.attrib['id'], trackCounter)) 
                           trackCounter += 1
                        else:
                            trackCounter += 1
                    # Aggiungere eventlist e controllare che label sia in eventlist
                    if (track.attrib.get('label') is None):
                        raise Exception('No attribute "label" in /track')
                    else:
                        eventName = track.attrib['label']
                    
                    eventAttributes = {'name' : eventName, 'track' : trackCounter - 1}
                    box = track[0]
                    if (box.tag != 'box'):
                        raise Exception('No /box found in /track')
                    else:
                        if (box.attrib.get('frame') is None):
                             raise Exception('No attribute "frame" in /box')
                        else:
                            frameValue = int(box.attrib['frame'])
                            for attribute in box:
                                if (attribute.tag != 'attribute'):
                                    raise Exception('No /attribute found in /box')
                                else:
                                    if (attribute.attrib.get('name') is None):
                                        raise Exception('No attribute "name" in /attribute')
                                    else:
                                        eventAttributes[attribute.attrib['name']] =  attribute.text
                            for boxFrame in track:
                                lengthValue += 1
                            if (lengthValue > 1):
                                eventAttributes['finalFrame'] = frameValue + lengthValue - 1
                            
                            if not (oldAttributes is None):
                                if (oldFrame != frameValue):
                                    if ('BallDeflection' == eventAttributes['name']):
                                        # Considero solo le BallDeflection dei portieri
                                        if (eventAttributes["playerId"] == GOALKEEPER0 or eventAttributes["playerId"] == GOALKEEPER1):  
                                            labels.append([frameValue, 1])
                                        else:
                                            labels.append([frameValue, 0])
                                    elif ('Tackle' == eventAttributes['name']):
                                        labels.append([frameValue, 0])
                                    elif ('KickingTheBall' == eventAttributes['name']):
                                        labels.append([frameValue, 0])
                                    elif ('BallOut' == eventAttributes['name']):
                                        labels.append([frameValue, 0])
                                    elif ('BallPossession' == eventAttributes['name']):
                                        labels.append([frameValue, 0])
                            else:        
                                if ('BallDeflection' == eventAttributes['name']):
                                    # Considero solo le BallDeflection dei portieri
                                    if (eventAttributes["playerId"] == GOALKEEPER0 or eventAttributes["playerId"] == GOALKEEPER1):  
                                        labels.append([frameValue, 1])
                                    else:
                                        labels.append([frameValue, 0])
                                elif ('Tackle' == eventAttributes['name']):
                                    labels.append([frameValue, 0])
                                elif ('KickingTheBall' == eventAttributes['name']):
                                    labels.append([frameValue, 0])
                                elif ('BallOut' == eventAttributes['name']):
                                    labels.append([frameValue, 0])
                                elif ('BallPossession' == eventAttributes['name']):
                                    labels.append([frameValue, 0])
                            oldAttributes = eventAttributes
                            oldFrame = frameValue

        return labels

    @staticmethod
    def getHalfTimeFrame(filename):
        result = 54000000
        tree = ET.parse(filename)
        annotations = tree.getroot()
        if (annotations.tag != 'annotations'):
            raise Exception('No /annotations found in XML')
        else:
            for track in annotations:
                if (track.tag == 'track'):
                    if (track.attrib.get('id') is None):
                        raise Exception('No attribute "id" in /track')
                    elif (int(track.attrib['id']) == 0):
                        if (track.attrib.get('label') is None):
                            raise Exception('No attribute "label" in /track')
                        elif(track.attrib['label'] != 'SecondHalf'):
                            raise Exception('This track has an id = 0 but is not a second half!')
                        else:
                            box = track[0]
                            if (box.tag != 'box'):
                                raise Exception('No /box found in /track')
                            else:
                                if (box.attrib.get('frame') is None):
                                    raise Exception('No attribute "frame" in /box')
                                else:
                                    result = int(box.attrib['frame'])
        return result


def getLabels(path):
    annotationPath = PATH.join(path, 'Annotations_AtomicEvents_Manual.xml')
    eventPath = PATH.join(path, 'Annotations_AtomicEvents.xml')
    halfTimeFrame = XML.getHalfTimeFrame(annotationPath)
    labels = XML.createDictionary(eventPath)

    dictionary = {}
    for element in labels:
        if (dictionary.get(element[0]) is None):
            dictionary[element[0]] = element[1]
        else:
            # Se il nuovo elemento ha priorità maggiore (più è alta la priorità più basso è il valore), allora sostituisci il vecchio valore
            if (element[1] < dictionary.get(element[0])):
                dictionary[element[0]] = element[1]

    # find the last line, change to a file you have
    with open(PATH.join(path, 'positions.log')) as f:
        lastLine = list(f)[-1]
        # Numero totale di frame per questa partita
        numFrames = int(lastLine.split(" ")[0])

        num = 0

        newLabels = []
        for i in range(0, numFrames):
            # Se sto usando uno stride, devo saltare un certo numero di frame
            if (i % STRIDE != 0):
                continue
            # All'inizio non devo considerare le entry che non hanno abbastanza dati per riempire una finestra
            if (i < WINDOW_SIZE - 1):
                continue
            
            num = num + 1
            labelInFrame = dictionary.get(i)
            if (labelInFrame is not None):
                newLabels.append(labelInFrame)
                if (DEBUG and (i < 50 or i > numFrames - 50)):
                    print(i, labelInFrame)
            else:
                newLabels.append(0)
                if (DEBUG and (i < 50 or i > numFrames - 50)):
                    print(i, 0)

    if (DEBUG):
        print(num)

    return newLabels


def printLabels(path):
    labels = getLabels(path)
    labels = removeDeleted(labels, path)

    n0 = 0
    n1 = 0

    with open(PATH.join(path, 'labels.txt'),'w') as f:
        for label in labels:
            f.write('{}\n'.format(label))
            if (label == 0):
                n0 += 1
            else:
                n1 += 1

    print("[INFO] Class 0 = {}\n[INFO] Class 1 = {}".format(n0, n1))


def removeDeleted(labels, path):
    inputDeletedSamplesFile = os.path.join(path, 'deletedSamples.log')

    removed = 0
    to_remove = []
    with open(inputDeletedSamplesFile, "r") as f:
        for line in f.readlines():
            if (removed != 0):
                shifted_index = int(line) - 29
                if (shifted_index >= 0):
                    to_remove.append(shifted_index)
            removed += 1

    deleteIndex = numpy.asarray(to_remove, dtype=numpy.int32)
    #for index in deleteIndex:
        #if (labels[index] == 1):
        #    print("[DELETING] Elem of class 1 at pos = {}".format(index))
    for index in deleteIndex:
        try:
            if (labels[index] == 1):
                print("[DELETING] Elem {} at pos = {}".format(labels[index], index))
        except:
            print("[DELETING] Elem None at pos = {}".format(index))
        
    print("len(labels) =", len(labels), "lastIndexToDelete =", deleteIndex[-1], "\n\n\n")
    
    labels = numpy.delete(labels, deleteIndex, 0)
    print("[INFO] Deleted {} samples.\n".format(len(deleteIndex)))
    return labels



def main():
    datasetPath = 'dataset/training'
    for subdir, dirs, files in os.walk(datasetPath):
        for directory in dirs:
            if (not directory.startswith(".")):
                print("\n[INFO] Processing directory {}.".format(directory))
                printLabels(PATH.join(datasetPath, directory))
            else:
                print("\n[INFO] Skipping directory {}.".format(directory))

if __name__ == "__main__":
    main()

