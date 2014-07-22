import AbstractClasses
import ROOT
import os
from AbstractClasses.Helper.BetterConfigParser import BetterConfigParser


class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.method = self.Attributes['Method']
        self.chipNo = self.ParentObject.Attributes['ChipNo']
        self.Name = "CMSPixel_QualificationGroup_XrayCalibration_{Method}_Chips_Chip_{Chip}_Calibration_TestResult".format(
            Method=self.method, Chip=self.chipNo)
        self.NameSingle = "XrayCalibrationChipResults"
        if self.verbose:
            tag = self.Name + ": Custom Init"
            print "".ljust(len(tag), '=')
            print tag
            print self.Attributes['target_key']
            print self.Attributes['Target'], self.Attributes['Method']
        self.Title = 'X-ray Calibration - Vcal Calibration Method {Method} Chip C{ChipNo}'.format(ChipNo=self.chipNo,
                                                                                                  Method=self.method)

    def PopulateResultData(self):
        self.verbose = True
        if self.verbose:
            tag = self.Name + ": Populate"
            print "".ljust(len(tag), '=')
            print tag
            print 'target Key:', self.Attributes['target_key']

        all_targets = filter(lambda x: x.startswith('Fluorescence'),
                             self.ParentObject.ParentObject.ParentObject.ResultData['SubTestResults'])

        print self.ParentObject.ParentObject.ParentObject.ResultData['SubTestResults'].keys()

        all_targets = self.ParentObject.ParentObject.ParentObject.ResultData['SubTestResults'][
            self.Attributes['target_key']]
        all_targets = all_targets.ResultData['SubTestResults']
        target = all_targets.keys()
        if self.verbose:
            print target
        target = filter(lambda x: x.endswith('C' + str(self.chipNo)), target)

        for i in target:
            id = self.GetUniqueID()
            if self.verbose:
                print target
                print all_targets[i].ResultData['Plot']['ROOTObject']
            self.ResultData['Plot']['ROOTObject'] = all_targets[i].ResultData['Plot']['ROOTObject'].Clone(id)
            slope = all_targets[i].ResultData['KeyValueDictPairs']['Slope']
            offset = all_targets[i].ResultData['KeyValueDictPairs']['Offset']
            break
        if self.ResultData['Plot']['ROOTObject']:
            self.ResultData['Plot']['ROOTObject'].SetTitle("")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Center of pulseheigth / Vcal")
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("number of electrons")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].Draw('APL')

        if self.SavePlotFile:
            self.Canvas.SaveAs(self.GetPlotFileName())
        self.ResultData['Plot']['Enabled'] = 1
        self.ResultData['Plot']['ImageFile'] = self.GetPlotFileName()

        self.ResultData['KeyList'] = ['Slope', 'Offset']
        print slope
        self.ResultData['KeyValueDictPairs'] = {'Slope': slope,'Offset': offset}