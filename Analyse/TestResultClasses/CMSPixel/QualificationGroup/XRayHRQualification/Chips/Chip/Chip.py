import AbstractClasses
import ROOT
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):


    def CustomInit(self):
        ROOT.gStyle.SetOptStat(0)
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_XRayHRQualification_ROC'

        self.Name = 'CMSPixel_QualificationGroup_XRayHRQualification_Chips_Chip_TestResult'
        self.NameSingle = 'Chip'
        self.Title = 'Chip '+str(self.Attributes['ChipNo'])
        # order!
        self.ResultData['SubTestResultDictList'] = []

        for Rate in self.ParentObject.ParentObject.Attributes['Rates']:
            self.ResultData['SubTestResultDictList'] += [
                {
                    'Key':'EfficiencyMap_{:d}'.format(Rate),
                    'Module':'EfficiencyMap',
                    'InitialAttributes':{
                        'Rate':Rate,
                        'StorageKey':'EfficiencyMap_{:d}'.format(Rate),
                    
                    },
                },
                {
                    'Key':'EfficiencyDistribution_{:d}'.format(Rate),
                    'Module':'EfficiencyDistribution',
                    'InitialAttributes':{
                        'Rate':Rate,
                        'StorageKey':'EfficiencyDistribution_{:d}'.format(Rate),
                    
                    },
                },
                {
                    'Key':'BackgroundMap_{:d}'.format(Rate),
                    'Module':'BackgroundMap',
                    'InitialAttributes':{
                        'Rate':Rate,
                        'StorageKey':'BackgroundMap_{:d}'.format(Rate),
                    },
                }
            ]

        self.ResultData['SubTestResultDictList'] += [
                {
                    'Key':'EfficiencyInterpolation',
                    'InitialAttributes':{
                        
                    },
                },
            ]
        print self.ResultData['SubTestResultDictList']
        
    def PopulateResultData(self):
        self.CloseSubTestResultFileHandles()
