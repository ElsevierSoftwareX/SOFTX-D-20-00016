import matplotlib.pyplot as plt
import numpy as np


def autolabel(rects, xpos='center'):

   for e in rects:
        i = rects.index(e)
        plt.text(i, 1.01*e, e, ha='center', va='bottom')


def plot(events_cardinality):

    columns_number = len(events_cardinality)
    
    max = 0
    columns_names = []
    columns_values = []
    for e, c in events_cardinality.items():
        if c > max:
                max = c
        columns_values.append(c)
        columns_names.append(e)

    width = 0.35
    ind = np.arange(columns_number)
    plot = plt.bar(ind, columns_values, width, color='silver')

    plt.title('Events Cardinality')
    plt.ylabel('Number')
    plt.xticks(ind, tuple(columns_names))
    plt.yticks(np.arange(0, max + 1, 1000))
    autolabel(columns_values)
    plt.show()
