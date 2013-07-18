# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import ROOT
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_ModuleTestGroup_Module_Summary3_TestResult'
        self.NameSingle='Summary3'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
        self.Title = 'Summary 3'
    def SetStoragePath(self):
        pass
        
    def PopulateResultData(self):
        
        
        self.ResultData['KeyValueDictPairs'] = {
            'Noise': {
                'Value':self.ParentObject.ResultData['SubTestResults']['Noise'].ResultData['KeyValueDictPairs']['mu']['Value'], 
                'Label':'Noise',
                'Unit':'e',
            },
            'VcalThrWidth': {
                'Value':self.ParentObject.ResultData['SubTestResults']['VcalThresholdWidth'].ResultData['KeyValueDictPairs']['mu']['Value'], 
                'Label':'Vcal Thr. Width',
                'Unit':'e',
            },
            'RelGainWidth': {
                'Value':self.ParentObject.ResultData['SubTestResults']['RelativeGainWidth'].ResultData['KeyValueDictPairs']['mu']['Value'], 
                'Label':'Rel. Gain Width',
                'Unit':'%',
            },
            'PedestalSpread': {
                'Value':self.ParentObject.ResultData['SubTestResults']['PedestalSpread'].ResultData['KeyValueDictPairs']['mu']['Value'], 
                'Label':'Pedestal Spread',
                'Unit':'e',
            },
            'Parameter1': {
                'Value':self.ParentObject.ResultData['SubTestResults']['Parameter1'].ResultData['KeyValueDictPairs']['mu']['Value'], 
                'Label':'Parameter1',
                'Unit':'',
            },
            'CurrentAtVoltage150': {
                'Value':self.ParentObject.ParentObject.ResultData['SubTestResults']['ModuleFulltest_p17'].ResultData['SubTestResults']['IVCurve'].ResultData['KeyValueDictPairs']['CurrentAtVoltage150']['Value'], 
                'Label':'I(150 V) @ 17°C',
                'Unit':'μA',
            },
            'CurrentVariation': {
                'Value':self.ParentObject.ParentObject.ResultData['SubTestResults']['ModuleFulltest_p17'].ResultData['SubTestResults']['IVCurve'].ResultData['KeyValueDictPairs']['Variation']['Value'], 
                'Label':'I(150 V) /I(100 V) @ 17°C',
            },
        }
        
        self.ResultData['KeyList'] = ['Noise','VcalThrWidth','RelGainWidth','PedestalSpread','Parameter1','CurrentAtVoltage150','CurrentVariation']
         
        if self.ParentObject.Attributes.has_key('recalculateCurrentTo'):
            self.ResultData['KeyValueDictPairs']['recalculatedCurrentAtVoltage150V'] = {'Value':self.ParentObject.ResultData['SubTestResults']['IVCurve'].ResultData['KeyValueDictPairs']['recalculatedCurrentAtVoltage150V']['Value'],'Label':'recalculated IV','Unit':'μA',}
            self.ResultData['KeyList'].append('recalculatedCurrentAtVoltage150V')   

