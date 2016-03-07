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
            'Width': 2.5,
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

            for RowTuple in Rows:
                if RowTuple['ModuleID']==ModuleID:
                    TestDates.append(RowTuple['TestDate'])

            FinalGrade = 'None'
            if self.ModuleQualificationIsComplete(ModuleID, Rows):
                FinalGrade = self.GetFinalGrade(ModuleID, Rows)

            Module['ModuleID'] = ModuleID
            Module['Grade'] = FinalGrade
            if self.ParentObject.ParentObject.ModuleQualificationFinalDate == 'first':
                Module['TestDate'] = min(TestDates)
            else:
                Module['TestDate'] = max(TestDates)
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
                try:
                    relativeTestDate = float(Module['TestDate']) - TimeOffset
                    if Module['Grade'] == 'A':
                        hA.Fill(relativeTestDate)
                    elif Module['Grade'] == 'B':
                        hB.Fill(relativeTestDate)
                    elif Module['Grade'] == 'C':
                        hC.Fill(relativeTestDate)
                    else:
                        hN.Fill(relativeTestDate)
                except:
                    print "could not fill in module: ", Module['ModuleID']

            hA = self.GetCumulative(hA)
            hB = self.GetCumulative(hB)
            hC = self.GetCumulative(hC)
            hN = self.GetCumulative(hN)

            hA.GetXaxis().SetTimeDisplay(1)
            hA.GetXaxis().SetTimeOffset(dh.Convert())
            hA.GetXaxis().SetLabelOffset(0.035)
            hA.GetXaxis().SetTimeFormat("#splitline{%m-%d}{ %Y}")
            hA.GetYaxis().SetTitle("# modules")
            hA.GetYaxis().SetTitleOffset(0.7)

            ROOT.gStyle.SetOptStat(0)

            if 'AddAB' in self.Attributes and self.Attributes['AddAB']:
                hA.Add(hB)
                hA.GetYaxis().SetRangeUser(0, 1.05*max([hA.GetMaximum(),hC.GetMaximum(),hN.GetMaximum()]))
                hA.Draw()
            else:
                hA.GetYaxis().SetRangeUser(0, 1.05*max([hA.GetMaximum(),hB.GetMaximum(),hC.GetMaximum(),hN.GetMaximum()]))
                hA.Draw()
                hB.Draw("same")

            hC.Draw("same")
            hN.Draw("same")

            title = ROOT.TText()
            title.SetNDC()
            title.SetTextAlign(12)
            title.SetTextColor(self.GetGradeColor('A'))

            if 'AddAB' in self.Attributes and self.Attributes['AddAB']:
                title.DrawText(0.15,0.965,"Grade A+B")            
            else:
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

