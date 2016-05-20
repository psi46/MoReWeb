import AbstractClasses
import ROOT
import os
from AbstractClasses.Helper.BetterConfigParser import BetterConfigParser
from AbstractClasses.GeneralTestResult import GeneralTestResult


class TestResult(GeneralTestResult):
    def CustomInit(self):
        self.verbose = False
        self.Attributes['ChipNo'] = self.ParentObject.Attributes['ChipNo']
        self.Name = "CMSPixel_QualificationGroup_XrayCalibration_{Method}_Chips_Chip_{ChipNo}_{Target}_Calibration_TestResult".format(
            ChipNo=self.Attributes['ChipNo'],
            Target=self.Attributes['Target'],
            Method=self.Attributes['Method'])
        self.NameSingle = "XrayCalibrationChipResults"
        if self.verbose:
            tag = self.Name + ": Custom Init"
            print "".ljust(len(tag), '=')
            print tag
            print self.Attributes['target_key']
            print self.Attributes['Target'], self.Attributes['Method']
        self.Title = 'X-ray Calibration - Target {Target} Method {Method} Chip C{ChipNo}'.format(
            ChipNo=self.Attributes['ChipNo'],
            Target=self.Attributes['Target'],
            Method=self.Attributes['Method'])

    def PopulateResultData(self):
        ROOT.gPad.SetLogy(0)
        ROOT.gPad.SetLogx(0)
        if self.verbose:
            tag = self.Name + ": Populate"
            print "".ljust(len(tag), '=')
            print tag
            print 'target Key:', self.Attributes['target_key']
        # all_targets = filter(lambda x: x.startswith('Fluorescence'),
        #                      self.ParentObject.ParentObject.ParentObject.ResultData['SubTestResults'])
        all_targets = self.ParentObject.ParentObject.ParentObject.ResultData['SubTestResults'][
            self.Attributes['target_key']]
        all_targets = all_targets.ResultData['SubTestResults']
        target = all_targets.keys()
        if self.verbose:
            print target
        target = filter(lambda x: x.endswith('C' + str(self.Attributes['ChipNo'])), target)
        center = None
        energy = None
        n_electrons = None
        chi2 = None
        for i in target:
            uniqueID = self.GetUniqueID()
            if self.verbose:
                print target
                print all_targets[i].Attributes['Target']
                print all_targets[i].ResultData['Plot']['ROOTObject']
                print uniqueID
            self.ResultData['Plot']['ROOTObject'] = all_targets[i].ResultData['Plot']['ROOTObject'].Clone(uniqueID)
            # print  all_targets[i].ResultData['KeyValueDictPairs'].keys()
            nhits =  all_targets[i].ResultData['KeyValueDictPairs']['NHits']
            ntrig =  all_targets[i].ResultData['KeyValueDictPairs']['NTrig']
            rate =  all_targets[i].ResultData['KeyValueDictPairs']['Rate']
            center = all_targets[i].ResultData['KeyValueDictPairs']['Center']
            n_electrons = all_targets[i].ResultData['KeyValueDictPairs']['TargetNElectrons']
            energy = all_targets[i].ResultData['KeyValueDictPairs']['TargetEnergy']
            chi2 = all_targets[i].ResultData['KeyValueDictPairs']['Chi2PerNDF']
            break
        if self.ResultData['Plot']['ROOTObject']:
            self.ResultData['Plot']['ROOTObject'].SetTitle("")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Pulseheight / Vcal")
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("number of entries")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].Draw('')

        self.SaveCanvas()
        self.ResultData['KeyList'] = ['Center', 'TargetEnergy', 'TargetNElectrons', 'Chi2PerNDF','Rate']
        self.ResultData['KeyValueDictPairs'] = {'Center': center, 'TargetEnergy': energy,
                                                'TargetNElectrons': n_electrons, 'Chi2PerNDF': chi2,'Rate':rate,
                                                'NHits':nhits,'NTrig':ntrig}
        if self.verbose:
            tag = self.Name + ": Done"
            print "".ljust(len(tag), '=')