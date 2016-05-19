import ROOT
import AbstractClasses
import os
from operator import itemgetter
import warnings
import AbstractClasses.Helper.HistoGetter as HistoGetter
import array

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):


    def CustomInit(self):
        self.NameSingle = 'ReadbackCalVdig'
        self.Name = 'CMSPixel_QualificationGroup_Fulltest_Chips_Chip_%s_TestResult'%self.NameSingle
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'
        self.FitFunction = "[0]+[1]*x"


    def PopulateResultData(self):
        ROOT.gStyle.SetOptStat(0)
        self.Canvas.Clear()

        HistoDict = self.ParentObject.ParentObject.ParentObject.HistoDict
        HistoName = HistoDict.get(self.NameSingle, 'VdigCalibration')
        ChipNo = self.ParentObject.Attributes['ChipNo']
        ROOTFile = self.ParentObject.ParentObject.FileHandle

        try:
            self.ResultData['Plot']['ROOTObject'] = HistoGetter.get_histo(ROOTFile, HistoName, rocNo=ChipNo).Clone(self.GetUniqueID())
        except:
            pass

        #Add Graph
        try:
            h1 = HistoGetter.get_histo(ROOTFile, HistoName, rocNo=ChipNo).Clone(self.GetUniqueID())
        except:
            h1 = None

        if h1:
            NBinsX = h1.GetXaxis().GetNbins()
            pointListADC = []
            pointListV = []

            for i in range(NBinsX):
                if h1.GetBinContent(i+1):
                    voltage = 0.005+(i*5.0/NBinsX)
                    pointListV.append(voltage)
                    pointListADC.append(h1.GetBinContent(i+1))


            pointsADC = array.array('d', pointListADC)
            pointsV = array.array('d', pointListV)
            numPoints = len(pointsADC)

            g1 = ROOT.TGraph(numPoints, pointsV, pointsADC)
            if g1:
                g1.SetMarkerColor(4)
                g1.SetMarkerStyle(21)
                g1.SetTitle()
                g1.GetXaxis().SetTitle('Vdig [V]')
                g1.GetXaxis().SetTitleOffset(1.3)
                g1.GetYaxis().SetTitle('Vdig [ADC]')
                g1.GetYaxis().SetTitleOffset(1.4)

                #Make linear fit with pol1 and get fit parameters
                FitFunctionTF1 = ROOT.TF1('f1', self.FitFunction)
                g1.Fit(FitFunctionTF1, "QS")
                chi2 = FitFunctionTF1.GetChisquare() / FitFunctionTF1.GetNDF() if FitFunctionTF1.GetNDF() > 0 else -1

                #Draw the plot
                g1.Draw('AP')

                self.ResultData['KeyList'] = []
                self.ResultData['KeyValueDictPairs'] = {}

                # Write down the fit function + results
                self.ResultData['KeyValueDictPairs']['FitFunction'] = {
                        'Value': self.FitFunction,
                        'Label': 'fit'
                }
                self.ResultData['KeyList'].append('FitFunction')

                # parameters
                for i in range(FitFunctionTF1.GetNpar()):
                    self.ResultData['KeyValueDictPairs']['par%dvd'%i] = {
                            'Value': '{0:1.3e}'.format(FitFunctionTF1.GetParameter(i)),
                            'Label': 'par%dvd'%i
                    }
                    self.ResultData['KeyList'].append('par%dvd'%i)

                # chi2/ndf
                self.ResultData['KeyValueDictPairs']['chi2vd'] = {
                        'Value': round(chi2, 2),
                        'Label': 'chi2/ndf'
                }
                self.ResultData['KeyList'].append('chi2vd')

        self.Title = 'Vdig [ADC]/Vdig [V]'
        if self.Canvas:
            self.Canvas.SetCanvasSize(500, 500)
            self.SaveCanvas()




