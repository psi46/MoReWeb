import ROOT
import AbstractClasses
import ROOT
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_ModuleTestGroup_Module_VcalThresholdWidth_TestResult'
        self.NameSingle='VcalThresholdWidth'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
        self.Title = 'Vcal Threshold Width'
    def SetStoragePath(self):
        pass
        
    def PopulateResultData(self):
        
        ROOT.gPad.SetLogy(0);
        
        self.ResultData['HiddenData']['LimitB'] = self.TestResultEnvironmentObject.GradingParameters['trimmingB']
        self.ResultData['HiddenData']['LimitC'] = self.TestResultEnvironmentObject.GradingParameters['trimmingC']
        self.ParentObject.ResultData['SubTestResults']['Noise'].SpecialPopulateData(self, {
                'Key':'Vcal Threshold Width',
                'DataKey':'VcalThresholdTrimmed', # which sub test result to take the data from
                'DataParameterKey':'sigma', # which part of key value dict pairs
                'DataFactor':self.TestResultEnvironmentObject.GradingParameters['StandardADC2ElectronConversionFactor'],
                'YLimitB':self.TestResultEnvironmentObject.GradingParameters['trimmingB'],# limit for grading
                'MarkerColor':ROOT.kGreen,
                'LineColor':ROOT.kGreen,
                'MarkerStyle':21,
                'YaxisTitle':'Width of Vcal Threshold',
                
        })
