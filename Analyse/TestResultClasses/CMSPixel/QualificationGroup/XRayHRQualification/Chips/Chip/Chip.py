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
        i = 0
        for Rate in self.ParentObject.ParentObject.Attributes['Rates']['HREfficiency']:
            self.ResultData['SubTestResultDictList'] += [
                {
                    'Key':'EfficiencyMap_{:d}'.format(Rate),
                    'Module':'EfficiencyMap',
                    'InitialAttributes':{
                        'Rate':Rate,
                        'StorageKey':'EfficiencyMap_{:d}'.format(Rate),
                    },
                    'DisplayOptions':{
                        'Order':10+i
                    },
                },
                {
                    'Key':'EfficiencyDistribution_{:d}'.format(Rate),
                    'Module':'EfficiencyDistribution',
                    'InitialAttributes':{
                        'Rate':Rate,
                        'StorageKey':'EfficiencyDistribution_{:d}'.format(Rate),
                    },
                    'DisplayOptions':{
                        'Order':20+i
                    
                    },
                },
                {
                    'Key':'BackgroundMap_{:d}'.format(Rate),
                    'Module':'BackgroundMap',
                    'InitialAttributes':{
                        'Rate':Rate,
                        'StorageKey':'BackgroundMap_{:d}'.format(Rate),
                    },
                    'DisplayOptions':{
                        'Order':30+i
                    },
                },
            ]
            i+=1
        for Rate in self.ParentObject.ParentObject.Attributes['Rates']['HRData']:
            self.ResultData['SubTestResultDictList'] += [
                {
                    'Key':'HotPixelMap_{:d}'.format(Rate),
                    'Module':'HotPixelMap',
                    'InitialAttributes':{
                        'Rate':Rate,
                        'StorageKey':'HotPixelMap_{:d}'.format(Rate),
                    },
                    'DisplayOptions':{
                        'Order':40+i
                    },
                },
                {
                    'Key':'HitMap_{:d}'.format(Rate),
                    'Module':'HitMap',
                    'InitialAttributes':{
                        'Rate':Rate,
                        'StorageKey':'HitMap_{:d}'.format(Rate),
                    },
                    'DisplayOptions':{
                        'Order':50+i
                    },
                },
                {
                    'Key':'ColumnReadoutUniformity_{:d}'.format(Rate),
                    'Module':'ColumnReadoutUniformity',
                    'InitialAttributes':{
                        'Rate':Rate,
                        'StorageKey':'ColumnReadoutUniformity_{:d}'.format(Rate),
                    },
                    'DisplayOptions':{
                        'Order':60+i
                    },
                },
                {
                    'Key':'ReadoutUniformityOverTime_{:d}'.format(Rate),
                    'Module':'ReadoutUniformityOverTime',
                    'InitialAttributes':{
                        'Rate':Rate,
                        'StorageKey':'ReadoutUniformityOverTime_{:d}'.format(Rate),
                    },
                    'DisplayOptions':{
                        'Order':70+i
                    },
                },
                {
                    'Key':'ReadoutUniformityOverTimeDistribution_{:d}'.format(Rate),
                    'Module':'ReadoutUniformityOverTimeDistribution',
                    'InitialAttributes':{
                        'Rate':Rate,
                        'StorageKey':'ReadoutUniformityOverTimeDistribution_{:d}'.format(Rate),
                    },
                    'DisplayOptions':{
                        'Order':70+i
                    },
                },
                {
                    'Key':'ColumnUniformityEventsPerColumn',
                    'InitialAttributes':{
                        'Rate':Rate,
                    },
                    'DisplayOptions':{
                        'Order':90+i
                    },

                },
            ]
            i+=1
        for Rate in self.ParentObject.ParentObject.Attributes['Rates']['HRSCurves']:
            self.ResultData['SubTestResultDictList'] += [
                {
                    'Key':'SCurveWidths_{:d}'.format(Rate),
                    'Module':'SCurveWidths',
                    'InitialAttributes':{
                        'Rate':Rate,
                        'StorageKey':'SCurveWidths_{:d}'.format(Rate),
                    },
                    'DisplayOptions':{
                        'Order':100+i
                    },
                }
            ]
            i+=1

        self.ResultData['SubTestResultDictList'] += [
                {
                    'Key':'ColumnUniformityPerColumn',
                    'InitialAttributes':{
                    },
                    'DisplayOptions':{
                        'Order':80+i   
                    },
                    
                },
                {
                    'Key':'EfficiencyInterpolation',
                    'InitialAttributes':{
                    },
                    'DisplayOptions':{
                        'Order':2    
                    },
                    
                },
                {
                    'Key':'Grading',
                    'InitialAttributes':{
                    },
                    'DisplayOptions':{
                        'Order':0    
                    },
                    
                },
            ]
        
    def PopulateResultData(self):
        self.CloseSubTestResultFileHandles()
