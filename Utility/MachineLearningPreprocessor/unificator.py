import os
import pandas

def readLabels(path):
    labels = []
    with open(path, 'r') as f:
        for line in f:
            labels.append(int(line.rstrip('\n')))
    return labels

def main():
    datasetPath = 'E:\GameplayFootball\Prova'
    resultMatrixPath = os.path.join(datasetPath, 'totalMatrix.txt')
    resultLabelsPath = os.path.join(datasetPath, 'totalLabels.txt')
    totalMatrix = None
    totalLabels = []
    for subdir, dirs, files in os.walk(datasetPath):
        for directory in dirs:
            inputMatrixPath = os.path.join(datasetPath, directory, 'ballfeatures.log')
            inputLabelsPath = os.path.join(datasetPath, directory, 'labels.txt')
            newMatrix = pandas.read_csv(inputMatrixPath, sep=' ', engine='c', memory_map=True)
            if (totalMatrix is None):
                totalMatrix = newMatrix
            else:
                totalMatrix = totalMatrix.append(newMatrix, ignore_index=True)
            newLabels = readLabels(inputLabelsPath)
            for i in range(len(newLabels), len(newMatrix)):
                newLabels.append(0)
            totalLabels += newLabels
    
    print('Matrix row number is {}\nLabel number is {}\n'.format(len(totalMatrix),len(totalLabels)))
    
    totalMatrix.to_csv(resultMatrixPath, sep=' ', index=False)
    with open(resultLabelsPath, 'w') as f:
        for label in totalLabels:
            f.write('{}\n'.format(label))

if __name__ == "__main__":
    main()


