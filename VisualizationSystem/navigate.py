import os
import numpy as np
import cv2
import dicttoxml
import xml.etree.ElementTree as ET
import xml.dom.minidom as DOM
from datetime import datetime, timedelta


# Set variable(s)
directory = "."
app_name = "Visualization System"
input_folder = "frames"
description_file = "input/description.txt"
positions_input_file = "input/positions_timestamp.log"

ground_atomic_input_file = "input/Annotations_AtomicEvents.xml"
ground_complex_input_file = "input/Annotations_ComplexEvents.xml"
detected_atomic_input_file = "input/Annotations_AtomicEvents_Detected.xml"
detected_complex_input_file = "input/Annotations_ComplexEvents_Detected.xml"

# Initialize variable(s)
interaction_window = {}
interaction_window_pointer = [0]
interaction_windows_size = 21
video_frames_count = 0


# TODO configure these params 
# Offset to translate the starting time of the match taking it from the video, removing all previous frames from dir (calcio d'inizio)
initial_offset = 3280
# Value in milliseconds between 2 consecutive images. If FPS of video changes this must be set accordingly
step = 1000 * 1/25


def callback(x):
    """
    GUI Window Trackbar Callback
    """

    interaction_window_pointer[0] = x
    try:

        read_frames(interaction_window_pointer, interaction_windows_size, interaction_window, video_frames_count)
        frame = interaction_window[str(interaction_window_pointer[0])]
        cur_timestamp = str(int(int(interaction_window_pointer[0]) * 1000 / 25))
        if frame is not None:
            
            # Priting BBox and Annotations over the current image
            #frame = drawBoundingBox(frame, bounding_box_data_list)
            #frame = drawAnnotations(frame, dicts, current_complex_event, current_complex_event_detected)
            #frame = resize_image(frame)
            #cv2.imshow(app_name, frame)

            # Showing info to CLI
            if (not(is_exporting)):
                print("[Visualization System] Frame: {:06}".format(interaction_window_pointer[0]))
                print("[Visualization System] Second: " + str(int(cur_timestamp) / 1000), end="\r\n\r\n")
            
    except Exception as e:
        print("[Exception] " + e.args)
        


def drawText(img, text, x, y):
    # Write some Text over the image
    font                   = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (x,y)
    fontScale              = 0.5
    fontColor              = (0,255,255)
    lineType               = 1

    cv2.putText(img,text, 
        bottomLeftCornerOfText, 
        font, 
        fontScale,
        fontColor,
        lineType)


def read_players_positions(positions_file):
    """
    Read players positions
    """

    # Show info to CLI
    print("[Players Positions] Reading...")

    # Initialize dictionaries
    dict_timestamp = {}
    dict_game_frame = {}

    # Used to normalize data inside the same game_frame (each of 23 entry will have same timestamp) 
    counter = 0
    last_timestamp = 0

    # Read file
    with open(positions_file, "r") as input_file:

        # For each line
        lines = input_file.readlines()
        for line in lines:

            # Parse and extract
            timestamp, game_frame, player, x, y = line.rstrip().split(' ')

            # Normalization phase inside 23 elements (same timestamp). Used to avoid missing BB in a frame.
            if (counter == 0):
                last_timestamp = timestamp
            else:
                timestamp = last_timestamp
                if (counter == 22):
                    counter = -1

            counter = counter + 1

            # Create a list (if empty)
            if dict_timestamp.get(timestamp) is None:
                dict_timestamp[timestamp] = []

            # Fill the list
            dict_timestamp[timestamp].append({ 'game_frame': game_frame, 'player': player, 'x': x, 'y': y })
            
            # Create a list (if empty)
            if dict_game_frame.get(game_frame) is None:
                dict_game_frame[game_frame] = []

            # Fill the list
            dict_game_frame[game_frame].append({ 'timestamp': timestamp })

    # Show info to CLI
    print("[Players Positions] Loaded.", end='\r\n\r\n')

    return dict_game_frame, dict_timestamp


def read_frames(interaction_window_pointer, interaction_windows_size, interaction_window, video_frames_count):
    """
    Read frame from image and load in primary memory.
    """

    # Initialize variable(s)
    frames_to_read = []

    # Set the interaction window pointer
    p = interaction_window_pointer[0]
    frames_to_read.append(p)

    # Collect the previous and subsequent frames
    wing_size = int((interaction_windows_size) /2)
    for i in range(1, wing_size + 1):
        if (p - i) >= 0:
            frames_to_read.append(p - i)
        if (p + i ) <= video_frames_count:
            frames_to_read.append(p + i)

    # Check and add the frames
    for frame_number in frames_to_read:
        frame_number_string = str(frame_number)

        # If not already present into the interaction window
        if interaction_window.get(frame_number_string) is None:

            # Get the frame
            filename = "frame-" + str(frame_number).zfill(6) + ".jpg"
            image_path = os.path.join(input_folder, filename)
            frame = cv2.imread(image_path)

            # Add it to the interaction window
            interaction_window[str(frame_number)] = frame
            if (len(interaction_window)) > interaction_windows_size:
                break 

    # Delete old frames
    frames_to_delete = []
    for frame_number in interaction_window:
        if int(frame_number) not in frames_to_read:
            frames_to_delete.append(frame_number)
    for frames_number in frames_to_delete:
        del interaction_window[frames_number]
            

    return interaction_window


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




# Function to read data about annotations from filesystem specifing filenames. Returns an object containing 4 dictionaries
def read_annotations(ground_atomic_filename, ground_complex_filename, detected_atomic_filename = None, detected_complex_filename = None):
    
    ground_atomic = XML.createDictionary(ground_atomic_filename)
    ground_complex = XML.createDictionary(ground_complex_filename)

    detected_atomic = None
    detected_complex = None
    
    if (detected_atomic_filename is not None):
        detected_atomic = XML.createDictionary(detected_atomic_filename)
    if (detected_complex_filename is not None):
        detected_complex = XML.createDictionary(detected_complex_filename)

    annotations_dicts = {
        "ground_atomic": ground_atomic,
        "ground_complex": ground_complex,
        "detected_atomic": detected_atomic,
        "detected_complex": detected_complex 
    }

    return annotations_dicts


x_ground_atomic = 10
y_ground_atomic = 980

x_ground_complex = int(1920 / 4 + 10)
y_ground_complex = 980

x_detected_atomic = int(1920 / 2)
y_detected_atomic = 980

x_detected_complex = int(3 * 1920 / 4)
y_detected_complex = 980

# Distance between events on the same column
y_offset_between_events = 100


def get_xy(is_ground, is_atomic):
    if (is_ground):
        if (is_atomic):
            x = x_ground_atomic
            y = y_ground_atomic
        else:
            x = x_ground_complex
            y = y_ground_complex
    else:
        if (is_atomic):
            x = x_detected_atomic
            y = y_detected_atomic
        else:
            x = x_detected_complex
            y = y_detected_complex

    return x, y

def get_title(is_ground, is_atomic):
    if (is_ground):
        if (is_atomic):
            title = "Ground atomic event: "
        else:
            title = "Ground complex event: "
    else:
        if (is_atomic):
            title = "Detected atomic event: "
        else:
            title = "Detected complex event: "

    return title

# Atomic events

def printBallPossession(current_image, dict_elem, elem_num, is_ground):
    x, y = get_xy(is_ground, True)
    title = get_title(is_ground, True)

    player_id = dict_elem["playerId"]
    team_id   = dict_elem["teamId"]
    player_x  = dict_elem["x"]
    player_y  = dict_elem["y"]
    cur_frame = dict_elem["finalFrame"]

    if (team_id == '1'): player_id = str(int(player_id) + 128)
    
    outermost_player_id      = dict_elem["outermostOtherTeamDefensivePlayerId"]
    outermost_player_team_id = dict_elem["outermostOtherTeamDefensivePlayerTeamId"]
    outermost_player_x       = dict_elem["outermostOtherTeamDefensivePlayerX"]
    outermost_player_y       = dict_elem["outermostOtherTeamDefensivePlayerY"]

    if (outermost_player_team_id == '1'): outermost_player_id = str(int(outermost_player_id) + 128)

    offset = elem_num * y_offset_between_events

    drawText(current_image, title + "BALL POSSESSION", x, y - offset)

    text = "Player id = " + player_id + "    (x, y) = (" + player_x + ", " + player_y + ")"
    drawText(current_image, text, x, y + 20 - offset)

    text = "Outermost player id = " + outermost_player_id + "    (x, y) = (" + outermost_player_x + ", " + outermost_player_y + ")"
    drawText(current_image, text, x, y + 40 - offset)
    
    text = "Frame = " + str(cur_frame)
    drawText(current_image, text, x, y + 60 - offset)
    

def printKickingTheBall(current_image, dict_elem, elem_num, is_ground):
    x, y = get_xy(is_ground, True)
    title = get_title(is_ground, True)

    player_id = dict_elem["playerId"]
    team_id   = dict_elem["teamId"]
    player_x  = dict_elem["x"]
    player_y  = dict_elem["y"]
    cur_frame = dict_elem["finalFrame"]
    
    if (team_id == '1'): player_id = str(int(player_id) + 128)

    offset = elem_num * y_offset_between_events

    drawText(current_image, title + "KICKING THE BALL", x, y - offset)

    text = "Player id = " + player_id + "    (x, y) = (" + player_x + ", " + player_y + ")"
    drawText(current_image, text, x, y + 20 - offset)
    
    text = "Frame = " + str(cur_frame)
    drawText(current_image, text, x, y + 40 - offset)


def printAtomicTackle(current_image, dict_elem, elem_num, is_ground):
    x, y = get_xy(is_ground, True)
    title = get_title(is_ground, True)

    player_id = dict_elem["playerId"]
    team_id   = dict_elem["teamId"]
    player_x  = dict_elem["x"]
    player_y  = dict_elem["y"]
    cur_frame = dict_elem["finalFrame"]

    tackler_id      = dict_elem["tacklingPlayerId"]
    tackler_team_id = dict_elem["tacklingPlayerTeamId"]
    tackler_x       = dict_elem["tacklingPlayerX"]
    tackler_y       = dict_elem["tacklingPlayerY"]

    if (team_id == '1'):          player_id = str(int(player_id) + 128)
    if (tackler_team_id == '1'): tackler_id = str(int(tackler_id) + 128)

    offset = elem_num * y_offset_between_events

    drawText(current_image, title + "TACKLE", x, y - offset)

    text = "Victim id  = " + player_id + "    (x, y) = (" + player_x + ", " + player_y + ")"
    drawText(current_image, text, x, y + 20 - offset)

    text = "Tackler id = " + tackler_id + "    (x, y) = (" + tackler_x + ", " + tackler_y + ")"
    drawText(current_image, text, x, y + 40 - offset)

    text = "Frame = " + str(cur_frame)
    drawText(current_image, text, x, y + 60 - offset)


def printBallDeflection(current_image, dict_elem, elem_num, is_ground):
    x, y = get_xy(is_ground, True)
    title = get_title(is_ground, True)

    player_id = dict_elem["playerId"]
    team_id   = dict_elem["teamId"]
    player_x  = dict_elem["x"]
    player_y  = dict_elem["y"]
    cur_frame = dict_elem["finalFrame"]

    if (team_id == '1'): player_id = str(int(player_id) + 128)

    offset = elem_num * y_offset_between_events
    
    drawText(current_image, title + "BALL DEFLECTION", x, y - offset)

    text = "Player id  = " + player_id + "    (x, y) = (" + player_x + ", " + player_y + ")"
    drawText(current_image, text, x, y + 20 - offset)

    text = "Frame = " + str(cur_frame)
    drawText(current_image, text, x, y + 40 - offset)


def printBallOut(current_image, dict_elem, elem_num, is_ground):
    x, y = get_xy(is_ground, True)
    title = get_title(is_ground, True)

    cur_frame = dict_elem["finalFrame"]

    offset = elem_num * y_offset_between_events

    drawText(current_image, title + "BALL OUT", x, y - offset)

    text = "Frame = " + str(cur_frame)
    drawText(current_image, text, x, y + 20 - offset)


def printGoal(current_image, dict_elem, elem_num, is_ground):
    x, y = get_xy(is_ground, True)
    title = get_title(is_ground, True)

    player_id = dict_elem["scorer"]
    team_id   = dict_elem["team"]
    cur_frame = dict_elem["finalFrame"]

    if (team_id == '1'): player_id = str(int(player_id) + 128)

    offset = elem_num * y_offset_between_events

    drawText(current_image, title + "GOAL", x, y - offset)

    text = "Player id  = " + player_id
    drawText(current_image, text, x, y + 20 - offset)

    text = "Frame = " + str(cur_frame)
    drawText(current_image, text, x, y + 40 - offset)


def printFoul(current_image, dict_elem, elem_num, is_ground):
    x, y = get_xy(is_ground, True)
    title = get_title(is_ground, True)

    player_id = dict_elem["scorer"]
    team_id   = dict_elem["team"]
    cur_frame = dict_elem["finalFrame"]

    if (team_id == '1'): player_id = str(int(player_id) + 128)
    
    offset = elem_num * y_offset_between_events
    
    drawText(current_image, title + "FOUL", x, y - offset)

    text = "Player id  = " + player_id
    drawText(current_image, text, x, y + 20 - offset)

    text = "Frame = " + str(cur_frame)
    drawText(current_image, text, x, y + 40 - offset)


def printPenalty(current_image, dict_elem, elem_num, is_ground):
    x, y = get_xy(is_ground, True)
    title = get_title(is_ground, True)

    player_id = dict_elem["scorer"]
    team_id   = dict_elem["team"]
    cur_frame = dict_elem["finalFrame"]

    if (team_id == '1'): player_id = str(int(player_id) + 128)

    offset = elem_num * y_offset_between_events
    
    drawText(current_image, title + "PENALTY", x, y)

    text = "Player id  = " + player_id
    drawText(current_image, text, x, y + 20 - offset)

    text = "Frame = " + str(cur_frame)
    drawText(current_image, text, x, y + 40 - offset)


def printAtomicEvent(image, elem, elem_num, is_ground):
    event = elem["name"]

    if (event == "BallPossession"):
        printBallPossession(image, elem, elem_num, is_ground)
    elif (event == "KickingTheBall"):
        printKickingTheBall(image, elem, elem_num, is_ground)
    elif (event == "Tackle"):
        printAtomicTackle(image, elem, elem_num, is_ground)
    elif (event == "BallDeflection"):
        printBallDeflection(image, elem, elem_num, is_ground)
    elif (event == "BallOut"):
        printBallOut(image, elem, elem_num, is_ground)
    elif (event == "Goal"):
        printGoal(image, elem, elem_num, is_ground)
    elif (event == "Foul"):
        printFoul(image, elem, elem_num, is_ground)
    elif (event == "Penalty"):
        printPenalty(image, elem, elem_num, is_ground)


# Complex events

def printPass(current_image, dict_elem, elem_num, is_ground):
    x, y = get_xy(is_ground, False)
    title = get_title(is_ground, False)

    sender      = dict_elem["sender"]
    team_id     = dict_elem["teamId"]
    receiver    = dict_elem["receiver"]
    start_frame = dict_elem["startFrame"]
    final_frame = dict_elem["finalFrame"]

    if (team_id == '1'): 
        sender = str(int(sender) + 128)
        receiver = str(int(receiver) + 128)
    
    offset = elem_num * y_offset_between_events
    
    drawText(current_image, title + "PASS", x, y - offset)

    text = "Sender id = " + sender + "    Receiver id = " + receiver
    drawText(current_image, text, x, y + 20 - offset)

    text = "Start frame = " + str(start_frame) + "    Final frame = " + str(final_frame)
    drawText(current_image, text, x, y + 40 - offset)


def printPassThenGoal(current_image, dict_elem, elem_num, is_ground):
    x, y = get_xy(is_ground, False)
    title = get_title(is_ground, False)

    sender      = dict_elem["sender"]
    team_id     = dict_elem["teamId"]
    scorer      = dict_elem["scorer"]
    start_frame = dict_elem["startFrame"]
    final_frame = dict_elem["finalFrame"]

    if (team_id == '1'): 
        sender = str(int(sender) + 128)
        scorer = str(int(scorer) + 128)
    
    offset = elem_num * y_offset_between_events
    
    drawText(current_image, title + "PASS THEN GOAL", x, y - offset)

    text = "Sender id = " + sender + "    Scorer id = " + scorer
    drawText(current_image, text, x, y + 20 - offset)

    text = "Start frame = " + str(start_frame) + "    Final frame = " + str(final_frame)
    drawText(current_image, text, x, y + 40 - offset)


def printFilteringPass(current_image, dict_elem, elem_num, is_ground):
    x, y = get_xy(is_ground, False)
    title = get_title(is_ground, False)

    sender      = dict_elem["sender"]
    team_id     = dict_elem["teamId"]
    receiver    = dict_elem["receiver"]
    start_frame = dict_elem["startFrame"]
    final_frame = dict_elem["finalFrame"]

    if (team_id == '1'): 
        sender = str(int(sender) + 128)
        receiver = str(int(receiver) + 128)

    offset = elem_num * y_offset_between_events
    
    drawText(current_image, title + "FILTERING PASS", x, y - offset)

    text = "Sender id = " + sender + "    Receiver id = " + receiver
    drawText(current_image, text, x, y + 20 - offset)

    text = "Start frame = " + str(start_frame) + "    Final frame = " + str(final_frame)
    drawText(current_image, text, x, y + 40 - offset)


def printFilteringPassThenGoal(current_image, dict_elem, elem_num, is_ground):
    x, y = get_xy(is_ground, False)
    title = get_title(is_ground, False)

    sender      = dict_elem["sender"]
    team_id     = dict_elem["teamId"]
    scorer      = dict_elem["scorer"]
    start_frame = dict_elem["startFrame"]
    final_frame = dict_elem["finalFrame"]

    if (team_id == '1'): 
        sender = str(int(sender) + 128)
        scorer = str(int(scorer) + 128)

    offset = elem_num * y_offset_between_events
    
    drawText(current_image, title + "FILTERING PASS THEN GOAL", x, y - offset)

    text = "Sender id = " + sender + "    Scorer id = " + scorer
    drawText(current_image, text, x, y + 20 - offset)

    text = "Start frame = " + str(start_frame) + "    Final frame = " + str(final_frame)
    drawText(current_image, text, x, y + 40 - offset)


def printCross(current_image, dict_elem, elem_num, is_ground):
    x, y = get_xy(is_ground, False)
    title = get_title(is_ground, False)

    sender      = dict_elem["sender"]
    team_id     = dict_elem["teamId"]
    receiver    = dict_elem["receiver"]
    start_frame = dict_elem["startFrame"]
    final_frame = dict_elem["finalFrame"]
    outcome     = dict_elem["outcome"]

    if (team_id == '1'): 
        sender = str(int(sender) + 128)
        receiver = str(int(receiver) + 128)

    if (outcome == "true"):
        outcome = "Success"
    else:
        outcome = "Failure"
    
    offset = elem_num * y_offset_between_events

    drawText(current_image, title + "CROSS", x, y - offset)

    text = "Sender id = " + sender + "    Receiver id = " + receiver + "    Result = " + outcome
    drawText(current_image, text, x, y + 20 - offset)

    text = "Start frame = " + str(start_frame) + "    Final frame = " + str(final_frame)
    drawText(current_image, text, x, y + 40 - offset)


def printCrossTheGoal(current_image, dict_elem, elem_num, is_ground):
    x, y = get_xy(is_ground, False)
    title = get_title(is_ground, False)

    sender      = dict_elem["sender"]
    team_id     = dict_elem["teamId"]
    scorer      = dict_elem["scorer"]
    start_frame = dict_elem["startFrame"]
    final_frame = dict_elem["finalFrame"]

    if (team_id == '1'): 
        sender = str(int(sender) + 128)
        scorer = str(int(scorer) + 128)

    offset = elem_num * y_offset_between_events
    
    drawText(current_image, title + "CROSS THEN GOAL", x, y - offset)

    text = "Sender id = " + sender + "    Scorer id = " + scorer
    drawText(current_image, text, x, y + 20 - offset)

    text = "Start frame = " + str(start_frame) + "    Final frame = " + str(final_frame)
    drawText(current_image, text, x, y + 40 - offset)


def printTackle(current_image, dict_elem, elem_num, is_ground):
    x, y = get_xy(is_ground, False)
    title = get_title(is_ground, False)

    victim      = dict_elem["victimId"]
    team_id     = dict_elem["teamId"]
    tackler     = dict_elem["tacklerId"]
    start_frame = dict_elem["startFrame"]
    final_frame = dict_elem["finalFrame"]
    outcome     = dict_elem["outcome"]

    if (team_id == '1'): 
        victim = str(int(victim) + 128)
    else:
        tackler = str(int(tackler) + 128)

    if (outcome == "true"):
        outcome = "Success"
    else:
        outcome = "Failure"

    offset = elem_num * y_offset_between_events
    
    drawText(current_image, title + "TACKLE", x, y - offset)

    text = "Victim id = " + victim + "    Tackler id = " + tackler + "    Result = " + outcome
    drawText(current_image, text, x, y + 20 - offset)

    text = "Start frame = " + str(start_frame) + "    Final frame = " + str(final_frame)
    drawText(current_image, text, x, y + 40 - offset)


def printShot(current_image, dict_elem, elem_num, is_ground):
    x, y = get_xy(is_ground, False)
    title = get_title(is_ground, False)

    shooter     = dict_elem["shooterId"]
    team_id     = dict_elem["teamId"]
    start_frame = dict_elem["startFrame"]
    final_frame = dict_elem["finalFrame"]

    if (team_id == '1'): 
        shooter = str(int(shooter) + 128)

    offset = elem_num * y_offset_between_events
    
    drawText(current_image, title + "SHOT", x, y - offset)

    text = "Shooter id = " + shooter
    drawText(current_image, text, x, y + 20 - offset)

    text = "Start frame = " + str(start_frame) + "    Final frame = " + str(final_frame)
    drawText(current_image, text, x, y + 40 - offset)


def printShotThenGoal(current_image, dict_elem, elem_num, is_ground):
    x, y = get_xy(is_ground, False)
    title = get_title(is_ground, False)

    shooter     = dict_elem["shooterId"]
    team_id     = dict_elem["teamId"]
    start_frame = dict_elem["startFrame"]
    final_frame = dict_elem["finalFrame"]

    if (team_id == '1'): 
        shooter = str(int(shooter) + 128)

    offset = elem_num * y_offset_between_events
    
    drawText(current_image, title + "SHOT THEN GOAL", x, y - offset)

    text = "Shooter id = " + shooter
    drawText(current_image, text, x, y + 20 - offset)

    text = "Start frame = " + str(start_frame) + "    Final frame = " + str(final_frame)
    drawText(current_image, text, x, y + 40 - offset)


def printSavedShot(current_image, dict_elem, elem_num, is_ground):
    x, y = get_xy(is_ground, False)
    title = get_title(is_ground, False)

    shooter     = dict_elem["shooterId"]
    team_id     = dict_elem["teamId"]
    goolkeeper  = dict_elem["goalkeeperId"]
    if (dict_elem.get("team2Id") is not None):
        team_2_id   = dict_elem["team2Id"]
    else:    
        team_2_id = dict_elem["goalkeeperTeamId"]    
    start_frame = dict_elem["startFrame"]
    final_frame = dict_elem["finalFrame"]
    case        = dict_elem["case"]

    if (team_id == '1'):   shooter    = str(int(shooter) + 128)
    if (team_2_id == '1'): goolkeeper = str(int(goolkeeper) + 128)

    offset = elem_num * y_offset_between_events
    
    drawText(current_image, title + "SAVED SHOT", x, y - offset)

    text = "Shooter id = " + shooter + "    Goalkeeper id = " + goolkeeper
    drawText(current_image, text, x, y + 20 - offset)
    
    text = "Location = " + case
    drawText(current_image, text, x, y + 40 - offset)

    text = "Start frame = " + str(start_frame) + "    Final frame = " + str(final_frame)
    drawText(current_image, text, x, y + 60 - offset)

    
def printShotOut(current_image, dict_elem, elem_num, is_ground):
    x, y = get_xy(is_ground, False)
    title = get_title(is_ground, False)

    shooter     = dict_elem["shooterId"]
    team_id     = dict_elem["teamId"]
    start_frame = dict_elem["startFrame"]
    final_frame = dict_elem["finalFrame"]

    if (team_id == '1'): 
        shooter = str(int(shooter) + 128)

    offset = elem_num * y_offset_between_events
    
    drawText(current_image, title + "SHOT OUT", x, y - offset)

    text = "Shooter id = " + shooter
    drawText(current_image, text, x, y + 20 - offset)

    text = "Start frame = " + str(start_frame) + "    Final frame = " + str(final_frame)
    drawText(current_image, text, x, y + 40 - offset)


def printComplexEvent(image, elem, elem_num, is_ground):
    event = elem["name"]
    
    if (event == "Pass"):
        printPass(image, elem, elem_num, is_ground)
    elif (event == "Tackle"):
        printTackle(image, elem, elem_num, is_ground)
    elif (event == "PassThenGoal"):
        printPassThenGoal(image, elem, elem_num, is_ground)
    elif (event == "FilteringPass"):
        printFilteringPass(image, elem, elem_num, is_ground)
    elif (event == "FilteringPassThenGoal"):
        printFilteringPassThenGoal(image, elem, elem_num, is_ground)
    elif (event == "Cross"):
        printCross(image, elem, elem_num, is_ground)
    elif (event == "CrossThenGoal"):
        printCrossTheGoal(image, elem, elem_num, is_ground)
    elif (event == "Shot"):
        printShot(image, elem, elem_num, is_ground)
    elif (event == "ShotThenGoal"):
        printShotThenGoal(image, elem, elem_num, is_ground)
    elif (event == "SavedShot"):
        printSavedShot(image, elem, elem_num, is_ground)
    elif (event == "ShotOut"):
        printShotOut(image, elem, elem_num, is_ground)




def resize_image(image):
    # percent of original size
    scale_percent = 90
    width = int(image.shape[1] * scale_percent / 100) 
    height = int(image.shape[0] * scale_percent / 100) 
    dim = (width, height) 

    # resize image
    return cv2.resize(image, dim, interpolation = cv2.INTER_AREA) 


# Read the description file
# to get the total number of frames
f = open(description_file, "r")
if f.mode == 'r':
    l = f.readline()
    print("[Video Description] Number of frames: {}".format(l))
    video_frames_count = int(l)
f.close()

read_frames(interaction_window_pointer, interaction_windows_size, interaction_window, video_frames_count)
dict_game_frame, dict_timestamp = read_players_positions(positions_input_file)


dicts = None

# Deciding what to show depending on what file is in there
detected_atomic_found = os.path.isfile(detected_atomic_input_file)
detected_complex_found = os.path.isfile(detected_complex_input_file)

if (detected_atomic_found and detected_complex_found):
    dicts = read_annotations(ground_atomic_input_file, ground_complex_input_file, detected_atomic_input_file, detected_complex_input_file)
elif (detected_atomic_found): 
    dicts = read_annotations(ground_atomic_input_file, ground_complex_input_file, detected_atomic_input_file)
elif (detected_complex_found):
    dicts = read_annotations(ground_atomic_input_file, ground_complex_input_file, None, detected_complex_input_file)
else:
    # Reading only the ground-truth files
    dicts = read_annotations(ground_atomic_input_file, ground_complex_input_file)    


# Create the window
cv2.namedWindow(app_name, cv2.WINDOW_GUI_NORMAL)
cv2.createTrackbar('Frame', app_name, 0, video_frames_count, callback)

print("[Visualization System] Press arrow key to move around, Esc to exit.")
print("[Visualization System] Waiting for... ", end="\r\n\r\n")

lineThickness = 2
current_frame = None
current_complex_events = []
current_complex_events_detected = []

is_exporting = False
out_video = None

auto_play = False


def drawBoundingBox(image, bounding_box_data_list):
    # Here list is list is made of objects like that: {'game_frame': '230', 'player': '128', 'x': '812', 'y': '369'} ...
    for bounding_box_data in bounding_box_data_list:
        
        id = int(bounding_box_data["player"])
        x = int(bounding_box_data["x"])
        y = int(bounding_box_data["y"])

        # Painting BB of the ball
        if (id == 128):
            cv2.rectangle(image, (x - 10, y - 10), (x + 10, y + 10), (0,255,0), lineThickness)
            continue

        # Skipping players not visible on the screen
        if (x == 0 or x == 1919 or y == 0 or y == 1079):
            continue

        # Just correcting statically some BB sizes basing on x and y on the screen (this is optional)
        x1 = x - 20; x2 = x + 30
        y1 = y - 90; y2 = y + 10

        if (y < 270):   y1 = y1 + 20; x1 = x1 + 2; x2 = x2 - 2
        elif (y < 540): y1 = y1 + 10; x1 = x1 + 1; x2 = x2 - 1

        cv2.rectangle(image, (x1, y1), (x2, y2), (0,255,0), lineThickness)

    return image

# This value represents the ratio of frames of the game inside a single frame of the video
# If the game goes at 1 frame each 10 ms, and the video is 30 fps, each video frame may containt up to 4 events
# (1 frame video = 1/30 s = 0.033 ms -> 3 game frame + 1 game frame every 4 frames) 
# To avoid missing events, this value should be the integer greater than the ratio (video_frame_ms / game_frame_ms)
NUM_EVENTS_PER_FRAME = 4


def drawAnnotations(image, dicts, current_complex_event, current_complex_event_detected):
    # Printing atomic data on screen
    i = 0
    while (i < NUM_EVENTS_PER_FRAME):
        elem = dicts["ground_atomic"].get(str(int(frame) - i))
        if (elem is not None):
            printAtomicEvent(image, elem, i, True)
        i = i + 1

    
    # Printing complex data on screen
    i = 0
    while (i < NUM_EVENTS_PER_FRAME):
        elem = dicts["ground_complex"].get(str(int(frame) - i))
        if (elem is not None):
            elem["count"] = i
            printComplexEvent(image, elem, i, True)
            current_complex_events.append(elem)
        i = i + 1

    for elem in current_complex_events:
        if (elem is not None):
            final_frame = int(elem["finalFrame"])
            start_frame = int(elem["startFrame"])

            if (start_frame > int(frame)):
                current_complex_events.remove(elem)
            elif (final_frame > int(frame)):
                i = elem["count"]
                printComplexEvent(image, elem, i, True)
            else:
                current_complex_events.remove(elem)


    if (dicts["detected_atomic"] is not None):
        # Printing detected atomic data on screen
        i = 0
        while (i < NUM_EVENTS_PER_FRAME):
            elem = dicts["detected_atomic"].get(str(int(frame) - i))
            if (elem is not None):
                printAtomicEvent(image, elem, i, False)
            i = i + 1

    if (dicts["detected_complex"] is not None):
        # Printing detected complex data on screen
        i = 0
        while (i < NUM_EVENTS_PER_FRAME):
            elem = dicts["detected_complex"].get(str(int(frame) - i))
            if (elem is not None):
                elem["count"] = i
                printComplexEvent(image, elem, i, False)            
                current_complex_events_detected.append(elem)
            i = i + 1

        for elem in current_complex_events_detected:
            if (elem is not None):
                final_frame = int(elem["finalFrame"])
                start_frame = int(elem["startFrame"])

                if (start_frame > int(frame)):
                    current_complex_events_detected.remove(elem)
                elif (final_frame > int(frame)):
                    i = elem["count"]
                    printComplexEvent(image, elem, i, False)
                else:
                    current_complex_events_detected.remove(elem)

    return image



while(True):

    # Image to draw over to
    if interaction_window_pointer[0] != current_frame or current_frame is None:
        current_frame = interaction_window_pointer[0]
        # To avoid trackbar to go -1 and cause a crash 
        if (current_frame < 0): 
            current_frame = 0
            interaction_window_pointer[0] = 0
            current_image = interaction_window[str(current_frame)]
            cur_timestamp = str(initial_offset + int(step * current_frame))
            continue
        
        if (current_frame >= video_frames_count): 
            current_frame = video_frames_count - 1
            interaction_window_pointer[0] = current_frame
            current_image = interaction_window[str(current_frame)]
            cur_timestamp = str(initial_offset + int(step * current_frame))
            continue
        
        current_image = interaction_window[str(current_frame)]
        cur_timestamp = str(initial_offset + int(step * current_frame))
        
    # Taking from dictionary the list of 23 elements with that timestamp in millis
    bounding_box_data_list = dict_timestamp.get(str(cur_timestamp))
    while bounding_box_data_list is None:
        #Searching for the next timestamp in the dictionary
        cur_timestamp = int(cur_timestamp) + 1
        bounding_box_data_list = dict_timestamp.get(str(cur_timestamp))


    # Taking current frame to acces data on dictionaries
    frame = bounding_box_data_list[0]["game_frame"]
    if (not(is_exporting)):
        print("[Visualization System] Frame used to acces dicts: " + frame)

    # Priting BBox and Annotations over the current image
    current_image = drawBoundingBox(current_image, bounding_box_data_list)
    current_image = drawAnnotations(current_image, dicts, current_complex_events, current_complex_events_detected)

    current_image = resize_image(current_image)
    cv2.imshow(app_name, current_image)

    if (is_exporting and (video_frames_count - 1) == interaction_window_pointer[0]):  
        out_video.release()
        is_exporting = False
        print("[Visualization System] EXPORTING VIDEO: 100.0 %")
        print("[Visualization System] EXPORTING VIDEO DONE")

    elif (is_exporting):
        perc = float(interaction_window_pointer[0] / video_frames_count * 100).__round__(2)
        
        print("[Visualization System] EXPORTING VIDEO: " + str(perc) + " %")
        out_video.write(current_image)
        interaction_window_pointer[0] += 1
        cv2.setTrackbarPos('Frame', app_name, interaction_window_pointer[0])

        # Needed to let user stop the export
        pressed = cv2.waitKeyEx(1)
        if (pressed == 27):
            out_video.release()
            break
        continue

    if (auto_play):
        interaction_window_pointer[0] += 1
        cv2.setTrackbarPos('Frame', app_name, interaction_window_pointer[0])

        # Needed to let user stop the export
        pressed = cv2.waitKeyEx(1)
        if (pressed == 27):
            break
        elif ' ' == chr(pressed & 255):    
            auto_play = not(auto_play)
        continue


    pressed = cv2.waitKeyEx(0)
    if pressed == 2424832:
        # Left arrow Key
        interaction_window_pointer[0] -= 1
        cv2.setTrackbarPos('Frame', app_name, interaction_window_pointer[0])
    if pressed == 2555904:
        # Right arrow Key
        interaction_window_pointer[0] += 1
        cv2.setTrackbarPos('Frame', app_name, interaction_window_pointer[0])
    elif pressed == 27:
        if (is_exporting):
            out_video.release()
        # Esc key
        break
    elif 'w' == chr(pressed & 255):
        
        if (is_exporting == False):
            interaction_window_pointer[0] = 0

            height, width, layers = current_image.shape
            size = (width,height)
       
            out_video = cv2.VideoWriter('export.mp4', cv2.VideoWriter_fourcc(*'MP42'), 25, size)

            is_exporting = True
    
    elif ' ' == chr(pressed & 255):    
        auto_play = not(auto_play)
