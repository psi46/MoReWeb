import ROOT
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter
import math
import sys, traceback

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_XRayHRQualification_Chips_Chip_Grading_TestResult'
        self.NameSingle='Grading'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_XRayHRQualification_ROC'
        self.Attributes['GradeKeys'] = {
            'HREfficiency':[
            ],
            'HRData':[
                'HotPixelsGrade',
                'HitMapGrade',
                'ColumnUniformityGrade',
                'ReadoutUniformityOverTimeGrade',
                'ColumnReadoutUniformityOverTimeGrade'
            ],
            'HRSCurves':[],
            'RetrimHotPixels':[]
        }
        self.Attributes['NumberKeys'] = {
            'HREfficiency':[
                'NumberOfLowEfficiencyPixels',
            ],
            'HRData':[
                'NumberOfHotPixels',
                'NumberOfNonUniformColumns',
                'NumberOfNonUniformEvents',
                'NumberOfNonUniformColumnEvents',
                'BumpBondingDefects'
            ],
            'HRSCurves':[],
            'RetrimHotPixels':[]
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
        self.ResultData['KeyValueDictPairs']['EfficiencyFit'] = {
            'Value':'',
            'Label':'Efficiency Fit'
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
        self.ResultData['KeyValueDictPairs']['BumpBondingDefects'] = {
            'Value':'',
            'Label':'# Bump Bonding Defects '+RateData['HRData']['RatesString']
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
        self.ResultData['KeyValueDictPairs']['NoiseGrade'] = {
            'Value':'',
            'Label':'Noise Grade'
        }        
        self.ResultData['KeyValueDictPairs']['PixelDefects'] = {
            'Value':'',
            'Label':'Total Number of Pixel Defects',
        }

        self.ResultData['KeyList'] += [
                'ROCGrade',
                'NumberOfHotPixels',
                'NumberOfNonUniformColumns',
                'NumberOfNonUniformEvents',
                'NumberOfNonUniformColumnEvents',
                'BumpBondingDefects',
                'Efficiency',
                'EfficiencyFit',
                'EfficiencyGrade',
                'HotPixelsGrade',
                'HitMapGrade',
                'ReadoutUniformityOverTimeGrade',
                'ColumnReadoutUniformityOverTimeGrade',
                'ColumnUniformityGrade',
                'NoiseGrade'
            ]
        for Rate in RateData['HREfficiency']['Rates']:
            self.ResultData['HiddenData']['ListOfLowEfficiencyPixels_{Rate}'.format(Rate=Rate)] = []
        for Rate in RateData['HRData']['Rates']:
            self.ResultData['HiddenData']['ListOfHotPixels_{Rate}'.format(Rate=Rate)] = []

            
        for RateType in RateTypes:
            for Rate in RateData[RateType]['Rates']:
                for NumberKey in self.Attributes['NumberKeys'][RateType]:
                    self.ResultData['HiddenData'][NumberKey+'_{Rate}'.format(Rate=Rate)] = {'Value': '-1'}
                for GradeKey in self.Attributes['GradeKeys'][RateType]:
                    self.ResultData['HiddenData'][GradeKey+'_{Rate}'.format(Rate=Rate)] = {'Value': '-1'}

        for Rate in self.ParentObject.ParentObject.ParentObject.Attributes['InterpolatedEfficiencyRates']:
            self.ResultData['HiddenData']['Efficiency_{Rate}'.format(Rate=Rate)] = {
                'Label': 'Efficiency at %s MHz/cm2'%Rate,
                'Value': '',
                'Unit': '%',
            }
            self.ResultData['HiddenData']['EfficiencyGrade_{Rate}'.format(Rate=Rate)] = {
                'Label': 'Efficiency Grade at %s MHz/cm2'%Rate,
                'Value': '',
                'Unit': '',
            }

            self.ResultData['HiddenData']['NumberOfNonUniformColumns'] = {'Value': '-1'}
            self.ResultData['HiddenData']['ColumnUniformityGrade'] = {'Value': 'None'}
            
	
    def PopulateResultData(self):
        GradeMapping = {
            -1:'N/A',
            1: 'A',
            2: 'B',
            3: 'C'
        }
        ROCGrades = []
        ReadoutProblemsDetected = False
        ChipNo = self.ParentObject.Attributes['ChipNo']
        
        # efficiency grading
        NumberValues = {}
        for NumberKey in self.Attributes['NumberKeys']['HREfficiency']:
            NumberValues[NumberKey] = 0

        Grades = {}
        for GradeKey in self.Attributes['GradeKeys']['HREfficiency']:
            Grades[GradeKey] = -1

        OmitGradesInFinalGrading = self.TestResultEnvironmentObject.XRayHRQualificationConfiguration['OmitGradesInFinalGrading']

        RateIndex = 1
        for Rate in self.ParentObject.ParentObject.ParentObject.Attributes['InterpolatedEfficiencyRates']:
            MeanEfficiency = float(self.ParentObject.ResultData['SubTestResults']['EfficiencyInterpolation'].ResultData['KeyValueDictPairs']['InterpolatedEfficiency{Rate}'.format(Rate=Rate)]['Value'])
            Grades['EfficiencyGrade'] = 1
            if MeanEfficiency < self.TestResultEnvironmentObject.GradingParameters['XRayHighRateEfficiency_max_allowed_loweff_A_Rate{RateIndex}'.format(RateIndex=RateIndex)]:
                Grades['EfficiencyGrade'] = 2
            if MeanEfficiency < self.TestResultEnvironmentObject.GradingParameters['XRayHighRateEfficiency_max_allowed_loweff_B_Rate{RateIndex}'.format(RateIndex=RateIndex)]:
                Grades['EfficiencyGrade'] = 3

            if not 'EfficiencyGrade' in OmitGradesInFinalGrading and not 'EfficiencyGrade_{Rate}'.format(Rate=Rate) in OmitGradesInFinalGrading:
                ROCGrades.append(Grades['EfficiencyGrade'])

            RateIndex += 1

            self.ResultData['HiddenData']['Efficiency_{Rate}'.format(Rate=Rate)] = MeanEfficiency
            self.ResultData['KeyValueDictPairs']['Efficiency']['Value'] = (self.ResultData['KeyValueDictPairs']['Efficiency']['Value']+'/{Value}'.format(Value=MeanEfficiency)).strip('/')
            
            self.ResultData['HiddenData']['EfficiencyGrade_{Rate}'.format(Rate=Rate)] = Grades['EfficiencyGrade']

            Grade = '{Grade}'.format(Grade=GradeMapping[Grades['EfficiencyGrade']])
            if 'EfficiencyGrade' in OmitGradesInFinalGrading or 'EfficiencyGrade_{Rate}'.format(Rate=Rate) in OmitGradesInFinalGrading:
                Grade = '('+Grade+')'
            self.ResultData['KeyValueDictPairs']['EfficiencyGrade']['Value'] = (self.ResultData['KeyValueDictPairs']['EfficiencyGrade']['Value']+'/'+Grade).strip('/')

        try:
            EfficiencyFit = "chi2/ndf: {chi2}, # points: {n}".format(chi2=self.ParentObject.ResultData['SubTestResults']['EfficiencyInterpolation'].ResultData['KeyValueDictPairs']['Chi2NDF']['Value'], n=self.ParentObject.ResultData['SubTestResults']['EfficiencyInterpolation'].ResultData['KeyValueDictPairs']['NumberFitPoints']['Value'])
        except:
            EfficiencyFit = "fit failed"
        self.ResultData['KeyValueDictPairs']['EfficiencyFit']['Value'] = EfficiencyFit

        AliveMapROOTObject = self.ParentObject.ResultData['SubTestResults']['AliveMap'].ResultData['Plot']['ROOTObject']
       
        BumpBondingDefectsList = []
        NoiseDefectsList = []
        HotPixelDefectsList = []

        # hitmap and uniformity grading
        ColumnReadoutUniformityROOTObject = None
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
                    PixelIsHotPixel = HotPixelMapROOTObject.GetBinContent(Column+1, Row+1) if HotPixelMapROOTObject else False
                    if PixelIsHotPixel > 0:
                        NumberValues['NumberOfHotPixels'] += 1
                        self.ResultData['HiddenData']['ListOfHotPixels_{Rate}'.format(Rate=Rate)].append((ChipNo, Column, Row))
            HotPixelDefectsList.append(NumberValues['NumberOfHotPixels'])

            ### Hot Pixels Grade ###
            Grades['HotPixelsGrade'] = 1
            if NumberValues['NumberOfHotPixels'] > self.TestResultEnvironmentObject.GradingParameters['XRayHighRateHotPixels_max_allowed_hot']:
                Grades['HotPixelsGrade'] = 3
            
            ### Hit Map Grade ###
            BumpBondingDefects = int(self.ParentObject.ResultData['SubTestResults']['BumpBondingDefects_{Rate}'.format(Rate=Rate)].ResultData['KeyValueDictPairs']['NumberOfDefectivePixels']['Value'])

            Grades['HitMapGrade'] = 1
            if BumpBondingDefects >= self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_missing_xray_pixels_B']:
                Grades['HitMapGrade'] = 2
            if BumpBondingDefects >= self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_missing_xray_pixels_C']:
                Grades['HitMapGrade'] = 3

            if not 'HitMapGrade' in OmitGradesInFinalGrading and not 'HitMapGrade_{Rate}'.format(Rate=Rate) in OmitGradesInFinalGrading:
                ROCGrades.append(Grades['HitMapGrade'])

            self.ResultData['HiddenData']['BumpBondingDefects_{Rate}'.format(Rate=Rate)] = BumpBondingDefects
            BumpBondingDefectsList.append(BumpBondingDefects)
            NumberValues['BumpBondingDefects'] = BumpBondingDefects

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
                    ReadoutProblemsDetected = True
                    #print "non uniform event: %d %d / %f"%(Event, EventHits, ReadoutUniformityOverTimeMean)
            
            if not 'ReadoutUniformityOverTimeGrade' in OmitGradesInFinalGrading and not 'ReadoutUniformityOverTimeGrade_{Rate}'.format(Rate=Rate) in OmitGradesInFinalGrading:
                ROCGrades.append(Grades['ReadoutUniformityOverTimeGrade'])

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
                        ReadoutProblemsDetected = True

                ColumnReadoutUniformityHistogram.Delete()

            if not 'ColumnReadoutUniformityOverTimeGrade' in OmitGradesInFinalGrading and not 'ColumnReadoutUniformityOverTimeGrade_{Rate}'.format(Rate=Rate) in OmitGradesInFinalGrading:
                ROCGrades.append(Grades['ColumnReadoutUniformityOverTimeGrade'])

            ### Grade/Values summary for different rates ###
            for NumberKey in self.Attributes['NumberKeys']['HRData']:
                self.ResultData['HiddenData'][NumberKey+'_{Rate}'.format(Rate=Rate)] = {'Value': NumberValues[NumberKey]}
                self.ResultData['KeyValueDictPairs'][NumberKey]['Value'] = (self.ResultData['KeyValueDictPairs'][NumberKey]['Value']+'/{Rate}'.format(Rate=NumberValues[NumberKey])).strip('/')

            for GradeKey in self.Attributes['GradeKeys']['HRData']:
                self.ResultData['HiddenData'][GradeKey+'_{Rate}'.format(Rate=Rate)] = Grades[GradeKey]
                if not GradeKey in OmitGradesInFinalGrading and not GradeKey+'_{Rate}'.format(Rate=Rate) in OmitGradesInFinalGrading:
                    self.ResultData['KeyValueDictPairs'][GradeKey]['Value'] = (self.ResultData['KeyValueDictPairs'][GradeKey]['Value']+'/'+GradeMapping[Grades[GradeKey]]).strip('/')
                else:
                    self.ResultData['KeyValueDictPairs'][GradeKey]['Value'] = (self.ResultData['KeyValueDictPairs'][GradeKey]['Value']+'/('+GradeMapping[Grades[GradeKey]]+')').strip('/')

        ### Column Uniformity Grade ###
        Grades['ColumnUniformityGrade'] = 1         
        NumberValues['NumberOfNonUniformColumns'] = 0
        if ColumnReadoutUniformityROOTObject:
            for Column in range(self.nCols):
                ColumnHitRatio = ColumnReadoutUniformityROOTObject.GetBinContent(Column+1)
                if (ColumnHitRatio < self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_factor_dcol_uniformity_low'] 
                    or ColumnHitRatio > self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_factor_dcol_uniformity_high']):
                    NumberValues['NumberOfNonUniformColumns'] += 1
                    Grades['ColumnUniformityGrade'] = 3
            self.ResultData['HiddenData']['NumberOfNonUniformColumns']['Value'] = NumberValues['NumberOfNonUniformColumns']
            self.ResultData['KeyValueDictPairs']['NumberOfNonUniformColumns']['Value'] = '{Value}'.format(Value=NumberValues['NumberOfNonUniformColumns'])
            self.ResultData['HiddenData']['ColumnUniformityGrade']['Value'] = Grades['ColumnUniformityGrade']
            self.ResultData['KeyValueDictPairs']['ColumnUniformityGrade']['Value'] = GradeMapping[Grades['ColumnUniformityGrade']]
        else:
            # Start red color
            sys.stdout.write("\x1b[31m")
            sys.stdout.flush()
            print "X-ray test incomplete!!! Column uniformity tests needs at least HRData test for two different hit rates!"
            # Print traceback
            exc_type, exc_obj, exc_tb = sys.exc_info()
            traceback.print_exception(exc_type, exc_obj, exc_tb)
            # Reset color
            sys.stdout.write("\x1b[0m")
            sys.stdout.flush()
            self.ResultData['HiddenData']['MissingTests'] = 1

        if not 'ColumnUniformityGrade' in OmitGradesInFinalGrading:
            ROCGrades.append(Grades['ColumnUniformityGrade'])

        ### Noise Grading ###
        Grades['NoiseGrade'] = 1 
        for Rate in self.ParentObject.ParentObject.ParentObject.Attributes['Rates']['HRSCurves']:
            NoiseTestResultObject = self.ParentObject.ResultData['SubTestResults']['SCurveWidths_{Rate}'.format(Rate=Rate)]
            Noise = float(NoiseTestResultObject.ResultData['KeyValueDictPairs']['mu']['Value'])
            self.ResultData['HiddenData']['Noise_{Rate}'.format(Rate=Rate)] = Noise

            if Grades['NoiseGrade'] < 2 and Noise > self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_SCurve_Noise_Threshold_B']:
                Grades['NoiseGrade'] = 2

            if Grades['NoiseGrade'] < 3 and Noise > self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_SCurve_Noise_Threshold_C']:
                Grades['NoiseGrade'] = 3
                print "Grade noise to C: %f"%Noise

            #NoisyPixels = int(NoiseTestResultObject.ResultData['HiddenData']['NumberOfNoisyPixels']['Value'])
            #NoiseDefectsList.append(NoisyPixels)
        
        if not 'NoiseGrade' in OmitGradesInFinalGrading and not 'NoiseGrade_{Rate}'.format(Rate=Rate) in OmitGradesInFinalGrading:   
            ROCGrades.append(Grades['NoiseGrade'])

        self.ResultData['KeyValueDictPairs']['NoiseGrade']['Value'] = GradeMapping[Grades['NoiseGrade']]

        ### Pixel Alive ###
        PixelAliveROOTObject = self.ParentObject.ResultData['SubTestResults']['AliveMap'].ResultData['Plot']['ROOTObject']
        DeadPixels = 0
        InefficientPixels = 0
        if PixelAliveROOTObject:
            for col in range(0, 52):
                for row in range(0, 80):
                    if PixelAliveROOTObject.GetBinContent(col + 1, row + 1) < 10:
                        InefficientPixels += 1
                    if PixelAliveROOTObject.GetBinContent(col + 1, row + 1) < 1:
                        DeadPixels += 1
        self.ResultData['HiddenData']['NumberOfDeadPixels'] = DeadPixels
        self.ResultData['HiddenData']['NumberOfInefficientPixels'] = InefficientPixels


        ### Total Pixel Defects Grading ###
        try:
            NoiseRateGrading = max(self.ParentObject.ParentObject.ParentObject.Attributes['Rates']['HRSCurves'])
            BumpBondingRateGrading = max(self.ParentObject.ParentObject.ParentObject.Attributes['Rates']['HRData'])
            HotPixelRateGrading = max(self.ParentObject.ParentObject.ParentObject.Attributes['Rates']['HRData'])

            NoisePixelsList = self.ParentObject.ResultData['SubTestResults']['SCurveWidths_{Rate}'.format(Rate=NoiseRateGrading)].ResultData['HiddenData']['ListOfNoisyPixels']['Value']
            BumpBondingDefectPixelsList = self.ParentObject.ResultData['SubTestResults']['BumpBondingDefects_{Rate}'.format(Rate=BumpBondingRateGrading)].ResultData['HiddenData']['ListOfDefectivePixels']['Value']
            HotPixelsList = self.ParentObject.ResultData['SubTestResults']['HotPixelMap_{Rate}'.format(Rate=HotPixelRateGrading)].ResultData['HiddenData']['ListOfHotPixels']['Value']
        except:
            NoisePixelsList = set()
            BumpBondingDefectPixelsList = set()
            HotPixelsList = set()
            self.ResultData['HiddenData']['MissingTests'] = 1

            # Start red color
            sys.stdout.write("\x1b[31m")
            sys.stdout.flush()
            print "X-ray test incomplete!!!"
            # Print traceback
            exc_type, exc_obj, exc_tb = sys.exc_info()
            traceback.print_exception(exc_type, exc_obj, exc_tb)
            # Reset color
            sys.stdout.write("\x1b[0m")
            sys.stdout.flush()


        TotalPixelDefectsList = BumpBondingDefectPixelsList | NoisePixelsList | HotPixelsList
        TotalPixelDefects = len(TotalPixelDefectsList)

        self.ResultData['HiddenData']['BumpBondingDefectsList'] = {
            'Label': 'Bump Bonding Defects list',
            'Value': BumpBondingDefectPixelsList,
        }
        self.ResultData['HiddenData']['HotPixelDefectsList'] = {
            'Label': 'HotPixelDefectsList',
            'Value': HotPixelsList,
        }
        self.ResultData['HiddenData']['NoisePixelsList'] = {
            'Label': 'NoisePixelsList',
            'Value': NoisePixelsList,
        }
        self.ResultData['HiddenData']['TotalPixelDefectsList'] = {
            'Label': 'TotalPixelDefectsList',
            'Value': TotalPixelDefectsList,
        }
        self.ResultData['HiddenData']['BumpBondingDefects'] = {
            'Label': 'Bump Bonding Defects',
            'Value': len(BumpBondingDefectPixelsList),
        }
        self.ResultData['HiddenData']['HotPixelDefects'] = {
            'Label': 'Hot Pixels',
            'Value': len(HotPixelsList),
        }
        self.ResultData['HiddenData']['NoiseDefects'] = {
            'Label': 'Noisy Pixels which exceed noise_thr_C=%d'%self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_SCurve_Noise_Threshold_C'],
            'Value': len(NoisePixelsList),
        }        
        self.ResultData['HiddenData']['PixelDefects'] = {
            'Label': 'Total Pixel Defects',
            'Value': TotalPixelDefects,
        }
        self.ResultData['KeyValueDictPairs']['PixelDefects']['Value'] = TotalPixelDefects

        ### total pixel defects grading ###
        Grades['PixelDefectsGrade'] = 1
        if TotalPixelDefects >= self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_pixel_defects_B']:
            Grades['PixelDefectsGrade'] = 2
        if TotalPixelDefects >= self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_pixel_defects_C']:
            Grades['PixelDefectsGrade'] = 3
        if not 'PixelDefectsGrade' in OmitGradesInFinalGrading:   
            ROCGrades.append(Grades['PixelDefectsGrade'])

        ### Final ROC Grade ###
        self.ResultData['KeyValueDictPairs']['ROCGrade']['Value'] = GradeMapping[max(ROCGrades)]

        GradeFormatted = GradeMapping[max(ROCGrades)]
        try:
            InterpolatedEfficiency120 = self.ParentObject.ResultData['SubTestResults']['EfficiencyInterpolation'].ResultData['HiddenData']['InterpolatedEfficiency120']['Value']
            EfficiencyError120 = self.ParentObject.ResultData['SubTestResults']['EfficiencyInterpolation'].ResultData['KeyValueDictPairs']['InterpolatedEfficiency120Error']['Value']
        except:
            InterpolatedEfficiency120 = '-'
            EfficiencyError120 = '?'

        print ' ROC {ROC:2.0f}: Grade {Grade}'.format(ROC=self.ParentObject.Attributes['ChipNo'], Grade=GradeFormatted)
        print '         Pixel Defects:              {Defects}'.format(Defects=TotalPixelDefects)
        print '         BumpBonding Defects:        {Defects}'.format(Defects=len(BumpBondingDefectPixelsList))
        print '         Efficiency at 120 MHz/cm2:  {Eff} +/- {EffErr}'.format(Eff=InterpolatedEfficiency120, EffErr=EfficiencyError120)
        try:
            FitChi2 = float(self.ParentObject.ResultData['SubTestResults']['EfficiencyInterpolation'].ResultData['KeyValueDictPairs']['Chi2NDF']['Value'])
            if FitChi2 > 5:
                print '         \x1b[31mEfficiency fit chi2/ndf is high! chi2/ndf = %f\x1b[0m fit probably failed!'%FitChi2
        except:
            pass
        if int(NumberValues['NumberOfNonUniformColumns']) > 0:
            print '         \x1b[31mNumber of non uniform coulmns: %d'%int(NumberValues['NumberOfNonUniformColumns'])
        if int(NumberValues['NumberOfNonUniformColumnEvents']) > 0:
            print '         \x1b[31mNumber of non uniform events in a column: %d'%int(NumberValues['NumberOfNonUniformColumnEvents'])
        if ReadoutProblemsDetected:
            print '         \x1b[31mProblems in readout uniformity detected!\x1b[0m check for hot pixels!'


        print '-'*78
