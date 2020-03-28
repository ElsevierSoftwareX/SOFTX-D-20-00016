import xml.etree.ElementTree as ET
import xml.dom.minidom as DOM

# This script converts a cvat annotation file of positions into a position.log file with on screen positions

# Support function used to order on frame number
def frame_id(element):
    return int(element["frame_number"])

def main():

    # List of elements to be sorted
    myList = []
    otherTeamPlayerIDs = ['7','8','9','10','11','12','13'] 

    # Set I/O paths
    i = "annotation.xml"
    o = "positions_onscreen.log"

    # Open output file
    with open(o, "w") as f:

        # Parse XML
        tree = ET.parse(i)
        annotation = tree.getroot()

        # List of subelemnts (each one can be a track or meta elem) 
        for subelement in annotation:
            if subelement.tag == "track":
                # Taking attributes of that track
                attr = subelement.attrib
                data = attr.get("label", "")

                player_id = ""

                # If this track is a Player or the Ball I set a different ID
                if (data == "Player"):
                    player_id = attr.get("id", "")
                    if player_id in otherTeamPlayerIDs:
                        player_id = str(int(player_id) + 128)

                elif (data == "Ball"):
                    player_id = "128"
                
                # Scanning the list of boxes of that Track
                for box in subelement:
                    box_attr = box.attrib

                    # Taking details of the box from its attributes
                    frame_number = box_attr.get("frame", "")
                    x1 = float(box_attr.get("xtl", ""))
                    y = float(box_attr.get("ybr", ""))
                    x2 = float(box_attr.get("xbr", ""))
                    
                    # Computing the average of the bottom line (the nearest to the pitch, with z = 0)
                    x = (x1+x2)/2
                    
                    obj = {}
                    obj["frame_number"] = frame_number
                    obj["player_id"] = player_id
                    obj["x"] = x
                    obj["y"] = y
                
                    myList.append(obj)


        # Sort the list
        myList.sort(key = frame_id)

        for e in myList:
            line = "{0} {1} {2:.6f} {3:.6f}"
            print(line.format(e["frame_number"], e["player_id"], e["x"], e["y"]), file=f)
        
        print("[Conversion_to_PositionsLog] Done.")


if __name__ == "__main__":
    main()
