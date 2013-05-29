#!/usr/bin/env python
import ROOT
import sys

class Analyzer():
    def __init__(self,dirName,ivDirName):
        ROOT.gROOT.SetBatch(True)
        gMinuit = ROOT.TMinuit()
        ROOT.gSystem.Load("libpsi46ana.so")
        self.dirName = dirName
        self.ivDirName = ivDirName
        self.type = "m" #'a' or 'b' for half modules
        
    def fitAllPh(self, fitMode = 0):
        phFit = ROOT.PHCalibrationFit(fitMode)
        phFit.FitAllCurves(self.dirName)

    def fitPH(self, chip, col, row, fitMode = 0):
        phFit = ROOT.PHCalibrationFit(fitMode)
        phFit.FitAllCurves(self.dirName, chip, col, row)

    def fitAllSCurve(self):
        sCurve = ROOT.SCurve()
        sCurve.FitSCurves(self.dirName)

    def fitSCurve(self, roc, col, row):
        sCurve = ROOT.SCurve()
        sCurve.FitSCurve(self.dirName, roc, col, row)

    def tmpProfile(self):
        ROOT.gROOT.LoadMacro("tempProfile.C")
        ROOT.readProfile(self.dirName,1) #? (0 = short test, 1 = full test or so)

    def chipSummary(self):
        ROOT.gROOT.LoadMacro("chipSummaryPage.C")
        #chipSummaryPageShort.C
        ROOT.chipSummaries(self.dirName,self.type)

    def moduleSummary(self):
        ROOT.gROOT.LoadMacro("moduleSummaryPage.C")
        #moduleSummaryPageShort.C
        ROOT.moduleSummary(self.dirName,self.type,self.ivDirName)

    def analyzeModule(self):
        #self.fitAllPh()
        #self.fitAllSCurve()
        #self.chipSummary()
        self.moduleSummary()

if __name__ == '__main__':
    dirName = sys.argv[1]
    ivDirName = sys.argv[2]
    analyzer = Analyzer(dirName,ivDirName)
    analyzer.analyzeModule()
