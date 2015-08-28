import ROOT
import AbstractClasses
import ROOT
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Fulltest_VcalThresholdWidth_TestResult'
        self.NameSingle='VcalThresholdWidth'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
        self.Title = 'Vcal Threshold Width'
        self.Attributes['SpecialPopulateDataParameters'] = {
                'Key':'Vcal Threshold Width',
                'DataKey':'VcalThresholdTrimmed', # which sub test result to take the data from
                'DefectsKey': 'NTrimProblems',
                'DataParameterKey':'sigma', # which part of key value dict pairs
                'DataFactor':self.TestResultEnvironmentObject.GradingParameters['StandardVcal2ElectronConversionFactor'],
                'YLimitB':self.TestResultEnvironmentObject.GradingParameters['trimmingB'],# limit for grading
                'YLimitC':self.TestResultEnvironmentObject.GradingParameters['trimmingC'],# limit for grading
                'MarkerColor':ROOT.kGreen,
                'LineColor':ROOT.kGreen,
                'MarkerStyle':21,
                'YaxisTitle':'Width of Vcal Threshold',
        }

    def PopulateResultData(self):

        ROOT.gPad.SetLogy(0);

        self.ResultData['HiddenData']['LimitB'] = self.TestResultEnvironmentObject.GradingParameters['trimmingB']
        self.ResultData['HiddenData']['LimitC'] = self.TestResultEnvironmentObject.GradingParameters['trimmingC']
        self.ParentObject.ResultData['SubTestResults']['Noise'].SpecialPopulateData(self,self.Attributes['SpecialPopulateDataParameters'])
