# Import packages
import time
import xml.etree.ElementTree as ET
import xml.dom.minidom as DOM
from .converter.eventsToXML import *

def postprocess(
    input = "complex-events.stream",
    output = "complex-events.xml"):

    # Start measure time
    start = time.time()

    annotations = ET.Element('annotations')
    eventCount = 0
    fi = open(input, "r")
    for line in fi:
        event = line.split(' ')[1]
        eventName = event.split('(')[0]
        eventArgs = event.split('(')[1]
        eventArgs = eventArgs.split(')')[0]

        if eventName == "pass":
            eventCount += 1
            PassToXML(eventCount, eventArgs, annotations)
            continue
        elif eventName == "passThenGoal":
            eventCount += 1
            PassThenGoalToXML(eventCount, eventArgs, annotations)
            continue
        elif eventName == "filteringPass":
            eventCount += 1
            FilteringPassToXML(eventCount, eventArgs, annotations)
            continue
        elif eventName == "filteringPassThenGoal":
            eventCount += 1
            FilteringPassThenGoalToXML(eventCount, eventArgs, annotations)
            continue
        elif eventName == "cross":
            eventCount += 1
            CrossToXML(eventCount, eventArgs, annotations)
            continue
        elif eventName == "crossThenGoal":
            eventCount += 1
            CrossThenGoalToXML(eventCount, eventArgs, annotations)
            continue
        elif eventName == "tackleC":
            eventCount += 1
            TackleToXML(eventCount, eventArgs, annotations)
            continue
        elif eventName == "shot":
            eventCount += 1
            ShotToXML(eventCount, eventArgs, annotations)
            continue
        elif eventName == "shotOut":
            eventCount += 1
            ShotOutToXML(eventCount, eventArgs, annotations)
            continue
        elif eventName == "shotThenGoal":
            eventCount += 1
            ShotThenGoalToXML(eventCount, eventArgs, annotations)
            continue
        elif eventName == "savedShot":
            eventCount += 1
            SavedShotToXML(eventCount, eventArgs, annotations)
            continue

    # Export the content as XML file
    xml = DOM.parseString(ET.tostring(annotations))
    with open(output, 'w') as fo:
                fo.write(xml.toprettyxml())

    fi.close()

    # Stop measure time
    end = time.time()

    # Print info
    elapsed = round(end-start, 1)
    print("[ETALIS_to_XML]\t Postprocessed data in: " + str(elapsed) + "s.")