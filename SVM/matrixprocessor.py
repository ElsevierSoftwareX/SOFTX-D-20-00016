import pandas
import os

# selezionare i dati, fare la media in modo da avere 1 elemento ogni 30 frame e traslare di 30/2 frame
# Successivamente effettuare una normalizzazione.

WINDOW_SIZE = 30
STRIDE = 1

DEBUG = False


# Normalizza il dataframe tra 0 ed 1 anche per i valori negativi
def normalize(df):
    result = df.copy()
    for feature_name in df.columns:
        try:
            max_value = df[feature_name].max()
            min_value = df[feature_name].min()
            result[feature_name] = (df[feature_name] - min_value) / (max_value - min_value)
        except:
            raise Exception("Errore nella divisione?")
    return result


def writeBallData(path):
    inputFile = os.path.join(path, 'features.log')
    outputFile = os.path.join(path, 'ballfeatures.log')
    outputDeletedSamplesFile = os.path.join(path, 'deletedSamples.log')

    names = ['timestamp', 'playerID','xPosition0','yPosition0', 'direction0', 'velocity0', 'acceleration0', 
                'accPeak0', 'accPeakReal0','dirChange0','distToBall','distToTarget', 'distToGoal', 'crossOnTargLine']

    means_names = ['xPosition_ball_mean', 'yPosition_ball_mean', 'direction_ball_mean', 'velocity_ball_mean', 'acceleration_ball_mean', 'accPeak_ball_mean', 'accPeakReal_ball_mean', 'dirChange_ball_mean',
                'xPosition_gk1_mean', 'yPosition_gk1_mean', 'direction_gk1_mean', 'velocity_gk1_mean', 'acceleration_gk1_mean', 'accPeak_gk1_mean', 'accPeakReal_gk1_mean', 'dirChange_gk1_mean',
                'xPosition_gk2_mean', 'yPosition_gk2_mean', 'direction_gk2_mean', 'velocity_gk2_mean', 'acceleration_gk2_mean', 'accPeak_gk2_mean', 'accPeakReal_gk2_mean', 'dirChange_gk2_mean']

    std_names = ['xPosition_ball_std', 'yPosition_ball_std', 'direction_ball_std', 'velocity_ball_std', 'acceleration_ball_std', 'accPeak_ball_std', 'accPeakReal_ball_std', 'dirChange_ball_std',
                'xPosition_gk1_std', 'yPosition_gk1_std', 'direction_gk1_std', 'velocity_gk1_std', 'acceleration_gk1_std', 'accPeak_gk1_std', 'accPeakReal_gk1_std', 'dirChange_gk1_std',
                'xPosition_gk2_std', 'yPosition_gk2_std', 'direction_gk2_std', 'velocity_gk2_std', 'acceleration_gk2_std', 'accPeak_gk2_std', 'accPeakReal_gk2_std', 'dirChange_gk2_std']

    range_names = ['xPosition_ball_range', 'yPosition_ball_range', 'direction_ball_range', 'velocity_ball_range', 'acceleration_ball_range', 'accPeak_ball_range', 'accPeakReal_ball_range', 'dirChange_ball_range',
                'xPosition_gk1_range', 'yPosition_gk1_range', 'direction_gk1_range', 'velocity_gk1_range', 'acceleration_gk1_range', 'accPeak_gk1_range', 'accPeakReal_gk1_range', 'dirChange_gk1_range',
                'xPosition_gk2_range', 'yPosition_gk2_range', 'direction_gk2_range', 'velocity_gk2_range', 'acceleration_gk2_range', 'accPeak_gk2_range', 'accPeakReal_gk2_range', 'dirChange_gk2_range']


    parsedData = pandas.read_csv(inputFile, sep=' ', engine='c', memory_map=True, names=names)

    # Filter data
    columns_of_interest = [128]
    totalBallData = parsedData[parsedData.playerID.isin(columns_of_interest)].reset_index()

    del totalBallData['timestamp']
    del totalBallData['playerID']
    del totalBallData['distToBall']
    del totalBallData['distToTarget']
    del totalBallData['distToGoal']
    del totalBallData['crossOnTargLine']
    del totalBallData['index']

    goalkeeper1_data = parsedData[parsedData.playerID.isin([0])].reset_index()

    del goalkeeper1_data['timestamp']
    del goalkeeper1_data['playerID']
    del goalkeeper1_data['distToBall']
    del goalkeeper1_data['distToTarget']
    del goalkeeper1_data['distToGoal']
    del goalkeeper1_data['crossOnTargLine']
    del goalkeeper1_data['index']
    
    goalkeeper2_data = parsedData[parsedData.playerID.isin([146])].reset_index()

    del goalkeeper2_data['timestamp']
    del goalkeeper2_data['playerID']
    del goalkeeper2_data['distToBall']
    del goalkeeper2_data['distToTarget']
    del goalkeeper2_data['distToGoal']
    del goalkeeper2_data['crossOnTargLine']
    del goalkeeper2_data['index']
    
    
    merged_inner = pandas.merge(left=totalBallData, right=goalkeeper1_data, left_index=True, right_index=True)
    whole_data = pandas.merge(left=merged_inner, right=goalkeeper2_data, left_index=True, right_index=True)

    # Unisco le informazioni su tutta la finestra in ogni riga (WINDOW_SIZE elementi precedenti)
    window_data = whole_data.rolling(WINDOW_SIZE)

    # (-30 0) (-29 1) ...... (0 - 30)

    # Cacolo la media per le 8 feature su tutta la finestra
    means_data = window_data.mean().round(4)
    means_data.columns = means_names
    
    # Cacolo la std per le 8 feature su tutta la finestra
    std_data = window_data.std().round(4)
    std_data.columns = std_names
    
    # Cacolo max-min per le 8 feature su tutta la finestra
    max_data  = window_data.max()
    min_data  = window_data.min()
    range_data = max_data.subtract(min_data).round(4)
    range_data.columns = range_names
    
    # Unisco i risultati sugli 8 valori per media, std, max-min in una sola riga
    result = pandas.concat([means_data, std_data, range_data], axis=1, sort=False).reset_index()
    
    # Elimino tutte le row che hanno indice non multiplo di 30
    result.drop(result[result.index % STRIDE != 0].index , inplace=True)
    
    # Elimino tutti i sample che non sono a un raggio da uno dei due portieri di almeno 10 metri.
    near_gk_1 = ((result['xPosition_ball_mean'] - result['xPosition_gk1_mean'])**2 + (result['yPosition_ball_mean'] - result['yPosition_gk1_mean'])**2) < 6**2
    near_gk_2 = ((result['xPosition_ball_mean'] - result['xPosition_gk2_mean'])**2 + (result['yPosition_ball_mean'] - result['yPosition_gk2_mean'])**2) < 6**2
    ball_stopped = result['velocity_ball_mean'] == 0.0

    # Condizione per cui la palla è vicina o a gk1 o a gk2
    #near_to_gk_1_or_2 = near_gk_1 | near_gk_2
    # Condizione per cui la palla è lontana sia da gk1 che gk2
    #far_from_gk1_and_2 = ~near_to_gk_1_or_2
    
    # Condizione per cui la palla è vicina o a gk1 o a gk2
    near_to_gk_1_or_2 = (near_gk_1 | near_gk_2) & ~ball_stopped
    # Condizione per cui la palla è lontana sia da gk1 che gk2
    far_from_gk1_and_2 = (~near_gk_1 & ~near_gk_2) | ball_stopped
    
    # Seleziono gli indici da eliminare così posso eliminare anche i label corrispondenti
    index_to_delete = result[far_from_gk1_and_2]
    index_to_delete = index_to_delete[["index"]]
    # Seleziono solo gli elementi che sono vicini
    result = result[near_to_gk_1_or_2]

    # Sample in cui la palla è vicina al gk1
    sample_near_gk1 = result[near_gk_1]
    # Sample in cui la palla è vicina al gk2
    sample_near_gk2 = result[near_gk_2]
    
    # Elimnare da result le features (quindi le colonne) di GK2 perchè inutili usando gli index di sample_near_gk1
    # Elimnare da result le features (quindi le colonne) di GK1 perchè inutili usando gli index di sample_near_gk2

    gk1_features = ['xPosition_gk1_mean', 'yPosition_gk1_mean', 'direction_gk1_mean', 'velocity_gk1_mean', 'acceleration_gk1_mean', 'accPeak_gk1_mean', 'accPeakReal_gk1_mean', 'dirChange_gk1_mean',
                'xPosition_gk1_std', 'yPosition_gk1_std', 'direction_gk1_std', 'velocity_gk1_std', 'acceleration_gk1_std', 'accPeak_gk1_std', 'accPeakReal_gk1_std', 'dirChange_gk1_std',
                'xPosition_gk1_range', 'yPosition_gk1_range', 'direction_gk1_range', 'velocity_gk1_range', 'acceleration_gk1_range', 'accPeak_gk1_range', 'accPeakReal_gk1_range', 'dirChange_gk1_range']

    gk2_features = ['xPosition_gk2_mean', 'yPosition_gk2_mean', 'direction_gk2_mean', 'velocity_gk2_mean', 'acceleration_gk2_mean', 'accPeak_gk2_mean', 'accPeakReal_gk2_mean', 'dirChange_gk2_mean',
                'xPosition_gk2_std', 'yPosition_gk2_std', 'direction_gk2_std', 'velocity_gk2_std', 'acceleration_gk2_std', 'accPeak_gk2_std', 'accPeakReal_gk2_std', 'dirChange_gk2_std',
                'xPosition_gk2_range', 'yPosition_gk2_range', 'direction_gk2_range', 'velocity_gk2_range', 'acceleration_gk2_range', 'accPeak_gk2_range', 'accPeakReal_gk2_range', 'dirChange_gk2_range']

    # feature che rimangono dopo la selezione delle feature del solo portiere vicino e della palla stessa
    all_features = ['xPosition_ball_mean', 'yPosition_ball_mean', 'direction_ball_mean', 'velocity_ball_mean', 'acceleration_ball_mean', 'accPeak_ball_mean', 'accPeakReal_ball_mean', 'dirChange_ball_mean',
                    'xPosition_ball_std', 'yPosition_ball_std', 'direction_ball_std', 'velocity_ball_std', 'acceleration_ball_std', 'accPeak_ball_std', 'accPeakReal_ball_std', 'dirChange_ball_std',
                    'xPosition_ball_range', 'yPosition_ball_range', 'direction_ball_range', 'velocity_ball_range', 'acceleration_ball_range', 'accPeak_ball_range', 'accPeakReal_ball_range', 'dirChange_ball_range']

    # Nomi delle colonne dopo l'eliminazione delle colonne del portiere lontano
    result_features_names = ["index"] + all_features + gk1_features

    # Elimino le colonne che non interessano
    for feature in gk2_features:
        del sample_near_gk1[feature]
    sample_near_gk1.columns = result_features_names
    
    # Elimino le colonne che non interessano
    for feature in gk1_features:
        del sample_near_gk2[feature]
    sample_near_gk2.columns = result_features_names

    # Unione dei sample in cui il portiere 1 è vicino con quelli in cui il portiere 2 è vicino
    result = pandas.merge(left=sample_near_gk1, right=sample_near_gk2, how="outer")

    # Elimino gli elementi che sono NaN (perchè calcolatio prima di avere un numero di elementi pari a WINDOW_SIZE)
    result = result[result.xPosition_ball_mean.notnull()]

    # Normalizzazione dei dati
    result = normalize(result)

    # Rimozione della colonna inutile
    del result['index']

    if DEBUG:
        print(result)

    result.to_csv(outputFile, sep=' ', index=False)
    index_to_delete.to_csv(outputDeletedSamplesFile, sep=' ', index=False)


def main():
    datasetPath = 'dataset/training/'
    for subdir, dirs, files in os.walk(datasetPath):
        for directory in dirs:
            if (not directory.startswith(".")):
                print("\n[INFO] Processing directory {}.".format(directory))
                writeBallData(os.path.join(datasetPath, directory))
            else:
                print("\n[INFO] Skipping directory {}.".format(directory))

if __name__ == "__main__":
    main()
