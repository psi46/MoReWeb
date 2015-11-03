# -*- coding: utf-8 -*-
import ROOT
import array
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter
import os
import ROOT

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Fulltest_Chips_Chip_AnalogCurrent_TestResult'
        self.NameSingle='AnalogCurrent'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'

    def PopulateResultData(self):
        ROOT.gStyle.SetOptStat(0)
        try:
            histname = self.ParentObject.HistoDict.get(self.NameSingle, 'AnalogCurrent')
            self.ResultData['Plot']['ROOTHisto'] = HistoGetter.get_histo(self.ParentObject.FileHandle, histname)
        except Exception as e:
            print e
            raise e
        self.ParentObject.ResultData['SubTestResults']['DigitalCurrent'].SpecialPopulateResultData(self,{'name':'Analog Current'})

        try:
            if os.path.isfile(self.ParentObject.logfilePath):
                with open(self.ParentObject.logfilePath, 'r') as logfile:
                    for line in logfile:
                        if 'setVana() done' in line and 'Module Ia' in line:
                            ModuleIa = line.split("Module Ia")[1].strip().split(" ")[0]
                            self.ResultData['KeyValueDictPairs']['ModuleIa'] = {
                                'Label': 'Module Ia',
                                'Value': ModuleIa,
                                'Unit': 'mA'
                            }
                            self.ResultData['KeyList'].append('ModuleIa')
                            print "Module Ia: ", ModuleIa, " => per ROC: ",float(ModuleIa)/16.0, " mA"
                            break
        except:
            pass
