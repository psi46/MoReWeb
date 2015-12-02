import ROOT
import AbstractClasses
import os
from operator import itemgetter
import warnings
import AbstractClasses.Helper.HistoGetter as HistoGetter
import array

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):


#AdcVsDac: Readback.rbIa_C%d_V0
#CurrentVsDac : Readback.tbIa_C%d_V0

    def CustomInit(self):
        self.NameSingle = 'ReadbackCalIana'
        self.Name = 'CMSPixel_QualificationGroup_Fulltest_Chips_Chip_%s_TestResult'%self.NameSingle
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'


    def PopulateResultData(self):
        ROOT.gStyle.SetOptStat(0)

        ChipNo = self.ParentObject.Attributes['ChipNo']
        ROOTFile = self.ParentObject.ParentObject.FileHandle

        HistoDict = self.ParentObject.ParentObject.ParentObject.HistoDict
        HistoNameAdcVsDac = HistoDict.get(self.NameSingle, 'AdcVsDac')
        HistoNameCurrentVsDac = HistoDict.get(self.NameSingle, 'CurrentVsDac')

        try:
            HistogramAdcVsDac = HistoGetter.get_histo(ROOTFile, HistoNameAdcVsDac, rocNo=ChipNo).Clone(self.GetUniqueID())
            HistogramCurrentVsDac = HistoGetter.get_histo(ROOTFile, HistoNameCurrentVsDac, rocNo=ChipNo).Clone(self.GetUniqueID())
        except:
            HistogramAdcVsDac = None
            HistogramCurrentVsDac = None

        if HistogramAdcVsDac and HistogramCurrentVsDac:
            NBinsX = HistogramAdcVsDac.GetXaxis().GetNbins()
            NBinsX2 = HistogramCurrentVsDac.GetXaxis().GetNbins()
            #print "nbins:", NBinsX," ",NBinsX2
            #print "ADC vs DAC: ",
            #for i in range(NBinsX):
            #    print HistogramAdcVsDac.GetBinContent(i +1),"  ",
            #print ""
            #print "current vs DAC: ",
            #for i in range(NBinsX2):
            #    print HistogramCurrentVsDac.GetBinContent(i +1),"  ",
            #print ""
            pointListADC = []
            pointListCurrent = []

            if NBinsX==NBinsX2:
                for i in range(NBinsX):
                    if HistogramAdcVsDac.GetBinContent(i+1)!=0 or HistogramCurrentVsDac.GetBinContent(i+1)!=0:
                        pointListCurrent.append(HistogramCurrentVsDac.GetBinContent(i+1))
                        pointListADC.append(HistogramAdcVsDac.GetBinContent(i+1))


            pointsADC = array.array('d', pointListADC)
            pointsCurrent = array.array('d', pointListCurrent)
            numPoints = len(pointsADC)

            self.ResultData['Plot']['ROOTObject'] = ROOT.TGraph(numPoints, pointsADC, pointsCurrent)


            if self.ResultData['Plot']['ROOTObject']:
                self.ResultData['Plot']['ROOTObject'].Draw('AP*')

            self.Title = 'Iana [ADC]/Iana [mA]'
            if self.Canvas:
                self.Canvas.SetCanvasSize(500, 500)

        self.SaveCanvas()

        #TODO: Axis label, punkte blau, fit pol 1. ordnung, Graph wegmachen, etc.