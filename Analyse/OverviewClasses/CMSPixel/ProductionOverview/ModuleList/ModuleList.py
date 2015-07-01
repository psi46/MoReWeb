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

            for RowTuple in Rows:
                if RowTuple['ModuleID']==ModuleID:
                    TestType = RowTuple['TestType']
                    if TestType == 'm20_1':
                        FTMinus20BTC = self.DateFromTimestamp(RowTuple['TestDate'])
                        ModuleGrades.append(RowTuple['Grade'])
                    if TestType == 'm20_2':
                        FTMinus20ATC = self.DateFromTimestamp(RowTuple['TestDate'])
                        ModuleGrades.append(RowTuple['Grade'])
                    if TestType == 'p17_1':
                        FT17 = self.DateFromTimestamp(RowTuple['TestDate'])
                        ModuleGrades.append(RowTuple['Grade'])
                    if TestType == 'XrayCalibration_Spectrum':
                        XrayCal = self.DateFromTimestamp(RowTuple['TestDate'])
                        ModuleGrades.append(RowTuple['Grade'])
                    if TestType == 'XRayHRQualification':
                        XrayHR = self.DateFromTimestamp(RowTuple['TestDate'])
                        ModuleGrades.append(RowTuple['Grade'])
                    if TestType == 'LeakageCurrentPON':
                        LCTest = self.DateFromTimestamp(RowTuple['TestDate'])
                        ModuleGrades.append(RowTuple['Grade'])

            if len(FTMinus20BTC) > 0 and len(FTMinus20ATC) > 0 and len(FT17) > 0 and len(XrayHR) > 0:
                if len(XrayCal) > 0:
                    Complete = '<div style="text-align:center;" title="FullQualification, HR Test and Calibration done">&#x2713;</div>'
                if 'C' in ModuleGrades:
                    FinalGrade = 'C'
                elif 'B' in ModuleGrades:
                    FinalGrade = 'B'
                elif 'A' in ModuleGrades:
                    FinalGrade = 'A'

            TableData.append(
                [
                    ModuleID, Complete, FinalGrade, LCTest, FTMinus20BTC, FTMinus20ATC, FT17, XrayCal, XrayHR
                ]
            )

        RowLimit = 9
        HTML = self.Table(TableData, RowLimit)

        return self.Boxed(HTML)

