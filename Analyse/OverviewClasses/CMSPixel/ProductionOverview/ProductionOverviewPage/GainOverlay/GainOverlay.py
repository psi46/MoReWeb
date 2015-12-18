# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import glob
from AbstractClasses.ModuleMap import ModuleMap

class ProductionOverview(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def CustomInit(self):
        self.NameSingle='GainOverlay'
        self.Name='CMSPixel_ProductionOverview_%s'%self.NameSingle
        self.Title = 'Bad gain Overlay, Test: %s Grade: %s'%(self.Attributes['Test'], self.Attributes['Grade'])
        self.DisplayOptions = {
            'Width': 2.7,
        }
        self.SubPages = []
        self.SavePlotFile = True
        self.Canvas.SetCanvasSize(1330, 430)
        self.Canvas.Update()

    def GenerateOverview(self):

        # initialize module map
        self.ModuleMap = ModuleMap(Name=self.GetUniqueID(), nChips=16, StartChip=0)

        Rows = self.FetchData()
        ModuleIDsList = self.GetModuleIDsList(Rows)

        gainMin = float(self.TestResultEnvironmentObject.GradingParameters['gainMin'])
        gainMax = float(self.TestResultEnvironmentObject.GradingParameters['gainMax'])

        NModules = 0

        for RowTuple in Rows:
            if RowTuple['ModuleID'] in ModuleIDsList:
                ModuleID = RowTuple['ModuleID']
                TestType = RowTuple['TestType']
                if TestType == self.Attributes['Test'] and (RowTuple['Grade'] == self.Attributes['Grade'] or self.Attributes['Grade'] == 'All'):
                    ModuleOk = True
                    for Chip in range(0,16):
                        Path = '/'.join([self.GlobalOverviewPath, RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips' ,'Chip%s'%Chip, 'PHCalibrationGainMap', '*.root'])
                        RootFiles = glob.glob(Path)
                        ROOTObject = self.GetHistFromROOTFile(RootFiles, "PHCalibrationGainMap")
                        if ROOTObject:
                            for x in range(1, ROOTObject.GetNbinsX()+1):
                                for y in range(1, ROOTObject.GetNbinsY()+1):
                                    BinContent = ROOTObject.GetBinContent(x, y)
                                    if BinContent < gainMin or BinContent > gainMax:
                                        self.ModuleMap.UpdatePlot(Chip, x, y, 1)
                            ROOTObject.Delete()
                        else:
                            self.ProblematicModulesList.append(ModuleID)
                            ModuleOk = False
                            if self.Verbose:
                                print "      Dead Pixel map not found for module '%s' Chip '%d'"%(ModuleID, Chip)

                    if ModuleOk:
                        NModules += 1

        self.CloseFileHandles()

        # draw module map
        if self.ModuleMap:
            self.ModuleMap.Draw(self.Canvas)

        title = ROOT.TText()
        title.SetNDC()
        title.SetTextAlign(12)

        Subtitle = self.Attributes['Test']
        TestNames = {'m20_1' : 'Fulltest -20°C BTC', 'm20_2': 'Fulltest -20°C ATC', 'p17_1': 'Fulltest +17°C'}
        if TestNames.has_key(Subtitle):
            Subtitle = TestNames[Subtitle]
        Subtitle += ",  modules: %d, Grades: %s"%(NModules, self.Attributes['Grade'])
        title.DrawText(0.15,0.965,Subtitle)

        self.SaveCanvas('png')
        HTML = self.Image(self.Attributes['ImageFile']) + self.BoxFooter("Number of modules: %d"%NModules)

        AbstractClasses.GeneralProductionOverview.GeneralProductionOverview.GenerateOverview(self)
        self.DisplayErrorsList()
        return self.Boxed(HTML)