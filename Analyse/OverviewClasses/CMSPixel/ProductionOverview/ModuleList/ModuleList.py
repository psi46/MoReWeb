import ROOT
import AbstractClasses

class ProductionOverview(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def CustomInit(self):
    	self.Name='CMSPixel_ProductionOverview_ModuleList'
    	self.NameSingle='ModuleList'
        self.Title = 'Test overview'
        self.DisplayOptions = {
            'Width': 4,
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
                {'Class' : 'Header', 'Value' : 'Module'}, {'Class' : 'Header', 'Value' : 'OK'}, {'Class' : 'Header', 'Value' : 'LeakageCurrentPON'}, {'Class' : 'Header', 'Value' : 'FullTest@-20 BTC'}, {'Class' : 'Header', 'Value' : 'FullTest@-20 ATC'}, {'Class' : 'Header', 'Value' : 'FullTest@17'}, {'Class' : 'Header', 'Value' : 'X-ray Calibration'}, {'Class' : 'Header', 'Value' : 'X-ray HighRate'}
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

            for RowTuple in Rows:
                if RowTuple['ModuleID']==ModuleID:
                    TestType = RowTuple['TestType']
                    if TestType == 'm20_1':
                        FTMinus20BTC = self.DateFromTimestamp(RowTuple['TestDate'])
                    if TestType == 'm20_2':
                        FTMinus20ATC = self.DateFromTimestamp(RowTuple['TestDate'])
                    if TestType == 'p17_1':
                        FT17 = self.DateFromTimestamp(RowTuple['TestDate'])
                    if TestType == 'XrayCalibration_Spectrum':
                        XrayCal = self.DateFromTimestamp(RowTuple['TestDate'])
                    if TestType == 'XRayHRQualification':
                        XrayHR = self.DateFromTimestamp(RowTuple['TestDate'])
                    if TestType == 'LeakageCurrentPON':
                        LCTest = self.DateFromTimestamp(RowTuple['TestDate'])

            if len(FTMinus20BTC) > 0 and len(FTMinus20ATC) > 0 and len(FT17) > 0 and len(XrayCal) > 0 and len(XrayHR) > 0:
                Complete = '&#x2713;'

            TableData.append(
                [
                    ModuleID, Complete, LCTest, FTMinus20BTC, FTMinus20ATC, FT17, XrayCal, XrayHR
                ]
            )

        HTML = self.Table(TableData)

        return self.Boxed(HTML)

