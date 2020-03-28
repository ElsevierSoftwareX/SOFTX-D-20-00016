import os
import pandas

def readLabels(path):
    labels = []
    with open(path, 'r') as f:
        for line in f:
            labels.append(int(line.rstrip('\n')))
    return labels

def main():
    datasetPath = 'dataset/training'
    resultMatrixPath = os.path.join(datasetPath, 'ballfeatures.log')
    resultLabelsPath = os.path.join(datasetPath, 'labels.txt')
    totalMatrix = None
    totalLabels = []
    
    for directory in os.listdir(datasetPath):
        if (directory.startswith(".")):
            continue
        
        inputMatrixPath = os.path.join(datasetPath, directory, 'ballfeatures.log')
        inputLabelsPath = os.path.join(datasetPath, directory, 'labels.txt')

        if (os.path.exists(inputMatrixPath) and os.path.exists(inputLabelsPath)):
            print("[INFO] Using {} and {} as input files".format(inputMatrixPath, inputLabelsPath))
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


