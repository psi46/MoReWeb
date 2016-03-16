import AbstractClasses

try:
       set
except NameError:
       from sets import Set as set

def defectsListLength(defectsList):
    if defectsList is not None:
        return "%4d"%len(defectsList)
    else:
        return 'INCOMPLETE'

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.NameSingle = 'Grading'
        self.Name = 'CMSPixel_QualificationGroup_Reception_Chips_Chip_%s_TestResult'%self.NameSingle
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Reception_ROC'
        self.chipNo = self.ParentObject.Attributes['ChipNo']
        self.ResultData['HiddenData']['DeadPixelList'] = set()
        self.ResultData['HiddenData']['MaskDefectList'] = set()
        self.ResultData['HiddenData']['IneffPixelList'] = set()
        self.ResultData['HiddenData']['AddressProblemList'] = set()
        self.ResultData['HiddenData']['DeadBumpList'] = set()
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
        if 'BB4' in self.ParentObject.ResultData['SubTestResults'] and self.ParentObject.ResultData['SubTestResults']['BB4'].ResultData['Plot']['ROOTObject']:
            self.ResultData['HiddenData']['DeadBumpList'] = self.ParentObject.ResultData['SubTestResults']['BB4'].ResultData['KeyValueDictPairs']['DeadBumps']['Value']
            self.ResultData['HiddenData']['SpecialBumpBondingTestName'] = 'BB4'
        elif 'BB2Map' in self.ParentObject.ResultData['SubTestResults'] and self.ParentObject.ResultData['SubTestResults']['BB2Map'].ResultData['Plot']['ROOTObject']:
            self.ResultData['HiddenData']['DeadBumpList'] = self.ParentObject.ResultData['SubTestResults']['BB2Map'].ResultData['KeyValueDictPairs']['MissingBumps']['Value']
            self.ResultData['HiddenData']['SpecialBumpBondingTestName'] = 'BB2'
        else:
            self.ResultData['HiddenData']['DeadBumpList'] = self.ParentObject.ResultData['SubTestResults']['BumpBondingProblems'].ResultData['KeyValueDictPairs']['DeadBumps']['Value']
            self.ResultData['HiddenData']['SpecialBumpBondingTestName'] = ''

        if len(self.ResultData['HiddenData']['SpecialBumpBondingTestName']) > 0:
            print "using special bump bonding test: %s"%self.ResultData['HiddenData']['SpecialBumpBondingTestName']

        # other pixel defects
        self.ResultData['HiddenData']['DeadPixelList'] = self.ParentObject.ResultData['SubTestResults']['PixelMap'].ResultData['KeyValueDictPairs']['DeadPixels']['Value']
        self.ResultData['HiddenData']['IneffPixelList'] = self.ParentObject.ResultData['SubTestResults']['PixelMap'].ResultData['KeyValueDictPairs']['InefficentPixels']['Value']
        self.ResultData['HiddenData']['MaskDefectList'] = self.ParentObject.ResultData['SubTestResults']['PixelMap'].ResultData['KeyValueDictPairs']['MaskDefects']['Value']
        self.ResultData['HiddenData']['Noisy1PixelList'] = self.ParentObject.ResultData['SubTestResults']['PixelMap'].ResultData['KeyValueDictPairs']['NoisyPixels']['Value'] # pixels with too many hitys in pixel alive...

        # check if some data is missing and make unique list of total pixel defects
        self.ResultData['HiddenData']['DefectsGradingComplete'] = True
        self.ResultData['HiddenData']['TotalList'] = set([])
        for IndividualDefectsList in [
            self.ResultData['HiddenData']['DeadPixelList'],
            self.ResultData['HiddenData']['IneffPixelList'],
            self.ResultData['HiddenData']['MaskDefectList'],
            self.ResultData['HiddenData']['Noisy1PixelList'],
            self.ResultData['HiddenData']['DeadBumpList'],
            self.ResultData['HiddenData']['AddressProblemList'],
        ]:
            if IndividualDefectsList is not None:
                self.ResultData['HiddenData']['TotalList'] = self.ResultData['HiddenData']['TotalList'] | IndividualDefectsList
            else:
                self.ResultData['HiddenData']['DefectsGradingComplete'] = False

        # subtract dead pixels explicitly from individual defects which do not exclude them implicitly
        if self.ResultData['HiddenData']['DeadPixelList'] is not None:
            self.ResultData['HiddenData']['AddressProblemList'] = self.ResultData['HiddenData']['AddressProblemList'] - self.ResultData['HiddenData']['DeadPixelList'] if self.ResultData['HiddenData']['AddressProblemList'] is not None else None
            self.ResultData['HiddenData']['DeadBumpList'] = self.ResultData['HiddenData']['DeadBumpList'] - self.ResultData['HiddenData']['DeadPixelList'] if self.ResultData['HiddenData']['DeadBumpList'] is not None else None
            self.ResultData['HiddenData']['MaskDefectList'] = self.ResultData['HiddenData']['MaskDefectList'] - self.ResultData['HiddenData']['DeadPixelList'] if self.ResultData['HiddenData']['MaskDefectList'] is not None else None

        # total defects grading
        PixelDefectsGradeALimit = self.TestResultEnvironmentObject.GradingParameters['defectsB']
        PixelDefectsGradeBLimit = self.TestResultEnvironmentObject.GradingParameters['defectsC']
        totalDefects = len(self.ResultData['HiddenData']['TotalList'])
        self.ResultData['HiddenData']['NDefects'] = totalDefects
        self.ResultData['HiddenData']['NDefectiveBumps'] = len(self.ResultData['HiddenData']['DeadBumpList']) if self.ResultData['HiddenData']['DeadBumpList'] is not None else 0
        self.ResultData['HiddenData']['NDeadPixels'] = len(self.ResultData['HiddenData']['DeadPixelList']) if self.ResultData['HiddenData']['DeadPixelList'] is not None else 0
        if totalDefects < PixelDefectsGradeALimit:
            pixelDefectsGrade = 1
        elif totalDefects < PixelDefectsGradeBLimit:
            pixelDefectsGrade = 2
        else:
            pixelDefectsGrade = 3

        # mask defects grading
        MaskDefectsGradeALimit = self.TestResultEnvironmentObject.GradingParameters['maskDefectsB']
        MaskDefectsGradeBLimit = self.TestResultEnvironmentObject.GradingParameters['maskDefectsC']
        maskDefects = len(self.ResultData['HiddenData']['MaskDefectList']) if self.ResultData['HiddenData']['MaskDefectList'] is not None else 0
        if pixelDefectsGrade == 1 and maskDefects >= MaskDefectsGradeALimit:
            pixelDefectsGrade = 2
        if maskDefects >= MaskDefectsGradeBLimit:
            pixelDefectsGrade = 3

        GradeMapping = {1:'A', 2:'B', 3:'C'}
        Grade = 'None'

        if not self.ResultData['HiddenData']['DefectsGradingComplete']:
            pixelDefectsGrade = 3

        try:
            Grade = GradeMapping[pixelDefectsGrade]
        except:
            pass

        print '\nChip %d Pixel Defects Grade %s'%(self.chipNo, Grade)

        print '\ttotal: %s'%defectsListLength(self.ResultData['HiddenData']['TotalList']),
        print '\tdead:  %s'%defectsListLength(self.ResultData['HiddenData']['DeadPixelList']),
        print '\tinef:  %s'%defectsListLength(self.ResultData['HiddenData']['IneffPixelList']),
        print '\tmask:  %s'%defectsListLength(self.ResultData['HiddenData']['MaskDefectList']),
        print '\taddr:  %s'%defectsListLength(self.ResultData['HiddenData']['AddressProblemList']),
        print '\tbump:  %s'%defectsListLength(self.ResultData['HiddenData']['DeadBumpList'])

        print '-'*110

        self.ResultData['KeyValueDictPairs'] = {
            'PixelDefectsGrade':{
                'Value': '%d'%pixelDefectsGrade,
                'Label': 'Pixel Defects Grade ROC'
            },
        }
        self.ResultData['KeyList'] = ['PixelDefectsGrade']

