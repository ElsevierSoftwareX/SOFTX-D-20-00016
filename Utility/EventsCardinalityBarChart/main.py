# Import packages
import os
from utils.xml.parser import dictionaryBuilder
from utils.charts.barchart.draw import plot

# GLOBAL VARIABLES
# Edit here to make changes
input_folder = "input"
output_folder = "output"
output_file = "events_cardinality.txt"


def load(input_folder):

    # Initialize phase
    print("[LOAD] Loading data events.")

    # Check the existence of the input folder
    if os.path.isdir(input_folder) is False:
        print("[LOAD] Error - The input folder does not exists.")
        return None

    # Get the XML file
    entries = os.listdir(input_folder)
    file = ''
    for entry in entries:
        if entry.lower().endswith(".xml"):
            file = os.path.join(input_folder, entry)
            break
    if file is not "":
        print("[LOAD] Now processing: {}".format(file))
    
    # Build the dictionary upon the XML file
    dictionary = dictionaryBuilder(file)
    if dictionary is not None:
        print("[LOAD] Data events loaded.")

    # Return
    return dictionary


def count(dictionary):
    events_cardinality = {}

    for frame, event in dictionary.items():
        event_name = event["name"]
        event_count = events_cardinality.get(event_name, None)
        if event_count is None:
            events_cardinality[event_name] = 1
        else:
            events_cardinality[event_name] += 1
    
    return events_cardinality


def store(output_folder, output_file, events_cardinality):

    # Initialize phase
    print("[STORE] Storing data events.")

    # Check the existence of the output folder
    if os.path.isdir(output_folder) is False:
        print("[STORE] Error - The output folder does not exists.")
        return None

    # Write file
    output_path = os.path.join(output_folder, output_file)
    with open(output_path, 'w') as file:
        for event, cardinality in events_cardinality.items():    
            file.write("{},{}\r\n".format(event, cardinality))
        print("[STORE] Events data stored.")
    
    return True


def main():

    # Load data from XML files
    dict = load(input_folder)
    if dict is None:
        return
    
    # Count the number of events
    events_cardinality = count(dict)
    if events_cardinality is None:
        return

    # Store data to TXT file
    res = store(output_folder, output_file, events_cardinality)
    if res is None:
        return

    # Build a graph of events
    plot(events_cardinality)



# Main entry point
main()
