# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import time
import glob
import json

class ModuleSummaryValues(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def MakeArray(self):

        
        Numbers = {
        'nA' : 0,
        'nB' : 0,
        'nC' : 0,
        'nM' : 0,
        'BrokenROC' : 0,
        'BrokenROCX' : 0,
        'nAtoB' : 0,
        'nAtoC' : 0,
        'nBtoC' : 0,
        'nBtoA' : 0,
        'nCtoA' : 0,
        'nCtoB' : 0,
        'nAtoBX' : 0,
        'nAtoCX' : 0,
        'nBtoCX' : 0,
        'nBtoAX' : 0,
        'nCtoAX' : 0,
        'nCtoBX' : 0
        }

        Rows = self.FetchData()

        ModuleIDsList = []
        for RowTuple in Rows:
            if not RowTuple['ModuleID'] in ModuleIDsList:
                ModuleIDsList.append(RowTuple['ModuleID'])
        ModuleIDsList.sort(reverse=True)

        FullTests = ['m20_1','m20_2','p17_1'][::-1]
        Final_Grades = []

        FTMinus20BTC_Grades = []
        FTMinus20ATC_Grades = []
        FT17_Grades = []
        XrayCal_Grades = []
        XrayHR_Grades = []
        Final_Grades = []

        for ModuleID in ModuleIDsList:

            FTMinus20BTC = ''
            FTMinus20ATC = ''
            FT17 = ''
            XrayCal = ''
            XrayHR = ''
            Complete = ''

            ModuleGrades = []

            for RowTuple in Rows:
                if RowTuple['ModuleID']==ModuleID:
                    TestType = RowTuple['TestType']
                    if TestType == 'm20_1':
                        FTMinus20BTC = RowTuple['Grade'] if RowTuple['Grade'] is not None else ''
                        ModuleGrades.append(RowTuple['Grade'])
                    if TestType == 'm20_2':
                        FTMinus20ATC = RowTuple['Grade'] if RowTuple['Grade'] is not None else ''
                        ModuleGrades.append(RowTuple['Grade'])
                    if TestType == 'p17_1':
                        FT17 =  RowTuple['Grade'] if RowTuple['Grade'] is not None else ''
                        ModuleGrades.append(RowTuple['Grade'])
                    if TestType == 'XrayCalibration_Spectrum':
                        XrayCal = RowTuple['Grade'] if RowTuple['Grade'] is not None else ''
                        ModuleGrades.append(RowTuple['Grade'])
                    if TestType == 'XRayHRQualification':
                        XrayHR = RowTuple['Grade'] if RowTuple['Grade'] is not None else ''
                        ModuleGrades.append(RowTuple['Grade'])


            if self.ModuleQualificationIsComplete(ModuleID, Rows):
                FinalGrade = self.GetFinalGrade(ModuleID, Rows)
                Final_Grades.append(FinalGrade)
        

        Numbers['nA'] = len([x for x in Final_Grades if x=='A'])
        Numbers['nB'] = len([x for x in Final_Grades if x=='B'])
        Numbers['nC'] = len([x for x in Final_Grades if x=='C'])
        Numbers['nM'] = len(ModuleIDsList) - len(Final_Grades)

        DefectROCs = 0
        DefectROCsX = 0


        for ModuleID in ModuleIDsList:

            grades = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            Pixdefects = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            gradesX = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            PixdefectsX = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            initialF = [0,0,0]
            finalF = [0,0,0]
            initialX = 0 
            finalX = 0
            initial = 0
            final = 0

            for RowTuple in Rows:
                if RowTuple['ModuleID'] == ModuleID:

                    TestType = RowTuple['TestType']
                    if TestType != 'TemperatureCycle':

                        #Number of broken ROCs
                        if TestType in FullTests:
                            Pixdefects[0] = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip0', 'Summary' ,'KeyValueDictPairs.json', 'Total', 'Value'])
                            Pixdefects[1] = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip1', 'Summary' ,'KeyValueDictPairs.json', 'Total', 'Value'])
                            Pixdefects[2] = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip2', 'Summary' ,'KeyValueDictPairs.json', 'Total', 'Value'])
                            Pixdefects[3] = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip3', 'Summary' ,'KeyValueDictPairs.json', 'Total', 'Value'])                        
                            Pixdefects[4] = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip4', 'Summary' ,'KeyValueDictPairs.json', 'Total', 'Value'])                         
                            Pixdefects[5] = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip5', 'Summary' ,'KeyValueDictPairs.json', 'Total', 'Value'])
                            Pixdefects[6] = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip6', 'Summary' ,'KeyValueDictPairs.json', 'Total', 'Value'])
                            Pixdefects[7] = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip7', 'Summary' ,'KeyValueDictPairs.json', 'Total', 'Value'])
                            Pixdefects[8] = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip8', 'Summary' ,'KeyValueDictPairs.json', 'Total', 'Value'])
                            Pixdefects[9] = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip9', 'Summary' ,'KeyValueDictPairs.json', 'Total', 'Value'])
                            Pixdefects[10] = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip10', 'Summary' ,'KeyValueDictPairs.json', 'Total', 'Value'])
                            Pixdefects[11] = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip11', 'Summary' ,'KeyValueDictPairs.json', 'Total', 'Value'])
                            Pixdefects[12] = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip12', 'Summary' ,'KeyValueDictPairs.json', 'Total', 'Value'])
                            Pixdefects[13] = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip13', 'Summary' ,'KeyValueDictPairs.json', 'Total', 'Value'])
                            Pixdefects[14] = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip14', 'Summary' ,'KeyValueDictPairs.json', 'Total', 'Value'])
                            Pixdefects[15] = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip15', 'Summary' ,'KeyValueDictPairs.json', 'Total', 'Value'])

                        elif TestType == 'XRayHRQualification':
                            PixdefectsX[0] = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip0', 'Grading' ,'KeyValueDictPairs.json', 'PixelDefects', 'Value'])
                            PixdefectsX[1] = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip1', 'Grading' ,'KeyValueDictPairs.json', 'PixelDefects', 'Value'])
                            PixdefectsX[2] = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip2', 'Grading' ,'KeyValueDictPairs.json', 'PixelDefects', 'Value'])
                            PixdefectsX[3] = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip3', 'Grading' ,'KeyValueDictPairs.json', 'PixelDefects', 'Value'])
                            PixdefectsX[4] = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip4', 'Grading' ,'KeyValueDictPairs.json', 'PixelDefects', 'Value'])
                            PixdefectsX[5] = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip5', 'Grading' ,'KeyValueDictPairs.json', 'PixelDefects', 'Value'])
                            PixdefectsX[6] = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip6', 'Grading' ,'KeyValueDictPairs.json', 'PixelDefects', 'Value'])
                            PixdefectsX[7] = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip7', 'Grading' ,'KeyValueDictPairs.json', 'PixelDefects', 'Value'])
                            PixdefectsX[8] = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip8', 'Grading' ,'KeyValueDictPairs.json', 'PixelDefects', 'Value'])
                            PixdefectsX[9] = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip9', 'Grading' ,'KeyValueDictPairs.json', 'PixelDefects', 'Value'])
                            PixdefectsX[10] = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip10', 'Grading' ,'KeyValueDictPairs.json', 'PixelDefects', 'Value'])
                            PixdefectsX[11] = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip11', 'Grading' ,'KeyValueDictPairs.json', 'PixelDefects', 'Value'])
                            PixdefectsX[12] = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip12', 'Grading' ,'KeyValueDictPairs.json', 'PixelDefects', 'Value'])
                            PixdefectsX[13] = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip13', 'Grading' ,'KeyValueDictPairs.json', 'PixelDefects', 'Value'])
                            PixdefectsX[14] = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip14', 'Grading' ,'KeyValueDictPairs.json', 'PixelDefects', 'Value'])
                            PixdefectsX[15] = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip15', 'Grading' ,'KeyValueDictPairs.json', 'PixelDefects', 'Value'])
                 


                        for  i, v in enumerate(Pixdefects):
                            if v is not None and float(v) > 1000:
                                grades[i] = 1

                        for  i, v in enumerate(PixdefectsX):
                            if v is not None and float(v) > 1000:
                                gradesX[i] = 1

                        #Number of manual regradings
                        reg = str(self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Grading', 'KeyValueDictPairs.json', 'GradeComment', 'Value']))
                        
                        try: 
                            if (reg!=''):
                                if (TestType == "XRayHRQualification"):
                                    initialX=reg[28]
                                    finalX=reg[33]
                                elif (TestType == 'm20_1'):
                                    initialF[0] = reg[28]
                                    finalF[0] = reg[33]
                                elif (TestType == 'm20_2'):
                                    initialF[1] = reg[28]
                                    finalF[1] = reg[33]
                                elif (TestType == "p17_1"):
                                    initialF[2] = reg[28]
                                    finalF[2] = reg[33]

                                if 'C' in initialF:
                                    initial = 'C'
                                elif 'B' in initialF:
                                    initial = 'B'
                                elif 'A' in initialF:
                                    initial = 'A'

                                if 'C' in finalF:
                                    final = 'C'
                                elif 'B' in finalF:
                                    final = 'B'
                                elif 'A' in finalF:
                                    final = 'A'

                               
                        except:
                            pass

                    
            if (initialX=='A' and finalX=='B'):
                Numbers['nAtoBX'] += 1
            elif (initialX=='A' and finalX=='C'):
                Numbers['nAtoCX'] += 1
            elif (initialX=='B' and finalX=='A'):
                Numbers['nBtoAX'] += 1
            elif (initialX=='B' and finalX=='C'):
                Numbers['nBtoCX'] += 1
            elif (initialX=='C' and finalX=='A'):
                Numbers['nCtoAX'] += 1
            elif (initialX=='C' and finalX=='B'):
                Numbers['nCtoBX'] += 1

            if (initial=='A' and final=='B'):
                Numbers['nAtoB'] += 1
            elif (initial=='A' and final=='C'):
                Numbers['nAtoC'] += 1
            elif (initial=='B' and final=='A'):
                Numbers['nBtoA'] += 1
            elif (initial=='B' and final=='C'):
                Numbers['nBtoC'] += 1
            elif (initial=='C' and final=='A'):
                Numbers['nCtoA'] += 1
            elif (initial=='C' and final=='B'):
                Numbers['nCtoB'] += 1




            if (grades.count(1)>0):
                DefectROCs += 1

            if (gradesX.count(1)>0):
                DefectROCsX += 1


                        


        Numbers['BrokenROC'] = DefectROCs
        Numbers['BrokenROCX'] = DefectROCsX
        
        return Numbers


