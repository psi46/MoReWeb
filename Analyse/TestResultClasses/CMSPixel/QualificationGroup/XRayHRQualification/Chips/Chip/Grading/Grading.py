import ROOT
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_XRayHRQualification_Chips_Chip_Grading_TestResult'
        self.NameSingle='Grading'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_XRayHRQualification_ROC'
        for Rate in self.ParentObject.ParentObject.ParentObject.Attributes['Rates']:
            self.ResultData['HiddenData']['ListOfLowEfficiencyPixels_{Rate}'.format(Rate=Rate)] = []
            self.ResultData['HiddenData']['ListOfHotPixels_{Rate}'.format(Rate=Rate)] = []
            
            self.ResultData['KeyValueDictPairs']['NumberOfLowEfficiencyPixels_{Rate}'.format(Rate=Rate)] = {
                'Value':'{:d}'.format(-1),
                'Label':'# Low Eff. Pixels {Rate}'.format(Rate=Rate)
            }
            self.ResultData['KeyValueDictPairs']['NumberOfHotPixels_{Rate}'.format(Rate=Rate)] = {
                'Value':'{:d}'.format(-1),
                'Label':'# Hot Pixels {Rate}'.format(Rate=Rate)
            }
            self.ResultData['KeyValueDictPairs']['EfficiencyGrade_{Rate}'.format(Rate=Rate)] = {
                'Value':'C',
                'Label':'Efficiency Grade {Rate}'.format(Rate=Rate)
            }
            self.ResultData['KeyValueDictPairs']['HotPixelsGrade_{Rate}'.format(Rate=Rate)] = {
                'Value':'C',
                'Label':'Hot Pixels Grade {Rate}'.format(Rate=Rate)
            }
            self.ResultData['KeyList'] += [
                'NumberOfLowEfficiencyPixels_{Rate}'.format(Rate=Rate),
                'NumberOfHotPixels_{Rate}'.format(Rate=Rate),
                'EfficiencyGrade_{Rate}'.format(Rate=Rate),
                'HotPixelsGrade_{Rate}'.format(Rate=Rate)
            ]
	
    def PopulateResultData(self):
        GradeMapping = {
            1: 'A',
            2: 'B',
            3: 'C'
        }
        
        ChipNo = self.ParentObject.Attributes['ChipNo']
        
        for Rate in self.ParentObject.ParentObject.ParentObject.Attributes['Rates']:
            EfficiencyMapROOTObject = self.ParentObject.ResultData['SubTestResults']['EfficiencyMap_{Rate}'.format(Rate=Rate)].ResultData['Plot']['ROOTObject']
            HotPixelMapROOTObject = self.ParentObject.ResultData['SubTestResults']['HotPixelMap_{Rate}'.format(Rate=Rate)].ResultData['Plot']['ROOTObject']
            
            NumberOfLowEfficiencyPixels = 0
            NumberOfHotPixels = 0
            
            for Row in range(self.nRows):
                for Column in range(self.nCols):
                    PixelEfficiency = EfficiencyMapROOTObject.GetBinContent(Column+1, Row+1)
                    if Row == 0 or Row == self.nRows-1 or Column == 0 or Column == self.nCols -1:
                        EfficiencyThreshold = self.TestResultEnvironmentObject.GradingParameters['XRayHighRateEfficiency_min_allowed_efficiency_edge_{Rate}'.format(Rate=Rate)]
                    else:
                        EfficiencyThreshold = self.TestResultEnvironmentObject.GradingParameters['XRayHighRateEfficiency_min_allowed_efficiency_{Rate}'.format(Rate=Rate)]
                    
                    if PixelEfficiency < EfficiencyThreshold:
                        NumberOfLowEfficiencyPixels += 1
                        self.ResultData['HiddenData']['ListOfLowEfficiencyPixels_{Rate}'.format(Rate=Rate)].append((ChipNo, Row, Column))
                    
                    HotPixelThreshold =self.TestResultEnvironmentObject.GradingParameters['XRayHighRateHotPixels_Threshold']
                    PixelIsHotPixel = HotPixelMapROOTObject.GetBinContent(Column+1, Row+1)
                    if PixelIsHotPixel > 0:
                        NumberOfHotPixels += 1
                        self.ResultData['HiddenData']['ListOfHotPixels_{Rate}'.format(Rate=Rate)].append((ChipNo, Row, Column))
                    
            EfficiencyGrade = 1
            if NumberOfLowEfficiencyPixels > self.TestResultEnvironmentObject.GradingParameters['XRayHighRateEfficiency_max_allowed_loweff_A_{Rate}'.format(Rate=Rate)]:
                EfficiencyGrade = 2
            if NumberOfLowEfficiencyPixels > self.TestResultEnvironmentObject.GradingParameters['XRayHighRateEfficiency_max_allowed_loweff_B_{Rate}'.format(Rate=Rate)]:
                EfficiencyGrade = 3
            
            HotPixelsGrade = 1
            if NumberOfHotPixels > self.TestResultEnvironmentObject.GradingParameters['XRayHighRateHotPixels_max_allowed_hot']:
                HotPixelsGrade = 3
            
            self.ResultData['KeyValueDictPairs']['NumberOfLowEfficiencyPixels_{Rate}'.format(Rate=Rate)]['Value'] = '{:d}'.format(NumberOfLowEfficiencyPixels)
            self.ResultData['KeyValueDictPairs']['NumberOfHotPixels_{Rate}'.format(Rate=Rate)]['Value'] = '{:d}'.format(NumberOfHotPixels)
            
            self.ResultData['KeyValueDictPairs']['EfficiencyGrade_{Rate}'.format(Rate=Rate)]['Value'] = GradeMapping[EfficiencyGrade]
            self.ResultData['KeyValueDictPairs']['HotPixelsGrade_{Rate}'.format(Rate=Rate)]['Value'] = GradeMapping[HotPixelsGrade]
            
