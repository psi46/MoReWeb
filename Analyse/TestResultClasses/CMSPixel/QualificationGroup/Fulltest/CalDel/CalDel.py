# -*- coding: utf-8 -*-
import AbstractClasses
import ROOT

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_Fulltest_CalDel_TestResult'
        self.NameSingle = 'CalDel'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
        self.ResultData['HiddenData']['DacParameters'] = {}

    def PopulateResultData(self):
        ROOT.gPad.SetLogy(0)
        NChips = self.ParentObject.Attributes['NumberOfChips']
        StartChip = self.ParentObject.Attributes['StartChip']
       
        self.ResultData['Plot']['ROOTObject'] = ROOT.TH1D(self.GetUniqueID(), '', NChips, StartChip, StartChip + NChips)

        Ymin = 0.  # minimum / maximum of y-axis values
        Ymax = 255.

        Sum = 0.
        Mean = 0.
        Difference = 0

        if self.ResultData['Plot']['ROOTObject']:

            NChipResults = 0
            CalDelMin = 255
            CalDelMax = 0

            for i in self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults']:
                ChipTestResultObject = self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults'][i]
                ChipNo = ChipTestResultObject.Attributes['ChipNo']
                ChipPosition = ChipNo + 1
                ChipTestResultObject = \
                    self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults'][i]
                try:
                    strValue = ChipTestResultObject.ResultData['SubTestResults']['OpParameters'].ResultData[
                        'KeyValueDictPairs']['CalDel']['Value']
                    Value = int(strValue)
                    Sum += Value
                    if (CalDelMax<Value):
                        CalDelMax=Value
                    if (CalDelMin>Value):
                        CalDelMin=Value

                    self.ResultData['Plot']['ROOTObject'].SetBinContent(ChipPosition, Value)
                    if 1.2 * Value > Ymax:
                        Ymax = 1.2 * Value
                    elif 1.2 * Value <= Ymin:
                        Ymin = 1.2 * Value
                    NChipResults += 1
                except:
                    print "WARNING: cannot read CalDel DAC!"

            Mean = Sum / NChipResults if NChipResults > 0 else 0
            Difference = CalDelMax - CalDelMin

            self.ResultData['Plot']['ROOTObject'].SetMarkerColor(ROOT.kPink)
            self.ResultData['Plot']['ROOTObject'].SetLineColor(ROOT.kPink)

            self.ResultData['Plot']['ROOTObject'].SetMarkerStyle(21)
            self.ResultData['Plot']['ROOTObject'].SetMarkerSize(0.5)
            self.ResultData['Plot']['ROOTObject'].SetTitle("")
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetRangeUser(Ymin, Ymax)
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("ROC No.")
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle('CalDel [Vcal]')
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].Draw('LP')


        ROOT.gPad.SetLogy(0)

        self.SaveCanvas()
        self.ResultData['Plot']['Caption'] = 'CalDel'

        self.ResultData['KeyValueDictPairs'] = {
            'caldelspread': {
                'Value': '{0:}'.format(Difference),
                'Label': 'CalDel spread'
            },
            'mu': {
                'Value': '{0:1.2f}'.format(Mean),
                'Label': 'μ'
            },
        }


        self.ResultData['KeyList'] = ['mu','caldelspread']
