import ROOT
import AbstractClasses
from AbstractClasses.ModuleMap import ModuleMap

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_XRayHRQualification_EfficiencyOverview_TestResult'
        self.NameSingle='EfficiencyOverview'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'

    def PopulateResultData(self):
        ROOT.gPad.SetLogy(0)
        ROOT.gStyle.SetOptStat(0)

        # initialize module map
        self.ModuleMap = ModuleMap(Name=self.GetUniqueID(), nChips=self.ParentObject.Attributes['NumberOfChips'], StartChip=self.ParentObject.Attributes['StartChip'])

        for i in self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults']:
            ChipTestResultObject = self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults'][i]
            histo = ChipTestResultObject.ResultData['SubTestResults']['EfficiencyMap_{Rate}'.format(Rate=self.Attributes['Rate'])].ResultData['Plot']['ROOTObject']
            chipNo = ChipTestResultObject.Attributes['ChipNo']

            if histo:
                for col in range(self.nCols): 
                    for row in range(self.nRows):
                        result = histo.GetBinContent(col + 1, row + 1)
                        self.ModuleMap.UpdatePlot(chipNo, col, row, result)

        # draw module map
        if self.ModuleMap:
            self.ResultData['Plot']['ROOTObject'] = self.ModuleMap.GetHistogram()
            Ntrig = self.ParentObject.Attributes['Ntrig']['HREfficiency_{Rate}'.format(Rate=self.Attributes['Rate'])]
            self.ModuleMap.SetRangeUser(0, Ntrig)
            self.ModuleMap.Draw(self.Canvas)

        # save canvas
        self.ResultData['Plot']['Format'] = 'png'
        self.Title = 'HR Efficiency Map {Rate}'.format(Rate=self.Attributes['Rate'])
        self.SaveCanvas()