import ROOT
import AbstractClasses
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Fulltest_Parameter1_TestResult'
        self.NameSingle='Parameter1'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
        self.Attributes['SpecialPopulateDataParameters'] = {
                'Key':'Noise',
                'DataKey':'PHCalibrationTan', # which sub test result to take the data from
                'DataParameterKey':'mu', # which part of key value dict pairs
                'DefectsKey': 'NPar1Defects',
                'YLimitB':self.TestResultEnvironmentObject.GradingParameters['par1B'],# limit for grading
                'YLimitC':self.TestResultEnvironmentObject.GradingParameters['par1C'],# limit for grading
                'MarkerColor':ROOT.kBlue,
                'LineColor':ROOT.kBlue,
                'MarkerStyle':21,
                'ScaleToLimit':False,
                'YaxisTitle':'Parameter1',
                
        }

        
    def PopulateResultData(self):
        
        ROOT.gPad.SetLogy(0);
        
        self.ResultData['HiddenData']['LimitB'] = self.TestResultEnvironmentObject.GradingParameters['par1B']
        self.ResultData['HiddenData']['LimitC'] = self.TestResultEnvironmentObject.GradingParameters['par1C']
        self.ParentObject.ResultData['SubTestResults']['Noise'].SpecialPopulateData(self, self.Attributes['SpecialPopulateDataParameters'])
