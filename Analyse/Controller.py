# -*- coding: utf-8 -*-
'''
Program    : MORE-Web 
 Author    : Esteban Marin - estebanmarin@gmx.ch
 Version    : 2.1
 Release Date    : 2013-05-30
'''
from AbstractClasses import GeneralTestResult, TestResultEnvironment, ModuleResultOverview
import AbstractClasses.Helper.hasher as hasher
import argparse
# from AbstractClasses import Helper
import TestResultClasses.CMSPixel.QualificationGroup.TestResult
import os, time,shutil, sys
# import errno
import ConfigParser

#arg parse to analyse a single Fulltest
parser = argparse.ArgumentParser(description='MORE web Controller: an analysis software for CMS pixel modules and ROCs')
parser.add_argument('-FT','--singleFulltest',dest='singleFulltestPath',metavar='PATH',
                     help='option which can be used to analyse a single Fulltest, as the second argument needs the path where the single fulltest data are stored',
                     default='')
# parser.add_argument('-M','--ModuleVersion',dest='ModuleVersion',metavar='VERSION',
#                     help='option to choose which module version is analysed [singleROC =3, Module ={1,2}]',default='')
parser.add_argument('-noDB','--noDBupload',dest='DBUpload',action='store_false',
                    help='deactivates upload to DB within this analysis session')
parser.add_argument('-v','--verbose',dest='verbose',action='store_true',default = False,
                    help='activates verbose mode')
parser.add_argument('-withDB','--withDBupload',dest='DBUpload',action='store_true',
                    help='activates upload to DB within this analysis session [default]')
parser.add_argument('-rev','--analysis-revision',dest='revision',metavar='REV',default = -1,
                    help='setting analysis revision number by hand to create an extra directory, alternative: Configuration/SystemConfiguration.cfg --> AnalysisRevision')
parser.set_defaults(DBUpload=True)
args = parser.parse_args()
verbose = args.verbose

import AbstractClasses.Helper.ROOTConfiguration as ROOTConfiguration


ROOTConfiguration.initialise_ROOT()
Configuration = ConfigParser.ConfigParser()
Configuration.read([
    'Configuration/GradingParameters.cfg', 
    'Configuration/SystemConfiguration.cfg', 
    'Configuration/Paths.cfg',
    'Configuration/ModuleInformation.cfg'])

if args.revision != -1:
    revisionNumber = int(args.revision)
elif Configuration.has_option('SystemConfiguration', 'AnalysisRevision'):
    revisionNumber = Configuration.getint('SystemConfiguration', 'AnalysisRevision')
else:
    revisionNumber  = 0
print 'MORE web analysis script, Revision number %s'%revisionNumber
RevisionString = "-R%03d"%revisionNumber

GlobalDataDirectory = Configuration.get('Paths', 'GlobalDataDirectory')
GlobalOverviewPath = Configuration.get('Paths', 'GlobalOverviewPath')
if Configuration.has_option('Paths','GlobalFinalResultsPath'):
    GlobalFinalResultsPath = Configuration.get('Paths','GlobalFinalResultsPath')+'/REV%03d'%revisionNumber
else:
    GlobalFinalResultsPath = ''
print 'GlobalFinalResultsPath: "%s"'%GlobalFinalResultsPath
if GlobalFinalResultsPath!= '' and not os.path.exists(GlobalFinalResultsPath):
    os.makedirs(GlobalFinalResultsPath)
    
SQLiteDBPath = GlobalOverviewPath + '/ModuleResultDB.sqlite'
ModuleVersion = int(Configuration.get('ModuleInformation', 'ModuleVersion'))
     
TestType = Configuration.get('TestType','TestType')

TestResultEnvironmentInstance = TestResultEnvironment.TestResultEnvironment(Configuration)
TestResultEnvironmentInstance.SQLiteDBPath = SQLiteDBPath
TestResultEnvironmentInstance.GlobalOverviewPath = GlobalOverviewPath
TestResultEnvironmentInstance.OpenDBConnection()
TestResultEnvironmentInstance.GlobalDataDirectory = GlobalDataDirectory

if Configuration.has_option('Paths','AbsoluteOverviewPage'):
    TestResultEnvironmentInstance.Configuration['OverviewHTMLLink'] = Configuration.get('Paths','AbsoluteOverviewPage')
    raw_input('AbsoluteOverviewPage %s'%TestResultEnvironmentInstance.Configuration['OverviewHTMLLink'])

hasher.create_hash_file_directory('checksum.md5','.')

ModuleTestResults = []


def extractModuleInformation(ModuleInformationRaw):
    return {
                    'ModuleID': ModuleInformationRaw[0],
                    'TestDate': ModuleInformationRaw[4],
                    'QualificationType': ModuleInformationRaw[1]
                }

def GetFinalModuleResultsPath(ModuleFolder):
    if GlobalFinalResultsPath=='':
        FinalModuleResultsPath = GlobalDataDirectory+'/'+ModuleFolder+'/FinalResults'+RevisionString
    else:
        FinalModuleResultsPath = GlobalFinalResultsPath+'/'+ModuleFolder
    if not os.path.exists(FinalModuleResultsPath):
        os.makedirs(FinalModuleResultsPath)
    return FinalModuleResultsPath
   
def NeedsToBeAnalyzed(FinalModuleResultsPath,ModuleInformation):   
    md5FileName= FinalModuleResultsPath+'/'+ 'checksum.md5'
    retVal = True
    if os.path.exists(md5FileName):
        if verbose: print 'md5 sum exists %s'%md5FileName
        bSameFiles = hasher.compare_two_files('checksum.md5',md5FileName)
        if not Configuration.getboolean('SystemConfiguration','UseGlobalDatabase'):
            bExistInDB = TestResultEnvironmentInstance.existInDB(ModuleInformation['ModuleID'],ModuleInformation['QualificationType'])
            if verbose: print 'check if Module exists: %s'%bExistInDB
        else:
            if verbose: print 'use Global DataBase: ',Configuration.get('SystemConfiguration','UseGlobalDatabase')
            bExistInDB = False
        if verbose: print 'same file: %s / exists in DB: %s'%(bSameFiles,bExistInDB)
        if bSameFiles and bExistInDB:
            print 'do not analyse folder '+ FinalModuleResultsPath +'\n'
            retVal = False
    return retVal

def CopyMD5File(FinalModuleResultsPath):
    print 'copyfile checksum'
    md5FileName= FinalModuleResultsPath+'/'+ 'checksum.md5'
    shutil.copyfile('checksum.md5',md5FileName)

def GetModuleTestResult(TestResultEnvironment,FinalModuleResultsPath,ModuleInformation):
    return TestResultClasses.CMSPixel.QualificationGroup.TestResult.TestResult(
        TestResultEnvironmentInstance, 
        None, 
        'TestResultClasses.CMSPixel.QualificationGroup', 
        FinalModuleResultsPath,
        {
            'TestDate':ModuleInformation['TestDate'],
            'TestedObjectID':ModuleInformation['ModuleID'],
            'ModuleID':ModuleInformation['ModuleID'],
            'ModuleVersion':ModuleVersion,
            'ModuleType':'a',
            'TestType':TestType,
            'QualificationType': ModuleInformation['QualificationType']
        }    
    )
    

def CreateApacheWebserverConfiguration(FinalResultsPath):
    # add apache webserver configuration for compressed svg images  
    f = open(FinalResultsPath + '/.htaccess', 'w')
    f.write('''
    AddType image/svg+xml svg
    AddType image/svg+xml svgz
    AddEncoding x-gzip .svgz
    ''')
    f.close()    
    
def AnalyseTestData(ModuleInformationRaw,ModuleFolder):
    global FinalResultDirectory
    #,ModuleInformation
    ModuleInformation = extractModuleInformation(ModuleInformationRaw) 
    FinalModuleResultsPath = GetFinalModuleResultsPath(ModuleFolder)
    TestResultEnvironmentInstance.ModuleDataDirectory = GlobalDataDirectory+'/'+ModuleFolder
   
    TestResultEnvironmentInstance.FinalModuleResultsPath = FinalModuleResultsPath 

    if not NeedsToBeAnalyzed(TestResultEnvironmentInstance.FinalModuleResultsPath ,ModuleInformation):
        return
    
    ModuleTestResult = GetModuleTestResult(TestResultEnvironment,FinalModuleResultsPath,ModuleInformation)
    
    CreateApacheWebserverConfiguration(FinalModuleResultsPath)
    
    print 'Working on: ',ModuleInformation
    print ' -- '
    
    print '    Populating Data'
    ModuleTestResult.PopulateAllData()
    ModuleTestResult.WriteToDatabase() # needed before final output
    
    print '    Generating Final Output'
    ModuleTestResult.GenerateFinalOutput()
    ModuleTestResults.append(ModuleTestResult)
    CopyMD5File(TestResultEnvironmentInstance.FinalModuleResultsPath)
    print 'DONE' 
    pass


def AnalyseAllTestDataInDirectory(GlobalDataDirectory):
    for Folder in os.listdir(GlobalDataDirectory):
        absPath = GlobalDataDirectory+'/'+Folder
        if not os.path.isdir(absPath):
            continue
        ModuleInformationRaw = Folder.split('_')
        if len(ModuleInformationRaw) == 5:
            AnalyseTestData(ModuleInformationRaw,Folder)
            
def AnalyseSingleFullTest(singleFulltestPath):
    print 'analysing a single Fulltest at destination: "%s"'%args.singleFulltestPath 
    TestResultEnvironmentInstance.ModuleDataDirectory  = args.singleFulltestPath
    TestResultEnvironmentInstance.FinalModuleResultsPath = args.singleFulltestPath
    ModuleID = args.singleFulltestPath.split('/')[-1]
    TestDate = '%s'%int(time.time())
    TestType = 'singleFulltest'
    ModuleInformation = {
        'ModuleID': ModuleID,
        'TestDate': TestDate,
        'QualificationType': 'SingleFulltest',
    }
    FinalResultsPath = args.singleFulltestPath+'/FinalResults'+RevisionString
    ModuleTestResult = GetModuleTestResult(TestResultEnvironment, FinalResultsPath, ModuleInformation)
                # add apache webserver configuration for compressed svg images  
    CreateApacheWebserverConfiguration(FinalResultsPath)
    print 'Working on: ',ModuleInformation
    print ' -- '
    
    print '    Populating Data'
    ModuleTestResult.PopulateAllData()
    if args.DBUpload:
        ModuleTestResult.WriteToDatabase() # needed before final output
    
    print '    Generating Final Output'
    ModuleTestResult.GenerateFinalOutput()
    pass  

if not args.singleFulltestPath=='':
    AnalyseSingleFullTest(args.singleFulltestPath)
elif int(Configuration.get('SystemConfiguration', 'GenerateResultData')):
    AnalyseAllTestDataInDirectory(GlobalDataDirectory)
    
ModuleResultOverviewObject = ModuleResultOverview.ModuleResultOverview(TestResultEnvironmentInstance)
ModuleResultOverviewObject.GenerateOverviewHTMLFile()
# TestResultEnvironmentInstance.ErrorList.append( {'test1':'bla'})
# print TestResultEnvironmentInstance.ErrorList
sys.exit(len(TestResultEnvironmentInstance.ErrorList))

