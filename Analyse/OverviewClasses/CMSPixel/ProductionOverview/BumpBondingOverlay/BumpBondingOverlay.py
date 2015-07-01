import ROOT
import AbstractClasses
import glob

class ProductionOverview(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def CustomInit(self):
    	self.Name='CMSPixel_ProductionOverview_BumpBondingOverlay'
    	self.NameSingle='BumpBondingOverlay'
        self.Title = 'Bump Bonding Defects Overlay, Grade: %s'%self.Attributes['Grade']
        self.DisplayOptions = {
            'Width': 3,
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
        SummaryMap.Fill(10,10)

        SubtestSubfolder = "BumpBondingProblems_150"

        NModules = 0
        for ModuleID in ModuleIDsList:

            for RowTuple in Rows:
                if RowTuple['ModuleID'] == ModuleID:
                    TestType = RowTuple['TestType']
                    if TestType == 'XRayHRQualification' and (RowTuple['Grade'] == self.Attributes['Grade'] or self.Attributes['Grade'] == 'All'):
                        Path = '/'.join([self.GlobalOverviewPath, RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], SubtestSubfolder, '*.root'])
                        RootFiles = glob.glob(Path)
                        if len(RootFiles) > 1:
                            print "more than 1 root file found"
                        elif len(RootFiles) < 1:
                            print "root file not found in: '%s"%Path
                        else:
                            ROOTObject = self.GetHistFromROOTFile(RootFiles[0], "BumpBonding")
                            if ROOTObject:
                                SummaryMap.Add(ROOTObject)
                                NModules += 1
                            else:
                                print "th2d in root file not found"
        
        SummaryMap.Draw("colz")

        self.SaveCanvas()
        HTML = self.Image(self.Attributes['ImageFile']) + self.BoxFooter("Number of modules: %d"%NModules)

        AbstractClasses.GeneralProductionOverview.GeneralProductionOverview.GenerateOverview(self)
        return self.Boxed(HTML)

