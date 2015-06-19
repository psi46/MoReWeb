import ROOT
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_XRayHRQualification_Chips_Chip_Grading_TestResult'
        self.NameSingle='Grading'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_XRayHRQualification_ROC'
        self.Attributes['GradeKeys'] = {
            'HREfficiency':[
                'EfficiencyGrade',
            ],
            'HRData':[
                'HotPixelsGrade',
                'HitMapGrade',
                'ColumnReadoutUniformityGrade',
                'ReadoutUniformityOverTimeGrade'
            ],
            'HRSCurves':[]
        }
        self.Attributes['NumberKeys'] = {
            'HREfficiency':[
                'NumberOfLowEfficiencyPixels',
            ],
            'HRData':[
                'NumberOfHotPixels',
                'NumberOfNonUniformColumns',
                'NumberOfNonUniformEvents'
            ],
            'HRSCurves':[]
        }
        RateTypes = self.ParentObject.ParentObject.ParentObject.Attributes['Rates'].keys()
        RateData = {}
        for RateType in RateTypes:
            Rates = self.ParentObject.ParentObject.ParentObject.Attributes['Rates'][RateType]
            RateData[RateType]={
                'Rates':Rates,
                'RatesString':('/'.join('{Rate}'.format(Rate=Rate) for Rate in Rates))
            }

        Rates = self.ParentObject.ParentObject.ParentObject.Attributes['InterpolatedEfficiencyRates']
        RateData['InterpolatedEfficiencyRates']={
            'Rates':Rates,
            'RatesString':('/'.join('{Rate}'.format(Rate=Rate) for Rate in Rates))
        }

        self.ResultData['KeyValueDictPairs']['ROCGrade'] = {
            'Value':'',
            'Label':'Final ROC Grade'
        }
        #self.ResultData['KeyValueDictPairs']['NumberOfLowEfficiencyPixels'] = {
        #    'Value':'',
        #    'Label':'# Low Eff. Pixels '+RateData['HREfficiency']['RatesString']
        #}
        self.ResultData['KeyValueDictPairs']['EfficiencyGrade'] = {
            'Value':'',
            'Label':'Efficiency Grade '+RateData['InterpolatedEfficiencyRates']['RatesString']
        }

        self.ResultData['KeyValueDictPairs']['NumberOfHotPixels'] = {
            'Value':'',
            'Label':'# Hot Pixels '+RateData['HRData']['RatesString']
        }
        self.ResultData['KeyValueDictPairs']['NumberOfNonUniformColumns'] = {
            'Value':'',
            'Label':'# Non-Uniform Columns '+RateData['HRData']['RatesString']
        }
        self.ResultData['KeyValueDictPairs']['NumberOfNonUniformEvents'] = {
            'Value':'',
            'Label':'# Non-Uniform Events '+RateData['HRData']['RatesString']
        }
        self.ResultData['KeyValueDictPairs']['NumberOfLowUniformityColumns'] = {
            'Value':'',
            'Label':'# Low Efficiency Columns'
        }
        self.ResultData['KeyValueDictPairs']['NumberOfLowUniformityColumnEvents'] = {
            'Value':'',
            'Label':'# Low Uniformity Col. Events'
        }

        self.ResultData['KeyValueDictPairs']['HotPixelsGrade'] = {
            'Value':'',
            'Label':'Hot Pixels Grade '+RateData['HRData']['RatesString']
        }
        self.ResultData['KeyValueDictPairs']['HitMapGrade'] = {
            'Value':'',
            'Label':'Hit Map Grade '+RateData['HRData']['RatesString']
        }
        self.ResultData['KeyValueDictPairs']['ColumnReadoutUniformityGrade'] = {
            'Value':'',
            'Label':'Col. Read. Unif. Grade '+RateData['HRData']['RatesString']
        }
        self.ResultData['KeyValueDictPairs']['ReadoutUniformityOverTimeGrade'] = {
            'Value':'',
            'Label':'Read. Unif. over t Grade '+RateData['HRData']['RatesString']
        }
        self.ResultData['KeyValueDictPairs']['ColumnUniformityGrade'] = {
            'Value':'',
            'Label':'Column Efficiency Grade'
        }
        self.ResultData['KeyValueDictPairs']['ColumnUniformityEventGrade'] = {
            'Value':'',
            'Label':'Column Efficiency Event Grade'
        }

        self.ResultData['KeyList'] += [
                'ROCGrade',
                'NumberOfHotPixels',
                'NumberOfNonUniformColumns',
                'NumberOfNonUniformEvents',
                'NumberOfLowUniformityColumns',
                'NumberOfLowUniformityColumnEvents',
                'EfficiencyGrade',
                'HotPixelsGrade',
                'HitMapGrade',
                'ColumnReadoutUniformityGrade',
                'ReadoutUniformityOverTimeGrade',
                'ColumnUniformityGrade',
                'ColumnUniformityEventGrade'
            ]
        for Rate in RateData['HREfficiency']['Rates']:
            self.ResultData['HiddenData']['ListOfLowEfficiencyPixels_{Rate}'.format(Rate=Rate)] = []
        for Rate in RateData['HRData']['Rates']:
            self.ResultData['HiddenData']['ListOfHotPixels_{Rate}'.format(Rate=Rate)] = []

            
        for RateType in RateTypes:
            for Rate in RateData[RateType]['Rates']:
                for NumberKey in self.Attributes['NumberKeys'][RateType]:
                    self.ResultData['HiddenData'][NumberKey+'_{Rate}'.format(Rate=Rate)] = -1
                for GradeKey in self.Attributes['GradeKeys'][RateType]:
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
        
        # efficiency grading
        NumberValues = {}
        for NumberKey in self.Attributes['NumberKeys']['HREfficiency']:
            NumberValues[NumberKey] = 0

        Grades = {}
        for GradeKey in self.Attributes['GradeKeys']['HREfficiency']:
            Grades[GradeKey] = -1

        RateIndex = 1
        for Rate in self.ParentObject.ParentObject.ParentObject.Attributes['InterpolatedEfficiencyRates']:
            MeanEfficiency = float(self.ParentObject.ResultData['SubTestResults']['EfficiencyInterpolation'].ResultData['KeyValueDictPairs']['InterpolatedEfficiency%d'%int(Rate)]['Value'])
            Grades['EfficiencyGrade'] = 1
            if MeanEfficiency < self.TestResultEnvironmentObject.GradingParameters['XRayHighRateEfficiency_max_allowed_loweff_A_Rate{RateIndex}'.format(RateIndex=RateIndex)]:
                Grades['EfficiencyGrade'] = 2
            if MeanEfficiency < self.TestResultEnvironmentObject.GradingParameters['XRayHighRateEfficiency_max_allowed_loweff_B_Rate{RateIndex}'.format(RateIndex=RateIndex)]:
                Grades['EfficiencyGrade'] = 3
            RateIndex += 1
            
            for GradeKey in self.Attributes['GradeKeys']['HREfficiency']:
                self.ResultData['HiddenData'][GradeKey+'_{Rate}'.format(Rate=Rate)] = Grades[GradeKey]
                self.ResultData['KeyValueDictPairs'][GradeKey]['Value'] = (self.ResultData['KeyValueDictPairs'][GradeKey]['Value']+'/'+GradeMapping[Grades[GradeKey]]).strip('/')

        # hitmap and uniformity grading
        for Rate in self.ParentObject.ParentObject.ParentObject.Attributes['Rates']['HRData']:
            NumberValues = {}
            for NumberKey in self.Attributes['NumberKeys']['HRData']:
                NumberValues[NumberKey] = 0

            Grades = {}
            for GradeKey in self.Attributes['GradeKeys']['HRData']:
                Grades[GradeKey] = -1

            HotPixelMapROOTObject = self.ParentObject.ResultData['SubTestResults']['HotPixelMap_{Rate}'.format(Rate=Rate)].ResultData['Plot']['ROOTObject']
            HitMapROOTObject = self.ParentObject.ResultData['SubTestResults']['HitMap_{Rate}'.format(Rate=Rate)].ResultData['Plot']['ROOTObject']
            ColumnReadoutUniformityROOTObject = self.ParentObject.ResultData['SubTestResults']['ColumnReadoutUniformity_{Rate}'.format(Rate=Rate)].ResultData['Plot']['ROOTObject']
            ReadoutUniformityOverTimeTestResultObject = self.ParentObject.ResultData['SubTestResults']['ReadoutUniformityOverTime_{Rate}'.format(Rate=Rate)]

            HotPixelThreshold =self.TestResultEnvironmentObject.GradingParameters['XRayHighRateHotPixels_Threshold']
            for Row in range(self.nRows):
                for Column in range(self.nCols):
                    PixelIsHotPixel = HotPixelMapROOTObject.GetBinContent(Column+1, Row+1)
                    if PixelIsHotPixel > 0:
                        NumberValues['NumberOfHotPixels'] += 1
                        self.ResultData['HiddenData']['ListOfHotPixels_{Rate}'.format(Rate=Rate)].append((ChipNo, Column, Row))

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
                    *ColumnReadoutUniformityMean*0.01
                    or ColumnHits > self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_factor_dcol_uniformity_high']
                    *ColumnReadoutUniformityMean*0.01
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
            

            for NumberKey in self.Attributes['NumberKeys']['HRData']:
                self.ResultData['HiddenData'][NumberKey+'_{Rate}'.format(Rate=Rate)] = NumberValues[NumberKey]
                self.ResultData['KeyValueDictPairs'][NumberKey]['Value'] = (self.ResultData['KeyValueDictPairs'][NumberKey]['Value']+'/{:d}'.format(NumberValues[NumberKey])).strip('/')



            for GradeKey in self.Attributes['GradeKeys']['HRData']:
                self.ResultData['HiddenData'][GradeKey+'_{Rate}'.format(Rate=Rate)] = Grades[GradeKey]
                self.ResultData['KeyValueDictPairs'][GradeKey]['Value'] = (self.ResultData['KeyValueDictPairs'][GradeKey]['Value']+'/'+GradeMapping[Grades[GradeKey]]).strip('/')
        
        ### Column Efficiency (Event) Grade ###
        NumberOfLowUniformityColumns = 0
        NumberOfLowUniformityColumnEvents = 0
        ColumnUniformityGrade = 1
        ColumnUniformityEventGrade = 1
        ColumnUniformityPerColumnResultObject = self.ParentObject.ResultData['SubTestResults']['ColumnUniformityPerColumn']
        ColumnUniformityEventsPerColumnResultObject = self.ParentObject.ResultData['SubTestResults']['ColumnUniformityEventsPerColumn']
        ColumnUniformitySigma = float(ColumnUniformityPerColumnResultObject.ResultData['KeyValueDictPairs']['sigma']['Value'])
        ColumnUniformityEventBins = int(ColumnUniformityEventsPerColumnResultObject.ResultData['HiddenData']['EventBins'])
        for Column in range(self.nCols):
            ColumnUniformity = ColumnUniformityPerColumnResultObject.ResultData['Plot']['ROOTObject'].GetBinContent(Column+1)
            if ColumnUniformity < self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_Factor_ColUniformity']*ColumnUniformitySigma:
                NumberOfLowUniformityColumns += 1
                ColumnUniformityGrade = 3
            else:
                for EventBin in range(ColumnUniformityEventBins):
                    ColumnUniformityPerEvent = ColumnUniformityEventsPerColumnResultObject.ResultData['Plot']['ROOTObject'].GetBinContent(EventBin+1,Column+1)
                    if ColumnUniformityPerEvent < self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_Factor_ColUniformity']*ColumnUniformitySigma:
                        NumberOfLowUniformityColumnEvents += 1
                        ColumnUniformityEventGrade = 3
        self.ResultData['HiddenData']['ColumnUniformityGrade'] = ColumnUniformityGrade
        self.ResultData['KeyValueDictPairs']['ColumnUniformityGrade']['Value'] = GradeMapping[ColumnUniformityGrade]
        self.ResultData['HiddenData']['NumberOfLowUniformityColumns'] = NumberOfLowUniformityColumns
        self.ResultData['KeyValueDictPairs']['NumberOfLowUniformityColumns']['Value'] = '{:d}'.format(NumberOfLowUniformityColumns)
        self.ResultData['HiddenData']['ColumnUniformityGrade'] = ColumnUniformityGrade
        self.ResultData['KeyValueDictPairs']['ColumnUniformityGrade']['Value'] = GradeMapping[ColumnUniformityGrade]
        self.ResultData['HiddenData']['NumberOfLowUniformityColumnEvents'] = NumberOfLowUniformityColumnEvents
        self.ResultData['KeyValueDictPairs']['NumberOfLowUniformityColumnEvents']['Value'] = '{:d}'.format(NumberOfLowUniformityColumnEvents)
        ROCGrades.append(ColumnUniformityGrade)
        ROCGrades.append(ColumnUniformityEventGrade)
        

        
        ### Final ROC Grade ###
        self.ResultData['KeyValueDictPairs']['ROCGrade']['Value'] = GradeMapping[max(ROCGrades)]
            
            
