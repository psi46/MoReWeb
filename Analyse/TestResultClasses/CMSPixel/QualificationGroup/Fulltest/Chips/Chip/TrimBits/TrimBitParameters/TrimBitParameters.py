# -*- coding: utf-8 -*-
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter
import ROOT
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Fulltest_Chips_Chip_TrimBits_TrimBitParameters'+str(self.Attributes['TrimValue'])+'_TestResult'
        self.NameSingle='TrimBitParameters'+str(self.Attributes['TrimValue'])
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'

    def PopulateResultData(self):
        self.ResultData['Plot']['ROOTObject'] =ROOT.TH1F(self.GetUniqueID(), '', 17, -.5, 16.5)
        
        ChipNo=self.ParentObject.ParentObject.Attributes['ChipNo']
        TrimBitParametersFile = self.Attributes['TrimParametersFile']
        if not TrimBitParametersFile:
            raise Exception('Cannot find TrimBitParametersFile')
        else:
            
            for column in range(self.nCols): #Columns
                for row in range(self.nRows): #Rows
                    Line = TrimBitParametersFile.readline()
                    if Line:
                        LineArray = Line.strip().split()
                        TrimBitValue = float(LineArray[0])
                        self.ResultData['Plot']['ROOTObject'].Fill(TrimBitValue)
                        
        if self.ResultData['Plot']['ROOTObject']:
            # for i in range(self.nCols): # Columns
            #    for j in range(self.nRows): # Rows
            #        self.ResultData['Plot']['ROOTObject'].SetBinContent(i+1, j+1, self.ResultData['Plot']['ROOTObject_TrimMap'].GetBinContent(i+1, j+1))

            self.ResultData['Plot']['ROOTObject'].SetTitle("")
            self.ResultData['Plot']['ROOTObject'].SetFillStyle(3002)
            self.ResultData['Plot']['ROOTObject'].SetLineColor(ROOT.kBlack)
            #self.ResultData['Plot']['ROOTObject'].GetZaxis().SetRangeUser(0., self.nTotalChips);
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Trim bits")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetRangeUser(0, 15)

            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("entries")
            #            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Column No.");
            #            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Row No.");
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].Draw('')
            mean = self.ResultData['Plot']['ROOTObject'].GetMean()
            rms = self.ResultData['Plot']['ROOTObject'].GetRMS()
        self.ResultData['KeyValueDictPairs'] = {
            'mu': {
                'Value': '{0:1.2f}'.format(mean),
                'Label': 'μ'
            },
            'sigma': {
                'Value': '{0:1.2f}'.format(rms),
                'Label': 'σ'
            },
            'trimValue': {
                'Value': '{0}'.format(self.Attributes['TrimValue']),
                'Label': 'TrimValue'
            }
        }
        self.ResultData['KeyList'] = ['mu', 'sigma']
        self.SaveCanvas()
        self.Title = 'Trim Bits - Trim '+self.Attributes['TrimValue']
        