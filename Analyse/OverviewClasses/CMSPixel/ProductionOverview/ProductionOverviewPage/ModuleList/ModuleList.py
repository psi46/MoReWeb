import ROOT
import AbstractClasses

class ProductionOverview(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def CustomInit(self):
    	self.Name='CMSPixel_ProductionOverview_ModuleList'
    	self.NameSingle='ModuleList'
        self.Title = 'Test overview'
        self.DisplayOptions = {
            'Width': 5,
        }
        self.SubPages = []

    def GenerateOverview(self):

        TableData = []
        Rows = self.FetchData()

        ModuleIDsList = []
        for RowTuple in Rows:
            if not RowTuple['ModuleID'] in ModuleIDsList:
                ModuleIDsList.append(RowTuple['ModuleID'])
        ModuleIDsList.sort(reverse=True)

        TableData.append(    
            [
                {'Class' : 'Header', 'Value' : 'Module'}, {'Class' : 'Header', 'Value' : 'Testing complete'}, {'Class' : 'Header', 'Value' : 'Grade'}, {'Class' : 'Header', 'Value' : 'LeakageCurrentPON'}, {'Class' : 'Header', 'Value' : 'FullTest@-20 BTC'}, {'Class' : 'Header', 'Value' : 'FullTest@-20 ATC'}, {'Class' : 'Header', 'Value' : 'FullTest@17'}, {'Class' : 'Header', 'Value' : 'X-ray Calibration'}, {'Class' : 'Header', 'Value' : 'X-ray HighRate'}
            ]
        )

        for ModuleID in ModuleIDsList:

            LCTest = ''
            FTMinus20BTC = ''
            FTMinus20ATC = ''
            FT17 = ''
            XrayCal = ''
            XrayHR = ''
            Complete = ''
            FinalGrade = 'None'
            ModuleGrades = []
            LCGrade = ''

            for RowTuple in Rows:
                if RowTuple['ModuleID']==ModuleID:
                    TestType = RowTuple['TestType']
                    Url = '../../' + RowTuple['RelativeModuleFinalResultsPath'] + '/' + RowTuple['FulltestSubfolder'] + '/TestResult.html'

                    if TestType == 'm20_1':
                        FTMinus20BTC = "<a href='{url}'>{text}</a>".format(text=self.DateFromTimestamp(RowTuple['TestDate']), url=Url)
                    if TestType == 'm20_2':
                        FTMinus20ATC = "<a href='{url}'>{text}</a>".format(text=self.DateFromTimestamp(RowTuple['TestDate']), url=Url)
                    if TestType == 'p17_1':
                        FT17 = "<a href='{url}'>{text}</a>".format(text=self.DateFromTimestamp(RowTuple['TestDate']), url=Url)
                    if TestType == 'XrayCalibration_Spectrum':
                        XrayCal = "<a href='{url}'>{text}</a>".format(text=self.DateFromTimestamp(RowTuple['TestDate']), url=Url)
                    if TestType == 'XRayHRQualification':
                        XrayHR = "<a href='{url}'>{text}</a>".format(text=self.DateFromTimestamp(RowTuple['TestDate']), url=Url)
                    if TestType == 'LeakageCurrentPON':
                        LCTest = "<a href='{url}'>{text}</a>".format(text=self.DateFromTimestamp(RowTuple['TestDate']), url=Url)
                        ModuleGrades.append(RowTuple['Grade'])
                        LCGrade = RowTuple['Grade']

            if LCGrade == 'C':
                Complete = '<div style="text-align:center;color:#999;" title="Grade C due to high leakage current">&#x2713;</div>'
                FinalGrade = 'C'
            elif self.ModuleQualificationIsComplete(ModuleID, Rows):
                Complete = '<div style="text-align:center;" title="FullQualification, HR Test and Calibration done">&#x2713;</div>'
                FinalGrade = self.GetFinalGrade(ModuleID, Rows)


            TableData.append(
                [
                    ModuleID, Complete, FinalGrade, LCTest, FTMinus20BTC, FTMinus20ATC, FT17, XrayCal, XrayHR
                ]
            )

        RowLimit = 9
        HTML = self.Table(TableData, RowLimit)

        return self.Boxed(HTML)

