import ROOT
import AbstractClasses
import ROOT
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Fulltest_Chips_Chip_PixelMap_TestResult'
        self.NameSingle='PixelMap'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'
        self.verbose = True

        
    def PopulateResultData(self):
        ROOT.gPad.SetLogy(0);
        # TH2D
        fileHandle = self.ParentObject.ParentObject.FileHandle
        HistoDict = self.ParentObject.ParentObject.ParentObject.HistoDict
        ChipNo=self.ParentObject.Attributes['ChipNo']
        if HistoDict.has_option(self.NameSingle,'PixelMap'):
            histname = HistoDict.get(self.NameSingle,'PixelMap')%ChipNo
            self.ResultData['Plot']['ROOTObject'] =  fileHandle.Get(histname).Clone(self.GetUniqueID())
        elif HistoDict.has_option(self.NameSingle,'Calibrate') and HistoDict.has_option(self.NameSingle,'Mask'):
            # TO BE CHECKED
            histname_Calibrate = HistoDict.get(self.NameSingle,'Calibrate')%ChipNo
            self.ResultData['Plot']['ROOTObject_Calibrate'] = fileHandle.Get(histname_Calibrate).Clone(self.GetUniqueID())
            histname_Calibrate = HistoDict.get(self.NameSingle,'Mask')%ChipNo
            self.ResultData['Plot']['ROOTObject_Mask'] = fileHandle.Get(histname_Calibrate).Clone(self.GetUniqueID())
            if not self.ResultData['Plot']['ROOTObject_Mask'] or not self.ResultData['Plot']['ROOTObject_Calibrate']:
                raise Exception('Cannot create PixelMap because of not found histos Mask: %s, Calibrate: %s'%(
                                 self.ResultData['Plot']['ROOTObject_Mask'],
                                 self.ResultData['Plot']['ROOTObject_Calibrate'],
                                 ))
            self.ResultData['Plot']['ROOTObject'] = self.ResultData['Plot']['ROOTObject_Calibrate'].Clone(self.GetUniqueID())
            nXbins = self.ResultData['Plot']['ROOTObject'].GetNbinsX()
            nYbins = self.ResultData['Plot']['ROOTObject'].GetNbinsY()
            for xbin in range(1,nXbins+1):
                for ybin in range(1,nYbins+1):
                    binContent = self.ResultData['Plot']['ROOTObject_Mask'].GetBinContent(xbin,ybin)
                    if binContent != 0:
                        if self.verbose: print 'MaskProblem with %d/%d'%(xbin,ybin)
                        self.ResultData['Plot']['ROOTObject'].SetBinContent(xbin,ybin,-1)
        
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

        if self.SavePlotFile:
            self.Canvas.SaveAs(self.GetPlotFileName())      
        self.ResultData['Plot']['Enabled'] = 1
        self.Title = 'Pixel Map: C{ChipNo}'.format(ChipNo=self.ParentObject.Attributes['ChipNo'])
        self.ResultData['Plot']['ImageFile'] = self.GetPlotFileName()
