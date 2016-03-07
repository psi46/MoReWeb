# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import array

class ProductionOverview(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def CustomInit(self):
        self.NameSingle='ErrorsVsFW'
        self.Name='CMSPixel_ProductionOverview_%s'%self.NameSingle
        self.Title = 'Average Errors vs DTB FW'
        self.DisplayOptions = {
            'Width': 1,
        }
        if self.Attributes.has_key('Width'):
            self.DisplayOptions['Width'] = self.Attributes['Width']
        self.SubPages = []
        self.SavePlotFile = True
        self.Canvas.SetCanvasSize(400, 500)
        self.Canvas.Update()

    def GenerateOverview(self):
        ROOT.gStyle.SetOptStat(0)

        Rows = self.FetchData()
        ErrorType = self.Attributes['ErrorType']

        # extract data
        data = {}
        ErrorTypeLabel = None

        for RowTuple in Rows:
            TestType = RowTuple['TestType']

            if TestType in ['p17_1', 'm20_1', 'm20_2', 'p17_2']:
                try:
                    DTB_FW = self.GetJSONValue([RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Summary2', 'KeyValueDictPairs.json', 'DTB_FW', 'Value'])
                    if DTB_FW is None:
                        raise
                except:
                    DTB_FW = 'NA'

                if ErrorTypeLabel is None:
                    try:
                        ErrorTypeLabel = self.GetJSONValue([RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Errors', 'KeyValueDictPairs.json', ErrorType, 'Label'])
                        if ErrorTypeLabel is None:
                            raise
                    except:
                        ErrorTypeLabel = ErrorType

                try:
                    nErrors = int(self.GetJSONValue([RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Errors', 'KeyValueDictPairs.json', ErrorType, 'Value']))
                except:
                    break

                if DTB_FW not in data:
                    data[DTB_FW] = []

                data[DTB_FW].append(nErrors)

        if ErrorTypeLabel is None:
            ErrorTypeLabel = ErrorType

        # histogram options
        ROOT.gPad.SetLeftMargin(0.04)
        ROOT.gPad.SetRightMargin(0.03)
        Histograms = {}
        HistogramMin = -10
        HistogramMax = 110
        HistogramBins = 12
        first = True

        HistogramColors = [ROOT.kBlue, ROOT.kRed, ROOT.kGreen, ROOT.kCyan+2, ROOT.kOrange, ROOT.kMagenta, ROOT.kGreen+2, ROOT.kBlue+2, ROOT.kYellow+2]
        HistogramColorIndex = 0

        # histograms
        MaximumY = 0
        for DTB_FW in data:
            Histograms[DTB_FW] = ROOT.TH1D(self.GetUniqueID(), "", HistogramBins, HistogramMin, HistogramMax)
            for nErrors in data[DTB_FW]:
                if nErrors > 0:
                    Histograms[DTB_FW].Fill(nErrors)
                else:
                    Histograms[DTB_FW].Fill(-1)

            MaxBinContent = Histograms[DTB_FW].GetBinContent(Histograms[DTB_FW].GetMaximumBin())
            if MaxBinContent > MaximumY:
                MaximumY = MaxBinContent


            OverflowBinContent = Histograms[DTB_FW].GetBinContent(HistogramBins + 1)
            Histograms[DTB_FW].SetBinContent(HistogramBins, Histograms[DTB_FW].GetBinContent(HistogramBins) + OverflowBinContent)

            Histograms[DTB_FW].SetLineColor(HistogramColors[HistogramColorIndex])
            try:
                Histograms[DTB_FW].SetFillColorAlpha(HistogramColors[HistogramColorIndex], 0.25)
            except:
                pass
            HistogramColorIndex += 1
            if HistogramColorIndex >= len(HistogramColors):
                HistogramColorIndex = 0

            Histograms[DTB_FW].Draw("same" if not first else "hist")
            first = False

        # set correct height
        for DTB_FW in data:
            Histograms[DTB_FW].GetYaxis().SetRangeUser(0, MaximumY * 1.1)

        # caption
        title = ROOT.TText()
        title.SetNDC()
        title.SetTextAlign(11)
        title.SetTextAlign(12)
        title.SetTextColor(ROOT.kBlack)
        Subtitle = "Fulltests, %s"%ErrorTypeLabel
        title.DrawText(0.05, 0.965, Subtitle)

        # legend
        Legend = ROOT.TLegend(0.75,0.7,0.9,0.9)
        for DTB_FW in data:
            Legend.AddEntry(Histograms[DTB_FW], "{FW}, mu = {mean:1.1f}".format(FW=DTB_FW, mean=Histograms[DTB_FW].GetMean()))
        Legend.Draw("same")

        self.SaveCanvas()
        HTML = self.Image(self.Attributes['ImageFile'])

        AbstractClasses.GeneralProductionOverview.GeneralProductionOverview.GenerateOverview(self)
        return self.Boxed(HTML)

