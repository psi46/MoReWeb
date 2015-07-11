# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import ROOT


class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_Fulltest_Noise_TestResult'
        self.NameSingle = 'Noise'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
        self.Attributes['SpecialPopulateDataParameters'] = {
            'Key': 'Noise',
            'DataKey': 'SCurveWidths',  # which sub test result to take the data from
            'DataParameterKey': 'mu',  # which part of key value dict pairs
            'YLimitB': self.TestResultEnvironmentObject.GradingParameters['noiseB'],  # limit for grading
            'YLimitC': self.TestResultEnvironmentObject.GradingParameters['noiseC'],  # limit for grading
            'MarkerColor': ROOT.kPink,
            'LineColor': ROOT.kPink,
            'MarkerStyle': 21,
            'YaxisTitle': 'Noise [e]',
        }


    def PopulateResultData(self):
        ROOT.gPad.SetLogy(0);
        self.ResultData['HiddenData']['LimitB'] = self.TestResultEnvironmentObject.GradingParameters['noiseB']
        self.ResultData['HiddenData']['LimitC'] = self.TestResultEnvironmentObject.GradingParameters['noiseC']
        self.SpecialPopulateData(self, self.Attributes['SpecialPopulateDataParameters'])


    def SpecialPopulateData(self, TestResultObject, Parameters):
        # limit for grading
        YLimitB = Parameters['YLimitB']

        TestResultObject.ResultData['Plot']['ROOTObject'] = ROOT.TH1D(TestResultObject.GetUniqueID(), '',
                                                                      TestResultObject.ParentObject.Attributes[
                                                                          'NumberOfChips'],
                                                                      TestResultObject.ParentObject.Attributes[
                                                                          'StartChip'],
                                                                      TestResultObject.ParentObject.Attributes[
                                                                          'StartChip'] +
                                                                      TestResultObject.ParentObject.Attributes[
                                                                          'NumberOfChips'])

        # stores the integral values
        TestResultObject.ResultData['Plot']['ROOTObject_h2'] = ROOT.TH1D(TestResultObject.GetUniqueID(), '',
                                                                         TestResultObject.ParentObject.Attributes[
                                                                             'NumberOfChips'],
                                                                         TestResultObject.ParentObject.Attributes[
                                                                             'StartChip'],
                                                                         TestResultObject.ParentObject.Attributes[
                                                                             'StartChip'] +
                                                                         TestResultObject.ParentObject.Attributes[
                                                                             'NumberOfChips'])

        # TestResultObject.ResultData['Plot']['ROOTObject'] =  ROOT.TGraph(TestResultObject.ParentObject.Attributes['NumberOfChips'])
        Ymin = 0.  # minimum / maximum of y-axis values
        Ymax = 0.

        if not Parameters.has_key('ScaleToLimit') or Parameters['ScaleToLimit']:
            Ymax = YLimitB * 1.1

        Line = ROOT.TLine()
        Sum = 0.
        Average = 0.

        if TestResultObject.ResultData['Plot']['ROOTObject']:

            i2 = 0

            for i in TestResultObject.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults']:
                ChipTestResultObject = \
                    self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults'][i]
                ChipNo = ChipTestResultObject.Attributes['ChipNo']
                ChipPosition = ChipNo + 1
                strValue = ''
                try:
                    strValue = ChipTestResultObject.ResultData['SubTestResults'][Parameters['DataKey']].ResultData[
                        'KeyValueDictPairs'][Parameters['DataParameterKey']]['Value']
                    Value = float(strValue)
                    nValue = float(ChipTestResultObject.ResultData['SubTestResults'][Parameters['DataKey']].ResultData[
                        'KeyValueDictPairs']['N']['Value'])
                except KeyError as e:
                    e.message += ' ' + str((Parameters['DataKey'], Parameters['DataParameterKey'], strValue))
                    if Parameters['DataKey'] not in ChipTestResultObject.ResultData['SubTestResults']:
                        e.message += '\n\tMissing: %s, Keys: %s' % (
                            Parameters['DataKey'], ChipTestResultObject.ResultData['SubTestResults'].keys())
                    elif Parameters['DataParameterKey'] not in \
                            ChipTestResultObject.ResultData['SubTestResults'][Parameters['DataKey']].ResultData[
                                'KeyValueDictPairs']:
                        e.message += '\n\tMissing: %s, Keys: %s ' % (Parameters['DataParameterKey'],
                                                                     ChipTestResultObject.ResultData['SubTestResults'][
                                                                         Parameters['DataKey']].ResultData[
                                                                         'KeyValueDictPairs'].keys())
                    raise e
                except TypeError as e:
                    e.message += ' ' + str((Parameters['DataKey'], Parameters['DataParameterKey'], strValue))
                    e.message += '.\n\tParamters: %s' % Parameters
                    e.message += '\n\t Value: %s' % strValue
                    raise e

                except ValueError as e:
                    e.message += ' ' + str((Parameters['DataKey'], Parameters['DataParameterKey'], strValue))
                    e.message += '.\n\tParamters: %s' % Parameters
                    e.message += '\n\t Value: %s' % strValue
                    raise e


                if Parameters.has_key('DataFactor'):
                    Value = Value * Parameters['DataFactor']
                if Parameters.has_key('CalcFunction'):
                    Value = Parameters['CalcFunction'](Value, ChipTestResultObject.ResultData['SubTestResults'][
                        Parameters['DataKey']].ResultData['KeyValueDictPairs'])

                Value = float(Value)
                Sum += Value

                TestResultObject.ResultData['Plot']['ROOTObject'].SetBinContent(ChipPosition, Value)
                TestResultObject.ResultData['Plot']['ROOTObject_h2'].SetBinContent(ChipPosition, nValue)
                #TestResultObject.ResultData['Plot']['ROOTObject'].SetPoint(i2+1,i2+1,Value)
                if 1.2 * Value > Ymax:
                    Ymax = 1.2 * Value
                elif 1.2 * Value <= Ymin:
                    Ymin = 1.2 * Value
                i2 += 1

            if i2 == 0: i2 = 1
            Average = Sum / (i2)

            TestResultObject.ResultData['Plot']['ROOTObject'].SetMarkerColor(Parameters['MarkerColor']);
            TestResultObject.ResultData['Plot']['ROOTObject'].SetLineColor(Parameters['LineColor']);

            TestResultObject.ResultData['Plot']['ROOTObject'].SetMarkerStyle(Parameters['MarkerStyle']);  #
            TestResultObject.ResultData['Plot']['ROOTObject'].SetMarkerSize(0.5)
            TestResultObject.ResultData['Plot']['ROOTObject'].SetTitle("");
            TestResultObject.ResultData['Plot']['ROOTObject'].GetYaxis().SetRangeUser(Ymin, Ymax)
            TestResultObject.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("ROC No.");
            TestResultObject.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle(Parameters['YaxisTitle']);
            TestResultObject.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle();
            TestResultObject.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5);
            TestResultObject.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle();
            TestResultObject.ResultData['Plot']['ROOTObject'].Draw('LP');
            lineB = Line.DrawLine(TestResultObject.ParentObject.Attributes['StartChip'], YLimitB,
                                  TestResultObject.ParentObject.Attributes['StartChip'] +
                                  TestResultObject.ParentObject.Attributes['NumberOfChips'], YLimitB)
            lineB.SetLineWidth(2);
            lineB.SetLineStyle(2)
            lineB.SetLineColor(ROOT.kRed)
            #TestResultObject.ResultData['Plot']['ROOTObject'].SaveAs(TestResultObject.GetPlotFileName()+'.cpp')
        ROOT.gPad.SetLogy(0);

        TestResultObject.SaveCanvas()
        TestResultObject.ResultData['Plot']['Caption'] = Parameters['Key']
        

        #mG
        #Mean = TestResultObject.ResultData['Plot']['ROOTObject'].GetMean()
        Mean = Average
        #sG
        RMS = TestResultObject.ResultData['Plot']['ROOTObject'].GetRMS()
        #nG
        Integral = TestResultObject.ResultData['Plot']['ROOTObject'].Integral(
            TestResultObject.ResultData['Plot']['ROOTObject'].GetXaxis().GetFirst(),
            TestResultObject.ResultData['Plot']['ROOTObject'].GetXaxis().GetLast()
        )
        #nG_entries
        Integral_Entries = TestResultObject.ResultData['Plot']['ROOTObject'].GetEntries()
        #Integral_Entries = TestResultObject.ParentObject.Attributes['NumberOfChips']

        under = TestResultObject.ResultData['Plot']['ROOTObject'].GetBinContent(0)
        over = TestResultObject.ResultData['Plot']['ROOTObject'].GetBinContent(
            TestResultObject.ResultData['Plot']['ROOTObject'].GetNbinsX() + 1)

        TestResultObject.ResultData['KeyValueDictPairs'] = {
            #'N': {
            #   'Value':'{0:1.0f}'.format(Integral),
            #   'Label':'N'
            #},
            'mu': {
                'Value': '{0:1.2f}'.format(Mean),
                'Label': 'μ'
            },
            #'sigma':{
            #   'Value':'{0:1.2f}'.format(RMS),
            #   'Label':'σ'
            #}
        }

        #TestResultObject.ResultData['KeyList'] = ['N','mu','sigma']
        TestResultObject.ResultData['KeyList'] = ['mu']
        if under:
            TestResultObject.ResultData['KeyValueDictPairs']['under'] = {'Value': '{0:1.2f}'.format(under),
                                                                         'Label': '<='}
            TestResultObject.ResultData['KeyList'] += ['under']
        if over:
            TestResultObject.ResultData['KeyValueDictPairs']['over'] = {'Value': '{0:1.2f}'.format(over), 'Label': '>='}
            TestResultObject.ResultData['KeyList'] += ['over']