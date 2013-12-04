
# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import array
import math
import re
import warnings
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Fulltest_Chips_Chip_IVCurve_TestResult'
        self.NameSingle='IVCurve'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'
        self.ResultData['KeyValueDictPairs'] = {
            'CurrentAtVoltage150': {
                'Value':'{0:1.2f}'.format(0), 
                'Label':'I(150 V)',
                'Unit':'μA'
            },
            'Variation': {
                'Value':'{0:1.2f}'.format(0), 
                'Label':'I(150 V) / I(100 V)'
            }                                       
        }
        self.ResultData['KeyList'] = ['CurrentAtVoltage150','Variation']

        if self.ParentObject.Attributes.has_key('recalculateCurrentTo'):
            self.ResultData['KeyValueDictPairs']['recalculatedCurrentAtVoltage150V'] = {
                    'Value':'{0:1.2f}'.format(0), 
                    'Label':'I_rec(150 V, 17 degC))',
                    'Unit': 'μA'
                }
        self.ResultData['KeyList'].append('recalculatedCurrentAtVoltage150V')

    
    def recalculateCurrent(self,inputCurrent, inputTemp, outputTemp):
        inputTemp += 273.15
        outputTemp += 273.15
        Eef = 1.21
        kB = 8.62e-5
        exp = Eef/2/kB*(1/inputTemp-1/outputTemp)
        outputCurrent = inputCurrent * outputTemp**2/inputTemp**2 *math.exp(exp) 
        return outputCurrent

    def getFactorOfUnit(self,unitstring,unit):
        if not unitstring.endswith(unit):
            warnings.warn('Cannot extract Unit prefix for unit %s in unitstring  %s'%(unit,unitstring))
            return 1
        unitprefix= unitstring[:-len(unit)]
        unitprefix = unitprefix.strip()
        if 'T' == unitprefix:
            return 1e12
        elif 'G' == unitprefix:
            return 1e9
        elif 'M' == unitprefix:
            return 1e6
        elif 'k' == unitprefix:
            return 1e3
        elif 'h' == unitprefix:
            return 1e2
        elif '' == unitprefix:
            return 1
        elif 'd' == unitprefix:
            return 1e-1
        elif 'c' == unitprefix:
            return 1e-2
        elif 'm' == unitprefix:
            return 1e-3
        elif 'mu' in unitprefix or 'μ' == unitprefix:
            return 1e-6
        elif 'n' == unitprefix:
            return 1e-9
        elif 'p' == unitprefix:
            return 1e-12
        elif 'f' == unitprefix:
            return 1e-15
        else:
            warnings.warn('Cannot extract Unit prefix for unit %s in unitstring  %s'%(unit,unitstring))
            return 1
        return 1
    
    def analyseUnits(self,varlist,units):
        self.ResultData['HiddenData']['UnitV'] = 'V'
        self.ResultData['HiddenData']['UnitI'] = 'A'
        self.ResultData['HiddenData']['FactorV'] = 1
        self.ResultData['HiddenData']['FactorI'] = 1
        if len(varlist) != len(units):
            raise Exception('Cannot analyse Units of the IV tuples: %s,%s'%(varlist,units))
        currents = [i for i,x in enumerate(varlist) if 'current' in x.lower()]
        voltages = [i for i,x in enumerate(varlist) if 'voltage' in x.lower()]
        if len(currents) == 0:
            raise Exception('Cannot find column "current" in IV tuple: %s'%varlist)
        elif len(currents) > 1:
            warnings.warn('There is more than one possible candidate for current, taking the first: %s, %s'%(currents,varlist))
        currents = currents[0]
        if len(voltages) == 0:
            raise Exception('Cannot find column "voltages" i IV tuple: %s'%varlist)
        elif len(voltages) > 1:
            warnings.warn('There is more than one possible candidate for voltage, taking the first: %s, %s'%(voltages,varlist))
        voltages = voltages[0]
        if units[currents] == '':
            units[currents] = 'A'
        if units[voltages] == '':
            units[voltages] = 'V'
        
        if units[voltages].startswith('mu'):
            self.ResultData['HiddenData']['UnitV'] = '#' + units[voltages]
        else:
            self.ResultData['HiddenData']['UnitV'] = units[voltages]
        if units[currents].startswith('mu'):
            self.ResultData['HiddenData']['UnitI'] = '#'+units[currents]
        else:
            self.ResultData['HiddenData']['UnitI'] = units[currents]
        self.ResultData['HiddenData']['FactorI'] =self.getFactorOfUnit(units[currents],'A')
        self.ResultData['HiddenData']['FactorV'] =self.getFactorOfUnit(units[voltages],'V')
        
    def getIVTuple(self,fileName,analyser):
#         print analyser
        varlist = [re.sub("[\(\[].*?[\)\]]", "", entry).strip().title() for entry in analyser]
        units =  []
        for entry in analyser:
            group = re.compile('[\(\[]([^)]*)[\)\]]').search(entry)
            if group == None:
                units.append('')
            else:
                units.append(group.groups()[0].strip())
        
        self.analyseUnits(varlist,units)
        varlist = ':'.join(varlist)
        if 'Current' not in varlist or 'Voltage' not in varlist:
            raise Exception('Invalid IV Curve File, varlist:"%s"'%varlist)
#         print 'The varlist of the file "%s" is: "%s"'%(fileName,varlist)
        IVTuple = ROOT.TNtuple(self.GetUniqueID(),"IVTuple",varlist); # IVTuple
        IVTuple.ReadFile(fileName)
        self.ResultData['HiddenData']['IVTuple'] = IVTuple
        
        

    def PopulateResultData(self):
        ROOT.gPad.SetLogy(1);
        
        Directory = self.TestResultEnvironmentObject.ModuleDataDirectory+'/'+self.ParentObject.Attributes['IVCurveSubDirectory']
        
        IVCurveFileName =  "{Directory}/ivCurve.log".format(Directory=Directory);
        IVCurveFile = open(IVCurveFileName, "r");
        
        lines = IVCurveFile.readlines()
        lines = [line.replace('\n','') for line in lines]
        lines2 = [line for line in lines if line != '#' and 'LOG' not in line and line != '']
        
        analyser = ''
        if lines2[0].startswith('#'):
            analyser = lines2[0]
        else:
            analyser = ''
        analyser = analyser.strip('#').split('\t')
        if len(analyser) == 0:
            self.getIVTuple(IVCurveFileName,['voltage(V)','current(A)'])
        else:
            self.getIVTuple(IVCurveFileName,analyser)
                
        IVTuple = self.ResultData['HiddenData']['IVTuple']
        
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
            recalculatedCurrentAtVoltage150V *= self.ResultData['HiddenData']['FactorI']*1e6
            
        self.ResultData['Plot']['ROOTObject'] = ROOT.TGraph(len(Voltage_List), Voltage_List,Current_List);
        
        self.ResultData['Plot']['ROOTObject'].SetTitle('');
        self.ResultData['Plot']['ROOTObject'].SetLineColor(4);
        self.ResultData['Plot']['ROOTObject'].SetLineWidth(2);
        
        self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Voltage [%s]"%self.ResultData['HiddenData']['UnitV']);
        self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Current [%s]"%self.ResultData['HiddenData']['UnitI']);
        
        self.ResultData['Plot']['ROOTObject'].GetYaxis().SetDecimals();
        self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5);
        self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle();
        self.ResultData['Plot']['ROOTObject'].Draw("aC");
        
        CurrentAtVoltage150 *= self.ResultData['HiddenData']['FactorI']*1e6
        self.ResultData['KeyValueDictPairs']['CurrentAtVoltage150']['Value'] = '{0:1.2f}'.format(CurrentAtVoltage150)
        self.ResultData['KeyValueDictPairs']['Variation']['Value'] = '{0:1.2f}'.format(Variation)
                                            
        if self.ParentObject.Attributes.has_key('recalculateCurrentTo'):
            self.ResultData['KeyValueDictPairs']['recalculatedCurrentAtVoltage150V']['Value'] = '{0:1.2f}'.format(recalculatedCurrentAtVoltage150V) 
        if self.SavePlotFile:
            self.Canvas.SaveAs(self.GetPlotFileName())      
        self.ResultData['Plot']['Enabled'] = 1
        self.ResultData['Plot']['Caption'] = 'I-V-Curve'
        self.ResultData['Plot']['ImageFile'] = self.GetPlotFileName()
