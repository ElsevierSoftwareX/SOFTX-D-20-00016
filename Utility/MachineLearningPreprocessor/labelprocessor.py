import os
import os.path as PATH
import argparse
import dicttoxml
import xml.etree.ElementTree as ET
import xml.dom.minidom as DOM

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
                                        labels.append([frameValue, 1])
                                    elif ('Tackle' == eventAttributes['name']):
                                        labels.append([frameValue, 2])
                                    elif ('KickingTheBall' == eventAttributes['name']):
                                        labels.append([frameValue, 3])
                                    elif ('BallOut' == eventAttributes['name']):
                                        labels.append([frameValue, 4])
                                    elif ('BallPossession' == eventAttributes['name']):
                                        labels.append([frameValue, 5])
                            else:        
                                if ('BallDeflection' == eventAttributes['name']):
                                    labels.append([frameValue, 1])
                                elif ('Tackle' == eventAttributes['name']):
                                    labels.append([frameValue, 2])
                                elif ('KickingTheBall' == eventAttributes['name']):
                                    labels.append([frameValue, 3])
                                elif ('BallOut' == eventAttributes['name']):
                                    labels.append([frameValue, 4])
                                elif ('BallPossession' == eventAttributes['name']):
                                    labels.append([frameValue, 5])
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
        numFrames = int(lastLine.split(" ")[0])

        newLabels = []
        for i in range(0, numFrames):
            labelInFrame = dictionary.get(i)
            if (labelInFrame is not None):
                newLabels.append(labelInFrame)
            else:
                newLabels.append(0)

    return newLabels[:-6]

def printLabels(path):
    labels = getLabels(path)

    with open(PATH.join(path, 'labels.txt'),'w') as f:
        for label in labels:
            f.write('{}\n'.format(label))

def main():
    datasetPath = 'dataset/training'
    for subdir, dirs, files in os.walk(datasetPath):
        for directory in dirs:
            printLabels(PATH.join(datasetPath, directory))

if __name__ == "__main__":
    main()

