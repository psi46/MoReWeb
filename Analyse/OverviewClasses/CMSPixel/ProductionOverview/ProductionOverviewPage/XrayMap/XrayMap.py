# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import glob
from AbstractClasses.ModuleMap import ModuleMap

class ProductionOverview(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def CustomInit(self):
        self.Name='CMSPixel_ProductionOverview_XrayMap'
        self.NameSingle='XrayMap'

        self.DisplayOptions = {
            'Width': 2.7*2,
        }
        self.SubPages = []
        self.SavePlotFile = True
        self.Canvas.SetCanvasSize(1330, 430)
        self.Canvas.Update()

    def GenerateOverview(self):
        Rows = self.FetchData()
        ModuleIDsList = self.GetModuleIDsList(Rows)
        ROOT.gStyle.SetOptStat(0)

        # initialize module map
        self.ModuleMap = ModuleMap(Name=self.GetUniqueID(), nChips=16, StartChip=0)
        self.ModuleMap.SetContour(100)

        NModules = 0
        TotalMaximum = 0
        for RowTuple in Rows:
            if RowTuple['ModuleID'] in ModuleIDsList:
                ModuleID = RowTuple['ModuleID']

                TestType = 'XrayCalibration_Spectrum'
                if RowTuple['TestType'].startswith(TestType):

                    Path = '/'.join([self.GlobalOverviewPath, RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], "HitmapOverview_" + self.Attributes["Target"], '*.root'])
                    print Path
                    RootFiles = glob.glob(Path)
                    ROOTObject = self.GetHistFromROOTFile(RootFiles, "Map")

                    if ROOTObject:
                        self.ModuleMap.AddTH2D(ROOTObject=ROOTObject)
                        TotalMaximum += ROOTObject.GetMaximum()
                        NModules += 1
                    else:
                        self.ProblematicModulesList.append(ModuleID)
                        print "warning: xray map not found for module: '%s'"%ModuleID
                else:
                    print RowTuple['TestType']
        self.ModuleMap.Map2D.GetZaxis().SetRangeUser(0, TotalMaximum)

        # draw module map
        if self.ModuleMap:
            self.ModuleMap.Draw(self.Canvas)

        title = ROOT.TText()
        title.SetNDC()
        title.SetTextAlign(12)
        Subtitle = self.Attributes["Target"] + " modules: %d"%NModules
        title.DrawText(0.15,0.965,Subtitle)

        self.SaveCanvas('png')
        HTML = self.Image(self.Attributes['ImageFile'])

        AbstractClasses.GeneralProductionOverview.GeneralProductionOverview.GenerateOverview(self)

        self.DisplayErrorsList()
        return self.Boxed(HTML)

