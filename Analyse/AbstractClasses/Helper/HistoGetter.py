
import ROOT

def get_histo(rootfile,name,rocNo = None):
    histoname = name
    if rocNo !=None:
        try:
            histoname = histoname%rocNo
        except TypeError:
            print 'cannot append RocNo: ',rocNo,' at ', histoname

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
    histo = dir.Get(histoname[-1])
    if name.startswith('Xray.q_'):
        l = []
        for i in dir.GetListOfKeys():
            if i.GetName().startswith('q_'):
                l.append(i)
        if rocNo == None:
            rocNo = 0
        l = filter(lambda x: 'C{ROC}_'.format(ROC=rocNo) in x.GetName(), l)
        if len(l) == 1:
            histo = dir.Get(l[0].GetName())
        elif len(l) > 1:
            histo = None
            raise NameError('Found more than one possible candidate for the Xray spectrum: {Candidates}'.format(Candidates=l))
        else:
            histo = None
            all_names = []
            for i in dir.GetListOfKeys():
                all_names.append(i.GetName())
            raise NameError("Didn't found any possible candidate for the Xray spectrum: {Name} in {Names}".format(Name=name,Names=all_names))
    return histo
