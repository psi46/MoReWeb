# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import glob
from AbstractClasses.ModuleMap import ModuleMap

class ProductionOverview(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def CustomInit(self):
        self.NameSingle='DeadPixelClusters'
        self.Name='CMSPixel_ProductionOverview_%s'%self.NameSingle
        self.Title = 'Dead Pixel Clusters, Test: %s'%(self.Attributes['Test'])
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

                if TestType == self.Attributes['Test']:
                    nClusteredPixelsPerModule = 0
                    for Chip in range(0,16):
                        Path = '/'.join([self.GlobalOverviewPath, RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips' ,'Chip%s'%Chip, 'PixelMap', '*.root'])
                        RootFiles = glob.glob(Path)
                        ROOTObject = self.GetHistFromROOTFile(RootFiles, "PixelMap")
                        if ROOTObject:
                            for x in range(1, ROOTObject.GetNbinsX()+1):
                                for y in range(1, ROOTObject.GetNbinsY()+1):
                                    BinContent = ROOTObject.GetBinContent(x, y)
                                    if BinContent < 1:
                                        Clustered = False
                                        if (x > 1 and ROOTObject.GetBinContent(x-1, y) < 1):
                                            Clustered = True
                                        if (x < 52 and ROOTObject.GetBinContent(x+1, y) < 1):
                                            Clustered = True
                                        if (y > 1 and ROOTObject.GetBinContent(x, y-1) < 1):
                                            Clustered = True
                                        if (y < 80 and ROOTObject.GetBinContent(x, y+1) < 1):
                                            Clustered = True

                                        if Clustered:
                                            #print "C",Chip," ",x,y
                                            self.ModuleMap.UpdatePlot(Chip, x, y, 1)
                                            nClusteredPixelsPerModule += 1

                            ROOTObject.Delete()
                        else:
                            self.ProblematicModulesList.append(ModuleID)
                            if self.Verbose:
                                print "      Dead Pixel map not found for module '%s' Chip '%d'"%(ModuleID, Chip)
                    Value = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'IVCurve', 'KeyValueDictPairs.json', 'CurrentAtVoltage150V', 'Value'])
                    try:
                        Value = float(Value)
                    except:
                        Value = None
                    print "%s: %d, %f"%(ModuleID, nClusteredPixelsPerModule, Value if Value else 0.0)
                    NModules += 1

            self.CloseFileHandles()

        # draw module map
        if self.ModuleMap:
            ROOT.gStyle.SetOptStat(0)
            self.ModuleMap.Draw(self.Canvas)

        self.ModuleMap.DrawCaption({'Test': self.Attributes['Test'], 'NModules': NModules})

        self.SaveCanvas('png')
        HTML = self.Image(self.Attributes['ImageFile']) + self.BoxFooter("Number of modules: %d"%NModules)

        AbstractClasses.GeneralProductionOverview.GeneralProductionOverview.GenerateOverview(self)
        self.DisplayErrorsList()
        return self.Boxed(HTML)