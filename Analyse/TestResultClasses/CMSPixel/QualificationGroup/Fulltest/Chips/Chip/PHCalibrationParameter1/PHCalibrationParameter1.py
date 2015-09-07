# -*- coding: utf-8 -*-
import AbstractClasses
from AbstractClasses.GeneralTestResult import GeneralTestResult
import ROOT


class TestResult(GeneralTestResult):
    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_Fulltest_Chips_Chip_PHCalibrationParameter1_TestResult'
        self.NameSingle = 'PHCalibrationParameter1'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'
        if self.verbose:
            tag = self.Name + ": Custom Init"
            print "".ljust(len(tag), '=')
            print tag

    def PopulateResultData(self):
        if self.verbose:
            tag = self.Name + ": Populate"
            print "".ljust(len(tag), '=')
            print tag
        ROOT.gPad.SetLogy(1)
        self.ResultData['Plot']['ROOTObject'] = \
            self.ParentObject.ResultData['SubTestResults']['PHCalibrationTan'].ResultData['Plot'][
                'ROOTObject'].Clone(self.GetUniqueID())
        self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
        self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.2)
        self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
        self.ResultData['Plot']['ROOTObject'].SetLineColor(ROOT.kBlue)
        self.ResultData['Plot']['ROOTObject'].Draw('')
        self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Par1")
        self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("No. of Entries")
        self.ResultData['KeyValueDictPairs'].update({
            'Par1N': {
                'Value': self.ParentObject.ResultData['SubTestResults']['PHCalibrationTan'].ResultData[
                    'KeyValueDictPairs']['N']['Value'],
                'Label': 'Par1 N'
            },
            'Par1mu': {
                'Value': self.ParentObject.ResultData['SubTestResults']['PHCalibrationTan'].ResultData[
                    'KeyValueDictPairs']['mu']['Value'],
                'Label': 'Par1 μ'
            },
            'Par1sigma': {
                'Value': self.ParentObject.ResultData['SubTestResults']['PHCalibrationTan'].ResultData[
                    'KeyValueDictPairs']['sigma']['Value'],
                'Label': 'Par1 RMS'
            }
        })
        self.ResultData['KeyList'] += ['Par1N', 'Par1mu', 'Par1sigma']

        if self.verbose:
            print self.ResultData['KeyValueDictPairs']

        self.ResultData['Plot']['ROOTObject_LowEdge'] = ROOT.TCutG('lLower', 2)
        self.ResultData['Plot']['ROOTObject_LowEdge'].SetPoint(0, self.TestResultEnvironmentObject.GradingParameters['par1Min'], -1e6)
        self.ResultData['Plot']['ROOTObject_LowEdge'].SetPoint(1, self.TestResultEnvironmentObject.GradingParameters['par1Min'], +1e6)
        self.ResultData['Plot']['ROOTObject_LowEdge'].SetLineColor(ROOT.kRed)
        self.ResultData['Plot']['ROOTObject_LowEdge'].SetLineStyle(2)
        self.ResultData['Plot']['ROOTObject_LowEdge'].Draw('same')

        self.ResultData['Plot']['ROOTObject_UpEdge'] = ROOT.TCutG('lUpper', 2)
        self.ResultData['Plot']['ROOTObject_UpEdge'].SetPoint(0, self.TestResultEnvironmentObject.GradingParameters['par1Max'], -1e6)
        self.ResultData['Plot']['ROOTObject_UpEdge'].SetPoint(1, self.TestResultEnvironmentObject.GradingParameters['par1Max'], +1e6)
        self.ResultData['Plot']['ROOTObject_UpEdge'].SetLineColor(ROOT.kRed)
        self.ResultData['Plot']['ROOTObject_UpEdge'].SetLineStyle(2)
        self.ResultData['Plot']['ROOTObject_UpEdge'].Draw('same')

        self.SaveCanvas()

        self.ResultData['Plot']['Caption'] = 'Parameter1'
        ROOT.gPad.SetLogy(0)
