# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import glob
import array

class ProductionOverview(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def CustomInit(self):
        self.NameSingle='BumpBondingVsId'
    	self.Name='CMSPixel_ProductionOverview_%s'%self.NameSingle
        self.Title = 'Bump Bonding per Module'
        self.DisplayOptions = {
            'Width': 5,
        }
        self.SubPages = []
        self.SavePlotFile = True
        self.Canvas.SetCanvasSize(1330, 430)
        self.Canvas.Update()

    def GenerateOverview(self):
        ROOT.gStyle.SetOptStat(0)

        TableData = []

        Rows = self.FetchData()

        ModuleIDsList = []
        for RowTuple in Rows:
            if not RowTuple['ModuleID'] in ModuleIDsList:
                ModuleIDsList.append(RowTuple['ModuleID'])

        HTML = ""

        ModuleIndex = array.array('d', [])
        ModulePixelDefects = array.array('d', [])

        NModules = 0
        for ModuleID in ModuleIDsList:

            for RowTuple in Rows:
                if RowTuple['ModuleID'] == ModuleID:
                    TestType = RowTuple['TestType']
                    if TestType == 'XRayHRQualification':
                        NumberOfPixelDefects = []
                        for Chip in range(0,16):
                            NumberOfPixelDefectsROC = int(self.GetJSONValue([RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip%d'%Chip, 'BumpBondingDefects_150', 'KeyValueDictPairs.json', 'NumberOfDefectivePixels', 'Value']))
                            NumberOfPixelDefects.append(NumberOfPixelDefectsROC)
                        ModulePixelDefects.append(sum(NumberOfPixelDefects))
                        ModuleIndex.append(NModules)
                        NModules += 1

        if NModules > 0:
            ROOTObject = ROOT.TGraph(NModules, ModuleIndex, ModulePixelDefects)
            ROOTObject.SetLineColor(ROOT.kBlue + 2)
            ROOTObject.Draw("APL")

            title = ROOT.TText()
            title.SetNDC()
            title.SetTextAlign(12)
            title.SetTextColor(ROOT.kBlue + 2)
            Subtitle = "total number of BB defects, modules: %s to %s (%d)"%(ModuleIDsList[0], ModuleIDsList[-1], NModules)
            title.DrawText(0.15, 0.965, Subtitle)

        self.SaveCanvas()
        HTML = self.Image(self.Attributes['ImageFile']) + self.BoxFooter("Number of modules: %d"%NModules)

        AbstractClasses.GeneralProductionOverview.GeneralProductionOverview.GenerateOverview(self)
        return self.Boxed(HTML)

