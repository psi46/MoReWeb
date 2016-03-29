import ROOT
import AbstractClasses
import time

class ProductionOverview(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def CustomInit(self):
        self.Name='CMSPixel_ProductionOverview_GradingOverview'
        self.NameSingle='GradingOverview'
        self.Title = 'Grading overview'
        self.DisplayOptions = {
            'Width': 2.5,
        }
        self.SubPages = []

    def GenerateOverview(self):

        TableData = []

        Rows = self.FetchData()
        ModuleIDsList = self.GetModuleIDsList(Rows)
        ModuleIDsList.sort(reverse=True)

        FTMinus20BTC_Grades = []
        FTMinus20ATC_Grades = []
        FT17_Grades = []
        XrayCal_Grades = []
        XrayHR_Grades = []
        FullQualification_Grades = []
        Final_Grades = []

        for ModuleID in ModuleIDsList:

            FTMinus20BTC = ''
            FTMinus20ATC = ''
            FT17 = ''
            XrayCal = ''
            XrayHR = ''
            Complete = ''

            ModuleGrades = []

            for RowTuple in Rows:
                if RowTuple['ModuleID']==ModuleID:
                    TestType = RowTuple['TestType']
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


            if self.ModuleQualificationIsComplete(ModuleID, Rows):
                FinalGrade = self.GetFinalGrade(ModuleID, Rows)
                Final_Grades.append(FinalGrade)

            FTMinus20BTC_Grades.append(FTMinus20BTC)
            FTMinus20ATC_Grades.append(FTMinus20ATC)
            FT17_Grades.append(FT17)

            if 'C' in [FTMinus20BTC, FTMinus20ATC, FT17]:
                FullQualification_Grades.append('C')
            elif 'B' in [FTMinus20BTC, FTMinus20ATC, FT17]:
                FullQualification_Grades.append('B')
            elif 'A' in [FTMinus20BTC, FTMinus20ATC, FT17]:
                FullQualification_Grades.append('A')

            XrayCal_Grades.append(XrayCal)
            XrayHR_Grades.append(XrayHR)

        TableData = [
            [{'Class' : 'Header', 'Value' : 'Tested modules:'}, {'Class' : 'Value', 'Value' : "%d"%len(ModuleIDsList)}],
            [{'Class' : 'Header', 'Value' : 'Qualification complete*:'}, {'Class' : 'Value', 'Value' : "%d"%len(Final_Grades)}],
        ]
        HTML = self.Table(TableData)

        TableData = []
        TableData.append(    
            [
                {'Class' : 'Header', 'Value' : 'Grade'}, {'Class' : 'Header', 'Value' : 'A'}, {'Class' : 'Header', 'Value' : 'B'}, {'Class' : 'Header', 'Value' : 'C'}
            ]
        )

        ### Full Qualification
        TableData.append(
            [{'Class' : 'Value', 'Value' : 'T = -20 BTC'}, {'Class' : 'Value', 'Value' : "%d"%len([x for x in FTMinus20BTC_Grades if x=='A']) }, {'Class' : 'Value', 'Value' : "%d"%len([x for x in FTMinus20BTC_Grades if x=='B']) }, {'Class' : 'Value', 'Value' : "%d"%len([x for x in FTMinus20BTC_Grades if x=='C']) }]
        )
        TableData.append(
            [{'Class' : 'Value', 'Value' : 'T = -20 ATC'}, {'Class' : 'Value', 'Value' : "%d"%len([x for x in FTMinus20ATC_Grades if x=='A']) }, {'Class' : 'Value', 'Value' : "%d"%len([x for x in FTMinus20ATC_Grades if x=='B']) }, {'Class' : 'Value', 'Value' : "%d"%len([x for x in FTMinus20ATC_Grades if x=='C']) }]
        )
        TableData.append(
            [{'Class' : 'Value', 'Value' : 'T = +17 ATC'}, {'Class' : 'Value', 'Value' : "%d"%len([x for x in FT17_Grades if x=='A']) }, {'Class' : 'Value', 'Value' : "%d"%len([x for x in FT17_Grades if x=='B']) }, {'Class' : 'Value', 'Value' : "%d"%len([x for x in FT17_Grades if x=='C']) }]
        )

        TableData.append(
            [{'Class' : 'Value', 'Value' : 'FullQualification'}, {'Class' : 'Value', 'Value' : "%d"%len([x for x in FullQualification_Grades if x=='A']) }, {'Class' : 'Value', 'Value' : "%d"%len([x for x in FullQualification_Grades if x=='B']) }, {'Class' : 'Value', 'Value' : "%d"%len([x for x in FullQualification_Grades if x=='C']) }]
        )
        ### X-ray
        TableData.append(    
            [{'Class' : 'Value', 'Value' : 'High Rate'}, {'Class' : 'Value', 'Value' : "%d"%len([x for x in XrayHR_Grades if x=='A']) }, {'Class' : 'Value', 'Value' : "%d"%len([x for x in XrayHR_Grades if x=='B']) }, {'Class' : 'Value', 'Value' : "%d"%len([x for x in XrayHR_Grades if x=='C']) }]
        )

        ### Final
        TableData.append(    
            [{'Class' : 'Header', 'Value' : '<div title="all tests completed">Final</div>'}, {'Class' : 'Value', 'Value' : "%d"%len([x for x in Final_Grades if x=='A']) }, {'Class' : 'Value', 'Value' : "%d"%len([x for x in Final_Grades if x=='B']) }, {'Class' : 'Value', 'Value' : "%d"%len([x for x in Final_Grades if x=='C']) }]
        )

        nFinalA = len([x for x in Final_Grades if x=='A'])
        nFinalB = len([x for x in Final_Grades if x=='B'])
        nFinalC = len([x for x in Final_Grades if x=='C'])
        nTotal = nFinalA + nFinalB + nFinalC

        TotalYield = '{0:1.1f}%'.format(float(nFinalA + nFinalB)/nTotal*100) if nTotal > 0 else "-"

        VersionInfo = time.strftime("%Y-%m-%d %H:%M:%S") + "<br>"
        try:
            VersionInfo = VersionInfo + self.TestResultEnvironmentObject.MoReWebVersion + " on branch " + self.TestResultEnvironmentObject.MoReWebBranch 
        except:
            VersionInfo = VersionInfo + "unknown version"

        try:
            Footnotes = '*: required: ' + ','.join(self.TestResultEnvironmentObject.Configuration['RequiredTestTypesForComplete'].strip().split(','))
        except:
            Footnotes = ''

        HTML += self.Table(TableData) + self.BoxFooter("<div style='height:10px;'></div><div style='text-align:center;' title='fraction of A+B modules'><b>A+B: %d modules, yield: %s</b></div><div style='height:10px;'></div><div>%s</div><div>%s</div>"%(nFinalA + nFinalB, TotalYield, VersionInfo, Footnotes))

        return self.Boxed(HTML)

