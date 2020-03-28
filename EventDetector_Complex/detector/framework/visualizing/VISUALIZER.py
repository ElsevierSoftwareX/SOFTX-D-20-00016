import numpy as np, time
import matplotlib.pyplot as plt

def visualize(precision_means, recall_means):

    # Start measuring time
    start = time.time()

    ind = np.arange(len(precision_means))  # the x locations for the groups
    width = 0.20  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind - width/2, precision_means, width,
                    color='SkyBlue', label='Precision')
    rects2 = ax.bar(ind + width/2, recall_means, width,
                    color='IndianRed', label='Recall')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Percentage')
    ax.set_title('Precision/Recall for each event')
    ax.set_yticks(np.arange(0, 110, 10))
    ax.set_xticks(ind)
    ax.set_xticklabels(('Pass', 'PassThenGoal', 'FilteringPass', 'FilteringPassThenGoal', 'Cross', 'CrossThenGoal', 'Tackle', 'Shot', 'ShotOut', 'ShotThenGoal', 'SavedShot'))
    ax.legend(bbox_to_anchor=(1, 1))


    def autolabel(rects, xpos='center'):
        """
        Attach a text label above each bar in *rects*, displaying its height.

        *xpos* indicates which side to place the text w.r.t. the center of
        the bar. It can be one of the following {'center', 'right', 'left'}.
        """

        xpos = xpos.lower()  # normalize the case of the parameter
        ha = {'center': 'center', 'right': 'left', 'left': 'right'}
        offset = {'center': 0.1, 'right': 0.4, 'left': 0.6}  # x_txt = x + w*off

        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()*offset[xpos], 1.01*height,
                    '{}'.format(height), ha=ha[xpos], va='bottom')


    autolabel(rects1, "left")
    autolabel(rects2, "right")

    # Stop measuring time
    end = time.time()

    # Print info
    elapsed = round(end - start, 1)
    print("[VISUALIZER]\t Plotted results in: " + str(elapsed) + "s.")
    print("\r")

    plt.show()