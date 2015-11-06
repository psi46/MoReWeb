import ROOT
import AbstractClasses
import glob
import json

class ProductionOverview(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def CustomInit(self):
        self.NameSingle='MeanNoiseROC'
    	self.Name='CMSPixel_ProductionOverview_ProductionOverviewPage_%s'%self.NameSingle
        self.Title = 'MeanNoiseROC {Test}'.format(Test=self.Attributes['Test'])
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

        NoiseMax = 1200
        NBins = 120

        ModuleGrade = {
            '1' : [],
            '2' : [],
            '3' : [],
        }

        Histogram = ROOT.THStack(self.GetUniqueID(),"")
       

        NROCs = 0
        for ModuleID in ModuleIDsList:

            for RowTuple in Rows:
                if RowTuple['ModuleID'] == ModuleID:
                    TestType = RowTuple['TestType']

                    if TestType == self.Attributes['Test']:

                        for Chip in range(0, 16):
                            Value = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips','Chip%d'%Chip, 'SCurveWidths', 'KeyValueDictPairs.json', 'mu', 'Value'])
                            Grade = self.GetJSONValue([RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips','Chip%d'%Chip,'Grading','KeyValueDictPairs.json','PixelDefectsGrade','Value'])
                            if Value is not None and Grade is not None:
                                ModuleGrade[Grade].append(float(Value))
                                NROCs += 1
                            if Value is not None and Grade is None:
                                ModuleGrade['3'].append(float(Value))
                                NROCs += 1

                        break

        hA = ROOT.TH1D("vcalslope_A_%s"%self.GetUniqueID(), "", NBins, 0, NoiseMax)
        hB = ROOT.TH1D("vcalslope_B_%s"%self.GetUniqueID(), "", NBins, 0, NoiseMax)
        hC = ROOT.TH1D("vcalslope_C_%s"%self.GetUniqueID(), "", NBins, 0, NoiseMax)
        hAB = ROOT.TH1D("vcalslope_AB_%s"%self.GetUniqueID(), "", NBins, 0, NoiseMax)
        h = ROOT.TH1D("vcalslope_all_%s"%self.GetUniqueID(), "", NBins, 0, NoiseMax)

        hA.SetFillStyle(1001)
        hA.SetFillColor(self.GetGradeColor('A'))
        hA.SetLineColor(self.GetGradeColor('A'))
        hB.SetFillStyle(1001)
        hB.SetFillColor(self.GetGradeColor('B'))
        hB.SetLineColor(self.GetGradeColor('B'))
        hC.SetFillStyle(1001)
        hC.SetFillColor(self.GetGradeColor('C'))
        hC.SetLineColor(self.GetGradeColor('C'))

        for x in ModuleGrade['1']:
            hA.Fill(x)
        for x in ModuleGrade['2']:
            hB.Fill(x)
        for x in ModuleGrade['3']:
            hC.Fill(x)

        Histogram.Add(hA)
        Histogram.Add(hB)
        Histogram.Add(hC)

        hAB.Add(hA,hB)
        h.Add(hAB,hC)
        
        Histogram.Draw("")


        Histogram.GetXaxis().SetTitle("Noise [e-]")
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


        
        stats = ROOT.TPaveText(0.6,0.6,0.9,0.8, "NDCNB")
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
        GradeAB = float(self.TestResultEnvironmentObject.GradingParameters['noiseB'])
        GradeBC = float(self.TestResultEnvironmentObject.GradingParameters['noiseC'])

        PM = Histogram.GetMaximum()*1.1
        Histogram.SetMaximum(PM)

        PlotMaximum = Histogram.GetMaximum()*3.0


        try:
            CloneHistogram = ROOT.TH1D(self.GetUniqueID(), "", NBins, 0, NoiseMax)
            for i in range(1,NBins):
                if i > GradeAB/NoiseMax*NBins and i < GradeBC/NoiseMax*NBins:
                    CloneHistogram.SetBinContent(i, PlotMaximum)
              
            CloneHistogram.SetFillColorAlpha(ROOT.kBlue, 0.12)
            CloneHistogram.SetFillStyle(1001)
            CloneHistogram.Draw("same")

            CloneHistogram2 = ROOT.TH1D(self.GetUniqueID(), "", NBins, 0, NoiseMax)
            for i in range(1,NBins):
                if i >= GradeBC/NoiseMax*NBins:
                    CloneHistogram2.SetBinContent(i, PlotMaximum)
              
            CloneHistogram2.SetFillColorAlpha(ROOT.kRed, 0.15)
            CloneHistogram2.SetFillStyle(1001)
            CloneHistogram2.Draw("same")

            CloneHistogram3 = ROOT.TH1D(self.GetUniqueID(), "", NBins, 0, NoiseMax)
            for i in range(1,NBins):
                if i <= GradeAB/NoiseMax*NBins:
                    CloneHistogram3.SetBinContent(i, PlotMaximum)
              
            CloneHistogram3.SetFillColorAlpha(ROOT.kGreen+2, 0.1)
            CloneHistogram3.SetFillStyle(1001)
            CloneHistogram3.Draw("same")
        except:
            pass

        # mean, rms and gauss fit sigma
        GaussFitFunction = ROOT.TF1("GaussFitFunction", "gaus(0)")
        GaussFitFunction.SetParameter(0, h.GetBinContent(h.GetMaximumBin()))
        GaussFitFunction.SetParameter(1, h.GetMean())
        GaussFitFunction.SetParameter(2, h.GetRMS())
        GaussFitFunction.SetParLimits(1,0,1000)
        GaussFitFunction.SetParLimits(2,0,200)
        h.Fit(GaussFitFunction, "QB0")
        GaussFitSigma = GaussFitFunction.GetParameter(2)
        title = ROOT.TText()
        title.SetNDC()
        title.SetTextAlign(12)
        title.SetTextSize(0.035)
        TitleText = "Mean: %d, RMS: %.1f, Gauss-fit sigma: %.1f"%(h.GetMean(), h.GetRMS(), GaussFitSigma)
        title.DrawText(0.15, 0.965, TitleText)

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
        return self.Boxed(HTML)

