import AbstractClasses
import ROOT
import os
from AbstractClasses.Helper.BetterConfigParser import BetterConfigParser
from AbstractClasses.GeneralTestResult import GeneralTestResult


class TestResult(GeneralTestResult):
    def CustomInit(self):
        self.verbose = False
        self.Attributes['ChipNo'] = self.ParentObject.Attributes['ChipNo']
        self.Name = "CMSPixel_QualificationGroup_XrayHitMap_{Method}_Chips_Chip_{ChipNo}_{Target}_Calibration_TestResult".format(
            ChipNo=self.Attributes['ChipNo'],
            Target=self.Attributes['Target'],
            Method=self.Attributes['Method'])
        self.NameSingle = "XrayHitMapChipResults"
        if self.verbose:
            tag = self.Name + ": Custom Init"
            print "".ljust(len(tag), '=')
            print tag
            print self.Attributes['target_key']
            print self.Attributes['Target'], self.Attributes['Method']
        self.Title = 'X-ray Hit Map - Target {Target} Method {Method} Chip C{ChipNo}'.format(
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
            print 'Targetlist: ',target
        target = filter(lambda x: x.endswith('C' + str(self.Attributes['ChipNo'])), target)
        # if self.verbose:
        # print 'Target: ',target,len(target)
        for i in target:
            uniqueID = self.GetUniqueID()
            if self.verbose:
                print target
                print all_targets[i].Attributes
                print all_targets[i].Attributes['Target']
                print all_targets[i].ResultData['Plot']['ROOTObject']
                print uniqueID
                print all_targets[i].ResultData['Plot'].keys()
            self.ResultData['Plot']['ROOTObject'] = all_targets[i].ResultData['Plot']['ROOTObjectHitMap'].Clone(uniqueID)
            # print i
            # print all_targets[i].ResultData['KeyValueDictPairs'].keys()
            rate = all_targets[i].ResultData['KeyValueDictPairs']['Rate']
            nhits = all_targets[i].ResultData['KeyValueDictPairs']['NHits']
            ntrigs = all_targets[i].ResultData['KeyValueDictPairs']['NTrig']
        if self.ResultData['Plot']['ROOTObject']:
            self.ResultData['Plot']['ROOTObject'].Draw('colz')
            self.ResultData['Plot']['ROOTObject'].SetStats(False)
            self.ResultData['Plot']['ROOTObject'].SetTitle("")
            # self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Pulseheight / Vcal")
            # self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("number of entries")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()

        if self.Canvas:
            self.Canvas.SetCanvasSize(500, 500)
        self.ResultData['Plot']['Format'] = 'png'
        self.SaveCanvas()
        if self.verbose:
            tag = self.Name + ": Done"
            print "".ljust(len(tag), '=')+'\n'
        self.ResultData['KeyList'] = ['Rate', 'NTrigs', 'NHits']
        self.ResultData['KeyValueDictPairs'] = {'Rate': rate, 'NTrigs': ntrigs,'NHits':nhits}