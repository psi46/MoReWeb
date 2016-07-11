# -*- coding: utf-8 -*-
import AbstractClasses
import os
import sys
import traceback

from AbstractClasses.Helper.GlobalDatabaseQuery import GlobalDatabaseQuery

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.NameSingle = 'Database'
        self.Name = 'CMSPixel_QualificationGroup_Reception_%s_TestResult'%self.NameSingle
        self.Title = 'Database comparison'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'


    def GradeColoredValue(self, value, grade, center=False):
        GradeAHTMLTemplate = "<div style='%s'>%s</div>"
        GradeBHTMLTemplate = "<div style='color:#f70;font-weight:bold;%s'>%s</div>"
        GradeCHTMLTemplate = "<div style='color:red;font-weight:bold;%s'>%s</div>"

        if center:
            Style = 'text-align:center;'
        else:
            Style = ''

        if grade == 1:
            return GradeAHTMLTemplate%(Style,value)
        elif grade == 2:
            return GradeBHTMLTemplate%(Style,value)
        elif grade == 3:
            return GradeCHTMLTemplate%(Style,value)
        else:
            return value

    def GradeColoredDefectsValue(self, value):
        if value == '#':
            return self.GradeColoredValue(value, 3)
        try:
            limitB = self.TestResultEnvironmentObject.GradingParameters['defectsB']
            limitC = self.TestResultEnvironmentObject.GradingParameters['defectsC']
            if int(value) >= limitC:
                return self.GradeColoredValue(value, 3)
            elif int(value) >= limitB:
                return self.GradeColoredValue(value, 2)
            else:
                return self.GradeColoredValue(value, 1)
        except:
            return self.GradeColoredValue(value, 3)


    def PopulateResultData(self):
        if self.TestResultEnvironmentObject.Configuration['Database']['UseGlobal']:
            return

        if 'Type' in self.Attributes and self.Attributes['Type'] == 'PixelDefects':
            self.PopulateResultDataPixelDefects()
            self.Title += " - Pixel Defects"
        else:
            self.PopulateResultDataFullQualifications()

    def PopulateResultDataFullQualifications(self):

        LeakageCurrent150p17 = -1
        try:
            ModuleID = self.ParentObject.Attributes['ModuleID']
            DB = GlobalDatabaseQuery()
            rows = DB.GetFullQualificationResult(ModuleID=ModuleID)

            HeaderRow = ['FULLMODULE_ID', 'GRADE', 'BAREMODULE_ID', 'HDI_ID', 'SENSOR_ID', 'BUILTON', 'BUILTBY', 'STATUS', 'tempnominal', 'I150', 'IVSLOPE', 'PIXELDEFECTS']
            if len(rows) >0:
                for k,v in rows[0].items():
                    if k not in HeaderRow:
                        HeaderRow.append(k)
            self.ResultData['Table'] = {
               'HEADER': [HeaderRow],
               'BODY': [],
               'FOOTER': [],
            }

            for row in rows:
                FulltestRow = []
                for k in HeaderRow:
                    FulltestRow.append(row[k] if k in row else '-')
                    if k == 'I150' and row['tempnominal'] == 'p17_1':
                        try:
                            LeakageCurrent150p17 = float(row[k])
                        except:
                            LeakageCurrent150p17 = -2

                self.ResultData['Table']['BODY'].append(FulltestRow)

            IVdata = DB.GetFulltestIVCurve(ModuleID=ModuleID)
            self.ResultData['HiddenData']['IVCurveDB'] = IVdata
            if len(IVdata) < 1:
                print "\x1b[31merror: can't read IV curve from global DB!\x1b[0m"

        except:
            self.ResultData['Table'] = {
               'HEADER': [['Error']],
               'BODY': [["Can't compare with DB, either no connection or module not in database!"]],
               'FOOTER': [],
            }


        self.ResultData['HiddenData']['LeakageCurrent150p17'] = LeakageCurrent150p17


    def PopulateResultDataPixelDefects(self):
        chipResults = self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResultDictList']
        nChips = len(chipResults)
        gradingResult = self.ParentObject.ResultData['SubTestResults']['Grading']

        HeaderRow = ['',
                   'Total',
                   'Dead']
        if nChips > 1:
            for i in range(nChips):
                HeaderRow.append('')
        HeaderRow.append('Bump')
        if nChips > 1:
            for i in range(nChips):
                HeaderRow.append('')

        self.ResultData['Table'] = {
           'HEADER': [HeaderRow],
           'BODY': [],
           'FOOTER': [],
        }

        LinkHTMLTemplate = self.TestResultEnvironmentObject.HtmlParser.getSubpart(
           self.TestResultEnvironmentObject.OverviewHTMLTemplate,
           '###LINK###'
        )
        ROCRow = [
               '',
               '',
               ''
               ]
        ROCRowResults = []
        i = 0
        for chipResult in chipResults:
            ROCRowResults.append(
                self.TestResultEnvironmentObject.HtmlParser.substituteMarkerArray(
                     LinkHTMLTemplate,
                     {
                         '###LABEL###':'C%d'%i,
                         '###URL###':os.path.relpath(chipResult['TestResultObject'].FinalResultsStoragePath, self.ParentObject.FinalResultsStoragePath)+'/TestResult.html'
                     }
                 )
            )
            i += 1
        ROCRow += ROCRowResults
        ROCRow += ['']
        ROCRow += ROCRowResults

        self.ResultData['Table']['BODY'].append(ROCRow)

        ### fill row for reception test
        ReceptionDataRow = ['Reception']

        # pixel defects per module
        NDefects = 0 #gradingResult.ResultData['KeyValueDictPairs']['Defects']['Value']
        NDeadPixels = 0 #gradingResult.ResultData['KeyValueDictPairs']['DeadPixels']['Value']
        NDefectiveBumps = 0 #gradingResult.ResultData['KeyValueDictPairs']['DefectiveBumps']['Value']


        # pixel defects per ROC
        NDefectiveBumpsList = []
        NDeadPixelsList = []
        for chipResult in chipResults:
            #NDefectsROC = int(chipResult['TestResultObject'].ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['NDefects'])
            NDefectiveBumpsROC = int(chipResult['TestResultObject'].ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['NDefectiveBumps'])
            NDeadPixelsROC = int(chipResult['TestResultObject'].ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['NDeadPixels'])
            NDefectiveBumpsList.append(NDefectiveBumpsROC)
            NDeadPixelsList.append(NDeadPixelsROC)

            NDeadPixels +=  NDeadPixelsROC
            NDefectiveBumps += NDefectiveBumpsROC
            NDefects += NDeadPixelsROC + NDefectiveBumpsROC

        ReceptionDataRow += [NDefects, NDeadPixels]

        ReceptionDataRow += NDeadPixelsList
        ReceptionDataRow += [NDefectiveBumps]
        ReceptionDataRow += NDefectiveBumpsList

        self.ResultData['Table']['BODY'].append(ReceptionDataRow)

        #fill row for Pisa DB result
        try:
            ModuleID = self.ParentObject.Attributes['ModuleID']
            DB = GlobalDatabaseQuery()
            rows = DB.GetFulltestPixelDefects(ModuleID=ModuleID)

            if rows is None:
                raise Exception("Could not connect to DB or module not found in DB! Use Configuration/GlobalDatabase.cfg to specify connection parameters to MySQL database!")

            DBDataRow = ['Database']
            DBDataRow.append(sum([x['Total'] for x in rows]))

            NDeadPixelsDB = sum([x['nDeadPixel'] for x in rows])
            DBDataRow.append(NDeadPixelsDB)
            for ChipNo in range(len(chipResults)):
                try:
                    DBDataRow.append([x['nDeadPixel'] for x in rows if int(x['ROC_POS']) == ChipNo][0])
                except:
                    DBDataRow.append('#')

            NMissingBumpsDB = sum([x['nDeadBumps'] for x in rows])
            DBDataRow.append(NMissingBumpsDB)
            for ChipNo in range(len(chipResults)):
                try:
                    DBDataRow.append([x['nDeadBumps'] for x in rows if int(x['ROC_POS']) == ChipNo][0])
                except:
                    DBDataRow.append('#')

            self.ResultData['HiddenData']['NPixelDefectsDB'] = NDeadPixelsDB + NMissingBumpsDB
            self.ResultData['Table']['BODY'].append(DBDataRow)
        except Exception as inst:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            # Start red color
            sys.stdout.write("\x1b[31m")
            sys.stdout.flush()
            print '\x1b[31mException while processing', self.FinalResultsStoragePath
            # Print traceback
            traceback.print_exception(exc_type, exc_obj, exc_tb)
            # Stop red color
            sys.stdout.write("\x1b[0m")
            sys.stdout.flush()