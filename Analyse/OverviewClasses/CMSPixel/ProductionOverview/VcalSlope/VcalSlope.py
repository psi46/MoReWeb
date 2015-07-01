import ROOT
import AbstractClasses
import glob
import json

class ProductionOverview(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def CustomInit(self):
        self.NameSingle='VcalSlope'
    	self.Name='CMSPixel_ProductionOverview_%s'%self.NameSingle
        self.Title = 'Vcal Slope'
        self.DisplayOptions = {
            'Width': 1,
        }
        self.SubPages = []
        self.SavePlotFile = True
        self.Canvas.SetCanvasSize(400,500)

    def GenerateOverview(self):
        ROOT.gStyle.SetOptStat(1)
        ROOT.gPad.SetLogy(1)

        TableData = []

        Rows = self.FetchData()

        ModuleIDsList = []
        for RowTuple in Rows:
            if not RowTuple['ModuleID'] in ModuleIDsList:
                ModuleIDsList.append(RowTuple['ModuleID'])

        HTML = ""

        HistogramMin = 30
        HistogramMax = 64
        NBins = 68
        Histogram = ROOT.TH1D(self.GetUniqueID(), "", NBins, HistogramMin, HistogramMax)

        PlotColor = ROOT.kRed
        Histogram.SetLineColor(PlotColor)
        Histogram.SetFillColor(PlotColor)
        Histogram.SetFillStyle(1001)
        Histogram.GetXaxis().SetTitle("e^-/Vcal[DAC]")
        Histogram.GetYaxis().SetTitle("# ROCs")
        Histogram.GetYaxis().SetTitleOffset(1.5)

        NROCs = 0
        for ModuleID in ModuleIDsList:

            for RowTuple in Rows:
                if RowTuple['ModuleID'] == ModuleID:
                    TestType = RowTuple['TestType']

                    if TestType == 'XrayCalibration_Spectrum':
                        for Chip in range(0, 16):
                            Path = '/'.join([self.GlobalOverviewPath, RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips_Xray','Chip_Xray%d'%Chip, 'Xray_Calibration_Spectrum_Chip%d'%Chip, 'KeyValueDictPairs.json'])
                            JSONFiles = glob.glob(Path)
                            if len(JSONFiles) > 1:
                                print "WARNING: %s more than 1 file found '%s"%(self.Name, Path)
                            elif len(JSONFiles) < 1:
                                print "WARNING: %s json file not found: '%s"%(self.Name, Path)
                            else:
                                
                                with open(JSONFiles[0]) as data_file:    
                                    JSONData = json.load(data_file)
                                
                                Histogram.Fill(float(JSONData["Slope"]['Value']))
                                NROCs += 1

                        break
        
        Histogram.Draw("")

        # subtitle
        title = ROOT.TText()
        title.SetNDC()
        title.SetTextAlign(12)
        title.SetTextSize(0.03)
        Subtitle = "Vcal calibration slope, Spectrum Method, ROCs:{NROCs}".format(NROCs=NROCs)
        title.DrawText(0.15,0.95,Subtitle)

        self.SaveCanvas()

        HTML = self.Image(self.Attributes['ImageFile']) + self.BoxFooter("Number of ROCs: %d"%NROCs)

        AbstractClasses.GeneralProductionOverview.GeneralProductionOverview.GenerateOverview(self)


        ROOT.gPad.SetLogy(0)
        return self.Boxed(HTML)


