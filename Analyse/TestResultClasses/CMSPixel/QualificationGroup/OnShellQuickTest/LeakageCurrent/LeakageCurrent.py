import ROOT
import AbstractClasses
import ROOT
from AbstractClasses.ModuleMap import ModuleMap
import os
import math

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.NameSingle = 'Leakagecurrent'
        self.Name = 'CMSPixel_QualificationGroup_OnShellQuickTest_Chips_Chip_{NameSingle}_TestResult'.format(NameSingle=self.NameSingle)
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'

        self.ResultData['KeyValueDictPairs']['I150'] = {'Value': '-', 'Label': 'I(150 V) max.', 'Unit': 'uA'}
        self.ResultData['KeyValueDictPairs']['I150Recalculated'] = {'Value': '-', 'Label': 'I(150 V) recalculated', 'Unit': 'uA'}
        self.ResultData['KeyValueDictPairs']['I150Initial'] = {'Value': '-', 'Label': 'I(150 V) initial', 'Unit': 'uA'}
        self.ResultData['KeyValueDictPairs']['I150Database'] = {'Value': '-', 'Label': 'I(150 V) Database', 'Unit': 'uA'}

        self.ResultData['KeyList'] += ['I150Recalculated', 'I150Initial', 'I150', 'I150Database']


    def recalculate_current(self, inputCurrent, inputTemp, outputTemp):
        inputTemp += 273.15
        outputTemp += 273.15
        Eef = 1.21
        kB = 8.62e-5
        exp = Eef / 2 / kB * (1 / inputTemp - 1 / outputTemp)
        outputCurrent = inputCurrent * outputTemp ** 2 / inputTemp ** 2 * math.exp(exp)
        return outputCurrent


    def PopulateResultData(self):
        ROOT.gStyle.SetOptStat(0)

        LeakageCurrentFileName = self.RawTestSessionDataPath + '/../logfiles/IV.log'

        if os.path.isfile(LeakageCurrentFileName):
            LeakageCurrentLines = []
            with open(LeakageCurrentFileName, 'r') as LeakageCurrentFile:
                LeakageCurrentLines = [x for x in LeakageCurrentFile.readlines() if not x.strip().startswith('#')]
            LeakageCurrentTuples = [[float(y) for y in x.strip().replace('\t', ' ').split(' ') if len(y) > 0] for x in LeakageCurrentLines]
            try:
                LeakageCurrentTuples = [x for x in LeakageCurrentTuples if abs(float(x[1])) > 1.0e-8]
            except:
                pass

            InitialLeakageCurrent = abs(float(LeakageCurrentTuples[0][1])) if len(LeakageCurrentTuples) > 0 else 0
            MaxLeakageCurrent = abs(float(max([abs(x[1]) for x in LeakageCurrentTuples]))) if len(LeakageCurrentTuples) > 0 else 0
            RecalculatedLeakageCurrent = self.recalculate_current(InitialLeakageCurrent, 21.0, 17.0) if len(LeakageCurrentTuples) > 0 else 0

            self.ResultData['KeyValueDictPairs']['I150']['Value'] = '%1.2f'%(MaxLeakageCurrent*1.0e6)
            self.ResultData['KeyValueDictPairs']['I150Initial']['Value'] = '%1.2f'%(InitialLeakageCurrent*1.0e6)
            self.ResultData['KeyValueDictPairs']['I150Recalculated']['Value'] = '%1.2f'%(RecalculatedLeakageCurrent*1.0e6)

        dbLeakageCurrentFileName = self.RawTestSessionDataPath + '/dbIvCurve.log'
        if os.path.isfile(dbLeakageCurrentFileName):
            with open(dbLeakageCurrentFileName, 'r') as dbLeakageCurrentFile:
                dbLeakageCurrentLines = [x for x in dbLeakageCurrentFile.readlines() if not x.strip().startswith('#')]
            dbLeakageCurrentTuples = [[float(y) for y in x.strip().replace('\t', ' ').split(' ') if len(y) > 0] for x in dbLeakageCurrentLines]
            for dbLeakageCurrentTuple in dbLeakageCurrentTuples:
                if abs(dbLeakageCurrentTuple[0]) > 147.0:
                    self.ResultData['KeyValueDictPairs']['I150Database']['Value'] = '%1.2f'%(abs(dbLeakageCurrentTuple[1])*1.0e6)
                    break
