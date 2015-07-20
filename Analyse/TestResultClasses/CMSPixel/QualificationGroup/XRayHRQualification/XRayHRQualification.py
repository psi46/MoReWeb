import os
import sys
import ROOT
import os.path
import glob

import AbstractClasses
from AbstractClasses.Helper.BetterConfigParser import BetterConfigParser

from AbstractClasses.GeneralTestResult import GeneralTestResult
import subprocess

class TestResult(GeneralTestResult):
    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_XRayHRQualification_TestResult'
        self.NameSingle = 'XRayHRQualification'
        self.Title = str(self.Attributes['ModuleID']) + ' ' + self.Attributes['StorageKey']
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
        self.Attributes['NumberOfChips'] = self.nTotalChips
        #self.MergePyxarData()

        if self.Attributes['ModuleVersion'] == 1:
            if self.Attributes['ModuleType'] == 'a':
                self.Attributes['StartChip'] = 0
            elif self.Attributes['ModuleType'] == 'b':
                self.Attributes['StartChip'] = 7
            else:
                self.Attributes['StartChip'] = 0

        elif self.Attributes['ModuleVersion'] == 2:
            self.Attributes['StartChip'] = 0
        elif self.Attributes['ModuleVersion'] == 3:
            self.Attributes['NumberOfChips'] = 1
            self.Attributes['StartChip'] = 0
        
        self.Attributes['Rates'] = {
            'HREfficiency':[],
            'HRData':[],
            'HRSCurves':[]
        }

        self.FileHandle = []

        self.Attributes['InterpolatedEfficiencyRates'] = []
        for r in range(1, int(1 + self.TestResultEnvironmentObject.GradingParameters['XRayHighRateEfficiency_NInterpolationRates'])):
            self.Attributes['InterpolatedEfficiencyRates'].append(int(self.TestResultEnvironmentObject.GradingParameters['XRayHighRateEfficiency_InterpolationRate%d'%r]))

        self.Attributes['ROOTFiles'] = {}
        self.Attributes['SCurvePaths'] = {}
        self.Attributes['Ntrig'] = {}
            
        HREfficiencyPaths = glob.glob(self.RawTestSessionDataPath+'/0[0-9][0-9]_HREfficiency_*')
        for Path in HREfficiencyPaths:
            FolderName = os.path.basename(Path)
            Rate = int(FolderName.split('_')[2])
            self.Attributes['Rates']['HREfficiency'].append(Rate)
            ROOTFiles = glob.glob(Path+'/*.root')
            self.Attributes['ROOTFiles']['HREfficiency_{Rate}'.format(Rate=Rate)] = ROOT.TFile.Open(ROOTFiles[0])
            self.FileHandle.append(self.Attributes['ROOTFiles']['HREfficiency_{Rate}'.format(Rate=Rate)])

            self.Attributes['Ntrig']['HREfficiency_{Rate}'.format(Rate=Rate)] = 50 #pxar default
            NTriggersReadFromFile = False            
            testParametersFilename = "/".join(ROOTFiles[0].split("/")[0:-1]) + "/testParameters.dat"
            if os.path.exists(testParametersFilename):
                testParametersFile = open(testParametersFilename, "r")
                if testParametersFile:
                    testParametersSection = ""
                    for line in testParametersFile:
                        sline = line.strip()
                        if sline[0:2] == "--":
                            testParametersSection = sline[2:].strip()
                        elements = sline.strip().split(" ")
                        if testParametersSection.lower() == "highrate" and elements[0].lower() == "ntrig":
                            NTriggersReadFromFile = True
                            self.Attributes['Ntrig']['HREfficiency_{Rate}'.format(Rate=Rate)] = float(elements[-1])
                    testParametersFile.close()
            if not NTriggersReadFromFile:
                print '\x1b[31mWARNING: testParameters.dat file not found in "%s", using default number of triggers Ntrig = %d\x1b[0m'%(FolderName, self.Attributes['Ntrig']['HREfficiency_{Rate}'.format(Rate=Rate)])

        HRDataPaths = glob.glob(self.RawTestSessionDataPath+'/0[0-9][0-9]_HRData_*')
        for Path in HRDataPaths:
            FolderName = os.path.basename(Path)
            Rate = int(FolderName.split('_')[2])
            self.Attributes['Rates']['HRData'].append(Rate)
            ROOTFiles = glob.glob(Path+'/*.root')
            self.Attributes['ROOTFiles']['HRData_{Rate}'.format(Rate=Rate)] = ROOT.TFile.Open(ROOTFiles[0])
            self.FileHandle.append(self.Attributes['ROOTFiles']['HRData_{Rate}'.format(Rate=Rate)])


        HRSCurvesPaths = glob.glob(self.RawTestSessionDataPath+'/0[0-9][0-9]_HRS[Cc]urves_*')
        for Path in HRSCurvesPaths:
            FolderName = os.path.basename(Path)
            Rate = int(FolderName.split('_')[2])
            self.Attributes['Rates']['HRSCurves'].append(Rate)
            self.Attributes['SCurvePaths']['HRSCurves_{Rate}'.format(Rate=Rate)] = Path


        HRHotPixelsPaths = glob.glob(self.RawTestSessionDataPath+'/0[0-9][0-9]_MaskHotPixels_*')
        if len(HRHotPixelsPaths) > 1:
                warnings.warn("multiple MaskHotPixel tests found")

        for Path in HRHotPixelsPaths:
            FolderName = os.path.basename(Path)
            ROOTFiles = glob.glob(Path+'/*.root')
            if len(ROOTFiles) > 1:
                warnings.warn("The directory '%s' contains more than one .root file, choosing first one: '%s'"%(FolderName, ROOTFiles[0]))
            self.Attributes['ROOTFiles']['MaskHotPixels'] = ROOT.TFile.Open(ROOTFiles[0])
            self.FileHandle.append(self.Attributes['ROOTFiles']['MaskHotPixels'])
            break

        PixelAlivePaths = glob.glob(self.RawTestSessionDataPath+'/0[0-9][0-9]_PixelAlive_*')
        for Path in PixelAlivePaths:
            ROOTFiles = glob.glob(Path+'/*.root')
            self.Attributes['ROOTFiles']['PixelAlive'] = ROOT.TFile.Open(ROOTFiles[0])
            self.FileHandle.append(self.Attributes['ROOTFiles']['PixelAlive'])

        CalDelScanPaths = glob.glob(self.RawTestSessionDataPath+'/0[0-9][0-9]_CalDel*_*')
        for Path in CalDelScanPaths:
            ROOTFiles = glob.glob(Path+'/*.root')
            if len(ROOTFiles) > 0:
                self.Attributes['ROOTFiles']['CalDelScan'] = ROOT.TFile.Open(ROOTFiles[0])
                self.FileHandle.append(self.Attributes['ROOTFiles']['CalDelScan'])

        self.ResultData['SubTestResultDictList'] = []

        for Rate in self.Attributes['Rates']['HRSCurves']:
            self.ResultData['SubTestResultDictList'].append({
                'Key': 'Fitting_{Rate}'.format(Rate=Rate),
                'Module': 'Fitting',
                'DisplayOptions': {
                    'Order': 99,
                    'Show': False,
                },
                'InitialAttributes': {
                    'Rate': Rate,
                    'ModuleVersion': self.Attributes['ModuleVersion'],
                },
            })

        self.ResultData['SubTestResultDictList'] += [
            {
                'Key': 'Chips',
                'DisplayOptions': {
                    'GroupWithNext': True,
                    'Order': 1,
                },
                'InitialAttributes': {
                    'ModuleVersion': self.Attributes['ModuleVersion'],
                },
            },
            {
                'Key': 'Grading',
                'DisplayOptions': {
                    'GroupWithNext': True,
                    'Order': 99,
                    'Show': False,
                },
                'InitialAttributes': {
                    'ModuleVersion': self.Attributes['ModuleVersion'],
                },
            },
            {
                'Key': 'Summary',
                'DisplayOptions': {
                    'GroupWithNext': False,
                    'Order': 2,
                },
                'InitialAttributes': {
                    'ModuleVersion': self.Attributes['ModuleVersion'],
                },
            }
        ]

        # value per ROC summary plots
        self.ResultData['SubTestResultDictList'].append({
                'Key': 'AliveOverview',
                'Module': 'AliveOverview',
                'DisplayOptions': {
                    'Width': 4,
                    'Order': 40,
                },
                'InitialAttributes': {
                    'NumberOfChips': self.Attributes['NumberOfChips'],
                    'StorageKey': 'AliveOverview'
                },
            })
        self.ResultData['SubTestResultDictList'].append({
                'Key': 'AliveSummary',
                'Module': 'AliveSummary',
                'DisplayOptions': {
                    'Width': 1,
                    'Order': 40,
                },
                'InitialAttributes': {
                    'NumberOfChips': self.Attributes['NumberOfChips'],
                    'StorageKey': 'AliveSummary'
                },
            })
        for Rate in self.Attributes['InterpolatedEfficiencyRates']:
            self.ResultData['SubTestResultDictList'].append({
                'Key': 'EfficiencySummary_{Rate}'.format(Rate=Rate),
                'Module': 'EfficiencySummary',
                'DisplayOptions': {
                    'Width': 1,
                    'Order': 6,
                },
                'InitialAttributes': {
                    'Rate': Rate,
                    'NumberOfChips': self.Attributes['NumberOfChips'],
                    'StorageKey': 'EfficiencySummary_{Rate}'.format(Rate=Rate)
                },
            })
        for Rate in self.Attributes['Rates']['HRData']:
            self.ResultData['SubTestResultDictList'].append({
                'Key': 'BumpBondingSummary_{Rate}'.format(Rate=Rate),
                'Module': 'BumpBondingSummary',
                'DisplayOptions': {
                    'Width': 1,
                    'Order': 7,
                },
                'InitialAttributes': {
                    'Rate': Rate,
                    'NumberOfChips': self.Attributes['NumberOfChips'],
                    'StorageKey': 'BumpBondingSummary_{Rate}'.format(Rate=Rate)
                },
            })
        for Rate in self.Attributes['Rates']['HRSCurves']:
            self.ResultData['SubTestResultDictList'].append({
                'Key': 'NoiseSummary_{Rate}'.format(Rate=Rate),
                'Module': 'NoiseSummary',
                'DisplayOptions': {
                    'Width': 1,
                    'Order': 8,
                },
                'InitialAttributes': {
                    'Rate': Rate,
                    'NumberOfChips': self.Attributes['NumberOfChips'],
                    'StorageKey': 'NoiseSummary_{Rate}'.format(Rate=Rate)
                },
            })

        # value per pixel + distribution summary plots
        for Rate in self.Attributes['Rates']['HRData']:
            self.ResultData['SubTestResultDictList'].append({
                'Key': 'HitOverview_{Rate}'.format(Rate=Rate),
                'Module': 'HitOverview',
                'DisplayOptions': {
                    'Width': 4,
                    'Order': 9,
                },
                'InitialAttributes': {
                    'Rate': Rate,
                    'NumberOfChips': self.Attributes['NumberOfChips'],
                    'StorageKey': 'HitOverview_{Rate}'.format(Rate=Rate)
                },
            })
            self.ResultData['SubTestResultDictList'].append({
                'Key': 'HitMapDistribution_{Rate}'.format(Rate=Rate),
                'Module': 'HitMapDistribution',
                'DisplayOptions': {
                    'Width': 1,
                    'Order': 9,
                },
                'InitialAttributes': {
                    'Rate': Rate,
                    'NumberOfChips': self.Attributes['NumberOfChips'],
                    'StorageKey': 'HitMapDistribution_{Rate}'.format(Rate=Rate)
                },
            })

        for Rate in self.Attributes['Rates']['HRData']:
            self.ResultData['SubTestResultDictList'].append({
                'Key': 'HotPixelOverview_{Rate}'.format(Rate=Rate),
                'Module': 'HotPixelOverview',
                'DisplayOptions': {
                    'Width': 4,
                    'Order': 20,
                },
                'InitialAttributes': {
                    'Rate': Rate,
                    'NumberOfChips': self.Attributes['NumberOfChips'],
                    'StorageKey': 'HotPixelOverview_{Rate}'.format(Rate=Rate)
                },
            })
            self.ResultData['SubTestResultDictList'].append({
                'Key': 'HotPixelSummary_{Rate}'.format(Rate=Rate),
                'Module': 'HotPixelSummary',
                'DisplayOptions': {
                    'Width': 1,
                    'Order': 20,
                },
                'InitialAttributes': {
                    'Rate': Rate,
                    'NumberOfChips': self.Attributes['NumberOfChips'],
                    'StorageKey': 'HotPixelSummary_{Rate}'.format(Rate=Rate)
                },
            })

        for Rate in self.Attributes['Rates']['HRData']:
            self.ResultData['SubTestResultDictList'].append({
                'Key': 'BumpBondingProblems_{Rate}'.format(Rate=Rate),
                'Module': 'BumpBondingProblems',
                'DisplayOptions': {
                    'Width': 4,
                    'Order': 10,
                },
                'InitialAttributes': {
                    'Rate': Rate,
                    'NumberOfChips': self.Attributes['NumberOfChips'],
                    'StorageKey': 'BumpBondingProblems_{Rate}'.format(Rate=Rate)
                },
            })
            self.ResultData['SubTestResultDictList'].append({
                'Key': 'BumpBondingSummary_{Rate}'.format(Rate=Rate),
                'Module': 'BumpBondingSummary',
                'DisplayOptions': {
                    'Width': 1,
                    'Order': 10,
                },
                'InitialAttributes': {
                    'Rate': Rate,
                    'NumberOfChips': self.Attributes['NumberOfChips'],
                    'StorageKey': 'BumpBondingSummary_{Rate}'.format(Rate=Rate)
                },
            })

        for Rate in self.Attributes['Rates']['HRSCurves']:
            self.ResultData['SubTestResultDictList'].append({
                'Key': 'ThresholdOverview_{Rate}'.format(Rate=Rate),
                'Module': 'ThresholdOverview',
                'DisplayOptions': {
                    'Width': 4,
                    'Order': 30,
                },
                'InitialAttributes': {
                    'Rate': Rate,
                    'NumberOfChips': self.Attributes['NumberOfChips'],
                    'StorageKey': 'ThresholdOverview_{Rate}'.format(Rate=Rate)
                },
            })
            self.ResultData['SubTestResultDictList'].append({
                'Key': 'ThresholdDistribution_{Rate}'.format(Rate=Rate),
                'Module': 'ThresholdDistribution',
                'DisplayOptions': {
                    'Width': 1,
                    'Order': 30,
                },
                'InitialAttributes': {
                    'Rate': Rate,
                    'NumberOfChips': self.Attributes['NumberOfChips'],
                    'StorageKey': 'ThresholdDistribution_{Rate}'.format(Rate=Rate)
                },
            })

        for Rate in self.Attributes['Rates']['HRSCurves']:
            self.ResultData['SubTestResultDictList'].append({
                'Key': 'NoiseOverview_{Rate}'.format(Rate=Rate),
                'Module': 'NoiseOverview',
                'DisplayOptions': {
                    'Width': 4,
                    'Order': 31,
                },
                'InitialAttributes': {
                    'Rate': Rate,
                    'NumberOfChips': self.Attributes['NumberOfChips'],
                    'StorageKey': 'NoiseOverview_{Rate}'.format(Rate=Rate)
                },
            })
            self.ResultData['SubTestResultDictList'].append({
                'Key': 'NoiseDistribution_{Rate}'.format(Rate=Rate),
                'Module': 'NoiseDistribution',
                'DisplayOptions': {
                    'Width': 1,
                    'Order': 31,
                },
                'InitialAttributes': {
                    'Rate': Rate,
                    'NumberOfChips': self.Attributes['NumberOfChips'],
                    'StorageKey': 'NoiseDistribution_{Rate}'.format(Rate=Rate)
                },
            })

        for Rate in self.Attributes['Rates']['HREfficiency']:
            self.ResultData['SubTestResultDictList'].append({
                'Key': 'EfficiencyOverview_{Rate}'.format(Rate=Rate),
                'Module': 'EfficiencyOverview',
                'DisplayOptions': {
                    'Width': 4,
                    'Order': 50,
                },
                'InitialAttributes': {
                    'Rate': Rate,
                    'NumberOfChips': self.Attributes['NumberOfChips'],
                    'StorageKey': 'EfficiencyOverview_{Rate}'.format(Rate=Rate)
                },
            })
            self.ResultData['SubTestResultDictList'].append({
                'Key': 'EfficiencyDistribution_{Rate}'.format(Rate=Rate),
                'Module': 'EfficiencyDistribution',
                'DisplayOptions': {
                    'Width': 1,
                    'Order': 50,
                },
                'InitialAttributes': {
                    'Rate': Rate,
                    'NumberOfChips': self.Attributes['NumberOfChips'],
                    'StorageKey': 'EfficiencyDistribution_{Rate}'.format(Rate=Rate)
                },
            })

        self.ResultData['SubTestResultDictList'].append({
                'Key': 'SummaryROCs',
                'DisplayOptions': {
                    'GroupWithNext': False,
                    'Order': 3,
                    'Width': 4,
                },
                'InitialAttributes': {
                    'ModuleVersion': self.Attributes['ModuleVersion'],
                },
            })
       

    def OpenFileHandle(self):
        pass

    def PopulateResultData(self):
        self.CloseSubTestResultFileHandles()
        pass

    def CustomWriteToDatabase(self, ParentID):
        if self.verbose:
            print 'Write to DB: ',ParentID

        try:
            grade = self.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['ModuleGrade']['Value']
        except KeyError:
            grade = 'None'

        try:
            PixelDefects = self.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['PixelDefects']['Value']
        except KeyError:
            PixelDefects = 'None'

        try:
            ROCsLessThanOnePercent = self.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['ROCsLessThanOnePercent']['Value']
        except KeyError:
            ROCsLessThanOnePercent = 'None'

        try:
            ROCsMoreThanOnePercent = self.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['ROCsMoreThanOnePercent']['Value']
        except KeyError:
            ROCsMoreThanOnePercent = 'None'

        try:
            ROCsMoreThanFourPercent = self.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['ROCsMoreThanFourPercent']['Value']
        except KeyError:
            ROCsMoreThanFourPercent = 'None'

        try:
            NoisyPixels = float(self.ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['NoisyPixels']['Value'])
        except KeyError:
            NoisyPixels = 'None'

        print 'fill row'
        Row = {
            'ModuleID': self.Attributes['ModuleID'],
            'TestDate': self.Attributes['TestDate'],
            'TestType': self.Attributes['TestType'],
            'QualificationType': self.ParentObject.Attributes['QualificationType'],
            'Grade': grade,
            'PixelDefects': PixelDefects,
            'ROCsLessThanOnePercent': ROCsLessThanOnePercent,
            'ROCsMoreThanOnePercent': ROCsMoreThanOnePercent,
            'ROCsMoreThanFourPercent': ROCsMoreThanFourPercent,
            'Noise': NoisyPixels,
            'RelativeModuleFinalResultsPath': os.path.relpath(self.TestResultEnvironmentObject.FinalModuleResultsPath,
                                                              self.TestResultEnvironmentObject.GlobalOverviewPath),
            'FulltestSubfolder': os.path.relpath(self.FinalResultsStoragePath,
                                                 self.TestResultEnvironmentObject.FinalModuleResultsPath),
            # needed for PixelDB
            'AbsModuleFulltestStoragePath': self.TestResultEnvironmentObject.FinalModuleResultsPath,
            'AbsFulltestSubfolder': self.FinalResultsStoragePath,
            'InputTarFile': os.environ.get('TARFILE', None),
            'MacroVersion': os.environ.get('MACROVERSION', None),
            
            'TestCenter': self.Attributes['TestCenter'],
            'Hostname': self.Attributes['Hostname'],
            'Operator': self.Attributes['Operator'],
        }

        print 'fill row end'
        if False and self.TestResultEnvironmentObject.Configuration['Database']['UseGlobal']:

            HighRateData = Row.deepcopy()

            HighRateData['HRGrade'] = grade
            del(HighRateData['Grade'])

            GradingTestResultObject = self.ResultData['SubTestResults']['Grading']

            # '#Pix NoHit'
            HighRateData['BumpBondingDefects'] = GradingTestResultObject.ResultData['KeyValueDictPairs']['BumpBondingDefects']['Value']

            # '#Pix Hot'
            HighRateData['HotPixelDefects'] = GradingTestResultObject.ResultData['KeyValueDictPairs']['HotPixelDefects']['Value']

            # 'Eff @50'
            HighRateData['Efficiency50'] = GradingTestResultObject.ResultData['KeyValueDictPairs']['Efficiency_50']['Value']

            # efficiency at 120 MHz/cm2
            HighRateData['Efficiency120'] = GradingTestResultObject.ResultData['KeyValueDictPairs']['Efficiency_120']['Value']

            #### some more variables that would be nice to have

            # number of ROCs with readout problems
            HighRateData['ROCsWithReadoutProblems'] = GradingTestResultObject.ResultData['KeyValueDictPairs']['ROCsWithReadoutProblems']['Value']
            
            # number of ROCs with uniformity problems
            HighRateData['ROCsWithUniformityProblems'] = GradingTestResultObject.ResultData['KeyValueDictPairs']['ROCsWithUniformityProblems']['Value']

            # mean noise
            HighRateData['MeanNoise'] = GradingTestResultObject.ResultData['KeyValueDictPairs']['MeanNoise']['Value']


            from PixelDB import *
            # modified by Tommaso
            #
            # try and speak directly with PixelDB
            #
            pdb = PixelDBInterface(operator="tommaso", center="pisa")
            pdb.connectToDB()
            
            OPERATOR = os.environ['PIXEL_OPERATOR']
            CENTER = os.environ['PIXEL_CENTER']
            s = Session(CENTER, OPERATOR)
            pdb.insertSession(s)
            print "--------------------"
            print "INSERTING INTO DB", self.TestResultEnvironmentObject.FinalModuleResultsPath, s.SESSION_ID, HighRateData
            print "--------------------"
            pp = pdb.insertTestFullModuleDirPlusMapv96Plus(s.SESSION_ID, HighRateData)
               
            if pp is None:
                print "INSERTION FAILED!"
                sys.exit(31)
            insertedID=pp.TEST_ID

            # here comes the code for pixel db upload
            pass
            
        else:
            with self.TestResultEnvironmentObject.LocalDBConnection:
                self.TestResultEnvironmentObject.LocalDBConnectionCursor.execute(
                    'DELETE FROM ModuleTestResults WHERE ModuleID = :ModuleID AND TestType=:TestType AND QualificationType=:QualificationType AND TestDate <= :TestDate',
                    Row)
                self.TestResultEnvironmentObject.LocalDBConnectionCursor.execute(
                    '''INSERT INTO ModuleTestResults
                    (
                        ModuleID,
                        TestDate,
                        TestType,
                        QualificationType,
                        Grade,
                        PixelDefects,
                        ROCsLessThanOnePercent,
                        ROCsMoreThanOnePercent,
                        ROCsMoreThanFourPercent,
                        Noise,
                        RelativeModuleFinalResultsPath,
                        FulltestSubfolder
                        
                    )
                    VALUES (
                        :ModuleID,
                        :TestDate,
                        :TestType,
                        :QualificationType,
                        :Grade,
                        :PixelDefects,
                        :ROCsLessThanOnePercent,
                        :ROCsMoreThanOnePercent,
                        :ROCsMoreThanFourPercent,
                        :Noise,
                        :RelativeModuleFinalResultsPath,
                        :FulltestSubfolder
                        
                    )
                    ''', Row)
                return self.TestResultEnvironmentObject.LocalDBConnectionCursor.lastrowid


