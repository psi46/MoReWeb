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


#arg parse to analyse a single Fulltest
parser = argparse.ArgumentParser(description='MORE web Controller: an analysis software for CMS pixel modules and ROCs')
parser.add_argument('-FT','--singleFulltest',dest='singleFulltestPath',metavar='PATH',
                     help='option which can be used to analyse a single Fulltest, as the second argument needs the path where the single fulltest data are stored',
                     default='')
parser.add_argument('-M','--ModuleVersion',dest='ModuleVersion',metavar='VERSION',
                    help='option to choose which module version is analysed [singleROC =3, Module ={1,2}]',default='')
parser.add_argument('-noDB','--noDBupload',dest='DBUpload',action='store_false',
                    help='deactivates upload to DB within this analysis session')
parser.add_argument('-withDB','--withDBupload',dest='DBUpload',action='store_true',
                    help='activates upload to DB within this analysis session [default]')
parser.set_defaults(DBUpload=True)
args = parser.parse_args()


import TestResultClasses.CMSPixel.QualificationGroup.TestResult
import os, time,shutil
import ROOT
import time
import ConfigParser

# Suppress "info"-level notices from TCanvas that it has saved a .png
# see root/core/base/inc/TError.h for information on error levels
ROOT.gErrorIgnoreLevel = 1001

ROOT.gROOT.SetBatch(True)
Configuration = ConfigParser.ConfigParser()
Configuration.read([
    'Configuration/GradingParameters.cfg', 
    'Configuration/SystemConfiguration.cfg', 
    'Configuration/Paths.cfg',
    'Configuration/ModuleInformation.cfg'])


TestResultDirectory = Configuration.get('Paths', 'TestResultDirectory')
OverviewPath = Configuration.get('Paths', 'OverviewPath')
if Configuration.has_option('Paths',''):
    FinalResultDirectory = Configuration.get('Paths','FinalResultsPath')
else:
    FinalResultDirectory = ''
if FinalResultDirectory!= '' and not os.path.exists(FinalResultDirectory):
    os.makedirs(FinalResultDirectory)
SQLiteDBPath = OverviewPath + '/ModuleResultDB.sqlite'
ModuleVersion = int(Configuration.get('ModuleInformation', 'ModuleVersion'))
if not args.ModuleVersion == '':
    ModuleVersion = int(args.ModuleVersion)
print ModuleVersion
     
TestType = Configuration.get('TestType','TestType')


TestResultEnvironmentInstance = TestResultEnvironment.TestResultEnvironment(Configuration)
TestResultEnvironmentInstance.SQLiteDBPath = SQLiteDBPath
TestResultEnvironmentInstance.OverviewPath = OverviewPath
TestResultEnvironmentInstance.OpenDBConnection()
TestResultEnvironmentInstance.TestResultsBasePath = TestResultDirectory

hasher.create_hash_file_directory('checksum.md5','.')

ModuleTestResults = []
if not args.singleFulltestPath=='':
    print 'analysing a single Fulltest at destination: "%s"'%args.singleFulltestPath 
    TestResultEnvironmentInstance.TestResultsPath  = args.singleFulltestPath
    TestResultEnvironmentInstance.FinalResultsPath = args.singleFulltestPath
    ModuleID = args.singleFulltestPath.split('/')[-1]
    TestDate = '%s'%int(time.time())
    TestType = 'singleFulltest'
    ModuleInformation = {
        'ModuleID': ModuleID,
        'TestDate': TestDate,
        'QualificationType': 'SingleFulltest',
    }
    FinalResultsPath = args.singleFulltestPath+'/FinalResults'
    ModuleTestResult = TestResultClasses.CMSPixel.QualificationGroup.TestResult.TestResult(
                    TestResultEnvironmentInstance, 
                    None, 
                    'TestResultClasses.CMSPixel.QualificationGroup', 
                    FinalResultsPath,
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
                # add apache webserver configuration for compressed svg images  
    f = open(FinalResultsPath + '/.htaccess', 'w')
    f.write('''
AddType image/svg+xml svg
AddType image/svg+xml svgz
AddEncoding x-gzip .svgz
    ''')
    f.close()
    
    print 'Working on: ',ModuleInformation
    print ' -- '
    
    print '    Populating Data'
    ModuleTestResult.PopulateAllData()
    if args.DBUpload:
        ModuleTestResult.WriteToDatabase() # needed before final output
    
    print '    Generating Final Output'
    ModuleTestResult.GenerateFinalOutput()
    pass  
elif int(Configuration.get('SystemConfiguration', 'GenerateResultData')):
    for Folder in os.listdir(TestResultDirectory):
        absPath = TestResultDirectory+'/'+Folder
        if not os.path.isdir(absPath):
            continue
        if not Folder.find('.') == 0:
            ModuleInformationRaw = Folder.split('_')
            if len(ModuleInformationRaw) == 5:
                ModuleInformation = {
                    'ModuleID': ModuleInformationRaw[0],
                    'TestDate': ModuleInformationRaw[4],
                    'QualificationType': ModuleInformationRaw[1]
                }
                
                if FinalResultDirectory=='':
                    FinalResultsPath = TestResultDirectory+'/'+Folder+'/FinalResults'
                else:
                    FinalResultsPath = FinalResultDirectory+'/'+Folder
                                    
                TestResultEnvironmentInstance.TestResultsPath = TestResultDirectory+'/'+Folder
                TestResultEnvironmentInstance.FinalResultsPath = FinalResultsPath 
                #TestResultEnvironmentInstance.FinalResultsPath = TestResultDirectory+'/'+Folder
                
                
                if not os.path.exists(FinalResultsPath):
                    os.makedirs(FinalResultsPath)

                md5FileName= FinalResultsPath+'/'+ 'checksum.md5'

                if os.path.exists(md5FileName):
                    print 'md5 sum exists %s'%md5FileName
                    bSameFiles = hasher.compare_two_files('checksum.md5',md5FileName)
                    if Configuration.get('SystemConfiguration','UseGlobalDatabase') == 0:
                        bExistInDB = TestResultEnvironmentInstance.existInDB(ModuleInformation['ModuleID'],ModuleInformation['QualificationType'])
                    else:
                        bExistInDB = false
                    if bSameFiles and bExistInDB:
                        print 'do not analyse folder '+ Folder
                        continue
                
                
                ModuleTestResult = TestResultClasses.CMSPixel.QualificationGroup.TestResult.TestResult(
                    TestResultEnvironmentInstance, 
                    None, 
                    'TestResultClasses.CMSPixel.QualificationGroup', 
                    FinalResultsPath,
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
                # add apache webserver configuration for compressed svg images  
                f = open(FinalResultsPath + '/.htaccess', 'w')
                f.write('''
AddType image/svg+xml svg
AddType image/svg+xml svgz
AddEncoding x-gzip .svgz
                ''')
                f.close()
                
                print 'Working on: ',ModuleInformation
                print ' -- '
                
                print '    Populating Data'
                ModuleTestResult.PopulateAllData()
                ModuleTestResult.WriteToDatabase() # needed before final output
                
                print '    Generating Final Output'
                ModuleTestResult.GenerateFinalOutput()
                ModuleTestResults.append(ModuleTestResult)
                print 'copyfile checksum'
                shutil.copyfile('checksum.md5',md5FileName)
    
ModuleResultOverviewObject = ModuleResultOverview.ModuleResultOverview(TestResultEnvironmentInstance)
ModuleResultOverviewObject.GenerateOverviewHTMLFile()
