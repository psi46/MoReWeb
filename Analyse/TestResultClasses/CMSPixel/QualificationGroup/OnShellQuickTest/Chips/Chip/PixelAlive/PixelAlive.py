import ROOT
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter
import AbstractClasses.Helper.ROOTConfiguration as ROOTConfiguration

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        ROOTConfiguration.initialise_ROOT()
        self.NameSingle = 'PixelAlive'
        self.Name = 'CMSPixel_QualificationGroup_OnShellQuickTest_Chips_Chip_{NameSingle}_TestResult'.format(NameSingle=self.NameSingle)
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_OnShellQuickTest_ROC'

        self.DeadPixelList = set()
        self.IneffPixelList = set()
        self.chipNo = self.ParentObject.Attributes['ChipNo']

        self.PixelMapMaxValue = self.TestResultEnvironmentObject.GradingParameters['PixelMapMaxValue']
        self.PixelMapMinValue = self.TestResultEnvironmentObject.GradingParameters['PixelMapMinValue']

        self.ResultData['KeyValueDictPairs']['DeadPixels'] = {'Value': None, 'Label': 'Dead Pixels'}
        self.ResultData['KeyValueDictPairs']['InefficientPixels'] = {'Value': None, 'Label': 'Inefficient Pixels'}

    def PopulateResultData(self):

        # check if a ntrig settings has been read from testParameters.dat config file
        try:
            if self.ParentObject.ParentObject.ParentObject.nTrigPixelAlive:
                if self.ParentObject.ParentObject.ParentObject.nTrigPixelAlive != self.PixelMapMaxValue:
                    print "PixelAliveMap: ntrig = %d from testParameters.dat is used instead of value from gradingParameters.cfg"%self.ParentObject.ParentObject.ParentObject.nTrigPixelAlive
                self.PixelMapMaxValue = self.ParentObject.ParentObject.ParentObject.nTrigPixelAlive
        except:
            pass

        ROOT.gStyle.SetOptStat(0)
        ROOT.gPad.SetLogy(0)

        # read histograms
        self.HistoDict = self.ParentObject.ParentObject.ParentObject.HistoDict
        ChipNo = self.ParentObject.Attributes['ChipNo']

        if self.HistoDict.has_option('OnShellQuickTest', 'PixelAlive'):
            histname = self.HistoDict.get('OnShellQuickTest', 'PixelAlive')
            rootObject = HistoGetter.get_histo(self.ParentObject.ParentObject.FileHandle, histname, rocNo=ChipNo)
            self.ResultData['Plot']['ROOTObject'] = rootObject.Clone(self.GetUniqueID())

        # check dead and inefficient pixels
        self.IneffPixelList = set([])
        self.DeadPixelList = set([])
        ChipNo = self.ParentObject.Attributes['ChipNo']
        for column in range(self.nCols):
            for row in range(self.nRows):
                nHits = self.ResultData['Plot']['ROOTObject'].GetBinContent(column+1, row+1)
                if nHits < self.PixelMapMaxValue:
                    self.IneffPixelList.add((ChipNo, column, row))
                if nHits < 1:
                    self.DeadPixelList.add((ChipNo, column, row))
        nInefficientPixels = len(self.IneffPixelList)
        nDeadPixels = len(self.DeadPixelList)

        # fill dictionaries
        self.ResultData['KeyValueDictPairs']['DeadPixels'] = {'Value': (self.DeadPixelList), 'Label':'  Dead Pixels', }
        self.ResultData['KeyValueDictPairs']['NDeadPixels'] = {'Value': nDeadPixels, 'Label':'- N Dead Pixels', }
        self.ResultData['KeyList'].append('NDeadPixels')

        self.ResultData['KeyValueDictPairs']['InefficentPixels'] = {'Value': (self.IneffPixelList), 'Label':'  Inefficent Pixels', }
        self.ResultData['KeyValueDictPairs']['NInefficentPixels'] = {'Value': nInefficientPixels, 'Label':'- N Inefficent Pixels', }
        self.ResultData['KeyList'].append('NInefficentPixels')

        # style histogram
        if self.ResultData['Plot']['ROOTObject']:
            self.ResultData['Plot']['ROOTObject'].SetTitle("")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Column No.")
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Row No.")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].GetZaxis().SetTitle("No. of Readouts")
            self.ResultData['Plot']['ROOTObject'].GetZaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].Draw('colz')

        self.Title = 'Pixel Map: C{ChipNo}'.format(ChipNo=ChipNo)

        # save canvas
        if self.Canvas:
            self.Canvas.SetCanvasSize(500, 500)
        self.ResultData['Plot']['Format'] = 'png'
        self.SaveCanvas()
