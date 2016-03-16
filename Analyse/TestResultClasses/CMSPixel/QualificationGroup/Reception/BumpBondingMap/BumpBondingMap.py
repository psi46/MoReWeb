import ROOT
import AbstractClasses
import ROOT
from AbstractClasses.ModuleMap import ModuleMap

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Reception_Chips_Chip_BumpBondingMap_TestResult'
        self.NameSingle='BumpBondingMap'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'

    def PopulateResultData(self):
        ROOT.gStyle.SetOptStat(0)

        # initialize module map
        self.ModuleMap = ModuleMap(Name=self.GetUniqueID(), nChips=self.ParentObject.Attributes['NumberOfChips'], StartChip=self.ParentObject.Attributes['StartChip'])

        # fill plot
        SpecialBumpBondingTestNamesROC = []
        for i in self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults']:
            ChipTestResultObject = self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults'][i]

            # take the same bb map that has been used in the grading
            SpecialBumpBondingTestName = ChipTestResultObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['SpecialBumpBondingTestName']
            if SpecialBumpBondingTestName == 'BB4':
                histo = ChipTestResultObject.ResultData['SubTestResults']['BB4'].ResultData['Plot']['ROOTObject']
                self.ResultData['HiddenData']['SpecialBumpBondingTestName'] = 'BB4'
            elif SpecialBumpBondingTestName == 'BB2':
                histo = ChipTestResultObject.ResultData['SubTestResults']['BB2Map'].ResultData['Plot']['ROOTObject']
                self.ResultData['HiddenData']['SpecialBumpBondingTestName'] = 'BB2'
            else:
                histo = ChipTestResultObject.ResultData['SubTestResults']['BumpBondingMap'].ResultData['Plot']['ROOTObject']

            SpecialBumpBondingTestNamesROC.append(SpecialBumpBondingTestName)
                
            if not histo:
                print 'cannot get BumpBondingProblems histo for chip ',ChipTestResultObject.Attributes['ChipNo']
                continue
            chipNo = ChipTestResultObject.Attributes['ChipNo']
            for col in range(self.nCols):
                for row in range(self.nRows):
                    result = histo.GetBinContent(col + 1, row + 1)
                    self.ModuleMap.UpdatePlot(chipNo, col, row, result)

        UniqueBBTestNames = list(set(SpecialBumpBondingTestNamesROC))
        if len(UniqueBBTestNames) == 1:
            self.ResultData['HiddenData']['SpecialBumpBondingTestName'] = UniqueBBTestNames[0]
        elif len(UniqueBBTestNames) > 1:
            self.ResultData['HiddenData']['SpecialBumpBondingTestName'] = '/'.join(UniqueBBTestNames)
        else:
            self.ResultData['HiddenData']['SpecialBumpBondingTestName'] = ''

        # draw module map
        if self.ModuleMap:
            self.ResultData['Plot']['ROOTObject'] = self.ModuleMap.GetHistogram()
            self.ModuleMap.Draw(self.Canvas)

        # save canvas
        self.ResultData['Plot']['Format'] = 'png'
        self.Title = 'Bump Bonding Defects Map %s'%("(" + self.ResultData['HiddenData']['SpecialBumpBondingTestName'] + ")" if len(self.ResultData['HiddenData']['SpecialBumpBondingTestName']) > 0 else "")
        self.SaveCanvas()