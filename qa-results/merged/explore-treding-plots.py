#!/usr/bin/python

# This macro will not work on lxplus, since not all dependencies are satisfied
import ROOT
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

import sys 
DIRECTORY = sys.argv[1]

def convert_rdata(dser, dlist):
    if len(dser) < 1 : return []
    if dlist and len(dser) != len(dlist): return []
    print max(dser), max(dlist)
    coef = max(dser) * 1. / max(dlist)
    res = np.array(dlist) * coef
    return  res



def draw_data(i, frame, rdata, rtitle):
    if 'time' in i.lower() : return
    data = frame[i].dropna()
    rdata = convert_rdata(data, rdata)

    if not len(rdata) > 1: return

    fig = plt.figure(figsize=(2500, 5));
    alpha = 0 if frame[i].dtype == np.int else 1
    ax = frame[i].plot(style='o', alpha=alpha, label = i)
    plt.subplots_adjust(left=0.02, right=0.98, top=0.9, bottom=0.15)
    axbar = plt.bar(data.index, rdata, color='g', alpha=0.5, align='center', label = rtitle)
    plt.legend((axbar, ), (rtitle, ))

    if frame[i].dtype == np.int:
        for x, y in frame[i].iteritems(): ax.annotate(str(y),xy=(x, y), rotation=90, horizontalalignment='center', verticalalignment='center')

    if 'event' in i.lower(): ax.set_yscale('log')
    plt.xticks(frame.index, frame['run'], rotation='vertical')
    plt.title(i.replace('_', ' '))
    x1, x2, y1, y2 = plt.axis()
    plt.axis((x1, x2* 1.0001, y1, y2 * 1.0001))
    plt.show()
    # fig.tight_layout()
    fig.savefig(i + '.pdf')

def read_averages(mdir):
    infile = ROOT.TFile(mdir + '/images/cluster-averages.root.png')
    # infile.ls()
    mhsit = infile.Get('hAvNCluster_NC1_Emin=0.30GeV_corr4accept')
    mhsit.GetName()
    return [ mhsit.GetBinContent(i) for i in range(1, mhsit.GetNbinsX() + 1) ], mhsit.GetTitle()



def main():
    frame = pd.read_csv(DIRECTORY + '/goodruns.csv', delimiter=';').sort_values(by='run')
    frame = frame[frame.applymap(np.isreal)]
    data, t = read_averages(DIRECTORY)
    for i in frame[0:1]:
        draw_data(i, frame, data, t)

if __name__ == '__main__':
    main()