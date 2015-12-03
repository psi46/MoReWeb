import ROOT
import AbstractClasses
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
                self.ResultData['Plot']['ROOTObject'].SetMarkerColor(4)
                self.ResultData['Plot']['ROOTObject'].SetMarkerStyle(21)
                self.ResultData['Plot']['ROOTObject'].SetTitle()
                self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle('Iana [ADC]')
                self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitleOffset(1.3)
                self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle('Iana [ma]')
                self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.4)

                #Make linear fit with pol1 and get fit parameters
                f1=ROOT.TF1('f1','1 ++ x')
                self.ResultData['Plot']['ROOTObject'].Fit("f1","Q")
                p0 = f1.GetParameter(0)
                p1 = f1.GetParameter(1)
                chi2 = f1.GetChisquare()

                #Draw the plot
                self.ResultData['Plot']['ROOTObject'].Draw('AP')                


            self.Title = 'Iana [mA]/Iana [ADC]'
            if self.Canvas:
                self.Canvas.SetCanvasSize(500, 500)
                self.SaveCanvas()

                #Write down the fit results
                self.ResultData['KeyValueDictPairs'] = {
                    'par0ia': {
                    'Value': round(p0, 2),
                    'Label':'par0ia'
                    },
                    'par1ia': {
                        'Value': round(p1, 2),
                        'Label':'par1ia'
                    },
                    'chi2ia': {
                        'Value': round(chi2, 2),
                        'Label':'chi2'
                    },

                }
                self.ResultData['KeyList'] = ['par0ia', 'par1ia', 'chi2ia']
