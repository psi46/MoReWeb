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
        self.FitFunction = "[0]+[1]*x+[2]*x**2"

        self.ResultData['KeyList'] = []
        self.ResultData['KeyValueDictPairs'] = {}

    def PopulateResultData(self):
        ROOT.gStyle.SetOptStat(0)
        self.Canvas.Clear()

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

            if NBinsX == NBinsX2:
                for i in range(NBinsX):
                    if HistogramAdcVsDac.GetBinContent(i+1) != 0 or HistogramCurrentVsDac.GetBinContent(i+1) != 0:
                        pointListCurrent.append(HistogramCurrentVsDac.GetBinContent(i+1))
                        pointListADC.append(HistogramAdcVsDac.GetBinContent(i+1))

            pointsADC = array.array('d', pointListADC)
            pointsCurrent = array.array('d', pointListCurrent)
            numPoints = len(pointsADC)

            self.ResultData['Plot']['ROOTObject'] = ROOT.TGraph(numPoints, pointsCurrent, pointsADC)

            if self.ResultData['Plot']['ROOTObject']:
                self.ResultData['Plot']['ROOTObject'].SetMarkerColor(4)
                self.ResultData['Plot']['ROOTObject'].SetMarkerStyle(21)
                self.ResultData['Plot']['ROOTObject'].SetTitle()
                self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle('Iana [mA]')
                self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitleOffset(1.3)
                self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle('Iana [ADC]')
                self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.4)

                # Make linear fit with pol1 and get fit parameters
                FitFunctionTF1 = ROOT.TF1('f1', self.FitFunction)
                self.ResultData['Plot']['ROOTObject'].Fit(FitFunctionTF1, "QS")
                chi2 = FitFunctionTF1.GetChisquare() / FitFunctionTF1.GetNDF() if FitFunctionTF1.GetNDF() > 0 else -1

                # Draw the plot
                self.ResultData['Plot']['ROOTObject'].Draw('AP')                

            self.Title = 'Iana [ADC]/Iana [mA]'
            if self.Canvas:
                self.Canvas.SetCanvasSize(500, 500)
                self.SaveCanvas()

                # Write down the fit function + results
                self.ResultData['KeyValueDictPairs']['FitFunction'] = {
                        'Value': self.FitFunction,
                        'Label':'fit'
                }
                self.ResultData['KeyList'].append('FitFunction')

                # parameters
                for i in range(FitFunctionTF1.GetNpar()):
                    self.ResultData['KeyValueDictPairs']['par%dia'%i] = {
                            'Value': '{0:1.3e}'.format(FitFunctionTF1.GetParameter(i)),
                            'Label':'par%dia'%i
                    }
                    self.ResultData['KeyList'].append('par%dia'%i)

                # chi2/ndf
                self.ResultData['KeyValueDictPairs']['chi2ia'] = {
                        'Value': round(chi2, 2),
                        'Label':'chi2/ndf'
                }
                self.ResultData['KeyList'].append('chi2ia')
