import ROOT
import AbstractClasses
import glob
import json

class ProductionOverview(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def CustomInit(self):
        self.NameSingle='VcalOffset'
    	self.Name='CMSPixel_ProductionOverview_%s'%self.NameSingle
        self.Title = 'Vcal Offset'
        self.DisplayOptions = {
            'Width': 1,
        }
        self.SubPages = []
        self.SavePlotFile = True
        self.Canvas.SetCanvasSize(400,500)

    def GenerateOverview(self):
        ROOT.gStyle.SetOptStat(111210)
        ROOT.gPad.SetLogy(1)

        TableData = []

        Rows = self.FetchData()
        ModuleIDsList = self.GetModuleIDsList(Rows)

        HTML = ""

        HistogramMin = -2000
        HistogramMax = 2000
        NBins = 50


        ModuleGrade = {
            'A' : [],
            'B' : [],
            'C' : [],
        }

        Histogram = ROOT.THStack(self.GetUniqueID(),"")


        NROCs = 0
        for ModuleID in ModuleIDsList:

            for RowTuple in Rows:
                if RowTuple['ModuleID'] == ModuleID:
                    TestType = RowTuple['TestType']

                    if TestType == 'XrayCalibration_Spectrum':
                        for Chip in range(0, 16):
                            Value = self.GetJSONValue([RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips_Xray', 'Chip_Xray%d'%Chip,  'Xray_Calibration_Spectrum_Chip%d'%Chip, 'KeyValueDictPairs.json', "Offset", 'Value'])
                            Grade = self.GetJSONValue([RowTuple['RelativeModuleFinalResultsPath'],'QualificationGroup','XRayHRQualification','Chips','Chip%d'%Chip,'Grading','KeyValueDictPairs.json','ROCGrade','Value'])

                            if Value is not None:
                                try:
                                    ModuleGrade[Grade].append(float(Value))
                                    NROCs += 1
                                except:
                                    self.ProblematicModulesList.append(ModuleID)
                            else:
                                self.ProblematicModulesList.append(ModuleID)

                        break


        hA = ROOT.TH1D("vcaloffset_A_%s"%self.GetUniqueID(), "", NBins, HistogramMin, HistogramMax)
        hB = ROOT.TH1D("vcaloffset_B_%s"%self.GetUniqueID(), "", NBins, HistogramMin, HistogramMax)
        hC = ROOT.TH1D("vcaloffset_C_%s"%self.GetUniqueID(), "", NBins, HistogramMin, HistogramMax)
        hAB = ROOT.TH1D("vcaloffset_AB_%s"%self.GetUniqueID(), "", NBins, HistogramMin, HistogramMax)
        h = ROOT.TH1D("vcaloffset_all_%s"%self.GetUniqueID(), "", NBins, HistogramMin, HistogramMax)

        hA.SetFillStyle(1001)
        hA.SetFillColor(self.GetGradeColor('A'))
        hA.SetLineColor(self.GetGradeColor('A'))
        hB.SetFillStyle(1001)
        hB.SetFillColor(self.GetGradeColor('B'))
        hB.SetLineColor(self.GetGradeColor('B'))
        hC.SetFillStyle(1001)
        hC.SetFillColor(self.GetGradeColor('C'))
        hC.SetLineColor(self.GetGradeColor('C'))

        for x in ModuleGrade['A']:
            hA.Fill(x)
        for x in ModuleGrade['B']:
            hB.Fill(x)
        for x in ModuleGrade['C']:
            hC.Fill(x)

        Histogram.Add(hA)
        Histogram.Add(hB)
        Histogram.Add(hC)

        hAB.Add(hA,hB)
        h.Add(hAB,hC)

        Histogram.Draw("")

        Histogram.GetXaxis().SetTitle("Offset [e^-]")
        Histogram.GetYaxis().SetTitle("# ROCs")
        Histogram.GetYaxis().SetTitleOffset(1.5)

        meanAll = round(h.GetMean(),2)
        meanAB = round(hAB.GetMean(),2)
        meanC = round(hC.GetMean(),2)
        meanerrAll = round(h.GetMeanError(),2)
        meanerrAB = round(hAB.GetMeanError(),2)
        meanerrC = round(hC.GetMeanError(),2)
        RMSAll = round(h.GetRMS(),2)
        RMSAB = round(hAB.GetRMS(),2)
        RMSC = round(hC.GetRMS(),2)
        underAll = int(h.GetBinContent(0))
        underAB = int(hAB.GetBinContent(0))
        underC = int(hC.GetBinContent(0))
        overAll = int(h.GetBinContent(NBins+1))
        overAB = int(hAB.GetBinContent(NBins+1))
        overC = int(hC.GetBinContent(NBins+1))


        
        stats = ROOT.TPaveText(0.15,0.7,0.45,0.9, "NDCNB")
        stats.SetFillColor(ROOT.kWhite)
        stats.SetTextSize(0.025)
        stats.SetTextAlign(10)
        stats.SetTextFont(62)
        stats.SetBorderSize(0)
        stats.AddText("All: #mu = {0} #pm {1}".format(meanAll,meanerrAll))
        stats.AddText(" #sigma = {0}".format(RMSAll))
        stats.AddText("  UF = {0}, OF = {1}".format(underAll,overAll))
        stats.AddText("AB: #mu = {0} #pm {1}".format(meanAB,meanerrAB))
        stats.AddText(" #sigma = {0}".format(RMSAB))
        stats.AddText("  UF = {0}, OF = {1}".format(underAB,overAB))
        stats.AddText("C: #mu = {0} #pm {1}".format(meanC,meanerrC))
        stats.AddText(" #sigma = {0}".format(RMSC))
        stats.AddText("  UF = {0}, OF = {1}".format(underC,overC))
        stats.Draw("same")


        # subtitle
        title = ROOT.TText()
        title.SetNDC()
        title.SetTextAlign(12)
        title.SetTextSize(0.03)
        Subtitle = "Vcal calibration offset, Spectrum Method, ROCs:{NROCs}".format(NROCs=NROCs)
        title.DrawText(0.15,0.95,Subtitle)

        title4 = ROOT.TText()
        title4.SetNDC()
        title4.SetTextAlign(12)
        title4.SetTextSize(0.03)
        title4.SetTextColor(self.GetGradeColor('A'))
        title4.DrawText(0.72,0.9,"Grade A")

        title2 = ROOT.TText()
        title2.SetNDC()
        title2.SetTextAlign(12)
        title2.SetTextSize(0.03)
        title2.SetTextColor(self.GetGradeColor('B'))
        title2.DrawText(0.72,0.88,"Grade B")

        title3 = ROOT.TText()
        title3.SetNDC()
        title3.SetTextAlign(12)
        title3.SetTextSize(0.03)
        title3.SetTextColor(self.GetGradeColor('C'))
        title3.DrawText(0.72,0.86,"Grade C")

        self.SaveCanvas()

        HTML = self.Image(self.Attributes['ImageFile']) + self.BoxFooter("Number of ROCs: %d"%NROCs)

        AbstractClasses.GeneralProductionOverview.GeneralProductionOverview.GenerateOverview(self)


        ROOT.gPad.SetLogy(0)
        self.DisplayErrorsList()
        return self.Boxed(HTML)


