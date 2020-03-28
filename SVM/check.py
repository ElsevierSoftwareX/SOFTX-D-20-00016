# Questo file controlla se il file di features presenta dei buchi nei frame
# e ne restituisce la lista, così da poter eventualmente correggere

import pandas
import os

def check_data(path):
    inputFile = os.path.join(path, 'features.log')

    print("\n[INFO] Generating results for {}.".format(path))

    names = ['timestamp', 'playerID','xPosition0','yPosition0', 'direction0', 'velocity0', 'acceleration0', 
                'accPeak0', 'accPeakReal0','dirChange0','distToBall','distToTarget', 'distToGoal', 'crossOnTargLine']


    parsedData = pandas.read_csv(inputFile, sep=' ', engine='c', memory_map=True, names=names)

    totalBallData = parsedData[parsedData.playerID.isin([128])].reset_index()

    # Unisco le informazioni su tutta la finestra in ogni riga (WINDOW_SIZE elementi precedenti)
    window_data = totalBallData.rolling(2)
    
    # Cacolo max-min per le feature su tutta la finestra
    max_data  = window_data.max()
    min_data  = window_data.min()
    result = max_data.subtract(min_data).round(4)
    
    # Elimino tutte le row che hanno indice non multiplo di 30
    result.drop(result[result.timestamp == 1].index , inplace=True)
    
    print(result)


def main():
    datasetPath = 'dataset/testing/'
    for _, dirs, _ in os.walk(datasetPath):
        for directory in dirs:
            check_data(os.path.join(datasetPath, directory))

if __name__ == "__main__":
    main()
