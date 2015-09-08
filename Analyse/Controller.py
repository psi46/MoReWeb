#!/usr/bin/env python
 # -*- coding: utf-8 -*-
from AbstractClasses import GeneralTestResult, TestResultEnvironment, ModuleResultOverview, GeneralProductionOverview
import AbstractClasses.Helper.hasher as hasher
import argparse
# from AbstractClasses import Helper
import TestResultClasses.CMSPixel.QualificationGroup.QualificationGroup
from OverviewClasses.CMSPixel.ProductionOverview import ProductionOverview
import os, time,shutil, sys
# import errno
import ConfigParser
import datetime

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
parser.add_argument('-c', '--comment', dest = 'comment', action = 'store_true', default = False,
                    help = 'Add a comment to a local db row.')
parser.add_argument('-d', '--delete-row', dest = 'deleterow', action = 'store_true', default = False,
                    help = 'Let you select a row in the local database to delete.')
parser.add_argument('-r', '--refit', dest = 'refit', action = 'store_true', default = False,
                    help = 'Forces refitting even if files exist')
parser.add_argument('-p', '--production-overview', dest = 'production_overview', action = 'store_true', default = False,
                    help = 'Creates production overview page in the end')

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
    'Configuration/ModuleInformation.cfg',
    'Configuration/ProductionOverview.cfg'
    ])

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
    try :
	    os.makedirs(GlobalFinalResultsPath)
    except: #it could be created by another instance running in parallel
	    if not os.path.exists(GlobalFinalResultsPath) :
			raise
	    else :
		print "Kind of magic, they made the dir for me while I was checking" 

SQLiteDBPath = GlobalOverviewPath + '/ModuleResultDB.sqlite'
ModuleVersion = int(Configuration.get('ModuleInformation', 'ModuleVersion'))

TestType = Configuration.get('TestType','TestType')

TestResultEnvironmentInstance = TestResultEnvironment.TestResultEnvironment(Configuration)
TestResultEnvironmentInstance.SQLiteDBPath = SQLiteDBPath
TestResultEnvironmentInstance.GlobalOverviewPath = GlobalOverviewPath
TestResultEnvironmentInstance.OpenDBConnection()
TestResultEnvironmentInstance.GlobalDataDirectory = GlobalDataDirectory

MoReWebVersion = None
try:
    MoReWebVersion = subprocess.check_output(["git", "describe"])
except:
    try:
        import commands
        MoReWebVersion = commands.getstatusoutput('git describe')[1]
    except:
        pass

MoReWebBranch = None
try:
    MoReWebBranch = subprocess.check_output(["git", "rev-parse --abbrev-ref HEAD"])
except:
    try:
        import commands
        MoReWebBranch = commands.getstatusoutput('git rev-parse --abbrev-ref HEAD')[1]
    except:
        pass

if MoReWebVersion:
    TestResultEnvironmentInstance.MoReWebVersion = MoReWebVersion

if MoReWebBranch:
    TestResultEnvironmentInstance.MoReWebBranch = MoReWebBranch


if args.refit:
    TestResultEnvironmentInstance.Configuration['Fitting']['refit'] = True

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

# allows to add comments to local db file
if args.comment:
    ModuleID = raw_input("Enter module ID (eg. M1234): ")

    if TestResultEnvironmentInstance.Configuration['Database']['UseGlobal']:
        print "--comment option not supported for global db"
    else:
        AdditionalWhere = ''
        if ModuleID:
            AdditionalWhere += ' AND ModuleID=:ModuleID '
        TestResultEnvironmentInstance.LocalDBConnectionCursor.execute(
            'SELECT * FROM ModuleTestResults '+
            'WHERE 1=1 '+
            AdditionalWhere+
            'ORDER BY ModuleID ASC,TestType ASC,TestDate ASC ',
            {
                'ModuleID':ModuleID
            }
        )
        Rows = TestResultEnvironmentInstance.LocalDBConnectionCursor.fetchall()

        print "Available qualifications for module %s:"%ModuleID
        print "  ", 'ID'.ljust(6), ' QualificationType'.ljust(30), 'TestType'.ljust(30), 'Grade'.ljust(3), 'Comments'.ljust(30)
        RowID = 0
        for Row in Rows:
            print " ", "\x1b[31m", ("%d"%RowID).ljust(6), "\x1b[0m", Row['QualificationType'].ljust(30), Row['TestType'].ljust(30), ("%s"%Row['Grade']).ljust(3), ("%s"%Row['Comments']).ljust(30)
            RowID += 1

        RowID = int(raw_input("Select row: "))
        if RowID >= 0 and RowID < len(Rows) and Rows[RowID]:
            print ""
            print "current comment: %s"%Rows[RowID]['Comments']

            Comments = raw_input("Enter new comment: ")
            result = TestResultEnvironmentInstance.LocalDBConnectionCursor.execute( 
                'UPDATE ModuleTestResults SET Comments = :Comments WHERE ModuleID = :ModuleID AND TestType = :TestType AND TestDate = :TestDate AND QualificationType = :QualificationType',
                {
                    'ModuleID': Rows[RowID]['ModuleID'],
                    'TestType': Rows[RowID]['TestType'],
                    'TestDate': Rows[RowID]['TestDate'],
                    'QualificationType': Rows[RowID]['QualificationType'],
                    'Comments': Comments
                }
            )
            if TestResultEnvironmentInstance.LocalDBConnection:
                TestResultEnvironmentInstance.LocalDBConnection.commit()
            else:
                print "no connection to local db!"

        else:
            print "row id not found!"


# allows to delete a row in local db file
if args.deleterow:
    print "First enter module ID and then select one of the existing rows to delete or type 'all' to delete all of them."
    ModuleID = raw_input("Enter module ID (eg. M1234): ")

    if TestResultEnvironmentInstance.Configuration['Database']['UseGlobal']:
        print "--delete option not supported for global db"
    else:
        AdditionalWhere = ''
        if ModuleID:
            AdditionalWhere += ' AND ModuleID=:ModuleID '
        TestResultEnvironmentInstance.LocalDBConnectionCursor.execute(
            'SELECT * FROM ModuleTestResults '+
            'WHERE 1=1 '+
            AdditionalWhere+
            'ORDER BY ModuleID ASC,TestType ASC,TestDate ASC ',
            {
                'ModuleID':ModuleID
            }
        )
        Rows = TestResultEnvironmentInstance.LocalDBConnectionCursor.fetchall()

        print "Available qualifications for module %s:"%ModuleID
        print "  ", 'ID'.ljust(6),  ' TestDate'.ljust(25),  'QualificationType'.ljust(30), 'TestType'.ljust(30), 'Grade'.ljust(3), 'Comments'.ljust(30)
        RowID = 0
        for Row in Rows:
            print " ", "\x1b[31m", ("%d"%RowID).ljust(6), "\x1b[0m", datetime.datetime.fromtimestamp(int(Row['TestDate'])).strftime('%Y-%m-%d %H:%M:%S').ljust(25), Row['QualificationType'].ljust(30), Row['TestType'].ljust(30), ("%s"%Row['Grade']).ljust(3), ("%s"%Row['Comments']).ljust(30)
            RowID += 1

        RowID = raw_input("Select row: ")
        if RowID.lower().strip() == 'all':
            print "delete module %s from local DB?"%ModuleID
            confirmation = raw_input("(y/N)")
            if confirmation.lower().strip() == 'y':
                result = TestResultEnvironmentInstance.LocalDBConnectionCursor.execute( 
                    'DELETE FROM ModuleTestResults WHERE ModuleID = :ModuleID',
                    {
                        'ModuleID': ModuleID,
                    }
                )
                if TestResultEnvironmentInstance.LocalDBConnection:
                    TestResultEnvironmentInstance.LocalDBConnection.commit()
                else:
                    print "no connection to local db!"
        elif int(RowID) >= 0 and int(RowID) < len(Rows) and Rows[int(RowID)]:
            RowID = int(RowID)
            Row = Rows[RowID]
            print "delete? ", ("%d"%RowID), datetime.datetime.fromtimestamp(int(Row['TestDate'])).strftime('%Y-%m-%d %H:%M:%S'), Row['QualificationType'], Row['TestType'], ("%s"%Row['Grade']), ("%s"%Row['Comments'])
            confirmation = raw_input("(y/N)")
            if confirmation.lower().strip() == 'y':
                result = TestResultEnvironmentInstance.LocalDBConnectionCursor.execute( 
                    'DELETE FROM ModuleTestResults WHERE ModuleID = :ModuleID AND TestType = :TestType AND TestDate = :TestDate AND QualificationType = :QualificationType',
                    {
                        'ModuleID': Rows[RowID]['ModuleID'],
                        'TestType': Rows[RowID]['TestType'],
                        'TestDate': Rows[RowID]['TestDate'],
                        'QualificationType': Rows[RowID]['QualificationType']
                    }
                )
                if TestResultEnvironmentInstance.LocalDBConnection:
                    TestResultEnvironmentInstance.LocalDBConnection.commit()
                else:
                    print "no connection to local db!"

        else:
            print "row id not found!"

ModuleResultOverviewObject = ModuleResultOverview.ModuleResultOverview(TestResultEnvironmentInstance)
ModuleResultOverviewObject.GenerateOverviewHTMLFile()

if args.production_overview:
    print "production overview:"
    ProductionOverviewObject = ProductionOverview.ProductionOverview(TestResultEnvironmentInstance)
    ProductionOverviewObject.GenerateOverview()

# TestResultEnvironmentInstance.ErrorList.append( {'test1':'bla'})
print '\nErrorList:'
for i in TestResultEnvironmentInstance.ErrorList:
    print i
    print '\t - %s: %s'%(i['ModulePath'],i['ErrorCode'])
sys.exit(len(TestResultEnvironmentInstance.ErrorList))

