import ROOT
import AbstractClasses
import time
import datetime

class ProductionOverview(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def CustomInit(self):
        self.Name='CMSPixel_ProductionOverview_WeeklyProduction'
        self.NameSingle='WeeklyProduction'
        self.Title = 'Weekly Production A/B/C'
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
        
        ### list of modules tested
        ModuleIDsList = self.GetModuleIDsList(Rows)

        ## check if all grades are available
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
            SecondsPerWeek = 7 * 24 * 60 * 60
            TimestampBegin = min(ModuleData, key=lambda x: x['TestDate'])['TestDate']
            TimeBegin = datetime.datetime.fromtimestamp(TimestampBegin)

            YearBegin = TimeBegin.isocalendar()[0]
            WeekNumberBegin = TimeBegin.isocalendar()[1]
            TimeBegin = self.iso_to_gregorian(YearBegin, WeekNumberBegin, 1)
            TimestampBegin = time.mktime(TimeBegin.timetuple())

            TimestampNow = time.time()
            TimeEnd = datetime.datetime.fromtimestamp(TimestampNow) + datetime.timedelta(days=1) - datetime.timedelta(seconds=1)

            YearEnd = TimeEnd.isocalendar()[0]
            WeekNumberEnd = TimeEnd.isocalendar()[1]
            TimeEnd = self.iso_to_gregorian(YearEnd, WeekNumberEnd, 1) + datetime.timedelta(days=7) - datetime.timedelta(seconds=1)
            TimestampEnd = time.mktime(TimeEnd.timetuple())

            TimeOffset = TimestampBegin

            HistStack = ROOT.THStack("hs_weekly_production%s"%self.GetUniqueID(),"")
            NBins = int((TimestampEnd - TimestampBegin)/SecondsPerWeek)
            LeftEdge = TimestampBegin - TimeOffset
            RightEdge = TimestampEnd - TimeOffset

            hA = ROOT.TH1D("h1a", "h1-a_%s"%self.GetUniqueID(), NBins, LeftEdge, RightEdge)
            hB = ROOT.TH1D("h1b", "h1-b_%s"%self.GetUniqueID(), NBins, LeftEdge, RightEdge)
            hC = ROOT.TH1D("h1c", "h1-c_%s"%self.GetUniqueID(), NBins, LeftEdge, RightEdge)
            hN = ROOT.TH1D("h1n", "h1-n_%s"%self.GetUniqueID(), NBins, LeftEdge, RightEdge)

            dh = ROOT.TDatime(int(TimeBegin.strftime("%Y")),int(TimeBegin.strftime("%m")),int(TimeBegin.strftime("%d")),00,00,00)
            hA.SetFillStyle(1001)
            hA.SetFillColor(self.GetGradeColor('A'))
            hB.SetFillStyle(1001)
            hB.SetFillColor(self.GetGradeColor('B'))
            hC.SetFillStyle(1001)
            hC.SetFillColor(self.GetGradeColor('C'))
            hN.SetFillStyle(1001)
            hN.SetFillColor(self.GetGradeColor('None'))

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

            HistStack.Add(hA)
            HistStack.Add(hB)
            HistStack.Add(hC)
            HistStack.Add(hN)

            HistStack.Draw()
            HistStack.GetXaxis().SetTimeDisplay(1)
            HistStack.GetXaxis().SetTimeOffset(dh.Convert())
            HistStack.GetXaxis().SetLabelOffset(0.05)
            HistStack.GetXaxis().SetTimeFormat("#splitline{%m-%d}{ %Y}")
            HistStack.GetXaxis().SetTitle("")
            HistStack.GetXaxis().SetTitleOffset(1)
            HistStack.GetYaxis().SetTitle("# modules")
            HistStack.GetYaxis().SetTitleOffset(0.7)

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
        else:
            title4 = ROOT.TText()
            title4.SetNDC()
            title4.SetTextAlign(12)
            title4.SetTextColor(self.GetGradeColor('None'))
            title4.DrawText(0.60,0.965,"no modules found")


        self.SaveCanvas()

    def GenerateOverview(self):
        self.CreatePlot()

        HTML = self.Image(self.Attributes['ImageFile'])
        return self.Boxed(HTML)

