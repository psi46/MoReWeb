# -*- coding: utf-8 -*-
import AbstractClasses


class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_Fulltest_Grading_TestResult'
        self.NameSingle = 'Grading'
        self.Title = 'Grading'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
        self.ResultData['KeyValueDictPairs']['SpecialDefects'] = {'Label': 'Defects', 'Value': ''}

    def getNumberOfRocsWithGrade(self, Grade, GradeList):
        l = [i for i in GradeList if i == Grade]
        return len(l)

    def PopulateResultData(self):
        SubGradings = {}
        ModuleGrade = 1
        GradeMapping = {
            1: 'A',
            2: 'B',
            3: 'C'
        }
        self.ResultData['HiddenData']['SpecialDefects'] = []
        PixelDefectsRocsA = 0
        PixelDefectsRocsB = 0
        PixelDefectsRocsC = 0
        chipResults = self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResultDictList']
        SubGrading = []

        # Grading

        # Chip Grading
        for i in chipResults:

            ROCSummaryResult = i['TestResultObject'].ResultData['SubTestResults']['Summary']
            TotalPixelDefectsROC = int(ROCSummaryResult.ResultData['KeyValueDictPairs']['Total']['Value'])

            if TotalPixelDefectsROC >= self.TestResultEnvironmentObject.GradingParameters['defectsC']:
                PixelDefectsRocsC += 1
            elif TotalPixelDefectsROC >= self.TestResultEnvironmentObject.GradingParameters['defectsB']:
                PixelDefectsRocsB += 1
            else:
                PixelDefectsRocsA += 1
            SubGrading.append(TotalPixelDefectsROC)

        SubGradings['PixelDefects'] = SubGrading

        # performance parameters grading
        for i in ['Noise', 'VcalThresholdWidth', 'RelativeGainWidth', 'PedestalSpread', 'Parameter1']:
            if not self.ParentObject.ResultData['SubTestResults'].has_key(i):
                continue
            TestResultObject = self.ParentObject.ResultData['SubTestResults'][i]
            SubGrading = []
            ChipResults = self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResultDictList']
            for j in ChipResults:
                try:
                    ChipGradingTestResultObject = j['TestResultObject'].ResultData['SubTestResults']['Grading']

                    # Grading
                    ChipGrade = ChipGradingTestResultObject.GetSingleChipSubtestGrade(
                        TestResultObject.Attributes['SpecialPopulateDataParameters'], 1)
                    SubGrading.append('%d' % ChipGrade)

                    ChipGradeMean = ChipGradingTestResultObject.GetSingleChipSubtestGrade(
                        TestResultObject.Attributes['SpecialPopulateDataParameters'], 1, False)
                    self.ResultData['HiddenData']['SubGrading_%s_Mean_C%d'%(i, j['TestResultObject'].Attributes["ChipNo"])] = {'Label': 'Subgrade', 'Value': ChipGradeMean}

                    ModuleGrade = ChipGradingTestResultObject.GetSingleChipSubtestGrade(
                        TestResultObject.Attributes['SpecialPopulateDataParameters'], ModuleGrade)
                except:
                    SubGrading.append('C')

            if self.verbose:
                print '%s: %s'%(i,SubGrading)
            SubGradings[i] = SubGrading

        # IV Grading
        IVGrade = 0
        if self.ParentObject.ResultData['SubTestResults'].has_key('IVCurve'):
            IVGrade = 1
            IVTestResult = self.ParentObject.ResultData['SubTestResults']['IVCurve']
            CurrentAtVoltage150V = float(IVTestResult.ResultData['KeyValueDictPairs']['CurrentAtVoltage150V']['Value'])
            CurrentVariation = float(IVTestResult.ResultData['KeyValueDictPairs']['Variation']['Value'])

            # current
            #    grading is done with the measured value at +17 and -20
            if IVGrade == 1 and CurrentAtVoltage150V > self.TestResultEnvironmentObject.GradingParameters['currentB']:
                IVGrade = 2
            if CurrentAtVoltage150V > self.TestResultEnvironmentObject.GradingParameters['currentC']:
                IVGrade = 3

            # slope
            #    grading is only done with the measured value at +17
            if self.ParentObject.Attributes['TestType'].startswith('p17_'):
                if IVGrade == 1 and CurrentVariation > self.TestResultEnvironmentObject.GradingParameters['slopeivB']:
                    IVGrade = 2
                if CurrentVariation > self.TestResultEnvironmentObject.GradingParameters['slopeivC']:
                    IVGrade = 3

            # ratio +17/-20
            #    grade on ratio of measured current I(+17C)/I(-20C)
            #    (this value is stored in the fulltest at -20C)
            if 'CurrentRatio150V' in IVTestResult.ResultData['KeyValueDictPairs']:
                RatioP17M20 = float(IVTestResult.ResultData['KeyValueDictPairs']['CurrentRatio150V']['Value'])

                # only grade on ratio if I(-20C) could be correctly measured
                if RatioP17M20 > 0:
                    RatioB = float(self.TestResultEnvironmentObject.GradingParameters['leakageCurrentRatioB'])
                    RatioC = float(self.TestResultEnvironmentObject.GradingParameters['leakageCurrentRatioC'])

                    if (RatioP17M20 < RatioC):
                        IVGrade = 3
                    elif (RatioP17M20 < RatioB) and IVGrade == 1:
                        IVGrade = 2
                else:
                    print "#"*80,"\nWARNING: could not calculate I(+17)/I(-20) ratio, no grading on ratio is done!\n","#"*80
        else:
            pass

        # add pixel defects grading to final grade
        if ModuleGrade == 1 and PixelDefectsRocsB > 0:
            ModuleGrade = 2
        if PixelDefectsRocsC > 0:
            ModuleGrade = 3

        # HDI ground resistance
        if self.ParentObject.ResultData['SubTestResults']['IanaLoss'].ResultData['HiddenData']['IanaLossProblems']:
            print "#"*80,"\nWARNING: module seems to have HDI ground resistance problem!\n","#"*80
            self.ResultData['HiddenData']['SpecialDefects'].append('HDI_RESISTANCE')
            ModuleGrade = 3

        # ROCs not programmable
        try:
            NROCsNotProgrammable = int(self.ParentObject.ResultData['SubTestResults']['IanaLoss'].ResultData['KeyValueDictPairs']['NROCsNotProgrammable']['Value'])
        except:
            # if no pretest ahs been done
            NROCsNotProgrammable = 0
        if NROCsNotProgrammable > 0:
            print "#"*80,"\nWARNING: some ROCs are not programmable!\n","#"*80
            self.ResultData['HiddenData']['SpecialDefects'].append('NOT_PROGRAMMABLE')
            ModuleGrade = 3

        # missing subtest results
        MissingSubtests = False
        nChips = len(self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResultDictList'])
        try:
            nChipsExpected = self.ParentObject.Attributes['NumberOfChips']
        except:
            nChipsExpected = 16

        if nChips != nChipsExpected:
            print "nChips: %d != %d (expected)"%(nChips, nChipsExpected)
            MissingSubtests = True
            ModuleGrade = 3

        if nChips < 1:
            print "Found nChips < 1 => Grade C"
            MissingSubtests = True
            ModuleGrade = 3


        ChipResults = self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResultDictList']
        for j in ChipResults:
            ChipGradingTestResultObject = j['TestResultObject'].ResultData['SubTestResults']['Grading']
            if not ChipGradingTestResultObject.ResultData['HiddenData']['DefectsGradingComplete']:
                MissingSubtests = True
                ModuleGrade = 3

        # special defects from 'defects.txt' => grade C
        SpecialDefectsList = []
        try:
            if self.ParentObject.ResultData['SubTestResults']['IanaLoss'].ResultData['HiddenData']['IanaLossProblems']:
                SpecialDefectsList.append('HDI')
        except:
            pass

        try:
            UserSpecifiedDefects = self.check_for_defects()
            SpecialDefectsList += UserSpecifiedDefects
        except:
            print "checking for user specified defect information in defects.txt failed!"
            pass

        SpecialDefectsList = list(set(SpecialDefectsList))
        if len(SpecialDefectsList) > 0:
            ModuleGrade = 3
            SpecialDefects = ", ".join(SpecialDefectsList)
            self.ResultData['HiddenData']['SpecialDefects'] = SpecialDefects

        # electrical grade = ModuleGrade before IV
        ElectricalGrade = ModuleGrade

        # combine with IV grade
        if IVGrade > ModuleGrade:
            ModuleGrade = IVGrade

        #if grade was manually specified, apply it
        GradeComment = ''
        ManualGrade = self.check_for_manualGrade()
        if ManualGrade != '':
            if GradeMapping[ModuleGrade] != GradeMapping[int(ManualGrade)]:
                GradeComment = "Grade manually changed from "+str(GradeMapping[ModuleGrade])+" to "+str(GradeMapping[int(ManualGrade)])
                print GradeComment
            ModuleGrade =int(ManualGrade)

        print 'Fulltest Summary:'
        if MissingSubtests:
            print "\x1b[31mMISSING TESTS!\x1b[0m"
        print " %s: %s"%('Grade'.ljust(23), GradeMapping[ModuleGrade] if ModuleGrade in GradeMapping else 'None')
        print " SubGradings:"
        print "  %s: %s"%('Electrical'.ljust(22), GradeMapping[ElectricalGrade] if ElectricalGrade in GradeMapping else 'None')
        print "  %s: %s"%('IV'.ljust(22), GradeMapping[IVGrade] if IVGrade in GradeMapping else 'None')
        if ManualGrade != '':
            print "  %s: %s"%('Manual'.ljust(22), GradeMapping[int(ManualGrade)] if int(ManualGrade) in GradeMapping else 'None')

        for i in SubGradings:
            print '  %s: %s/%s/%s' % (
                i.ljust(22), self.getNumberOfRocsWithGrade('1', SubGradings[i]),
                self.getNumberOfRocsWithGrade('2', SubGradings[i]),
                self.getNumberOfRocsWithGrade('3', SubGradings[i]))

        self.ResultData['KeyValueDictPairs'] = {
            'Module': {
                'Value': self.ParentObject.Attributes['ModuleID'],
                'Label': 'Module'
            },
            'ModuleGrade': {
                'Value': '{0:1.0f}'.format(ModuleGrade),
                'Label': 'Grade'
            },
            'ElectricalGrade': {
                'Value': '{0:1.0f}'.format(ElectricalGrade),
                'Label': 'Electrical Grade'
            },
            'IVGrade': {
                'Value': '{0:1.0f}'.format(IVGrade),
                'Label': 'IV Grade'
            },
            'PixelDefectsRocsA': {
                'Value': '{0:1.0f}'.format(PixelDefectsRocsA),
                'Label': 'ROCs < 1% defects'
            },
            'PixelDefectsRocsB': {
                'Value': '{0:1.0f}'.format(PixelDefectsRocsB),
                'Label': 'ROCs > 1% defects'
            },
            'PixelDefectsRocsC': {
                'Value': '{0:1.0f}'.format(PixelDefectsRocsC),
                'Label': 'ROCs < 4% defects'
            },
            'nPixelDefectsGradeA': {
                'Value': '{0:1.0f}'.format(PixelDefectsRocsA),
                'Label': 'ROCs with Grade A'
            },
            'nPixelDefectsGradeB': {
                'Value': '{0:1.0f}'.format(PixelDefectsRocsB),
                'Label': 'ROCs with Grade B'
            },
            'nPixelDefectsGradeC': {
                'Value': '{0:1.0f}'.format(PixelDefectsRocsC),
                'Label': 'ROCs with Grade C'
            },
            'GradeComment': {
                'Value': GradeComment,
                'Label': 'Grade comment'
            },
            
        }
        self.ResultData['HiddenData']['SubGradings'] = SubGradings
        self.ResultData['HiddenData']['MissingSubtests'] = {'Label': 'Missing Subtests', 'Value': '1' if MissingSubtests else '0'}
        self.ResultData['KeyList'] = ['Module', 'ModuleGrade', 'PixelDefectsRocsB']

        if ManualGrade != '':
            self.ResultData['KeyValueDictPairs']['ManualGrade'] = {'Label': 'Manual grade', 'Value': str(int(ManualGrade))}
            self.ResultData['KeyList'].append('ManualGrade')

        # needed in summary1
        if self.verbose:
            print 'SubGradings of ROCs:'
        for i in SubGradings:
            for Grade in GradeMapping:
                key = i + 'Grade' + GradeMapping[Grade] + "ROCs"
                try:
                    nRocs = self.getNumberOfRocsWithGrade('%d' % Grade, SubGradings[i])
                except:
                    nRocs = -1
                entry = {
                    'Value': nRocs,
                    'Label': '%s Grade %s ROCs' % (i, GradeMapping[Grade])
                }
                if self.verbose:
                    print key, entry
                self.ResultData['KeyValueDictPairs'][key] = entry



