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
                print 'WARNING: testParameters.dat file not found, using default number of triggers Ntrig = %d'%self.Attributes['Ntrig']['HREfficiency_{Rate}'.format(Rate=Rate)]

        HRDataPaths = glob.glob(self.RawTestSessionDataPath+'/0[0-9][0-9]_HRData_*')
        for Path in HRDataPaths:
            FolderName = os.path.basename(Path)
            Rate = int(FolderName.split('_')[2])
            self.Attributes['Rates']['HRData'].append(Rate)
            ROOTFiles = glob.glob(Path+'/*.root')
            self.Attributes['ROOTFiles']['HRData_{Rate}'.format(Rate=Rate)] = ROOT.TFile.Open(ROOTFiles[0])


        HRSCurvesPaths = glob.glob(self.RawTestSessionDataPath+'/0[0-9][0-9]_HRScurves_*')
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
            break

        self.ResultData['SubTestResultDictList'] = [
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
            },
            {
                'Key': 'SummaryROCs',
                'DisplayOptions': {
                    'GroupWithNext': False,
                    'Order': 3,
                    'Width': 4,
                },
                'InitialAttributes': {
                    'ModuleVersion': self.Attributes['ModuleVersion'],
                },
            }
        ]

        # value per ROC summary plots
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
            
       

    def OpenFileHandle(self):
        pass

    def PopulateResultData(self):
        pass

    def CustomWriteToDatabase(self, ParentID):
        if self.verbose:
            print 'Write to DB: ',ParentID

        try:
            grade = self.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs']['Grade']['Value']
        except KeyError:
            grade = 'None'
        
        
        print 'fill row'
        Row = {
            'ModuleID': self.Attributes['ModuleID'],
            'TestDate': self.Attributes['TestDate'],
            'TestType': self.Attributes['TestType'],
            'QualificationType': self.ParentObject.Attributes['QualificationType'],
            'Grade': grade,
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
            #from PixelDB import *
            #pdb = PixelDBInterface(operator="tommaso", center="pisa")
            #pdb.connectToDB()
            HighRateData = {
                'Rates':self.Attributes['Rates']
            }
            GradingTestResultObject = self.ResultData['SubTestResults']['Grading']
            EfficiencyOverviewTestResultObject = self.ResultData['SubTestResults']['EfficiencyOverview']
            

            
            for Rate in self.Attributes['Rates']['HREfficiency']:
                # Number of pixels with efficiency below cut (Sum over all 16 ROCs is module value)
                HighRateData['LowEffPixels_Module_{Rate}'.format(Rate=Rate)] = int(
                    GradingTestResultObject.ResultData['KeyValueDictPairs']['NumberOfLowEfficiencyPixels_{Rate}'.format(Rate=Rate)]['Value']
                )
                # Measured Efficiency (Mean of all 16 ROCs is module value)
                HighRateData['Eff_measured_Module_{Rate}'.format(Rate=Rate)] = float(
                    EfficiencyOverviewTestResultObject.ResultData['KeyValueDictPairs']['MeasuredEfficiencyMean_{Rate}'.format(Rate=Rate)]['Value']
                )
                
                # Measured Hitrate (Mean of all 16 ROCs is module value)
                HighRateData['HRate_Eff_measured_Module_{Rate}'.format(Rate=Rate)] = float(
                    EfficiencyOverviewTestResultObject.ResultData['KeyValueDictPairs']['MeasuredHitrateMean_{Rate}'.format(Rate=Rate)]['Value']
                )
                
                # Interpolated Efficiency (Mean of all 16 ROCs is module value)
                HighRateData['Eff_Module_{Rate}'.format(Rate=Rate)] = float(
                    EfficiencyOverviewTestResultObject.ResultData['KeyValueDictPairs']['InterpolatedEfficiencyMean_{Rate}'.format(Rate=Rate)]['Value']
                )

                # Number of columns with efficiency below cut (Sum over all 16 ROCs is module value)
                HighRateData['LowUniformityColumns_Module_{Rate}'.format(Rate)] = int(
                    EfficiencyOverviewTestResultObject.ResultData['KeyValueDictPairs']['NumberOfLowEfficiencyColumnsSum_{Rate}'.format(Rate=Rate)]['Value']
                )

            # Interpolated Efficiency
            for Rate in self.Attributes['InterpolatedEfficiencyRates']:
                HighRateData['Eff_C{ChipNo}_{Rate}'.format(ChipNo=ChipNo, Rate=Rate)] = float(
                    EfficiencyInterpolationTestResultObject.ResultData['KeyValueDictPairs']['InterpolatedEfficiency{Rate}'.format(Rate=Rate)]['Value']
                )

            for Rate in self.Attributes['Rates']['HRData']:
                # Number of hot pixels (Sum over all 16 ROCs is module value)
                HighRateData['HotPixels_Module_{Rate}'.format(Rate=Rate)] = int(
                    EfficiencyOverviewTestResultObject.ResultData['KeyValueDictPairs']['NumberOfHotPixelsSum_{Rate}'.format(Rate=Rate)]['Value']
                )
                
                # Number of pixels with no hits (Sum over all 16 ROCs is module value)
                HighRateData['NoHitPixels_Module_{Rate}'.format(ChipNo=ChipNo, Rate=Rate)] = int(
                    EfficiencyOverviewTestResultObject.ResultData['KeyValueDictPairs']['NumberOfHotPixelsSum_{Rate}'.format(Rate=Rate)]['Value']
                )
                
                # Number of columns with non uniform readout (Sum over all 16 ROCs is module value)
                HighRateData['NonUniformColumns_Module_{Rate}'.format(ChipNo=ChipNo, Rate=Rate)] = int(
                    EfficiencyOverviewTestResultObject.ResultData['KeyValueDictPairs']['NumberOfNonUniformColumnsSum_{Rate}'.format(Rate=Rate)]['Value']
                )
                
            
                
            for i in self.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults']:
                ChipTestResultObject = self.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults'][i]
                GradingTestResultObject = ChipTestResultObject.ResultData['SubTestResults']['Grading']
                EfficiencyInterpolationTestResultObject = ChipTestResultObject.ResultData['SubTestResults']['EfficiencyInterpolation']
                
                
                ChipNo = ChipTestResultObject.Attributes['ChipNo']
                
                ## Column Efficiency
                # Number of columns with efficiency below cut
                # before: 'LowEffColumns_C{ChipNo}'
                HighRateData['LowUniformityColumns_C{ChipNo}'.format(ChipNo=ChipNo)] = int(
                    GradingTestResultObject.ResultData['HiddenData']['NumberOfNonUniformColumns']
                )
                
                # Number of events where a column has low efficiency
                # before: 'LowEffCol_Events_C{ChipNo}'
                #HighRateData['LowUniformityCol_Events_C{ChipNo}'.format(ChipNo=ChipNo)] = int(
                #    GradingTestResultObject.ResultData['HiddenData']['NumberOfLowUniformityColumnEvents']
                #)
                
                for Rate in self.Attributes['Rates']['HREfficiency']:
                    EfficiencyDistributionTestResultObject = ChipTestResultObject.ResultData['SubTestResults']['EfficiencyDistribution_{Rate}'.format(Rate)]
                    BackgroundMapTestResultObject = ChipTestResultObject.ResultData['SubTestResults']['BackgroundMap_{Rate}'.format(Rate=Rate)]

                    
                    ## Pixel Efficiency
                    
                    # Number of pixels with efficiency below cut
                    HighRateData['LowEffPixels_C{ChipNo}_{Rate}'.format(ChipNo=ChipNo, Rate=Rate)] = float(
                        GradingTestResultObject.ResultData['KeyValueDictPairs']['NumberOfLowEfficiencyPixels_{Rate}'.format(Rate=Rate)]['Value']
                    )
                    # Addresses of low efficiency pixels
                    HighRateData['Addr_LowEffPixels_C{ChipNo}_{Rate}'.format(ChipNo=ChipNo, Rate=Rate)] = (
                        GradingTestResultObject.ResultData['HiddenData']['ListOfLowEfficiencyPixels_{Rate}'.format(Rate=Rate)]
                    )
                    
                    # Measured Efficiency
                    HighRateData['Eff_measured_C{ChipNo}_{Rate}'.format(ChipNo=ChipNo, Rate=Rate)] = float(
                        EfficiencyDistributionTestResultObject.ResultData['KeyValueDictPairs']['RealHitrate']['NumericValue']
                    )
                    
                    # Measured Hitrate
                    HighRateData['HRate_Eff_measured_C{ChipNo}_{Rate}'.format(ChipNo=ChipNo, Rate=Rate)] = float(
                        BackgroundMapTestResultObject.ResultData['KeyValueDictPairs']['mu']['Value']
                    )
                

                for Rate in self.Attributes['Rates']['HRData']:
                    HitMapTestResultObject = ChipTestResultObject.ResultData['SubTestResults']['HitMap_{Rate}'.format(Rate=Rate)]
                    ColumnReadoutUniformityTestResultObject = ChipTestResultObject.ResultData['SubTestResults']['ColumnReadoutUniformity_{Rate}'.format(Rate=Rate)]

                    ## Hot Pixels
                    # Number of pixels with efficiency below cut
                    HighRateData['HotPixels_C{ChipNo}_{Rate}'.format(ChipNo=ChipNo, Rate=Rate)] = int(
                        GradingTestResultObject.ResultData['KeyValueDictPairs']['NumberOfHotPixels_{Rate}'.format(Rate=Rate)]['Value']
                    )
                    # Addresses of hot pixels
                    HighRateData['Addr_HotPixels_C{ChipNo}_{Rate}'.format(ChipNo=ChipNo, Rate=Rate)] = (
                        GradingTestResultObject.ResultData['HiddenData']['ListOfHotPixels_{Rate}'.format(Rate=Rate)]
                    )
                    
                    ## No Hit Pixels
                    # Number of pixels with no hits
                    HighRateData['NoHitPixels_C{ChipNo}_{Rate}'.format(ChipNo=ChipNo, Rate=Rate)] = int(
                        HitMapTestResultObject.ResultData['KeyValueDictPairs']['NumberOfDefectivePixels']['Value']
                    )
                    # Measured hit rate
                    HighRateData['XRay_Hitrate_C{ChipNo}_{Rate}'.format(ChipNo=ChipNo, Rate=Rate)] = float(
                        HitMapTestResultObject.ResultData['KeyValueDictPairs']['RealHitrate']['NumericValue']
                    )
                    # Addresses of hot pixels
                    HighRateData['Addr_NoHitPixels_C{ChipNo}_{Rate}'.format(ChipNo=ChipNo, Rate=Rate)] = (
                        HitMapTestResultObject.ResultData['HiddenData']['ListOfDefectivePixels']
                    )
                    
                    ## Column Readout Uniformity
                    # Number of columns with non uniform readout
                    HighRateData['NonUniformColumns_C{ChipNo}_{Rate}'.format(ChipNo=ChipNo, Rate=Rate)] = int(
                        GradingTestResultObject.ResultData['HiddenData']['NumberOfNonUniformColumns_{Rate}'.format(Rate=Rate)]
                    )
                    
                    # Sigma/Mean column uniformity
                    HighRateData['UniformColumns_RelSigma_C{ChipNo}_{Rate}'.format(ChipNo=ChipNo, Rate=Rate)] = float(
                        ColumnReadoutUniformityTestResultObject.ResultData['KeyValueDictPairs']['sigma']['Value']
                    )/float(
                        ColumnReadoutUniformityTestResultObject.ResultData['KeyValueDictPairs']['mu']['Value']
                    )
                    
                    ## Column Readout Uniformity over Time
                    # Number of Events with non uniform readout
                    HighRateData['NonUniformEvents_C{ChipNo}_{Rate}'.format(ChipNo=ChipNo, Rate=Rate)] = int(
                        GradingTestResultObject.ResultData['HiddenData']['NumberOfNonUniformEvents_{Rate}'.format(Rate=Rate)]
                    )
                    
                    
                    
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
                        RelativeModuleFinalResultsPath,
                        FulltestSubfolder
                        
                    )
                    VALUES (
                        :ModuleID,
                        :TestDate,
                        :TestType,
                        :QualificationType,
                        :Grade,
                        :RelativeModuleFinalResultsPath,
                        :FulltestSubfolder
                        
                    )
                    ''', Row)
                return self.TestResultEnvironmentObject.LocalDBConnectionCursor.lastrowid


