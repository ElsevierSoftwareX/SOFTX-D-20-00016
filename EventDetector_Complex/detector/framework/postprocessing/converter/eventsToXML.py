import xml.etree.ElementTree as ET

def PassToXML(trackId, eventArgs, annotations):

    track = ET.SubElement(annotations, 'track')
    track.attrib['id'] = str(trackId)
    track.attrib['label'] = "Pass"

    attributes = eventArgs.split(',')
    startFrame = int(attributes[0])
    endFrame = int(attributes[1])
    senderId = attributes[2]
    teamId = attributes[3]
    receiverId = attributes[4]

    for f in range(startFrame, endFrame):
    
        box = ET.SubElement(track, 'box')
        box.attrib['frame'] = str(f)
        box.attrib['keyframe'] = '1'
        box.attrib['occluded'] = '0'
        box.attrib['outside'] = '0'
        box.attrib['xbr'] = '10'
        box.attrib['xtl'] = '100'
        box.attrib['ybr'] = '10'
        box.attrib['ytl'] = '100'

        attr = ET.SubElement(box, 'attribute')
        attr.attrib['name'] = "sender"
        attr.text = senderId

        attr = ET.SubElement(box, 'attribute')
        attr.attrib['name'] = "teamId"
        attr.text = teamId

        attr = ET.SubElement(box, 'attribute')
        attr.attrib['name'] = "receiver"
        attr.text = receiverId
    
    return

def PassThenGoalToXML(trackId, eventArgs, annotations):

    track = ET.SubElement(annotations, 'track')
    track.attrib['id'] = str(trackId)
    track.attrib['label'] = "PassThenGoal"

    attributes = eventArgs.split(',')
    startFrame = int(attributes[0])
    endFrame = int(attributes[1])
    senderId = attributes[2]
    teamId = attributes[3]
    scorerId = attributes[4]

    for f in range(startFrame, endFrame):

        box = ET.SubElement(track, 'box')
        box.attrib['frame'] = str(f)
        box.attrib['keyframe'] = '1'
        box.attrib['occluded'] = '0'
        box.attrib['outside'] = '0'
        box.attrib['xbr'] = '10'
        box.attrib['xtl'] = '100'
        box.attrib['ybr'] = '10'
        box.attrib['ytl'] = '100'

        attr = ET.SubElement(box, 'attribute')
        attr.attrib['name'] = "sender"
        attr.text = senderId

        attr = ET.SubElement(box, 'attribute')
        attr.attrib['name'] = "teamId"
        attr.text = teamId

        attr = ET.SubElement(box, 'attribute')
        attr.attrib['name'] = "scorer"
        attr.text = scorerId
    
    return

def FilteringPassToXML(trackId, eventArgs, annotations):

    track = ET.SubElement(annotations, 'track')
    track.attrib['id'] = str(trackId)
    track.attrib['label'] = "FilteringPass"

    attributes = eventArgs.split(',')
    startFrame = int(attributes[0])
    endFrame = int(attributes[1])
    senderId = attributes[2]
    teamId = attributes[3]
    receiverId = attributes[4]

    for f in range(startFrame, endFrame):

        box = ET.SubElement(track, 'box')
        box.attrib['frame'] = str(f)
        box.attrib['keyframe'] = '1'
        box.attrib['occluded'] = '0'
        box.attrib['outside'] = '0'
        box.attrib['xbr'] = '10'
        box.attrib['xtl'] = '100'
        box.attrib['ybr'] = '10'
        box.attrib['ytl'] = '100'

        attr = ET.SubElement(box, 'attribute')
        attr.attrib['name'] = "sender"
        attr.text = senderId

        attr = ET.SubElement(box, 'attribute')
        attr.attrib['name'] = "teamId"
        attr.text = teamId

        attr = ET.SubElement(box, 'attribute')
        attr.attrib['name'] = "receiver"
        attr.text = receiverId
    
    return

def FilteringPassThenGoalToXML(trackId, eventArgs, annotations):

    track = ET.SubElement(annotations, 'track')
    track.attrib['id'] = str(trackId)
    track.attrib['label'] = "FilteringPassThenGoal"

    attributes = eventArgs.split(',')
    startFrame = int(attributes[0])
    endFrame = int(attributes[1])
    senderId = attributes[2]
    teamId = attributes[3]
    scorerId = attributes[4]

    for f in range(startFrame, endFrame):

        box = ET.SubElement(track, 'box')
        box.attrib['frame'] = str(f)
        box.attrib['keyframe'] = '1'
        box.attrib['occluded'] = '0'
        box.attrib['outside'] = '0'
        box.attrib['xbr'] = '10'
        box.attrib['xtl'] = '100'
        box.attrib['ybr'] = '10'
        box.attrib['ytl'] = '100'

        attr = ET.SubElement(box, 'attribute')
        attr.attrib['name'] = "sender"
        attr.text = senderId

        attr = ET.SubElement(box, 'attribute')
        attr.attrib['name'] = "teamId"
        attr.text = teamId

        attr = ET.SubElement(box, 'attribute')
        attr.attrib['name'] = "scorerId"
        attr.text = scorerId
    
    return
    
    
def CrossToXML(trackId, eventArgs, annotations):

    track = ET.SubElement(annotations, 'track')
    track.attrib['id'] = str(trackId)
    track.attrib['label'] = "Cross"

    attributes = eventArgs.split(',')
    startFrame = int(attributes[0])
    endFrame = int(attributes[1])
    senderId = attributes[2]
    teamId = attributes[3]
    receiverId = attributes[4]
    outcome = attributes[5]

    for f in range(startFrame, endFrame):

        box = ET.SubElement(track, 'box')
        box.attrib['frame'] = str(f)
        box.attrib['keyframe'] = '1'
        box.attrib['occluded'] = '0'
        box.attrib['outside'] = '0'
        box.attrib['xbr'] = '10'
        box.attrib['xtl'] = '100'
        box.attrib['ybr'] = '10'
        box.attrib['ytl'] = '100'

        attr = ET.SubElement(box, 'attribute')
        attr.attrib['name'] = "sender"
        attr.text = senderId

        attr = ET.SubElement(box, 'attribute')
        attr.attrib['name'] = "teamId"
        attr.text = teamId

        attr = ET.SubElement(box, 'attribute')
        attr.attrib['name'] = "receiver"
        attr.text = receiverId

        attr = ET.SubElement(box, 'attribute')
        attr.attrib['name'] = "outcome"
        attr.text = outcome
    
    return

def CrossThenGoalToXML(trackId, eventArgs, annotations):

    track = ET.SubElement(annotations, 'track')
    track.attrib['id'] = str(trackId)
    track.attrib['label'] = "CrossThenGoal"

    attributes = eventArgs.split(',')
    startFrame = int(attributes[0])
    endFrame = int(attributes[1])
    senderId = attributes[2]
    teamId = attributes[3]
    scorerId = attributes[4]

    for f in range(startFrame, endFrame):

        box = ET.SubElement(track, 'box')
        box.attrib['frame'] = str(f)
        box.attrib['keyframe'] = '1'
        box.attrib['occluded'] = '0'
        box.attrib['outside'] = '0'
        box.attrib['xbr'] = '10'
        box.attrib['xtl'] = '100'
        box.attrib['ybr'] = '10'
        box.attrib['ytl'] = '100'

        attr = ET.SubElement(box, 'attribute')
        attr.attrib['name'] = "sender"
        attr.text = senderId

        attr = ET.SubElement(box, 'attribute')
        attr.attrib['name'] = "teamId"
        attr.text = teamId

        attr = ET.SubElement(box, 'attribute')
        attr.attrib['name'] = "scorer"
        attr.text = scorerId
    
    return

def TackleToXML(trackId, eventArgs, annotations):

    track = ET.SubElement(annotations, 'track')
    track.attrib['id'] = str(trackId)
    track.attrib['label'] = "Tackle"

    attributes = eventArgs.split(',')
    startFrame = int(attributes[0])
    endFrame = int(attributes[1])
    victimId = attributes[2]
    teamId = attributes[3]
    tacklerId = attributes[4]
    tacklerTeamId = attributes[5]
    outcome = attributes[6]

    if endFrame == startFrame:
        endFrame = startFrame + 1

    for f in range(startFrame, endFrame):

        box = ET.SubElement(track, 'box')
        box.attrib['frame'] = str(f)
        box.attrib['keyframe'] = '1'
        box.attrib['occluded'] = '0'
        box.attrib['outside'] = '0'
        box.attrib['xbr'] = '10'
        box.attrib['xtl'] = '100'
        box.attrib['ybr'] = '10'
        box.attrib['ytl'] = '100'

        attr = ET.SubElement(box, 'attribute')
        attr.attrib['name'] = "victimId"
        attr.text = victimId

        attr = ET.SubElement(box, 'attribute')
        attr.attrib['name'] = "teamId"
        attr.text = teamId

        attr = ET.SubElement(box, 'attribute')
        attr.attrib['name'] = "tacklerId"
        attr.text = tacklerId

        attr = ET.SubElement(box, 'attribute')
        attr.attrib['name'] = "tacklerTeamId"
        attr.text = tacklerTeamId

        attr = ET.SubElement(box, 'attribute')
        attr.attrib['name'] = "outcome"
        attr.text = outcome

    return

def ShotToXML(trackId, eventArgs, annotations):

    track = ET.SubElement(annotations, 'track')
    track.attrib['id'] = str(trackId)
    track.attrib['label'] = "Shot"

    attributes = eventArgs.split(',')
    startFrame = int(attributes[0])
    endFrame = int(attributes[1])
    shooterId = attributes[2]
    teamId = attributes[3]

    for f in range(startFrame, endFrame):

        box = ET.SubElement(track, 'box')
        box.attrib['frame'] = str(f)
        box.attrib['keyframe'] = '1'
        box.attrib['occluded'] = '0'
        box.attrib['outside'] = '0'
        box.attrib['xbr'] = '10'
        box.attrib['xtl'] = '100'
        box.attrib['ybr'] = '10'
        box.attrib['ytl'] = '100'

        attr = ET.SubElement(box, 'attribute')
        attr.attrib['name'] = "shooterId"
        attr.text = shooterId

        attr = ET.SubElement(box, 'attribute')
        attr.attrib['name'] = "teamId"
        attr.text = teamId

    return

def ShotOutToXML(trackId, eventArgs, annotations):

    track = ET.SubElement(annotations, 'track')
    track.attrib['id'] = str(trackId)
    track.attrib['label'] = "ShotOut"

    attributes = eventArgs.split(',')
    startFrame = int(attributes[0])
    endFrame = int(attributes[1])
    shooterId = attributes[2]
    teamId = attributes[3]

    for f in range(startFrame, endFrame):

        box = ET.SubElement(track, 'box')
        box.attrib['frame'] = str(f)
        box.attrib['keyframe'] = '1'
        box.attrib['occluded'] = '0'
        box.attrib['outside'] = '0'
        box.attrib['xbr'] = '10'
        box.attrib['xtl'] = '100'
        box.attrib['ybr'] = '10'
        box.attrib['ytl'] = '100'

        attr = ET.SubElement(box, 'attribute')
        attr.attrib['name'] = "shooterId"
        attr.text = shooterId

        attr = ET.SubElement(box, 'attribute')
        attr.attrib['name'] = "teamId"
        attr.text = teamId

    return

def ShotThenGoalToXML(trackId, eventArgs, annotations):

    track = ET.SubElement(annotations, 'track')
    track.attrib['id'] = str(trackId)
    track.attrib['label'] = "ShotThenGoal"

    attributes = eventArgs.split(',')
    startFrame = int(attributes[0])
    endFrame = int(attributes[1])
    shooterId = attributes[2]
    teamId = attributes[3]

    for f in range(startFrame, endFrame):

        box = ET.SubElement(track, 'box')
        box.attrib['frame'] = str(f)
        box.attrib['keyframe'] = '1'
        box.attrib['occluded'] = '0'
        box.attrib['outside'] = '0'
        box.attrib['xbr'] = '10'
        box.attrib['xtl'] = '100'
        box.attrib['ybr'] = '10'
        box.attrib['ytl'] = '100'

        attr = ET.SubElement(box, 'attribute')
        attr.attrib['name'] = "shooterId"
        attr.text = shooterId

        attr = ET.SubElement(box, 'attribute')
        attr.attrib['name'] = "teamId"
        attr.text = teamId
        
    return

def SavedShotToXML(trackId, eventArgs, annotations):

    track = ET.SubElement(annotations, 'track')
    track.attrib['id'] = str(trackId)
    track.attrib['label'] = "SavedShot"

    attributes = eventArgs.split(',')
    startFrame = int(attributes[0])
    endFrame = int(attributes[1])
    shooterId = attributes[2]
    teamId = attributes[3]
    goalkeeperId = attributes[4]
    goalkeeperTeamId = attributes[5]
    goalkeeperPosX = attributes[6]
    goalkeeperPosY = attributes[7]
    case = attributes[8]
    
    for f in range(startFrame, endFrame):

        box = ET.SubElement(track, 'box')
        box.attrib['frame'] = str(f)
        box.attrib['keyframe'] = '1'
        box.attrib['occluded'] = '0'
        box.attrib['outside'] = '0'
        box.attrib['xbr'] = '10'
        box.attrib['xtl'] = '100'
        box.attrib['ybr'] = '10'
        box.attrib['ytl'] = '100'

        attr = ET.SubElement(box, 'attribute')
        attr.attrib['name'] = "shooterId"
        attr.text = shooterId

        attr = ET.SubElement(box, 'attribute')
        attr.attrib['name'] = "teamId"
        attr.text = teamId

        attr = ET.SubElement(box, 'attribute')
        attr.attrib['name'] = "goalkeeperId"
        attr.text = goalkeeperId

        attr = ET.SubElement(box, 'attribute')
        attr.attrib['name'] = "goalkeeperTeamId"
        attr.text = goalkeeperTeamId

        attr = ET.SubElement(box, 'attribute')
        attr.attrib['name'] = "goalkeeperPosX"
        attr.text = goalkeeperPosX

        attr = ET.SubElement(box, 'attribute')
        attr.attrib['name'] = "goalkeeperPosY"
        attr.text = goalkeeperPosY

        attr = ET.SubElement(box, 'attribute')
        attr.attrib['name'] = "case"
        attr.text = case[0].upper() + case[1:]
        
    return