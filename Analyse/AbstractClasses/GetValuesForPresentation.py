# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import time
import glob
import json


class ModuleSummaryValues(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def MakeArray(self,p):

        
        Numbers = {
        'nA' : 0,
        'nB' : 0,
        'nC' : 0,
        'nM' : 0,
        'ntoB' : 0,
        'ntoC' : 0,
        'ntoA' : 0,
        'ntoBX' : 0,
        'ntoCX' : 0,
        'ntoAX' : 0,
        'nlcstartupB': 0, 
        'nlcstartupC' : 0,
        'nIV150B' : 0,
        'nIV150C' : 0,
        'nIV150B+' : 0,
        'nIV150C+' : 0,
        'nIV150m20B' : 0,
        'nIV150m20C' : 0,
        'nIVSlopeB' : 0,
        'nIVSlopeC' : 0,
        'nRecCurrentB' : 0,
        'nRecCurrentC' : 0,
        'nCurrentRatioB' : 0,
        'nCurrentRatioC' : 0,
        'ntotDefectsB' : 0,
        'ntotDefectsC' : 0,
        'ntotDefectsXrayB' : 0,
        'ntotDefectsXrayC' : 0,
        'nBBFullB' : 0,
        'nBBFullC' : 0,
        'nBBXrayB' : 0,
        'nBBXrayC' : 0,
        'nAddressdefB' : 0,
        'nAddressdefC' : 0,
        'nTrimbitdefB' : 0,
        'nTrimbitdefC' : 0,
        'nMaskdefB' : 0,
        'nMaskdefC' : 0,
        'ndeadpixB' : 0,
        'ndeadpixC' : 0,
        'nNoiseB' : 0,
        'nNoiseC' : 0,
        'nNoiseXrayB' : 0,
        'nNoiseXrayC' : 0,
        'nPedSpreadB' : 0,
        'nPedSpreadC' : 0,
        'nRelGainWB' : 0,
        'nRelGainWC' : 0,
        'nVcalThrWB' : 0,
        'nVcalThrWC' : 0,
        'nLowHREfB' : 0,
        'nLowHREfC' : 0,
        'nHDIf' : 0,
        'nIV' : 0,
        'nIVP' : 0,
        'nBB' : 0,
        'nNP' : 0,
        'ntotDefects' : 0,
        'nDC' : 0,
        'nLowHREf' : 0,
        'nOthers' : 0,
        'commentsgradechange' : '',
        'commentsgradechangeX' : '',
        'nFirstModule' : '',
        'nLastModule' : '',
        'PrimaryFailureReason' : {}
}



        Rows = self.FetchData()

        ModuleIDsList = []
        for RowTuple in Rows:
            if not RowTuple['ModuleID'] in ModuleIDsList:
                ModuleIDsList.append(RowTuple['ModuleID'])
        ModuleIDsList.sort(reverse=True)

        Numbers['nFirstModule'] = ModuleIDsList[0]
        Numbers['nLastModule'] = ModuleIDsList[len(ModuleIDsList)-1]


        FullTests = ['m20_1','m20_2','p17_1'][::-1]
        TestTypeLeakageCurrentPON = ['LeakageCurrentPON']
        Final_Grades = []

        FTMinus20BTC_Grades = []
        FTMinus20ATC_Grades = []
        FT17_Grades = []
        XrayCal_Grades = []
        XrayHR_Grades = []
        Final_Grades = []
        comments = ''
        commentsX = ''


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


        HDIProblems = 0
        DCProblems = 0

        #Get primary defect leading to downgrade - from pie chart
        Path = p
        filename_primaryfailure = "{Path}/ProductionOverview/ProductionOverviewPage_Total/PrimaryFailureReason/KeyValueDictPairs.json".format(Path=Path)
        data = open(filename_primaryfailure, 'r')
        primarydefect = json.load(data)

        Numbers['PrimaryFailureReason'] = primarydefect

        #Number of manual regradings

        for ModuleID in ModuleIDsList:

            finalF = [0]*3
            finalX = 0
            final = 0
            co = ""

            for RowTuple in Rows:
                if RowTuple['ModuleID'] == ModuleID:

                    TestType = RowTuple['TestType']
                    if TestType != 'TemperatureCycle':

                        
                       
                        reg = str(self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Grading', 'KeyValueDictPairs.json','ManualGrade', 'Value']))
                        if (co=='' or co=='None'):
                            c = str(self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], 'QualificationGroup', 'KeyValueDictPairs.json', 'Comment', 'Value']))
                            c = c[13:-2]
                            if (c is not 'None' and c is not ''):
                                co = RowTuple['ModuleID'] + " : " + c
                                #print co 

                        try: 
                            if (reg!='' and reg!='None'):
                                if (TestType == "XRayHRQualification"):
                                    finalX=reg
                                elif (TestType == 'm20_1'):
                                    finalF[0] = reg
                                elif (TestType == 'm20_2'):
                                    finalF[1] = reg
                                elif (TestType == "p17_1"):
                                    finalF[2] = reg

                                if '3' in finalF:
                                    final = '3'
                                elif '2' in finalF:
                                    final = '2'
                                elif '1' in finalF:
                                    final = '1'
                        except:
                            pass



            modg = 0
            modgX = 0
            if (finalX=='2'):
                Numbers['ntoBX'] += 1
                modgX = 1
            elif (finalX=='3'):
                Numbers['ntoCX'] += 1
                modgX = 1
            elif (finalX=='1'):
                Numbers['ntoAX'] += 1
                modgX = 1

            if (final=='2'):
                Numbers['ntoB'] += 1
                modg = 1
            elif (final=='3'):
                Numbers['ntoC'] += 1
                modg = 1
            elif (final=='1'):
                Numbers['ntoA'] += 1
                modg = 1


            if modg == 1:
                comments = comments + co + "\\\\"
            if modgX == 1:
                commentsX = commentsX + co + "\\\\"


        Numbers['commentsgradechange'] = comments
        Numbers['commentsgradechangeX'] = commentsX


        # Get number of modules for each defect from module defects table
        filename = "{Path}/ProductionOverview/ProductionOverviewPage_Total/ModuleFailuresOverview/KeyValueDictPairs.json".format(Path=Path)
        data = open(filename, 'r')
        moduledefects = json.load(data)
       

        for mod, defects in moduledefects.iteritems():


            for d, grade in defects.iteritems():

                if (d == 'TotalDefects' and grade!=""):
                    tag = "A"
                    for test, g in grade.iteritems():
                        if g == "C":
                            tag = "C"
                        elif (tag!="C" and g == "B"):
                            tag = "B"
                    if tag == "B" :
                        Numbers['ntotDefectsB'] += 1
                    elif tag == "C":
                        Numbers['ntotDefectsC'] += 1

                if (d == 'TotalDefects_X-ray' and grade!=""):
                    if grade == "B" :
                        Numbers['ntotDefectsXrayB'] += 1
                    elif grade == "C":
                        Numbers['ntotDefectsXrayC'] += 1
                        

        for mod, defects in moduledefects.iteritems():


            for d, grade in defects.iteritems():


                if (d == 'AddressDefects' and grade!=""):
                    tag = "A"
                    for test, g in grade.iteritems():
                        if g == "C":
                            tag = "C"
                        elif (tag!="C" and g == "B"):
                            tag = "B"
                    if tag == "B":
                        Numbers['nAddressdefB'] += 1
                    elif tag == "C":
                        Numbers['nAddressdefC'] += 1

                if (d == 'BB_Fulltest' and grade!=""):
                    tag = "A"
                    for test, g in grade.iteritems():
                        if g == "C":
                            tag = "C"
                        elif (tag!="C" and g == "B"):
                            tag = "B"
                    if tag == "B" :
                        Numbers['nBBFullB'] += 1
                    elif tag == "C":
                        Numbers['nBBFullC'] += 1

                if (d == 'BB_X-ray' and grade!=""):
                    if grade == "B" :
                        Numbers['nBBXrayB'] += 1
                    elif grade == "C":
                        Numbers['nBBXrayC'] += 1           

                if (d == 'IVRatio150' and grade!=""):
                    tag = "A"
                    for test, g in grade.iteritems():
                        if g == "C":
                            tag = "C"
                        elif (tag!="C" and g == "B"):
                            tag = "B"
                    if tag == "B" :
                        Numbers['nCurrentRatioB'] += 1
                    elif tag == "C":
                        Numbers['nCurrentRatioC'] += 1

                if (d == 'IVSlope' and grade!=""):
                    if grade == "B" :
                        Numbers['nIVSlopeB'] += 1
                    elif grade == "C":
                        Numbers['nIVSlopeC'] += 1

                if (d == 'LCStartup' and grade!=""):
                    if grade == "B" :
                        Numbers['nlcstartupB'] += 1
                    elif grade == "C":
                        Numbers['nlcstartupC'] += 1

                if (d == 'Noise' and grade!=""):
                    tag = "A"
                    for test, g in grade.iteritems():
                        if g == "C":
                            tag = "C"
                        elif (tag!="C" and g == "B"):
                            tag = "B"
                    if tag == "B" :
                        Numbers['nNoiseB'] += 1
                    elif tag == "C":
                        Numbers['nNoiseC'] += 1

                if (d == 'Noise_X-ray' and grade!=""):
                    if grade == "B" :
                        Numbers['nNoiseXrayB'] += 1
                    elif grade == "C":
                        Numbers['nNoiseXrayC'] += 1

                if (d == 'PedestalSpread' and grade!=""):
                    tag = "A"
                    for test, g in grade.iteritems():
                        if g == "C":
                            tag = "C"
                        elif (tag!="C" and g == "B"):
                            tag = "B"
                    if tag == "B" :
                        Numbers['nPedSpreadB'] += 1
                    elif tag == "C":
                        Numbers['nPedSpreadC'] += 1

                if (d == 'RelativeGainWidth' and grade!=""):
                    tag = "A"
                    for test, g in grade.iteritems():
                        if g == "C":
                            tag = "C"
                        elif (tag!="C" and g == "B"):
                            tag = "B"
                    if tag == "B" :
                        Numbers['nRelGainWB'] += 1
                    elif tag == "C":
                        Numbers['nRelGainWC'] += 1


                if (d == 'VcalThrWidth' and grade!=""):
                    tag = "A"
                    for test, g in grade.iteritems():
                        if g == "C":
                            tag = "C"
                        elif (tag!="C" and g == "B"):
                            tag = "B"
                    if tag == "B" :
                        Numbers['nVcalThrWB'] += 1
                    elif tag == "C":
                        Numbers['nVcalThrWC'] += 1

                if (d == 'deadPixels' and grade!=""):
                    tag = "A"
                    for test, g in grade.iteritems():
                        if g == "C":
                            tag = "C"
                        elif (tag!="C" and g == "B"):
                            tag = "B"
                    if tag == "B" :
                        Numbers['ndeadpixB'] += 1
                    elif tag == "C":
                        Numbers['ndeadpixC'] += 1

                if (d == 'lowHREfficiency' and grade!=""):
                    if grade == "B" :
                        Numbers['nLowHREfB'] += 1
                    elif grade == "C":
                        Numbers['nLowHREfC'] += 1

                if (d == 'maskDefects' and grade!=""):
                    tag = "A"
                    for test, g in grade.iteritems():
                        if g == "C":
                            tag = "C"
                        elif (tag!="C" and g == "B"):
                            tag = "B"
                    if tag == "B" :
                        Numbers['nMaskdefB'] += 1
                    elif tag == "C":
                        Numbers['nMaskdefC'] += 1

                if (d == 'trimbitDefects' and grade!=""):
                    tag = "A"
                    for test, g in grade.iteritems():
                        if g == "C":
                            tag = "C"
                        elif (tag!="C" and g == "B"):
                            tag = "B"
                    if tag == "B" :
                        Numbers['nTrimbitdefB'] += 1
                    elif tag == "C":
                        Numbers['nTrimbitdefC'] += 1


        #Categorize modules with leakage current problems
        for ModuleID in ModuleIDsList:

            lcm20 = 0
            lcp17 = 0

            for RowTuple in Rows:
                if RowTuple['ModuleID']==ModuleID:
                    TestType = RowTuple['TestType']

                    if (TestType == "m20_2"):
                        try: 
                            lcm20 = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], 'QualificationGroup', 'ModuleFulltestPxar_m20_2', 'IVCurve','KeyValueDictPairs.json', 'CurrentAtVoltage150V', 'Value'])
                            if not lcm20:
                                lcm20 = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], 'QualificationGroup', 'ModuleFulltest_m20_2', 'IVCurve','KeyValueDictPairs.json', 'CurrentAtVoltage150V', 'Value'])
                        except:
                            pass

                    if (TestType == "p17_1"):
                        try: 
                            lcp17 = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], 'QualificationGroup', 'ModuleFulltestPxar_p17_1', 'IVCurve','KeyValueDictPairs.json', 'CurrentAtVoltage150V', 'Value'])
                            if not lcp17:
                                lcp17 = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], 'QualificationGroup', 'ModuleFulltest_p17_1', 'IVCurve','KeyValueDictPairs.json', 'CurrentAtVoltage150V', 'Value'])
                        except:
                            pass
                                
            try:
                if (float(lcp17)>10 and float(lcm20)<2): 
                    Numbers['nIV150C'] += 1
                elif (float(lcp17)>2 and float(lcm20)<2):
                    Numbers['nIV150B'] += 1
                elif (float(lcp17)>10 and float(lcm20)>2): 
                    Numbers['nIV150C+'] += 1
                elif (float(lcp17)>2 and float(lcm20)>2):
                    Numbers['nIV150B+'] += 1
                if (float(lcm20)>2):
                    Numbers['nIV150m20B'] += 1
            except:
                pass

       
        return Numbers

