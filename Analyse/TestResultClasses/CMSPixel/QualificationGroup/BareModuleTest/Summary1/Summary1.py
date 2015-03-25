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
        MissingBumps = 0
        totalMissingBumps = 0
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
                DeadPixels = int(i['TestResultObject'].ResultData['SubTestResults']['PixelMap'].ResultData['KeyValueDictPairs']['NDeadPixels']['Value']);
                totalDeadPixels = totalDeadPixels + DeadPixels;
                listDefectAlive = i['TestResultObject'].ResultData['SubTestResults']['PixelMap'].ResultData['KeyValueDictPairs']['DeadPixels']['Value'];
            else:
                DeadPixels = int(i['TestResultObject'].ResultData['SubTestResults']['BarePixelMap'].ResultData['KeyValueDictPairs']['NDeadPixels']['Value']);
                totalDeadPixels = totalDeadPixels + DeadPixels;
                listDefectAlive = i['TestResultObject'].ResultData['SubTestResults']['BarePixelMap'].ResultData['KeyValueDictPairs']['DeadPixels']['Value'];
            

            if not listDefectAlive:
                print 'Nothing here'
            else:
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
        
        if os.path.isfile(bareModulefilename):        
            BareModuleInfoFile = open(bareModulefilename, "r")
            print 'Opening BareModuleInfoFile: ', BareModuleInfoFile
        
            if BareModuleInfoFile:
                for line in BareModuleInfoFile:
                    print 'line',line
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

                        print 'globalNameLab: ',globalNameLab

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

        for i in chipResults:
            if self.ParentObject.testSoftware == 'pxar':
                DeadBumps = int(i['TestResultObject'].ResultData['SubTestResults']['BumpBondingProblems'].ResultData['KeyValueDictPairs']['NDeadBumps']['Value']);
                totalMissingBumps = totalMissingBumps + DeadBumps;
                print 'Inside Chips-loop:',i,totalDeadBumps
                listDefectBumps = i['TestResultObject'].ResultData['SubTestResults']['BumpBondingProblems'].ResultData['KeyValueDictPairs']['DeadBumps']['Value'];
            else:
                MissingBumps = int(i['TestResultObject'].ResultData['SubTestResults']['BareBBMap'].ResultData['KeyValueDictPairs']['NMissingBumps']['Value']);
                totalMissingBumps = totalMissingBumps + MissingBumps;
                DeadBumps = int(i['TestResultObject'].ResultData['SubTestResults']['BareBBMap'].ResultData['KeyValueDictPairs']['NDeadBumps']['Value']);
                totalDeadBumps = totalDeadBumps + DeadBumps;
                #print 'Inside Chips-loop:',i,MissingBumps,totalDeadBumps
                listDefectBumps = i['TestResultObject'].ResultData['SubTestResults']['BareBBMap'].ResultData['KeyValueDictPairs']['MissingBumps']['Value'];


            if not listDefectBumps:
                print 'Nothing here'
            else:
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
        fbbmapforDB.write('BB_cut_criteria: ' + globalBBcut + '\n')
        fbbmapforDB.close()
        
        # copy png images to this DB subdirectory
        
        if self.ParentObject.testSoftware == 'pxar':
            srcBumpBondingFigDir = str(self.FinalResultsStoragePath).split('Summary1')[-2]+'BumpBondingMap/BumpBondingMap.png'
            srcPixelAliveFigDir = str(self.FinalResultsStoragePath).split('Summary1')[-2]+'BarePixelMap/BarePixelMap.png'
        else:
            srcBumpBondingFigDir = str(self.FinalResultsStoragePath).split('Summary1')[-2]+'bareBBMap/bareBBMap.png'
            srcPixelAliveFigDir = str(self.FinalResultsStoragePath).split('Summary1')[-2]+'BarePixelMap/BarePixelMap.png'

        shutil.copyfile(srcBumpBondingFigDir,self.FinalResultsStoragePath +'/' + bareModuleBBDBName +'/bareModuleQA.png' )
        shutil.copyfile(srcPixelAliveFigDir,self.FinalResultsStoragePath +'/' + bareModulePADBName +'/bareModuleQA.png' )

        self.ResultData['KeyValueDictPairs'] = {
            'NMissingBumps': {
                'Value':totalMissingBumps,
                'Label':'Total MissingBumps'
            },
            'NDeadBumps': {
                'Value':totalDeadPixels,
                'Label':'Total DeadPixels'
            },
        }


        self.ResultData['KeyList'] = ['NMissingBumps','NDeadBumps']

        

        
