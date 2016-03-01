# -*- coding: utf-8 -*-
import ROOT
import json
import os
import shutil
import AbstractClasses

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):

    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_BareModuleTest_Summary1_TestResult'
        self.NameSingle='Summary1'
        self.Title = 'Module Statistic'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'


    def getNumberOfRocsWithGrade(self,grade,gradeList):
        l = [i for i in gradeList if i == grade]
        return len(l)
    
    def PopulateResultData(self):

        #
        # Define subdirectories to store needed DB files to be upload
        #

        bareModuleID = str(self.FinalResultsStoragePath).split('/')[-5]
        bareModuleIDName = bareModuleID.split('_')[-4]
        bareModuleTime = bareModuleID.split('_')[-3] + '_' + bareModuleID.split('_')[-2] + '_' + bareModuleID.split('_')[-1]  
        bareModuleBBDBName = bareModuleIDName + '-BareModuleTestBumpBonding-' + bareModuleTime
        bareModulePADBName = bareModuleIDName + '-BareModuleTestPixelAlive-' + bareModuleTime
        print 'bareModuleID: ',bareModuleID,'  ' ,bareModuleIDName,'  ',bareModuleTime
        #print 'final Name: ', bareModuleBBDBName
        
        
        print 'Creating BumpBonding Subdirectory for DB upload', bareModuleBBDBName

        if not os.path.exists(self.FinalResultsStoragePath + '/' + bareModuleBBDBName ):
            os.makedirs(self.FinalResultsStoragePath + '/' + bareModuleBBDBName )

        print 'Creating PixelAlive Subdirectory for DB upload ', bareModulePADBName

        if not os.path.exists(self.FinalResultsStoragePath + '/' + bareModulePADBName ):
            os.makedirs(self.FinalResultsStoragePath + '/' + bareModulePADBName )  

        # calculate needed variables

        DeadPixels = 0
        DeadBumps = 0
        DeadBumpsBB2 = 0
        MissingBumps = 0
        totalMissingBumps = 0
        totalMissingBumpsBB2 = 0
        totalDeadBumps = 0
        totalDeadPixels = 0
        listDefectBumps = []
        listDefectAlive = []



        # obtain the values to get dispayed

        print 'Begin Summary1: ',self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResultDictList']

        chipResults = self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResultDictList']
        
        #DeadPixelList
        
        allrocslistAlive = []
        allrocs2Alive = {}

        for i in chipResults:
            
            if self.ParentObject.testSoftware == 'pxar':
                try:
                    DeadPixels = int(i['TestResultObject'].ResultData['SubTestResults']['PixelMap'].ResultData['KeyValueDictPairs']['NDeadPixels']['Value']);
                    totalDeadPixels = totalDeadPixels + DeadPixels;
                    listDefectAlive = i['TestResultObject'].ResultData['SubTestResults']['PixelMap'].ResultData['KeyValueDictPairs']['DeadPixels']['Value'];
                except:
                    print 'No PixelAlive data for Chip ',i['TestResultObject'].Attributes['ChipNo'],' adding 4160 dead pixels!'
                    #DeadPixels = 4160;
                    totalDeadPixels = totalDeadPixels + 4160;

            else:
                DeadPixels = int(i['TestResultObject'].ResultData['SubTestResults']['BarePixelMap'].ResultData['KeyValueDictPairs']['NDeadPixels']['Value']);
                totalDeadPixels = totalDeadPixels + DeadPixels;
                listDefectAlive = i['TestResultObject'].ResultData['SubTestResults']['BarePixelMap'].ResultData['KeyValueDictPairs']['DeadPixels']['Value'];
            

            if not listDefectAlive:
                print 'pixel alive test without defects'
            else:
            #if listDefectAlive:
                #print 'blabla', listDefectAlive
                combsAlive = []
                roccombsAlive = {}
                for key in listDefectAlive:
                    dataChipa = key[0];
                    val1a = key[1];
                    val2a = key[2];
                    #print 'again ',dataChipa, val1a, val2a
                    combsAlive.append((val1a,val2a))
                    finalwordAlive = "ROC" + str(dataChipa)
                roccombsAlive[finalwordAlive] = combsAlive
                allrocslistAlive.append(roccombsAlive)
                allrocs2Alive[finalwordAlive] = combsAlive

        # save list of defects bumps in json format
        #fdefectalive = open(self.FinalResultsStoragePath + '/defectsalive.json', 'w')
        fdefectalive = open(self.FinalResultsStoragePath +'/' + bareModulePADBName +'/' + 'defects.json', 'w')
        fdefectalive.write(json.dumps(allrocs2Alive, separators=(',', ': ')))
        fdefectalive.close()

        # prepare files for DB

        Directory = self.RawTestSessionDataPath
        bareModulefilename = Directory+"/bareModuleInfo.txt"

        globalNameLab = ""
        globalOperatorName = ""
        globalTemp = ""
        globalRH = ""
        globalBBcut = ""
        globalBMname = ""
        globaluseBB2Map = ""
        #useBB2Map = "yes"

        
        if os.path.isfile(bareModulefilename):        
            BareModuleInfoFile = open(bareModulefilename, "r")
            print 'Opening BareModuleInfoFile: ', BareModuleInfoFile
        
            if BareModuleInfoFile:
                for line in BareModuleInfoFile:
                    #print 'line',line
                    results  = line.strip().split()
                    if len(results) == 2:
                        Key, ParameterValue = results
                        print Key,ParameterValue
                        if (Key=="Laboratory:"):
                            globalNameLab = ParameterValue
                        if (Key=="Operator:"):
                            globalOperatorName = ParameterValue
                        if (Key=="Temperature:"):
                            globalTemp = ParameterValue
                        if (Key=="RH:"):
                            globalRH = ParameterValue
                        if (Key=="BBcut:"):
                            globalBBcut = ParameterValue
                        if (Key=="BMname:"):
                            globalBMname = ParameterValue
                        if (Key=="useBB2Map:"):
                            globaluseBB2Map = ParameterValue

                        print 'globalNameLab: ',globalNameLab
                        print 'globaluseBB2Map: ',globaluseBB2Map

            BareModuleInfoFile.close()

        else:
            print 'BareModuleInfoFile could not be open: ', bareModulefilename


        falivemapforDB = open(self.FinalResultsStoragePath +'/' + bareModulePADBName +'/' + 'Bare_module_QA_Alive.csv', 'w')
        falivemapforDB.write('Bare_module_ID: ' +  bareModuleIDName + '\n')
        falivemapforDB.write('Laboratory_ID: ' +  ' ' + globalNameLab + '\n')
        falivemapforDB.write('Operator_NickName: ' +  ' ' + globalOperatorName + '\n')
        falivemapforDB.write('Temperature: ' + globalTemp + '\n')
        falivemapforDB.write('RH: ' + globalRH + '\n' )
        falivemapforDB.write('Dead_Missing_Channels: ' + str(totalDeadPixels) + '\n' )
        falivemapforDB.close()
                
        allrocslist = []
        allrocs2 = {}
        allrocslistBB2 = []
        allrocs2BB2 = {}

        digCurrentList = {}
        listPlWidthCut = {}

        for i in chipResults:
            if self.ParentObject.testSoftware == 'pxar':

                try:
                    chipNum = i['TestResultObject'].Attributes['ChipNo'];
                    #print 'DIgCurrent???! ', (i['TestResultObject'].ResultData['SubTestResults']['DigChipCurrent'].ResultData['KeyValueDictPairs']['MaxCurrent']['Value'])
                    valdigChip =  (i['TestResultObject'].ResultData['SubTestResults']['DigChipCurrent'].ResultData['KeyValueDictPairs']['MaxCurrent']['Value'])
                    #print 'DIgCurrent???! ',valdigChip
                    if valdigChip=='None':                    
                        digCurrentList[chipNum] = 'None'
                    else:
                        digCurrentList[chipNum] = 1000.*i['TestResultObject'].ResultData['SubTestResults']['DigChipCurrent'].ResultData['KeyValueDictPairs']['MaxCurrent']['Value'];
                    #print 'chipno ',i['TestResultObject'].Attributes['ChipNo']
                    #print 'DIgCurrent???! ', (i['TestResultObject'].ResultData['SubTestResults']['DigChipCurrent'].ResultData['KeyValueDictPairs']['MaxCurrent']['Value']),i

                    DeadBumps = int(i['TestResultObject'].ResultData['SubTestResults']['BumpBondingProblems'].ResultData['KeyValueDictPairs']['NDeadBumps']['Value']);
                    totalMissingBumps = totalMissingBumps + DeadBumps;
                    #print 'Inside Chips-loop :',chipNum,' : ',totalDeadBumps
                    listDefectBumps = i['TestResultObject'].ResultData['SubTestResults']['BumpBondingProblems'].ResultData['KeyValueDictPairs']['DeadBumps']['Value'];

                    #Check if BB2 Histogram exist:
                    if (globaluseBB2Map=='yes'):
                        listDefectBumpsBB2 = i['TestResultObject'].ResultData['SubTestResults']['BareBBMap'].ResultData['KeyValueDictPairs']['MissingBumps']['Value'];
                        DeadBumpsBB2 = int(i['TestResultObject'].ResultData['SubTestResults']['BareBBMap'].ResultData['KeyValueDictPairs']['NMissingBumps']['Value']);
                        totalMissingBumpsBB2 = totalMissingBumpsBB2 + DeadBumpsBB2;

                except:
                    print 'No BB-Histogram is found Chip: ', i['TestResultObject'].Attributes['ChipNo']
                    #DeadBumps = 4160;
                    totalMissingBumps = totalMissingBumps + 4160;
                    #DeadBumpsBB2 = 4160;
                    totalMissingBumpsBB2 = totalMissingBumpsBB2 + 4160;


            else:
                chipNum = i['TestResultObject'].Attributes['ChipNo'];
                MissingBumps = int(i['TestResultObject'].ResultData['SubTestResults']['BareBBMap'].ResultData['KeyValueDictPairs']['NMissingBumps']['Value']);
                totalMissingBumps = totalMissingBumps + MissingBumps;
                DeadBumps = int(i['TestResultObject'].ResultData['SubTestResults']['BareBBMap'].ResultData['KeyValueDictPairs']['NDeadBumps']['Value']);
                totalDeadBumps = totalDeadBumps + DeadBumps;
                #print 'Inside Chips-loop:',i,MissingBumps,totalDeadBumps
                listDefectBumps = i['TestResultObject'].ResultData['SubTestResults']['BareBBMap'].ResultData['KeyValueDictPairs']['MissingBumps']['Value'];
                listPlWidthCut[chipNum] = i['TestResultObject'].ResultData['SubTestResults']['BareBBWidth'].ResultData['KeyValueDictPairs']['thrCutBB2Map']['Value']


            if not listDefectBumps:
                print 'No list of DefectBumps'
            else:
            #if listDefectBumps:
                #print 'blabla', listDefectBumps
                combs = []
                roccombs = {}
                for key in listDefectBumps:
                    dataChip = key[0];
                    val1 = key[1];
                    val2 = key[2];
                    #print 'again ',dataChip, val1, val2
                    combs.append((val1,val2))
                    finalword = "ROC" + str(dataChip)
                roccombs[finalword] = combs
                allrocslist.append(roccombs)
                allrocs2[finalword] = combs


            if (globaluseBB2Map=='yes'):
                if not listDefectBumpsBB2:
                    print 'listDefectBB2 empty'
                else:
                    combsBB2 = []
                    roccombsBB2 = {}
                    for key in listDefectBumpsBB2:
                        dataChipBB2 = key[0];
                        val1BB2 = key[1];
                        val2BB2 = key[2];
                    #print 'again ',dataChip, val1, val2
                        combsBB2.append((val1BB2,val2BB2))
                        finalwordBB2 = "ROC" + str(dataChipBB2)
                    roccombsBB2[finalwordBB2] = combsBB2
                    allrocslistBB2.append(roccombsBB2)
                    allrocs2BB2[finalwordBB2] = combsBB2


        print 'allroclist ',json.dumps(allrocslist, separators=(',', ':'))
        print 'totalMissingBumps: ',totalMissingBumps,totalDeadBumps

        fdefect = open(self.FinalResultsStoragePath +'/' + bareModuleBBDBName +'/' + 'defects.json', 'w')        
        fdefect.write(json.dumps(allrocs2, separators=(',', ': ')))
        fdefect.close()
        
        fbbmapforDB = open(self.FinalResultsStoragePath +'/' + bareModuleBBDBName +'/' + 'Bare_module_QA_Bump.csv', 'w')
        fbbmapforDB.write('Bare_module_ID: ' +  bareModuleIDName + '\n')
        fbbmapforDB.write('Laboratory_ID: ' +  ' ' +  globalNameLab + '\n')
        fbbmapforDB.write('Operator_NickName: ' +  ' ' + globalOperatorName + '\n')
        fbbmapforDB.write('Temperature: ' + globalTemp +'\n')
        fbbmapforDB.write('RH: ' + globalRH + '\n' )
        fbbmapforDB.write('Dead_Missing_Channels: ' + str(totalMissingBumps) + '\n' )
        #fbbmapforDB.write('BB_cut_criteria: ' + globalBBcut + '\n')
        fbbmapforDB.write('BB_cut_criteria: ' + str(listPlWidthCut) + '\n')
        fbbmapforDB.close()
        
        if (globaluseBB2Map=='yes'):
            fdefectBB2 = open(self.FinalResultsStoragePath +'/' + bareModuleBBDBName +'/' + 'defectsBB2.json', 'w')        
            fdefectBB2.write(json.dumps(allrocs2BB2, separators=(',', ': ')))
            fdefectBB2.close()
            
            fbbmap2forDB = open(self.FinalResultsStoragePath +'/' + bareModuleBBDBName +'/' + 'Bare_module_QA_BumpBB2.csv', 'w')
            fbbmap2forDB.write('Bare_module_ID: ' +  bareModuleIDName + '\n')
            fbbmap2forDB.write('Laboratory_ID: ' +  ' ' +  globalNameLab + '\n')
            fbbmap2forDB.write('Operator_NickName: ' +  ' ' + globalOperatorName + '\n')
            fbbmap2forDB.write('Temperature: ' + globalTemp +'\n')
            fbbmap2forDB.write('RH: ' + globalRH + '\n' )
            fbbmap2forDB.write('Dead_Missing_Channels: ' + str(totalMissingBumpsBB2) + '\n' )
        #fbbmapforDB.write('BB_cut_criteria: ' + globalBBcut + '\n')
            fbbmap2forDB.write('BB_cut_criteria: ' + str(listPlWidthCut) + '\n')
            fbbmap2forDB.close()

        # copy png images to this DB subdirectory
        
        if self.ParentObject.testSoftware == 'pxar':
            srcBumpBondingFigDir = str(self.FinalResultsStoragePath).split('Summary1')[-2]+'BumpBondingMap/BumpBondingMap.png'
            srcPixelAliveFigDir = str(self.FinalResultsStoragePath).split('Summary1')[-2]+'BarePixelMap/BarePixelMap.png'
            if (globaluseBB2Map=='yes'):
                srcBumpBondingBB2FigDir = str(self.FinalResultsStoragePath).split('Summary1')[-2]+'bareBBMap/bareBBMap.png'

        else:
            srcBumpBondingFigDir = str(self.FinalResultsStoragePath).split('Summary1')[-2]+'bareBBMap/bareBBMap.png'
            srcPixelAliveFigDir = str(self.FinalResultsStoragePath).split('Summary1')[-2]+'BarePixelMap/BarePixelMap.png'

        shutil.copyfile(srcBumpBondingFigDir,self.FinalResultsStoragePath +'/' + bareModuleBBDBName +'/bareModuleQA.png' )
        shutil.copyfile(srcPixelAliveFigDir,self.FinalResultsStoragePath +'/' + bareModulePADBName +'/bareModuleQA.png' )
        if (globaluseBB2Map=='yes'):
            shutil.copyfile(srcBumpBondingBB2FigDir,self.FinalResultsStoragePath +'/' + bareModuleBBDBName +'/bareModuleBB2QA.png' )

        self.ResultData['KeyValueDictPairs'] = {
            'NMissingBumps': {
                'Value':totalMissingBumps,
                'Label':'Total MissingBumps'
            },
            'NMissingBumpsBB2': {
                'Value':totalMissingBumpsBB2,
                'Label':'Total MissingBumpsBB2'
            },
            'NDeadBumps': {
                'Value':totalDeadPixels,
                'Label':'Total DeadPixels'
            },
        }

        #self.ResultData['KeyList'] = ['NMissingBumps','NDeadBumps']
        if (globaluseBB2Map=="yes"):
            self.ResultData['KeyList'] = ['NMissingBumps','NMissingBumpsBB2','NDeadBumps']
        else:
            self.ResultData['KeyList'] = ['NMissingBumps','NDeadBumps']

        # prepare also DAC files for DB upload
        DirectoryDac = self.RawTestSessionDataPath
        DirectoryDacToSave = self.FinalResultsStoragePath +'/' + bareModuleBBDBName

        #DAQ_Parameters:    #DAQ_number DAQ_Name Value
        #Bare_module_ROC00_setup.csv


        #digCurrentList = {}
        deser160val = 0
        clkval = 0

        if self.ParentObject.testSoftware == 'pxar':
            #print 'ID measurement from hd histogram'
            deser160val = 4
            clkval = 0
        else:
            deser160val = 5
            clkval = 22
        #    # get the ID measurement from log file
            digCurrentNameFile = DirectoryDac+"/digCurrent.dat"
            fileDigCurrent = open(digCurrentNameFile, 'r')
            for line in fileDigCurrent:
                #results  = line.strip().split()
                #if len(results) == 2:
                #    Key, ParameterValue = results
                #    print 'quees', Key
                #    print 'bla: ',ParameterValue
                digCurrentList[int(line.split()[0])] = str(line.split()[1])
            fileDigCurrent.close()


        for i in range(0,16):            
            print
            #if self.ParentObject.testSoftware == 'pxar':
            dacFileName = DirectoryDac+"/dacParameters_C"+ str(i)+".dat"
            #else:
            #    if i < 10:
            #        dacFileName = DirectoryDac+"/dacParameters_c500_"+ str(globalBMname) + "c0" + str(i)+".dat"
            #    else:
            #        dacFileName = DirectoryDac+"/dacParameters_c500_"+ str(globalBMname) + "c" + str(i)+".dat"
            #    print 'DACFIle: ', dacFileName
            if i < 10:
                dacFileNameForDB =  DirectoryDacToSave+"/Bare_module_ROC0"+ str(i)+"_setup.csv"
            else:
                dacFileNameForDB =  DirectoryDacToSave+"/Bare_module_ROC"+ str(i)+"_setup.csv"
            #print 'the Dac Original Name: ', dacFileName
            #print 'the new file name: ', dacFileNameForDB
            # create the new DAC file
            fileDAC_DB = open(dacFileNameForDB, 'w')
            fileDAC_DB.write('Bare_module_ID: ' +  bareModuleIDName + '\n')
            fileDAC_DB.write('LaboratoryTest: ' +  ' ' +  globalNameLab + '\n')
            fileDAC_DB.write('Operator_NickName: ' +  ' ' + globalOperatorName + '\n')
            fileDAC_DB.write('Temperature: ' + globalTemp +'\n')
            fileDAC_DB.write('RH: ' + globalRH + '\n' )
            fileDAC_DB.write('ROC_type: psi46digv2.1respin'  +'\n')
            fileDAC_DB.write('ROC_ID: '  + str(i) + '\n')
            fileDAC_DB.write('IDig: '  + str(digCurrentList[i]) + '  mA' '\n')
            fileDAC_DB.write('clk:'  + str(deser160val) + '\n')
            fileDAC_DB.write('deser: ' + str(clkval)  +'\n')
            fileDAC_DB.write('DAQ_Parameters: '  + u"\u0023" + 'DAQ_number DAQ_Name Value' + '\n')
                
            existingDacFile = open(dacFileName, 'r')

            for line in existingDacFile:
                #print line
                fileDAC_DB.write(line.lower())
            
            fileDAC_DB.close()
            existingDacFile.close()

