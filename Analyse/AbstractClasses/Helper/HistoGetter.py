
import ROOT

def get_histo(rootfile,histoname,rocNo = None):
    if rocNo !=None:
        histoname = histoname%rocNo
    histoname = histoname.split('.')
    dir = rootfile
    for  i in histoname:
        if histoname.index(i)==len(histoname)-1:
            break
        dir = dir.Get(i)
        if dir==None:
            break
    if dir == None:
        return None
    histo = dir.Get(histoname[-1])
    return histo
