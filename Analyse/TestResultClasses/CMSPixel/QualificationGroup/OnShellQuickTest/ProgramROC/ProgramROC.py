import ROOT
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.NameSingle = 'ProgramROC'
        self.Name = 'CMSPixel_QualificationGroup_OnShellQuickTest_{NameSingle}_TestResult'.format(NameSingle=self.NameSingle)
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'

        self.ResultData['KeyValueDictPairs']['RocsProgrammable'] = {'Value': '-', 'Label': '# programmable ROCs'}
        self.ResultData['KeyList'].append('RocsProgrammable')

    def PopulateResultData(self):
        ROOT.gStyle.SetOptStat(0)
        ROOT.gPad.SetLogy(0)

        # read histograms
        self.HistoDict = self.ParentObject.HistoDict
        if self.HistoDict.has_option('OnShellQuickTest', 'ProgramROC'):
            histname = self.HistoDict.get('OnShellQuickTest', 'ProgramROC')
            rootObject = HistoGetter.get_histo(self.ParentObject.FileHandle, histname)
            self.ResultData['Plot']['ROOTObject'] = rootObject.Clone(self.GetUniqueID())

            # check dead and inefficient pixels
            nChipsProgrammable = 0
            nChips = self.ParentObject.Attributes['NumberOfChips']
            deltaIanaRocs = []
            for chipNo in range(nChips):
               if self.ResultData['Plot']['ROOTObject'].GetBinContent(1 + chipNo) > 5:
                   nChipsProgrammable += 1
               deltaIanaRocs.append(self.ResultData['Plot']['ROOTObject'].GetBinContent(1 + chipNo))

            # fill dictionaries
            self.ResultData['KeyValueDictPairs']['RocsProgrammable']['Value'] = nChipsProgrammable
            self.ResultData['HiddenData']['DeltaIanaRocs'] = deltaIanaRocs

            # style histogram
            if self.ResultData['Plot']['ROOTObject']:
                self.ResultData['Plot']['ROOTObject'].SetTitle("")
                self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("ROC")
                self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
                self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
                self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
                self.ResultData['Plot']['ROOTObject'].SetStats(0)
                self.ResultData['Plot']['ROOTObject'].Draw('')

            self.Title = 'Program ROC'

            # save canvas
            if self.Canvas:
                self.Canvas.SetCanvasSize(500, 500)
            self.ResultData['Plot']['Format'] = 'svg'
            self.SaveCanvas()
