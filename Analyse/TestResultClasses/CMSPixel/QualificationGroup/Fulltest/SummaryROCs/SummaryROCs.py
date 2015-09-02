# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import os

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Fulltest_SummaryROCs_TestResult'
        self.NameSingle='SummaryROCs'
        self.Title = 'Summary ROCs'
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
        
    def PopulateResultData(self):
        self.ResultData['Table'] = {
           'HEADER':[
               [
                   'ROC',
                   'Grade',
                   'Total',
                   'Dead',
                   'Mask',
                   'Bumps',
                   'Trim(Bits)',
                   'Address',
                   'Noise',
                   'Thresh',
                   'Gain',
                   'Ped',
                   'Par1',
                   'Mean noise',
                   'Thr [e-]',
                   'Thr width',
                   'Rel gain width',
                   'Ped spread',
               ]
           ],
           'BODY':[],
           'FOOTER':[],
        }
        LinkHTMLTemplate = self.TestResultEnvironmentObject.HtmlParser.getSubpart(
           self.TestResultEnvironmentObject.OverviewHTMLTemplate,
           '###LINK###'
        )

        GradeMapping = {1:'A', 2:'B', 3:'C'}

        for i in self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResultDictList']:

            ChipNo = i['TestResultObject'].Attributes['ChipNo']
            PixelDefectsGrade = int(i['TestResultObject'].ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['PixelDefectsGrade']['Value'])
            VcalThresholdWidthGrade = int(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['SubGrading_VcalThresholdWidth_C%d'%ChipNo]['Value'])
            RelativeGainWidthGrade = int(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['SubGrading_RelativeGainWidth_C%d'%ChipNo]['Value'])
            PedestalSpreadGrade = int(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['SubGrading_PedestalSpread_C%d'%ChipNo]['Value'])
            Parameter1Grade = int(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['SubGrading_Parameter1_C%d'%ChipNo]['Value'])

            PixelDefectsTotal = self.GradeColoredValue(i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['Total']['Value'], PixelDefectsGrade)
            Threshold = i['TestResultObject'].ResultData['SubTestResults']['PerformanceParameters'].ResultData['KeyValueDictPairs']['Threshold']['Value']
            ThresholdWidth = self.GradeColoredValue(i['TestResultObject'].ResultData['SubTestResults']['PerformanceParameters'].ResultData['KeyValueDictPairs']['ThresholdWidth']['Value'], VcalThresholdWidthGrade)
            RelativeGainWidth = self.GradeColoredValue(i['TestResultObject'].ResultData['SubTestResults']['PerformanceParameters'].ResultData['KeyValueDictPairs']['RelativeGainWidth']['Value'], RelativeGainWidthGrade)
            PedestalSpread = self.GradeColoredValue(i['TestResultObject'].ResultData['SubTestResults']['PerformanceParameters'].ResultData['KeyValueDictPairs']['PedestalSpread']['Value'], PedestalSpreadGrade)
            Noise = self.GradeColoredValue(i['TestResultObject'].ResultData['SubTestResults']['PerformanceParameters'].ResultData['KeyValueDictPairs']['Noise']['Value'], 1)

            RocGrade = max([PixelDefectsGrade, VcalThresholdWidthGrade, RelativeGainWidthGrade, PedestalSpreadGrade, Parameter1Grade])
            RocGradeFormatted = self.GradeColoredValue(GradeMapping[RocGrade] if RocGrade in GradeMapping else 'None', RocGrade, True)

            self.ResultData['Table']['BODY'].append(
               [
                   self.TestResultEnvironmentObject.HtmlParser.substituteMarkerArray(
                       LinkHTMLTemplate,
                       {
                           '###LABEL###':'Chip '+str(ChipNo),
                           '###URL###':os.path.relpath(i['TestResultObject'].FinalResultsStoragePath, self.ParentObject.FinalResultsStoragePath)+'/TestResult.html'
                       }
                   ),
                   RocGradeFormatted,
                   PixelDefectsTotal,
                   i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nDeadPixel']['Value'],
                   i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nMaskDefect']['Value'],
                   i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nDeadBumps']['Value'],
                   i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nDeadTrimbits']['Value'],
                   i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nAddressProblems']['Value'],
                   i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nNoisy2Pixel']['Value'],
                   i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nThrDefect']['Value'],
                   i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nGainDefect']['Value'],
                   i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nPedDefect']['Value'],
                   i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nPar1Defect']['Value'],
                   Noise,
                   Threshold,
                   ThresholdWidth,
                   RelativeGainWidth,
                   PedestalSpread,

               ]   
           )
