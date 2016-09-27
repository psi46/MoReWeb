import ROOT
import AbstractClasses
import ROOT
from AbstractClasses.ModuleMap import ModuleMap

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.NameSingle = 'BumpBonding'
        self.Name = 'CMSPixel_QualificationGroup_OnShellQuickTest_Chips_Chip_{NameSingle}_TestResult'.format(NameSingle=self.NameSingle)
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'

    def PopulateResultData(self):
        ROOT.gStyle.SetOptStat(0)

        # initialize module map
        self.ModuleMap = ModuleMap(Name=self.GetUniqueID(), nChips=self.ParentObject.Attributes['NumberOfChips'], StartChip=self.ParentObject.Attributes['StartChip'])

        # fill plot
        for i in self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults']:
            ChipTestResultObject = self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults'][i]
            histo = ChipTestResultObject.ResultData['SubTestResults']['BumpBonding'].ResultData['Plot']['ROOTObject']

            if not histo:
                print 'cannot get BumpBondingProblems histo for chip ',ChipTestResultObject.Attributes['ChipNo']
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
        self.Title = 'Bump Bonding Defects'
        self.SaveCanvas()

    def UpdatePlot(self, chipNo, col, row, value):
        result = value
        if chipNo < 8:
            tmpCol = 8 * self.nCols - 1 - chipNo * self.nCols - col
            tmpRow = 2 * self.nRows - 1 - row
        else:
            tmpCol = (chipNo % 8 * self.nCols + col)
            tmpRow = row
        # Get the data from the chip sub test result bump bonding

        if result and self.verbose:
            print chipNo, col, row, '--->', tmpCol, tmpRow, result
        self.ResultData['Plot']['ROOTObject'].Fill(tmpCol, tmpRow, result)
