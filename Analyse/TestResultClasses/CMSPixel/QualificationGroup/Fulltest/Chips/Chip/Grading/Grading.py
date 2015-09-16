import ROOT
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter

try:
       set
except NameError:
       from sets import Set as set
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Fulltest_Chips_Chip_Grading_TestResult'
        self.NameSingle='Grading'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'
        self.chipNo = self.ParentObject.Attributes['ChipNo']
        self.ResultData['HiddenData']['DeadPixelList'] = set()
        self.ResultData['HiddenData']['Noisy1PixelList'] = set()
        self.ResultData['HiddenData']['MaskDefectList'] = set()
        self.ResultData['HiddenData']['IneffPixelList'] = set()

        self.ResultData['HiddenData']['AddressProblemList'] = set()
        self.ResultData['HiddenData']['ThrDefectList'] = set()
        self.ResultData['HiddenData']['NoiseDefectList'] = set()
        self.ResultData['HiddenData']['GainDefectList'] = set()
        self.ResultData['HiddenData']['PedDefectList'] = set()
        self.ResultData['HiddenData']['Par1DefectList'] = set()
        self.ResultData['HiddenData']['TotalList'] = set()
        self.isDigitalROC = self.ParentObject.ParentObject.ParentObject.Attributes['isDigital']

    def GetSingleChipSubtestGrade(self, SpecialPopulateDataParameters, CurrentGrade, IncludeDefects = True):
        Value = float(self.ParentObject.ResultData['SubTestResults'][SpecialPopulateDataParameters['DataKey']].ResultData['KeyValueDictPairs'][SpecialPopulateDataParameters['DataParameterKey']]['Value'])

        nDefects = 0
        if SpecialPopulateDataParameters.has_key('DefectsKey'):
            nDefects = float(self.ParentObject.ResultData['SubTestResults'][SpecialPopulateDataParameters['DataKey']].ResultData['KeyValueDictPairs'][SpecialPopulateDataParameters['DefectsKey']]['Value'])

        if SpecialPopulateDataParameters.has_key('DataFactor'):
            Value = Value*SpecialPopulateDataParameters['DataFactor']
        if SpecialPopulateDataParameters.has_key('CalcFunction'):
            Value = SpecialPopulateDataParameters['CalcFunction'](Value, self.ParentObject.ResultData['SubTestResults'][SpecialPopulateDataParameters['DataKey']].ResultData['KeyValueDictPairs'])

        Value = float(Value)
        ChipGrade = CurrentGrade

        # roc value based grading
        if ChipGrade == 1 and Value > SpecialPopulateDataParameters['YLimitB']:
            ChipGrade = 2
        if Value > SpecialPopulateDataParameters['YLimitC']:
            ChipGrade = 3

        if IncludeDefects:
            # number of pixel defects based grading
            if ChipGrade == 1 and nDefects >= self.TestResultEnvironmentObject.GradingParameters['defectsB']:
                ChipGrade = 2
            if nDefects >= self.TestResultEnvironmentObject.GradingParameters['defectsC']:
                ChipGrade = 3

        return ChipGrade

    def PopulateResultData(self):
        ChipNo = self.ParentObject.Attributes['ChipNo']

        # get individual pixel defect lists
        self.ResultData['HiddenData']['AddressProblemList'] = self.ParentObject.ResultData['SubTestResults']['AddressDecoding'].ResultData['KeyValueDictPairs']['AddressDecodingProblems']['Value'] 
        
        # Bump Bonding Defects
        # priority: BB4 > BB2 > BB  (BB4 > BB2 is arbitrary, they should not be present at the same time)
        if self.ParentObject.ResultData['SubTestResults']['BB4'].ResultData['Plot']['ROOTObject']:
            self.ResultData['HiddenData']['DeadBumpList'] = self.ParentObject.ResultData['SubTestResults']['BB4'].ResultData['KeyValueDictPairs']['DeadBumps']['Value']
            self.ResultData['HiddenData']['SpecialBumpBondingTestName'] = 'BB4'
        elif self.ParentObject.ResultData['SubTestResults']['BB2Map'].ResultData['Plot']['ROOTObject']:
            self.ResultData['HiddenData']['DeadBumpList'] = self.ParentObject.ResultData['SubTestResults']['BB2Map'].ResultData['KeyValueDictPairs']['MissingBumps']['Value']
            self.ResultData['HiddenData']['SpecialBumpBondingTestName'] = 'BB2'
        else:
            self.ResultData['HiddenData']['DeadBumpList'] = self.ParentObject.ResultData['SubTestResults']['BumpBondingProblems'].ResultData['KeyValueDictPairs']['DeadBumps']['Value']
            self.ResultData['HiddenData']['SpecialBumpBondingTestName'] = ''


        self.ResultData['HiddenData']['DeadPixelList'] = self.ParentObject.ResultData['SubTestResults']['PixelMap'].ResultData['KeyValueDictPairs']['DeadPixels']['Value']
        self.ResultData['HiddenData']['DeadTrimbitsList'] = self.ParentObject.ResultData['SubTestResults']['TrimBitProblems'].ResultData['KeyValueDictPairs']['DeadTrimbits']['Value']
        self.ResultData['HiddenData']['GainDefectList'] = self.ParentObject.ResultData['SubTestResults']['PHCalibrationGain'].ResultData['KeyValueDictPairs']['GainDefects']['Value']
        self.ResultData['HiddenData']['IneffPixelList'] = self.ParentObject.ResultData['SubTestResults']['PixelMap'].ResultData['KeyValueDictPairs']['InefficentPixels']['Value']
        self.ResultData['HiddenData']['MaskDefectList'] = self.ParentObject.ResultData['SubTestResults']['PixelMap'].ResultData['KeyValueDictPairs']['MaskDefects']['Value']
        self.ResultData['HiddenData']['Noisy1PixelList'] = self.ParentObject.ResultData['SubTestResults']['PixelMap'].ResultData['KeyValueDictPairs']['NoisyPixels']['Value'] # pixels with too many hitys in pixel alive...
        self.ResultData['HiddenData']['NoiseDefectList'] = self.ParentObject.ResultData['SubTestResults']['SCurveWidths'].ResultData['KeyValueDictPairs']['NoiseDefects']['Value'] # pixels with too wide S-curve...
        self.ResultData['HiddenData']['Par1DefectList'] = self.ParentObject.ResultData['SubTestResults']['PHCalibrationTan'].ResultData['KeyValueDictPairs']['Par1Defects']['Value']
        self.ResultData['HiddenData']['ThrDefectList'] = self.ParentObject.ResultData['SubTestResults']['VcalThresholdTrimmed'].ResultData['KeyValueDictPairs']['TrimProblems']['Value']

        self.ResultData['HiddenData']['AddressProblemList'] = self.ResultData['HiddenData']['AddressProblemList'] - self.ResultData['HiddenData']['DeadPixelList']
        self.ResultData['HiddenData']['DeadBumpList'] = self.ResultData['HiddenData']['DeadBumpList'] - self.ResultData['HiddenData']['DeadPixelList']
        self.ResultData['HiddenData']['DeadTrimbitsList'] = self.ResultData['HiddenData']['DeadTrimbitsList'] - self.ResultData['HiddenData']['DeadPixelList']
        self.ResultData['HiddenData']['MaskDefectList'] = self.ResultData['HiddenData']['MaskDefectList'] - self.ResultData['HiddenData']['DeadPixelList']



        # make unique list of total pixel defects
        self.ResultData['HiddenData']['TotalList'] = (
            self.ResultData['HiddenData']['AddressProblemList'] |
            self.ResultData['HiddenData']['DeadBumpList'] |
            self.ResultData['HiddenData']['DeadPixelList'] |
            self.ResultData['HiddenData']['DeadTrimbitsList'] |
            self.ResultData['HiddenData']['GainDefectList'] |
            self.ResultData['HiddenData']['IneffPixelList'] |
            self.ResultData['HiddenData']['MaskDefectList'] |
            self.ResultData['HiddenData']['NoiseDefectList'] |
            self.ResultData['HiddenData']['Par1DefectList'] |
            self.ResultData['HiddenData']['ThrDefectList']
        )

        # total defects grading
        PixelDefectsGradeALimit = self.TestResultEnvironmentObject.GradingParameters['defectsB']
        PixelDefectsGradeBLimit = self.TestResultEnvironmentObject.GradingParameters['defectsC']
        totalDefects = len(self.ResultData['HiddenData']['TotalList'])
        if totalDefects < PixelDefectsGradeALimit:
            pixelDefectsGrade = 1
        elif totalDefects < PixelDefectsGradeBLimit:
            pixelDefectsGrade = 2
        else:
            pixelDefectsGrade = 3

        # mask defects grading
        MaskDefectsGradeALimit = self.TestResultEnvironmentObject.GradingParameters['maskDefectsB']
        MaskDefectsGradeBLimit = self.TestResultEnvironmentObject.GradingParameters['maskDefectsC']
        maskDefects = len(self.ResultData['HiddenData']['MaskDefectList'])
        if pixelDefectsGrade == 1 and maskDefects >= MaskDefectsGradeALimit:
            pixelDefectsGrade = 2
        if maskDefects >= MaskDefectsGradeBLimit:
            pixelDefectsGrade = 3

        GradeMapping = {1:'A', 2:'B', 3:'C'}
        Grade = 'None'
        try:
            Grade = GradeMapping[pixelDefectsGrade]
        except:
            pass

        print '\nChip %d Pixel Defects Grade %s'%(self.chipNo, Grade)

        print '\ttotal: %4d'%len(self.ResultData['HiddenData']['TotalList'])
        print '\tdead:  %4d'%len(self.ResultData['HiddenData']['DeadPixelList'])
        print '\tinef:  %4d'%len(self.ResultData['HiddenData']['IneffPixelList'])
        print '\tmask:  %4d'%len(self.ResultData['HiddenData']['MaskDefectList'])
        print '\taddr:  %4d'%len(self.ResultData['HiddenData']['AddressProblemList'])
        print '\tbump:  %4d'%len(self.ResultData['HiddenData']['DeadBumpList'])
        print '\ttrim:  %4d'%len(self.ResultData['HiddenData']['ThrDefectList'])
        print '\ttbit:  %4d'%len(self.ResultData['HiddenData']['DeadTrimbitsList'])
        print '\tnois:  %4d'%len(self.ResultData['HiddenData']['NoiseDefectList'])
        print '\tgain:  %4d'%len(self.ResultData['HiddenData']['GainDefectList'])
        print '\tpar1:  %4d'%len(self.ResultData['HiddenData']['Par1DefectList'])

        print '-'*78

        self.ResultData['KeyValueDictPairs'] = {
            'PixelDefectsGrade':{
                'Value': '%d'%pixelDefectsGrade,
                'Label': 'Pixel Defects Grade ROC'
            },
        }
        self.ResultData['KeyList'] = ['PixelDefectsGrade']

