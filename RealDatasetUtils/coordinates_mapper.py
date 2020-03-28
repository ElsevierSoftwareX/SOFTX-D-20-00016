# This script transforms positional data from dataset coordinate system to ours

# Those values may change depending on the size of the picth
pitchHalfH = 36000.0
pitchHalfW = 55000.0
pitchFullH = 72000.0
pitchFullW = 110000.0


# File to read with positions with center the axes in the center of the pitch 
input_position_file = "positions_onthepitch.log"
# Output file to write in coordinates compliant with our system
output_position_file = "positions_final_partial.log"


with open(input_position_file, 'r') as f:
    with open(output_position_file, "w") as f_o: 
        for line in f:
            data = line.split(" ")

            # Check on the right format of the line
            if (len(data) != 4):
                raise Exception("Wrong data format in the line")

            x = data[2]     # X Position of the player
            y = data[3]     # Y Position of the player

            # Translation to the new center and scaling to metres from centimeters
            x_final = (pitchHalfW - float(x)) / 1000   
            y_final = (float(y) + pitchHalfH) / 1000

            frame_number = data[0]
            player_id = data[1]

            # Writing the result to output file
            line = "{0} {1} {2:.6f} {3:.6f}"
            print(line.format(frame_number, player_id, x_final, y_final), file=f_o)
        
        print ("[Coordinates_mapper] Done.")