
import ROOT

def get_histo(rootfile,histoname,rocNo = None):
    if rocNo !=None:
        histoname = histoname%rocNo

    histoname = histoname.split('.')
    if not type(rootfile) == ROOT.TFile:
        print 'INVALID input: ROOTFILE'
        raise TypeError('Cannot use %s as a ROOT TFile'%type(rootfile))
    dir = rootfile
    for  i in histoname:
        if histoname.index(i)==len(histoname)-1:
            break
        dir = dir.Get(i)
        if dir==None:
            break
    if dir == None:
        return None
    # print dir,type(dir)
    histo = dir.Get(histoname[-1])
    # print histo
    return histo
