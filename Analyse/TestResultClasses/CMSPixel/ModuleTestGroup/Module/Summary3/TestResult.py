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
        }
        self.ResultData['KeyList'] = ['Noise','VcalThrWidth','RelGainWidth','PedestalSpread','Parameter1']
        if self.ParentObject.ResultData['SubTestResults'].has_key('IVCurve'):
            print 'HasIV CURVE @ %s'%self.ParentObject.Attributes['TestTemperature'] 
            self.ResultData['KeyList'].append('CurrentAtVoltage150')
            result = self.ParentObject.ResultData['SubTestResults']['IVCurve'].ResultData
            if self.ParentObject.Attributes.has_key('recalculateCurrentTo'):
                print 'has recalculated Voltage: '
#                currentAtVoltage150 = result['KeyValueDictPairs']['recalculatedCurrentAtVoltage150V']['Value']
                self.ResultData['KeyValueDictPairs']['CurrentAtVoltage150'] = result['KeyValueDictPairs']['recalculatedCurrentAtVoltage150V']
                self.ResultData['KeyValueDictPairs']['CurrentAtVoltage150']['Label'] = 'I_rec(150 V) @ %s°C'%self.ParentObject.Attributes['recalculateCurrentTo']
                self.ResultData['KeyValueDictPairs']['CurrentAtVoltage150_ORIG'] = result['KeyValueDictPairs']['CurrentAtVoltage150']
                self.ResultData['KeyValueDictPairs']['CurrentAtVoltage150_ORIG']['Label'] = 'I_orig(150V) @ %s °C'%self.ParentObject.Attributes['TestTemperature']
                self.ResultData['KeyList'].append('CurrentAtVoltage150_ORIG')
            else:
                self.ResultData['KeyValueDictPairs']['CurrentAtVoltage150'] = result['KeyValueDictPairs']['CurrentAtVoltage150']
#                currentAtVoltage150 = result['KeyValueDictPairs']['CurrentAtVoltage150']['Value']
            self.ResultData['KeyList'].append('CurrentVariation')
            self.ResultData['KeyValueDictPairs']['CurrentVariation'] = result['KeyValueDictPairs']['Variation']
            
#            CurrentAtVoltage150 = result['KeyValueDictPairs']['Variation']['Value']
            
#        if self.ParentObject.ParentObject.ResultData['SubTestResults'].has_key('ModuleFulltest_p17_1'):
#            if self.ParentObject.ParentObject.ResultData['SubTestResults']['ModuleFulltest_p17_1'].ResultData['SubTestResults'].has_key('IVCurve'):
#                IVTestResultData = self.ParentObject.ParentObject.ResultData['SubTestResults']['ModuleFulltest_p17_1'].ResultData['SubTestResults']['IVCurve']
#                currentAtVoltage150 = IVTestResultData.ResultData['KeyValueDictPairs']['']['Value']
#                currentVariation = IVTestResultData.ResultData['KeyValueDictPairs']['Variation']['Value'], 
#                self.ResultData['KeyValueDictPairs']['CurrentAtVoltage150'] = {
#                        'Value': currentAtVoltage150,
#                        'Label':'I(150 V) @ 17°C',
#                        'Unit':'μA',
#                    }
#                self.ResultData['KeyValueDictPairs']['CurrentVariation'] = {
#                        'Value': currentVariation,
#                        'Label':'I(150 V) /I(100 V) @ 17°C',
#                    }
        
#       ,'CurrentAtVoltage150','CurrentVariation']
#         
#        if self.ParentObject.Attributes.has_key('recalculateCurrentTo'):
#            self.ResultData['KeyValueDictPairs']['recalculatedCurrentAtVoltage150V'] = {'Value':self.ParentObject.ResultData['SubTestResults']['IVCurve'].ResultData['KeyValueDictPairs']['recalculatedCurrentAtVoltage150V']['Value'],'Label':'recalculated IV','Unit':'μA',}
#            self.ResultData['KeyList'].append('recalculatedCurrentAtVoltage150V')   

