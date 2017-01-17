#!/usr/bin/env python
import ROOT
import glob
import array
import os

# requirements
#
# 1) MySQLdb python module: e.g. install with with the command: 'pip install MySQL-python'
# 2) DB password


# how to run
#
# 1) ./IVcurves_download.py
# 2) ./IVcurves_plot.py

def extract_points(fileName):
    with open(fileName, 'r') as inputFile:
        lines = inputFile.readlines()
    lines = [x.strip() for x in lines if not x.strip().startswith('#')]
    lines = [[y for y in x.replace('\t', ' ').split(' ') if len(y.strip()) > 0][0:2] for x in lines]
    lines = [[-float(y) for y in x] for x in lines]
    return lines

def list_files(mask, temp = '_m20_*'):
    rawList = glob.glob('ivcurves/%s%s.root'%(mask, temp))
    rawList.sort()
    modulesDict = {}
    for r in rawList:
        fileName = '_'.join(r.split('/')[-1].split('_')[0:6])
        if fileName not in modulesDict:
            modulesDict[fileName] = r

    print len(modulesDict), " modules found for ", mask
    return modulesDict


def plot_iv_curves(outputFileName, mask = 'BPix_*', temp = 'm20_*'):
    try:
        os.mkdir('plots')
    except:
        pass

    multiGraph = ROOT.TMultiGraph()
    graphs = []
    fileNames = list_files(mask, temp)
    nModules = 0


    for moduleName, fileName in fileNames.iteritems():


        RootFile = ROOT.TFile.Open(fileName, 'read')

        RootFileCanvas = RootFile.Get("c1")

        ClonedROOTObject = None
        graph = None

        try:
            graph = RootFileCanvas.GetPrimitive("Graph").Clone("graph_" + moduleName)
            graphs.append(graph)
            multiGraph.Add(graph)
            graph.SetLineWidth(1)
            graph.SetLineColorAlpha(ROOT.kBlue,0.3)

            nModules += 1
        except:
            pass

    c2 = ROOT.TCanvas("c2", "c2", 1200, 800)
    c2.SetGrid()

    multiGraph.SetTitle("IV(%s) %s, %d modules"%(temp, mask, nModules))
    multiGraph.Draw("AL")
    ROOT.gPad.Update()
    multiGraph.GetYaxis().SetRangeUser(1e-9,1e-4)
    multiGraph.GetYaxis().SetTitle('current [A]')
    multiGraph.GetXaxis().SetTitle('voltage [V]')
    ROOT.gPad.SetLogy()


    cutG = ROOT.TCutG("cut1", 2)
    cutG.SetPoint(0,200,1e-10)
    cutG.SetPoint(1,200,1)
    cutG.SetLineColor(ROOT.kRed)
    cutG.Draw("same")

    ROOT.gPad.Update()
    for ext in ['root', 'pdf', 'png']:
        c2.SaveAs('plots/' + outputFileName + '.' + ext)



plot_iv_curves('LAYER1_p17', 'BPix_*_LYR1_*', 'p17_*')
plot_iv_curves('LAYER2_p17', 'BPix_*_LYR2_*', 'p17_*')
plot_iv_curves('LAYER3_p17', 'BPix_*_LYR3_*', 'p17_*')
plot_iv_curves('LAYER4_p17', 'BPix_*_LYR4_*', 'p17_*')

plot_iv_curves('LAYER1_m20', 'BPix_*_LYR1_*', 'm20_*')
plot_iv_curves('LAYER2_m20', 'BPix_*_LYR2_*', 'm20_*')
plot_iv_curves('LAYER3_m20', 'BPix_*_LYR3_*', 'm20_*')
plot_iv_curves('LAYER4_m20', 'BPix_*_LYR4_*', 'm20_*')