import pandas
import numpy
import os
import matplotlib.pyplot as plt

def createParameters(path)
    names = ['permutationCode', 'windowSize1','windowSize2','windowSize3', 'windowSize4', 'innerDistance1', 'innerDistance2', 
            'innerDistance3', 'innerDistance4','deltaDistance1','deltaDistance2','speed1', 'speed2', 'speed3', 'speed4', 'acceleration']
    populationAvg = [[] for name in names]
    populationStd = [[] for name in names]

    for subdir, dirs, files in os.walk(path):
        for f in files:
            if ('ArchiveGen_' in f) and not('png' in f):
                print(f)
                currentFile = os.path.join(path, f)
                parsedData = pandas.read_csv(currentFile, sep=' ', engine='c', memory_map=True, names=names, header=None)
                average = parsedData.mean(axis=0)
                standard = parsedData.std(axis=0)
                for i,element in enumerate(populationAvg):
                    element.append(average[i])
                for i,element in enumerate(populationStd):
                    element.append(standard[i])

    generations = [i for i in range(len(populationAvg[0]))]
    #print(populationAvg[2])
    #print(generations)
    for i,name in enumerate(names):
        averageName = '{}'.format(name)
        borderValueUpper = []
        borderValueLower = []
        for k, element in enumerate(generations):
            borderValueUpper.append(populationAvg[i][k]+populationStd[i][k])
            borderValueLower.append(populationAvg[i][k]-populationStd[i][k])
        plt.clf()
        fig, ax = plt.subplots()
        plt.plot(generations, populationAvg[i], 'b', label='average'.format(name))
        #plt.plot(generations, borderValueUpper, 'b', label='{} average evolution'.format(name), alpha=0.5)
        #plt.plot(generations, borderValueLower, 'b', label='{} average evolution'.format(name), alpha=0.5)
        plt.fill_between(generations, borderValueLower, borderValueUpper, color='b', alpha=0.25, label='standard deviation')
        #ax.set_ylabel('Media e deviazione standard')
        ax.set_xlabel("Generazioni")
        ax.set_title('Evoluzione del parametro {}'.format(name))
        plt.savefig(os.path.join(path,averageName))

def main():
    path = 'E:\git\Results9'
    createParameters(path)

if __name__ == "__main__":
    main()