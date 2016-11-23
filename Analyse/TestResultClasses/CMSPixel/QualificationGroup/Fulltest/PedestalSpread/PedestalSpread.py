import ROOT
from AbstractClasses.GeneralTestResult import GeneralTestResult


class TestResult(GeneralTestResult):
    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_Fulltest_PedestalSpread_TestResult'
        self.NameSingle = 'PedestalSpread'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
        self.Attributes['SpecialPopulateDataParameters'] = {
            'Key': 'Pedestal Spread',
            'DataKey': 'PHCalibrationPedestal',  # which sub test result to take the data from
            'DataParameterKey': 'sigma',  # which part of key value dict pairs
            'DataFactor': self.TestResultEnvironmentObject.GradingParameters['StandardVcal2ElectronConversionFactor'],
            'YLimitB': self.TestResultEnvironmentObject.GradingParameters['pedestalB'] if not self.isPROC else 1e9,  # limit for grading
            'YLimitC': self.TestResultEnvironmentObject.GradingParameters['pedestalC'] if not self.isPROC else 1e9,  # limit for grading
            'MarkerColor': ROOT.kRed,
            'LineColor': ROOT.kRed,
            'MarkerStyle': 21,
            'YaxisTitle': 'Average Pedestal [e]',
        }

        if self.isPROC:
            self.Attributes['SpecialPopulateDataParameters']['Ymin'] = 0
            self.Attributes['SpecialPopulateDataParameters']['Ymax'] = 10000

    def PopulateResultData(self):
        ROOT.gPad.SetLogy(0)

        self.ResultData['HiddenData']['LimitB'] = self.TestResultEnvironmentObject.GradingParameters['pedestalB']
        self.ResultData['HiddenData']['LimitC'] = self.TestResultEnvironmentObject.GradingParameters['pedestalC']
        self.SpecialPopulateData(self, self.Attributes['SpecialPopulateDataParameters'])
