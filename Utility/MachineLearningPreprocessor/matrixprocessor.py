
import pandas
import os


def writeBallData(path):
    inputFile = os.path.join(path, 'features.log')
    outputFile = os.path.join(path, 'ballfeatures.log')

    names = ['timestamp', 'playerID','xPosition0','yPosition0', 'direction0', 'velocity0', 'acceleration0', 
                        'accPeak0', 'accPeakReal0','dirChange0','distToBall','distToTarget', 'distToGoal', 'crossOnTargLine']

    parsedData = pandas.read_csv(inputFile, sep=' ', engine='c', memory_map=True, names=names)

    totalBallData = parsedData[parsedData.playerID == 128]
    del totalBallData['playerID']
    del totalBallData['distToBall']
    del totalBallData['distToTarget']
    del totalBallData['distToGoal']
    del totalBallData['crossOnTargLine']

    # Rimuovo gli ultimi 4 frame dalla fine
    ballData = totalBallData[:-4].reset_index() 

    # Aggiungo i dati dei 4 frame successivi al frame corrente (5 dati in ogni frame)
    ballDatas = []
    ballDatas.append(totalBallData[1:-3].reset_index())
    ballDatas.append(totalBallData[2:-2].reset_index())
    ballDatas.append(totalBallData[3:-1].reset_index())
    ballDatas.append(totalBallData[4:].reset_index())

    del totalBallData

    ballData = ballData.assign(xPosition1=ballDatas[0].xPosition0, yPosition1=ballDatas[0].yPosition0, direction1=ballDatas[0].direction0, 
                    velocity1=ballDatas[0].velocity0, acceleration1=ballDatas[0].acceleration0, accPeak1=ballDatas[0].accPeak0,
                    accPeakReal1=ballDatas[0].accPeakReal0)
    ballData = ballData.assign(xPosition2=ballDatas[1].xPosition0, yPosition2=ballDatas[1].yPosition0, direction2=ballDatas[1].direction0, 
                    velocity2=ballDatas[1].velocity0, acceleration2=ballDatas[1].acceleration0, accPeak2=ballDatas[1].accPeak0,
                    accPeakReal2=ballDatas[1].accPeakReal0)
    ballData = ballData.assign(xPosition3=ballDatas[2].xPosition0, yPosition3=ballDatas[2].yPosition0, direction3=ballDatas[2].direction0, 
                    velocity3=ballDatas[2].velocity0, acceleration3=ballDatas[2].acceleration0, accPeak3=ballDatas[2].accPeak0,
                    accPeakReal3=ballDatas[2].accPeakReal0)
    ballData = ballData.assign(xPosition4=ballDatas[3].xPosition0, yPosition4=ballDatas[3].yPosition0, direction4=ballDatas[3].direction0, 
                    velocity4=ballDatas[3].velocity0, acceleration4=ballDatas[3].acceleration0, accPeak4=ballDatas[3].accPeak0,
                    accPeakReal4=ballDatas[3].accPeakReal0)

    del ballData['index']

    ballData.to_csv(outputFile, sep=' ', index=False)

def main():
    datasetPath = 'dataset/training'
    for subdir, dirs, files in os.walk(datasetPath):
        for directory in dirs:
            writeBallData(os.path.join(datasetPath, directory))

if __name__ == "__main__":
    main()
