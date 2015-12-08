# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
from AbstractClasses.ModuleMap import ModuleMap

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.NameSingle='HotPixelRetrimming'
        self.Name='CMSPixel_QualificationGroup_XRayHRQualification_%s_TestResult'%self.NameSingle
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'

    def PopulateResultData(self):
        ROOT.gPad.SetLogy(0)
        ROOT.gStyle.SetOptStat(0)

        # initialize module map
        self.ModuleMap = ModuleMap(Name=self.GetUniqueID(), nChips=self.ParentObject.Attributes['NumberOfChips'], StartChip=self.ParentObject.Attributes['StartChip'])
        DisplayOptionsShow = True

        for i in self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults']:
            ChipTestResultObject = self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults'][i]
            histo = ChipTestResultObject.ResultData['SubTestResults']['HotPixelRetrimming_{Rate}'.format(Rate=self.Attributes['Rate'])].ResultData['Plot']['ROOTObject']
            chipNo = ChipTestResultObject.Attributes['ChipNo']

            if histo:
                for col in range(self.nCols): 
                    for row in range(self.nRows):
                        result = histo.GetBinContent(col + 1, row + 1)
                        self.ModuleMap.UpdatePlot(chipNo, col, row, result)
            DisplayOptionsShow = DisplayOptionsShow and (ChipTestResultObject.ResultData['SubTestResults']['HotPixelRetrimming_{Rate}'.format(Rate=self.Attributes['Rate'])].DisplayOptions['Show'] if ChipTestResultObject.ResultData['SubTestResults']['HotPixelRetrimming_{Rate}'.format(Rate=self.Attributes['Rate'])].DisplayOptions.has_key('Show') else True)

        self.DisplayOptions['Show'] = DisplayOptionsShow

        # draw module map
        if self.ModuleMap:
            self.ResultData['Plot']['ROOTObject'] = self.ModuleMap.GetHistogram()
            self.ModuleMap.Draw(Canvas=self.Canvas, TitleZ="Δ trimbit")

        # save canvas
        self.ResultData['Plot']['Format'] = 'png'
        self.Title = 'Retrimmed Hot Pixels {Rate}'.format(Rate=self.Attributes['Rate'])
        self.SaveCanvas()