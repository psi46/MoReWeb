# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import glob
import os

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
        ROOT.gStyle.SetOptStat(0)

        for RowTuple in Rows:
            if RowTuple['ModuleID'] in ModuleIDsList:
                ModuleID = RowTuple['ModuleID']
                TestType = RowTuple['TestType']
                if TestType == self.Attributes['Test'] and (RowTuple['Grade'] == self.Attributes['Grade'] or self.Attributes['Grade'] == 'All'):
                    ModuleOk = True
                    for Chip in range(0,16):
                        Path = '/'.join([self.GlobalOverviewPath, RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips','Chip%s'%Chip, 'PHCalibrationGainMap', '*.root'])
                        RootFiles = glob.glob(Path)
                        ROOTObject = self.GetHistFromROOTFile(RootFiles, "PHCalibrationGainMap")
                        if ROOTObject:
                            if ROOTObject.GetEntries() > 0:
                                for x in range(ROOTObject.GetNbinsX()):
                                    for y in range(ROOTObject.GetNbinsY()):
                                        BinContent = ROOTObject.GetBinContent(1 + x, 1 + y)
                                        if BinContent < gainMin or BinContent > gainMax:
                                            self.ModuleMap.UpdatePlot(Chip, x, y, 1)
                            ROOTObject.Delete()
                        else:
                            self.ProblematicModulesList.append(ModuleID)
                            ModuleOk = False
                            if self.Verbose:
                                print "      Gain map not found for module '%s' Chip '%d'"%(ModuleID, Chip)

                    if ModuleOk:
                        NModules += 1

        self.CloseFileHandles()

        # draw module map
        if self.ModuleMap:
            self.ModuleMap.Draw(self.Canvas)

        self.ModuleMap.DrawCaption({'Test': self.Attributes['Test'], 'NModules': NModules, 'Grades': self.Attributes['Grade']})

        self.SaveCanvas('png')
        HTML = self.Image(self.Attributes['ImageFile']) + self.BoxFooter("Number of modules: %d"%NModules)

        AbstractClasses.GeneralProductionOverview.GeneralProductionOverview.GenerateOverview(self)
        self.DisplayErrorsList()
        return self.Boxed(HTML)