# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import glob

class ProductionOverview(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def CustomInit(self):
        self.NameSingle='IVCurveOverlay'
    	self.Name='CMSPixel_ProductionOverview_%s'%self.NameSingle
        self.Title = 'IVCurve Overlay %s'%self.Attributes['Test']
        self.DisplayOptions = {
            'Width': 2.5,
        }
        self.SubPages = []
        self.SavePlotFile = True
        self.Canvas.SetCanvasSize(800, 430)
        self.Canvas.Update()

    def GenerateOverview(self):
        ROOT.gStyle.SetOptStat(0)
        ROOT.gPad.SetLogy(1)

        TableData = []

        Rows = self.FetchData()
        ModuleIDsList = self.GetModuleIDsList(Rows)
        HTML = ""

        self.Canvas.Clear()

        MultiGraph = ROOT.TMultiGraph()
        NModules = 0
        for ModuleID in ModuleIDsList:
            for RowTuple in Rows:
                if RowTuple['ModuleID'] == ModuleID:
                    TestType = RowTuple['TestType']
                    if TestType == self.Attributes['Test']:
                        Path = '/'.join([self.GlobalOverviewPath, RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'IVCurve', '*.root'])
                        RootFiles = glob.glob(Path)
                        if len(RootFiles) > 1:
                            if self.Verbose:
                                print "more than 1 root file found in: '%s"%Path
                            self.ProblematicModulesList.append(ModuleID)
                        elif len(RootFiles) < 1:
                            if '_m20_1' not in Path:
                                if self.Verbose:
                                    print "root file not found in: '%s"%Path
                                self.ProblematicModulesList.append(ModuleID)
                        else:
                            ROOTObject = self.GetHistFromROOTFile(RootFiles[0], "Graph")
                            if ROOTObject:
                                IVGrade = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Grading', 'KeyValueDictPairs.json', 'IVGrade', 'Value'])
                                IVColor = ROOT.kBlue
                                try:
                                    if int(IVGrade) == 3:
                                        IVColor = self.GradeColors['C']
                                    elif int(IVGrade) == 2:
                                        IVColor = self.GradeColors['B']
                                    elif int(IVGrade) == 1:
                                        IVColor = self.GradeColors['A']
                                except:
                                    if self.Verbose:
                                        print "WARNING: ",ModuleID," IV ",TestType, " unable to read IV grade or IV grade not A/B/C: '",IVGrade,"'"
                                    self.ProblematicModulesList.append(ModuleID)

                                try:
                                    ROOTObject.SetLineColorAlpha(IVColor, 0.35)
                                except:
                                    # might fail in old ROOT versions
                                    pass
                                MultiGraph.Add(ROOTObject)
                                NModules += 1
                            else:
                                if self.Verbose:
                                    print "WARNING: graph in root file not found"
                                self.ProblematicModulesList.append(ModuleID)
        if MultiGraph:
            MultiGraph.Draw("AL")
            if MultiGraph.GetXaxis():
                MultiGraph.GetXaxis().SetTitle("Voltage [V]")
                MultiGraph.GetYaxis().SetTitle("Current [A]")
                MultiGraph.GetYaxis().SetTitleOffset(1)

            title = ROOT.TText()
            title.SetNDC()
            title.SetTextAlign(12)
            Subtitle = self.Attributes['Test']
            TestNames = {'m20_1' : 'Fulltest -20C BTC', 'm20_2': 'Fulltest -20C ATC', 'p17_1': 'Fulltest +17C'}
            if TestNames.has_key(Subtitle):
                Subtitle = TestNames[Subtitle]
            title.DrawText(0.15,0.965,"%s, modules: %d"%(Subtitle,NModules))

        self.SaveCanvas()
        HTML = self.Image(self.Attributes['ImageFile'])

        AbstractClasses.GeneralProductionOverview.GeneralProductionOverview.GenerateOverview(self)
        ROOT.gPad.SetLogy(0)
        self.DisplayErrorsList()
        return self.Boxed(HTML)

