import ROOT
import AbstractClasses.Helper.HistoGetter as HistoGetter
import AbstractClasses
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Fulltest_Chips_Chip_AddressDecoding_TestResult'
        self.NameSingle='AddressDecoding'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'
        self.AddressProblemList = set()
        self.chipNo = self.ParentObject.Attributes['ChipNo']


    def PopulateResultData(self):
        ROOT.gStyle.SetOptStat(0);
        ROOT.gPad.SetLogy(0);

        # TH2D
        ChipNo = self.ParentObject.Attributes['ChipNo']
        self.HistoDict = self.ParentObject.ParentObject.ParentObject.HistoDict
        histname = self.ParentObject.ParentObject.ParentObject.HistoDict.get(self.NameSingle,'AddressDecoding')
        self.ResultData['Plot']['ROOTObject'] =  HistoGetter.get_histo(self.ParentObject.ParentObject.FileHandle,histname,rocNo=ChipNo).Clone(self.GetUniqueID())

        if self.ResultData['Plot']['ROOTObject']:
            self.ResultData['Plot']['ROOTObject'].SetTitle("")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Column No.")
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Row No.")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].Draw('colz')
            for column in range(self.nCols): #Column
                for row in range(self.nRows): #Row
                    self.HasAddressDecodingProblem(column, row)

        self.Title = 'Address Decoding: C{ChipNo}'.format(ChipNo=self.ParentObject.Attributes['ChipNo'])
        self.SaveCanvas()
        self.ResultData['KeyValueDictPairs']['AddressDecodingProblems'] = {'Value':self.AddressProblemList, 'Label':'Address Decoding Problems', }
        self.ResultData['KeyValueDictPairs']['NAddressDecodingProblems'] = {'Value':len(self.AddressProblemList), 'Label':'N Address DecodingProblems', }
        self.ResultData['KeyList'].append('NAddressDecodingProblems')

    def HasAddressDecodingProblem(self, column, row):
        if self.ResultData['Plot']['ROOTObject'].GetBinContent(column + 1, row + 1) < -0.5:
            self.AddressProblemList.add((self.chipNo, column, row))
            return True
        return False
