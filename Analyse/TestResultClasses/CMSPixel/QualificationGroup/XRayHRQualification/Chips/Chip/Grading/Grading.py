import ROOT
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_XRayHRQualification_Chips_Chip_Grading_TestResult'
        self.NameSingle='Grading'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_XRayHRQualification_ROC'
        self.ResultData['HiddenData']['ListOfLowEfficiencyPixels'] = []
        

    def GetSingleChipSubtestGrade(self, SpecialPopulateDataParameters, CurrentGrade):
        Value = float(self.ParentObject.ResultData['SubTestResults'][SpecialPopulateDataParameters['DataKey']].ResultData['KeyValueDictPairs'][SpecialPopulateDataParameters['DataParameterKey']]['Value'])
        nValue = float(self.ParentObject.ResultData['SubTestResults'][SpecialPopulateDataParameters['DataKey']].ResultData['KeyValueDictPairs']['N']['Value'])
        
        if SpecialPopulateDataParameters.has_key('DataFactor'):
            Value = Value*SpecialPopulateDataParameters['DataFactor']
        if SpecialPopulateDataParameters.has_key('CalcFunction'):
            Value = SpecialPopulateDataParameters['CalcFunction'](Value, self.ParentObject.ResultData['SubTestResults'][SpecialPopulateDataParameters['DataKey']].ResultData['KeyValueDictPairs'])
        
        Value = float(Value)
        ChipGrade = CurrentGrade
        
        if ChipGrade == 1 and Value > SpecialPopulateDataParameters['YLimitB']:
            ChipGrade = 2
        if Value > SpecialPopulateDataParameters['YLimitC']:
            ChipGrade = 3
        if ChipGrade == 1 and nValue < (8*self.nCols - self.TestResultEnvironmentObject.GradingParameters['defectsB']):
            ChipGrade = 2
        if nValue < (8*self.nCols - self.TestResultEnvironmentObject.GradingParameters['defectsC']):
            ChipGrade = 3
        return ChipGrade
	
    def PopulateResultData(self):

        
        for column in range(self.nCols): #Column
            for row in range(self.nRows): #Row
                # -- Bump bonding
                if  (self.chipNo,column,row) not in notAlivePixels:
                    pass

        PixelDefectsGradeALimit = self.TestResultEnvironmentObject.GradingParameters['defectsB']
        PixelDefectsGradeBLimit = self.TestResultEnvironmentObject.GradingParameters['defectsC']
        totalDefects = len(self.ResultData['HiddenData']['TotalList'])
        if totalDefects < PixelDefectsGradeALimit:
            pixelDefectsGrade = 1
        elif totalDefects < PixelDefectsGradeBLimit:
            pixelDefectsGrade = 2
        else:
            pixelDefectsGrade = 3
            
        self.ResultData['KeyValueDictPairs'] = {
            'PixelDefectsGrade':{
                'Value': '%d'%pixelDefectsGrade,
                'Label': 'Pixel Defects Grade ROC'
            },
        }
        self.ResultData['KeyList'] = ['PixelDefectsGrade']

