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

        # always show the full available data, but draw marker around selected period
        self.Attributes['DateBeginMarker'] = self.Attributes['DateBegin']
        self.Attributes['DateEndMarker'] = self.Attributes['DateEnd']
        self.Attributes['DateBegin'] = None
        self.Attributes['DateEnd'] = None
        Rows = AbstractClasses.GeneralProductionOverview.GeneralProductionOverview.FetchData(self)
        
        # create list of module ids
        ModuleIDsList = []
        for RowTuple in Rows:
            if not RowTuple['ModuleID'] in ModuleIDsList:
                ModuleIDsList.append(RowTuple['ModuleID'])

        # check if all grades are available
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
            LeakageCurrent = ''

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
                    if TestType == 'LeakageCurrentPON':
                        LeakageCurrent = RowTuple['Grade'] if RowTuple['Grade'] is not None else ''
                        ModuleGrades.append(RowTuple['Grade'])


            FinalGrade = 'None'
            if len(FTMinus20BTC) > 0 and len(FTMinus20ATC) > 0 and len(FT17) > 0 and len(XrayHR) > 0:
                if 'C' in ModuleGrades:
                    FinalGrade = 'C'
                elif 'B' in ModuleGrades:
                    FinalGrade = 'B'
                elif 'A' in ModuleGrades:
                    FinalGrade = 'A'

            # only use leakage current grade as final grade if it is C
            if len(LeakageCurrent) > 0:
                if LeakageCurrent.upper() == 'C':
                    FinalGrade = 'C'

            Module['ModuleID'] = ModuleID
            Module['Grade'] = FinalGrade
            Module['TestDate'] = max(TestDates) #datetime.datetime.fromtimestamp(max(TestDates)).strftime("%Y-%m-%d %H:%m")
            ModuleData.append(Module)

        ModuleData.sort(key=lambda x: x['TestDate'], reverse=True)

        self.Attributes['ModuleData'] = ModuleData
        return ModuleData

    def CreatePlot(self):

        ModuleData = self.FetchData()
       
        if len(ModuleData) > 0:

            # get first day of the week in which the first test was done
            SecondsPerDay = 24 * 60 * 60
            SecondsPerWeek = 7 * SecondsPerDay
            TimestampBegin = min(ModuleData, key=lambda x: x['TestDate'])['TestDate']
            TimeBegin = datetime.datetime.fromtimestamp(TimestampBegin)
            YearBegin = TimeBegin.isocalendar()[0]
            WeekNumberBegin = TimeBegin.isocalendar()[1]
            TimeBegin = self.iso_to_gregorian(YearBegin, WeekNumberBegin, 1)
            TimestampBegin = time.mktime(TimeBegin.timetuple())

            # get last day of the current week
            TimestampNow = time.time()
            TimeEnd = datetime.datetime.fromtimestamp(TimestampNow) + datetime.timedelta(days=1) - datetime.timedelta(seconds=1)
            YearEnd = TimeEnd.isocalendar()[0]
            WeekNumberEnd = TimeEnd.isocalendar()[1]
            TimeEnd = self.iso_to_gregorian(YearEnd, WeekNumberEnd, 1) + datetime.timedelta(days=7) - datetime.timedelta(seconds=1)
            TimestampEnd = time.mktime(TimeEnd.timetuple())
            TimeOffset = TimestampBegin

            HistStack = ROOT.THStack("hs_cummulative_graph","")

            HistogramXMin = TimestampBegin - TimeOffset
            HistogramXMax = TimestampEnd - TimeOffset
            HistogramNBins = int((TimestampEnd - TimestampBegin)/SecondsPerDay)

            hA = ROOT.TH1D("h1ac%s"%self.GetUniqueID(), "", HistogramNBins, HistogramXMin, HistogramXMax)
            hB = ROOT.TH1D("h1bc%s"%self.GetUniqueID(), "", HistogramNBins, HistogramXMin, HistogramXMax)
            hC = ROOT.TH1D("h1cc%s"%self.GetUniqueID(), "", HistogramNBins, HistogramXMin, HistogramXMax)
            hN = ROOT.TH1D("h1nc%s"%self.GetUniqueID(), "", HistogramNBins, HistogramXMin, HistogramXMax)

            dh = ROOT.TDatime(int(TimeBegin.strftime("%Y")),int(TimeBegin.strftime("%m")),int(TimeBegin.strftime("%d")),00,00,00)
            hA.SetLineColor(self.GetGradeColor('A'))
            hB.SetLineColor(self.GetGradeColor('B'))
            hC.SetLineColor(self.GetGradeColor('C'))
            hN.SetLineColor(self.GetGradeColor('None'))

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
            title.SetTextColor(self.GetGradeColor('A'))
            title.DrawText(0.15,0.965,"Grade A")

            title2 = ROOT.TText()
            title2.SetNDC()
            title2.SetTextAlign(12)
            title2.SetTextColor(self.GetGradeColor('B'))
            title2.DrawText(0.30,0.965,"Grade B")

            title3 = ROOT.TText()
            title3.SetNDC()
            title3.SetTextAlign(12)
            title3.SetTextColor(self.GetGradeColor('C'))
            title3.DrawText(0.45,0.965,"Grade C")

            title4 = ROOT.TText()
            title4.SetNDC()
            title4.SetTextAlign(12)
            title4.SetTextColor(self.GetGradeColor('None'))
            title4.DrawText(0.60,0.965,"incomplete")

        self.SaveCanvas()

    def GenerateOverview(self):
        self.CreatePlot()

        HTML = self.Image(self.Attributes['ImageFile'])
        return self.Boxed(HTML)

