import ROOT
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_XRayHRQualification_Chips_Chip_Grading_TestResult'
        self.NameSingle='Grading'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_XRayHRQualification_ROC'
        self.Attributes['GradeKeys'] = [
            'ROCGradePerRate',
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
            'Label':'Final ROC Grade'
        }
        self.ResultData['KeyValueDictPairs']['ROCGradePerRate'] = {
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
        self.ResultData['KeyValueDictPairs']['NumberOfLowEfficiencyColumns'] = {
            'Value':'',
            'Label':'# Low Efficiency Columns'
        }
        self.ResultData['KeyValueDictPairs']['NumberOfLowEfficiencyColumnEvents'] = {
            'Value':'',
            'Label':'# Low Efficiency Col. Events'
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
        self.ResultData['KeyValueDictPairs']['ColumnEfficiencyGrade'] = {
            'Value':'',
            'Label':'Column Efficiency Grade'
        }
        self.ResultData['KeyValueDictPairs']['ColumnEfficiencyEventGrade'] = {
            'Value':'',
            'Label':'Column Efficiency Event Grade'
        }
        self.ResultData['KeyList'] += [
                'ROCGrade',
                'ROCGradePerRate',
                'NumberOfLowEfficiencyPixels',
                'NumberOfHotPixels',
                'NumberOfNonUniformColumns',
                'NumberOfNonUniformEvents',
                'NumberOfLowEfficiencyColumns',
                'NumberOfLowEfficiencyColumnEvents',
                'EfficiencyGrade',
                'HotPixelsGrade',
                'HitMapGrade',
                'ColumnReadoutUniformityGrade',
                'ReadoutUniformityOverTimeGrade',
                'ColumnEfficiencyGrade',
                'ColumnEfficiencyEventGrade'
            ]
        for Rate in Rates:
            self.ResultData['HiddenData']['ListOfLowEfficiencyPixels_{Rate}'.format(Rate=Rate)] = []
            self.ResultData['HiddenData']['ListOfHotPixels_{Rate}'.format(Rate=Rate)] = []
            
            
            for NumberKey in self.Attributes['NumberKeys']:
                self.ResultData['HiddenData'][NumberKey+'_{Rate}'.format(Rate=Rate)] = -1
            for GradeKey in self.Attributes['GradeKeys']:
                self.ResultData['HiddenData'][GradeKey+'_{Rate}'.format(Rate=Rate)] = -1
            
	
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
            
            
                    
            ### Efficiency Grade ###    
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
            
            ### Hot Pixels Grade ###
            Grades['HotPixelsGrade'] = 1
            if NumberValues['NumberOfHotPixels'] > self.TestResultEnvironmentObject.GradingParameters['XRayHighRateHotPixels_max_allowed_hot']:
                Grades['HotPixelsGrade'] = 3
            
            ### Hit Map Grade ###
            Grades['HitMapGrade'] = 3
            
            ### Column Readout Uniformity Grade ###
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
            
            ### Readout Uniformity Over Time Grade ###
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
                    Grades['ReadoutUniformityOverTimeGrade'] = 3
            
            
            for NumberKey in self.Attributes['NumberKeys']:
                self.ResultData['HiddenData'][NumberKey+'_{Rate}'.format(Rate=Rate)] = NumberValues[NumberKey]
                self.ResultData['KeyValueDictPairs'][NumberKey]['Value'] = (self.ResultData['KeyValueDictPairs'][NumberKey]['Value']+'/{:d}'.format(NumberValues[NumberKey])).strip('/')
            
            for GradeKey in self.Attributes['GradeKeys']:
                Grades['ROCGradePerRate'] = max(Grades['ROCGradePerRate'], Grades[GradeKey])
                
            ROCGrades.append(Grades['ROCGradePerRate'])
            
            for GradeKey in self.Attributes['GradeKeys']:
                self.ResultData['HiddenData'][GradeKey+'_{Rate}'.format(Rate=Rate)] = Grades[GradeKey]
                self.ResultData['KeyValueDictPairs'][GradeKey]['Value'] = (self.ResultData['KeyValueDictPairs'][GradeKey]['Value']+'/'+GradeMapping[Grades[GradeKey]]).strip('/')
        
        ### Column Efficiency (Event) Grade ###
        NumberOfLowEfficiencyColumns = 0
        NumberOfLowEfficiencyColumnEvents = 0
        ColumnEfficiencyGrade = 1
        ColumnEfficiencyEventGrade = 1
        ColumnEfficiencyPerColumnResultObject = self.ParentObject.ResultData['SubTestResults']['ColumnEfficiencyPerColumn']
        ColumnEfficiencyEventsPerColumnResultObject = self.ParentObject.ResultData['SubTestResults']['ColumnEfficiencyEventsPerColumn']
        ColumnEfficiencySigma = float(ColumnEfficiencyPerColumnResultObject.ResultData['KeyValueDictPairs']['sigma']['Value'])
        ColumnEfficiencyEventBins = int(ColumnEfficiencyEventsPerColumnResultObject.ResultData['HiddenData']['EventBins'])
        for Column in range(self.nCols):
            ColumnEfficiency = ColumnEfficiencyPerColumnResultObject.ResultData['Plot']['ROOTObject'].GetBinContent(Column+1)
            if ColumnEfficiency < self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_Factor_ColEfficiency']*ColumnEfficiencySigma:
                NumberOfLowEfficiencyColumns += 1
                ColumnEfficiencyGrade = 3
            else:
                for EventBin in range(ColumnEfficiencyEventBins):
                    ColumnEfficiencyPerEvent = ColumnEfficiencyEventsPerColumnResultObject.ResultData['Plot']['ROOTObject'].GetBinContent(EventBin+1,Column+1)
                    if ColumnEfficiencyPerEvent < self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_Factor_ColEfficiency']*ColumnEfficiencySigma:
                        NumberOfLowEfficiencyColumnEvents += 1
                        ColumnEfficiencyEventGrade = 3
        self.ResultData['HiddenData']['ColumnEfficiencyGrade'] = ColumnEfficiencyGrade
        self.ResultData['KeyValueDictPairs']['ColumnEfficiencyGrade']['Value'] = GradeMapping[ColumnEfficiencyGrade]
        self.ResultData['HiddenData']['NumberOfLowEfficiencyColumns'] = NumberOfLowEfficiencyColumns
        self.ResultData['KeyValueDictPairs']['NumberOfLowEfficiencyColumns']['Value'] = '{:d}'.format(NumberOfLowEfficiencyColumns)
        self.ResultData['HiddenData']['ColumnEfficiencyGrade'] = ColumnEfficiencyGrade
        self.ResultData['KeyValueDictPairs']['ColumnEfficiencyGrade']['Value'] = GradeMapping[ColumnEfficiencyGrade]
        self.ResultData['HiddenData']['NumberOfLowEfficiencyColumnEvents'] = NumberOfLowEfficiencyColumnEvents
        self.ResultData['KeyValueDictPairs']['NumberOfLowEfficiencyColumnEvents']['Value'] = '{:d}'.format(NumberOfLowEfficiencyColumnEvents)
        ROCGrades.append(ColumnEfficiencyGrade)
        ROCGrades.append(ColumnEfficiencyEventGrade)
        
        
        #ColumnEfficiencyPerColumnResultObject = self.ParentObject.ResultData['SubTestResults']['ColumnEfficiencyPerColumn']
        
        
        ### Final ROC Grade ###
        self.ResultData['KeyValueDictPairs']['ROCGrade']['Value'] = GradeMapping[max(ROCGrades)]
            
            
