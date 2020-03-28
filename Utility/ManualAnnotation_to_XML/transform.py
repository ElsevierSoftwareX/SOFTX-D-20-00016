# Import packages
import xml.etree.ElementTree as ET
import xml.dom.minidom as DOM


def add_GoalKeeper(annotations, teamId, goalKeeperId):

    track = ET.SubElement(annotations, 'track')
    track.attrib['id'] = str(-1)
    track.attrib['label'] = "GoalKeeper"

    box = ET.SubElement(track, 'box')
    box.attrib['frame'] = str(0)
    box.attrib['keyframe'] = '1'
    box.attrib['occluded'] = '0'
    box.attrib['outside'] = '0'
    box.attrib['xbr'] = '10'
    box.attrib['xtl'] = '100'
    box.attrib['ybr'] = '10'
    box.attrib['ytl'] = '100'

    attr = ET.SubElement(box, 'attribute')
    attr.attrib['name'] = "goalKeeperId"
    attr.text = goalKeeperId

    attr = ET.SubElement(box, 'attribute')
    attr.attrib['name'] = "teamId"
    attr.text = teamId


def add_SecondHalf_start_frame(annotations, secondHalf_start_frame):

    track = ET.SubElement(annotations, 'track')
    track.attrib['id'] = str(0)
    track.attrib['label'] = "SecondHalf"

    box = ET.SubElement(track, 'box')
    box.attrib['frame'] = str(secondHalf_start_frame)
    box.attrib['keyframe'] = '1'
    box.attrib['occluded'] = '0'
    box.attrib['outside'] = '0'
    box.attrib['xbr'] = '10'
    box.attrib['xtl'] = '100'
    box.attrib['ybr'] = '10'
    box.attrib['ytl'] = '100'


def chomp(x):
    if x.endswith("\r\n"): return x[:-2]
    if x.endswith("\n") or x.endswith("\r"): return x[:-1]
    return x


def main():

    # Set I/O Filepaths
    i = "input.txt"
    o = "Annotations_AtomicEvents_Manual.xml"

    annotations = ET.Element('annotations')
    lineCount = 0
    fi = open(i, "r")
    for line in fi:
        if lineCount == 0:
            add_SecondHalf_start_frame(annotations, chomp(line))
            lineCount += 1
        else:
            teamId = line.split(',')[0]
            goalKeeperId = chomp(line.split(',')[1])
            add_GoalKeeper(annotations, teamId, goalKeeperId)

    # Export the content as XML file
    xml = DOM.parseString(ET.tostring(annotations))
    with open(o, 'w') as fo:
                fo.write(xml.toprettyxml())

    fi.close()
    print("[ManualAnnotations_to_XML] Done.")


if __name__ == "__main__":
    main()
