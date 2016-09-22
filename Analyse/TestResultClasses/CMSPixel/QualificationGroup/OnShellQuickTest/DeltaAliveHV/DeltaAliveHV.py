import ROOT
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.NameSingle = 'DeltaAliveHV'
        self.Name = 'CMSPixel_QualificationGroup_OnShellQuickTest_{NameSingle}_TestResult'.format(NameSingle=self.NameSingle)
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'

        self.ResultData['KeyValueDictPairs']['DeltaAliveHVRoc'] = {'Value': '-', 'Label': 'Delta Alive HV ROC'}
        self.ResultData['KeyValueDictPairs']['DeltaAliveHV'] = {'Value': '-', 'Label': 'Delta Alive HV'}
        self.ResultData['KeyList'].append('DeltaAliveHV')

    def PopulateResultData(self):
        ROOT.gStyle.SetOptStat(0)
        ROOT.gPad.SetLogy(0)

        # read histograms
        self.HistoDict = self.ParentObject.HistoDict
        if self.HistoDict.has_option('OnShellQuickTest', 'DeltaAliveHV'):
            histname = self.HistoDict.get('OnShellQuickTest', 'DeltaAliveHV')
            rootObject = HistoGetter.get_histo(self.ParentObject.FileHandle, histname)
            self.ResultData['Plot']['ROOTObject'] = rootObject.Clone(self.GetUniqueID())

            # check dead and inefficient pixels
            deltaAliveHV = 0
            deltaAliveHVRocs = []
            nChips = self.ParentObject.Attributes['NumberOfChips']
            for chipNo in range(nChips):
                deltaAliveHV += self.ResultData['Plot']['ROOTObject'].GetBinContent(1 + chipNo)
                deltaAliveHVRocs.append(self.ResultData['Plot']['ROOTObject'].GetBinContent(1 + chipNo))

            # fill dictionaries
            self.ResultData['KeyValueDictPairs']['DeltaAliveHV']['Value'] = deltaAliveHV
            self.ResultData['HiddenData']['DeltaAliveHVRocs'] = deltaAliveHVRocs

            # style histogram
            if self.ResultData['Plot']['ROOTObject']:
                self.ResultData['Plot']['ROOTObject'].SetTitle("")
                self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("ROC")
                self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("# dead pixels")
                self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
                self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
                self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
                self.ResultData['Plot']['ROOTObject'].Draw('')

            self.Title = 'Delta Alive HV'

            # save canvas
            if self.Canvas:
                self.Canvas.SetCanvasSize(500, 500)
            self.ResultData['Plot']['Format'] = 'svg'
            self.SaveCanvas()
