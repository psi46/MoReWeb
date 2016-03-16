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
            'Width': 5.4,
        }
        if self.Attributes.has_key('Width'):
            self.DisplayOptions['Width'] = self.Attributes['Width']
        self.SubPages = []
        self.SavePlotFile = True
        self.Canvas.SetCanvasSize(1600, 400)
        self.Canvas.Update()

    def GenerateOverview(self):
        ROOT.gStyle.SetOptStat(0)

        TableData = []

        Rows = self.FetchData()
        ModuleIDsList = self.GetModuleIDsList(Rows)

        HTML = ""

        ModuleIndex = array.array('d', [])
        ModulePixelDefects = array.array('d', [])

        NModules = len(ModuleIDsList)
        HistogramXray = ROOT.TH1D(self.GetUniqueID(), "", NModules, 0, NModules)
        HistogramXray.GetXaxis().SetNdivisions(-NModules)
        HistogramColdbox = ROOT.TH1D(self.GetUniqueID(), "", NModules, 0, NModules)
        HistogramColdbox.GetXaxis().SetNdivisions(-NModules)

        ROOT.gPad.SetLeftMargin(0.04)
        ROOT.gPad.SetRightMargin(0.03)

        if HistogramXray and HistogramColdbox:
            binX = 1
            for ModuleID in ModuleIDsList:
                HistogramXray.GetXaxis().SetBinLabel(binX, ModuleID)
                binX = binX + 1

            for RowTuple in Rows:
                ModuleID = RowTuple['ModuleID']
                TestType = RowTuple['TestType']
                binX = 1 + ModuleIDsList.index(ModuleID)

                if TestType == 'XRayHRQualification':
                    NumberOfPixelDefects = []
                    for Chip in range(0,16):
                        try:
                            NumberOfPixelDefectsROC = int(self.GetJSONValue([RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip%d'%Chip, 'BumpBondingDefects_150', 'KeyValueDictPairs.json', 'NumberOfDefectivePixels', 'Value']))
                        except:
                            self.ProblematicModulesList.append(ModuleID)
                            NumberOfPixelDefectsROC = 0
                        NumberOfPixelDefects.append(NumberOfPixelDefectsROC)
                    HistogramXray.SetBinContent(binX, sum(NumberOfPixelDefects))

                if TestType == 'p17_1':
                    try:
                        NumberOfPixelDefects = int(self.GetJSONValue([RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Summary1', 'KeyValueDictPairs.json', 'DeadBumps', 'Value']))
                    except:
                        self.ProblematicModulesList.append(ModuleID)
                        NumberOfPixelDefects = 0
                    HistogramColdbox.SetBinContent(binX, NumberOfPixelDefects)

            HistogramXray.GetXaxis().LabelsOption("v")
            if len(ModuleIDsList) > 200:
                HistogramXray.GetXaxis().SetLabelSize(0.015)
            elif len(ModuleIDsList) > 100:
                HistogramXray.GetXaxis().SetLabelSize(0.025)
            elif len(ModuleIDsList) > 50:
                HistogramXray.GetXaxis().SetLabelSize(0.035)
            else:
                HistogramXray.GetXaxis().SetLabelSize(0.05)

            MaxXray = HistogramXray.GetBinContent(HistogramXray.GetMaximumBin())
            MaxColdbox = HistogramColdbox.GetBinContent(HistogramColdbox.GetMaximumBin())
            HistogramXray.SetMaximum(max(MaxXray, MaxColdbox)*1.05)
            HistogramXray.SetLineColor(ROOT.kBlue + 2)
            HistogramColdbox.SetLineColor(ROOT.kRed + 2)
            HistogramXray.Draw("HIST")
            HistogramColdbox.Draw("*PE SAME")
            ROOT.gPad.Update()

            title = ROOT.TText()
            title.SetNDC()
            title.SetTextAlign(11)
            title.SetTextAlign(12)
            title.SetTextColor(ROOT.kBlack)
            if len(ModuleIDsList) > 0:
                Subtitle = "total number of BB defects, modules: %s to %s (%d)"%(ModuleIDsList[0], ModuleIDsList[-1], NModules)
            else:
                Subtitle = "no modules available"
            title.DrawText(0.05, 0.965, Subtitle)

            title2 = ROOT.TText()
            title2.SetNDC()
            title2.SetTextAlign(12)
            title2.SetTextColor(ROOT.kRed + 2)
            Subtitle2 = "ColdBox+17"
            title2.DrawText(0.9, 0.965, Subtitle2)

            title2 = ROOT.TText()
            title2.SetNDC()
            title2.SetTextAlign(12)
            title2.SetTextColor(ROOT.kBlue + 2)
            Subtitle2 = "Xray"
            title2.DrawText(0.85, 0.965, Subtitle2)

        self.SaveCanvas()
        HTML = self.Image(self.Attributes['ImageFile'], {'height': '300px'})

        AbstractClasses.GeneralProductionOverview.GeneralProductionOverview.GenerateOverview(self)
        return self.Boxed(HTML)

