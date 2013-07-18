# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import ROOT
import array
import math
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_ModuleTestGroup_Module_Chips_Chip_IVCurve_TestResult'
        self.NameSingle='IVCurve'
        self.Attributes['TestedObjectType'] = 'CMSPixel_ModuleTestGroup_Module_ROC'
        
    def SetStoragePath(self):
        pass
    
    def recalculateCurrent(self,inputCurrent, inputTemp, outputTemp):
        inputTemp += 273.15
        outputTemp += 273.15
        Eef = 1.21
        kB = 8.62e-5
        exp = Eef/2/kB*(1/inputTemp-1/outputTemp)
        outputCurrent = inputCurrent * outputTemp**2/inputTemp**2 *math.exp(exp) 
        return outputCurrent

    def PopulateResultData(self):
        ROOT.gPad.SetLogy(1);
        
        Directory = self.TestResultEnvironmentObject.TestResultsPath+'/'+self.ParentObject.Attributes['IVCurveSubDirectory']
        
        IVCurveFileName =  "{Directory}/ivCurve.log".format(Directory=Directory);
        IVCurveFile = open(IVCurveFileName, "r");

        IVTuple = ROOT.TNtuple(self.GetUniqueID(),"IVTuple","Timestamp:Voltage:Current"); # IVTuple
        
        
        
        IVTuple.ReadFile(IVCurveFileName);
        
        Voltage_List = array.array('d',[])
        Current_List = array.array('d',[])
        CurrentAtVoltage100 = 0;
        CurrentAtVoltage150 = 0;
        recalculatedCurrentAtVoltage150V = 0;
        NoOfEntries = min(IVTuple.GetEntries(), 250)
        i = 0
        for Entry in IVTuple:
            if Entry.Voltage <=0:
                Voltage_List.append(-1.*Entry.Voltage)
                Current_List.append(self.TestResultEnvironmentObject.GradingParameters['IVCurrentFactor']*Entry.Current)
                
                if Entry.Current>-1e-10:
                        continue;
                if i > 0:
                    
                    if Voltage_List[i] >= 100. and Voltage_List[i-1] <= 100. :  
                        CurrentAtVoltage100 = Current_List[i-1] + (100. - Voltage_List[i-1])*(Current_List[i] - Current_List[i-1])/(Voltage_List[i] - Voltage_List[i-1]) 
                    
                    if  Voltage_List[i] >= 150. and Voltage_List[i-1] <= 150. :
                        CurrentAtVoltage150 = Current_List[i-1] + (150. - Voltage_List[i-1])*(Current_List[i] - Current_List[i-1])/(Voltage_List[i] - Voltage_List[i-1])
                i += 1
        
        IVCurveFile.close()
        
        if CurrentAtVoltage100 != 0.:
            Variation = CurrentAtVoltage150/CurrentAtVoltage100
        else:
            Variation = 0;
        if self.ParentObject.Attributes.has_key('recalculateCurrentTo'):
            recalculatedCurrentAtVoltage150V = self.recalculateCurrent(CurrentAtVoltage150, self.ParentObject.Attributes['TestTemperature'],self.ParentObject.Attributes['recalculateCurrentTo'])
        
        #print Voltage_List
        
        self.ResultData['Plot']['ROOTObject'] = ROOT.TGraph(len(Voltage_List), Voltage_List,Current_List);
    
        
        self.ResultData['Plot']['ROOTObject'].SetTitle('');
        self.ResultData['Plot']['ROOTObject'].SetLineColor(4);
        self.ResultData['Plot']['ROOTObject'].SetLineWidth(2);
        
        self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Voltage [V]");
        self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Current [#muA]");
        
        self.ResultData['Plot']['ROOTObject'].GetYaxis().SetDecimals();
        self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5);
        self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle();
        self.ResultData['Plot']['ROOTObject'].Draw("aC");
        
        self.ResultData['KeyValueDictPairs'] = {
            'CurrentAtVoltage150': {
                'Value':'{0:1.2f}'.format(CurrentAtVoltage150), 
                'Label':'I(150 V)',
                'Unit':'μA'
            },
            'Variation': {
                'Value':'{0:1.2f}'.format(Variation), 
                'Label':'I(150 V) / I(100 V)'
            }                                       
                                            
        }
        self.ResultData['KeyList'] = ['CurrentAtVoltage150','Variation']
        if self.ParentObject.Attributes.has_key('recalculateCurrentTo'):
            self.ResultData['KeyValueDictPairs']['recalculatedCurrentAtVoltage150V'] = {
                    'Value':'{0:1.2f}'.format(recalculatedCurrentAtVoltage150V), 
                    'Label':'I_rec(150 V, 17 degC))',
                    'Unit': 'μA'
                }
            self.ResultData['KeyList'].append('recalculatedCurrentAtVoltage150V') 
        if self.SavePlotFile:
            self.Canvas.SaveAs(self.GetPlotFileName())      
        self.ResultData['Plot']['Enabled'] = 1
        self.ResultData['Plot']['Caption'] = 'I-V-Curve'
        self.ResultData['Plot']['ImageFile'] = self.GetPlotFileName()
