# This script adds filler data to position.log. So if players or ball are missing, they are added in each frame

# Those values may change depending on the size of the picth
pitchHalfH = 36.0
pitchHalfW = 55.0
pitchFullH = 72.0
pitchFullW = 11.0


# File to read with positions with center the axes in the center of the pitch
input_position_file = "positions_final_partial.log"
# Output file to write in coordinates compliant with our system
output_position_file = "positions.log"

otherTeamPlayerIDs = ['7', '8', '9', '10', '11',
                      '12', '13', '14', '18', '19', '20']


def filler(
    frame_data_team_1,
    frame_data_team_2,
    ball,
    f_o,
    last_frame,
    counter
):

    # Check whether we filled all 23 elements for that frame
    if (len(frame_data_team_1) + len(frame_data_team_2) < 23):
        # We have to fill
        # Adding ids only for players
        element_id = 0
        while (len(frame_data_team_1) < 11):
            if (frame_data_team_1.get(element_id) is None):
                # Adding this element to the dictionary
                new_data = [
                    last_frame,
                    str(element_id),
                    pitchHalfW,
                    pitchHalfH
                ]
                frame_data_team_1[element_id] = new_data
                counter += 1
            element_id += 1

        element_id = 129
        while (len(frame_data_team_2) < 11):
            if (frame_data_team_2.get(element_id) is None):
                # Adding this value into the dictionary
                new_data = [
                    last_frame,
                    str(element_id),
                    pitchHalfW,
                    pitchHalfH
                ]
                frame_data_team_2[element_id] = new_data
                counter += 1
            element_id += 1

        # Now managing the ball
        if (ball is None):
            new_data = [last_frame, str(
                128), pitchHalfW, 0]
            ball = new_data
            counter += 1

    if (len(frame_data_team_1) + len(frame_data_team_2) > 22):
        raise Exception(
            "Too much data for frame {0}".format(last_frame))

    dictionary = dict(frame_data_team_1)
    dictionary.update(frame_data_team_2)
    dictionary[128] = ball

    # Now writing all data for that frame into the output file
    for element_id in sorted(dictionary.keys()):
        print_data = dictionary.get(element_id)

        frame_number = print_data[0]
        player_number = print_data[1]
        x = print_data[2]     # X Position of the player
        y = print_data[3]     # Y Position of the player

        line = "{0} {1} {2:.6f} {3:.6f}"
        print(line.format(
            frame_number, player_number, float(x), float(y)), file=f_o)

    return counter

with open(input_position_file, 'r') as f:
    with open(output_position_file, "w") as f_o:

        # Represents the data of a single frame for all players and ball
        frame_data_team_1 = {}
        frame_data_team_2 = {}
        ball = None
        last_frame = '0'
        counter = 0

        for line in f:
            data = line.split(" ")

            # Check on the right format of the line
            if (len(data) != 4):
                raise Exception("Wrong data format in the line")

            frame = data[0]
            player_id = int(data[1])

            # Check current line is of a new frame or not
            if (last_frame != frame):
                counter = filler(
                    frame_data_team_1, frame_data_team_2,
                    ball, f_o, last_frame, counter
                )

                # Resetting for the next frame iteration
                last_frame = frame
                frame_data_team_1.clear()
                frame_data_team_2.clear()
                ball = None

            # Saving data of the current line into the dictionary
            if (str(player_id - 128) in otherTeamPlayerIDs):
                frame_data_team_2[player_id] = data
            elif (player_id == 128):
                ball = data
            else:
                frame_data_team_1[player_id] = data

        # To export last frame
        counter = filler(
            frame_data_team_1,
            frame_data_team_2,
            ball,
            f_o,
            last_frame,
            counter
        )

        print("[data_filler] Filled with {0} elements.".format(counter))
        print("[data_filler] Done.")
