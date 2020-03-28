# coding=UTF-8
import pprint
import os.path as PATH
import argparse
import dicttoxml
import xml.etree.ElementTree as ET
import xml.dom.minidom as DOM
from multiprocessing import Process,Queue
from time import time

def is_integer(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

class AtomicProcessor(Process):
    def __init__(self, queue, idx, event, ground, detected, window):
        super(AtomicProcessor,self).__init__()
        self.queue = queue
        self.idx = idx
        self.eventListFile = event
        self.groundDictionary = ground
        self.detectedDictionary = detected
        self.windowSize = window
    def run(self):
        try:
            print("Starting process {}".format(self.idx))
            atomic = AtomicValidator(self.eventListFile, self. groundDictionary, self.detectedDictionary, self.windowSize)
            atomic.validate()
            #self.queue.put(atomic.output)
            print("Ending process {}".format(self.idx))
        except:
            print('ERROR: exiting process {}!'.format(self.idx))

class XML():
    @staticmethod
    def createAtomicDictionaryFromList(eventList):
        dictionary = {}
        id = 1
        for event in eventList:
            eventTimestamp = str(int(event['timestamp']))
            eventAttributes = {'name' : event['event'], 'track' : id}
            for key in event:
                if (key != 'event') and (key != 'timestamp'):
                    eventAttributes[key] = str(event[key])
            dictionary[eventTimestamp] = eventAttributes
            id += 1
        return dictionary
    
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
        dictionary = {}
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
                                if ('BallPossession' == eventAttributes['name']) and (oldFrame + 1 == frameValue) and (frameCount < samples -1 ):
                                    frameCount += 1
                                elif ('BallOut' == oldAttributes['name']) or ('Goal' == oldAttributes['name']):
                                    if (oldFrame == frameValue):
                                        frameCount = 0
                                else:
                                    frameCount = 0
                                    dictionary[str(frameValue)] = eventAttributes
                            else:        
                                dictionary[str(frameValue)] = eventAttributes
                            oldAttributes = eventAttributes
                            oldFrame = frameValue
        return dictionary
    
    @staticmethod
    def createOutputFile(dictionary, filename):
        """
        Crea un file xml con gli eventi riconosciuti a partire da un dizionario. 
        L'XML creato sarà così organizzato:
        <results>
            <overall>
                <nomeEvento1>
                    <total> -numero occorrenze totali dell'evento nel ground truth- </total>
                    <TP> -numero occorrenze di veri positivi dell'evento - </TP>
                    <FN> -numero occorrenze di falsi negativi dell'evento- </TN>
                    <FP> -numero occorrenze di falsi positivi dell'evento- </FP>
                </nomeEvento1>
                <nomeEvento2>
                ...
            </overall>
            <ground>
                <frame number=1>
                    <name> "nomeEvento" </name>
                    <track> -numero della track- </track>
                    <match> True/False </match>
                <frame>
                <frame number=2>
                ...
            </ground>
            <detected>
                come ground ma per gli eventi rilevati dal detector, ma aggiunge la percentuale/distanza
                dall'evento del ground truth per quelli che sono rilevati
            </detected>
        </results>
            
        :param dictionary: Dizionario da convertire in XML
        :param filename: Stringa con il percorso al file XML di output
        :return: Dizionario con tutti gli eventi nell'XML
        """
        #dicttoxml.set_debug()
        output = dicttoxml.dicttoxml(dictionary, custom_root='results', attr_type=False)
        xml = DOM.parseString(output)
        with open(filename, 'w') as f:
            f.write(xml.toprettyxml())

class BaseValidator():
    """
    Classe base che compara gli eventi nel ground truth con quelli rilevati.
    Verrà specializzata dalle classi figlie, una per gli eventi atomici e una per quelli complessi.
    """
    def __init__(self, eventListFile, groundDictionary, detectedDictionary):
        """
        :param eventListFile:  File con i parametri da confrontare per ciasciun evento
        :param groundDictionary: Dizionario con gli eventi del ground truth
        :param detectedDictionary: Dizionario con gli eventi rilevati
        """
        self.atomic = True
        self.groundDictionary = groundDictionary
        self.detectedDictionary = detectedDictionary
        self.knownEvent = self._populateKnowEventList(eventListFile)
        # lista di dizionari con tutti gli eventi, positivo/negativo
        self.output =  {}
        self.output['overall'] = self._populateOutputDictionary(self.knownEvent)
        self.output['ground'] = self._populateOutputDictionary(self.groundDictionary)
        self.output['detected'] = self._populateOutputDictionary(self.detectedDictionary)
        self.totalTruePositive = 0
        self.totalFalseNegative = 0
        self.totalFalsePositive = 0
    
    def validate(self):
        """
        Per ogni evento nel ground truth controlla se è nella vista degli eventi accettata.
        A questo punto chiama la funzione che confronta gli eventi e seguirà logiche diverse
        in base alla classe in cui verrà definita
        """
        for frame in self.groundDictionary:
            eventFoundName = None
            for eventName in self.knownEvent:
                if (eventName == self.groundDictionary[frame]['name']):
                    eventFoundName = eventName
                    break
            if (eventFoundName is None):
                raise Exception('Malformed dictionary, event {} does not match accepted event'.format(self.groundDictionary[frame]['name']))
            else:
                self._compareEvent(True, frame, eventFoundName)    
        for frame in self.detectedDictionary:
            eventFoundName = None
            for eventName in self.knownEvent:
                if (eventName == self.detectedDictionary[frame]['name']):
                    eventFoundName = eventName
                    break
            if (eventFoundName is None):
                raise Exception('Malformed dictionary, event {} does not match accepted event'.format(self.groundDictionary[frame]['name']))
            else:
                if not (self.output['detected'][frame]['match']):
                    self._compareEvent(False, frame, eventFoundName)
        self._calculateOutputOverall()
    def _subsampleEvents(self, sample):
        for key in list(self.groundDictionary.keys()):
            if not(self.groundDictionary.get(key) is None):
                eventName = self.groundDictionary[key]['name']
                for i in range(1, sample+1):
                    nextKey = str(int(key)+i)
                    if not (self.groundDictionary.get(nextKey) is None):
                        if (self.groundDictionary[nextKey]['name'] == eventName):
                            del self.groundDictionary[nextKey]
                        else:
                            break
    
    def _populateKnowEventList(self, file):
        """
        Popola la lista con gli eventi riconosciuti dal detector e gli attributi che dovrà confrontare
        Questi saranno presenti in un file di testo in cui ciasciuna linea avrà la seguente struttura:
        nomeEvento attributoEvento1 attributoEvento2 attributoEvento3 ...
        
        :param file: File con la lista eventi 
        :return: Dizionario con tutti gli eventi da riconoscere, la chiave è il nome dell'evento
        """
        newDictionary = {}
        if (PATH.isfile(file)):
            with open(file, 'r') as f:
                for line in f :
                    elements = line.rstrip('\n').split(" ")
                    newDictionary[elements[0]] = elements[1:]
        elif (type(file) is list):
            for line in f :
                    elements = line.rstrip('\n').split(" ")
                    newDictionary[elements[0]] = elements[1:]
        return newDictionary
        
    def _populateOutputDictionary(self, dictionary):
        """
        Crea un dizionario con gli eventi da confrontare, contenente solo nome, track e se è stato trovato o meno
        Inizializzo tutto a False così poi mi limito a rendere True quelli corrispondenti

        :param dictionary: Dizionario di cui creare una formattazione di base
        :return: Dizionario creato
        """
        newDictionary = {}
        for key in dictionary:
            if (isinstance( dictionary[key], list) ):
                newDictionary[key] = {'total'   : 0,
                                      'TP'      : 0,
                                      'FP'      : 0,
                                      'FN'      : 0}
            else:   
                newDictionary[key] = {'name'    :   dictionary[key]['name'],
                                      'track'   :   dictionary[key]['track'],
                                      'match'   :   False}
        return newDictionary
    
    def _compareEvent(self, isGround, frame, eventFoundName):
        "Compara gli eventi in base all'algoritmo scelto fra atomici e complessi"
        pass
    
    def _compareFrame(self, isGround, originalFrame, comparedFrame, eventAttributes):
        """
        Controlla che fra gli eventi ai frame del confronto vi sia una corrispondenza di tutti gli attributi
        
        :param originalFrame: Frame dell'evento da confrontare nel ground truth
        :param comparedFrame: Frame dell'evento da confrontare tra quelli rilevati
        :param eventAttributes: Lista di attributi da confrontare
        :return: [booleano che indica se è stata trovata una corrispondenza, indice dell'evento corrispondente]
        """
        equal = True
        if (isGround):
            dictionary = self.groundDictionary
            otherDictionary = self.detectedDictionary
        else:
            dictionary = self.detectedDictionary
            otherDictionary = self.groundDictionary
        if (otherDictionary.get(comparedFrame) is None):
            equal = False
        else:   
            for attribute in eventAttributes:
                if(dictionary[originalFrame]['name'] == otherDictionary[comparedFrame]['name']):
                    if not(is_integer(attribute)):
                        if (dictionary[originalFrame].get(attribute) is None) or (otherDictionary[comparedFrame].get(attribute) is None):
                            raise Exception('Malformed dictionary, accessing wrong attribute {}'.format(attribute))
                        elif (dictionary[originalFrame][attribute] != otherDictionary[comparedFrame][attribute]):    
                            equal = False
                            break
                else:
                    equal = False
                    break 
        return [equal, comparedFrame]
    
    def _calculateOutputOverall(self):
        "Calcola l'output sulla base degli eventi riconosciuti, calcolando i valori di precision e recall per ciascun evento"
        for frame in self.output['ground']:
            groundEvent = self.output['ground'][frame]
            if (groundEvent['match']):
                self.output['overall'][groundEvent['name']]['TP'] += 1
                self.totalTruePositive +=1
            else:
                self.output['overall'][groundEvent['name']]['FN'] += 1
                self.totalFalseNegative += 1
        for frame in self.output['detected']:
            detectedEvent = self.output['detected'][frame]
            if not (detectedEvent['match']):
                self.output['overall'][detectedEvent['name']]['FP'] += 1
                self.totalFalsePositive += 1
        for key in self.output['overall']:
            if (isinstance(self.output['overall'][key], dict)):
                self.output['overall'][key]['total'] = self.output['overall'][key]['TP'] + self.output['overall'][key]['FN']
                precisionFraction = self.output['overall'][key]['TP'] + self.output['overall'][key]['FP']
                recallFraction = self.output['overall'][key]['TP'] + self.output['overall'][key]['FN']
                if (precisionFraction != 0):
                    self.output['overall'][key]['precision'] = self.output['overall'][key]['TP'] / precisionFraction
                if (recallFraction != 0):
                    self.output['overall'][key]['recall'] = self.output['overall'][key]['TP'] / recallFraction
        
class AtomicValidator(BaseValidator):
    "Confronta gli eventi atomici"
    def __init__(self, eventListFile, groundDictionary, detectedDictionary, windowSize):
        """
        :param eventListFile:  File con i parametri da confrontare per ciasciun evento
        :param groundDictionary: Dizionario con gli eventi del ground truth
        :param detectedDictionary: Dizionario con gli eventi rilevati
        :param windowSize: Dimensione con la finestra di confronto
        """
        super().__init__(eventListFile, groundDictionary, detectedDictionary)
        self.atomic = True
        self.windowSize = windowSize 
        self.output['overall']['windowSize'] = windowSize     
    
    def _compareEvent(self, isGround, frame, eventFoundName):
        "Confronta gli eventi nella distanza inserita come parametro windowSize"
        found, index = [False, -1]
        intFrame = int(frame)
        if (self.windowSize == -1):
            window = int(self.knownEvent[eventFoundName][-1])
        else:
            window = self.windowSize
        for i in range(window):
                    found, index = self._compareFrame(isGround, frame, str(intFrame + i), self.knownEvent[eventFoundName])
                    if (not found):
                        found, index = self._compareFrame(isGround, frame, str(intFrame - i), self.knownEvent[eventFoundName])
                    if (found):
                        break
        if (isGround):
            checkString = 'detected'
            otherString = 'ground'
        else:
            checkString = 'ground'
            otherString = 'detected'
        if (found):

            if (not self.output[checkString][index]['match'] or self.atomic):
                self.output[checkString][index]['match'] = True
                self.output[otherString][frame]['match'] = True
                self.output[otherString][frame]['distance'] = abs(int(index) - int(frame))

class AtomiMultiprocessValidator(AtomicValidator):
    "Confronta gli eventi atomici con il multiprocessing"
    def __init__(self, eventListFile, groundDictionary, detectedDictionary, windowSize):
        """
        :param eventListFile:  File con i parametri da confrontare per ciasciun evento
        :param groundDictionary: Dizionario con gli eventi del ground truth
        :param detectedDictionary: Dizionario con gli eventi rilevati
        :param windowSize: Dimensione con la finestra di confronto
        """
        self.groundDictionary = groundDictionary
        self.detectedDictionary = detectedDictionary
        self.knownEvent = self._populateKnowEventList(eventListFile)
        self.eventListFile = eventListFile
        self.windowSize = windowSize
        #self._parseEvent() 
        # lista di dizionari con tutti gli eventi, positivo/negativo
        self.output = []
    def validate(self, nProcess):
        splitValue = int(len(self.groundDictionary)/nProcess)
        itemList = list(self.groundDictionary.items())
        dictionaries = [dict(itemList[i:i+splitValue]) for i in range(0, len(self.groundDictionary), splitValue)]
        q = Queue()
        processes = list()
        for i in range(nProcess):
            p = AtomicProcessor(q,i,self.eventListFile,dictionaries[i],self.detectedDictionary, self.windowSize)
            p.start()
            processes.append(p)

        [proc.join() for proc in processes]

class ComplexValidator(BaseValidator):
    "Confronta gli eventi complessi"
    def __init__(self, eventListFile, groundDictionary, detectedDictionary, percentage):
        """
        :param eventListFile:  File con i parametri da confrontare per ciasciun evento
        :param groundDictionary: Dizionario con gli eventi del ground truth
        :param detectedDictionary: Dizionario con gli eventi rilevati
        :param percentage: Percentuale minima intersection / union affinché l'evento si dichiari rilevato
        """
        super().__init__(eventListFile, groundDictionary, detectedDictionary)
        self.atomic = False     
        self.percentage = percentage
        self.output['overall']['percentage'] = percentage
    
    def _compareEvent(self, isGround, frame, eventFoundName):
        "Confronta gli eventi sulla base di intersection/union"
        found, index, percentage = [False, -1, 0]
        finalFrame = frame  
        if (isGround):
            dictionary = self.groundDictionary
            otherDictionary = self.detectedDictionary
        else:
            dictionary = self.detectedDictionary
            otherDictionary = self.groundDictionary

        if (dictionary[frame].get('finalFrame') is None):
            raise Exception('Event {} in ground has not final frame!'.format(eventFoundName))
        else:
            finalFrame = dictionary[frame]['finalFrame']
        
        for newStartFrame in range(frame, finalFrame):
            newStartFrame = str(newStartFrame)
            if not(otherDictionary.get(newStartFrame) is None):
                found, index = self._compareFrame(isGround, frame, newStartFrame, self.knownEvent[eventFoundName])
                if (found):
                    if (otherDictionary[newStartFrame].get('finalFrame') is None):
                        raise Exception('Event {} in detected has not final frame!'.format(eventFoundName))
                    else:
                        newFinalFrame = otherDictionary[newStartFrame]['finalFrame']
                        intFrame, intFinalFrame, intNewFrame, intNewFinalFrame = [int(frame), int(finalFrame), int(newStartFrame), int(newFinalFrame)]
                        union = max(intFinalFrame, intNewFinalFrame) - intFrame
                        intersection = min(intFinalFrame, intNewFinalFrame) - intNewFinalFrame
                        percentage = ( intersection / union ) * 100
                        if (percentage > self.percentage):
                            break
                        else:
                            found = False
                    break
        if (isGround):
            checkString = 'detected'
            otherString = 'ground'
        else:
            checkString = 'ground'
            otherString = 'detected'
        if (found):
            if (not self.output[checkString][index]['match'] or self.atomic):
                self.output[checkString][index]['match'] = True
                self.output[otherString][frame]['match'] = True
                self.output[otherString][frame]['percentage'] = percentage
            
                    
def main(): 
    print('Starting validation')
    startTime = time()
    atomic = True

    # Ricordati di cancellare i parametri di default per ground truth e detected path
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--datasetPath", default='E:\GameplayFootball\Prova\Match_2019_02_15_#001_2nd_half', help="Path to the dataset")
    parser.add_argument("-e", "--eventFile", default='events.txt', help="Path to txt with a list of recognized event and attributes to compare")
    parser.add_argument("-o", "--outputFile", default='Annotations_AtomicEvents_Results.xml', help="Name of the output path")
    parser.add_argument("-a", "--atomic", action="store_true", help="Use this flag if you are comparing atomic event")
    parser.add_argument("-w", "--windowSize", type=int, default=-1, help="Size of the distance from atomic event to be compared as true")
    parser.add_argument("-p", "--percentage", type=float, default=20, help="Percentage of intersection / union for a complex event to be compared as true")
    parser.add_argument("-s", "--samples", type=int, default=1, help="Number of samples to subsample events")
    args = parser.parse_args()
    if not(PATH.isdir(args.datasetPath)):
        raise Exception("No files with such names found!")
    groundTruthPath = args.datasetPath + "//Annotations_AtomicEvents.xml"
    detectedPath = args.datasetPath + "//Annotations_AtomicEvents_Detected.xml"
    samples = args.samples
    ground = XML.createDictionary(groundTruthPath, samples)
    detected = XML.createDictionary(detectedPath)
    outputPath = args.datasetPath + '//'+ args.outputFile
    checkEventFile = args.eventFile

    if not(PATH.isfile(args.eventFile)):
        raise Exception("No event file found!")
    windowSize = args.windowSize
    percentage = args.percentage
    
    print('Ground length is {}'.format(len(ground)))

    if (atomic):
        validator = AtomicValidator(checkEventFile, ground, detected, windowSize)
    else:
        validator = ComplexValidator(checkEventFile, ground, detected, percentage)
    validator.validate()
    XML.createOutputFile(validator.output, outputPath)
    elapsedTime = time() - startTime
    print('Elapsed {}'.format(elapsedTime))

    #pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(dictionary)

def main2():
    eventList = 'E://git//footballeventdetector//events.txt'
    groundDictionary = XML.createDictionary('E:\GameplayFootball\Dataset\Match_2019_02_09_#001\Annotations_AtomicEvents.xml')
    detectedDictionary = XML.createDictionary('E:\GameplayFootball\Dataset\Match_2019_02_09_#001\Annotations_AtomicEvents_Detected_OLD.xml')
    
    print('Starting single')
    startTime = time()
    a = AtomicValidator(eventList,groundDictionary, detectedDictionary, -1)
    a.validate()
    elapsedTime = time() - startTime
    print('Elapsed {}'.format(elapsedTime))

    print('Starting multi')
    startTime = time()
    b = AtomiMultiprocessValidator(eventList,groundDictionary, detectedDictionary, -1)
    b.validate(4)
    elapsedTime = time() - startTime
    print('Elapsed {}'.format(elapsedTime))

if __name__ == "__main__":
    main()
