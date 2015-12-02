import ROOT
import AbstractClasses
import ROOT
import math
from AbstractClasses.ModuleMap import ModuleMap

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Fulltest_VcalThreshold_TestResult'
        self.NameSingle='VcalThreshold'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
        self.Title = 'Vcal Threshold'


    def PopulateResultData(self):
        ROOT.gStyle.SetOptStat(0)
        self.ResultData['Plot']['ROOTObject'] = None

        # initialize module map
        self.ModuleMap = ModuleMap(Name=self.GetUniqueID(), nChips=self.ParentObject.Attributes['NumberOfChips'], StartChip=self.ParentObject.Attributes['StartChip'])

        # loop over all chips
        ValueList = []
        for i in self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults']:
            ChipTestResultObject = self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults'][i]
            histo = ChipTestResultObject.ResultData['SubTestResults']['VcalThresholdUntrimmed'].ResultData['Plot']['ROOTObject']
            if not histo:
                print 'cannot get VcalThresholdUntrimmed histo for chip ',ChipTestResultObject.Attributes['ChipNo']
                continue
            
            for col in range(self.nCols):
                for row in range(self.nRows):
                    Value = histo.GetBinContent(col + 1, row + 1)
                    ValueList.append(Value)
                    self.ModuleMap.UpdatePlot(ChipTestResultObject.Attributes['ChipNo'], col, row, Value)

        # draw module map
        if self.ModuleMap:
            self.ResultData['Plot']['ROOTObject'] = self.ModuleMap.GetHistogram()
            self.ModuleMap.Draw(self.Canvas)

        # get minimum and maximum threshold
        if self.ResultData['Plot']['ROOTObject']:
            mThresholdMin = 0.
            mThresholdMax = 255.

            if self.ResultData['Plot']['ROOTObject'].GetMaximum() < mThresholdMax:
                mThresholdMax = self.ResultData['Plot']['ROOTObject'].GetMaximum()

            if self.ResultData['Plot']['ROOTObject'].GetMinimum() > mThresholdMin:
                mThresholdMin = self.ResultData['Plot']['ROOTObject'].GetMinimum()
            if len(ValueList) > 0:
                SortedValueList = sorted(ValueList)
                LowerIndex = int(math.floor(len(SortedValueList)*0.05))
                UpperIndex = int(math.floor(len(SortedValueList)*0.95))
                LowerValueList = SortedValueList[0:LowerIndex-1]
                UpperValueList = SortedValueList[UpperIndex:]
                if SortedValueList[LowerIndex] > 5.*sum(LowerValueList)/float(len(LowerValueList)):
                    mThresholdMin = SortedValueList[LowerIndex]*0.1
                if SortedValueList[UpperIndex]*5. < sum(UpperValueList)/float(len(UpperValueList)):
                    mThresholdMax = SortedValueList[UpperIndex]*1.1

        # save canvas
        self.ResultData['Plot']['Format'] = 'png'
        self.ResultData['Plot']['Caption'] = 'Vcal Threshold'
        self.SaveCanvas()        