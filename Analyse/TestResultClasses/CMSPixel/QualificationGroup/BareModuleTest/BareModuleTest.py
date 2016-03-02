import os

import ROOT

import AbstractClasses
from AbstractClasses.Helper.BetterConfigParser import BetterConfigParser

from AbstractClasses.GeneralTestResult import GeneralTestResult


class TestResult(GeneralTestResult):
    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_BareModuletest_TestResult'
        self.NameSingle = 'BareModuleTest'
        self.Title = str(self.Attributes['ModuleID']) + ' ' + self.Attributes['StorageKey']
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
        self.Attributes['NumberOfChips'] = self.nTotalChips

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
        ROCtype, nRocs, halfModule = self.ReadModuleVersion()
        self.Attributes['NumberOfChips'] = nRocs
        if halfModule:
            self.Attributes['StartChip'] = 8
        self.Attributes['isDigital'] = (ROCtype.find('dig') != -1)
        self.Attributes['isBareModule'] = True
        if self.verbose:
            print 'Analysing BareModuletest with the following Attributes:'
            for name, value in self.Attributes.items():
                print "\t%25s:  %s" % (name, value)

                
        print 'Software used: ',self.testSoftware

        if self.testSoftware == 'pxar':

            self.ResultData['SubTestResultDictList'] = [

                {
                    'Key': 'Chips',
                    'DisplayOptions': {
                        'GroupWithNext': False,
                        'Order': 1,
                        },
                    'InitialAttributes': {
                        'ModuleVersion': self.Attributes['ModuleVersion'],
                        },
                },
                {
                    'Key': 'BumpBondingMap',
                    'DisplayOptions': {
                        'GroupWithNext': True,
                        'Width': 4,
                        'Order': 1,
                        }
                },
                {
                    'Key': 'BareBBSummary',
                    'DisplayOptions': {
                        'GroupWithNext': True,
                        'Width': 4,
                        'Order': 3,
                        }
                 },
                 {
                    'Key': 'BareAliveSummary',
                    'DisplayOptions': {
                        'Width': 4,
                        'Order': 3,
                        }
                 },
                ]
        else:

            self.ResultData['SubTestResultDictList'] = [
                {
                    'Key': 'Chips',
                    'DisplayOptions': {
                        'GroupWithNext': False,
                        'Order': 1,
                        },
                    'InitialAttributes': {
                        'ModuleVersion': self.Attributes['ModuleVersion'],
                        },
                    },
                                
                {
                    'Key': 'BareBBSummary',
                    'DisplayOptions': {
                        'GroupWithNext': True, 
                        'Width': 4,
                        'Order': 3,
                        }
                    },
                {
                    'Key': 'BareAliveSummary',
                    'DisplayOptions': {
                        'Width': 4,
                        'Order': 3,
                        }
                 },               
                ]         

        self.ResultData['SubTestResultDictList'] += [
            {
                'Key': 'Summary1',
                'DisplayOptions': {
                    'Order': 4,
                }
            },
            ]


    def OpenFileHandle(self):
        self.check_Test_Software()
        fileHandlePath = self.RawTestSessionDataPath + '/commander_BareModuletest.root'
        self.FileHandle = ROOT.TFile.Open(fileHandlePath)
        if not self.FileHandle:
            print 'problem to find %s' % fileHandlePath
            files = [f for f in os.listdir(self.RawTestSessionDataPath) if f.endswith('.root')]
            i = 0
            if len(files) > 1:
                print '\nPossible Candidates for ROOT files are:'
                for f in files:
                    print '\t[%3d]\t%s' % (i, f)
                    i += 1
                i = len(files)
                if self.HistoDict.has_option('RootFile', 'filename'):
                    print 'checking for backup rootfile name'
                    if self.HistoDict.has_option('RootFile', 'filename'):
                        if self.HistoDict.get('RootFile', 'filename') in files:
                            i = files.index(self.HistoDict.get('RootFile', 'filename'))
                            print 'rootfile exists: index ', i
                while i < 0 or i >= len(files):
                    try:
                        # TODO: How to continue when it happens in automatic processing...
                        rawInput = ''
                        i = 0
                        if self.verbose:
                            rawInput = raw_input(
                                'There are more than one possbile candidate for the ROOT file. Which file should be used? [0-%d]\t' % (
                                    len(files) - 1))
                            i = int(rawInput)
                        elif self.HistoDict.has_option('RootFile', 'filename'):
                            if self.HistoDict.get('RootFile', 'filename') in files:
                                i = files.index(self.HistoDict.get('RootFile', 'filename'))
                        else:
                            i = 0
                    except TypeError:
                        print '%s is not an integer, please enter a valid integer' % rawInput
                    except ValueError:
                        print '%s is not an integer, please enter a valid integer' % rawInput

                fileHandlePath = self.RawTestSessionDataPath + '/' + files[i]
                print "open '%s'" % fileHandlePath
                self.FileHandle = ROOT.TFile.Open(fileHandlePath)
            elif len(files) == 1:
                i = 0
                fileHandlePath = self.RawTestSessionDataPath + '/' + files[i]
                print "only one other ROOT file exists. Open '%s'" % fileHandlePath
                self.FileHandle = ROOT.TFile.Open(fileHandlePath)
            else:
                print 'There exist no ROOT file in "%s"' % self.RawTestSessionDataPath

    def PopulateResultData(self):
        self.FileHandle.Close()

