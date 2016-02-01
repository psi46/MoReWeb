# -*- coding: utf-8 -*-
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

            try:
                VcalThresholdWidthGrade = int(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['SubGrading_VcalThresholdWidth_Mean_C%d'%ChipNo]['Value'])
            except:
                VcalThresholdWidthGrade = 3

            try:
                RelativeGainWidthGrade = int(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['SubGrading_RelativeGainWidth_Mean_C%d'%ChipNo]['Value'])
            except:
                RelativeGainWidthGrade = 3

            try:
                PedestalSpreadGrade = int(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['SubGrading_PedestalSpread_Mean_C%d'%ChipNo]['Value'])
            except:
                PedestalSpreadGrade = 3

            try:
                Parameter1Grade = int(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['SubGrading_Parameter1_Mean_C%d'%ChipNo]['Value'])
            except:
                Parameter1Grade = 3

            try:
                NoiseGrade = int(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['SubGrading_Noise_Mean_C%d'%ChipNo]['Value'])
            except:
                NoiseGrade = 3

            try:
                PixelDefectsTotal = self.GradeColoredValue(i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['Total']['Value'], PixelDefectsGrade)
            except:
                PixelDefectsTotal = '#'

            try:
                Threshold = i['TestResultObject'].ResultData['SubTestResults']['PerformanceParameters'].ResultData['KeyValueDictPairs']['Threshold']['Value']
                ThresholdWidth = self.GradeColoredValue(i['TestResultObject'].ResultData['SubTestResults']['PerformanceParameters'].ResultData['KeyValueDictPairs']['ThresholdWidth']['Value'], VcalThresholdWidthGrade)
            except:
                Threshold = '#'
                ThresholdWidth = self.GradeColoredValue('#', 3)

            try:
                RelativeGainWidth = self.GradeColoredValue(i['TestResultObject'].ResultData['SubTestResults']['PerformanceParameters'].ResultData['KeyValueDictPairs']['RelativeGainWidth']['Value'], RelativeGainWidthGrade)
            except:
                RelativeGainWidth = self.GradeColoredValue('#', 3)

            try:
                PedestalSpread = self.GradeColoredValue(i['TestResultObject'].ResultData['SubTestResults']['PerformanceParameters'].ResultData['KeyValueDictPairs']['PedestalSpread']['Value'], PedestalSpreadGrade)
            except:
                PedestalSpread = self.GradeColoredValue('#', 3)

            try:
                Noise = self.GradeColoredValue(i['TestResultObject'].ResultData['SubTestResults']['PerformanceParameters'].ResultData['KeyValueDictPairs']['Noise']['Value'], NoiseGrade)
            except:
                Noise = self.GradeColoredValue('#', 3)

            try:
                RocGrade = max([PixelDefectsGrade, VcalThresholdWidthGrade, RelativeGainWidthGrade, PedestalSpreadGrade, Parameter1Grade, NoiseGrade])
            except:
                RocGrade = 3

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
                   self.GradeColoredDefectsValue(i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nDeadPixel']['Value']),
                   self.GradeColoredDefectsValue(i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nMaskDefect']['Value']),
                   self.GradeColoredDefectsValue(i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nDeadBumps']['Value']),
                   self.GradeColoredDefectsValue(i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nDeadTrimbits']['Value']),
                   self.GradeColoredDefectsValue(i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nAddressProblems']['Value']),
                   self.GradeColoredDefectsValue(i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nNoisy2Pixel']['Value']),
                   self.GradeColoredDefectsValue(i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nThrDefect']['Value']),
                   self.GradeColoredDefectsValue(i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nGainDefect']['Value']),
                   self.GradeColoredDefectsValue(i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nPedDefect']['Value']),
                   self.GradeColoredDefectsValue(i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nPar1Defect']['Value']),
                   Noise,
                   Threshold,
                   ThresholdWidth,
                   RelativeGainWidth,
                   PedestalSpread,

               ]   
           )
