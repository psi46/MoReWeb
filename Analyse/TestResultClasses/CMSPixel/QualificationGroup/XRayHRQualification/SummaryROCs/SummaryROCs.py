# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import os

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Fulltest_XRayHRQualification_TestResult'
        self.NameSingle='SummaryROCs'
        self.Title = 'Summary ROCs'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
        

        
    def PopulateResultData(self):
      TableHeader = ['ROC','Grade']
      for Rate in self.ParentObject.Attributes['InterpolatedEfficiencyRates']:
        TableHeader.append('Eff {Rate}'.format(Rate=Rate))

      for Rate in self.ParentObject.Attributes['Rates']['HRData']:
        TableHeader.append('Rate "{Rate}"'.format(Rate=Rate))
        TableHeader.append('BB defect'.format(Rate=Rate))
        TableHeader.append('RO prob '.format(Rate=Rate))

      TableHeader.append('Unif. prob'.format(Rate=Rate))

      for Rate in self.ParentObject.Attributes['Rates']['HRSCurves']:
        TableHeader.append('Noise [e-] "{Rate}"'.format(Rate=Rate))

      self.ResultData['Table'] = {
         'HEADER': [TableHeader],
         'BODY':[],
         'FOOTER':[],
      }
      LinkHTMLTemplate = self.TestResultEnvironmentObject.HtmlParser.getSubpart(
         self.TestResultEnvironmentObject.OverviewHTMLTemplate,
         '###LINK###'
      )

      GradeBHTMLTemplate = "<span style='color:#f70;font-weight:bold;'>%s</span>"
      GradeCHTMLTemplate = "<span style='color:red;font-weight:bold;'>%s</span>"

      ChipsSubTestResult = self.ParentObject.ResultData['SubTestResults']['Chips']
      for i in ChipsSubTestResult.ResultData['SubTestResultDictList']:
        ChipNo = i['TestResultObject'].Attributes['ChipNo']

        TableRow = [
                 self.TestResultEnvironmentObject.HtmlParser.substituteMarkerArray(
                     LinkHTMLTemplate,
                     {
                         '###LABEL###':'Chip '+str(ChipNo),
                         '###URL###':os.path.relpath(i['TestResultObject'].FinalResultsStoragePath, self.ParentObject.FinalResultsStoragePath)+'/TestResult.html'
                     }
                 ), ChipsSubTestResult.ResultData['SubTestResults']['Chip%d'%ChipNo].ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['ROCGrade']['Value']
        ]

        RateIndex = 1
        for Rate in self.ParentObject.Attributes['InterpolatedEfficiencyRates']:
          Efficiency = float(ChipsSubTestResult.ResultData['SubTestResults']['Chip%d'%ChipNo].ResultData['SubTestResults']['EfficiencyInterpolation'].ResultData['KeyValueDictPairs']['InterpolatedEfficiency{Rate}'.format(Rate=Rate)]['Value'])
          if Efficiency < self.TestResultEnvironmentObject.GradingParameters['XRayHighRateEfficiency_max_allowed_loweff_B_Rate%d'%RateIndex]:
            TableRow.append(GradeCHTMLTemplate%("{Value:1.2f}".format(Value=Efficiency)))
          elif Efficiency < self.TestResultEnvironmentObject.GradingParameters['XRayHighRateEfficiency_max_allowed_loweff_A_Rate%d'%RateIndex]:
            TableRow.append(GradeBHTMLTemplate%("{Value:1.2f}".format(Value=Efficiency)))
          else:
            TableRow.append("{Value:1.2f}".format(Value=Efficiency))
          RateIndex += 1

        for Rate in self.ParentObject.Attributes['Rates']['HRData']:
          TableRow.append(float(ChipsSubTestResult.ResultData['SubTestResults']['Chip%d'%ChipNo].ResultData['SubTestResults']['HitMap_{Rate}'.format(Rate=Rate)].ResultData['KeyValueDictPairs']['RealHitrate']['Value']))
          BumpBondingDefects = int(ChipsSubTestResult.ResultData['SubTestResults']['Chip%d'%ChipNo].ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['BumpBondingDefects_{Rate}'.format(Rate=Rate)])
          
          if BumpBondingDefects >= self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_missing_xray_pixels_C']:
            TableRow.append(GradeCHTMLTemplate%("{Value:1.0f}".format(Value=BumpBondingDefects)))
          elif BumpBondingDefects >= self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_missing_xray_pixels_B']:
            TableRow.append(GradeBHTMLTemplate%("{Value:1.0f}".format(Value=BumpBondingDefects)))
          else:
            TableRow.append("{Value:1.0f}".format(Value=BumpBondingDefects))

          NonUniformEvents = int(ChipsSubTestResult.ResultData['SubTestResults']['Chip%d'%ChipNo].ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['NumberOfNonUniformEvents_{Rate}'.format(Rate=Rate)])
          if NonUniformEvents > 0:
            TableRow.append(GradeCHTMLTemplate%("{Value:1.0f}".format(Value=NonUniformEvents)))
          else:
            TableRow.append("{Value:1.0f}".format(Value=NonUniformEvents))

        NonUniformColumns = int(ChipsSubTestResult.ResultData['SubTestResults']['Chip%d'%ChipNo].ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['NumberOfNonUniformColumns']['Value'])
        if NonUniformColumns > 0:
          TableRow.append(GradeCHTMLTemplate%("{Value:1.0f}".format(Value=NonUniformColumns)))
        else:
          TableRow.append("{Value:1.0f}".format(Value=NonUniformColumns))

        for Rate in self.ParentObject.Attributes['Rates']['HRSCurves']:
          Noise = float(ChipsSubTestResult.ResultData['SubTestResults']['Chip%d'%ChipNo].ResultData['SubTestResults']['SCurveWidths_{Rate}'.format(Rate=Rate)].ResultData['KeyValueDictPairs']['mu']['Value'])
          if Noise >= self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_SCurve_Noise_Threshold_C']:
            TableRow.append(GradeCHTMLTemplate%("{Value:1.0f}".format(Value=Noise)))
          elif Noise >= self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_SCurve_Noise_Threshold_B']:
            TableRow.append(GradeBHTMLTemplate%("{Value:1.0f}".format(Value=Noise)))
          else:
            TableRow.append("{Value:1.0f}".format(Value=Noise))

        self.ResultData['Table']['BODY'].append(TableRow)
