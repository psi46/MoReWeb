import ROOT
import AbstractClasses
from AbstractClasses.ModuleMap import ModuleMap

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_XrayCalibrationSpectrum_HitmapOverview_TestResult'
        self.NameSingle='HitmapOverview'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'

    def PopulateResultData(self):
        ROOT.gPad.SetLogy(0)
        ROOT.gStyle.SetOptStat(0)

        # initialize module map
        self.ModuleMap = ModuleMap(Name=self.GetUniqueID(), nChips=self.ParentObject.Attributes['NumberOfChips'], StartChip=self.ParentObject.Attributes['StartChip'])

        for i in self.ParentObject.ResultData['SubTestResults']['Chips_Xray'].ResultData['SubTestResults']:
            ChipTestResultObject = self.ParentObject.ResultData['SubTestResults']['Chips_Xray'].ResultData['SubTestResults'][i]
            chipNo = ChipTestResultObject.Attributes['ChipNo']
            SubTestKey = 'Xray_HitMap_{Method}_{Target}_Chip{Chip}'.format(Method=self.Attributes['Method'], Target=self.Attributes['Target'], Chip=chipNo)
            histo = ChipTestResultObject.ResultData['SubTestResults'][SubTestKey].ResultData['Plot']['ROOTObject']

            for col in range(self.nCols):
                for row in range(self.nRows):
                    result = histo.GetBinContent(col + 1, row + 1)
                    self.ModuleMap .UpdatePlot(chipNo, col, row, result)

        # draw module map
        if self.ModuleMap:
            self.ResultData['Plot']['ROOTObject'] = self.ModuleMap.GetHistogram()
            self.ModuleMap.SetContour(100)

            self.ResultData['Plot']['ROOTObject'].GetZaxis().SetRangeUser(0, self.ResultData['Plot']['ROOTObject'].GetMaximum())

            try:
                XProjection = self.ResultData['Plot']['ROOTObject'].ProjectionX('hproj_{Target}_{id}'.format(Target=self.Attributes['Target'], id=self.GetUniqueID()), 50, 50)
                XProjectionList = []
                for col in range(XProjection.GetXaxis().GetFirst(), XProjection.GetXaxis().GetLast()+1):
                    XProjectionList.append(XProjection.GetBinContent(col))
                XProjectionList.sort()
                Median = XProjectionList[int(len(XProjectionList)/2)]

                if Median < 1:
                    XProjectionList = []
                    for col in range(self.nCols):
                        XProjectionList.append(self.ResultData['Plot']['ROOTObject'].GetBinContent(7*self.nCols + col, int(self.nRows * 1.5)))
                    XProjectionList.sort()
                    Median = XProjectionList[int(len(XProjectionList) / 2)]

                if self.ResultData['Plot']['ROOTObject'].GetMaximum() > Median*3:
                    self.ResultData['Plot']['ROOTObject'].GetZaxis().SetRangeUser(0, Median*3)
            except:
                pass

            self.ModuleMap.Draw(Canvas=self.Canvas, TitleZ="# hits")

        # save canvas
        self.ResultData['Plot']['Format'] = 'png'
        self.Title = 'Hit Map {Target}'.format(Target=self.Attributes['Target'])
        self.SaveCanvas()

    def UpdatePlot(self, chipNo, col, row, value):
        result = value
        if chipNo < 8:
            tmpCol = 8 * self.nCols - 1 - chipNo * self.nCols - col
            tmpRow = 2 * self.nRows - 1 - row
        else:
            tmpCol = (chipNo % 8 * self.nCols + col)
            tmpRow = row
        # Get the data from the chip sub test result hitmap

        if result and self.verbose:
            print chipNo, col, row, '--->', tmpCol, tmpRow, result
        self.ResultData['Plot']['ROOTObject'].Fill(tmpCol, tmpRow, result)
