import AbstractClasses
import ROOT
import os
from AbstractClasses.Helper.BetterConfigParser import BetterConfigParser
import sys

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
        ROOT.gPad.SetLogy(0)
        ROOT.gPad.SetLogx(0)
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

        slope = None
        offset = None
        chi2 = None
        for i in target:
            id = self.GetUniqueID()
            if self.verbose:
                print target
                print all_targets[i].ResultData['Plot']['ROOTObject']
            self.ResultData['Plot']['ROOTObject'] = all_targets[i].ResultData['Plot']['ROOTObject'].Clone(id)
            slope = all_targets[i].ResultData['KeyValueDictPairs']['Slope']
            offset = all_targets[i].ResultData['KeyValueDictPairs']['Offset']
            chi2 =   all_targets[i].ResultData['KeyValueDictPairs']['chi2']
            break
        if self.ResultData['Plot']['ROOTObject']:
            self.ResultData['Plot']['ROOTObject'].SetTitle("")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Center of pulseheigth / Vcal")
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("number of electrons")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].Draw('APL')

        self.SaveCanvas()
        
        self.ResultData['KeyList'] = ['Slope', 'Offset']
        if slope['Value'] < 0:
            sys.stdout.write("\x1b[31m")
        print ("ROC %d"%self.chipNo).ljust(6) + " Slope = " + ("%.2f"%slope['Value']).ljust(5) + " +/- " + ("%.1f"%slope['Sigma']).ljust(4) + " Offset = " + ("%.1f"%offset['Value']).ljust(8)
        if slope['Value'] < 0:
            sys.stdout.write("\x1b[0m")
        self.ResultData['KeyValueDictPairs'] = {'Slope': slope,'Offset': offset,'chi2': chi2}
