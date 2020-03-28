import xml.etree.ElementTree as ET
import copy
import xml.dom.minidom as DOM
import os
import time

tackle_min_timespan = 15
max_time_between_tackles = 120

def mergeNearTackles(annotations, newAnnotations, numFrameDistance):   
    eliminated = 0
    frameCount = 0
    trackCounter = 1
    diff = { 'any': False, 'outcome': False, 'teamId': False, 'victimId': False, 'tacklerId': False }    

    for i,track in enumerate(annotations):
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
                print("[ERROR] At: " + eventAttributes['name'] + ", Id: " + str(eventAttributes['track']))
                continue

            if (box.tag != 'box'):
                raise Exception('No /box found in /track')
            else:
                if (box.attrib.get('frame') is None):
                        raise Exception('No attribute "frame" in /box')
                else:
                    frameValue = int(box.attrib['frame'])
                    eventAttributes['frame'] = frameValue
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

                    # Correzione dell'id della traccia
                    thisTrack = newAnnotations[i-eliminated]
                    oldId = thisTrack.attrib.get('id')                    
                    thisTrack.attrib['id'] = str(int(oldId) - eliminated)

                    if (eventAttributes['name'] == 'Tackle'):
                        if (old is not None):
                            if (old['finalFrame'] + numFrameDistance >= eventAttributes['frame']):
                                oldTrack = newAnnotations[i-1-eliminated]

                                #print('frame modified: ' + str(eventAttributes['finalFrame']+1))
                                
                                # Aggiungendo un insieme di box dentro questa traccia 
                                for k in range(old['finalFrame']+1, eventAttributes['finalFrame']+1):
                                    newBox = ET.SubElement(oldTrack, 'box')
                                    newBox.attrib['frame'] = str(int(k))
                                    newBox.attrib['keyframe'] = '0'
                                    newBox.attrib['occluded'] = '0'
                                    newBox.attrib['outside'] = '0'
                                    newBox.attrib['xbr'] = '1.24157999999999993e+03'
                                    newBox.attrib['xtl'] = '1.20052999999999997e+03'
                                    newBox.attrib['ybr'] = '1.68740000000000009e+02'
                                    newBox.attrib['ytl'] = '9.17900000000000063e+01'

                                    # Prendo i valori del box che erano presenti nel tackle vecchio (rimosso) e che stanno per essere aggiunti al track precedente 
                                    new_victimId  = old['victimId']
                                    new_teamId    = old['teamId']
                                    new_tacklerId = old['tacklerId']
                                    new_outcome   = old['outcome']

                                    # Prendo il primo box per vederne i valori iniziali
                                    box = oldTrack[0]                                        
                                    for attribute in box:
                                        attributeName = attribute.attrib['name']

                                        if (attributeName == 'victimId'):    old_victimId   = attribute.text
                                        elif (attributeName == 'teamId'):    old_teamId     = attribute.text                                        
                                        elif (attributeName == 'tacklerId'): old_tacklerId  = attribute.text                                        
                                        elif (attributeName == 'outcome'):   old_outcome    = attribute.text                                            

                                    # Controllo se ci sono stati dei cambiamenti
                                    if (new_outcome != old_outcome or new_teamId != old_teamId or new_victimId != old_victimId or new_tacklerId != old_tacklerId):
                                        diff['any'] = True

                                        # Dumb Rule: se il primo tackle è vinto e il successivo perso, l'outcome resta vinto se le squadre si invertono
                                    
                                        if (new_outcome != old_outcome):     diff['outcome']    = True 
                                        if (new_teamId != old_teamId):       diff['teamId']     = True
                                        if (new_victimId != old_victimId):   diff['victimId']   = True                                        
                                        if (new_tacklerId != old_tacklerId): diff['tacklerId']  = True

                                        # Di base lascio l'outcome che c'era prima
                                        final_outcome = old_outcome
                                        if (diff['outcome'] and not diff['teamId']):
                                            # Se cambia l'outcome e non le squadre, uso l'outcome finale
                                            final_outcome = new_outcome
                                        elif (not diff['outcome'] and diff['teamId']):
                                            # Se non cambia l'outcome ma le squadre si, uso l'outcome opposto                              
                                            if (new_outcome == 'false'):
                                                final_outcome = 'true'
                                            else:
                                                final_outcome = 'false'

                                    # devono restare i valori di victim, team e tackler id uguali a quelli iniziali e modificare solo il valore dell'outcome
                                    # Scandisco tutti i box che sono presenti e aggiusto i valori unificandoli a quello corretto che devo costruire
                                    
                                    # Aggiungo gli attributi a questo box
                                    for attributeName in old:
                                        if ((attributeName != 'name') and (attributeName != 'track') and (attributeName != 'frame') and (attributeName != 'finalFrame')):                                        
                                            attribute = ET.SubElement(newBox, 'attribute')
                                            attribute.attrib['name'] = attributeName
                                            attribute.text = str(old[attributeName])  

                                if (diff['any']):
                                    for box in oldTrack:
                                        for attribute in box:
                                            attributeName = attribute.attrib['name']
                                            if (attributeName == 'outcome'):
                                                attribute.text = final_outcome
                                        
                                    #print('oldVictimId = ' + old_victimId + ' oldTeamId = ' + old_teamId + ' oldTacklerId = ' + old_tacklerId + ' oldOutcome = ' + old_outcome)
                                    #print('newVictimId = ' + new_victimId + ' newTeamId = ' + new_teamId + ' newTacklerId = ' + new_tacklerId + ' newOutcome = ' + new_outcome)
                                    #print('final_outcome = ' + final_outcome)
                                    #print('DIFFERENCE FOUND: fixing...\n')                                                                                                                    
                                    
                                    for value in diff:
                                        diff[value] = False
                                                                                                                
                                #newAnnotations.remove(newAnnotations[i-eliminated])
                                del newAnnotations[i-eliminated]
                                eliminated += 1

                        old = eventAttributes
                    else:
                        old = None

    return eliminated


def removeOneFrameTackles(annotations):   
    # Ricerca di tackle che hanno durata di un frame anche dopo il merge precedente
    frameCount = 0
    trackCounter = 1
    removed = 0
    for i,track in enumerate(annotations):
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
                print("[ERROR] At: " + eventAttributes['name'] + ", Id: " + str(eventAttributes['track']))
                continue

            if (box.tag != 'box'):
                raise Exception('No /box found in /track')
            else:
                if (box.attrib.get('frame') is None):
                        raise Exception('No attribute "frame" in /box')
                else:
                    frameValue = int(box.attrib['frame'])
                    eventAttributes['frame'] = frameValue
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
                    
                    # Correzione dell'id della traccia
                    thisTrack = annotations[i]
                    oldId = thisTrack.attrib.get('id')
                    thisTrack.attrib['id'] = str(int(oldId) - removed)

                    # Rimozione della traccia da un solo frame
                    if (lengthValue <= tackle_min_timespan and eventAttributes['name'] == 'Tackle'):
                        #print('Deleting 1 frame tackle track #' + str(int(thisTrack.attrib['id']) + removed))
                        del annotations[i] # o track?
                        removed += 1

    return removed



def main():
    # Start time of computation
    start = time.time()

    stdfilename    = 'Annotations_ComplexEvents.xml'
    stdoutfilename = 'Annotations_ComplexEvents_NEW.xml'
    merged  = 0
    removed = 0
    filelist = []

    print('[INFO] Files to be processed:')
    elements = os.listdir('.')
    for name in elements:
        if (os.path.isfile(name) and name == stdfilename):
            print('\t.\\' + name)
            filelist.append(name)

        if (os.path.isdir(name)):
            elements1 = os.listdir(name)
            for name1 in elements1:
                if os.path.isfile(os.path.join(name,name1)) and name1 == stdfilename:
                        print(os.path.join(name,name1))
                        filelist.append(os.path.join(name,name1))

                if os.path.isdir(os.path.join(name, name1)):
                    elements2 = os.listdir(os.path.join(name,name1))
                    for name2 in elements2:
                        if (os.path.isfile(os.path.join(name, name1, name2)) and name2 == stdfilename):
                            print('\t.\\' + os.path.join(name, name1, name2))     
                            filelist.append(os.path.join(name, name1, name2))        

    for filename in filelist:
        start_partial = time.time()
        print('\n')
        print('[INFO] Starting computation for file {}.'.format(filename))

        tree = ET.parse(filename)
        old = None
        annotations = tree.getroot()
        newAnnotations = copy.deepcopy(annotations)

        if (annotations.tag != 'annotations'):
            raise Exception('No /annotations found in XML')
        else:            
            merged_now  = mergeNearTackles(annotations, newAnnotations, max_time_between_tackles)
            removed_now = removeOneFrameTackles(newAnnotations)
            
            merged  += merged_now
            removed += removed_now
        
        # Scrivo i dati finali su file 
        xml = DOM.parseString(ET.tostring(newAnnotations))
        outfilename = os.path.join(os.path.dirname(filename),stdoutfilename)

        end_partial = time.time()        
        print('[INFO] The number of tackles merged is: ' + str(merged_now) + '.')
        print('[INFO] The number of tackles removed of 1 frame removed is: ' + str(removed_now) + '.')
        print('[INFO] Done computation for {} in {} seconds.'.format(outfilename, round(end_partial-start_partial, 1)))
        
        with open(outfilename, 'w') as f:
            text = xml.toprettyxml()
            text = '\r'.join([s for s in text.splitlines() if s.strip()])                    
            f.write(text)

        print('[INFO] Done writing file for {} in {} seconds.\n'.format(outfilename, round(time.time()-end_partial, 1)))

    end = time.time()
    print('[INFO] The total number of tackles merged is: \t' + str(merged) + '.')
    print('[INFO] The total number of tackles of 1 frame removed is: ' + str(removed) + '.')
    print('[INFO] Done total computation in {} seconds.\n'.format(round(end-start, 1))) 

    return



if __name__ == '__main__':
    main()