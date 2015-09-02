import ROOT
import math
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
        #self.CutList = set()
        self.cut = 0
        self.ResultData['KeyValueDictPairs']['thrCutBB2Map'] = {'Value': self.cut, 'Label': 'thrCutBB2'}


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

        #print 'Inside BareBBWidth ChipNo: ', ChipNo
        #print 'and the histname: ', histname

        if self.HistoDict.has_option(self.NameSingle,'BareBBWidth'):
            histname = self.HistoDict.get(self.NameSingle,'BareBBWidth')            
            object = HistoGetter.get_histo(self.ParentObject.ParentObject.FileHandle, histname, rocNo = ChipNo)
            self.ResultData['Plot']['ROOTObject']  = object.Clone(self.GetUniqueID())       
#
#  Find PlateauSize cut to define the number of active/missing/inefficient bump-bonding
#            

            cutmax = 45
            maxbin = self.ResultData['Plot']['ROOTObject'].GetMaximumBin()                
            ymax = self.ResultData['Plot']['ROOTObject'].GetBinContent( maxbin )
            xmax = self.ResultData['Plot']['ROOTObject'].GetBinCenter( maxbin )
            y50 = 0.5*ymax
            sigma = self.ResultData['Plot']['ROOTObject'].GetRMS()
            xi = 0.
            xj = 0.
            ni = 0.
            nj = 0.
            
            #print '"====== !!! max ', ymax, ' at ',xmax, ' and sigma: ', sigma               
            for ii in range (maxbin,1,-2):
                jj = ii -2
                #print 'ii jj',ii,jj,' ',self.ResultData['Plot']['ROOTObject'].GetBinContent(jj),self.ResultData['Plot']['ROOTObject'].GetBinContent(ii)
                if (self.ResultData['Plot']['ROOTObject'].GetBinContent(jj) < y50) and (self.ResultData['Plot']['ROOTObject'].GetBinContent(ii) >= y50):
                    #print 'aqui ',ii, ' - - ',jj,'',y50
                    ni = self.ResultData['Plot']['ROOTObject'].GetBinContent(ii)
                    nj = self.ResultData['Plot']['ROOTObject'].GetBinContent(jj)
                    xi = self.ResultData['Plot']['ROOTObject'].GetBinCenter(ii)
                    xj = self.ResultData['Plot']['ROOTObject'].GetBinCenter(jj)
                    dx = xi - xj
                    dn = ni - nj
                    x50 = xj + (y50 - nj) / dn * dx
                    sigma = (xmax - x50)/ 1.3863
                    break

            #print 'n50 ', nj,' at ', xj, ' sigma ',sigma
            x1 = xmax - sigma*math.sqrt(2*math.log(ymax))    
            #print 'x1 , x1',x1
            #cut = x1
            cut = x1 - sigma
            #print 'First Cut: ', cut
            if cut > cutmax:
                cut = cutmax

            print '!!!!!!!!!!!!!CUT: ', cut, ' sigma: ',sigma
            self.ResultData['KeyValueDictPairs']['thrCutBB2Map']['Value'] = cut
            self.ResultData['KeyList'].append('thrCutBB2Map')

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

        
            self.CutLine = ROOT.TCutG('bumpWidthCut',2)
            self.CutLine.SetPoint(0,cut,-1e9)
            self.CutLine.SetPoint(1,cut,+1e9)
            self.CutLine.SetLineWidth(2)
            self.CutLine.SetLineStyle(2)
            self.CutLine.SetLineColor(ROOT.kRed)
            self.CutLine.Draw('PL')



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
