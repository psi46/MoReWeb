import ROOT
import AbstractClasses.Helper.HistoGetter as HistoGetter
import AbstractClasses
import TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Chips.Chip.PixelMap as bla
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        if self.ParentObject.ParentObject.ParentObject.testSoftware=='pxar':
            print 'using Fulltest code'
            #self.Name='CMSPixel_QualificationGroup_BareModuleTest_Chips_Chip_BarePixelMap_TestResult'
            #self.NameSingle='PixelMap'
            #self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_BareModuleTest_ROC'
            #self.AddressProblemList = set()
            #self.chipNo = self.ParentObject.Attributes['ChipNo']
        else:
            self.Name='CMSPixel_QualificationGroup_BareModuleTest_Chips_Chip_BarePixelMap_TestResult'
            self.NameSingle='BarePixelMap'
            self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_BareModuleTest_ROC'
            self.AddressProblemList = set()
            self.chipNo = self.ParentObject.Attributes['ChipNo']
            self.DeadPixelList = set()
            self.NDeadPixels = 0

    def PopulateResultData(self):
            ROOT.gStyle.SetOptStat(0);
            ROOT.gPad.SetLogy(0);
        # TH2D
            ChipNo = self.ParentObject.Attributes['ChipNo']
            self.HistoDict = self.ParentObject.ParentObject.ParentObject.HistoDict
            print 'HistoDict BarePixelMap: ', self.HistoDict

            if self.ParentObject.ParentObject.ParentObject.testSoftware=='pxar':

                #blablabla = bla(self)
                #self.ResultData['Plot']['ROOTObject']=bla.ResultData['Plot']['ROOTObject'];

                histname = self.HistoDict.get(self.NameSingle,'Calibrate')
                if self.HistoDict.has_option(self.NameSingle,'Calibrate'):
                    histname = self.HistoDict.get(self.NameSingle,'Calibrate')            
                    object = HistoGetter.get_histo(self.ParentObject.ParentObject.FileHandle, histname, rocNo = ChipNo)
                    self.ResultData['Plot']['ROOTObject']  = object.Clone(self.GetUniqueID())
                    
            else:
                histname = self.HistoDict.get(self.NameSingle,'BarePixelMap') 
                if self.HistoDict.has_option(self.NameSingle,'BarePixelMap'):
                    histname = self.HistoDict.get(self.NameSingle,'BarePixelMap')
                    object = HistoGetter.get_histo(self.ParentObject.ParentObject.FileHandle, histname, rocNo = ChipNo)
                    if not object:
                        print 'no Histogram for ChipNo',ChipNo
                    else:
                        self.ResultData['Plot']['ROOTObject']  = object.Clone(self.GetUniqueID())
                        # loop over the histogram and find list of dead pixels
                        nXbins = self.ResultData['Plot']['ROOTObject'].GetNbinsX()
                        nYbins = self.ResultData['Plot']['ROOTObject'].GetNbinsY()
                        for xbin in range(1,nXbins+1):
                            for ybin in range(1,nYbins+1):
                                binContent = self.ResultData['Plot']['ROOTObject'].GetBinContent(xbin,ybin)
                                if binContent ==0:
                                    self.DeadPixelList.add((ChipNo,xbin-1,ybin-1))


            if not object:   
                print 'Inside BarePixelMap ChipNo: ', ChipNo
            else:
                

                if self.ResultData['Plot']['ROOTObject']:
                    self.ResultData['Plot']['ROOTObject'].SetTitle("")
                    self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Column No.")
                    self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Row No.")
                    self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
                    self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
                    self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
                    self.ResultData['Plot']['ROOTObject'].Draw('colz')
                    self.ResultData['KeyValueDictPairs']['DeadPixels'] = {'Value':self.DeadPixelList, 'Label':'Dead Pixels'}
                    self.ResultData['KeyValueDictPairs']['NDeadPixels'] = { 'Value':len(self.DeadPixelList), 'Label':'N Dead Pixels'}

                    self.Title = 'BarePixelMap: C{ChipNo}'.format(ChipNo=self.ParentObject.Attributes['ChipNo'])
                    self.SaveCanvas()
