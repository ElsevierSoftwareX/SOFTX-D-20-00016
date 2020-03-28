# coding=UTF-8
import pprint
import os.path as PATH, time
import argparse
import dicttoxml
import xml.etree.ElementTree as ET
import xml.dom.minidom as DOM

class XML():
    @staticmethod
    def createDictionary(filename):
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

                    try:
                        box = track[0]
                    except:
                        print("Error at: " + eventAttributes['name'] + ", Id: " + str(eventAttributes['track']))
                        continue

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
                            if (lengthValue >= 1):
                                eventAttributes['finalFrame'] = frameValue + lengthValue - 1

                            # Before assignment
                            if dictionary.get(str(frameValue)) is None:
                                # Assignment
                                dictionary[str(frameValue)] = eventAttributes
                            else:
                                # Search an empty slot
                                i = 1
                                while dictionary.get(str(frameValue-i)) is not None:
                                    i += 1
                                # Found an empty slot -> Assignment
                                # print("Event: " + eventAttributes['name'] + ", moved from: " + str(frameValue) + " to: " + str(frameValue-i))
                                dictionary[str(frameValue-i)] = eventAttributes

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
        self.output['detected'] = self._populateOutputDictionary(detectedDictionary)

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
                raise Exception('Malformed dictionary, no event {} match accepted events'.format(self.groundDictionary[frame]['name']))
            else:
                self._compareEvent_ground(frame, eventFoundName)

        for frame in self.detectedDictionary:
            eventFoundName = None
            for eventName in self.knownEvent:
                if (eventName == self.detectedDictionary[frame]['name']):
                    eventFoundName = eventName
                    break
            if (eventFoundName is None):
                raise Exception('Malformed dictionary, no event {} match accepted events'.format(self.detectedDictionary[frame]['name']))
            else:
                self._compareEvent_detected(frame, eventFoundName)

        self._calculateOutputOverall()
    
    def _populateKnowEventList(self, file):
        """
        Popola la lista con gli eventi riconosciuti dal detector e gli attributi che dovrà confrontare
        Questi saranno presenti in un file di testo in cui ciasciuna linea avrà la seguente struttura:
        nomeEvento attributoEvento1 attributoEvento2 attributoEvento3 ...
        
        :param file: File con la lista eventi 
        :return: Dizionario con tutti gli eventi da riconoscere, la chiave è il nome dell'evento
        """
        newDictionary = {}
        with open(file, 'r') as f:
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
    
    def _compareEvent(self, frame, eventFoundName):
        "Compara gli eventi in base all'algoritmo scelto fra atomici e complessi"
        pass
    
    def _compareFrame_ground(self, originalFrame, comparedFrame, eventAttributes):
        """
        Controlla che fra gli eventi ai frame del confronto vi sia una corrispondenza di tutti gli attributi
        
        :param originalFrame: Frame dell'evento da confrontare nel ground truth
        :param comparedFrame: Frame dell'evento da confrontare tra quelli rilevati
        :param eventAttributes: Lista di attributi da confrontare
        :return: [booleano che indica se è stata trovata una corrispondenza, indice dell'evento corrispondente]
        """

        # Normalize data
        originalFrame = str(originalFrame)
        comparedFrame = str(comparedFrame)

        equal = True
        if (self.detectedDictionary.get(comparedFrame) is None):
            equal = False
        else:
            if (len(eventAttributes) <= 0):
                for attribute in eventAttributes:
                    if (self.groundDictionary[originalFrame]['name'] == self.detectedDictionary[comparedFrame]['name']):
                        if (self.groundDictionary[originalFrame].get(attribute) is None) or (self.detectedDictionary[comparedFrame].get(attribute) is None):
                            raise Exception('Malformed dictionary, accessing wrong attribute {}'.format(attribute))

                        elif (self.groundDictionary[originalFrame][attribute] != self.detectedDictionary[comparedFrame][attribute]):    
                            equal = False
                            break
                    else:
                        equal = False
                        break
            else:
                if (self.groundDictionary[originalFrame]['name'] != self.detectedDictionary[comparedFrame]['name']):
                    equal = False

        return [equal, comparedFrame]

    def _compareFrame_detected(self, originalFrame, comparedFrame, eventAttributes):
        """
        Controlla che fra gli eventi ai frame del confronto vi sia una corrispondenza di tutti gli attributi
        
        :param originalFrame: Frame dell'evento da confrontare nel ground truth
        :param comparedFrame: Frame dell'evento da confrontare tra quelli rilevati
        :param eventAttributes: Lista di attributi da confrontare
        :return: [booleano che indica se è stata trovata una corrispondenza, indice dell'evento corrispondente]
        """

        # Normalize data
        originalFrame = str(originalFrame)
        comparedFrame = str(comparedFrame)

        equal = True
        if (self.groundDictionary.get(comparedFrame) is None):
            equal = False
        else:
            if (len(eventAttributes) <= 0):
                for attribute in eventAttributes:
                    if(self.detectedDictionary[originalFrame]['name'] == self.groundDictionary[comparedFrame]['name']):
                        if (self.detectedDictionary[originalFrame].get(attribute) is None) or (self.groundDictionary[comparedFrame].get(attribute) is None):
                            raise Exception('Malformed dictionary, accessing wrong attribute {}'.format(attribute))
                        elif (self.detectedDictionary[originalFrame][attribute] != self.groundDictionary[comparedFrame][attribute]):    
                            equal = False
                            break
                    else:
                        equal = False
                        break
            else:
                if(self.detectedDictionary[originalFrame]['name'] != self.groundDictionary[comparedFrame]['name']):
                    equal = False

        return [equal, comparedFrame]
    
    def _calculateOutputOverall(self):
        "Calcola l'output sulla base degli eventi riconosciuti, calcolando i valori di precision e recall per ciascun evento"
        for frame in self.output['ground']:
            groundEvent = self.output['ground'][frame]
            if (groundEvent['match']):
                self.output['overall'][groundEvent['name']]['TP'] += 1
            else:
                self.output['overall'][groundEvent['name']]['FN'] += 1
        for frame in self.output['detected']:
            detectedEvent = self.output['detected'][frame]
            if not (detectedEvent['match']):
                self.output['overall'][detectedEvent['name']]['FP'] += 1
        for key in self.output['overall']:
            if (isinstance(self.output['overall'][key], dict)):
                self.output['overall'][key]['total'] = self.output['overall'][key]['TP'] + self.output['overall'][key]['FN']
                precisionFraction = self.output['overall'][key]['TP'] + self.output['overall'][key]['FP']
                recallFraction = self.output['overall'][key]['TP'] + self.output['overall'][key]['FN']
                if (precisionFraction != 0):
                    self.output['overall'][key]['precision'] = self.output['overall'][key]['TP'] / precisionFraction
                if (recallFraction != 0):
                    self.output['overall'][key]['recall'] = self.output['overall'][key]['TP'] / recallFraction

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

    def _compareEvent_ground(self, frame, eventFoundName):
        "Confronta gli eventi sulla base di intersection/union"
        found, index, percentage = [False, -1, 0]
        finalFrame = frame
        if (self.groundDictionary[frame].get('finalFrame') is None):
            raise Exception('Event {} in ground has not final frame!'.format(eventFoundName))
        else:
            finalFrame = self.groundDictionary[frame]['finalFrame']
        
        for newStartFrame in range(int(frame), int(finalFrame)):
            newStartFrame = str(newStartFrame)

            if not(self.detectedDictionary.get(newStartFrame) is None):
                found, index = self._compareFrame_ground(frame, newStartFrame, self.knownEvent[eventFoundName])
            if (found):
                if (self.detectedDictionary[newStartFrame].get('finalFrame') is None):
                    raise Exception('Event {} in detected has not final frame!'.format(eventFoundName))
                else:
                    newFinalFrame = self.detectedDictionary[newStartFrame]['finalFrame']
                    intFrame, intFinalFrame, intNewStartFrame, intNewFinalFrame = [int(frame), int(finalFrame), int(newStartFrame), int(newFinalFrame)]
                    union = max(intFinalFrame, intNewFinalFrame) - intFrame
                    intersection = min(intFinalFrame, intNewFinalFrame) - intNewStartFrame
                    percentage = ( intersection / union ) * 100
                    if (percentage > self.percentage):
                        break
                    else:
                        found = False
        if( found):
            if (not self.output['detected'][index]['match'] or self.atomic):
                self.output['detected'][index]['match'] = True
                self.output['ground'][frame]['match'] = True
                self.output['ground'][frame]['percentage'] = percentage
            
    def _compareEvent_detected(self, frame, eventFoundName):
        "Confronta gli eventi sulla base di intersection/union"
        found, index, percentage = [False, -1, 0]
        finalFrame = frame
        if (self.detectedDictionary[frame].get('finalFrame') is None):
            raise Exception('Event {} in ground has not final frame!'.format(eventFoundName))
        else:
            finalFrame = self.detectedDictionary[frame]['finalFrame']
        
        for newStartFrame in range(int(frame), int(finalFrame)):
            newStartFrame = str(newStartFrame)

            if not(self.groundDictionary.get(newStartFrame) is None):
                found, index = self._compareFrame_detected(frame, newStartFrame, self.knownEvent[eventFoundName])
            if (found):
                if (self.groundDictionary[newStartFrame].get('finalFrame') is None):
                    raise Exception('Event {} in detected has not final frame!'.format(eventFoundName))
                else:
                    newFinalFrame = self.groundDictionary[newStartFrame]['finalFrame']
                    intFrame, intFinalFrame, intNewStartFrame, intNewFinalFrame = [int(frame), int(finalFrame), int(newStartFrame), int(newFinalFrame)]
                    union = max(intFinalFrame, intNewFinalFrame) - intFrame
                    intersection = min(intFinalFrame, intNewFinalFrame) - intNewStartFrame
                    percentage = ( intersection / union ) * 100
                    if (percentage > self.percentage):
                        break
                    else:
                        found = False
        if (found):
            if (not self.output['ground'][index]['match'] or self.atomic):
                self.output['ground'][index]['match'] = True
                self.output['detected'][frame]['match'] = True
                self.output['detected'][frame]['percentage'] = percentage

    
def evaluate(ground, detected, outputPath, checkEventFile, windowSize, percentage, atomic):

    # Start measuring time
    start = time.time()

    ground = XML.createDictionary(ground)
    detected = XML.createDictionary(detected)
    validator = ComplexValidator(checkEventFile, ground, detected, percentage)

    validator.validate()
    XML.createOutputFile(validator.output, outputPath)
    #pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(dictionary)

    # End measuring time
    end = time.time()

    # Give info to output
    elapsed = round(end - start, 1)
    print("[EVALUATOR]\t Evaluated data in: " + str(elapsed) + "s.")

def main(): 
    atomic = True

    # Ricordati di cancellare i parametri di default per ground truth e detected path
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--groundTruthPath",  default="Annotations_AtomicEvents.xml", help="Path to the ground truth events xml file. Is the FIRST argument")
    parser.add_argument("-d" ,"--detectedPath", default="xmlevents.txt", help="Path to the detected events xml file. Is the SECOND argument")
    parser.add_argument("-e", "--eventFile", default='events.txt', help="Path to txt with a list of recognized event and attributes to compare")
    parser.add_argument("-o", "--outputFile", default='output.xml', help="Name of the output path")
    parser.add_argument("-a", "--atomic", action="store_true", help="Use this flag if you are comparing atomic event")
    parser.add_argument("-w", "--windowSize", type=int, default=10, help="Size of the distance from atomic event to be compared as true")
    parser.add_argument("-p", "--percentage", type=float, default=20, help="Percentage of intersection / union for a complex event to be compared as true")
    args = parser.parse_args()
    if not(PATH.isfile(args.groundTruthPath) and PATH.isfile(args.detectedPath) ):
        raise Exception("No files with such names found!")
    ground = args.groundTruthPath
    detected = args.detectedPath
    outputPath = args.outputFile
    checkEventFile = args.eventFile
    if not(PATH.isfile(args.groundTruthPath)):
        raise Exception("No event file found!")
    windowSize = args.windowSize
    percentage = args.percentage

    evaluate(ground, detected, outputPath, checkEventFile, windowSize, percentage, atomic)

if __name__ == "__main__":
    main()