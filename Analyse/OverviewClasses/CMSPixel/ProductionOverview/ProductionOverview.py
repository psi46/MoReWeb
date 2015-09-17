import ROOT
import AbstractClasses
import datetime
import time
from operator import attrgetter
import ConfigParser

class ProductionOverview(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def CustomInit(self, TestResultEnvironmentObject = 0):
        if TestResultEnvironmentObject:
            self.TestResultEnvironmentObject = TestResultEnvironmentObject
        self.HTMLFileName = 'ProductionOverview.html'
        self.ImportPath = 'OverviewClasses.CMSPixel.ProductionOverview'
        self.NameSingle = 'ProductionOverview'
        self.Name = 'CMSPixel_%s'%self.NameSingle
        self.Attributes['StorageKey'] = self.NameSingle
        self.SaveHTML = True

        SysConfiguration = ConfigParser.ConfigParser()
        SysConfiguration.read(['Configuration/ProductionOverview.cfg'])

        try:
            self.ModuleQualificationFinalDate = SysConfiguration.get('ProductionOverview','ModuleQualificationFinalDate').lower()
            if self.ModuleQualificationFinalDate not in ['first', 'last']:
                self.ModuleQualificationFinalDate = 'last'
        except:
            self.ModuleQualificationFinalDate = 'last'

        if int(SysConfiguration.get('ProductionOverview','GenerateTotalOverview'))>0:
            self.SubPages.append(
                {
                    "Key": "ProductionOverviewPage_Total",
                    "Module": "ProductionOverviewPage",
                    "InitialAttributes" : {
                        "StorageKey" : "ProductionOverviewPage_Total",
                        "ShowWeeklyPlots": "True",
                        "Title" : "Total production Overview",
                    },
                }
            )

        if int(SysConfiguration.get('ProductionOverview','GenerateWeeklyOverviews'))>0:

            ISOCal = datetime.date.today().isocalendar()
            YearNow = ISOCal[0]
            WeekNow = ISOCal[1]

            Rows = self.FetchData()

            FirstTestTimestamp = time.time()

            for Row in Rows:
                if Row['TestDate'] < FirstTestTimestamp:
                    FirstTestTimestamp = Row['TestDate']

            FirstTestDatetime = datetime.datetime.fromtimestamp(FirstTestTimestamp)
            FirstTestICOCal = FirstTestDatetime.isocalendar()
            YearFirst = FirstTestICOCal[0]
            WeekFirst = FirstTestICOCal[1]

            YearWeeks = []

            if YearFirst==YearNow:
                for Week in range(WeekFirst, WeekNow+1):
                    YearWeeks.append([YearNow, Week])
            else:
                # first add weeks of the first year
                IsoWeeksInYear = datetime.date(YearFirst, 12, 28).isocalendar()[1] #last iso week contains 28th of december
                for Week in range(WeekFirst, IsoWeeksInYear+1):
                    YearWeeks.append([YearFirst, Week])

                for Year in range(YearFirst+1, YearNow):
                    IsoWeeksInYear = datetime.date(Year, 12, 28).isocalendar()[1] #last iso week contains 28th of december
                    for Week in range(1, IsoWeeksInYear+1):
                        YearWeeks.append([Year, Week])

                # current year
                for Week in range(1, WeekNow+1):
                    YearWeeks.append([YearNow, Week])

            YearWeeks.reverse()

            # add allweekly summaries
            for YearWeek in YearWeeks:
                self.SubPages.append(
                    {
                        "Key": "ProductionOverviewPage_Week%s_%s"%(YearWeek[0],YearWeek[1]),
                        "Module": "ProductionOverviewPage",
                        "InitialAttributes" : {
                            "StorageKey" : "ProductionOverviewPage_Total%s_%s"%(YearWeek[0],YearWeek[1]),
                            "Title" : "Overview week %d/%d"%(YearWeek[1],YearWeek[0]),
                            "DateBegin" : self.iso_to_gregorian(YearWeek[0], YearWeek[1], 1),
                            "DateEnd" : self.iso_to_gregorian(YearWeek[0], YearWeek[1], 1) + datetime.timedelta(days=7) - datetime.timedelta(seconds=1),
                            "ShowWeeklyPlots": False,
                         },
                    }
                )


    def GenerateOverview(self):
        AbstractClasses.GeneralProductionOverview.GeneralProductionOverview.GenerateOverview(self)
        return ""