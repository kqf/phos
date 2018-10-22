import ROOT


def main():
    infile = ROOT.TFile("corrected-yield-pi^{0}.root", "read")
    directory = infile.Get(
        "corrected-yield-#pi^{0}/corrected-yield/efficiency/output")
    print("Inside the directory:")
    print()
    directory.ls()

    canvas = directory.Get("rationmesons-data-eff-#pi^{0}-copied;1")
    print("Inside the canvas:")
    print()
    canvas.ls()

    # All histograms are stored in the THStack("test", ...)
    stack = canvas.FindObject("test")
    eff = stack.GetHists().FindObject("rationmesons_data_eff_#pi^{0}_copied")
    print(eff)


if __name__ == '__main__':
    main()
