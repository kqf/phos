#!/usr/bin/python

# This macro will not work on lxplus, since not all dependencies are satisfied
import ROOT
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

import sys 
PERIOD = sys.argv[1]
DIRECTORY = sys.argv[2]

def scale_averages(dser, dlist):
    if len(dser) < 1 : return []
    if dlist and len(dser) != len(dlist): return []
    coef = max(dser) * 1. / max(dlist)
    res = np.array(dlist) * coef
    return  res


def draw_averages(indeces, averages, avtitle):
    fig = plt.figure(figsize=(2500, 5));
    plt.subplots_adjust(left=0.02, right=0.98, top=0.9, bottom=0.15)
    axbar = plt.bar(indeces, averages, color='g', alpha=0.5, align='center', label = avtitle)
    plt.bar(indeces, averages, color='g', alpha=0.5, align='center', label = avtitle)
    plt.bar(indeces, np.zeros_like(averages) + averages * (averages > averages.mean()), color='r', alpha=0.5, align='center', label = avtitle)

    # fig.tight_layout()
    return fig, axbar




def draw_data(i, frame, averages, runs, avtitle):
    if 'time' in i.lower() : return
    data = frame[i].dropna()
    averages = scale_averages(data, averages)

    if not len(averages) > 1: return

    # Draw Scaled averages
    fig, axbar = draw_averages(data.index, averages, avtitle)

    # Draw data
    ax = data.plot(style='o', alpha= int(data.dtype != np.int) , label = i)

    # Legend, and labels
    plt.legend((axbar, ), (avtitle, ))
    if data.dtype == np.int:
        for x, y in data.iteritems(): 
            ax.annotate(str(y),xy=(x, y), rotation=90, horizontalalignment='center', verticalalignment='center')


    if 'event' in i.lower(): ax.set_yscale('log')
    if 'duration' in i.lower(): ax.set_yscale('log')

    # Run numbers/ titles
    plt.xticks(frame.index, frame['run'], rotation='vertical')
    plt.title(i.replace('_', ' '))

    # Image sizes
    x1, x2, y1, y2 = plt.axis()
    plt.axis((x1, x2* 1.0001, y1, y2 * 1.0001))

    plt.show()

    fig.savefig(DIRECTORY + '/from-logbook-' + i + '.pdf')

def read_averages(mdir):
    infile = ROOT.TFile(mdir + '/cluster-averages.move.root')
    mhsit = infile.Get('hAvNCluster_NC1_Emin=0.30GeV_corr4accept')
    values = [ mhsit.GetBinContent(i) for i in range(1, mhsit.GetNbinsX() + 1) ]
    runs =  [mhsit.GetXaxis().GetBinLabel(i) for i in range(1, mhsit.GetNbinsX() + 1)]
    return values, map(int, runs), mhsit.GetTitle()


def main():
    frame = pd.read_csv(PERIOD + '/goodruns.csv', delimiter=';').sort_values(by='run')
    frame = frame[frame.applymap(np.isreal)]
    averages, runs, t = read_averages(DIRECTORY)
    frame = frame[frame['run'].isin(runs)]
    frame.sort_values('run')
    frame = frame.reset_index(drop=True) # No gaps
    for i in frame: draw_data(i, frame, averages, runs, t)


if __name__ == '__main__':
    main()