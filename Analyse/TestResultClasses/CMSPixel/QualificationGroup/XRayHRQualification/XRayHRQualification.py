import os
import sys
import ROOT
import os.path
import glob
import copy
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

        try:
            self.AnalyzeHRQualificationFolder()
        except Exception as inst:
            self.TestResultEnvironmentObject.ErrorList.append(
               {'ModulePath': self.TestResultEnvironmentObject.ModuleDataDirectory,
                'ErrorCode': inst,
                'FinalResultsStoragePath':'unkown'
                }
            )
            print "\x1b[31mProblems in X-ray HR directory structure detected, skip qualification directory! %s\x1b[0m"%self.TestResultEnvironmentObject.ModuleDataDirectory

    def AnalyzeHRQualificationFolder(self):

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
        self.Attributes['Rates']['HREfficiency'].sort()

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
            ROOTFiles = glob.glob(Path+'/*.root')
            if len(ROOTFiles) == 1:
                self.Attributes['ROOTFiles']['HRSCurves_{Rate}'.format(Rate=Rate)] = ROOT.TFile.Open(ROOTFiles[0])
                self.FileHandle.append(self.Attributes['ROOTFiles']['HRSCurves_{Rate}'.format(Rate=Rate)])


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

        RetrimHotPixelsPaths = glob.glob(self.RawTestSessionDataPath+'/0[0-9][0-9]_RetrimHotPixels_*')
        if len(RetrimHotPixelsPaths) > 1:
                warnings.warn("multiple RetrimHotPixels tests found")

        for Path in RetrimHotPixelsPaths:
            FolderName = os.path.basename(Path)
            ROOTFiles = glob.glob(Path+'/*.root')
            if len(ROOTFiles) > 1:
                warnings.warn("The directory '%s' contains more than one .root file, choosing first one: '%s'"%(FolderName, ROOTFiles[0]))
            if len(ROOTFiles) >= 1:
                self.Attributes['ROOTFiles']['RetrimHotPixels'] = ROOT.TFile.Open(ROOTFiles[0])
                self.Attributes['RetrimHotPixelsPath'] = Path
                self.FileHandle.append(self.Attributes['ROOTFiles']['RetrimHotPixels'])
            break


        PixelAlivePaths = glob.glob(self.RawTestSessionDataPath+'/0[0-9][0-9]_PixelAlive_*')
        for Path in PixelAlivePaths:
            ROOTFiles = glob.glob(Path+'/*.root')
            self.Attributes['ROOTFiles']['PixelAlive'] = ROOT.TFile.Open(ROOTFiles[0])
            self.FileHandle.append(self.Attributes['ROOTFiles']['PixelAlive'])

            testParametersFilename = "/".join(ROOTFiles[0].split("/")[0:-1]) + "/testParameters.dat"
            NTriggersReadFromFile = False
            if os.path.exists(testParametersFilename):
                testParametersFile = open(testParametersFilename, "r")
                if testParametersFile:
                    testParametersSection = ""
                    for line in testParametersFile:
                        sline = line.strip()
                        if sline[0:2] == "--":
                            testParametersSection = sline[2:].strip()
                        elements = sline.strip().split(" ")
                        if testParametersSection.lower() == "pixelalive" and elements[0].lower() == "ntrig":
                            NTriggersReadFromFile = True
                            self.Attributes['Ntrig']['PixelAlive'] = float(elements[-1])
                    testParametersFile.close()
            if not NTriggersReadFromFile:
                print '\x1b[31mWARNING: testParameters.dat file not found in "%s", using default number of triggers Ntrig = 10\x1b[0m'%FolderName
        

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

        for Rate in self.Attributes['Rates']['HRData']:
            self.ResultData['SubTestResultDictList'].append({
                'Key': 'HotPixelRetrimming_{Rate}'.format(Rate=Rate),
                'Module': 'HotPixelRetrimming',
                'DisplayOptions': {
                    'Width': 4,
                    'Order': 60,
                },
                'InitialAttributes': {
                    'Rate': Rate,
                    'NumberOfChips': self.Attributes['NumberOfChips'],
                    'StorageKey': 'HotPixelRetrimming_{Rate}'.format(Rate=Rate)
                },
            })
            self.ResultData['SubTestResultDictList'].append({
                'Key': 'HotPixelRetrimSummary_{Rate}'.format(Rate=Rate),
                'Module': 'HotPixelRetrimSummary',
                'DisplayOptions': {
                    'Width': 1,
                    'Order': 60,
                },
                'InitialAttributes': {
                    'Rate': Rate,
                    'NumberOfChips': self.Attributes['NumberOfChips'],
                    'StorageKey': 'HotPixelRetrimSummary_{Rate}'.format(Rate=Rate)
                },
            })
       

    def OpenFileHandle(self):
        pass

    def PopulateResultData(self):
        self.CloseSubTestResultFileHandles()
        pass

    def PrintDatabaseRow(self, Row):
        print '-'*100
        print ' ROW'
        print '-'*100
        for i in Row:
            print ("%s: "%i).ljust(32),Row[i]
        print '-'*100

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

        if self.TestResultEnvironmentObject.Configuration['Database']['UseGlobal']:
            DebugGlobalDB = True
            GlobalDBRowTemplate = copy.deepcopy(Row)
            del(GlobalDBRowTemplate['Grade'])
            del(GlobalDBRowTemplate['Noise'])
            del(GlobalDBRowTemplate['PixelDefects'])
            del(GlobalDBRowTemplate['ROCsLessThanOnePercent'])
            del(GlobalDBRowTemplate['ROCsMoreThanOnePercent'])
            del(GlobalDBRowTemplate['ROCsMoreThanFourPercent'])

            GradingTestResultObject = self.ResultData['SubTestResults']['Grading']

            # first fill all fields which do not correspond to a specific rate, e.g. ratios of two rates, final grade etc.
            if True:
                HighRateData = copy.deepcopy(Row)

                #GRADE
                del(HighRateData['Grade'])
                HighRateData['HRGrade'] = grade

                # N_ROCS_READOUT_PROBLEM <- new
                HighRateData['ROCsWithReadoutProblems'] = GradingTestResultObject.ResultData['KeyValueDictPairs']['ROCsWithReadoutProblems']['Value']

                # ADDR_PIXELS_BAD
                HighRateData['AddrPixelsBad'] = GradingTestResultObject.ResultData['HiddenData']['TotalDefectPixelsList']['Value']

                # ADDR_PIXELS_HOT
                HighRateData['AddrPixelsHot'] = GradingTestResultObject.ResultData['HiddenData']['HotPixelsList']['Value']

                # N_HOT_PIXEL
                HighRateData['NHotPixel'] = len(GradingTestResultObject.ResultData['HiddenData']['HotPixelsList']['Value'])

                #-------------------------------------------------
                # <--- here comes the code for pixel db upload
                #-------------------------------------------------
                if DebugGlobalDB:
                    self.PrintDatabaseRow(HighRateData)

                ROCNumbers = []
                TotalPixelDefectsLists = []
                HotPixelsLists = []
                RocGrades = []
                NColNonUniform = []
                ChipsSubTestResult = self.ResultData['SubTestResults']['Chips']
                for i in ChipsSubTestResult.ResultData['SubTestResultDictList']:
                    ChipNo = i['TestResultObject'].Attributes['ChipNo']
                    ROCNumbers.append(ChipNo)
                    TotalPixelDefectsLists.append(ChipsSubTestResult.ResultData['SubTestResults']['Chip%d'%ChipNo].ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['TotalPixelDefectsList']['Value'])
                    HotPixelsLists.append(ChipsSubTestResult.ResultData['SubTestResults']['Chip%d'%ChipNo].ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['HotPixelDefectsList']['Value'])
                    RocGrades.append(ChipsSubTestResult.ResultData['SubTestResults']['Chip%d'%ChipNo].ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['ROCGrade']['Value'])
                    NColNonUniform.append(ChipsSubTestResult.ResultData['SubTestResults']['Chip%d'%ChipNo].ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['NumberOfNonUniformColumns']['Value'])
          
                # ROC rows
                for i in range(0, len(ROCNumbers)):
                    # remove grade from individual rows
                    HighRateData = copy.deepcopy(GlobalDBRowTemplate)

                    #ROC_POS
                    HighRateData['RocPos'] = ROCNumbers[i]

                    # ADDR_PIXELS_BAD
                    HighRateData['AddrPixelsBad'] = TotalPixelDefectsLists[i]

                    # ADDR_PIXELS_HOT
                    HighRateData['AddrPixelsHot'] = HotPixelsLists[i]

                    # N_HOT_PIXEL
                    HighRateData['NHotPixel'] = len(HotPixelsLists[i])

                    # GRADE
                    HighRateData['Grade'] = RocGrades[i]

                    # N_COL_NONUNIFORM
                    HighRateData['NColNonUniform'] = NColNonUniform[i]

                    #-------------------------------------------------
                    # <--- here comes the code for pixel db upload
                    #-------------------------------------------------
                    if DebugGlobalDB:
                        self.PrintDatabaseRow(HighRateData)


            # all hitmap rates  ("50", "150")
            for Rate in self.Attributes['Rates']['HRData']:

                # prepare data
                MeasuredHitrates = []
                NonUniformEventBins = []
                BumpBondingDefects = []
                ROCNumbers = []
                ChipsSubTestResult = self.ResultData['SubTestResults']['Chips']
                for i in ChipsSubTestResult.ResultData['SubTestResultDictList']:
                    ChipNo = i['TestResultObject'].Attributes['ChipNo']
                    ROCNumbers.append(ChipNo)
                    MeasuredHitrates.append(float(ChipsSubTestResult.ResultData['SubTestResults']['Chip%d'%ChipNo].ResultData['SubTestResults']['HitMap_{Rate}'.format(Rate=Rate)].ResultData['KeyValueDictPairs']['RealHitrate']['Value']))
                    NonUniformEventBins.append(int(ChipsSubTestResult.ResultData['SubTestResults']['Chip%d'%ChipNo].ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['NumberOfNonUniformEvents_{Rate}'.format(Rate=Rate)]['Value']))
                    BumpBondingDefects.append(int(ChipsSubTestResult.ResultData['SubTestResults']['Chip%d'%ChipNo].ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['BumpBondingDefects_{Rate}'.format(Rate=Rate)]['Value']))
          
                # apply aggregation function
                ModuleMeanHitrate = sum(MeasuredHitrates) / float(len(MeasuredHitrates))
                ModuleNonUniformEventBins = sum(NonUniformEventBins)
                ModuleBumpBondingDefects = sum(BumpBondingDefects)

                # remove grade from individual rows
                HighRateData = copy.deepcopy(GlobalDBRowTemplate)

                #HITRATENOMINAL
                HighRateData['HitrateNominal'] = Rate

                # MEASURED_HITRATE
                HighRateData['MeasuredHitrate'] = ModuleMeanHitrate

                # N_BINS_LOWHIGH
                HighRateData['NBinsLowHigh'] = ModuleNonUniformEventBins

                # N_PIXEL_NO_HIT
                HighRateData['NPixelNoHit'] = ModuleBumpBondingDefects

                #-------------------------------------------------
                # <--- here comes the code for pixel db upload
                #-------------------------------------------------
                if DebugGlobalDB:
                    self.PrintDatabaseRow(HighRateData)

                # ROC rows
                for i in range(0, len(ROCNumbers)):
                    # remove grade from individual rows
                    HighRateData = copy.deepcopy(GlobalDBRowTemplate)

                    #HITRATENOMINAL
                    HighRateData['HitrateNominal'] = Rate

                    #ROC_POS
                    HighRateData['RocPos'] = ROCNumbers[i]

                    # MEASURED_HITRATE
                    HighRateData['MeasuredHitrate'] = MeasuredHitrates[i]

                    # N_BINS_LOWHIGH
                    HighRateData['NBinsLowHigh'] = NonUniformEventBins[i]

                    # N_PIXEL_NO_HIT
                    HighRateData['NPixelNoHit'] = BumpBondingDefects[i]

                    #-------------------------------------------------
                    # <--- here comes the code for pixel db upload
                    #-------------------------------------------------
                    if DebugGlobalDB:
                        self.PrintDatabaseRow(HighRateData)


            # all noise rates
            for Rate in self.Attributes['Rates']['HRSCurves']:

                # prepare data
                MeasuredHitrates = []
                NoiseMeans = []
                NoiseWidths = []
                ROCNumbers = []
                NoisePixelsLists = []

                ChipsSubTestResult = self.ResultData['SubTestResults']['Chips']
                for i in ChipsSubTestResult.ResultData['SubTestResultDictList']:
                    ChipNo = i['TestResultObject'].Attributes['ChipNo']
                    ROCNumbers.append(ChipNo)
                    NoiseMeans.append(float(ChipsSubTestResult.ResultData['SubTestResults']['Chip%d'%ChipNo].ResultData['SubTestResults']['SCurveWidths_{Rate}'.format(Rate=Rate)].ResultData['KeyValueDictPairs']['mu']['Value']))
                    NoiseWidths.append(float(ChipsSubTestResult.ResultData['SubTestResults']['Chip%d'%ChipNo].ResultData['SubTestResults']['SCurveWidths_{Rate}'.format(Rate=Rate)].ResultData['KeyValueDictPairs']['sigma']['Value']))
                    MeasuredHitrates.append(float(ChipsSubTestResult.ResultData['SubTestResults']['Chip%d'%ChipNo].ResultData['SubTestResults']['SCurveWidths_{Rate}'.format(Rate=Rate)].ResultData['KeyValueDictPairs']['MeasuredHitrate']['Value']))
                    NoisePixelsLists.append(ChipsSubTestResult.ResultData['SubTestResults']['Chip%d'%ChipNo].ResultData['SubTestResults']['SCurveWidths_{Rate}'.format(Rate=Rate)].ResultData['HiddenData']['ListOfNoisyPixels']['Value'])

                # apply aggregation function
                ModuleMeanHitrate = sum(MeasuredHitrates) / float(len(MeasuredHitrates)) if len(MeasuredHitrates) > 0 else -1
                ModuleNoiseMean = sum(NoiseMeans) / float(len(NoiseMeans)) if len(NoiseMeans) > 0 else -1
                ModuleNoiseWidth = sum(NoiseWidths) / float(len(NoiseWidths)) if len(NoiseWidths) > 0 else -1

                # remove grade from individual rows
                HighRateData = copy.deepcopy(GlobalDBRowTemplate)

                #HITRATENOMINAL
                HighRateData['HitrateNominal'] = Rate

                # MEASURED_HITRATE
                HighRateData['MeasuredHitrate'] = ModuleMeanHitrate

                # MEAN_NOISE_ALLPIXELS
                HighRateData['MeanNoiseAllPixels'] = ModuleNoiseMean

                # WIDTH_NOISE_ALLPIXELS
                HighRateData['WidthNoiseAllPixels'] = ModuleNoiseWidth

                # ADDR_PIXELS_NOISE
                HighRateData['AddrPixelsNoise'] = self.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['NoiseDefectPixelsList']

                # N_PIXELS_NOISE  (or N_PIXELS_NOISE_ABOVETH)
                HighRateData['NPixelsNoise'] = self.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['NoiseDefects']

                #-------------------------------------------------
                # <--- here comes the code for pixel db upload
                #-------------------------------------------------
                if DebugGlobalDB:
                    self.PrintDatabaseRow(HighRateData)


                # ROC rows
                for i in range(0, len(ROCNumbers)):
                    # remove grade from individual rows
                    HighRateData = copy.deepcopy(GlobalDBRowTemplate)

                    #HITRATENOMINAL
                    HighRateData['HitrateNominal'] = Rate

                    #ROC_POS
                    HighRateData['RocPos'] = ROCNumbers[i]

                    # MEASURED_HITRATE
                    HighRateData['MeasuredHitrate'] = MeasuredHitrates[i]

                    # MEAN_NOISE_ALLPIXELS
                    HighRateData['MeanNoiseAllPixels'] = NoiseMeans[i]

                    # WIDTH_NOISE_ALLPIXELS
                    HighRateData['WidthNoiseAllPixels'] = NoiseWidths[i]

                    # ADDR_PIXELS_NOISE
                    HighRateData['AddrPixelsNoise'] = NoisePixelsLists[i]

                    # N_PIXELS_NOISE  (or N_PIXELS_NOISE_ABOVETH)
                    HighRateData['NPixelsNoise'] = len(NoisePixelsLists[i])

                    #-------------------------------------------------
                    # <--- here comes the code for pixel db upload
                    #-------------------------------------------------
                    if DebugGlobalDB:
                        self.PrintDatabaseRow(HighRateData)


            # all efficiency interpolation rates
            for Rate in self.Attributes['InterpolatedEfficiencyRates']:

                # prepare data
                MeasuredEfficiencies = []
                ROCNumbers = []

                ChipsSubTestResult = self.ResultData['SubTestResults']['Chips']
                for i in ChipsSubTestResult.ResultData['SubTestResultDictList']:
                    ChipNo = i['TestResultObject'].Attributes['ChipNo']
                    ROCNumbers.append(ChipNo)
                    MeasuredEfficiencies.append(float(ChipsSubTestResult.ResultData['SubTestResults']['Chip%d'%ChipNo].ResultData['SubTestResults']['EfficiencyInterpolation'].ResultData['KeyValueDictPairs']['InterpolatedEfficiency{Rate}'.format(Rate=Rate)]['Value']))
          
                # apply aggregation function
                ModuleMeanEfficiency= sum(MeasuredEfficiencies) / float(len(MeasuredEfficiencies)) if len(MeasuredEfficiencies) > 0 else -1

                # remove grade from individual rows
                HighRateData = copy.deepcopy(GlobalDBRowTemplate)

                # HITRATENOMINAL
                HighRateData['HitrateNominal'] = Rate

                # INTERP_EFF_TESTPOINT
                HighRateData['InterpEffTestpoint'] = ModuleMeanEfficiency

                #-------------------------------------------------
                # <--- here comes the code for pixel db upload
                #-------------------------------------------------
                if DebugGlobalDB:
                    self.PrintDatabaseRow(HighRateData)

                # ROC rows
                for i in range(0, len(ROCNumbers)):
                    # remove grade from individual rows
                    HighRateData = copy.deepcopy(GlobalDBRowTemplate)

                    #HITRATENOMINAL
                    HighRateData['HitrateNominal'] = Rate

                    #ROC_POS
                    HighRateData['RocPos'] = ROCNumbers[i]

                    # INTERP_EFF_TESTPOINT
                    HighRateData['InterpEffTestpoint'] = MeasuredEfficiencies[i]

                    #-------------------------------------------------
                    # <--- here comes the code for pixel db upload
                    #-------------------------------------------------
                    if DebugGlobalDB:
                        self.PrintDatabaseRow(HighRateData)


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


