# -*- coding: utf-8 -*-
import ROOT

from AbstractClasses.GeneralTestResult import GeneralTestResult


class TestResult(GeneralTestResult):
    def CustomInit(self):
        self.NameSingle = 'ThresholdDistribution'
        self.Name = 'CMSPixel_QualificationGroup_Fulltest_Chips_Chip_%s_TestResult'%self.NameSingle
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'

    def PopulateResultData(self):

        ROOT.gPad.SetLogy(1)

        try:
            ThresholdMap = self.ParentObject.ResultData['SubTestResults']['VcalThresholdUntrimmed'].ResultData['Plot'][
                'ROOTObject']
        except:
            print "warning: couldn't find map 'VcalThresholdUntrimmed' which is needed for 'ThresholdDistribution'."
            ThresholdMap = None

        if ThresholdMap:
            self.ResultData['Plot']['ROOTObject'] = ROOT.TH1D(self.GetUniqueID(), "", 256, 0, 256)
            Columns = ThresholdMap.GetXaxis().GetNbins()
            Rows = ThresholdMap.GetYaxis().GetNbins()

            if self.ResultData['Plot']['ROOTObject']:
                for Column in range(Columns):
                    for Row in range(Rows):
                        self.ResultData['Plot']['ROOTObject'].Fill(ThresholdMap.GetBinContent(1 + Column, 1 + Row))

                self.ResultData['Plot']['ROOTObject'].SetTitle("")
                self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Vcal Threshold")
                self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("No. of Entries")
                self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
                self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
                self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
                self.ResultData['Plot']['ROOTObject'].Draw()


        self.SaveCanvas()

        ROOT.gPad.SetLogy(0)
