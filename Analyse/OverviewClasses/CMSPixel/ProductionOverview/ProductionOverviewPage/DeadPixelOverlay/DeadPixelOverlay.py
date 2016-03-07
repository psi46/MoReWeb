# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import glob
from AbstractClasses.ModuleMap import ModuleMap

class ProductionOverview(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def CustomInit(self):
        self.NameSingle='DeadPixelOverlay'
        self.Name='CMSPixel_ProductionOverview_%s'%self.NameSingle
        self.Title = 'Dead Pixel Overlay, Test: %s Grade: %s'%(self.Attributes['Test'], self.Attributes['Grade'])
        self.DisplayOptions = {
            'Width': 2.7,
        }
        self.SubPages = []
        self.SavePlotFile = True
        self.Canvas.SetCanvasSize(1330, 430)
        self.Canvas.Update()

    def GenerateOverview(self):
        Rows = self.FetchData()
        ModuleIDsList = self.GetModuleIDsList(Rows)

        # initialize module map
        self.ModuleMap = ModuleMap(Name=self.GetUniqueID(), nChips=16, StartChip=0)

        NModules = 0

        for RowTuple in Rows:
            if RowTuple['ModuleID'] in ModuleIDsList:
                ModuleID = RowTuple['ModuleID']
                TestType = RowTuple['TestType']
                if TestType == self.Attributes['Test'] and (RowTuple['Grade'] == self.Attributes['Grade'] or self.Attributes['Grade'] == 'All'):
                    for Chip in range(0,16):
                        Path = '/'.join([self.GlobalOverviewPath, RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips' ,'Chip%s'%Chip, 'PixelMap', '*.root'])
                        RootFiles = glob.glob(Path)
                        ROOTObject = self.GetHistFromROOTFile(RootFiles, "PixelMap")
                        if ROOTObject:
                            if ROOTObject.GetEntries() > 0:
                                for x in range(ROOTObject.GetNbinsX()):
                                    for y in range(ROOTObject.GetNbinsY()):
                                        BinContent = ROOTObject.GetBinContent(1 + x, 1 + y)
                                        if BinContent < 1:
                                            self.ModuleMap.UpdatePlot(Chip, x, y, 1)
                            ROOTObject.Delete()
                        else:
                            self.ProblematicModulesList.append(ModuleID)
                            if self.Verbose:
                                print "      Dead Pixel map not found for module '%s' Chip '%d'"%(ModuleID, Chip)
                    NModules += 1

            self.CloseFileHandles()

        # draw module map
        if self.ModuleMap:
            ROOT.gStyle.SetOptStat(0)
            self.ModuleMap.Draw(self.Canvas)

        self.ModuleMap.DrawCaption({'Test': self.Attributes['Test'], 'NModules': NModules, 'Grades': self.Attributes['Grade']})

        self.SaveCanvas('png')
        HTML = self.Image(self.Attributes['ImageFile']) + self.BoxFooter("Number of modules: %d"%NModules)

        AbstractClasses.GeneralProductionOverview.GeneralProductionOverview.GenerateOverview(self)
        self.DisplayErrorsList()
        return self.Boxed(HTML)