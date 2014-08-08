# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Fulltest_Summary3_TestResult'
        self.NameSingle='Summary3'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
        self.Title = 'Summary 3'

  
        
    def PopulateResultData(self):
        try:
            noise = self.ParentObject.ResultData['SubTestResults']['Noise'].ResultData['KeyValueDictPairs']['mu']['Value']
        except:
            noise  = -9999
            print "Summary3: cannot find ResultData['SubTestResults']['Noise'].ResultData['KeyValueDictPairs']['mu']['Value']"  
        try:
            vcalthrwidth = self.ParentObject.ResultData['SubTestResults']['VcalThresholdWidth'].ResultData['KeyValueDictPairs']['mu']['Value']
        except: 
            vcalthrwidth  = -9999
            print "Summary3: cannot find .ResultData['SubTestResults']['VcalThresholdWidth'].ResultData['KeyValueDictPairs']['mu']['Value']"
        try:
            relGainWidth = self.ParentObject.ResultData['SubTestResults']['RelativeGainWidth'].ResultData['KeyValueDictPairs']['mu']['Value']
        except:
            relGainWidth = -9999
            print "Summary3: cannot find ResultData['SubTestResults']['RelativeGainWidth'].ResultData['KeyValueDictPairs']['mu']['Value']"
        try:
            pedestalSpread = self.ParentObject.ResultData['SubTestResults']['PedestalSpread'].ResultData['KeyValueDictPairs']['mu']['Value']
        except:
            pedestalSpread = -9999
            print "Summary3: cannot find ResultData['SubTestResults']['PedestalSpread'].ResultData['KeyValueDictPairs']['mu']['Value']"
        try:
            parameter1 = self.ParentObject.ResultData['SubTestResults']['Parameter1'].ResultData['KeyValueDictPairs']['mu']['Value']
        except:
            parameter1 = -9999 
            print "Summary3: cannot find ResultData['SubTestResults']['PedestalSpread'].ResultData['KeyValueDictPairs']['mu']['Value']"
        
        nNoiseA = self.ParentObject.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs']['NoiseGradeAROCs']['Value']
        nNoiseB = self.ParentObject.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs']['NoiseGradeBROCs']['Value']
        nNoiseC = self.ParentObject.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs']['NoiseGradeCROCs']['Value']
        nVcalA =  self.ParentObject.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs']['VcalThresholdWidthGradeAROCs']['Value']
        nVcalB =  self.ParentObject.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs']['VcalThresholdWidthGradeBROCs']['Value']
        nVcalC =  self.ParentObject.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs']['VcalThresholdWidthGradeCROCs']['Value']
        nGainA =  self.ParentObject.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs']['RelativeGainWidthGradeAROCs']['Value']
        nGainB =  self.ParentObject.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs']['RelativeGainWidthGradeBROCs']['Value']
        nGainC =  self.ParentObject.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs']['RelativeGainWidthGradeCROCs']['Value']
        nPedA =   self.ParentObject.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs']['PedestalSpreadGradeAROCs']['Value']
        nPedB =   self.ParentObject.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs']['PedestalSpreadGradeBROCs']['Value']
        nPedC =   self.ParentObject.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs']['PedestalSpreadGradeCROCs']['Value']
        try:
            nPar1A =  self.ParentObject.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs']['Parameter1GradeAROCs']['Value']
        except:
            nPar1A = -1
        try:
            nPar1B =  self.ParentObject.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs']['Parameter1GradeBROCs']['Value']
        except:
            nPar1C = -1
        try:
            nPar1C =  self.ParentObject.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs']['Parameter1GradeCROCs']['Value']
        except:
            nPar1C = -1
        self.ResultData['KeyValueDictPairs'] = {
            'Noise': {
                'Value':noise, 
                'Label':'Noise',
                'Unit':'e',
            },
            'VcalThrWidth': {
                'Value':vcalthrwidth,
                'Label':'Vcal Thr. Width',
                'Unit':'e',
            },
            'RelGainWidth': {
                'Value':relGainWidth, 
                'Label':'Rel. Gain Width',
                'Unit':'%',
            },
            'PedestalSpread': {
                'Value':pedestalSpread, 
                'Label':'Pedestal Spread',
                'Unit':'e',
            },
            'Parameter1': {
                'Value':parameter1, 
                'Label':'Parameter1',
                'Unit':'',
            },
            'NoiseROCs': {
                'Value':'%d/%d/%d'%(nNoiseA,nNoiseB,nNoiseC), 
                'Label':'Noise grades',
            },
            'VcalThrWidthROCs': {
                'Value':'%d/%d/%d'%(nVcalA,nVcalB,nVcalC),
                'Label':'Vcal Thr. W. grades',
            },
            'RelGainWidthROCs': {
                'Value':'%d/%d/%d'%(nGainA,nGainB,nGainC),
                'Label':'Rel. Gain W. grades',
            },
            'PedestalSpreadROCs': {
                'Value':'%d/%d/%d'%(nPedA,nPedB,nPedC), 
                'Label':'Ped. Spread grades',
            },
            'Parameter1ROCs': {
                'Value':'%d/%d/%d'%(nPar1A,nPar1B,nPar1C),  
                'Label':'Par1 grades',
            },
        }
        self.ResultData['KeyList'] = ['Noise','NoiseROCs','VcalThrWidth','VcalThrWidthROCs','RelGainWidth','RelGainWidthROCs','PedestalSpread','PedestalSpreadROCs','Parameter1','Parameter1ROCs']
        if self.ParentObject.ResultData['SubTestResults'].has_key('IVCurve'):
            self.ResultData['KeyList'].append('CurrentAtVoltage150')
            result = self.ParentObject.ResultData['SubTestResults']['IVCurve'].ResultData
            if self.ParentObject.Attributes.has_key('recalculateCurrentTo'):
                self.ResultData['KeyValueDictPairs']['CurrentAtVoltage150'] = result['KeyValueDictPairs']['recalculatedCurrentAtVoltage150V']
                self.ResultData['KeyValueDictPairs']['CurrentAtVoltage150']['Label'] = 'I_rec(150 V) @ %s°C'%self.ParentObject.Attributes['recalculateCurrentTo']
                self.ResultData['KeyValueDictPairs']['CurrentAtVoltage150_ORIG'] = result['KeyValueDictPairs']['CurrentAtVoltage150']
                self.ResultData['KeyValueDictPairs']['CurrentAtVoltage150_ORIG']['Label'] = 'I_orig(150V) @ %s °C'%self.ParentObject.Attributes['TestTemperature']
                self.ResultData['KeyList'].append('CurrentAtVoltage150_ORIG')
            else:
                self.ResultData['KeyValueDictPairs']['CurrentAtVoltage150'] = result['KeyValueDictPairs']['CurrentAtVoltage150']
            self.ResultData['KeyList'].append('CurrentVariation')
            self.ResultData['KeyValueDictPairs']['CurrentVariation'] = result['KeyValueDictPairs']['Variation']
            
