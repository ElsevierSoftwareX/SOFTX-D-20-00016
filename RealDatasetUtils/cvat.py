import xml.etree.ElementTree as ET
import xml.dom.minidom as DOM

# This script converts the input file from Amhir to raw position.log file of our system 

def main():

    # Set I/O paths
    i = "cam01.xml"                     # Input file from Amhir
    o = "positions_onscreen.log"        

    # Open output file
    with open(o, "w") as f:

        # Parse XML
        tree = ET.parse(i)
        camera = tree.getroot()

        # List of frames, each one containing a list of tracks
        for frame in camera:
            frame_number = frame.attrib["frameNr"]
            for track in frame:
                player_id = track.attrib["trackId"]
                x1 = float(track.find('Xmin').text)
                x2 = float(track.find('Xmax').text)
                y1 = float(track.find('Ymin').text)
                y2 = float(track.find('Ymax').text)
                
                # Computing the 2D position on screen of the player as the center of the BB
                x = (x1+x2)/2
                y = (y1+y2)/2
                line = "{0} {1} {2:.6f} {3:.6f}"
                print(line.format(frame_number, player_id, x, y), file=f)
        
        print("[INFO] Done convertion successfully!")


if __name__ == "__main__":
    main()
