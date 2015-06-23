import ROOT
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter
import math

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
                'ColumnUniformityGrade',
                'ReadoutUniformityOverTimeGrade',
                'ColumnReadoutUniformityOverTimeGrade'
            ],
            'HRSCurves':[]
        }
        self.Attributes['NumberKeys'] = {
            'HREfficiency':[
                'NumberOfLowEfficiencyPixels',
                'Efficiency'
            ],
            'HRData':[
                'NumberOfHotPixels',
                'NumberOfNonUniformColumns',
                'NumberOfNonUniformEvents',
                'NumberOfNonUniformColumnEvents',
                'MissingHits'
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
        self.ResultData['KeyValueDictPairs']['Efficiency'] = {
            'Value':'',
            'Label':'Efficiency '+RateData['InterpolatedEfficiencyRates']['RatesString']
        }
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
            'Label':'# Non-Uniform ROC Events '+RateData['HRData']['RatesString']
        }
        self.ResultData['KeyValueDictPairs']['NumberOfNonUniformColumnEvents'] = {
            'Value':'',
            'Label':'# Non-Uniform Col. Events '+RateData['HRData']['RatesString']
        }
        self.ResultData['KeyValueDictPairs']['MissingHits'] = {
            'Value':'',
            'Label':'# Missing hits '+RateData['HRData']['RatesString']
        }
        self.ResultData['KeyValueDictPairs']['HotPixelsGrade'] = {
            'Value':'',
            'Label':'Hot Pixels Grade '+RateData['HRData']['RatesString']
        }
        self.ResultData['KeyValueDictPairs']['HitMapGrade'] = {
            'Value':'',
            'Label':'Hit Map Grade '+RateData['HRData']['RatesString']
        }
        self.ResultData['KeyValueDictPairs']['ReadoutUniformityOverTimeGrade'] = {
            'Value':'',
            'Label':'ROC Read. Unif. Grade '+RateData['HRData']['RatesString']
        }        
        self.ResultData['KeyValueDictPairs']['ColumnReadoutUniformityOverTimeGrade'] = {
            'Value':'',
            'Label':'Column Read. Unif. Grade '+RateData['HRData']['RatesString']
        }
        self.ResultData['KeyValueDictPairs']['ColumnUniformityGrade'] = {
            'Value':'',
            'Label':'Column Uniformity Grade'
        }

        self.ResultData['KeyList'] += [
                'ROCGrade',
                'NumberOfHotPixels',
                'NumberOfNonUniformColumns',
                'NumberOfNonUniformEvents',
                'NumberOfNonUniformColumnEvents',
                'MissingHits',
                'Efficiency',
                'EfficiencyGrade',
                'HotPixelsGrade',
                'HitMapGrade',
                'ReadoutUniformityOverTimeGrade',
                'ColumnReadoutUniformityOverTimeGrade',
                'ColumnUniformityGrade',
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
            MeanEfficiency = float(self.ParentObject.ResultData['SubTestResults']['EfficiencyInterpolation'].ResultData['KeyValueDictPairs']['InterpolatedEfficiency{Rate}'.format(Rate=Rate)]['Value'])
            Grades['EfficiencyGrade'] = 1
            if MeanEfficiency < self.TestResultEnvironmentObject.GradingParameters['XRayHighRateEfficiency_max_allowed_loweff_A_Rate{RateIndex}'.format(RateIndex=RateIndex)]:
                Grades['EfficiencyGrade'] = 2
            if MeanEfficiency < self.TestResultEnvironmentObject.GradingParameters['XRayHighRateEfficiency_max_allowed_loweff_B_Rate{RateIndex}'.format(RateIndex=RateIndex)]:
                Grades['EfficiencyGrade'] = 3
            ROCGrades.append(Grades['EfficiencyGrade'])
            RateIndex += 1

            self.ResultData['HiddenData']['Efficiency_{Rate}'.format(Rate=Rate)] = MeanEfficiency
            self.ResultData['KeyValueDictPairs']['Efficiency']['Value'] = (self.ResultData['KeyValueDictPairs']['Efficiency']['Value']+'/{Value}'.format(Value=MeanEfficiency)).strip('/')
            
            self.ResultData['HiddenData']['EfficiencyGrade_{Rate}'.format(Rate=Rate)] = Grades['EfficiencyGrade']
            self.ResultData['KeyValueDictPairs']['EfficiencyGrade']['Value'] = (self.ResultData['KeyValueDictPairs']['EfficiencyGrade']['Value']+'/{Grade}'.format(Grade=GradeMapping[Grades['EfficiencyGrade']])).strip('/')


        AliveMapROOTObject = self.ParentObject.ResultData['SubTestResults']['AliveMap'].ResultData['Plot']['ROOTObject']
        
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
            ColumnReadoutUniformityROOTObject = self.ParentObject.ResultData['SubTestResults']['ColumnUniformityPerColumn'].ResultData['Plot']['ROOTObject']
            ColumnReadoutUniformityOverTimeROOTObject = self.ParentObject.ResultData['SubTestResults']['ColumnUniformityEventsPerColumn_{Rate}'.format(Rate=Rate)].ResultData['Plot']['ROOTObject']
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
            MissingHits = 0
            for col in range(0, 52):
                for row in range(0, 80):
                    PixelOk = True if AliveMapROOTObject.GetBinContent(col + 1, row + 1) == 10 and HotPixelMapROOTObject.GetBinContent(col + 1, row + 1) < 1 else False
                    if HitMapROOTObject.GetBinContent(col + 1, row + 1) < 1 and PixelOk:
                        MissingHits += 1

            Grades['HitMapGrade'] = 1
            if MissingHits >= self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_missing_xray_pixels_B']:
                Grades['HitMapGrade'] = 2
            if MissingHits >= self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_missing_xray_pixels_C']:
                Grades['HitMapGrade'] = 3
            ROCGrades.append(Grades['HitMapGrade'])

            NumberValues['MissingHits'] = MissingHits

            ### ROC Readout Uniformity Over Time Grade ###
            Grades['ReadoutUniformityOverTimeGrade'] = 1
            FirstBin = ReadoutUniformityOverTimeTestResultObject.ResultData['Plot']['ROOTObject'].GetXaxis().GetFirst()
            LastBin = ReadoutUniformityOverTimeTestResultObject.ResultData['Plot']['ROOTObject'].FindLastBinAbove(0)
            ReadoutUniformityOverTimeTestResultObject.ResultData['Plot']['ROOTObject'].GetXaxis().SetRange(1, LastBin - 1)
            ReadoutUniformityOverTimeMean = ReadoutUniformityOverTimeTestResultObject.ResultData['Plot']['ROOTObject'].Integral(FirstBin, LastBin) / (LastBin - FirstBin + 1)

            ReadoutUniformityOverTimeSigma = math.sqrt(ReadoutUniformityOverTimeMean)
            NumberValues['NumberOfNonUniformEvents'] = 0
            for Event in range(1, LastBin-1):
                EventHits = ReadoutUniformityOverTimeTestResultObject.ResultData['Plot']['ROOTObject'].GetBinContent(Event+1)
                if( abs(EventHits-ReadoutUniformityOverTimeMean) > self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_factor_readout_uniformity']
                    *ReadoutUniformityOverTimeSigma
                ):
                    NumberValues['NumberOfNonUniformEvents'] += 1
                    Grades['ReadoutUniformityOverTimeGrade'] = 3
                    #print "non uniform event: %d %d / %f"%(Event, EventHits, ReadoutUniformityOverTimeMean)
            
            ### Column Readout Uniformity Over Time Grade ###
            Grades['ColumnReadoutUniformityOverTimeGrade'] = 1
            NumberValues['NumberOfNonUniformColumnEvents'] = 0
            for Column in range(0, 52):
                ColumnReadoutUniformityHistogram = ColumnReadoutUniformityOverTimeROOTObject.ProjectionX(self.GetUniqueID(), Column + 1, Column + 1)
                NEvents = ColumnReadoutUniformityHistogram.GetNbinsX()
                FirstBin = ColumnReadoutUniformityHistogram.GetXaxis().GetFirst()
                LastBin = ColumnReadoutUniformityHistogram.FindLastBinAbove(0)
                ColumnReadoutUniformityHistogram.GetXaxis().SetRange(1, LastBin - 1)

                MeanHitsPerBin = ColumnReadoutUniformityHistogram.Integral(FirstBin, LastBin) / (LastBin - FirstBin + 1)
                ReadoutUniformityOverTimeSigma = math.sqrt(MeanHitsPerBin) # poisson

                #exclude last bin
                for Event in range(0, LastBin - 1):
                    BinHits = ColumnReadoutUniformityHistogram.GetBinContent(Event + 1)

                    if( abs(BinHits-MeanHitsPerBin) > self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_factor_readout_uniformity']
                        *ReadoutUniformityOverTimeSigma
                    ):
                        NumberValues['NumberOfNonUniformColumnEvents'] += 1
                        Grades['ColumnReadoutUniformityOverTimeGrade'] = 3

                ColumnReadoutUniformityHistogram.Delete()        

            ### Grade/Values summary for different rates ###
            for NumberKey in self.Attributes['NumberKeys']['HRData']:
                self.ResultData['HiddenData'][NumberKey+'_{Rate}'.format(Rate=Rate)] = NumberValues[NumberKey]
                self.ResultData['KeyValueDictPairs'][NumberKey]['Value'] = (self.ResultData['KeyValueDictPairs'][NumberKey]['Value']+'/{Rate}'.format(Rate=NumberValues[NumberKey])).strip('/')

            for GradeKey in self.Attributes['GradeKeys']['HRData']:
                self.ResultData['HiddenData'][GradeKey+'_{Rate}'.format(Rate=Rate)] = Grades[GradeKey]
                self.ResultData['KeyValueDictPairs'][GradeKey]['Value'] = (self.ResultData['KeyValueDictPairs'][GradeKey]['Value']+'/'+GradeMapping[Grades[GradeKey]]).strip('/')
       
        ### Column Uniformity Grade ###
        Grades['ColumnUniformityGrade'] = 1         
        NumberValues['NumberOfNonUniformColumns'] = 0
        for Column in range(self.nCols):
            ColumnHitRatio = ColumnReadoutUniformityROOTObject.GetBinContent(Column+1)
            if (ColumnHitRatio < self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_factor_dcol_uniformity_low'] 
                or ColumnHitRatio > self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_factor_dcol_uniformity_high']):
                NumberValues['NumberOfNonUniformColumns'] += 1
                Grades['ColumnUniformityGrade'] = 3
        self.ResultData['HiddenData']['NumberOfNonUniformColumns'] = NumberValues['NumberOfNonUniformColumns']
        self.ResultData['KeyValueDictPairs']['NumberOfNonUniformColumns']['Value'] = '{Value}'.format(Value=NumberValues['NumberOfNonUniformColumns'])
        self.ResultData['HiddenData']['ColumnUniformityGrade'] = Grades['ColumnUniformityGrade']
        self.ResultData['KeyValueDictPairs']['ColumnUniformityGrade']['Value'] = GradeMapping[Grades['ColumnUniformityGrade']]

        ### Pixel Alive ###
        PixelAliveROOTObject = self.ParentObject.ResultData['SubTestResults']['AliveMap'].ResultData['Plot']['ROOTObject']
        DeadPixels = 0
        InefficientPixels = 0
        for col in range(0, 52):
            for row in range(0, 80):
                if PixelAliveROOTObject.GetBinContent(col + 1, row + 1) < 10:
                    InefficientPixels += 1
                if PixelAliveROOTObject.GetBinContent(col + 1, row + 1) < 1:
                    DeadPixels += 1
        self.ResultData['HiddenData']['NumberOfDeadPixels'] = DeadPixels
        self.ResultData['HiddenData']['NumberOfInefficientPixels'] = InefficientPixels

        ROCGrades.append(Grades['ColumnUniformityGrade'])        
        
        ### Final ROC Grade ###
        self.ResultData['KeyValueDictPairs']['ROCGrade']['Value'] = GradeMapping[max(ROCGrades)]
            
            
