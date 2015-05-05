import ROOT
import AbstractClasses.Helper.HistoGetter as HistoGetter
import AbstractClasses
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Fulltest_Chips_Chip_BareBBWidth_TestResult'
        self.NameSingle='BareBBWidth'
#       self.NameSingle='BBtestMap'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'
        self.AddressProblemList = set()
        self.chipNo = self.ParentObject.Attributes['ChipNo']


    def PopulateResultData(self):
        ROOT.gStyle.SetOptStat(0);
        ROOT.gPad.SetLogy(1);

        # TH2D
        ChipNo = self.ParentObject.Attributes['ChipNo']
#        print 'display options1: ',self.ParentObject.ParentObject.HistoDict
#        print 'display options2: ',self.ParentObject.HistoDict
#        print 'display options3: ',self.HistoDict
        self.HistoDict = self.ParentObject.ParentObject.ParentObject.HistoDict
        print 'HistoDict BareBBWidth: ', self.HistoDict
        histname = self.HistoDict.get(self.NameSingle,'BareBBWidth')
#        histname = self.ParentObject.ParentObject.ParentObject.HistoDict.get(self.NameSingle,'BareBBWidth')        
#        histname = self.ParentObject.ParentObject.ParentObject.HistoDict.get(self.NameSingle,'BBtestMap')

        print 'Inside BareBBWidth ChipNo: ', ChipNo
        print 'and the histname: ', histname

        if self.HistoDict.has_option(self.NameSingle,'BareBBWidth'):
            histname = self.HistoDict.get(self.NameSingle,'BareBBWidth')            
            object = HistoGetter.get_histo(self.ParentObject.ParentObject.FileHandle, histname, rocNo = ChipNo)
            self.ResultData['Plot']['ROOTObject']  = object.Clone(self.GetUniqueID())
        
            

        #self.ResultData['Plot']['ROOTObject'] =  HistoGetter.get_histo(self.ParentObject.ParentObject.FileHandle,histname,rocNo=ChipNo).Clone(self.GetUniqueID())


        print 'Inside BareBBWidth ChipNo: ', ChipNo
        print 'and the histname: ', histname


        if self.ResultData['Plot']['ROOTObject']:
            self.ResultData['Plot']['ROOTObject'].SetTitle("")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Column No.")
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Row No.")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].Draw()
            #            for column in range(self.nCols): #Column
            #                for row in range(self.nRows): #Row
            #                    self.HasAddressDecodingProblem(column, row)

        
            self.Cut = ROOT.TCutG('bumpWidthCut',2)
            self.Cut.SetPoint(0,33,-1e9)
            self.Cut.SetPoint(1,33,+1e9)
            self.Cut.SetLineWidth(2)
            self.Cut.SetLineStyle(2)
            self.Cut.SetLineColor(ROOT.kRed)
            self.Cut.Draw('PL')



            self.Title = 'Bare BBWidth: C{ChipNo}'.format(ChipNo=self.ParentObject.Attributes['ChipNo'])
            self.SaveCanvas()
#        self.ResultData['KeyValueDictPairs']['AddressDecodingProblems'] = {'Value':self.AddressProblemList, 'Label':'Address Decoding Problems', }
#        self.ResultData['KeyValueDictPairs']['NAddressDecodingProblems'] = {'Value':len(self.AddressProblemList), 'Label':'N Address DecodingProblems', }
#        self.ResultData['KeyList'].append('NAddressDecodingProblems')

#    def HasAddressDecodingProblem(self, column, row):
#        if self.ResultData['Plot']['ROOTObject'].GetBinContent(column + 1, row + 1) < 1:
#            self.AddressProblemList.add((self.chipNo, column, row))
#            return True
#        return False
