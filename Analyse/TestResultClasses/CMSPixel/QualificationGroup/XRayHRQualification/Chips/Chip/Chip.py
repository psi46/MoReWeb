import AbstractClasses
import ROOT
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):


    def CustomInit(self):
        ROOT.gStyle.SetOptStat(0)
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_XRayHRQualification_ROC'

        self.Name = 'CMSPixel_QualificationGroup_XRayHRQualification_Chips_Chip_TestResult'
        self.NameSingle = 'Chip'
        self.Title = 'Chip '+str(self.Attributes['ChipNo'])
        self.ResultData['SubTestResultDictList'] = [
                {
                    'Key':'AliveMap',
                    'InitialAttributes':{
                    },
                    'DisplayOptions':{
                        'Order':200
                    },
                }
        ]
        # order!
        i = 0
        for Rate in self.ParentObject.ParentObject.Attributes['Rates']['HREfficiency']:
            self.ResultData['SubTestResultDictList'] += [
                {
                    'Key':'EfficiencyMap_{Rate}'.format(Rate=Rate),
                    'Module':'EfficiencyMap',
                    'InitialAttributes':{
                        'Rate':Rate,
                        'StorageKey':'EfficiencyMap_{Rate}'.format(Rate=Rate),
                    },
                    'DisplayOptions':{
                        'Order':10+i
                    },
                },
                {
                    'Key':'EfficiencyDistribution_{Rate}'.format(Rate=Rate),
                    'Module':'EfficiencyDistribution',
                    'InitialAttributes':{
                        'Rate':Rate,
                        'StorageKey':'EfficiencyDistribution_{Rate}'.format(Rate=Rate),
                    },
                    'DisplayOptions':{
                        'Order':20+i
                    
                    },
                },
                {
                    'Key':'BackgroundMap_{Rate}'.format(Rate=Rate),
                    'Module':'BackgroundMap',
                    'InitialAttributes':{
                        'Rate':Rate,
                        'StorageKey':'BackgroundMap_{Rate}'.format(Rate=Rate),
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
                    'Key':'HotPixelRetrimming_{Rate}'.format(Rate=Rate),
                    'Module':'HotPixelRetrimming',
                    'InitialAttributes':{
                        'Rate':Rate,
                        'StorageKey':'HotPixelRetrimming_{Rate}'.format(Rate=Rate),
                    },
                    'DisplayOptions':{
                        'Order':40+i
                    },
                },
                {
                    'Key':'HotPixelMap_{Rate}'.format(Rate=Rate),
                    'Module':'HotPixelMap',
                    'InitialAttributes':{
                        'Rate':Rate,
                        'StorageKey':'HotPixelMap_{Rate}'.format(Rate=Rate),
                    },
                    'DisplayOptions':{
                        'Order':40+i
                    },
                },
                {
                    'Key':'HitMap_{Rate}'.format(Rate=Rate),
                    'Module':'HitMap',
                    'InitialAttributes':{
                        'Rate':Rate,
                        'StorageKey':'HitMap_{Rate}'.format(Rate=Rate),
                    },
                    'DisplayOptions':{
                        'Order':50+i
                    },
                },
                {
                    'Key':'BumpBondingDefects_{Rate}'.format(Rate=Rate),
                    'Module':'BumpBondingDefects',
                    'InitialAttributes':{
                        'Rate':Rate,
                        'StorageKey':'BumpBondingDefects_{Rate}'.format(Rate=Rate),
                    },
                    'DisplayOptions':{
                        'Order':50+i
                    },
                },
                {
                    'Key':'ColumnReadoutUniformity_{Rate}'.format(Rate=Rate),
                    'Module':'ColumnReadoutUniformity',
                    'InitialAttributes':{
                        'Rate':Rate,
                        'StorageKey':'ColumnReadoutUniformity_{Rate}'.format(Rate=Rate),
                    },
                    'DisplayOptions':{
                        'Order':60+i
                    },
                },
                {
                    'Key':'ReadoutUniformityOverTime_{Rate}'.format(Rate=Rate),
                    'Module':'ReadoutUniformityOverTime',
                    'InitialAttributes':{
                        'Rate':Rate,
                        'StorageKey':'ReadoutUniformityOverTime_{Rate}'.format(Rate=Rate),
                    },
                    'DisplayOptions':{
                        'Order':70+i
                    },
                },
                {
                    'Key':'ReadoutUniformityOverTimeDistribution_{Rate}'.format(Rate=Rate),
                    'Module':'ReadoutUniformityOverTimeDistribution',
                    'InitialAttributes':{
                        'Rate':Rate,
                        'StorageKey':'ReadoutUniformityOverTimeDistribution_{Rate}'.format(Rate=Rate),
                    },
                    'DisplayOptions':{
                        'Order':70+i
                    },
                },
                {
                    'Key':'ColumnUniformityEventsPerColumn_{Rate}'.format(Rate=Rate),
                    'Module':'ColumnUniformityEventsPerColumn',
                    'InitialAttributes':{
                        'Rate':Rate,
                        'StorageKey':'ColumnUniformityEventsPerColumn_{Rate}'.format(Rate=Rate),
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
                    'Key':'SCurveWidths_{Rate}'.format(Rate=Rate),
                    'Module':'SCurveWidths',
                    'InitialAttributes':{
                        'Rate':Rate,
                        'StorageKey':'SCurveWidths_{Rate}'.format(Rate=Rate),
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
                    'Key':'DoubleColumnEfficiencyDistribution',
                    'InitialAttributes':{
                    },
                    'DisplayOptions':{
                        'Order':200
                    },
                    
                },
                {
                    'Key':'CalDelScan',
                    'InitialAttributes':{
                    },
                    'DisplayOptions':{
                        'Order':250
                    },
                },
                {
                    'Key':'Grading',
                    'InitialAttributes':{
                    },
                    'DisplayOptions':{
                        'Order':0,
                        'Width':2
                    },

                },
            ]

    def PopulateResultData(self):
        self.CloseSubTestResultFileHandles()
