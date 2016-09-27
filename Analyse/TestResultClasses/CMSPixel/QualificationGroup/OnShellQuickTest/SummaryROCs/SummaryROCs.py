# -*- coding: utf-8 -*-
import AbstractClasses
import os
import sys
import traceback

from AbstractClasses.Helper.GlobalDatabaseQuery import GlobalDatabaseQuery

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.NameSingle = 'SummaryROCs'
        self.Name = 'CMSPixel_QualificationGroup_OnShellQuickTest_%s_TestResult'%self.NameSingle
        self.Title = 'Roc Summary'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'


    def GradeColoredValue(self, value, grade, center=False):
        GradeAHTMLTemplate = "<div style='%s'>%s</div>"
        GradeBHTMLTemplate = "<div style='color:#f70;font-weight:bold;%s'>%s</div>"
        GradeCHTMLTemplate = "<div style='color:red;font-weight:bold;%s'>%s</div>"

        if center:
            Style = 'text-align:center;'
        else:
            Style = ''

        if grade == 1:
            return GradeAHTMLTemplate%(Style,value)
        elif grade == 2:
            return GradeBHTMLTemplate%(Style,value)
        elif grade == 3:
            return GradeCHTMLTemplate%(Style,value)
        else:
            return value

    def GradeColoredDefectsValue(self, value):
        if value == '#':
            return self.GradeColoredValue(value, 3)
        try:
            limitB = self.TestResultEnvironmentObject.GradingParameters['defectsB']
            limitC = self.TestResultEnvironmentObject.GradingParameters['defectsC']
            if int(value) >= limitC:
                return self.GradeColoredValue(value, 3)
            elif int(value) >= limitB:
                return self.GradeColoredValue(value, 2)
            else:
                return self.GradeColoredValue(value, 1)
        except:
            return self.GradeColoredValue(value, 3)

    def LoadValuesFromFile(self, FileName, ValueType = ''):
        ValuesFileName = self.RawTestSessionDataPath + '/' + FileName
        if os.path.isfile(ValuesFileName):
            with open(ValuesFileName, 'r') as ValuesFile:
                ValuesLines = ValuesFile.readlines()
            ValuesLines = [x.strip().replace('\n', '') for x in ValuesLines if len(x.strip()) > 0]
            try:
                if ValueType == 'int':
                    ValuesLines = [int(float(x)) for x in ValuesLines]
                elif ValueType == 'float':
                    ValuesLines = [float(x) for x in ValuesLines]
            except:
                pass
            return ValuesLines
        else:
            return []


    def PopulateResultData(self):

        HeaderRow = ['ROC', 'Grade', 'Defects', 'Dead', 'Dead (R)', 'Dead (FQ)', 'Bump', 'Bump (R)', 'Bump (FQ)', 'Inefficient', 'ΔaliveHV', 'BB Vthrcomp', 'BB Vana', 'Vana', 'Iana', 'ΔIana', 'ΔIana(load)', 'Vdig', 'Caldel']

        self.ResultData['Table'] = {
           'HEADER': [HeaderRow],
           'BODY': [],
           'FOOTER': [],
        }

        BodyRows = []

        LinkHTMLTemplate = self.TestResultEnvironmentObject.HtmlParser.getSubpart(
           self.TestResultEnvironmentObject.OverviewHTMLTemplate,
           '###LINK###'
        )

        try:
            IanaRocs = self.ParentObject.ResultData['SubTestResults']['Iana'].ResultData['HiddenData']['IanaRocs']
        except:
            IanaRocs = []

        try:
            DeltaAliveHVRocs = self.ParentObject.ResultData['SubTestResults']['DeltaAliveHV'].ResultData['HiddenData']['DeltaAliveHVRocs']
        except:
            DeltaAliveHVRocs = []

        try:
            DeltaIanaRocs = self.ParentObject.ResultData['SubTestResults']['ProgramROC'].ResultData['HiddenData']['DeltaIanaRocs']
        except:
            DeltaIanaRocs = []

        try:
            DeltaIanaRocs2 = self.ParentObject.ResultData['SubTestResults']['Logfile'].ResultData['HiddenData']['IanaLossRoc']
        except:
            DeltaIanaRocs2 = []

        bumpBondingVthrcomp = self.LoadValuesFromFile('bumpBondingVthrcomp.dat', 'int')
        databaseDeadPixels = self.LoadValuesFromFile('databaseDeadPixels.dat', 'int')
        databaseBumpDefects = self.LoadValuesFromFile('databaseBumpDefects.dat', 'int')
        dbPretestCaldel = self.LoadValuesFromFile('dbPretestCaldel.dat', 'int')
        dbPretestVana = self.LoadValuesFromFile('dbPretestVana.dat', 'int')

        dbReceptionDead = self.LoadValuesFromFile('dbReceptionDead.dat', 'int')
        dbReceptionBB = self.LoadValuesFromFile('dbReceptionBB.dat', 'int')

        for i in self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResultDictList']:
            ChipNo = int(i['TestResultObject'].Attributes['ChipNo'])
            GradeMapping = {1: 'A', 2: 'B', 3: 'C', -1: 'None'}
            PixelDefectsGrade = GradeMapping[int(i['TestResultObject'].ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['PixelDefectsGrade']['Value'])]
            NDefects = int(i['TestResultObject'].ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['NDefects'])
            NDeadPixels = int(i['TestResultObject'].ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['NDeadPixels'])
            NDefectiveBumps = int(i['TestResultObject'].ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['NDefectiveBumps'])

            BodyRows.append([
                self.TestResultEnvironmentObject.HtmlParser.substituteMarkerArray(
                       LinkHTMLTemplate,
                       {
                           '###LABEL###':'Chip '+str(ChipNo),
                           '###URL###': os.path.relpath(i['TestResultObject'].FinalResultsStoragePath, self.ParentObject.FinalResultsStoragePath)+'/TestResult.html'
                       }
                ),
                PixelDefectsGrade,
                '%d'%NDefects,
                '%d'%NDeadPixels,
                '%d' % int(dbReceptionDead[ChipNo]) if ChipNo < len(dbReceptionDead) else '-',
                '%d' % int(databaseDeadPixels[ChipNo]) if ChipNo < len(databaseDeadPixels) else '-',
                '%d'%NDefectiveBumps,
                '%d' % int(dbReceptionBB[ChipNo]) if ChipNo < len(dbReceptionBB) else '-',
                '%d' % int(databaseBumpDefects[ChipNo]) if ChipNo < len(databaseBumpDefects) else '-',
                i['TestResultObject'].ResultData['SubTestResults']['PixelAlive'].ResultData['KeyValueDictPairs']['NInefficentPixels']['Value'],
                '%d' % int(DeltaAliveHVRocs[ChipNo]) if ChipNo < len(DeltaAliveHVRocs) else '-',
                '%d' % int(bumpBondingVthrcomp[ChipNo]) if ChipNo < len(bumpBondingVthrcomp) else '-',
                '%d' % int(dbPretestVana[ChipNo]) if ChipNo < len(dbPretestVana) else '-',
                i['TestResultObject'].ResultData['SubTestResults']['DACs'].ResultData['KeyValueDictPairs']['DAC_vana']['Value'] if 'DAC_vana' in i['TestResultObject'].ResultData['SubTestResults']['DACs'].ResultData['KeyValueDictPairs'] else 'None',
                '%1.1f'%IanaRocs[ChipNo] if ChipNo < len(IanaRocs) else '-',
                '%1.1f'%DeltaIanaRocs[ChipNo] if ChipNo < len(DeltaIanaRocs) else '-',
                '%1.1f'%DeltaIanaRocs2[ChipNo] if ChipNo < len(DeltaIanaRocs2) else '-',
                i['TestResultObject'].ResultData['SubTestResults']['DACs'].ResultData['KeyValueDictPairs']['DAC_vdig']['Value'] if 'DAC_vdig' in i['TestResultObject'].ResultData['SubTestResults']['DACs'].ResultData['KeyValueDictPairs'] else 'None',
                i['TestResultObject'].ResultData['SubTestResults']['DACs'].ResultData['KeyValueDictPairs']['DAC_caldel']['Value'] if 'DAC_caldel' in i['TestResultObject'].ResultData['SubTestResults']['DACs'].ResultData['KeyValueDictPairs'] else 'None',

            ])

        self.ResultData['Table']['BODY'] = BodyRows
