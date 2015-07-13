import ROOT
import AbstractClasses
import array

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_XRayHRQualification_HitOverview_TestResult'
        self.NameSingle='HitOverview'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'

    def PopulateResultData(self):
        ROOT.gPad.SetLogy(0)
        ROOT.gStyle.SetOptStat(0)
        self.Canvas.Clear()

        xBins = 8 * self.nCols + 1
        yBins = 2 * self.nRows + 1
        self.ResultData['Plot']['ROOTObject'] = ROOT.TH2D(self.GetUniqueID(), "", xBins, 0., xBins, yBins, 0., yBins)

        # copy ROC data to module data
        for i in self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults']:
            ChipTestResultObject = self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults'][i]
            histo = ChipTestResultObject.ResultData['SubTestResults']['HitMap_{Rate}'.format(Rate=self.Attributes['Rate'])].ResultData['Plot']['ROOTObject']
            chipNo = ChipTestResultObject.Attributes['ChipNo']

            for col in range(self.nCols): 
                for row in range(self.nRows):
                    result = histo.GetBinContent(col + 1, row + 1)
                    self.UpdatePlot(chipNo, col, row, result)

        if self.ResultData['Plot']['ROOTObject']:

            # calculate scale for hitmap
            self.ResultData['Plot']['ROOTObject'].GetZaxis().SetRangeUser(0, self.ResultData['Plot']['ROOTObject'].GetMaximum())

            XProjection = self.ResultData['Plot']['ROOTObject'].ProjectionX('hproj_{Rate}_{id}'.format(Rate=self.Attributes['Rate'], id=self.GetUniqueID()), 50, 50)
            #Quantiles = array.array('d', [0])
            #QuantilePositions = array.array('d', [0.5])
            #XProjection.GetQuantiles(len(QuantilePositions), Quantiles, QuantilePositions)
            #XProjection.Delete()
            XProjectionList = []
            for col in range(XProjection.GetXaxis().GetFirst(), XProjection.GetXaxis().GetLast()+1):
                XProjectionList.append(XProjection.GetBinContent(col))
            XProjectionList.sort()
            Median = XProjectionList[int(len(XProjectionList)/2)]

            self.ResultData['Plot']['ROOTObject'].SetTitle("")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Column No.")
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Row No.")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].GetZaxis().SetTitle("#hits")
            self.ResultData['Plot']['ROOTObject'].GetZaxis().SetTitleOffset(0.5)
            self.ResultData['Plot']['ROOTObject'].GetZaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].Draw('colz')

            if self.ResultData['Plot']['ROOTObject'].GetMaximum() > Median*3:
                self.ResultData['Plot']['ROOTObject'].GetZaxis().SetRangeUser(0, Median*3)

            ROOT.gPad.Update()

        self.ResultData['Plot']['Format'] = 'png'

        self.Title = 'Hit Map {Rate}'.format(Rate=self.Attributes['Rate'])
        self.SaveCanvas()

        if self.ResultData['Plot']['ROOTObject']:
            self.ResultData['Plot']['ROOTObject'].GetZaxis().SetRangeUser(0, self.ResultData['Plot']['ROOTObject'].GetMaximum())

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
