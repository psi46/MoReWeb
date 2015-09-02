import ROOT
import re

verbose = False
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
        if histoname.index(i) == len(histoname) - 1:
            break
        dir = dir.Get(i)
        if dir==None:
            break
    if dir == None:
        return None
    histo = dir.Get(histoname[-1])
    if not histo and '*' in histoname[-1]:
        try:
            regex = histoname[-1].replace('*','.*?')
            for Key in dir.GetListOfKeys():
                if re.match(regex, Key.GetName()):
                    histo = dir.Get(Key.GetName())
                    break
        except:
            pass

    if not histo:
        if verbose and 'Xray.' not in name:
            dir.GetListOfKeys().Print()
            raw_input('Cannot find key: %s'%histoname)
    if name.startswith('Xray.q_') or not histo:
        l = []
        if verbose: print 'FIND: ',name,histoname
        l = []
        key = histoname[-1].split('_')[0]+'_'
        if verbose: print 'KEY: ',key
        for i in dir.GetListOfKeys():
            if i.GetName().startswith(key):
                l.append(i)
        if verbose: print l
        if rocNo != None:
            # rocNo = 0
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
            try:
                raise NameError("Didn't find any possible candidate for the Xray spectrum: {Name} in {Names}".format(Name=name,Names=all_names))
            except NameError:
                print 'The histogram ',histoname , ' was not found'

    return histo
