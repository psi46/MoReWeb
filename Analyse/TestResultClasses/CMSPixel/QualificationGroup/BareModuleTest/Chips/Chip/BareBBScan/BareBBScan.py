import ROOT
import AbstractClasses.Helper.HistoGetter as HistoGetter
import AbstractClasses
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Fulltest_Chips_Chip_BareBBScan_TestResult'
        self.NameSingle='BareBBScan'
#       self.NameSingle='BBtestMap'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'
        self.AddressProblemList = set()
        self.chipNo = self.ParentObject.Attributes['ChipNo']


    def PopulateResultData(self):
        ROOT.gStyle.SetOptStat(0);
        ROOT.gPad.SetLogy(0);

        # TH2D
        ChipNo = self.ParentObject.Attributes['ChipNo']
        self.HistoDict = self.ParentObject.ParentObject.ParentObject.HistoDict
        print 'HistoDict BareBBScan: ', self.HistoDict
        histname = self.HistoDict.get(self.NameSingle,'BareBBScan')

        print 'Inside BareBBScan ChipNo: ', ChipNo
        print 'and the histname: ', histname

        if self.HistoDict.has_option(self.NameSingle,'BareBBScan'):
            histname = self.HistoDict.get(self.NameSingle,'BareBBScan')            
            object = HistoGetter.get_histo(self.ParentObject.ParentObject.FileHandle, histname, rocNo = ChipNo)
            self.ResultData['Plot']['ROOTObject']  = object.Clone(self.GetUniqueID())
        
        if self.ResultData['Plot']['ROOTObject']:
            self.ResultData['Plot']['ROOTObject'].SetTitle("")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Column No.")
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Row No.")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].Draw('colz')
            #            for column in range(self.nCols): #Column
            #                for row in range(self.nRows): #Row
            #                    self.HasAddressDecodingProblem(column, row)
            
            self.Title = 'Bare BBScan: C{ChipNo}'.format(ChipNo=self.ParentObject.Attributes['ChipNo'])
                
            
            self.ResultData['Plot']['Format'] = 'png'
            self.SaveCanvas()
			

