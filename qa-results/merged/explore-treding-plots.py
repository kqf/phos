#!/usr/bin/python2

# This macro will not work on lxplus, since not all dependencies are satisfied

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

import sys 
DIRECTORY = sys.argv[1]


def draw_data(i, frame):
    if 'time' in i.lower() : return
    data = frame[i].dropna()
    if len(data) < 1 : return
    print frame[i]

    my_dpi = 96
    fig = plt.figure(figsize=(2000, 5));
    alpha = 0 if frame[i].dtype == np.int else 1
    ax = frame[i].plot(style='o', alpha=alpha)
    plt.subplots_adjust(left=0.02, right=0.98, top=0.9, bottom=0.15)
    if frame[i].dtype == np.int:
        for x, y in frame[i].iteritems(): ax.annotate(str(y),xy=(x, y), rotation=90, horizontalalignment='center', verticalalignment='center')

    if 'event' in i.lower(): ax.set_yscale('log')
    plt.xticks(frame.index, frame['run'], rotation='vertical')
    plt.title(i.replace('_', ' '))
    x1, x2, y1, y2 = plt.axis()
    plt.axis((x1, x2* 1.0001, y1, y2 * 1.0001))
    plt.show()
    # fig.tight_layout()
    fig.savefig(i + '.png')



def main():
    frame = pd.read_csv(DIRECTORY + '/goodruns.csv', delimiter=';').sort_values(by='run')
    frame = frame[frame.applymap(np.isreal)]
    for i in frame:
        draw_data(i, frame)

if __name__ == '__main__':
    main()