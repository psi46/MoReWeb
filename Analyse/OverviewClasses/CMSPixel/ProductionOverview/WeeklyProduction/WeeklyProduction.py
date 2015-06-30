import ROOT
import AbstractClasses
import time
import datetime

class ProductionOverview(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def CustomInit(self):
    	self.Name='WeeklyProduction'
    	self.NameSingle='WeeklyProduction'
        self.Title = 'Weekly Production A/B/C'
        self.DisplayOptions = {
            'Width': 2,
        }
        self.SavePlotFile = True
        self.SubPages = []

    def FetchData(self):

        Rows = AbstractClasses.GeneralProductionOverview.GeneralProductionOverview.FetchData(self)
        
        ModuleIDsList = []

        for RowTuple in Rows:
            #print repr(RowTuple)
            if not RowTuple['ModuleID'] in ModuleIDsList:
                ModuleIDsList.append(RowTuple['ModuleID'])

        ModuleData = []

        for ModuleID in ModuleIDsList:
            Module = {}

            TestDates = []
            Grades = []

            for RowTuple in Rows:
                if RowTuple['ModuleID'] == ModuleID:
                    TestDates.append(RowTuple['TestDate'])
                    Grades.append(RowTuple['Grade'])

            FinalModuleGrade = 'None'
            if 'C' in Grades:
                FinalModuleGrade = 'C'
            elif 'B' in Grades:
                FinalModuleGrade = 'B'
            elif 'A' in Grades:
                FinalModuleGrade = 'A'

            Module['ModuleID'] = ModuleID
            Module['Grade'] = FinalModuleGrade
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

        SecondsPerWeek = 7 * 24 * 60 * 60
        TimeOffset = TimestampBegin

        HistStack = ROOT.THStack("hs_weekly_production","")

        hA = ROOT.TH1D("h1a", "h1-a", int((TimestampEnd - TimestampBegin)/SecondsPerWeek), TimestampBegin - TimeOffset, TimestampEnd - TimeOffset)
        hB = ROOT.TH1D("h1b", "h1-b", int((TimestampEnd - TimestampBegin)/SecondsPerWeek), TimestampBegin - TimeOffset, TimestampEnd - TimeOffset)
        hC = ROOT.TH1D("h1c", "h1-c", int((TimestampEnd - TimestampBegin)/SecondsPerWeek), TimestampBegin - TimeOffset, TimestampEnd - TimeOffset)
        hN = ROOT.TH1D("h1n", "h1-n", int((TimestampEnd - TimestampBegin)/SecondsPerWeek), TimestampBegin - TimeOffset, TimestampEnd - TimeOffset)

        dh = ROOT.TDatime(int(TimeBegin.strftime("%Y")),int(TimeBegin.strftime("%m")),int(TimeBegin.strftime("%d")),00,00,00)
        hA.SetFillStyle(1001)
        hA.SetFillColor(ROOT.kBlue)
        hB.SetFillStyle(1001)
        hB.SetFillColor(ROOT.kBlack)
        hC.SetFillStyle(1001)
        hC.SetFillColor(ROOT.kRed)
        hN.SetFillStyle(1001)
        hN.SetFillColor(ROOT.kMagenta)

        for Module in ModuleData:
            if Module['Grade'] == 'A':
                hA.Fill(Module['TestDate'] - TimeOffset)
            elif Module['Grade'] == 'B':
                hB.Fill(Module['TestDate'] - TimeOffset)
            elif Module['Grade'] == 'C':
                hC.Fill(Module['TestDate'] - TimeOffset)
            else:
                hN.Fill(Module['TestDate'] - TimeOffset)

        HistStack.Add(hA)
        HistStack.Add(hB)
        HistStack.Add(hC)
        HistStack.Add(hN)

        HistStack.Draw()
        HistStack.GetXaxis().SetTimeDisplay(1)
        HistStack.GetXaxis().SetTimeOffset(dh.Convert())
        HistStack.GetXaxis().SetLabelOffset(0.02)
        HistStack.GetXaxis().SetTimeFormat("%y-%W")

        self.SaveCanvas()

    def GenerateOverview(self):
        self.CreatePlot()

        HTML = self.Image(self.Attributes['ImageFile'])
        return self.Boxed(HTML)

