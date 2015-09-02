# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import ROOT
import datetime
import os

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.NameSingle='TBM'
        self.Name='CMSPixel_QualificationGroup_Fulltest_%s_TestResult'%self.NameSingle
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
        self.Title = 'TBM'
        
    def PopulateResultData(self):
        self.ResultData['KeyValueDictPairs'] = {}
        self.ResultData['KeyList'] = []
        AllTBMCoreParameters = {}
        Directory = self.RawTestSessionDataPath
        TBMCores = ['a', 'b']

        TBMParametersFileBaseName = 'tbmParameters'
        nTBMs = 1
        TBMType = 'unknown'

        ConfigParametersFileName = Directory + "/configParameters.dat"
        if os.path.isfile(ConfigParametersFileName):
            with open(ConfigParametersFileName, 'r') as ConfigParametersFile:
                for line in ConfigParametersFile:
                    lineParts = line.strip().split(" ")
                    if len(lineParts) > 1 and lineParts[0] == 'tbmParameters':
                         TBMParametersFileBaseName = lineParts[1]
                    if len(lineParts) > 1 and lineParts[0] == 'nTbms':
                         nTBMs = int(lineParts[1])
                    if len(lineParts) > 1 and lineParts[0] == 'tbmType':
                         TBMType = lineParts[1]

        self.ResultData['KeyValueDictPairs']['nTBMs'] = {'Label' : 'n', 'Value' : nTBMs}
        self.ResultData['KeyList'].append('nTBMs')

        self.ResultData['KeyValueDictPairs']['TBMType'] = {'Label' : 'Type', 'Value' : TBMType}
        self.ResultData['KeyList'].append('TBMType')

        for iTBM in range(nTBMs):
            for TBMCore in TBMCores:
                TBMParametersFileName = Directory + "/%s_C%d%s.dat"%(TBMParametersFileBaseName, iTBM, TBMCore)
                if os.path.isfile(TBMParametersFileName):
                    TBMCoreParameters = {}
                    with open(TBMParametersFileName, 'r') as TBMParametersFile:
                        for line in TBMParametersFile:
                            lineParts = line.lower().strip().split(" ")
                            if "basea" in lineParts or "delays" in lineParts:
                                TBMCoreParameters['basea'] = lineParts[-1]
                            if "basee" in lineParts:
                                TBMCoreParameters['basee'] = lineParts[-1]

                    self.ResultData['KeyValueDictPairs']['Core%d%s_basea'%(iTBM, TBMCore)] = {'Label': 'Core %d%s base a'%(iTBM, TBMCore), 'Value': TBMCoreParameters['basea'] if 'basea' in TBMCoreParameters else 'None'}
                    self.ResultData['KeyValueDictPairs']['Core%d%s_basee'%(iTBM, TBMCore)] = {'Label': 'Core %d%s base e'%(iTBM, TBMCore), 'Value': TBMCoreParameters['basee'] if 'basee' in TBMCoreParameters else 'None'}
                    self.ResultData['KeyList'].append('Core%d%s_basea'%(iTBM, TBMCore))
                    self.ResultData['KeyList'].append('Core%d%s_basee'%(iTBM, TBMCore))

                    AllTBMCoreParameters["%d%s"%(iTBM, TBMCore)] = TBMCoreParameters

        try:
            # ROC delays
            delaysCh0 = int((AllTBMCoreParameters["0a"]["basea"].split("x"))[-1], 16) & int('00000111', 2)
            delaysCh1 = (int((AllTBMCoreParameters["0a"]["basea"].split("x"))[-1], 16) & int('00111000', 2)) >> 3
            delaysCh2 = int((AllTBMCoreParameters["0b"]["basea"].split("x"))[-1], 16) & int('00000111', 2)
            delaysCh3 = (int((AllTBMCoreParameters["0b"]["basea"].split("x"))[-1], 16) & int('00111000', 2)) >> 3

            self.ResultData['KeyValueDictPairs']['RocDelay_Ch0'] = {'Label': 'Roc Delay Ch0', 'Value': delaysCh0}
            self.ResultData['KeyValueDictPairs']['RocDelay_Ch1'] = {'Label': 'Roc Delay Ch1', 'Value': delaysCh1}
            self.ResultData['KeyValueDictPairs']['RocDelay_Ch2'] = {'Label': 'Roc Delay Ch2', 'Value': delaysCh2}
            self.ResultData['KeyValueDictPairs']['RocDelay_Ch3'] = {'Label': 'Roc Delay Ch3', 'Value': delaysCh3}
            self.ResultData['KeyList'].extend(['RocDelay_Ch0','RocDelay_Ch1','RocDelay_Ch2','RocDelay_Ch3'])

            # phases
            phase400 = (int((AllTBMCoreParameters["0a"]["basee"].split("x"))[-1], 16) & int('00011100', 2)) >> 2
            phase160 = (int((AllTBMCoreParameters["0a"]["basee"].split("x"))[-1], 16) & int('11100000', 2)) >> 5

            self.ResultData['KeyValueDictPairs']['Phase400'] = {'Label': 'Phase 400', 'Value': phase400}
            self.ResultData['KeyValueDictPairs']['Phase160'] = {'Label': 'Phase 160', 'Value': phase160}
            self.ResultData['KeyList'].extend(['Phase400','Phase160'])

        except:
            pass
