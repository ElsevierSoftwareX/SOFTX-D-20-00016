# Import packages
import time
import xml.etree.ElementTree as ET

def preprocess(
    manual = "",
    db = "",
    input = "atomic-events.xml", 
    output = "atomic-events.stream"):

    # Static variables
    track = 'track'
    label = 'label'
    box = 'box'
    frame = 'frame'

    # Start measure time
    start = time.time()

    # Load the XMl input file and its root
    tree = ET.parse(input)
    root = tree.getroot()

    # Print the events
    f=open(output,"w+")
    for t in root.findall(track):
        l = t.get(label)
        f.write("event("+l[0].lower()+l[1:]+"(")
        b = t.find(box)
        fr = b.get(frame)
        f.write(fr)
        first = True
        for attrib in b:
            f.write(","+attrib.text)
        f.write(")).\r\n")
    f.close()

    # Get and frame and replace it
    replace(db, get_half_time_frame(manual), get_goalkeepers(manual))

    # Stop measure time
    end = time.time()

    # Print info
    elapsed = round(end-start, 1)
    print("[XML_to_ETALIS]\t Preprocessed data in: " + str(elapsed) + "s.")


def get_half_time_frame(filename):
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


def get_goalkeepers(filename):
    results = []
    tree = ET.parse(filename)
    annotations = tree.getroot()
    if (annotations.tag != 'annotations'):
        raise Exception('No /annotations found in XML')
    else:
        for track in annotations:
            if (track.tag == 'track'):
                if (track.attrib.get('id') is None):
                    raise Exception('No attribute "id" in /track')
                elif (int(track.attrib['id']) == -1):
                    if (track.attrib.get('label') is None):
                        raise Exception('No attribute "label" in /track')
                    elif(track.attrib['label'] != 'GoalKeeper'):
                        raise Exception('This track has not goalkeepers!')
                    else:
                        box = track[0]
                        if (box.tag != 'box'):
                            raise Exception('No /box found in /track')
                        else:
                            for attribute in box:
                                if (attribute.attrib['name'] == 'goalKeeperId'):
                                    results.append(attribute.text)

    return results


def replace(db_filepath, frame, goalKeeperIDs):

    print(goalKeeperIDs)

    # Open and read the file
    f = open(db_filepath, "r")
    lines = f.readlines()
    f.close()

    # Change the first row
    lineToChange = lines[0]
    start, rest = lineToChange.split('(')
    oldValue, end = rest.split(')')
    lines[0] = start + "(" + str(frame) + ")" + end

    # Change the first row
    lineToChange = lines[4]
    start, rest = lineToChange.split('(')
    middleStart, rest = rest.split(',')
    oldValue, end = rest.split(')')
    lines[4] = start + "(" + middleStart + "," + str(goalKeeperIDs[1]) + ")" + end

    # Change the first row
    lineToChange = lines[8]
    start, rest = lineToChange.split('(')
    middleStart, rest = rest.split(',')
    oldValue, end = rest.split(')')
    lines[8] = start + "(" + middleStart + "," + str(goalKeeperIDs[0]) + ")" + end

    # Open and write the file
    f = open(db_filepath, "w")
    for line in lines:
        f.write(line)
    f.close()
    