#!/usr/bin/env python
 # -*- coding: utf-8 -*-
from AbstractClasses import PresentationMaker, GeneralTestResult, TestResultEnvironment, ModuleResultOverview, GeneralProductionOverview, GetValuesForPresentation
import AbstractClasses.Helper.hasher as hasher
import argparse
# from AbstractClasses import Helper
import TestResultClasses.CMSPixel.QualificationGroup.QualificationGroup
from OverviewClasses.CMSPixel.ProductionOverview import ProductionOverview
from OverviewClasses.CMSPixel.ProductionOverview.ProductionOverviewPage.GradingOverview import GradingOverview
import os, time,shutil, sys,traceback
# import errno
import ConfigParser
import datetime
import subprocess

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
                    help = 'Forces refitting even if fit result files exist')
parser.add_argument('-p', '--production-overview', dest = 'production_overview', action = 'store_true', default = False,
                    help = 'Creates production overview page')
parser.add_argument('-new', '--new-folders-only', dest = 'no_re_analysis', action = 'store_true', default = False,
                    help = 'Do not analyze folder if it already exists in DB, even if MoReWeb version has changed')
parser.add_argument('-m', '--modules', dest = 'modules_list', default = '',
                    help = 'Comma separated list of modules which shall be analyzed')
parser.add_argument('-pres', '--make-presentation', dest = 'make_presentation', action = 'store_true', default = False,
                    help = 'Creates tex file and pdf with presentation, needs -p')
parser.add_argument('-tc', '--show-test-center', dest = 'show_test_center', action = 'store_true', default = False,
                    help = 'Show test-center in qualification list')
parser.add_argument('-i', '--include-path', dest = 'additional_include_path', metavar='PATH', default = '',
                    help = argparse.SUPPRESS)
parser.add_argument('-g', '--use-global-db', dest = 'use_global_db', action = 'store_true', default = False,
                    help = argparse.SUPPRESS)

parser.add_argument('-C', '--csv', dest = 'output_csv', action = 'store_true', default = False,
                    help = argparse.SUPPRESS)
parser.add_argument('-ps', '--production-overview-single', dest = 'production_overview_single', default = '',
                    help = argparse.SUPPRESS)


parser.set_defaults(DBUpload=True)
args = parser.parse_args()
verbose = args.verbose

# allows to import PixelDB module from a different location
if args.additional_include_path and len(args.additional_include_path) > 0:
    AdditionalIncludePaths = args.additional_include_path.split(';')
    for AdditionalIncludePath in AdditionalIncludePaths:
        if verbose:
            print "try adding additional python module include path: '%s'"%AdditionalIncludePath
        try:
            sys.path.append(AdditionalIncludePath)
            if verbose:
                print "ok."
        except:
            if verbose:
                print "failed."


import AbstractClasses.Helper.ROOTConfiguration as ROOTConfiguration


ROOTConfiguration.initialise_ROOT()
Configuration = ConfigParser.ConfigParser()

if not os.path.isfile('Configuration/Paths.cfg'):
    print "error: The config file 'Configuration/Paths.cfg' was not found, copy it from 'Configuration/Paths.cfg.default' and adjust the paths!"
    exit()


if not os.path.isfile('Configuration/ProductionOverview.cfg'):
    print "info: The config file 'Configuration/ProductionOverview.cfg' was not found, it will be automatically created with default settings!"
    try:
        shutil.copy('Configuration/ProductionOverview.cfg.default', 'Configuration/ProductionOverview.cfg')
        print " => done!"
    except:
        print " => failed! try to create 'Configuration/ProductionOverview.cfg' manually and run MoReWeb again!"
        exit()

Configuration.read([
    'Configuration/GradingParameters.cfg',
    'Configuration/SystemConfiguration.cfg',
    'Configuration/Paths.cfg',
    'Configuration/ModuleInformation.cfg',
    'Configuration/ProductionOverview.cfg'
    ])

if os.path.isfile('Configuration/UserConfiguration.cfg'):
    Configuration.read(['Configuration/UserConfiguration.cfg'])

if args.use_global_db:
    Configuration.set('SystemConfiguration', 'UseGlobalDatabase', '1')

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
    try:
        os.makedirs(GlobalFinalResultsPath)
    except: #it could be created by another instance running in parallel
        if not os.path.exists(GlobalFinalResultsPath):
            raise
        else:
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
    if 'Not a git repository' in MoReWebVersion:
        MoReWebVersion = 'MoReWeb version not detectable, no git repository'
    TestResultEnvironmentInstance.MoReWebVersion = MoReWebVersion

if MoReWebBranch:
    if 'Not a git repository' in MoReWebBranch:
        MoReWebBranch = '-'
    TestResultEnvironmentInstance.MoReWebBranch = MoReWebBranch

if args.refit:
    TestResultEnvironmentInstance.Configuration['Fitting']['refit'] = True

if 'SystemConfiguration' not in TestResultEnvironmentInstance.Configuration:
    TestResultEnvironmentInstance.Configuration['SystemConfiguration'] = {}

if args.show_test_center:
    TestResultEnvironmentInstance.Configuration['SystemConfiguration']['show_test_center'] = True
else:
    TestResultEnvironmentInstance.Configuration['SystemConfiguration']['show_test_center'] = False


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

    if len(args.modules_list) > 0:
        ModulesList = [x.strip().upper() for x in args.modules_list.replace(';',',').split(',')]
        if ModuleInformation['ModuleID'].upper() in ModulesList:
            print 'analyse folder '+ FinalModuleResultsPath +'\n'
            return True
        else:
            print 'do not analyse folder '+ FinalModuleResultsPath +'\n'
            return False

    if os.path.exists(md5FileName):
        if verbose: print 'md5 sum exists %s'%md5FileName
        bSameFiles = hasher.compare_two_files('checksum.md5',md5FileName)
        if not Configuration.getboolean('SystemConfiguration','UseGlobalDatabase'):
            if args.no_re_analysis:
                # if -new parameter is specified, check if there if a file with same date or even a newer file in db
                bExistInDB = TestResultEnvironmentInstance.existInDB(ModuleInformation['ModuleID'],ModuleInformation['QualificationType'],ModuleInformation['TestDate'])
            else:
                bExistInDB = TestResultEnvironmentInstance.existInDB(ModuleInformation['ModuleID'],ModuleInformation['QualificationType'])
            if verbose: print 'check if Module exists: %s'%bExistInDB
        else:
            if verbose: print 'use Global DataBase: ',Configuration.get('SystemConfiguration','UseGlobalDatabase')
            bExistInDB = False
        if verbose: print 'same file: %s / exists in DB: %s'%(bSameFiles,bExistInDB)
        if (bSameFiles or args.no_re_analysis) and bExistInDB:
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

    ModuleIdentifier = ModuleInformation['ModuleID'] + '-' + ModuleInformation['QualificationType'] + '-' + ModuleInformation['TestDate']
    TestResultEnvironmentInstance.ModulesAnalyzed.append(ModuleIdentifier)
    print 'Working on: ',ModuleInformation
    print ' -- '

    print '    Populating Data'
    ModuleTestResult.PopulateAllData()
    WriteToDBSuccess = ModuleTestResult.WriteToDatabase() # needed before final output

    if WriteToDBSuccess:
        TestResultEnvironmentInstance.ModulesInsertedIntoDB.append(ModuleIdentifier)

    print '    Generating Final Output'
    ModuleTestResult.GenerateFinalOutput()
    ModuleTestResults.append(ModuleTestResult)
    CopyMD5File(TestResultEnvironmentInstance.FinalModuleResultsPath)
    print '    Clean up'
    try:
        ModuleTestResult.CleanUp()
    except:
        pass

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
    Folders = os.listdir(GlobalDataDirectory)
    Folders.sort()
    print "FOLDERS:"
    print Folders
    FoldersToBeAnalyzed = []

    for Folder in Folders:

        absPath = GlobalDataDirectory+'/'+Folder
        if not os.path.isdir(absPath):
            continue

        ModuleInformationRaw = Folder.split('_')
        if len(ModuleInformationRaw) >= 5:
            ModuleInformation = extractModuleInformation(ModuleInformationRaw)

            if not args.singleQualificationPath == '':
                TestResultEnvironmentInstance.ModuleDataDirectory = Folder
                FinalModuleResultsPath = GetFinalModuleResultsPath(Folder)
            else:
                FinalModuleResultsPath = GetFinalModuleResultsPath(Folder)
                TestResultEnvironmentInstance.ModuleDataDirectory = GlobalDataDirectory+'/'+Folder
            TestResultEnvironmentInstance.FinalModuleResultsPath = FinalModuleResultsPath

            if NeedsToBeAnalyzed(TestResultEnvironmentInstance.FinalModuleResultsPath ,ModuleInformation):
                FoldersToBeAnalyzed.append(Folder)

    print "\x1b[34mINFO: %d folder%s found that needs to be analyzed!\x1b[0m"%(len(FoldersToBeAnalyzed), 's' if len(FoldersToBeAnalyzed)!=1 else '')
    Counter = 1
    for Folder in FoldersToBeAnalyzed:
        ModuleInformationRaw = Folder.split('_')
        print "\x1b[34mINFO: Analyzing folder %d/%d (%s %s)\x1b[0m"%(Counter, len(FoldersToBeAnalyzed),ModuleInformationRaw[1],ModuleInformationRaw[0])
        AnalyseTestData(ModuleInformationRaw,Folder)
        Counter += 1

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
            try:
                TestDate = datetime.datetime.fromtimestamp(int(Row['TestDate'])).strftime('%Y-%m-%d %H:%M:%S')
            except:
                TestDate = "INVALID: " + repr(Row['TestDate'])
            print " ", "\x1b[31m", ("%d"%RowID).ljust(6), "\x1b[0m", TestDate.ljust(25), Row['QualificationType'].ljust(30), Row['TestType'].ljust(30), ("%s"%Row['Grade']).ljust(3), ("%s"%Row['Comments']).ljust(30)
            RowID += 1

        RowIDs = raw_input("Select rows (separated by comma): ")
        if RowIDs.lower().strip() == 'all':
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
        else:
            RowIDsList = [int(x.strip()) for x in RowIDs.split(',')]
            for RowID in RowIDsList:
                if Rows[RowID]:
                    Row = Rows[RowID]
                    try:
                        TestDate = datetime.datetime.fromtimestamp(int(Row['TestDate'])).strftime('%Y-%m-%d %H:%M:%S')
                    except:
                        TestDate = "INVALID: " + repr(Row['TestDate'])
                    print "delete? ", ("%d"%RowID), TestDate, Row['QualificationType'], Row['TestType'], ("%s"%Row['Grade']), ("%s"%Row['Comments'])
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

# test analysis
if not args.deleterow and not args.comment and not args.production_overview and not args.make_presentation:

    # prepare test analysis
    #  database migrations
    

    # run test analysis
    if not args.singleFulltestPath=='':
        AnalyseSingleFullTest(args.singleFulltestPath)
    elif not args.singleQualificationPath=='':
        AnalyseSingleQualification(args.singleQualificationPath)
    elif not args.bareModuletestPath=='':
        AnalyseBareModuleTest(args.bareModuletestPath)
    elif int(Configuration.get('SystemConfiguration', 'GenerateResultData')):
        AnalyseAllTestDataInDirectory(GlobalDataDirectory)


# production overview page
ModuleResultOverviewObject = ModuleResultOverview.ModuleResultOverview(TestResultEnvironmentInstance)
ModuleResultOverviewObject.GenerateOverviewHTMLFile()

if args.production_overview:
    print "production overview:"
    if len(args.production_overview_single) > 0:
        SingleSubtest = [x.strip() for x in args.production_overview_single.replace(';',',').split(',')]
        print "produce plots only for following subtests:"
        print "-%s"%SingleSubtest
    else:
        SingleSubtest = None
    ProductionOverviewObject = ProductionOverview.ProductionOverview(TestResultEnvironmentObject=TestResultEnvironmentInstance, SingleSubtest=SingleSubtest, Verbose=args.verbose)
    ProductionOverviewObject.GenerateOverview()

    if args.make_presentation:
        print "presentation maker: collecting data..."
        Summary = PresentationMaker.MakeProductionSummary()
        GetInfo = GetValuesForPresentation.ModuleSummaryValues(TestResultEnvironmentInstance)
        grades = GetInfo.MakeArray(GlobalOverviewPath)
        print "presentation maker: write tex file..."
        try:
            Summary.MakeTexFile(grades)
            print "done."
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            # Start red color
            sys.stdout.write("\x1b[31m")
            sys.stdout.flush()
            # Print error message
            print "Could not produce tex file for Presentation!"
            # Print traceback
            traceback.print_exception(exc_type, exc_obj, exc_tb)
            # Stop red color
            sys.stdout.write("\x1b[0m")
            sys.stdout.flush()


# CSV output
if args.output_csv:
    print "CSV output"
    print "-"*80
    if TestResultEnvironmentInstance.Configuration['Database']['UseGlobal']:
        print "\x1b[31merror: CSV export is not supported for global database!\x1b[0m"
    else:
        TestResultEnvironmentInstance.LocalDBConnectionCursor.execute(
            'SELECT * FROM ModuleTestResults ORDER BY ModuleID ASC,TestType ASC,TestDate ASC'
        )
        Rows = TestResultEnvironmentInstance.LocalDBConnectionCursor.fetchall()

        ModuleData = {}
        GradeOrdering = {'M': 0, 'A':1, 'B':2, 'C':3, 'X':9999}

        for Row in Rows:
            ModuleID = Row['ModuleID']

            # add new modules
            if ModuleID not in ModuleData:
                ModuleData[ModuleID] = {'Grade': 'M', 'FullQualificationGrade': None, 'XrayGrade': None,  'LeakageCurrent': -1, 'PixelDefects': -1}

            # add FullQualification data
            if Row['QualificationType'] == 'FullQualification':
                Grade = Row['Grade']
                if ModuleData[ModuleID]['FullQualificationGrade'] is None:
                    ModuleData[ModuleID]['FullQualificationGrade'] = Grade
                PixelDefects = int(Row['PixelDefects']) if Row['PixelDefects'] else -1

                # grade, if worse
                if Grade in GradeOrdering:
                    if GradeOrdering[Grade] > GradeOrdering[ModuleData[ModuleID]['Grade']]:
                        ModuleData[ModuleID]['Grade'] = Grade
                    print "worst:",ModuleData[ModuleID]['FullQualificationGrade']
                    if GradeOrdering[Grade] > GradeOrdering[ModuleData[ModuleID]['FullQualificationGrade']]:
                        ModuleData[ModuleID]['FullQualificationGrade'] = Grade

                # number of defects, if higher
                if PixelDefects > ModuleData[ModuleID]['PixelDefects']:
                    ModuleData[ModuleID]['PixelDefects'] = PixelDefects

                # leakage current for 17 degrees
                if Row['Temperature'] and int(float(Row['Temperature'])) == 17:
                    try:
                        LeakageCurrent = float(Row['CurrentAtVoltage150V'])
                        if LeakageCurrent > ModuleData[ModuleID]['LeakageCurrent']:
                            ModuleData[ModuleID]['LeakageCurrent'] = LeakageCurrent
                    except:
                        pass

            # add X-ray data
            if Row['TestType'] == 'XRayHRQualification':
                Grade = Row['Grade']
                ModuleData[ModuleID]['XrayGrade'] = Grade
                # grade, if worse
                if Grade and Grade in GradeOrdering:
                    if GradeOrdering[Grade] > GradeOrdering[ModuleData[ModuleID]['Grade']]:
                        ModuleData[ModuleID]['Grade'] = Grade

        CSVPath = GlobalOverviewPath + '/ModuleResultDB.csv'
        with open(CSVPath, 'w') as csvfile:
            for ModuleID, Data in ModuleData.iteritems():
                CSVLine = "%s, %s, %s, %s, %d, %e\n"%(ModuleID, Data['Grade'], Data['FullQualificationGrade'], Data['XrayGrade'], Data['PixelDefects'], Data['LeakageCurrent'])
                csvfile.write(CSVLine)
                print CSVLine,

        print "-"*80

'''
            self.TestResultEnvironmentObject.ErrorList.append(
                {'ModuleID': self.Attributes['TestedObjectID'] if 'TestedObjectID' in self.Attributes else '',
                 'ModulePath': self.ModulePath,
                 'ErrorCode': inst,
                 'File': exc_tb.tb_frame.f_code.co_filename,
                 'Line': exc_tb.tb_lineno,
                 'FinalResultsStoragePath': self.FinalResultsStoragePath}
                # 'FinalResultsStoragePath':i['TestResultObject'].FinalResultsStoragePath}
'''

# display error list
print '\nErrorList:'
ModulePath = ''
ModuleID = ''
for i in TestResultEnvironmentInstance.ErrorList:
    if 'ModuleID' in i and i['ModuleID'] != ModuleID:
        print (i['ModuleID'] if len(i['ModuleID']) > 0 else 'MODULE') + ':'
        ModulePath = ''
        ModuleID = i['ModuleID']
    if 'ModulePath' in i and i['ModulePath'] != ModulePath:
        print "  %s"%i['ModulePath']
        ModulePath = i['ModulePath']
    ColumnWidth = 10
    if 'Message' in i:
        print "    %s%s"%('ERROR: '.ljust(ColumnWidth), i['Message'])
    else:
        print "    %s%s"%('ERROR: '.ljust(ColumnWidth), i['ErrorCode'] if 'ErrorCode' in i else '')

    print "    %s%s"%('in ', i['File'] if 'File' in i else '')
    print "    %s%s"%('PATH: '.ljust(ColumnWidth), i['FinalResultsStoragePath'] if 'FinalResultsStoragePath' in i else '')


ExitCode = -2

try:
    ModulesNotInsertedIntoDB = list(set(TestResultEnvironmentInstance.ModulesAnalyzed) - set(TestResultEnvironmentInstance.ModulesInsertedIntoDB))
except:
    ModulesNotInsertedIntoDB = []

if TestResultEnvironmentInstance.Configuration['Database']['UseGlobal']:

    if len(ModulesNotInsertedIntoDB) == 0 and len(TestResultEnvironmentInstance.ModulesInsertedIntoDB) > 0:
        ExitCode = 0
    else:
        ExitCode = len(TestResultEnvironmentInstance.ErrorList)

else:
    ExitCode = len(TestResultEnvironmentInstance.ErrorList)

try:
    if len(ModulesNotInsertedIntoDB) > 0:
        print 'Modules not inserted into DB: %s'%','.join(ModulesNotInsertedIntoDB)

        # if there was no error with processing
        if ExitCode == 0:
            # indicate there was an error with insertion
            ExitCode = 999
except:
    pass

if len(ModulesNotInsertedIntoDB) < 1 and len(TestResultEnvironmentInstance.ModulesInsertedIntoDB) < 1:
    print "Nothing to be inserted!"
    ExitCode = 404

print 'inserted: ', TestResultEnvironmentInstance.ModulesInsertedIntoDB
print 'failed: ', ModulesNotInsertedIntoDB
print 'Exit code: %d'%ExitCode

sys.exit(ExitCode)

