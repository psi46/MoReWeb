import ROOT
import AbstractClasses

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_XRayHRQualification_HitOverview_TestResult'
        self.NameSingle='HitOverview'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'

    def PopulateResultData(self):
        ROOT.gPad.SetLogy(0)
        ROOT.gStyle.SetOptStat(0)

        xBins = 8 * self.nCols + 1
        yBins = 2 * self.nRows + 1
        self.ResultData['Plot']['ROOTObject'] = ROOT.TH2D(self.GetUniqueID(), "", xBins, 0., xBins, yBins, 0., yBins);         

        Directory = self.ParentObject.Attributes['SCurvePaths']['HRSCurves_{Rate}'.format(Rate=self.Attributes['Rate'])]
        SCurveDataFileName = self.ParentObject.ParentObject.HistoDict.get('HighRate', 'SCurveDataFileName')

        for i in self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults']:
            ChipTestResultObject = self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults'][i]
            ChipNo = ChipTestResultObject.Attributes['ChipNo']

            SCurveFileName = Directory + '/' + self.ParentObject.ParentObject.HistoDict.get('HighRate', 'SCurveFileName').format(ChipNo=ChipNo)
            SCurveFile = open(SCurveFileName, "r")

            if not SCurveFile:
                raise Exception('Cannot find SCurveFile "%s"'%SCurveFileName)
            else:
                Line = SCurveFile.readline()
                Line = SCurveFile.readline()

                for column in range(self.nCols): #Columns
                    for row in range(self.nRows): #Rows
                        Line = SCurveFile.readline()
                        if Line:
                            LineArray = Line.strip().split()
                            Threshold = float(LineArray[0])
                            if 0 < Threshold < 10000:
                                self.UpdatePlot(ChipNo, column, row, Threshold)
            SCurveFile.close()


        if self.ResultData['Plot']['ROOTObject']:
            self.ResultData['Plot']['ROOTObject'].SetTitle("")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Column No.")
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Row No.")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].GetZaxis().SetTitle("electrons")
            self.ResultData['Plot']['ROOTObject'].GetZaxis().SetTitleOffset(0.5)
            self.ResultData['Plot']['ROOTObject'].GetZaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].Draw('colz')

        self.ResultData['Plot']['Format'] = 'png'

        self.Title = 'Threshold {Rate}'.format(Rate=self.Attributes['Rate'])
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
