import ROOT
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.NameSingle = 'Iana'
        self.Name = 'CMSPixel_QualificationGroup_OnShellQuickTest_{NameSingle}_TestResult'.format(NameSingle=self.NameSingle)
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'

        self.ResultData['KeyValueDictPairs']['IanaTotal'] = {'Value': '-', 'Label': 'Iana (total)', 'Unit': 'mA'}
        self.ResultData['KeyValueDictPairs']['IanaMean'] = {'Value': '-', 'Label': 'Iana (mean)', 'Unit': 'mA'}
        self.ResultData['KeyValueDictPairs']['IanaMin'] = {'Value': '-', 'Label': 'Iana (min)', 'Unit': 'mA'}
        self.ResultData['KeyValueDictPairs']['IanaMax'] = {'Value': '-', 'Label': 'Iana (max)', 'Unit': 'mA'}
        self.ResultData['KeyList'].append('IanaTotal')
        self.ResultData['KeyList'].append('IanaMean')
        self.ResultData['KeyList'].append('IanaMin')
        self.ResultData['KeyList'].append('IanaMax')

    def PopulateResultData(self):
        ROOT.gStyle.SetOptStat(0)
        ROOT.gPad.SetLogy(0)

        # read histograms
        self.HistoDict = self.ParentObject.HistoDict
        if self.HistoDict.has_option('OnShellQuickTest', 'Iana'):
            histname = self.HistoDict.get('OnShellQuickTest', 'Iana')
            rootObject = HistoGetter.get_histo(self.ParentObject.FileHandle, histname)
            self.ResultData['Plot']['ROOTObject'] = rootObject.Clone(self.GetUniqueID())

            # check dead and inefficient pixels
            IanaRoc = []
            nChips = self.ParentObject.Attributes['NumberOfChips']
            for chipNo in range(nChips):
                IanaRoc.append(self.ResultData['Plot']['ROOTObject'].GetBinContent(1 + chipNo))

            # fill dictionaries
            self.ResultData['KeyValueDictPairs']['IanaTotal']['Value'] = "%1.1f"%sum(IanaRoc)
            self.ResultData['KeyValueDictPairs']['IanaMean']['Value'] = "%1.1f"%(sum(IanaRoc) / len(IanaRoc) if len(IanaRoc) > 0 else -1)
            self.ResultData['KeyValueDictPairs']['IanaMin']['Value'] = "%1.1f"%min(IanaRoc) if len(IanaRoc) > 0 else -1
            self.ResultData['KeyValueDictPairs']['IanaMax']['Value'] = "%1.1f"%max(IanaRoc) if len(IanaRoc) > 0 else -1

            self.ResultData['HiddenData']['IanaRocs'] = IanaRoc

            # style histogram
            if self.ResultData['Plot']['ROOTObject']:
                self.ResultData['Plot']['ROOTObject'].SetTitle("")
                self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("ROC")
                self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
                self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
                self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
                self.ResultData['Plot']['ROOTObject'].SetStats(0)
                self.ResultData['Plot']['ROOTObject'].Draw('')

            self.Title = 'Iana'

            # save canvas
            if self.Canvas:
                self.Canvas.SetCanvasSize(500, 500)
            self.ResultData['Plot']['Format'] = 'svg'
            self.SaveCanvas()
