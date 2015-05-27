import ROOT
import AbstractClasses
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Fulltest_Chips_Chip_PHCalibrationGainMap_TestResult'
        self.NameSingle='PHCalibrationGainMap'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'



    def PopulateResultData(self):

        object = self.ParentObject.ResultData['SubTestResults']['PHCalibrationGain'].ResultData['Plot']['ROOTObject_hGainMap']
        self.ResultData['Plot']['ROOTObject'] = object.Clone(self.GetUniqueID())
        ROOT.gPad.SetLogy(0)
        if self.ResultData['Plot']['ROOTObject']:
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Column No.")
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Row No.")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].Draw("colz")
        else:
            raise Exception('PHCalibrationGainMap - ROOT Object does not exists!')
        self.Title = 'PH Calibration Gain Map'
        self.SaveCanvas()        
#
