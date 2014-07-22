import AbstractClasses
import ROOT
import os
from AbstractClasses.Helper.BetterConfigParser import BetterConfigParser


class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.method = self.Attributes['Method']
        self.chipNo = self.ParentObject.Attributes['ChipNo']
        self.target = self.Attributes['Target']
        self.Name = "CMSPixel_QualificationGroup_XrayCalibration_{Method}_Chips_Chip_{ChipNo}_{Target}_Calibration_TestResult".format(
            ChipNo=self.chipNo,
            Target=self.target,
            Method=self.method)
        self.NameSingle = "XrayCalibrationChipResults"
        self.chipNo = self.ParentObject.Attributes['ChipNo']
        if self.verbose:
            tag = self.Name + ": Custom Init"
            print "".ljust(len(tag), '=')
            print tag
            print self.Attributes['target_key']
            print self.Attributes['Target'], self.Attributes['Method']
        self.target = self.Attributes['Target']
        self.Title = 'X-ray Calibration - Target {Target} Method {Method} Chip C{ChipNo}'.format(ChipNo=self.chipNo,
                                                                                                 Target=self.target,
                                                                                                 Method=self.method)

    def PopulateResultData(self):
        if self.verbose:
            tag = self.Name + ": Populate"
            print "".ljust(len(tag), '=')
            print tag
            print 'target Key:', self.Attributes['target_key']
        all_targets = filter(lambda x: x.startswith('Fluorescence'),
                             self.ParentObject.ParentObject.ParentObject.ResultData['SubTestResults'])
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
                print all_targets[i].Attributes['Target']
                print all_targets[i].ResultData['Plot']['ROOTObject']
                print id
            self.ResultData['Plot']['ROOTObject'] = all_targets[i].ResultData['Plot']['ROOTObject'].Clone(id)
            center = all_targets[i].ResultData['KeyValueDictPairs']['Center']
            n_electrons = all_targets[i].ResultData['KeyValueDictPairs']['TargetNElectrons']
            energy = all_targets[i].ResultData['KeyValueDictPairs']['TargetEnergy']
            break
        if self.ResultData['Plot']['ROOTObject']:
            self.ResultData['Plot']['ROOTObject'].SetTitle("")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Pulseheight / Vcal")
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("number of entries")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].Draw('')

        if self.SavePlotFile:
            self.Canvas.SaveAs(self.GetPlotFileName())
        self.ResultData['Plot']['Enabled'] = 1
        self.ResultData['Plot']['ImageFile'] = self.GetPlotFileName()


        self.ResultData['KeyList'] = ['Center', 'TargetEnergy', 'TargetNElectrons']
        self.ResultData['KeyValueDictPairs'] = {'Center': center,'TargetEnergy': energy, 'TargetNElectrons': n_electrons}