# -*- coding: utf-8 -*-
import array
import math
import re
import warnings
# from AbstractClasses.Helper import helper
import AbstractClasses.Helper.helper as helper
import ROOT

from AbstractClasses.GeneralTestResult import GeneralTestResult


class TestResult(GeneralTestResult):
    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_Fulltest_Chips_Chip_IVCurve_TestResult'
        self.NameSingle = 'IVCurve'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'
        self.ResultData['KeyValueDictPairs'] = {
            'CurrentAtVoltage150V': {
                'Value': '{0:1.2f}'.format(0),
                'Label': 'I(150 V)',
                'Unit': 'μA',
                'Factor': 1e-6
            },
            'Variation': {
                'Value': '{0:1.2f}'.format(0),
                'Label': 'I(150 V) / I(100 V)'
            }
        }
        self.ResultData['KeyList'] = ['CurrentAtVoltage150V', 'Variation']

        if self.ParentObject.Attributes.has_key('recalculateCurrentTo'):
            self.ResultData['KeyValueDictPairs']['recalculatedCurrentAtVoltage150V'] = {
                'Value': '{0:1.2f}'.format(0),
                'Label': 'I_rec(150 V, 17 degC))',
                'Unit': 'μA',
                'Factor': 1e-6
            }
            self.ResultData['KeyValueDictPairs']['CurrentAtVoltage150V']['Label'] = 'I_rec(150 V, {temp} degC'.format(temp = self.ParentObject.Attributes['TestTemperature'])
            self.ResultData['KeyList'].append('recalculatedCurrentAtVoltage150V')
            self.ResultData['KeyValueDictPairs']['recalculatedCurrentVariation'] = {
                'Value': '{0:1.2f}'.format(0),
                'Label': 'I_rec(150 V) / I_rec(100 V)'
            }
            self.ResultData['KeyList'].append('recalculatedCurrentVariation')

    @staticmethod
    def recalculate_current(inputCurrent, inputTemp, outputTemp):
        inputTemp += 273.15
        outputTemp += 273.15
        Eef = 1.21
        kB = 8.62e-5
        exp = Eef / 2 / kB * (1 / inputTemp - 1 / outputTemp)
        outputCurrent = inputCurrent * outputTemp ** 2 / inputTemp ** 2 * math.exp(exp)
        return outputCurrent

    def analyseUnits(self, varlist, units):
        self.ResultData['HiddenData']['UnitV'] = 'V'
        self.ResultData['HiddenData']['UnitI'] = 'A'
        self.ResultData['HiddenData']['FactorV'] = 1
        self.ResultData['HiddenData']['FactorI'] = 1
        if len(varlist) != len(units):
            raise Exception('Cannot analyse Units of the IV tuples: %s,%s' % (varlist, units))
        currents = [i for i, x in enumerate(varlist) if 'current' in x.lower()]
        voltages = [i for i, x in enumerate(varlist) if 'voltage' in x.lower()]
        if len(currents) == 0:
            raise Exception('Cannot find column "current" in IV tuple: %s' % varlist)
        elif len(currents) > 1:
            warnings.warn(
                'There is more than one possible candidate for current, taking the first: %s, %s' % (currents, varlist))
        currents = currents[0]
        if len(voltages) == 0:
            raise Exception('Cannot find column "voltages" i IV tuple: %s' % varlist)
        elif len(voltages) > 1:
            warnings.warn(
                'There is more than one possible candidate for voltage, taking the first: %s, %s' % (voltages, varlist))
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
            self.ResultData['HiddenData']['UnitI'] = '#' + units[currents]
        else:
            self.ResultData['HiddenData']['UnitI'] = units[currents]
        self.ResultData['HiddenData']['FactorI'] = helper.get_factor_of_unit(units[currents], 'A')
        self.ResultData['HiddenData']['FactorV'] = helper.get_factor_of_unit(units[voltages], 'V')

    def getIVTuple(self, fileName, analyser):
        # print analyser
        varlist = [re.sub("[\(\[].*?[\)\]]", "", entry).strip().title() for entry in analyser]
        units = []
        for entry in analyser:
            group = re.compile('[\(\[]([^)]*)[\)\]]').search(entry)
            if group is None:
                units.append('')
            else:
                units.append(group.groups()[0].strip())

        self.analyseUnits(varlist, units)

        varlist = ':'.join(varlist)
        if 'Current' not in varlist or 'Voltage' not in varlist:
            raise Exception('Invalid IV Curve File, varlist:"%s"' % varlist)
        if self.verbose:
            print 'The varlist of the file "%s" is: "%s"' % (fileName, varlist)

        varlistSave = "Voltage:Current"
        IVTuple = ROOT.TNtuple(self.GetUniqueID(), "IVTuple", varlistSave)  # IVTuple

        IVCurveFile = open(fileName, "r")
        lines = IVCurveFile.readlines()
        lines = [line.replace('\n', '') for line in lines if not line.strip().startswith('#')]

        IndexCurrent = analyser.index("current(A)")
        IndexVoltage = analyser.index("voltage(V)")

        entries = 0
        for line in lines:
            values = line.strip().split("\t")
            IVTuple.Fill(float(values[IndexVoltage]), float(values[IndexCurrent]))
            entries += 1

        IVCurveFile.close()

        print 'read {entries} Entries from file {fileName}'.format(entries=entries, fileName=fileName)
        self.ResultData['HiddenData']['IVTuple'] = IVTuple

    def AnalyzeIVCurveFile(self, IVCurveFileName):
        IVCurveFile = open(IVCurveFileName, "r")
        
        self.ResultData['HiddenData']['IVCurveFilePath'] = IVCurveFileName
        self.ResultData['HiddenData']['TestTemperature'] = self.ParentObject.Attributes['TestTemperature']

        lines = IVCurveFile.readlines()
        lines = [line.replace('\n', '') for line in lines]

        VoltageColumnDescription = 'voltage(V)'
        CurrentColumnDescription = 'current(A)'

        ColumnDescriptorLines = [line for line in lines if line.strip().startswith('#') and VoltageColumnDescription in line and CurrentColumnDescription in line]

        if len(ColumnDescriptorLines) >= 1:
            analyser = ColumnDescriptorLines[0].strip('#').split('\t')
            if len(ColumnDescriptorLines) > 1:
                print "Multiple lines with column descriptions 'voltage(V)' and 'current(A)' found in file '%s', using first one."%IVCurveFileName
        else:
            analyser = [VoltageColumnDescription, CurrentColumnDescription]
            print "No line with column descriptions 'voltage(V)' and 'current(A)' found in file '%s', using default one."%IVCurveFileName

        self.getIVTuple(IVCurveFileName, analyser)

        IVTuple = self.ResultData['HiddenData']['IVTuple']

        Voltage_List = array.array('d', [])
        Current_List = array.array('d', [])
        CurrentAtVoltage100V = 0
        CurrentAtVoltage150V = 0
        # NoOfEntries = min(IVTuple.GetEntries(), 250)
        i = 0
        l = False
        if self.verbose:
            IVTuple.Print()
            print IVTuple, type(IVTuple), IVTuple.GetEntries()
        for Entry in IVTuple:
            try:
                voltage = Entry.Voltage
            except TypeError as e:
                if not l:
                    text = 'Fulltest.IVCurve: {Exception}'.format(Exception=e)
                    print text
                    warnings.warn(text)
                    l = True
                continue
                pass
            if voltage <= 0:
                if Entry.Current > -1e-10:
                    continue
                Voltage_List.append(-1. * voltage)
                Current_List.append(
                    self.TestResultEnvironmentObject.GradingParameters['IVCurrentFactor'] * Entry.Current)

                if i > 0:

                    if Voltage_List[i] >= 100. >= Voltage_List[i - 1]:
                        CurrentAtVoltage100V = Current_List[i - 1] + (100. - Voltage_List[i - 1]) * (
                            Current_List[i] - Current_List[i - 1]) / (Voltage_List[i] - Voltage_List[i - 1])

                    if Voltage_List[i] >= 150. >= Voltage_List[i - 1]:
                        CurrentAtVoltage150V = Current_List[i - 1] + (150. - Voltage_List[i - 1]) * (
                            Current_List[i] - Current_List[i - 1]) / (Voltage_List[i] - Voltage_List[i - 1])
                i += 1

        IVCurveFile.close()
        
        return [Voltage_List, Current_List, CurrentAtVoltage100V, CurrentAtVoltage150V]

    def PopulateResultData(self):
        ROOT.gPad.SetLogy(1)

        Directory = self.TestResultEnvironmentObject.ModuleDataDirectory + '/' + self.ParentObject.Attributes[
            'IVCurveSubDirectory']
        IVCurveFileName = "{Directory}/ivCurve.log".format(Directory=Directory)
        
        Voltage_List, Current_List, CurrentAtVoltage100V, CurrentAtVoltage150V = self.AnalyzeIVCurveFile(IVCurveFileName)

        self.ResultData['HiddenData']['IVCurveData'] = {
            'VoltageList':Voltage_List,
            'CurrentList':Current_List
        }
        
        # slope
        if CurrentAtVoltage100V != 0.:
            Variation = CurrentAtVoltage150V / CurrentAtVoltage100V
        else:
            Variation = 0

        # recalculation
        recalculatedCurrentAtVoltage150V = 0
        if self.ParentObject.Attributes.has_key('recalculateCurrentTo'):
            recalculatedCurrentAtVoltage150V = self.recalculate_current(CurrentAtVoltage150V,
                                                                        self.ParentObject.Attributes['TestTemperature'],
                                                                        self.ParentObject.Attributes[
                                                                            'recalculateCurrentTo'])

            recalculatedCurrentAtVoltage100V = self.recalculate_current(CurrentAtVoltage100V,
                                                                        self.ParentObject.Attributes['TestTemperature'],
                                                                        self.ParentObject.Attributes[
                                                                            'recalculateCurrentTo'])
            recalculatedCurrentAtVoltage100V *= self.ResultData['HiddenData']['FactorI']
            recalculatedCurrentVariation = 0
            if recalculatedCurrentAtVoltage100V != 0:
                recalculatedCurrentVariation = recalculatedCurrentAtVoltage150V / recalculatedCurrentAtVoltage100V
            else:
                recalculatedCurrentVariation = 0

        # ratio +17 / -20 (if applicable)
        LowTemperatureEnvironment = 'm20'
        HighTemperatureEnvironment = 'p17'

        if LowTemperatureEnvironment in self.TestResultEnvironmentObject.IVCurveFiles:
            IVCurveFilesListLowT = sorted(self.TestResultEnvironmentObject.IVCurveFiles[LowTemperatureEnvironment])
        else:
            IVCurveFilesListLowT = []


        #only for the first IV at low T
        if len(IVCurveFilesListLowT) > 0:
            if self.ParentObject.Attributes['IVCurveSubDirectory'] == IVCurveFilesListLowT[0]:
                if HighTemperatureEnvironment in self.TestResultEnvironmentObject.IVCurveFiles:
                    IVCurveFilesListHighT = sorted(self.TestResultEnvironmentObject.IVCurveFiles[HighTemperatureEnvironment])
                else:
                    IVCurveFilesListHighT = []


                if len(IVCurveFilesListHighT) > 1:
                    print "more than 1 IV curves for %s found, using first one: %s"%(HighTemperatureEnvironment, IVCurveFilesListHighT[0])

                if len(IVCurveFilesListHighT) > 0:
                    IVCurveFileNameHighT = "{Directory}/ivCurve.log".format(Directory=self.TestResultEnvironmentObject.ModuleDataDirectory + '/' + IVCurveFilesListHighT[0])
                    IVDataHighT = self.AnalyzeIVCurveFile(IVCurveFileNameHighT)
                    CurrentAtVoltage100VHighT = IVDataHighT[2]
                    CurrentAtVoltage150VHighT = IVDataHighT[3]

                    CurrentRatio100V = abs(CurrentAtVoltage100VHighT / CurrentAtVoltage100V) if abs(CurrentAtVoltage100V) > 0 else -1
                    CurrentRatio150V = abs(CurrentAtVoltage150VHighT / CurrentAtVoltage150V) if abs(CurrentAtVoltage150V) > 0 else -1

                    self.ResultData['KeyValueDictPairs']['CurrentRatio100V'] = {'Label': 'I(+17C)/I(-20C) 100V', 'Value': '{0:1.2f}'.format(CurrentRatio100V)}
                    self.ResultData['KeyValueDictPairs']['CurrentRatio150V'] = {'Label': 'I(+17C)/I(-20C) 150V', 'Value': '{0:1.2f}'.format(CurrentRatio150V)}
                    self.ResultData['KeyList'].append('CurrentRatio100V')
                    self.ResultData['KeyList'].append('CurrentRatio150V')
                    print "Low T IV curves: ", IVCurveFilesListLowT
                    print "High T IV curves: ", IVCurveFilesListHighT
                    print "LEAKAGE CURRENT RATIO: ", CurrentRatio150V
                else:
                    print "no %s IV for current ratio found :-("%HighTemperatureEnvironment
        else:
            # if IV curve at low T is missing, ignore grading on ratio, bu print warning
            if 'Reception' not in self.Attributes or ('Reception' in self.Attributes and not self.Attributes['Reception']):
                print "#"*80,"\nWARNING: IV curve at low temperature is missing, no grading on ratio is done!\n","#"*80

        # plot
        if len(Voltage_List) == 0:
            self.ResultData['Plot']['ROOTObject'] = ROOT.TGraph()
        else:
            self.ResultData['Plot']['ROOTObject'] = ROOT.TGraph(len(Voltage_List), Voltage_List, Current_List)

        self.ResultData['Plot']['ROOTObject'].SetTitle('')
        self.ResultData['Plot']['ROOTObject'].SetLineColor(4)
        self.ResultData['Plot']['ROOTObject'].SetLineWidth(2)

        self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle(
            "Voltage [%s]" % self.ResultData['HiddenData']['UnitV'])
        self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle(
            "Current [%s]" % self.ResultData['HiddenData']['UnitI'])

        self.ResultData['Plot']['ROOTObject'].GetYaxis().SetDecimals()
        self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
        self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
        self.ResultData['Plot']['ROOTObject'].Draw("aC")

        CurrentAtVoltage150V *= self.ResultData['HiddenData']['FactorI'] 
        CurrentAtVoltage150V *= 1./self.ResultData['KeyValueDictPairs']['CurrentAtVoltage150V']['Factor'] #to show the value in muA and not in A
        self.ResultData['KeyValueDictPairs']['CurrentAtVoltage150V']['Value'] = '{0:1.2f}'.format(CurrentAtVoltage150V)
        
        CurrentAtVoltage100V *= self.ResultData['HiddenData']['FactorI'] 
        self.ResultData['HiddenData']['CurrentAtVoltage100V'] = CurrentAtVoltage100V
        self.ResultData['KeyValueDictPairs']['Variation']['Value'] = '{0:1.2f}'.format(Variation)

        if self.ParentObject.Attributes.has_key('recalculateCurrentTo'):
            recalculatedCurrentAtVoltage150V *= 1./self.ResultData['KeyValueDictPairs']['recalculatedCurrentAtVoltage150V']['Factor']
            self.ResultData['KeyValueDictPairs']['recalculatedCurrentAtVoltage150V']['Value'] = '{0:1.2f}'.format(
                recalculatedCurrentAtVoltage150V)
            self.ResultData['KeyValueDictPairs']['recalculatedCurrentVariation']['Value'] = '{0:1.2f}'.format(
                recalculatedCurrentVariation)
        self.ResultData['Plot']['Caption'] = 'I-V-Curve'
        self.SaveCanvas()
        self.ResultData['Plot']['ImageFile'] = self.GetPlotFileName()
        if self.verbose:
            print  self.ResultData['Plot']['Caption'] 
            for key in  self.ResultData['KeyValueDictPairs']:
                print '*',key,self.ResultData['KeyValueDictPairs'][key]['Value'],self.ResultData['KeyValueDictPairs'][key].get('Unit',None),self.ResultData['KeyValueDictPairs'][key].get('Factor',None)
            #raw_input ('press enter')
        
