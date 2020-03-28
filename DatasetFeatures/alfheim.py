import numpy as np
import pandas
import scipy
import time
import visualizer
from scipy.spatial import distance


def load_from(filename):
    """Load the data from the specified filename."""

    # Data format of Alfheim Dataset
    columns = ['timestamp','tag_id','x_pos','y_pos','heading','direction','energy','speed','total_distance']

    # Start time of computation
    start = time.time()

    try:
        # Reading data in csv format
        print('[INFO] Loading data from csv file...')
        data = pandas.read_csv(filename, header=None, names=columns)
        return data
    except Exception as e:
        # Printing exception
        print('[ERROR] Exception occurred while reading data\n{}\n\n'.format(e))        

    finally:
        end = time.time()
        print('[INFO] Done loading csv data in {} seconds\n'.format(round(end-start, 1)))        
    

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

    start = time.time()

    ### COMPUTING THE DISTANCE RUN BY EACH PLAYER
    # Retrieving the distance for each Player 
    distanceData = data.groupby(['tag_id'])['total_distance']
    # Computing the max and the min value for each player as those are cumulative values
    # (values in this datasets does not start from 0 as probably they have already moved while the game was not started yet)
    distanceDataMinMax = distanceData.agg(['max','min'])
    # Computing the difference between the start distance (min) and the last value (max) for each player (each group)
    distanceDataMinMax['diff'] = distanceDataMinMax['max'] - distanceDataMinMax['min']

    # Computing the total distance run, and computing the mean (not using mean() because there are substitution in the game)
    totalDistance = distanceDataMinMax['diff'].sum()
    meanDistance = totalDistance / 11



    ### COMPUTING THE SPEED OF EACH PLAYER
    # Computing the mean and std of the speed for each player (not used now)
    speedData = data[['tag_id', 'speed']].groupby(['tag_id']).agg({'speed': ['mean', 'std']})

    # Computing the global mean and std of the speed
    meanSpeed = data['speed'].mean()
    stdSpeed = data['speed'].std()

    # Taking the players that have not moved during that part of the game
    notMovingPlayersIdList = distanceDataMinMax[distanceDataMinMax['diff'] == 0].reset_index()['tag_id'].to_list()

    # Computing the global mean and std of the speed eliminating players that are not effective in the calculation
    speedDepuredData = data[~data.tag_id.isin(notMovingPlayersIdList)]
    meanSpeedDepured = speedDepuredData['speed'].mean()
    stdSpeedDepured = speedDepuredData['speed'].std()

    # Computing the global mean and std of the low speed with clean data
    lowSpeedDepuredData = speedDepuredData[speedDepuredData['speed'] <= meanSpeedDepured]
    meanLowSpeedDepured = lowSpeedDepuredData['speed'].mean()
    stdLowSpeedDepured = lowSpeedDepuredData['speed'].std()

    # Computing the global mean and std of the high speed with clean data
    highSpeedDepuredData = speedDepuredData[speedDepuredData['speed'] > meanSpeedDepured]
    meanHighSpeedDepured = highSpeedDepuredData['speed'].mean()
    stdHighSpeedDepured = highSpeedDepuredData['speed'].std()

    # Output of the results up to now
    print('[FEATURES] Mean distance traveled by players: {} Km'.format(round(meanDistance / 1000, 1)))
    print('[FEATURES] Mean speed of the players: {} m/s'.format(round(meanSpeed, 1)))
    print('[FEATURES] Std speed of the players: {} m/s'.format(round(stdSpeed, 1)))
    print('[INFO] List of not moving players:', notMovingPlayersIdList)
    print('[INFO] Removing players that do not move during the match...')
    print('[FEATURES] Cleaned mean speed of the players: {} m/s'.format(round(meanSpeedDepured, 1)))
    print('[FEATURES] Cleaned std speed of the players: {} m/s'.format(round(stdSpeedDepured, 1)))
    print('[FEATURES] Cleaned mean low speed of the players: {} m/s'.format(np.round(meanLowSpeedDepured, 1)))
    print('[FEATURES] Cleaned std low speed of the players: {} m/s'.format(np.round(stdLowSpeedDepured, 1)))
    print('[FEATURES] Cleaned mean high speed of the players: {} m/s'.format(round(meanHighSpeedDepured, 1)))
    print('[FEATURES] Cleaned std high speed of the players: {} m/s\n'.format(round(stdHighSpeedDepured, 1)))

    
    
    # Grouping positional data by player, selecting only useful data
    positionsGroupedByPlayer = data[['tag_id', 'x_pos', 'y_pos', 'speed']].groupby(['tag_id'])

    players_num = 11
    players_avg_distance_traveled = 0 
    players_avg_distance_traveled_low_intensity = 0
    players_avg_distance_traveled_high_intensity = 0
    

    try:
        # Iterating for each group (each player)
        for name, group in positionsGroupedByPlayer:
            
            # CORE ALGORITHM
            distance_traveled = 0
            low_intesity_distance_traveled = 0
            high_intesity_distance_traveled = 0
            previous_coords = None
            coords = None
            v = 0
            
            # Iterate over the rows of the player data
            first = True
            for i, row in group.iterrows():

                # Ignore first row
                if first:
                    previous_coords = [row['x_pos'], row['y_pos']]
                    v = row['speed']
                    first = False
                    continue

                # Compute distance between current position and the previous one
                else:
                    coords = [row['x_pos'], row['y_pos']]
                    dist = distance.euclidean(previous_coords, coords)

                    # Check the velocity and discriminate between
                    # - low-intensity path traveled
                    # - high-intensity path traveled
                    if v > 0 and v < meanSpeedDepured:
                        low_intesity_distance_traveled += dist
                    elif v > meanSpeedDepured:
                        high_intesity_distance_traveled += dist

                    # Update previous coords
                    previous_coords = coords
                    v = row['speed']
            
            # Convert m to Km
            low_intesity_distance_traveled = round(low_intesity_distance_traveled / 1000, 3)
            high_intesity_distance_traveled = round(high_intesity_distance_traveled / 1000, 3)

            # Update values
            players_avg_distance_traveled_low_intensity += low_intesity_distance_traveled
            players_avg_distance_traveled_high_intensity += high_intesity_distance_traveled
            distance_traveled = round(low_intesity_distance_traveled + high_intesity_distance_traveled, 3)
            players_avg_distance_traveled += distance_traveled

            # Print info for each player
            print("[FEATURES] PlayerId: {}, distance traveled: {} Km.".format(name, distance_traveled))
            print("[FEATURES] PlayerId: {}, distance traveled with low-intensity: {} Km.".format(name, low_intesity_distance_traveled))
            print("[FEATURES] PlayerId: {}, distance traveled with low-intensity: {} Km.".format(name, high_intesity_distance_traveled))


        # Print global info
        print("\n[FEATURES] Global features:")
        players_avg_distance_traveled = round(players_avg_distance_traveled / players_num, 3)
        players_avg_distance_traveled_low_intensity = round(players_avg_distance_traveled_low_intensity / players_num, 3)
        players_avg_distance_traveled_high_intensity = round(players_avg_distance_traveled_high_intensity / players_num, 3)        

        print('[FEATURES] The mean velocity of the players is: {} m/s.'.format(round(meanSpeedDepured, 1)))
        print('[FEATURES] The mean distance traveled by the players is: {} Km.'.format(players_avg_distance_traveled))
        print('[FEATURES] The mean distance traveled with low-intensity by the players is: {} Km.'.format(players_avg_distance_traveled_low_intensity))
        print('[FEATURES] The mean distance traveled with high-intensity by the players is: {} Km.'.format(players_avg_distance_traveled_high_intensity))
        print('\n')
        print('[INFO] Legend:')
        print('[INFO] Low-intensity: player runs under {} m/s.'.format(round(meanSpeedDepured, 3)))
        print('[INFO] High-intensity: player runs over {} m/s.'.format(round(meanSpeedDepured, 3)))

        
    except Exception as e:

        # Print exception info
        print("Exception occurred:\n\n{}\n".format(e))
    
    finally:

        # Stop measuring time
        end = time.time()
        elapsed = round(end-start, 1)

        # Print performance info
        print("[INFO] Features computation ended, in: {} s.".format(elapsed))

        distance_values = [players_avg_distance_traveled, low_intesity_distance_traveled, high_intesity_distance_traveled]
        return [round(meanSpeedDepured, 1), distance_values]



def main():
    """Main function."""

    # Print program info
    print('AlfheimDataset features program.')

    # Specify the list of files to read
    files = ['2013-11-03_tromso_stromsgodset_first_ONLY_ONE_MINUTE.csv']#'2013-11-03_tromso_stromsgodset_first.csv']#, '2013-11-03_tromso_stromsgodset_second.csv']

    # Initializing list of frames
    frames = []

    # Reading data from files
    for file in files:
        data = load_from(file)
        frames.append(data)

    # Merging data from all files
    data = pandas.concat(frames)
    if data is None:
        return None
    
    # Extract features
    [alfheim_mean_speed, alfheim_mean_distances] = extract_features_from(data)

    # Features retrieved from game estraction
    # [FEATURES] The mean velocity of the players is: 3.8 m/s.
    # [FEATURES] The mean distance traveled by the players is: 8.4 Km.
    # [FEATURES] The mean distance traveled with low-intensity by the players is: 2.8 Km.
    # [FEATURES] The mean distance traveled with high-intensity by the players is: 5.6 Km.    
    
    # Mean speed (m/s),
    #game_mean_speed = [3.8]
    
    # Mean distance (m/s), mean distance at low speed (m/s), mean distance at low speed (m/s)
    #game_mean_distances = [8.4, 2.8, 5.6]

    
    # FOR ONLY ONE MINUTE OF GAME
    # Mean speed (m/s),
    game_mean_speed = [3.7]
    
    # Mean distance (m/s), mean distance at low speed (m/s), mean distance at low speed (m/s)
    game_mean_distances = [0.211, 0.064, 0.147]

    y_max = 7
    labels = ('Speed (m/s)', '')
    visualizer.visualize(game_mean_speed, alfheim_mean_speed, labels, y_max)

    y_max = 1
    labels = ('Distance (Km)', 'Low speed distance (Km)', 'High speed distance (Km)')
    visualizer.visualize(game_mean_distances, alfheim_mean_distances, labels, y_max)    


if __name__ == '__main__':
    main()