from scipy.spatial import distance
import pandas
import time
import numpy
import math


def load_from(filename):
    """Load the data from the specified filename."""

    # Set the columns
    columns = [
        'timestamp',
        'playerID',
        'xPosition',
        'yPosition',
        'direction',
        'velocity',
        'acceleration',
        'accPeak',
        'accPeakReal',
        'dirChange',
        'distToBall',
        'distToTarget',
        'distToGoal',
        'crossOnTargLine']

    try:

        # Print a new line
        print('\r')

        # Start measuring time
        print("[LOADING DATA] Reading file: {}.".format(filename))
        start = time.time()

        # Parse the data and build a DataFrame
        data = pandas.read_csv(
            filename,
            sep=' ',
            engine='c',
            memory_map=True,
            names=columns)

        # Stop measuring time
        end = time.time()
        elapsed = round(end-start, 2)

        # Return data
        return data

    except Exception as e:

        # Print exception info
        print("Exception occurred:\n\n{}\n".format(e))

    finally:

        # Stop measuring time
        end = time.time()
        elapsed = round(end-start, 2)

        # Print performance info
        print("[LOADING DATA] Load data ended, in: {} s.".format(elapsed))


def euclidean(XY):
    """
    Compute the euclidean distance from x and y 1-d arrays.

    INPUT:
    XY = [
        index=[0, 1, ...],
        xPosition=[x1, x2, ...],
        yPosition=[y1, y2, ...]
    ]
    
    TRANSFORMATION:
    coords = [[x1,y1], [x2,y2], ...]

    COMPUTATION
    distances = [euclidean([x1,y1]), euclidean([x2,y2]), ...]

    RETURN
    distance = distances[1] + distances[2] + ...
    """

    # Initialize result
    total_distance = 0
    coords = []

    # Transforma raw input into coords
    for i, row in XY.iterrows():
        coords.append([row['xPosition'],row['yPosition']])

    # Compute distances
    for i, coord in enumerate(coords):
        if i == 0:
            continue
        total_distance += distance.euclidean(coords[i],coords[i-1])

    return total_distance


def extract_features_from(data):
    """Extract the features from the specified dataFrame."""

    try:

        # Print a new line
        print('\r')

        # Initialize variable(s)
        players_num = 0
        players_avg_distance_traveled = 0 
        players_avg_distance_traveled_low_intensity = 0
        players_avg_distance_traveled_high_intensity = 0

        # Start measuring time
        print("[FEATURES] Computing features.")
        start = time.time()

        # Compute Velocity Mean
        velocities = data.loc[:, 'velocity']
        velocities_mean = round(velocities.mean(), 1)

        # Get the playersIds
        playersIds = data.loc[:, 'playerID'].unique()

        # Iterate over playersIds
        for player_id in numpy.nditer(playersIds):

            # Do not compute features for the ball
            if player_id == 128:
                continue
            else:
                players_num += 1

            # Get the quadiplet (id,x,y,v) values of the players
            playersXY = data.loc[:, ['playerID', 'xPosition', 'yPosition', 'velocity']]
            playerTrackingData = playersXY.loc[playersXY['playerID'] == player_id]
            cleanPlayerTrackingData = playerTrackingData.drop_duplicates()

            # CORE ALGORITHM
            distance_traveled = 0
            low_intesity_distance_traveled = 0
            high_intesity_distance_traveled = 0
            previous_coords = None
            coords = None
            v = 0

            # Iterate over the rows of the player data
            first = True
            for i, row in cleanPlayerTrackingData.iterrows():

                # Ignore first row
                if first:
                    previous_coords = [row['xPosition'], row['yPosition']]
                    v = row['velocity']
                    first = False
                    continue

                # Compute distance between current position and the previous one
                else:
                    coords = [row['xPosition'], row['yPosition']]
                    dist = distance.euclidean(previous_coords, coords)

                    # Check the velocity and discriminate between
                    # - low-intensity path traveled
                    # - high-intensity path traveled
                    if v > 0 and v < velocities_mean:
                        low_intesity_distance_traveled += dist
                    elif v > velocities_mean:
                        high_intesity_distance_traveled += dist

                    # Update previous coords
                    previous_coords = coords
                    v = row['velocity']
            
            # Convert m to Km
            low_intesity_distance_traveled = round(low_intesity_distance_traveled / 1000, 3)
            high_intesity_distance_traveled = round(high_intesity_distance_traveled / 1000, 3)

            # Update values
            players_avg_distance_traveled_low_intensity += low_intesity_distance_traveled
            players_avg_distance_traveled_high_intensity += high_intesity_distance_traveled
            distance_traveled = round(low_intesity_distance_traveled + high_intesity_distance_traveled, 3)
            players_avg_distance_traveled += distance_traveled

            # Print info for each player
            print("[FEATURES] PlayerId: {}, distance traveled: {} Km.".format(player_id, distance_traveled))
            print("[FEATURES] PlayerId: {}, distance traveled with low-intensity: {} Km.".format(player_id, low_intesity_distance_traveled))
            print("[FEATURES] PlayerId: {}, distance traveled with low-intensity: {} Km.".format(player_id, high_intesity_distance_traveled))

        # Print global info
        print("\n[FEATURES] Global features:")
        players_avg_distance_traveled = round(players_avg_distance_traveled / players_num, 3)
        players_avg_distance_traveled_low_intensity = round(players_avg_distance_traveled_low_intensity / players_num, 3)
        players_avg_distance_traveled_high_intensity = round(players_avg_distance_traveled_high_intensity / players_num, 3)
        print("[FEATURES] The mean velocity of the players is: {} m/s.".format(velocities_mean))
        print("[FEATURES] The mean distance traveled by the players is: {} Km.".format(players_avg_distance_traveled))
        print("[FEATURES] The mean distance traveled with low-intensity by the players is: {} Km.".format(players_avg_distance_traveled_low_intensity))
        print("[FEATURES] The mean distance traveled with high-intensity by the players is: {} Km.".format(players_avg_distance_traveled_high_intensity))
        print("\r")
        print("[FEATURES] Legend:")
        print("[FEATURES] Low-intensity: player runs under {} m/s.".format(velocities_mean))
        print("[FEATURES] High-intensity: player runs over {} m/s.".format(velocities_mean))
        print("\r")

        # Stop measuring time
        end = time.time()
        elapsed = round(end-start, 2)

    except Exception as e:

        # Print exception info
        print("Exception occurred:\n\n{}\n".format(e))

    finally:

        # Stop measuring time
        end = time.time()
        elapsed = round(end-start, 2)

        # Print performance info
        print("[FEATURES] Features computation ended, in: {} s.".format(elapsed))


def main():
    """Main function."""

    # Print program info
    print("DatasetFeatures program.")

    # Load the data
    data = load_from("features_Match_2019_02_13_#002_extracted.log")
    if data is None:
        return None

    # Extract features
    extract_features_from(data)


if __name__ == '__main__':
    main()
