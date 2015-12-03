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


    def PopulateResultData(self):
        ROOT.gStyle.SetOptStat(0)

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
                g1.SetTitle();
                g1.GetXaxis().SetTitle('Vdig [V]');
                g1.GetXaxis().SetTitleOffset(1.3);
                g1.GetYaxis().SetTitle('Vdig [ADC]');
                g1.GetYaxis().SetTitleOffset(1.4);

                #Make linear fit with pol1 and get fit parameters
                f1=ROOT.TF1('f1','1 ++ x')
                g1.Fit("f1","Q");
                p0 = f1.GetParameter(0)
                p1 = f1.GetParameter(1)
                chi2 = f1.GetChisquare()

                #Draw the plot
                g1.Draw('AP')

            #Write down the fit results
            self.ResultData['KeyValueDictPairs'] = {
                'par0vd': {
                'Value': round(p0,2),
                'Label':'par0vd'
                },
                'par1vd': {
                    'Value':round(p1,2),
                    'Label':'par1vd'
                },
                'chi2vd': {
                    'Value':round(chi2,2),
                    'Label':'chi2'
                },

                                                    }
            self.ResultData['KeyList'] = ['par0vd', 'par1vd', 'chi2vd']

        self.Title = 'Vdig [ADC]/Vdig [V]'
        if self.Canvas:
            self.Canvas.SetCanvasSize(500, 500)
            self.SaveCanvas()




