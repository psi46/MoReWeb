import ROOT
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_XRayHRQualification_Chips_Chip_Grading_TestResult'
        self.NameSingle='Grading'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_XRayHRQualification_ROC'
        self.Attributes['GradeKeys'] = [
            'ROCGrade',
            'EfficiencyGrade',
            'HotPixelsGrade',
            'HitMapGrade', 
            'ColumnReadoutUniformityGrade',
            'ReadoutUniformityOverTimeGrade'
        ]
        self.Attributes['NumberKeys'] = [
            'NumberOfLowEfficiencyPixels',
            'NumberOfHotPixels',
            'NumberOfNonUniformColumns',
            'NumberOfNonUniformEvents'
        ]
        Rates = self.ParentObject.ParentObject.ParentObject.Attributes['Rates']
        RatesString = ('/'.join('{Rate}'.format(Rate=Rate) for Rate in Rates))
        self.ResultData['KeyValueDictPairs']['ROCGrade'] = {
            'Value':'',
            'Label':'ROC Grade '+RatesString
        }
        self.ResultData['KeyValueDictPairs']['NumberOfLowEfficiencyPixels'] = {
            'Value':'',
            'Label':'# Low Eff. Pixels '+RatesString
        }
        self.ResultData['KeyValueDictPairs']['NumberOfHotPixels'] = {
            'Value':'',
            'Label':'# Hot Pixels '+RatesString
        }
        self.ResultData['KeyValueDictPairs']['NumberOfNonUniformColumns'] = {
            'Value':'',
            'Label':'# Non-Uniform Columns '+RatesString
        }
        self.ResultData['KeyValueDictPairs']['NumberOfNonUniformEvents'] = {
            'Value':'',
            'Label':'# Non-Uniform Events '+RatesString
        }
        self.ResultData['KeyValueDictPairs']['EfficiencyGrade'] = {
            'Value':'',
            'Label':'Efficiency Grade '+RatesString
        }
        self.ResultData['KeyValueDictPairs']['HotPixelsGrade'] = {
            'Value':'',
            'Label':'Hot Pixels Grade '+RatesString
        }
        self.ResultData['KeyValueDictPairs']['HitMapGrade'] = {
            'Value':'',
            'Label':'Hit Map Grade '+RatesString
        }
        self.ResultData['KeyValueDictPairs']['ColumnReadoutUniformityGrade'] = {
            'Value':'',
            'Label':'Col. Read. Unif. Grade '+RatesString
        }
        self.ResultData['KeyValueDictPairs']['ReadoutUniformityOverTimeGrade'] = {
            'Value':'',
            'Label':'Read. Unif. over t Grade '+RatesString
        }
        self.ResultData['KeyList'] += [
                'ROCGrade',
                'NumberOfLowEfficiencyPixels',
                'NumberOfHotPixels',
                'NumberOfNonUniformColumns',
                'NumberOfNonUniformEvents',
                'EfficiencyGrade',
                'HotPixelsGrade',
                'HitMapGrade',
                'ColumnReadoutUniformityGrade',
                'ReadoutUniformityOverTimeGrade'
            ]
        for Rate in Rates:
            self.ResultData['HiddenData']['ListOfLowEfficiencyPixels_{Rate}'.format(Rate=Rate)] = []
            self.ResultData['HiddenData']['ListOfHotPixels_{Rate}'.format(Rate=Rate)] = []
            
            self.ResultData['HiddenData']['NumberOfLowEfficiencyPixels_{Rate}'.format(Rate=Rate)] = -1
            self.ResultData['HiddenData']['NumberOfHotPixels_{Rate}'.format(Rate=Rate)] = -1
            self.ResultData['HiddenData']['NumberOfNonUniformColumns_{Rate}'.format(Rate=Rate)] = -1
            self.ResultData['HiddenData']['NumberOfNonUniformEvents_{Rate}'.format(Rate=Rate)] = -1
            self.ResultData['HiddenData']['EfficiencyGrade_{Rate}'.format(Rate=Rate)] = -1
            self.ResultData['HiddenData']['HotPixelsGrade_{Rate}'.format(Rate=Rate)] = -1
            self.ResultData['HiddenData']['HitMapGrade_{Rate}'.format(Rate=Rate)] = -1
            self.ResultData['HiddenData']['ColumnReadoutUniformityGrade_{Rate}'] = -1
            self.ResultData['HiddenData']['ReadoutUniformityOverTimeGrade_{Rate}'] = -1
            
	
    def PopulateResultData(self):
        GradeMapping = {
            -1:'N/A',
            1: 'A',
            2: 'B',
            3: 'C'
        }
        ROCGrades = []
        
        ChipNo = self.ParentObject.Attributes['ChipNo']
        
        for Rate in self.ParentObject.ParentObject.ParentObject.Attributes['Rates']:
            EfficiencyMapROOTObject = self.ParentObject.ResultData['SubTestResults']['EfficiencyMap_{Rate}'.format(Rate=Rate)].ResultData['Plot']['ROOTObject']
            EfficiencyDistributionTestResultObject = self.ParentObject.ResultData['SubTestResults']['EfficiencyDistribution_{Rate}'.format(Rate=Rate)]
            HotPixelMapROOTObject = self.ParentObject.ResultData['SubTestResults']['HotPixelMap_{Rate}'.format(Rate=Rate)].ResultData['Plot']['ROOTObject']
            HitMapROOTObject = self.ParentObject.ResultData['SubTestResults']['HitMap_{Rate}'.format(Rate=Rate)].ResultData['Plot']['ROOTObject']
            ColumnReadoutUniformityROOTObject = self.ParentObject.ResultData['SubTestResults']['ColumnReadoutUniformity_{Rate}'.format(Rate=Rate)].ResultData['Plot']['ROOTObject']
            ReadoutUniformityOverTimeTestResultObject = self.ParentObject.ResultData['SubTestResults']['ReadoutUniformityOverTime_{Rate}'.format(Rate=Rate)]
            
            NumberOfLowEfficiencyPixels = 0
            NumberOfHotPixels = 0
            
            NumberValues = {}
            for NumberKey in self.Attributes['NumberKeys']:
                NumberValues[NumberKey] = 0
            
            Grades = {}
            for GradeKey in self.Attributes['GradeKeys']:
                Grades[GradeKey] = -1
                
            for Row in range(self.nRows):
                for Column in range(self.nCols):
                    PixelEfficiency = EfficiencyMapROOTObject.GetBinContent(Column+1, Row+1)
                    if Row == 0 or Row == self.nRows-1 or Column == 0 or Column == self.nCols -1:
                        EfficiencyThreshold = self.TestResultEnvironmentObject.GradingParameters['XRayHighRateEfficiency_min_allowed_efficiency_edge_{Rate}'.format(Rate=Rate)]
                    else:
                        EfficiencyThreshold = self.TestResultEnvironmentObject.GradingParameters['XRayHighRateEfficiency_min_allowed_efficiency_{Rate}'.format(Rate=Rate)]
                    
                    if PixelEfficiency < EfficiencyThreshold:
                        NumberValues['NumberOfLowEfficiencyPixels'] += 1
                        self.ResultData['HiddenData']['ListOfLowEfficiencyPixels_{Rate}'.format(Rate=Rate)].append((ChipNo, Column, Row))
                    
                    HotPixelThreshold =self.TestResultEnvironmentObject.GradingParameters['XRayHighRateHotPixels_Threshold']
                    PixelIsHotPixel = HotPixelMapROOTObject.GetBinContent(Column+1, Row+1)
                    if PixelIsHotPixel > 0:
                        NumberValues['NumberOfHotPixels'] += 1
                        self.ResultData['HiddenData']['ListOfHotPixels_{Rate}'.format(Rate=Rate)].append((ChipNo, Column, Row))
            
            
                    
                
            MeanEfficiency = float(EfficiencyDistributionTestResultObject.ResultData['KeyValueDictPairs']['mu']['Value'])
            
            Grades['EfficiencyGrade'] = 1
            if( NumberValues['NumberOfLowEfficiencyPixels'] > self.TestResultEnvironmentObject.GradingParameters['XRayHighRateEfficiency_max_allowed_loweff_A_{Rate}'.format(Rate=Rate)]
                and MeanEfficiency > self.TestResultEnvironmentObject.GradingParameters['XRayHighRateEfficiency_min_allowed_efficiency_{Rate}'.format(Rate=Rate)]
            ):
                Grades['EfficiencyGrade'] = 2
            if( NumberValues['NumberOfLowEfficiencyPixels'] > self.TestResultEnvironmentObject.GradingParameters['XRayHighRateEfficiency_max_allowed_loweff_B_{Rate}'.format(Rate=Rate)]
                or MeanEfficiency < self.TestResultEnvironmentObject.GradingParameters['XRayHighRateEfficiency_min_allowed_efficiency_{Rate}'.format(Rate=Rate)]
            ):
                Grades['EfficiencyGrade'] = 3
            
            Grades['HotPixelsGrade'] = 1
            if NumberValues['NumberOfHotPixels'] > self.TestResultEnvironmentObject.GradingParameters['XRayHighRateHotPixels_max_allowed_hot']:
                Grades['HotPixelsGrade'] = 3
            
            Grades['HitMapGrade'] = 3
            
            
            Grades['ColumnReadoutUniformityGrade'] = 1         
            ColumnReadoutUniformityMean = float(self.ParentObject.ResultData['SubTestResults']['ColumnReadoutUniformity_{Rate}'.format(Rate=Rate)].ResultData['KeyValueDictPairs']['mu']['Value'])
            NumberValues['NumberOfNonUniformColumns'] = 0
            for Column in range(self.nCols):
                ColumnHits = ColumnReadoutUniformityROOTObject.GetBinContent(Column+1)
                if( ColumnHits < self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_factor_dcol_uniformity_low']
                    *ColumnReadoutUniformityMean
                    or ColumnHits > self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_factor_dcol_uniformity_high']
                    *ColumnReadoutUniformityMean  
                ):
                    NumberValues['NumberOfNonUniformColumns'] += 1
                    Grades['ColumnReadoutUniformityGrade'] = 3
            
            Grades['ReadoutUniformityOverTimeGrade'] = 1            
            ReadoutUniformityOverTimeMean = float(ReadoutUniformityOverTimeTestResultObject.ResultData['KeyValueDictPairs']['mu']['Value'])
            ReadoutUniformityOverTimeSigma = float(ReadoutUniformityOverTimeTestResultObject.ResultData['KeyValueDictPairs']['sigma']['Value'])
            NumberValues['NumberOfNonUniformEvents'] = 0
            for Event in range(ReadoutUniformityOverTimeTestResultObject.ResultData['Plot']['ROOTObject'].GetXaxis().GetLast()-1):
                EventHits = ReadoutUniformityOverTimeTestResultObject.ResultData['Plot']['ROOTObject'].GetBinContent(Event+1)
                if( abs(EventHits-ReadoutUniformityOverTimeMean) < self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_factor_readout_uniformity']
                    *ReadoutUniformityOverTimeSigma
                ):
                    NumberValues['NumberOfNonUniformEvents'] += 1
                    Grades['ColumnReadoutUniformityGrade'] = 3
            
            
            for NumberKey in self.Attributes['NumberKeys']:
                self.ResultData['HiddenData'][NumberKey+'_{Rate}'.format(Rate=Rate)] = NumberValues[NumberKey]
                self.ResultData['KeyValueDictPairs'][NumberKey]['Value'] = (self.ResultData['KeyValueDictPairs'][NumberKey]['Value']+'/{:d}'.format(NumberValues[NumberKey])).strip('/')
            
            
            for GradeKey in self.Attributes['GradeKeys']:
                Grades['ROCGrade'] = max(Grades['ROCGrade'], Grades[GradeKey])
                
            ROCGrades.append(Grades['ROCGrade'])
            
            for GradeKey in self.Attributes['GradeKeys']:
                self.ResultData['HiddenData'][GradeKey+'_{Rate}'.format(Rate=Rate)] = Grades[GradeKey]
                self.ResultData['KeyValueDictPairs'][GradeKey]['Value'] = (self.ResultData['KeyValueDictPairs'][GradeKey]['Value']+'/'+GradeMapping[Grades[GradeKey]]).strip('/')
                
        #self.ResultData['KeyValueDictPairs']['ROCGrade']['Value'] = GradeMapping[max(ROCGrades)]
            
            
