import AbstractClasses
import ROOT
from AbstractClasses.GeneralTestResult import GeneralTestResult


class TestResult(GeneralTestResult):
    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_Fulltest_PedestalSpread_TestResult'
        self.NameSingle = 'PedestalSpread'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'

    def PopulateResultData(self):
        ROOT.gPad.SetLogy(0)

        self.ResultData['HiddenData']['LimitB'] = self.TestResultEnvironmentObject.GradingParameters['pedestalB']
        self.ResultData['HiddenData']['LimitC'] = self.TestResultEnvironmentObject.GradingParameters['pedestalC']
        self.ParentObject.ResultData['SubTestResults']['Noise'].SpecialPopulateData(self, {
            'Key': 'Pedestal Spread',
            'DataKey': 'PHCalibrationPedestal',  # which sub test result to take the data from
            'DataParameterKey': 'sigma',  # which part of key value dict pairs
            'DataFactor': self.TestResultEnvironmentObject.GradingParameters['StandardVcal2ElectronConversionFactor'],
            'YLimitB': self.TestResultEnvironmentObject.GradingParameters['pedestalB'],  # limit for grading
            'MarkerColor': ROOT.kRed,
            'LineColor': ROOT.kRed,
            'MarkerStyle': 21,
            'YaxisTitle': 'Average Pedestal [e]',

        })
