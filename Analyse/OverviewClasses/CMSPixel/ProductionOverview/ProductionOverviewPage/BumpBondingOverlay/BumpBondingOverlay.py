# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import glob
from AbstractClasses.ModuleMap import ModuleMap

class ProductionOverview(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def CustomInit(self):
        self.Name='CMSPixel_ProductionOverview_BumpBondingOverlay'
        self.NameSingle='BumpBondingOverlay'
        self.Xray = False
        if 'Xray' in self.Attributes and self.Attributes['Xray']:
            self.Xray = True
            self.Title = 'BB Defects X-ray, Grade: %s'%self.Attributes['Grade']
        else:
            self.Title = 'BB Defects FT, Grade: %s'%self.Attributes['Grade']

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

        # initialize module map
        self.ModuleMap = ModuleMap(Name=self.GetUniqueID(), nChips=16, StartChip=0)

        NModules = 0
        for RowTuple in Rows:
            if RowTuple['ModuleID'] in ModuleIDsList:
                ModuleID = RowTuple['ModuleID']

                if RowTuple['Grade'] == self.Attributes['Grade'] or self.Attributes['Grade'] == 'All':

                    if self.Xray:
                        TestType = 'XRayHRQualification'
                    else:
                        TestType = 'p17'

                    if RowTuple['TestType'].startswith(TestType):

                        if self.Xray:
                            Path = '/'.join([self.GlobalOverviewPath, RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], "BumpBondingProblems_150", '*.root'])
                        else:
                            Path = '/'.join([self.GlobalOverviewPath, RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], "BumpBondingMap", '*.root'])

                        RootFiles = glob.glob(Path)
                        ROOTObject = self.GetHistFromROOTFile(RootFiles, "BumpBonding")

                        try:
                            SpecialBBTestName = self.GetJSONValue([RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'BumpBondingMap', 'HiddenData.json', 'SpecialBumpBondingTestName', 'Value'])
                            if ROOTObject and SpecialBBTestName.strip().upper() == 'BB2':
                                # BB2 reprocessing
                                for x in range(1, ROOTObject.GetNbinsX()+1):
                                    for y in range(1, ROOTObject.GetNbinsY()+1):
                                        Value = ROOTObject.GetBinContent(x, y)
                                        if Value > 1:
                                            ROOTObject.SetBinContent(x, y, 1)
                                        else:
                                            ROOTObject.SetBinContent(x, y, 0)

                        except:
                            pass

                        if ROOTObject:
                            self.ModuleMap.AddTH2D(ROOTObject=ROOTObject)
                            NModules += 1
                        else:
                            self.ProblematicModulesList.append(ModuleID)
                            if self.Verbose:
                                print "warning: BumpBonding map not found for module: '%s'"%ModuleID

        # draw module map
        if self.ModuleMap:
            self.ModuleMap.Draw(self.Canvas)

        title = ROOT.TText()
        title.SetNDC()
        title.SetTextAlign(12)
        Subtitle = "modules: %d, Grades: %s"%(NModules, self.Attributes['Grade'])
        title.DrawText(0.15,0.965,Subtitle)

        self.SaveCanvas('png')
        HTML = self.Image(self.Attributes['ImageFile']) + self.BoxFooter("Number of modules: %d"%NModules)

        AbstractClasses.GeneralProductionOverview.GeneralProductionOverview.GenerateOverview(self)

        self.DisplayErrorsList()
        return self.Boxed(HTML)

