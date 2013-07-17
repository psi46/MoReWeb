# -*- coding: utf-8 -*-
'''
Program	: MORE-Web 
 Author	: Esteban Marin - estebanmarin@gmx.ch
 Version	: 2.1
 Release Date	: 2013-05-30
'''
from AbstractClasses import GeneralTestResult, TestResultEnvironment, ModuleResultOverview

import TestResultClasses.CMSPixel.ModuleTestGroup.TestResult
import os, time
import ROOT
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
SQLiteDBPath = OverviewPath + '/ModuleResultDB.sqlite'

ModuleVersion = int(Configuration.get('ModuleInformation', 'ModuleVersion'))

TestResultEnvironmentInstance = TestResultEnvironment.TestResultEnvironment(Configuration)
TestResultEnvironmentInstance.SQLiteDBPath = SQLiteDBPath
TestResultEnvironmentInstance.OverviewPath = OverviewPath
TestResultEnvironmentInstance.OpenDBConnection()
TestResultEnvironmentInstance.TestResultsBasePath = TestResultDirectory

ModuleTestResults = []
if int(Configuration.get('SystemConfiguration', 'GenerateResultData')):
	for Folder in os.listdir(TestResultDirectory):
        if os.path.isdir(Folder) == False:
            continue
		if not Folder.find('.') == 0:
			ModuleInformationRaw = Folder.split('_')
			if len(ModuleInformationRaw) == 5:
				ModuleInformation = {
					'ModuleID': ModuleInformationRaw[0],
					'TestDate': ModuleInformationRaw[4],
					'TestType': ModuleInformationRaw[1]
				}
				
				
				TestResultEnvironmentInstance.TestResultsPath = TestResultDirectory+'/'+Folder
				
				FinalResultsPath = TestResultDirectory+'/'+Folder+'/FinalResults'
				if not os.path.exists(FinalResultsPath):
					os.makedirs(FinalResultsPath)
				
				
				ModuleTestResult = TestResultClasses.CMSPixel.ModuleTestGroup.TestResult.TestResult(
					TestResultEnvironmentInstance, 
					None, 
					'TestResultClasses.CMSPixel.ModuleTestGroup', 
					FinalResultsPath,
					{
						'TestDate':ModuleInformation['TestDate'],
						'TestedObjectID':ModuleInformation['ModuleID'],
						'ModuleID':ModuleInformation['ModuleID'],
						'ModuleVersion':ModuleVersion,
						'ModuleType':'a',
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
	
ModuleResultOverviewObject = ModuleResultOverview.ModuleResultOverview(TestResultEnvironmentInstance)
ModuleResultOverviewObject.GenerateOverviewHTMLFile()
