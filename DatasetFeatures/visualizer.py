import numpy as np, time
import matplotlib.pyplot as plt

def visualize(game_values, alfheim_values, labels, y_max):

    # Start measuring time
    start = time.time()

    ind = np.arange(len(game_values))  # the x locations for the groups
    width = 0.20  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind - width/2, game_values, width,
                    color='SkyBlue', label='Game')
    rects2 = ax.bar(ind + width/2, alfheim_values, width,
                    color='IndianRed', label='Alfheim')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Mean values per player')
    ax.set_title('Difference values between datasets')
    ax.set_yticks(np.arange(0, y_max, 1))
    ax.set_xticks(ind)
    ax.set_xticklabels(labels)
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