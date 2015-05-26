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
        
        self.Attributes['Rates'] = []
        self.Attributes['ROOTFiles'] = {}
        self.Attributes['SCurvePaths'] = {}
        for Rate in self.TestResultEnvironmentObject.XRayHRQualificationConfiguration['Rates']:
            
            HREfficiencyPaths = glob.glob(self.RawTestSessionDataPath+'/0[0-9][0-9]_HREfficiency_{:d}/'.format(Rate))
            HRDataPaths = glob.glob(self.RawTestSessionDataPath+'/0[0-9][0-9]_HRData_{:d}'.format(Rate))
            HRSCurvesPaths = glob.glob(self.RawTestSessionDataPath+'/0[0-9][0-9]_HRScurves_{:d}'.format(Rate))
            if len(HREfficiencyPaths) and len(HRDataPaths) and len(HRSCurvesPaths):
               self.Attributes['Rates'].append(Rate)
               self.Attributes['ROOTFiles']['HREfficiency_{:d}'.format(Rate)] = ROOT.TFile.Open(HREfficiencyPaths[0]+'/pxar.root')
               self.Attributes['ROOTFiles']['HRData_{:d}'.format(Rate)] = ROOT.TFile.Open(HRDataPaths[0]+'/pxar.root')
               self.Attributes['SCurvePaths']['HRSCurves_{:d}'.format(Rate)] = HRSCurvesPaths[0]
               

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

            # {
                # 'Key': 'BumpBondingMap',
                # 'DisplayOptions': {
                    # 'Width': 4,
                    # 'Order': 5,
                # }
            # },
            # {
                # 'Key': 'VcalThreshold',
                # 'DisplayOptions': {
                    # 'Width': 4,
                    # 'Order': 3,
                # }
            # },
        ]
       

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
            
            for Rate in self.Attributes['Rates']:
                # Number of pixels with efficiency below cut (Sum over all 16 ROCs is module value)
                HighRateData['LowEffPixels_Module_{Rate}'.format(Rate=Rate)] = float(
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
                
            for i in self.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults']:
                ChipTestResultObject = self.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults'][i]
                GradingTestResultObject = ChipTestResultObject.ResultData['SubTestResults']['Grading']
                EfficiencyInterpolationTestResultObject = ChipTestResultObject.ResultData['SubTestResults']['EfficiencyInterpolation']
                
                ChipNo = ChipTestResultObject.Attributes['ChipNo']
                
                
                for Rate in self.Attributes['Rates']:
                    EfficiencyDistributionTestResultObject = ChipTestResultObject.ResultData['SubTestResults']['EfficiencyDistribution_{Rate}'.format(Rate)]
                    BackgroundMapTestResultObject = ChipTestResultObject.ResultData['SubTestResults']['BackgroundMap_{Rate}'.format(Rate=Rate)]
                    
                    ## Efficiency
                    
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
                    
                    # Interpolated Efficiency
                    HighRateData['Eff_C{ChipNo}_{Rate}'.format(ChipNo=ChipNo, Rate=Rate)] = float(
                        EfficiencyInterpolationTestResultObject.ResultData['KeyValueDictPairs']['InterpolatedEfficiency{Rate}'.format(Rate=Rate)]['Value']
                    )
                    
                    ## Hot Pixels
                    # Number of pixels with efficiency below cut
                    HighRateData['HotPixels_C{ChipNo}_{Rate}'.format(ChipNo=ChipNo, Rate=Rate)] = float(
                        GradingTestResultObject.ResultData['KeyValueDictPairs']['NumberOfHotPixels_{Rate}'.format(Rate=Rate)]['Value']
                    )
                    # Addresses of hot pixels
                    HighRateData['Addr_HotPixels_C{ChipNo}_{Rate}'.format(ChipNo=ChipNo, Rate=Rate)] = (
                        GradingTestResultObject.ResultData['HiddenData']['ListOfHotPixels_{Rate}'.format(Rate=Rate)]
                    )
                    
            
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


