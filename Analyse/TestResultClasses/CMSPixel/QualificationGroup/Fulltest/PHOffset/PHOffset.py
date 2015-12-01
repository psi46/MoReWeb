# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import ROOT
import json


class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_Fulltest_PHOffset_TestResult'
        self.NameSingle = 'PHOffset'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
        

    def PopulateResultData(self):
        ROOT.gPad.SetLogy(0);
        NChips = self.ParentObject.Attributes['NumberOfChips']
        StartChip = self.ParentObject.Attributes['StartChip']
       
        self.ResultData['Plot']['ROOTObject'] = ROOT.TH1D(self.GetUniqueID(), '', NChips, StartChip, StartChip + NChips)

        Ymin = 0.  # minimum / maximum of y-axis values
        Ymax = 255.

        #Line = ROOT.TLine()
        Sum = 0.
        Mean = 0.
        Difference = 0

        if self.ResultData['Plot']['ROOTObject']:

            NChipResults = 0
            PHOffsetMin = 255
            PHOffsetMax = 0

            for i in self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults']:
                ChipTestResultObject = self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults'][i]
                ChipNo = ChipTestResultObject.Attributes['ChipNo']
                ChipPosition = ChipNo + 1
                strValue = ''
                Keys=['Chips', '%s'%i, 'DacParameterOverview', 'DacParameters35','KeyValueDictPairs.json', 'phoffset', 'Value']
                Path = self.FinalResultsStoragePath + '/../' + '/'.join(Keys[0:-2])
                JSONData = json.load(open(Path))
                try:
                    strValue = JSONData[Keys[-2]][Keys[-1]]
                    Value = int(strValue)
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


                
                Value = int(Value)
                Sum += Value
                if (PHOffsetMax<Value):
                    PHOffsetMax=Value
                if (PHOffsetMin>Value):
                    PHOffsetMin=Value

                self.ResultData['Plot']['ROOTObject'].SetBinContent(ChipPosition, Value)
                if 1.2 * Value > Ymax:
                    Ymax = 1.2 * Value
                elif 1.2 * Value <= Ymin:
                    Ymin = 1.2 * Value
                NChipResults += 1

            Mean = Sum / NChipResults if NChipResults > 0 else 0
            Difference = PHOffsetMax -  PHOffsetMin

            self.ResultData['Plot']['ROOTObject'].SetMarkerColor(ROOT.kPink)
            self.ResultData['Plot']['ROOTObject'].SetLineColor(ROOT.kPink)

            self.ResultData['Plot']['ROOTObject'].SetMarkerStyle(21)
            self.ResultData['Plot']['ROOTObject'].SetMarkerSize(0.5)
            self.ResultData['Plot']['ROOTObject'].SetTitle("")
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetRangeUser(Ymin, Ymax)
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("ROC No.")
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle('PHOffset [Vcal]')
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].Draw('LP')


        ROOT.gPad.SetLogy(0)

        self.SaveCanvas()
        self.ResultData['Plot']['Caption'] = 'PHOffset'

        self.ResultData['KeyValueDictPairs'] = {
            'phoffsetspread': {
                'Value': '{0:}'.format(Difference),
                'Label': 'PHOffset spread'
            },
            'mu': {
                'Value': '{0:1.2f}'.format(Mean),
                'Label': 'μ'
            },
        }


        self.ResultData['KeyList'] = ['mu','phoffsetspread']
        
        