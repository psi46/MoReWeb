import ROOT
import AbstractClasses
from AbstractClasses.ModuleMap import ModuleMap


class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_XRayHRQualification_HitOverview_TestResult'
        self.NameSingle='HitOverview'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'

    def PopulateResultData(self):
        ROOT.gStyle.SetOptStat(0)
        self.Canvas.Clear()

        # initialize module map
        self.ModuleMap = ModuleMap(Name=self.GetUniqueID(), nChips=self.ParentObject.Attributes['NumberOfChips'], StartChip=self.ParentObject.Attributes['StartChip'])

        try:
            Rate = self.Attributes['Rate']
        except:
            Rate = ''

        # copy ROC data to module data
        for i in self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults']:
            ChipTestResultObject = self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults'][i]
            histo = ChipTestResultObject.ResultData['SubTestResults']['HitMap_{Rate}'.format(Rate=Rate) if Rate else 'HitMap'].ResultData['Plot']['ROOTObject']
            chipNo = ChipTestResultObject.Attributes['ChipNo']

            for col in range(self.nCols): 
                for row in range(self.nRows):
                    result = histo.GetBinContent(col + 1, row + 1)
                    self.ModuleMap.UpdatePlot(chipNo, col, row, result)

        # draw module map
        if self.ModuleMap:
            self.ResultData['Plot']['ROOTObject'] = self.ModuleMap.GetHistogram()
            self.ModuleMap.SetContour(100)

            self.ResultData['Plot']['ROOTObject'].GetZaxis().SetRangeUser(0, self.ResultData['Plot']['ROOTObject'].GetMaximum())

            try:
                XProjection = self.ResultData['Plot']['ROOTObject'].ProjectionX('hproj_{Rate}_{id}'.format(Rate=Rate, id=self.GetUniqueID()), 50, 50)
                XProjectionList = []
                for col in range(XProjection.GetXaxis().GetFirst(), XProjection.GetXaxis().GetLast()+1):
                    XProjectionList.append(XProjection.GetBinContent(col))
                XProjectionList.sort()
                Median = XProjectionList[int(len(XProjectionList)/2)]

                if self.ResultData['Plot']['ROOTObject'].GetMaximum() > Median*3:
                    self.ResultData['Plot']['ROOTObject'].GetZaxis().SetRangeUser(0, Median*3)
            except:
                pass

            self.ModuleMap.Draw(Canvas=self.Canvas, TitleZ="# hits")

        # save canvas
        self.ResultData['Plot']['Format'] = 'png'
        self.Title = 'Hit Map {Rate}'.format(Rate=Rate)
        self.SaveCanvas()