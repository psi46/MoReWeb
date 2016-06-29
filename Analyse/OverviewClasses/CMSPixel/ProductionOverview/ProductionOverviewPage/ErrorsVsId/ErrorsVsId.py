# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import glob
import array

class ProductionOverview(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def CustomInit(self):
        self.NameSingle='ErrorsVsId'
        self.Name='CMSPixel_ProductionOverview_%s'%self.NameSingle
        self.Title = 'Readout Errors vs ID'
        self.DisplayOptions = {
            'Width': 5.4,
        }
        if self.Attributes.has_key('Width'):
            self.DisplayOptions['Width'] = self.Attributes['Width']
        self.SubPages = []
        self.SavePlotFile = True
        self.Canvas.SetCanvasSize(1600, 400)
        self.Canvas.Update()

    def GenerateOverview(self):
        ROOT.gStyle.SetOptStat(0)
        ROOT.gPad.SetLogy(1)
        ROOT.gPad.SetLeftMargin(0.04)
        ROOT.gPad.SetRightMargin(0.03)

        self.Canvas.SetFrameLineStyle(0)
        self.Canvas.SetFrameLineWidth(1)
        self.Canvas.SetFrameBorderMode(0)
        self.Canvas.SetFrameBorderSize(1)

        ErrorType = self.Attributes['ErrorType']
        Rows = self.FetchData()
        ModuleIDsList = self.GetModuleIDsList(Rows)
        NModules = len(ModuleIDsList)
        NTests = 0
        BinNames = []

        # find all possible firmwares
        DTB_FWs = []
        for RowTuple in Rows:
            TestType = RowTuple['TestType']
            if TestType in ['p17_1', 'm20_1', 'm20_2', 'p17_2']:
                try:
                    DTB_FW = self.GetJSONValue([RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Summary2', 'KeyValueDictPairs.json', 'DTB_FW', 'Value'])
                    if DTB_FW is None:
                        DTB_FW = 'NA'
                except:
                    DTB_FW = 'NA'
                try:
                    if DTB_FW not in DTB_FWs:
                        DTB_FWs.append(DTB_FW)
                    NTests +=1
                    BinNames.append(RowTuple['ModuleID'] if len(RowTuple['ModuleID'].strip()) > 0 else '')
                except:
                    print "could not add module",RowTuple," to error statistics plot."


        # initialize histograms
        Histograms = {}
        HistogramsCreated = True
        for DTB_FW in DTB_FWs:
            Histograms[DTB_FW] = ROOT.TH1D(self.GetUniqueID(), "", NTests, 0, NTests)
            Histograms[DTB_FW].GetXaxis().SetNdivisions(-NTests)
            Histograms[DTB_FW].GetXaxis().SetTickLength(0.015)
            Histograms[DTB_FW].GetYaxis().SetTickLength(0.012)
            try:
                Histograms[DTB_FW].GetXaxis().SetAxisColor(1, 0.4)
                Histograms[DTB_FW].GetYaxis().SetAxisColor(1, 0.4)
            except:
                pass
            HistogramsCreated = HistogramsCreated and Histograms[DTB_FW]

        # extract data
        data = {}
        for DTB_FW in DTB_FWs:
            data[DTB_FW] = []

        for RowTuple in Rows:
            TestType = RowTuple['TestType']

            if TestType in ['p17_1', 'm20_1', 'm20_2', 'p17_2']:
                try:
                    DTB_FW_JSON = self.GetJSONValue([RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Summary2', 'KeyValueDictPairs.json', 'DTB_FW', 'Value'])
                    if DTB_FW_JSON is None:
                        raise
                except:
                    DTB_FW_JSON = 'NA'

                try:
                    nErrors = int(self.GetJSONValue([RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Errors', 'KeyValueDictPairs.json', ErrorType, 'Value']))
                except:
                    break

                for DTB_FW in DTB_FWs:
                    if DTB_FW_JSON and DTB_FW == DTB_FW_JSON.strip():
                        data[DTB_FW].append(nErrors)
                    else:
                        data[DTB_FW].append(0)

        # fill histograms
        if HistogramsCreated:
            for DTB_FW, Histogram in Histograms.iteritems():
                if Histograms[DTB_FW]:
                    binX = 1
                    OldBinName = ''
                    for BinName in BinNames:
                        if BinName != OldBinName:
                            Histograms[DTB_FW].GetXaxis().SetBinLabel(binX, BinName)
                            OldBinName = BinName
                        binX = binX + 1

            for DTB_FW in DTB_FWs:
                binX = 1
                for nErrors in data[DTB_FW]:
                    Histograms[DTB_FW].SetBinContent(binX, nErrors)
                    binX += 1

        # set correct height
        MaxY = 0
        for DTB_FW in DTB_FWs:
            if max(data[DTB_FW]) > MaxY:
                MaxY = max(data[DTB_FW])
        for DTB_FW in data:
            Histograms[DTB_FW].GetYaxis().SetRangeUser(0.5, MaxY * 1.5)
            Histograms[DTB_FW].GetXaxis().LabelsOption("v")

        # draw histograms
        first = True
        HistogramColors = [ROOT.kBlue, ROOT.kRed, ROOT.kGreen, ROOT.kCyan+2, ROOT.kOrange, ROOT.kMagenta, ROOT.kGreen+2, ROOT.kBlue+2, ROOT.kYellow+2]
        HistogramColorIndex = 0

        for DTB_FW, Histogram in Histograms.iteritems():
            Histograms[DTB_FW].SetLineColor(HistogramColors[HistogramColorIndex])
            Histograms[DTB_FW].SetLineWidth(1)
            try:
                Histograms[DTB_FW].SetFillColorAlpha(HistogramColors[HistogramColorIndex], 0.25)
            except:
                pass
            HistogramColorIndex += 1
            if HistogramColorIndex >= len(HistogramColors):
                HistogramColorIndex = 0

            Histograms[DTB_FW].Draw("same" if not first else "hist")
            first = False

        # legend
        Legend = ROOT.TLegend(0.05,0.65,0.10,0.9)
        for DTB_FW in data:
            Legend.AddEntry(Histograms[DTB_FW], "{FW}".format(FW=DTB_FW))
        Legend.Draw("same")

        # caption
        title = ROOT.TText()
        title.SetNDC()
        title.SetTextAlign(11)
        title.SetTextAlign(12)
        title.SetTextColor(ROOT.kBlack)
        Subtitle = "Fulltests, %s"%ErrorType
        title.DrawText(0.04, 0.965, Subtitle)

        self.SaveCanvas()
        HTML = self.Image(self.Attributes['ImageFile'], {'height': '300px'})

        AbstractClasses.GeneralProductionOverview.GeneralProductionOverview.GenerateOverview(self)
        ROOT.gPad.SetLogy(0)
        return self.Boxed(HTML)

