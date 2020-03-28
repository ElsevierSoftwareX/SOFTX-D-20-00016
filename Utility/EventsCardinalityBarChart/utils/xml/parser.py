# Import packages
import xml.etree.ElementTree as ET
import xml.dom.minidom as DOM

def dictionaryBuilder(filename):
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
                            if (eventAttributes.get('startFrame') is None):
                                eventAttributes['startFrame'] = boxFrame.attrib.get('frame')
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