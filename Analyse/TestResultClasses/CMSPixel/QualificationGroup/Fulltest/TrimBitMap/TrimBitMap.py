import ROOT
import AbstractClasses
import ROOT
from AbstractClasses.ModuleMap import ModuleMap

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.NameSingle='TrimBitMap'
        self.Name='CMSPixel_QualificationGroup_Fulltest_Chips_Chip_%s_TestResult'%self.NameSingle
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'

    def PopulateResultData(self):
        ROOT.gStyle.SetOptStat(0)

        # initialize module map
        self.ModuleMap = ModuleMap(Name=self.GetUniqueID(), nChips=self.ParentObject.Attributes['NumberOfChips'], StartChip=self.ParentObject.Attributes['StartChip'])

        # fill plot
        for i in self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults']:
            ChipTestResultObject = self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults'][i]
            histo = ChipTestResultObject.ResultData['SubTestResults']['TrimBitMap'].ResultData['Plot']['ROOTObject']

            if not histo:
                print 'cannot get TrimBitMap histo for chip ',ChipTestResultObject.Attributes['ChipNo']
                continue
            chipNo = ChipTestResultObject.Attributes['ChipNo']
            for col in range(self.nCols):
                for row in range(self.nRows):
                    result = histo.GetBinContent(col + 1, row + 1)
                    self.ModuleMap.UpdatePlot(chipNo, col, row, result)

        # draw module map
        if self.ModuleMap:
            self.ResultData['Plot']['ROOTObject'] = self.ModuleMap.GetHistogram()
            self.ModuleMap.Draw(self.Canvas)

        # save canvas
        self.ResultData['Plot']['Format'] = 'png'
        self.Title = 'Trim Bit Map'
        self.SaveCanvas()