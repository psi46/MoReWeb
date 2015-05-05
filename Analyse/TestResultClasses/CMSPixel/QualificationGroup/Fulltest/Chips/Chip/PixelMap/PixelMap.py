import ROOT
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter
import AbstractClasses.Helper.ROOTConfiguration as ROOTConfiguration
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        ROOTConfiguration.initialise_ROOT()
        self.Name='CMSPixel_QualificationGroup_Fulltest_Chips_Chip_PixelMap_TestResult'
        self.NameSingle='PixelMap'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'
        self.verbose = True
        self.DeadPixelList = set()
        self.Noisy1PixelList = set()
        self.MaskDefectList = set()
        self.IneffPixelList = set()
        self.chipNo = self.ParentObject.Attributes['ChipNo']


    def PopulateResultData(self):
        ROOT.gStyle.SetOptStat(0)
        ROOT.gPad.SetLogy(0)
        # TH2D
        self.HistoDict = self.ParentObject.ParentObject.ParentObject.HistoDict
        ChipNo=self.ParentObject.Attributes['ChipNo']
        if self.HistoDict.has_option(self.NameSingle,'PixelMap'):
            histname = self.HistoDict.get(self.NameSingle,'PixelMap')
            object = HistoGetter.get_histo(self.ParentObject.ParentObject.FileHandle, histname, rocNo = ChipNo)
            self.ResultData['Plot']['ROOTObject']  = object.Clone(self.GetUniqueID())
        elif self.HistoDict.has_option(self.NameSingle,'Calibrate') and self.HistoDict.has_option(self.NameSingle,'Mask'):
            # TO BE CHECKED
            histname_Calibrate = self.HistoDict.get(self.NameSingle,'Calibrate')
            self.ResultData['Plot']['ROOTObject_Calibrate'] = HistoGetter.get_histo(self.ParentObject.ParentObject.FileHandle, histname_Calibrate, rocNo = ChipNo).Clone(self.GetUniqueID())
            histname_Mask = self.HistoDict.get(self.NameSingle,'Mask')
            self.ResultData['Plot']['ROOTObject_Mask'] = HistoGetter.get_histo(self.ParentObject.ParentObject.FileHandle, histname_Mask, rocNo = ChipNo).Clone(self.GetUniqueID())
            if not self.ResultData['Plot']['ROOTObject_Mask'] or not self.ResultData['Plot']['ROOTObject_Calibrate']:
                raise Exception('Cannot create PixelMap because of not found histos Mask: %s, Calibrate: %s'%(
                                 self.ResultData['Plot']['ROOTObject_Mask'],
                                 self.ResultData['Plot']['ROOTObject_Calibrate'],
                                 ))
            self.ResultData['Plot']['ROOTObject'] = self.ResultData['Plot']['ROOTObject_Calibrate'].Clone(self.GetUniqueID())
            nXbins = self.ResultData['Plot']['ROOTObject'].GetNbinsX()
            nYbins = self.ResultData['Plot']['ROOTObject'].GetNbinsY()
            if self.ParentObject.ParentObject.ParentObject.testSoftware=='pxar':
                comperateTo =1
            else:
                comperateTo=0

            for xbin in range(1,nXbins+1):
                for ybin in range(1,nYbins+1):
                    binContent = self.ResultData['Plot']['ROOTObject_Mask'].GetBinContent(xbin,ybin)

                    if binContent != comperateTo:
                        if self.verbose: print 'MaskProblem with %d/%d'%(xbin,ybin)
                        self.ResultData['Plot']['ROOTObject'].SetBinContent(xbin,ybin,-1)

        self.CheckPixelAlive()
        if self.ResultData['Plot']['ROOTObject']:
            self.ResultData['Plot']['ROOTObject'].SetTitle("");
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Column No.");
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Row No.");
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle();
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5);
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle();
            self.ResultData['Plot']['ROOTObject'].GetZaxis().SetTitle("No. of Readouts");
            self.ResultData['Plot']['ROOTObject'].GetZaxis().CenterTitle();
            self.ResultData['Plot']['ROOTObject'].Draw('colz');

        self.SaveCanvas()
        self.Title = 'Pixel Map: C{ChipNo}'.format(ChipNo=self.ParentObject.Attributes['ChipNo'])
        
    def CheckPixelAlive(self):
        for column in range(self.nCols): #Column
            for row in range(self.nRows): #Row
                pixelAlive = True
                PixelMapCurrentValue = self.ResultData['Plot']['ROOTObject'].GetBinContent(column+1, row+1)
                pixelAlive = pixelAlive and not self.IsDeadPixel(column, row,PixelMapCurrentValue)
                pixelAlive = pixelAlive and not self.IsNoisyPixel(column,row,PixelMapCurrentValue)
                pixelAlive = pixelAlive and not self.HasMaskDefect(column,row,PixelMapCurrentValue)
                pixelAlive = pixelAlive and not self.IsInefficientPixel(column,row,PixelMapCurrentValue)

        NotAlivePixelList = self.DeadPixelList.union(self.Noisy1PixelList).union(self.MaskDefectList).union(self.IneffPixelList)
        self.ResultData['KeyValueDictPairs'][ 'NotAlivePixels'] = {'Value':   (NotAlivePixelList), 'Label':'  Not Alive Pixels', }
        self.ResultData['KeyValueDictPairs']['NNotAlivePixels'] = {'Value':len(NotAlivePixelList), 'Label':'Tot. Dead Pixels', }
        self.ResultData['KeyList'].append('NNotAlivePixels')
        self.ResultData['KeyValueDictPairs'][ 'DeadPixels'] = {'Value':   (self.DeadPixelList), 'Label':'  Dead Pixels', }
        self.ResultData['KeyValueDictPairs']['NDeadPixels'] = {'Value':len(self.DeadPixelList), 'Label':'- N Dead Pixels', }
        self.ResultData['KeyList'].append('NDeadPixels')
        self.ResultData['KeyValueDictPairs'][ 'NoisyPixels'] = {'Value':   (self.Noisy1PixelList), 'Label':'  Noisy Pixels', }
        self.ResultData['KeyValueDictPairs']['NNoisyPixels'] = {'Value':len(self.Noisy1PixelList), 'Label':'- N Noisy Pixels', }
        self.ResultData['KeyList'].append('NNoisyPixels')
        self.ResultData['KeyValueDictPairs'][ 'MaskDefects'] = {'Value':   (self.MaskDefectList), 'Label':'  Mask Defects', }
        self.ResultData['KeyValueDictPairs']['NMaskDefects'] = {'Value':len(self.MaskDefectList), 'Label':'- N Mask Defects', }
        self.ResultData['KeyList'].append('NMaskDefects')
        self.ResultData['KeyValueDictPairs'][ 'InefficentPixels'] = {'Value':   (self.IneffPixelList), 'Label':'  Inefficent Pixels', }
        self.ResultData['KeyValueDictPairs']['NInefficentPixels'] = {'Value':len(self.IneffPixelList), 'Label':'- N Inefficent Pixels', }
        self.ResultData['KeyList'].append('NInefficentPixels')

    def IsDeadPixel(self, column, row,PixelMapCurrentValue):
        if PixelMapCurrentValue == 0:
            self.DeadPixelList.add((self.chipNo,column,row))
            return True
        return False

    def IsNoisyPixel(self,column, row, PixelMapCurrentValue):
        if PixelMapCurrentValue  > self.TestResultEnvironmentObject.GradingParameters['PixelMapMaxValue']:
            self.Noisy1PixelList.add((self.chipNo,column,row))
            return True
        return False

    def HasMaskDefect(self,column,row, PixelMapCurrentValue):
        thr = 0
        if self.TestResultEnvironmentObject.GradingParameters.has_key('PixelMapMaskDefectUpperThreshold'):
            thr = self.TestResultEnvironmentObject.GradingParameters['PixelMapMaskDefectUpperThreshold']
        else:
            print "self.TestResultEnvironmentObject.GradingParameters['PixelMapMaskDefectUpperThreshold'] doesn't exist..."
        if PixelMapCurrentValue  <  thr:
            self.MaskDefectList.add((self.chipNo,column,row))
            return True
        return False

    def IsInefficientPixel(self,column,row,PixelMapCurrentValue):
        if PixelMapCurrentValue  < self.TestResultEnvironmentObject.GradingParameters['PixelMapMinValue']:
            self.IneffPixelList.add((self.chipNo,column,row))
            return True
        return False
