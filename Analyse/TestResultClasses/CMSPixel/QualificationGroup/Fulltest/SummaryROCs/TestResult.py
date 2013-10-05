# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import os

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Fulltest_SummaryROCs_TestResult'
        self.NameSingle='SummaryROCs'
        self.Title = 'Summary ROCs'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
        

        
    def PopulateResultData(self):
        self.ResultData['Table'] = {
           'HEADER':[
               [
                   'ROC',
                   'Total',
                   'Dead',
                   'Mask',
                   'Bumps',
                   'Trim(Bits)',
                   'Address',
                   'Noise',
                   'Thresh',
                   'Gain',
                   'Ped',
                   'Par1',
               ]
           ],
           'BODY':[],
           'FOOTER':[],
        }
        LinkHTMLTemplate = self.TestResultEnvironmentObject.HtmlParser.getSubpart(
           self.TestResultEnvironmentObject.OverviewHTMLTemplate,
           '###LINK###'
        )
        for i in self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResultDictList']:
           self.ResultData['Table']['BODY'].append(
               [
                   self.TestResultEnvironmentObject.HtmlParser.substituteMarkerArray(
                       LinkHTMLTemplate,
                       {
                           '###LABEL###':'Chip '+str(i['TestResultObject'].Attributes['ChipNo']),
                           '###URL###':os.path.relpath(i['TestResultObject'].FinalResultsStoragePath, self.ParentObject.FinalResultsStoragePath)+'/TestResult.html'
                       }
                   ),
                   i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['Total']['Value'],
                   i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nDeadPixel']['Value'],
                   i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nMaskDefect']['Value'],
                   i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nDeadBumps']['Value'],
                   i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nDeadTrimbits']['Value'],
                   i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nAddressProblems']['Value'],
                   i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nNoisy1Pixel']['Value'],
                   i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nThrDefect']['Value'],
                   i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nGainDefect']['Value'],
                   i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nPedDefect']['Value'],
                   i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nPar1Defect']['Value'],
               ]   
           )
