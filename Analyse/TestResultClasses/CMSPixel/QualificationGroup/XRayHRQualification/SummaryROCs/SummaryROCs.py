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
        TableHeader = ['ROC','Grade','Defects']
        for Rate in self.ParentObject.Attributes['InterpolatedEfficiencyRates']:
            TableHeader.append('Eff {Rate}'.format(Rate=Rate))

        TableHeader.append('Eff chi2')

        for Rate in self.ParentObject.Attributes['Rates']['HRData']:
            TableHeader.append('Rate "{Rate}"'.format(Rate=Rate))
            # display bb defects only for highest rate = best statistics
            if Rate == max(self.ParentObject.Attributes['Rates']['HRData']):
              TableHeader.append('BB def'.format(Rate=Rate))
        TableHeader.append('RO prob '.format(Rate=Rate))

        TableHeader.append('Unif. prob'.format(Rate=Rate))

        for Rate in self.ParentObject.Attributes['Rates']['HRSCurves']:
            TableHeader.append('Thr [e-] "{Rate}"'.format(Rate=Rate))
            TableHeader.append('Noise "{Rate}"'.format(Rate=Rate))
            TableHeader.append('Noisy pix')

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
                         '###LABEL###':'<div style="width:55px;">Chip '+str(ChipNo)+'</div>',
                         '###URL###':os.path.relpath(i['TestResultObject'].FinalResultsStoragePath, self.ParentObject.FinalResultsStoragePath)+'/TestResult.html'
                     }
                 ), 
                 '<div style="text-align:center;">%s</div>'%ChipsSubTestResult.ResultData['SubTestResults']['Chip%d'%ChipNo].ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['ROCGrade']['Value'],             
            ]
        
            try:
                PixelDefects = int(ChipsSubTestResult.ResultData['SubTestResults']['Chip%d'%ChipNo].ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['PixelDefects']['Value'])
            except:
                PixelDefects = -1

            if PixelDefects > self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_pixel_defects_C']:
                TableRow.append(GradeCHTMLTemplate%("{Value:1.0f}".format(Value=PixelDefects)))
            elif PixelDefects > self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_pixel_defects_B']:
                TableRow.append(GradeBHTMLTemplate%("{Value:1.0f}".format(Value=PixelDefects)))
            else:
                TableRow.append("{Value:1.0f}".format(Value=PixelDefects))

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

            try:
                Chi2NDF = ChipsSubTestResult.ResultData['SubTestResults']['Chip%d'%ChipNo].ResultData['SubTestResults']['EfficiencyInterpolation'].ResultData['KeyValueDictPairs']['Chi2NDF']['Value']
            except:
                Chi2NDF = -1
            TableRow.append(Chi2NDF)

            # rate and bb defects
            for Rate in self.ParentObject.Attributes['Rates']['HRData']:
                RealHitrate = float(ChipsSubTestResult.ResultData['SubTestResults']['Chip%d'%ChipNo].ResultData['SubTestResults']['HitMap_{Rate}'.format(Rate=Rate)].ResultData['KeyValueDictPairs']['RealHitrate']['Value'])
                TableRow.append("{RealHitrate:1.1f}".format(RealHitrate=RealHitrate))
                BumpBondingDefects = int(ChipsSubTestResult.ResultData['SubTestResults']['Chip%d'%ChipNo].ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['BumpBondingDefects_{Rate}'.format(Rate=Rate)]['Value'])
          
                # display bb defects only for highest rate = best statistics
                if Rate == max(self.ParentObject.Attributes['Rates']['HRData']):
                    if BumpBondingDefects >= self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_missing_xray_pixels_C']:
                        TableRow.append(GradeCHTMLTemplate%("{Value:1.0f}".format(Value=BumpBondingDefects)))
                    elif BumpBondingDefects >= self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_missing_xray_pixels_B']:
                        TableRow.append(GradeBHTMLTemplate%("{Value:1.0f}".format(Value=BumpBondingDefects)))
                    else:
                       TableRow.append("{Value:1.0f}".format(Value=BumpBondingDefects))

            # readout problems
            NonUniformEvents = 0
            NonUniformEventsString = ''
            for Rate in self.ParentObject.Attributes['Rates']['HRData']:
                NonUniformEvents = NonUniformEvents + int(ChipsSubTestResult.ResultData['SubTestResults']['Chip%d'%ChipNo].ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['NumberOfNonUniformEvents_{Rate}'.format(Rate=Rate)]['Value'])
                NonUniformEventsString = NonUniformEventsString + str(NonUniformEvents) + '/'

            if NonUniformEvents > 0:
                TableRow.append(GradeCHTMLTemplate%("{Value}".format(Value=NonUniformEventsString.strip('/'))))
            else:
                TableRow.append("{Value}".format(Value=NonUniformEventsString.strip('/')))

            try:
                NonUniformColumns = int(ChipsSubTestResult.ResultData['SubTestResults']['Chip%d'%ChipNo].ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['NumberOfNonUniformColumns']['Value'])
            except:
                NonUniformColumns = 0

            try:
                NonUniformColumnEventsList = ChipsSubTestResult.ResultData['SubTestResults']['Chip%d'%ChipNo].ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['NumberOfNonUniformColumnEvents']['Value']
                NonUniformColumnEvents = sum([int(x) for x in NonUniformColumnEventsList.split('/')])
            except:
                NonUniformColumnEvents = 0

            if NonUniformColumns > 0 or NonUniformColumnEvents > 0:
                if NonUniformColumnEvents > 0:
                    TableRow.append(GradeCHTMLTemplate%("{Value:1.0f}+{Value2}".format(Value=NonUniformColumns, Value2=NonUniformColumnEventsList)))
                else:
                    TableRow.append(GradeCHTMLTemplate%("{Value:1.0f}".format(Value=NonUniformColumns)))
            else:
                TableRow.append("{Value:1.0f}".format(Value=NonUniformColumns))

            for Rate in self.ParentObject.Attributes['Rates']['HRSCurves']:
                Threshold = float(ChipsSubTestResult.ResultData['SubTestResults']['Chip%d'%ChipNo].ResultData['SubTestResults']['SCurveWidths_{Rate}'.format(Rate=Rate)].ResultData['KeyValueDictPairs']['threshold']['Value'])
                TableRow.append("{Value:1.0f}".format(Value=Threshold))
                Noise = float(ChipsSubTestResult.ResultData['SubTestResults']['Chip%d'%ChipNo].ResultData['SubTestResults']['SCurveWidths_{Rate}'.format(Rate=Rate)].ResultData['KeyValueDictPairs']['mu']['Value'])
                if Noise >= self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_SCurve_Noise_Threshold_C']:
                    TableRow.append(GradeCHTMLTemplate%("{Value:1.0f}".format(Value=Noise)))
                elif Noise >= self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_SCurve_Noise_Threshold_B']:
                    TableRow.append(GradeBHTMLTemplate%("{Value:1.0f}".format(Value=Noise)))
                else:
                    TableRow.append("{Value:1.0f}".format(Value=Noise))

                NoisyPixels = float(ChipsSubTestResult.ResultData['SubTestResults']['Chip%d'%ChipNo].ResultData['SubTestResults']['SCurveWidths_{Rate}'.format(Rate=Rate)].ResultData['HiddenData']['NumberOfNoisyPixels']['Value'])  
                if NoisyPixels > self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_pixel_defects_C']:
                    TableRow.append(GradeCHTMLTemplate%("{Value:1.0f}".format(Value=NoisyPixels)))
                elif NoisyPixels > self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_pixel_defects_B']:
                    TableRow.append(GradeBHTMLTemplate%("{Value:1.0f}".format(Value=NoisyPixels)))
                else:
                    TableRow.append("{Value:1.0f}".format(Value=NoisyPixels))

            self.ResultData['Table']['BODY'].append(TableRow)
