import ROOT
import AbstractClasses

class ProductionOverview(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def CustomInit(self):
    	self.Name='CMSPixel_ProductionOverview_NumberSummary'
    	self.NameSingle='NumberSummary'
        self.Title = 'Summary'
        self.DisplayOptions = {
            'Width': 1,
        }
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
            Module['TestDate'] = max(TestDates)
            ModuleData.append(Module)

        ModuleData.sort(key=lambda x: x['TestDate'], reverse=True)

        self.Attributes['ModuleData'] = ModuleData
        return ModuleData

    def GenerateOverview(self):

        ModuleData = self.FetchData()

        TableData = [
            [
                {'Class' : 'Header', 'Value' : 'Tested modules:'}, {'Class' : 'Value', 'Value' : "%d"%len(ModuleData)}
            ],
            [
                {'Class' : 'Header', 'Value' : 'Grade A:'}, {'Class' : 'Value', 'Value' : "%d"%len([x for x in ModuleData if x['Grade'] == 'A'])}
            ],
            [
                {'Class' : 'Header', 'Value' : 'Grade B:'}, {'Class' : 'Value', 'Value' : "%d"%len([x for x in ModuleData if x['Grade'] == 'B'])}
            ],
            [
                {'Class' : 'Header', 'Value' : 'Grade C:'}, {'Class' : 'Value', 'Value' : "%d"%len([x for x in ModuleData if x['Grade'] == 'C'])}
            ],
        ]
        HTML = self.Table(TableData)

        return self.Boxed(HTML)

