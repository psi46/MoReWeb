import ROOT
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.NameSingle = 'Vana'
        self.Name = 'CMSPixel_QualificationGroup_OnShellQuickTest_{NameSingle}_TestResult'.format(NameSingle=self.NameSingle)
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'

        self.ResultData['KeyValueDictPairs']['VanaMean'] = {'Value': '-', 'Label': 'Vana (mean)'}
        self.ResultData['KeyValueDictPairs']['VanaMin'] = {'Value': '-', 'Label': 'Vana (min)'}
        self.ResultData['KeyValueDictPairs']['VanaMax'] = {'Value': '-', 'Label': 'Vana (max)'}
        self.ResultData['KeyList'].append('VanaMean')
        self.ResultData['KeyList'].append('VanaMin')
        self.ResultData['KeyList'].append('VanaMax')

    def PopulateResultData(self):
        ROOT.gStyle.SetOptStat(0)
        ROOT.gPad.SetLogy(0)

        # read histograms
        self.HistoDict = self.ParentObject.HistoDict
        if self.HistoDict.has_option('OnShellQuickTest', 'Vana'):
            histname = self.HistoDict.get('OnShellQuickTest', 'Vana')
            rootObject = HistoGetter.get_histo(self.ParentObject.FileHandle, histname)
            self.ResultData['Plot']['ROOTObject'] = rootObject.Clone(self.GetUniqueID())

            # check dead and inefficient pixels
            VanaRoc = []
            nChips = self.ParentObject.Attributes['NumberOfChips']
            for chipNo in range(nChips):
                VanaRoc.append(self.ResultData['Plot']['ROOTObject'].GetBinContent(1 + chipNo))

            # fill dictionaries
            self.ResultData['KeyValueDictPairs']['VanaMean']['Value'] = "%1.1f"%(sum(VanaRoc) / len(VanaRoc) if len(VanaRoc) > 0 else -1)
            self.ResultData['KeyValueDictPairs']['VanaMin']['Value'] = "%1.0f"%min(VanaRoc) if len(VanaRoc) > 0 else -1
            self.ResultData['KeyValueDictPairs']['VanaMax']['Value'] = "%1.0f"%max(VanaRoc) if len(VanaRoc) > 0 else -1

            # style histogram
            if self.ResultData['Plot']['ROOTObject']:
                self.ResultData['Plot']['ROOTObject'].SetTitle("")
                self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("ROC")
                self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
                self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
                self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
                self.ResultData['Plot']['ROOTObject'].SetStats(0)
                self.ResultData['Plot']['ROOTObject'].Draw('')

            self.Title = 'Vana'

            # save canvas
            if self.Canvas:
                self.Canvas.SetCanvasSize(500, 500)
            self.ResultData['Plot']['Format'] = 'svg'
            self.SaveCanvas()
