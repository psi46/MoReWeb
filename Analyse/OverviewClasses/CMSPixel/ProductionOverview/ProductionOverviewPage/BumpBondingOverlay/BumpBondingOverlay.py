# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import glob

class ProductionOverview(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def CustomInit(self):
    	self.Name='CMSPixel_ProductionOverview_BumpBondingOverlay'
    	self.NameSingle='BumpBondingOverlay'
        self.Title = 'Bump Bonding Defects Overlay, Grade: %s'%self.Attributes['Grade']
        self.DisplayOptions = {
            'Width': 2.5,
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

        nCols = 8 * 52+1
        nRows = 2 * 80+1
        SummaryMap = ROOT.TH2D(self.GetUniqueID(), "", nCols, 0, nCols, nRows, 0, nRows)

        SubtestSubfolder = "BumpBondingProblems_150"

        NModules = 0
        for ModuleID in ModuleIDsList:

            for RowTuple in Rows:
                if RowTuple['ModuleID'] == ModuleID:
                    TestType = RowTuple['TestType']
                    if TestType == 'XRayHRQualification' and (RowTuple['Grade'] == self.Attributes['Grade'] or self.Attributes['Grade'] == 'All'):
                        Path = '/'.join([self.GlobalOverviewPath, RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], SubtestSubfolder, '*.root'])
                        RootFiles = glob.glob(Path)

                        ROOTObject = self.GetHistFromROOTFile(RootFiles, "BumpBonding")
                        if ROOTObject:
                            SummaryMap.Add(ROOTObject)
                            NModules += 1
                        else:
                            self.ProblematicModulesList.append(ModuleID)
                            if self.Verbose:
                                print "warning: BumpBonding map not found for module: '%s'"%ModuleID
        
        SummaryMap.Draw("colz")

        title = ROOT.TText()
        title.SetNDC()
        title.SetTextAlign(12)
        Subtitle = "modules: %d, Grades: %s"%(NModules, self.Attributes['Grade'])
        title.DrawText(0.15,0.965,Subtitle)

        self.SaveCanvas()
        HTML = self.Image(self.Attributes['ImageFile']) + self.BoxFooter("Number of modules: %d"%NModules)

        AbstractClasses.GeneralProductionOverview.GeneralProductionOverview.GenerateOverview(self)

        self.DisplayErrorsList()
        return self.Boxed(HTML)

