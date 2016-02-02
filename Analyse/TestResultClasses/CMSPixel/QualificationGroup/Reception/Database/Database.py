# -*- coding: utf-8 -*-
import AbstractClasses
import os

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

        chipResults = self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResultDictList']
        nChips = len(chipResults)
        gradingResult = self.ParentObject.ResultData['SubTestResults']['Grading']

        HeaderRow = ['',
                   'Total',
                   'Dead',
                   'Bump',
                   'D']
        if nChips > 1:
            for i in range(nChips-1):
                HeaderRow.append('')
        HeaderRow.append('B')
        if nChips > 1:
            for i in range(nChips-1):
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
               '',
               '']
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
        ROCRow += ROCRowResults

        self.ResultData['Table']['BODY'].append(ROCRow)

        ### fill row for reception test
        ReceptionDataRow = ['Reception']

        # pixel defects per module
        NDefects = gradingResult.ResultData['KeyValueDictPairs']['Defects']['Value']
        NDeadPixels = gradingResult.ResultData['KeyValueDictPairs']['DeadPixels']['Value']
        NDefectiveBumps = gradingResult.ResultData['KeyValueDictPairs']['DefectiveBumps']['Value']
        ReceptionDataRow += [NDefects, NDeadPixels, NDefectiveBumps]

        # pixel defects per ROC
        NDefectiveBumpsList = []
        NDeadPixelsList = []
        for chipResult in chipResults:
            #NDefectsROC = int(chipResult['TestResultObject'].ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['NDefects'])
            NDefectiveBumpsROC = int(chipResult['TestResultObject'].ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['NDefectiveBumps'])
            NDeadPixelsROC = int(chipResult['TestResultObject'].ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['NDeadPixels'])
            NDefectiveBumpsList.append(NDefectiveBumpsROC)
            NDeadPixelsList.append(NDeadPixelsROC)
        ReceptionDataRow += NDeadPixelsList
        ReceptionDataRow += NDefectiveBumpsList

        self.ResultData['Table']['BODY'].append(ReceptionDataRow)

        # todo: fill row for Pisa DB result

        # todo: fill row for local DB
