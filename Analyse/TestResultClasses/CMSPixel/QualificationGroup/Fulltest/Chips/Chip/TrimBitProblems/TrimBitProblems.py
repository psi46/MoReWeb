import ROOT
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter
try:
    set
except NameError:
    from sets import Set as set
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_Fulltest_Chips_Chip_TrimBitProblems_TestResult'
        self.NameSingle = 'TrimBitProblems'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'
        self.chipNo = self.ParentObject.Attributes['ChipNo']

    def PopulateResultData(self):

        ROOT.gStyle.SetOptStat(0);
        self.ResultData['Plot']['ROOTObject'] =  ROOT.TH2D(self.GetUniqueID(), "", self.nCols, 0., self.nCols, self.nRows, 0., self.nRows ) # htm
        # TH2D
        TrimBitHistograms = []
        ChipNo = self.ParentObject.Attributes['ChipNo']
        HistoDict = self.ParentObject.ParentObject.ParentObject.HistoDict
        self.DeadTrimbitsList = set()
        self.PixelNotAliveList = self.ParentObject.ResultData['SubTestResults']['PixelMap'].ResultData['KeyValueDictPairs']['NotAlivePixels']['Value']
        for k in range(5):
            histname = HistoDict.get(self.NameSingle, 'TrimBitMap%d' % k)
            tmpHistogram = HistoGetter.get_histo(self.ParentObject.ParentObject.FileHandle, histname, rocNo = ChipNo)
            tmpHistogram = tmpHistogram.Clone(self.GetUniqueID())
            TrimBitHistograms.append(tmpHistogram)
        for col in range(self.nCols):  # Column
            for row in range(self.nRows):  # Row
                deadTrimBits = self.GetDeadTrimBits(col, row, TrimBitHistograms)
                self.ResultData['Plot']['ROOTObject'].Fill(col, row, deadTrimBits)

        if self.ResultData['Plot']['ROOTObject']:

            self.ResultData['Plot']['ROOTObject'].SetTitle("");
            self.ResultData['Plot']['ROOTObject'].GetZaxis().SetRangeUser(0., self.nTotalChips);
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Trim bit Problems");
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("entries");
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Column No.");
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Row No.");
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle();
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5);
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle();
            self.ResultData['Plot']['ROOTObject'].Draw('colz');


        self.SaveCanvas()
        self.Title = 'Trim Bit Problems'
        self.ResultData['KeyValueDictPairs'] = {
            'DeadTrimbits': {
                'Value':self.DeadTrimbitsList,
                'Label':'Dead Trimbits'
            },
            'nDeadTrimbits': {
                'Value':'{0:1.0f}'.format(len(self.DeadTrimbitsList)),
                'Label':'Dead Trimbits'
            },
            'nDeadPixels': {
                'Value':'{0:1.0f}'.format(len(self.PixelNotAliveList)),
                'Label':'including Dead Pixels'
            },

                                                }
        self.ResultData['KeyList'] = ['nDeadTrimbits', 'nDeadPixels']

    def GetDeadTrimBits(self, column, row, TrimBitHistograms):
        gradingCriteria = self.TestResultEnvironmentObject.GradingParameters['TrimBitDifference']
        excludeTrimBit14 = bool(self.TestResultEnvironmentObject.GradingParameters['excludeTrimBit14'])
        retVal = 0
        for k in range(1, 5):
            trimBit0 = TrimBitHistograms[0].GetBinContent(column + 1, row + 1)
            trimBitK = TrimBitHistograms[k].GetBinContent(column + 1, row + 1)
            if excludeTrimBit14 and k == 1:
                continue
            TrimBitDifference = abs(trimBitK - trimBit0)
            if TrimBitDifference <= gradingCriteria :
                self.DeadTrimbitsList.add((self.chipNo, column, row))
                retVal += 2 ** (4 - (k - 1))
                if self.verbose:
                    print 'Dead TrimBit: added %2d,%2d %d' % (column, row, k), trimBitK, trimBit0, TrimBitDifference, gradingCriteria, (TrimBitDifference <= gradingCriteria), retVal
        return retVal
