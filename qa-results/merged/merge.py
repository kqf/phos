#!/usr/bin/env python2


from os import listdir

from ROOT import TFile, TObjArray, SetOwnership, TObject, TH1
import sys 

def get_container(ifile):

    try:
        try: lst = ifile.PHOSCellsQA2
        except: lst = ifile.PHOSCellsQA1
    except:
        lst = ifile.PHOSCellsQA

    return lst

def merge(fnames, oname):
    out = TObjArray()
    out.SetOwner(True)
    TH1.AddDirectory(False)


    for i, l in enumerate(fnames):
        print i
        f = TFile.Open(l)
        SetOwnership(f, 1)
        for h in get_container(f): 
            obj = out.FindObject(h.GetName())
            if not obj: 
                out.Add(h)
                continue
            obj.Add(h)
            h.IsA().Destructor( h )
        f.Close()


    fout2 = TFile(oname + 'Single' + '.root', 'recreate')
    out.Write('PHOSCellsQA', TObject.kSingleKey)
    fout2.cd()
    fout2.Write()
    fout2.Close()

    fout1 = TFile(oname + '.root', 'recreate')
    fout1.cd()
    out.Write()
    fout1.Write()
    fout1.Close()



def main():
    folder = sys.argv[1] + '/'
    fnames = [folder + l for  l in listdir(folder) if 'root' in l]
    print fnames[2912:]

    merge(fnames, folder + "CaloCellsQA")
    raw_input('press any key')

if __name__ == '__main__':
    main()

