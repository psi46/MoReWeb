import ROOT
import AbstractClasses
import ROOT
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.NameSingle='ReadbackStatus'
        self.Name='CMSPixel_QualificationGroup_Reception_Chips_Chip_%s_TestResult'%self.NameSingle
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'

    def PopulateResultData(self):
        ROOT.gPad.SetLogy(0)
        ROOT.gStyle.SetOptStat(0)

        self.ResultData['Plot']['ROOTObject'] = ROOT.TH2D(self.GetUniqueID(), "", 8, 0, 8, 2, 0, 2)
        ModuleCalibrationGood = True
        if self.ResultData['Plot']['ROOTObject']:

            for i in self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults']:
                ChipTestResultObject = self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults'][i]
                chipNo = ChipTestResultObject.Attributes['ChipNo']

                ParameterAllowedRanges = {'par0vd':[-50,50], 'par1vd':[50,80],'par0va':[-50,50],'par1va':[45,80],'par0rbia':[0,30],'par1rbia':[0.4,1.5],'par0tbia':[2,7],'par1tbia':[0,0.5],'par2tbia':[-0.001,0]}

                Uncalibrated = True
                RangeOk = True
                FileMissing = False

                try:
                    for Parameter,Range in ParameterAllowedRanges.items():
                        Value = float(ChipTestResultObject.ResultData['SubTestResults']['ReadbackCal'].ResultData['KeyValueDictPairs'][Parameter]['Value'])
                        if abs(Value-1.0) > 0.001:
                            Uncalibrated = False
                        if Value > Range[1] or Value < Range[0]:
                            RangeOk = False
                            print "range not ok ", chipNo, " : ", Parameter, " ", Value, " not in ", Range
                            ModuleCalibrationGood = False
                except:
                    FileMissing = True

                if chipNo>7:
                    binX = chipNo-7
                    binY = 1
                else:
                    binX = 8-chipNo
                    binY = 2

                colorMissing = 0.1
                colorUncalibrated = 0.75
                colorBad = 1.0
                colorOk = 0.5

                if FileMissing:
                    self.ResultData['Plot']['ROOTObject'].SetBinContent(binX,binY,colorMissing)
                    ModuleCalibrationGood = False
                elif Uncalibrated:
                    self.ResultData['Plot']['ROOTObject'].SetBinContent(binX,binY,colorUncalibrated)
                    ModuleCalibrationGood = False
                elif not RangeOk:
                    self.ResultData['Plot']['ROOTObject'].SetBinContent(binX,binY,colorBad)
                else:
                    self.ResultData['Plot']['ROOTObject'].SetBinContent(binX,binY,colorOk)

                self.ResultData['Plot']['ROOTObject'].GetZaxis().SetRangeUser(0, 1.0)
                self.ResultData['Plot']['ROOTObject'].SetTitle("")
                self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("")
                self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("")
                self.ResultData['Plot']['ROOTObject'].Draw('colz')
                self.SaveCanvas()


        self.ResultData['KeyValueDictPairs'] = {
            'ModuleCalibrationGood': {
                'Value': 'ok' if ModuleCalibrationGood else 'bad/unfinished',
                'Label':'Readback Calibration'
            },
            'ReadbackExplanation': {
                'Value': 'Red means not calibrated or parameter value outside of bulk distribution',
                'Label': 'Colors'
            }
        }
        self.ResultData['KeyList'] = ['ModuleCalibrationGood', 'ReadbackExplanation']