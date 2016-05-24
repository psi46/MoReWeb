import ROOT
import AbstractClasses


class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):

    def CustomInit(self):
        self.NameSingle = 'ReadbackParameter'
        self.Name = 'CMSPixel_QualificationGroup_Fulltest_%s_TestResult'%self.NameSingle

        self.Title = "Readback %s"%self.Attributes['Parameter']
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
        self.Attributes['SpecialPopulateDataParameters'] = {
                'Key': 'Readback: %s'%self.Attributes['Parameter'],
                'DataKey': 'ReadbackCal',  # which sub test result to take the data from
                'DataParameterKey': self.Attributes['Parameter'],  # which part of key value dict pairs
                'YLimitB': 0,  # limit for grading
                'YLimitC': 0,  # limit for grading
                'MarkerColor': ROOT.kBlue,
                'LineColor': ROOT.kBlue,
                'MarkerStyle': 21,
                'ScaleToLimit': False,
                'YaxisTitle': self.Attributes['Parameter'],
                'NoIntegralCheck': True,
        }

    def PopulateResultData(self):
        
        ROOT.gPad.SetLogy(0)
        self.SpecialPopulateData(self, self.Attributes['SpecialPopulateDataParameters'])
