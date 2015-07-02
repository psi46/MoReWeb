import ROOT
import AbstractClasses
import time
import datetime

class ProductionOverview(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def CustomInit(self):
        self.NameSingle='CumulativeProductionGraph'
        self.Name='CMSPixel_ProductionOverview_%s'%self.NameSingle
        self.Title = 'Cumulative Production Graph'
        self.DisplayOptions = {
            'Width': 2,
        }
        self.SavePlotFile = True
        self.SubPages = []

    def FetchData(self):

        Rows = AbstractClasses.GeneralProductionOverview.GeneralProductionOverview.FetchData(self)
        
        ModuleIDsList = []

        for RowTuple in Rows:
            if not RowTuple['ModuleID'] in ModuleIDsList:
                ModuleIDsList.append(RowTuple['ModuleID'])

        ## check if all grades are available
        FTMinus20BTC_Grades = []
        FTMinus20ATC_Grades = []
        FT17_Grades = []
        XrayCal_Grades = []
        XrayHR_Grades = []
        Final_Grades = []
        ModuleData = []

        for ModuleID in ModuleIDsList:
            Module = {}

            TestDates = []
            ModuleGrades = []

            FTMinus20BTC = ''
            FTMinus20ATC = ''
            FT17 = ''
            XrayCal = ''
            XrayHR = ''
            Complete = ''

            for RowTuple in Rows:
                if RowTuple['ModuleID']==ModuleID:
                    TestType = RowTuple['TestType']
                    TestDates.append(RowTuple['TestDate'])
                    if TestType == 'm20_1':
                        FTMinus20BTC = RowTuple['Grade'] if RowTuple['Grade'] is not None else ''
                        ModuleGrades.append(RowTuple['Grade'])
                    if TestType == 'm20_2':
                        FTMinus20ATC = RowTuple['Grade'] if RowTuple['Grade'] is not None else ''
                        ModuleGrades.append(RowTuple['Grade'])
                    if TestType == 'p17_1':
                        FT17 =  RowTuple['Grade'] if RowTuple['Grade'] is not None else ''
                        ModuleGrades.append(RowTuple['Grade'])
                    if TestType == 'XrayCalibration_Spectrum':
                        XrayCal = RowTuple['Grade'] if RowTuple['Grade'] is not None else ''
                        ModuleGrades.append(RowTuple['Grade'])
                    if TestType == 'XRayHRQualification':
                        XrayHR = RowTuple['Grade'] if RowTuple['Grade'] is not None else ''
                        ModuleGrades.append(RowTuple['Grade'])

            FinalGrade = 'None'
            if len(FTMinus20BTC) > 0 and len(FTMinus20ATC) > 0 and len(FT17) > 0 and len(XrayHR) > 0:
                if 'C' in ModuleGrades:
                    FinalGrade = 'C'
                elif 'B' in ModuleGrades:
                    FinalGrade = 'B'
                elif 'A' in ModuleGrades:
                    FinalGrade = 'A'

            Module['ModuleID'] = ModuleID
            Module['Grade'] = FinalGrade
            Module['TestDate'] = max(TestDates) #datetime.datetime.fromtimestamp(max(TestDates)).strftime("%Y-%m-%d %H:%m")
            ModuleData.append(Module)

        ModuleData.sort(key=lambda x: x['TestDate'], reverse=True)

        self.Attributes['ModuleData'] = ModuleData
        return ModuleData

    def CreatePlot(self):

        ModuleData = self.FetchData()
        
        TimestampBegin = min(ModuleData, key=lambda x: x['TestDate'])['TestDate']
        TimeBegin = datetime.datetime.fromtimestamp(TimestampBegin)
        YearBegin = int(TimeBegin.strftime("%Y"))
        WeekNumberBegin = int(TimeBegin.strftime("%W"))
        TimeBegin = datetime.datetime.strptime("%d-%d-1"%(YearBegin, WeekNumberBegin), '%Y-%W-%w')
        TimestampBegin = time.mktime(TimeBegin.timetuple())

        TimestampEnd = time.time() + 24*60*60
        TimeEnd = datetime.datetime.fromtimestamp(TimestampEnd)
        YearEnd = int(TimeEnd.strftime("%Y"))
        WeekNumberEnd = int(TimeEnd.strftime("%W"))
        TimeEnd = datetime.datetime.strptime("%d-%d-1"%(YearEnd, WeekNumberEnd), '%Y-%W-%w')
        TimestampEnd = time.mktime(TimeEnd.timetuple())

        SecondsPerDay = 24 * 60 * 60
        TimeOffset = TimestampBegin

        HistStack = ROOT.THStack("hs_cummulative_graph","")

        HistogramXMin = TimestampBegin - TimeOffset
        HistogramXMax = TimestampEnd - TimeOffset
        HistogramNBins = int((TimestampEnd - TimestampBegin)/SecondsPerDay)

        hA = ROOT.TH1D("h1ac", "", HistogramNBins, HistogramXMin, HistogramXMax)
        hB = ROOT.TH1D("h1bc", "", HistogramNBins, HistogramXMin, HistogramXMax)
        hC = ROOT.TH1D("h1cc", "", HistogramNBins, HistogramXMin, HistogramXMax)
        hN = ROOT.TH1D("h1nc", "", HistogramNBins, HistogramXMin, HistogramXMax)

        dh = ROOT.TDatime(int(TimeBegin.strftime("%Y")),int(TimeBegin.strftime("%m")),int(TimeBegin.strftime("%d")),00,00,00)
        hA.SetLineColor(ROOT.kBlue)
        hB.SetLineColor(ROOT.kBlack)
        hC.SetLineColor(ROOT.kRed)
        hN.SetLineColor(ROOT.kMagenta)

        for Module in ModuleData:
            if Module['Grade'] == 'A':
                hA.Fill(Module['TestDate'] - TimeOffset)
            elif Module['Grade'] == 'B':
                hB.Fill(Module['TestDate'] - TimeOffset)
            elif Module['Grade'] == 'C':
                hC.Fill(Module['TestDate'] - TimeOffset)
            else:
                hN.Fill(Module['TestDate'] - TimeOffset)

        hA = hA.GetCumulative()
        hB = hB.GetCumulative()
        hC = hC.GetCumulative()
        hN = hN.GetCumulative()

        hA.GetXaxis().SetTimeDisplay(1)
        hA.GetXaxis().SetTimeOffset(dh.Convert())
        hA.GetXaxis().SetLabelOffset(0.035)
        hA.GetXaxis().SetTimeFormat("#splitline{%m-%d}{ %Y}")
        hA.GetYaxis().SetTitle("# modules")
        hA.GetYaxis().SetTitleOffset(0.7)
        hA.GetYaxis().SetRangeUser(0, 1.05*max([hA.GetMaximum(),hB.GetMaximum(),hC.GetMaximum(),hN.GetMaximum()]))

        ROOT.gStyle.SetOptStat(0)

        hA.Draw()
        hB.Draw("same")
        hC.Draw("same")
        hN.Draw("same")

        title = ROOT.TText()
        title.SetNDC()
        title.SetTextAlign(12)
        title.SetTextColor(ROOT.kBlue)
        title.DrawText(0.15,0.965,"Grade A")

        title2 = ROOT.TText()
        title2.SetNDC()
        title2.SetTextAlign(12)
        title2.SetTextColor(ROOT.kBlack)
        title2.DrawText(0.30,0.965,"Grade B")

        title3 = ROOT.TText()
        title3.SetNDC()
        title3.SetTextAlign(12)
        title3.SetTextColor(ROOT.kRed)
        title3.DrawText(0.45,0.965,"Grade C")

        title4 = ROOT.TText()
        title4.SetNDC()
        title4.SetTextAlign(12)
        title4.SetTextColor(ROOT.kMagenta)
        title4.DrawText(0.60,0.965,"incomplete")

        self.SaveCanvas()

    def GenerateOverview(self):
        self.CreatePlot()

        HTML = self.Image(self.Attributes['ImageFile'])
        return self.Boxed(HTML)

