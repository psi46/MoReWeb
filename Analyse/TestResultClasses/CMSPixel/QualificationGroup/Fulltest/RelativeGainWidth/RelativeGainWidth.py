import ROOT
import AbstractClasses
import ROOT
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Fulltest_RelativeGainWidth_TestResult'
        self.NameSingle='RelativeGainWidth'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
        self.Attributes['SpecialPopulateDataParameters'] = {
                'Key':'RelativeGainWidth',
                'DataKey':'PHCalibrationGain', # which sub test result to take the data from
                'DefectsKey': 'NGainDefects',
                'DataParameterKey':'mu', # which part of key value dict pairs
                'CalcFunction':lambda Value, KeyValueDictPairs: float(KeyValueDictPairs['sigma']['Value']) / float(KeyValueDictPairs['mu']['Value']) if float(KeyValueDictPairs['mu']['Value'])>0 else 0,
                'YLimitB':self.TestResultEnvironmentObject.GradingParameters['gainB'],# limit for grading
                'YLimitC':self.TestResultEnvironmentObject.GradingParameters['gainC'],# limit for grading
                'MarkerColor':ROOT.kBlack,
                'LineColor':ROOT.kBlack,
                'MarkerStyle':21,
                'YaxisTitle':'Relative Gain Width',
                
        }

        
    def PopulateResultData(self):
        ROOT.gPad.SetLogy(0);
        self.ResultData['HiddenData']['LimitB'] = self.TestResultEnvironmentObject.GradingParameters['gainB']
        self.ResultData['HiddenData']['LimitC'] = self.TestResultEnvironmentObject.GradingParameters['gainC']
        self.ParentObject.ResultData['SubTestResults']['Noise'].SpecialPopulateData(self,  self.Attributes['SpecialPopulateDataParameters'])
        
