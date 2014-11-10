#!/usr/bin/env python
 # -*- coding: utf-8 -*-
from AbstractClasses import GeneralTestResult, TestResultEnvironment, ModuleResultOverview
import AbstractClasses.Helper.hasher as hasher
import argparse
# from AbstractClasses import Helper
import TestResultClasses.CMSPixel.QualificationGroup.QualificationGroup
import os, time,shutil, sys
# import errno
import ConfigParser

#arg parse to analyse a single Fulltest
parser = argparse.ArgumentParser(description='MORE web Controller: an analysis software for CMS pixel modules and ROCs')
parser.add_argument('-FT','--singleFulltest',dest='singleFulltestPath',metavar='PATH',
                     help='option which can be used to analyse a single Fulltest, as the second argument needs the path where the single fulltest data are stored',
                     default='')
parser.add_argument('-BT','--bareModuletest',dest='bareModuletestPath',metavar='PATH',
                     help='option which can be used to analyse a bare Module Test, as the second argument needs the path where the single fulltest data are stored',
                     default='')


parser.add_argument('-FQ','--singleQualification',dest='singleQualificationPath',metavar='PATH',
                    help='option which activates an analysis of a single Qualification',
                    default='')
# parser.add_argument('-M','--ModuleVersion',dest='ModuleVersion',metavar='VERSION',
#                     help='option to choose which module version is analysed [singleROC =3, Module ={1,2}]',default='')
parser.add_argument('-noDB', '--noDBupload', dest = 'DBUpload', action = 'store_false', default = True,
                    help='deactivates upload to DB within this analysis session')
parser.add_argument('-v','--verbose',dest='verbose',action='store_true',default = False,
                    help='activates verbose mode')
parser.add_argument('-withDB','--withDBupload',dest='DBUpload',action='store_true',
                    help='activates upload to DB within this analysis session [default]')
parser.add_argument('-rev','--analysis-revision',dest='revision',metavar='REV',default = -1,
                    help='setting analysis revision number by hand to create an extra directory, alternative: Configuration/SystemConfiguration.cfg --> AnalysisRevision')
parser.add_argument('-norev','--no-revisionnumber',dest='norev',action='store_true',default=False,
                    help='deactivates the revsion sting with in the path')
parser.add_argument('-f', '--force', dest = 'force', action = 'store_true', default = False,
                    help = 'Forces runnig analysis even if checksums agree')
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
outputstring = 'MORE web analysis script, Revision number %s'%revisionNumber
if args.norev:
    outputstring += ', Revision number is not included in folder names'
print outputstring
if args.norev:
    RevisionString = ""
else:
    RevisionString = "-R%03d"%revisionNumber

if verbose:
    print 'RevisionString "%s"'%RevisionString
GlobalDataDirectory = Configuration.get('Paths', 'GlobalDataDirectory')
GlobalOverviewPath = Configuration.get('Paths', 'GlobalOverviewPath')
if Configuration.has_option('Paths','GlobalFinalResultsPath'):
    if args.norev:
        GlobalFinalResultsPath = Configuration.get('Paths','GlobalFinalResultsPath')
    else:
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
    if verbose:
        raw_input('AbsoluteOverviewPage %s. Please press enter.'%TestResultEnvironmentInstance.Configuration['OverviewHTMLLink'])

hasher.create_hash_file_directory('checksum.md5','.')

ModuleTestResults = []


def extractModuleInformation(ModuleInformationRaw):
    lenght = len(ModuleInformationRaw)
    type = '_'.join(ModuleInformationRaw[1: 1 + lenght - 4])
    return {
                    'ModuleID': ModuleInformationRaw[0],
                    'TestDate': ModuleInformationRaw[-1],
                    'QualificationType': ModuleInformationRaw[1]
                }

def GetFinalModuleResultsPath(ModuleFolder):
    if len(ModuleFolder.rstrip('/').split('/'))!=1:
        folder = ModuleFolder.rstrip('/')
        folders = folder.rsplit('/',1)
        ModuleFolder = folders[-1]
        ModuleFolderPath = folders[0]

    if GlobalFinalResultsPath=='':
        if args.singleQualificationPath == '':
            ModuleFolderPath = GlobalDataDirectory

        FinalModuleResultsPath = ModuleFolderPath+'/'+ModuleFolder+'/FinalResults'+RevisionString
    else:
        if RevisionString == '':
            FinalModuleResultsPath = GlobalFinalResultsPath+'/'+ModuleFolder
        else:
            FinalModuleResultsPath = GlobalFinalResultsPath+'/'+RevisionString[1:]+'/'+ModuleFolder
    if not os.path.exists(FinalModuleResultsPath):
        os.makedirs(FinalModuleResultsPath)
    return FinalModuleResultsPath

def NeedsToBeAnalyzed(FinalModuleResultsPath,ModuleInformation):
    if args.force == True:
        return True
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
    newModuleInformation = {
                'TestDate':ModuleInformation['TestDate'],
                'TestedObjectID':ModuleInformation['ModuleID'],
                'ModuleID':ModuleInformation['ModuleID'],
                'ModuleVersion':ModuleVersion,
                'ModuleType':'a',
                'TestType':TestType,
                'QualificationType': ModuleInformation['QualificationType']
            }
    if ModuleInformation.has_key('TestType'):
        newModuleInformation['TestType'] =  ModuleInformation['TestType']
    return TestResultClasses.CMSPixel.QualificationGroup.QualificationGroup.TestResult(
            TestResultEnvironmentInstance,
            ParentObject = None,
            InitialModulePath = 'TestResultClasses.CMSPixel.QualificationGroup',
            InitialFinalResultsStoragePath = FinalModuleResultsPath,
            InitialAttributes = newModuleInformation
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
    print 'AnalyseTestData',ModuleInformationRaw,ModuleFolder
    global final_result_directory
    print ModuleInformationRaw, ModuleFolder
    #,ModuleInformation
    ModuleInformation = extractModuleInformation(ModuleInformationRaw)

    if not args.singleQualificationPath == '':
        print 'singleQualification'
        TestResultEnvironmentInstance.ModuleDataDirectory = ModuleFolder
        FinalModuleResultsPath = GetFinalModuleResultsPath(ModuleFolder)

    else:
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


def AnalyseSingleQualification(Folder):
    print 'AnalyseSingleQualification "%s"'%Folder
    if not os.path.isdir(Folder):
        print '"%s" is not a directory ---> ABORT'%Folder
        TestResultEnvironmentInstance.ErrorList.append(
                       {'ModulePath':Folder,
                        'ErrorCode': -999,
                        'FinalResultsStoragePath':'unkown'
                        }
       )
        print TestResultEnvironmentInstance
        print 'ERROR'
        return
    Folder.rstrip('/')
    ModuleInformationRaw = Folder.rstrip('/').split('/')[-1]
    print ModuleInformationRaw
    ModuleInformationRaw = ModuleInformationRaw.split('_')
    print ModuleInformationRaw
    if len(ModuleInformationRaw) >= 5:
        AnalyseTestData(ModuleInformationRaw, Folder)

def AnalyseAllTestDataInDirectory(GlobalDataDirectory):
    for Folder in os.listdir(GlobalDataDirectory):
        absPath = GlobalDataDirectory+'/'+Folder
        if not os.path.isdir(absPath):
            continue
        ModuleInformationRaw = Folder.split('_')
        if len(ModuleInformationRaw) >= 5:
            AnalyseTestData(ModuleInformationRaw,Folder)

def AnalyseSingleFullTest(singleFulltestPath):
    print 'analysing a single Fulltest at destination: "%s"' % args.singleFulltestPath
    TestResultEnvironmentInstance.ModuleDataDirectory  = args.singleFulltestPath
    TestResultEnvironmentInstance.FinalModuleResultsPath = args.singleFulltestPath
    ModuleID = args.singleFulltestPath.split('/')[-1]
    TestDate = '%s'%int(time.time())
    TestType = 'singleFulltest'
    ModuleInformation = {
        'ModuleID': ModuleID,
        'TestDate': TestDate,
        'QualificationType': 'SingleFulltest',
        'TestType': 'singleFulltest'
    }
    FinalResultsPath = args.singleFulltestPath+'/FinalResults'+RevisionString
    ModuleTestResult = GetModuleTestResult(TestResultEnvironment, FinalResultsPath, ModuleInformation)
    print 'ModuleTestResult',ModuleTestResult
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

def AnalyseBareModuleTest(bareModuletestPath):
    print 'analysing a single Fulltest at destination: "%s"' % args.bareModuletestPath
    TestResultEnvironmentInstance.ModuleDataDirectory  = args.bareModuletestPath
    TestResultEnvironmentInstance.FinalModuleResultsPath = args.bareModuletestPath
    ModuleID = args.bareModuletestPath.split('/')[-1]
    TestDate = '%s'%int(time.time())
    TestType = 'bareModuletest'
    ModuleInformation = {
        'ModuleID': ModuleID,
        'TestDate': TestDate,
        'QualificationType': 'BareModuletest',
        'TestType': 'bareModuletest'
    }
    FinalResultsPath = args.bareModuletestPath+'/BareFinalResults'+RevisionString
    ModuleTestResult = GetModuleTestResult(TestResultEnvironment, FinalResultsPath, ModuleInformation)
    print 'ModuleTestResult',ModuleTestResult
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
elif not args.singleQualificationPath=='':
    AnalyseSingleQualification(args.singleQualificationPath)
elif not args.bareModuletestPath=='':
    AnalyseBareModuleTest(args.bareModuletestPath)
elif int(Configuration.get('SystemConfiguration', 'GenerateResultData')):
    AnalyseAllTestDataInDirectory(GlobalDataDirectory)

ModuleResultOverviewObject = ModuleResultOverview.ModuleResultOverview(TestResultEnvironmentInstance)
ModuleResultOverviewObject.GenerateOverviewHTMLFile()
# TestResultEnvironmentInstance.ErrorList.append( {'test1':'bla'})
print '\nErrorList:'
for i in TestResultEnvironmentInstance.ErrorList:
    print i
    print '\t - %s: %s'%(i['ModulePath'],i['ErrorCode'])
sys.exit(len(TestResultEnvironmentInstance.ErrorList))

