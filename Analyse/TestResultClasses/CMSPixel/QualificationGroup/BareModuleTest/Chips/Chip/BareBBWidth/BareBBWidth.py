import ROOT
import math
import AbstractClasses.Helper.HistoGetter as HistoGetter
import AbstractClasses
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Fulltest_Chips_Chip_BareBBWidth_TestResult'
        self.NameSingle='BareBBWidth'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'
        self.AddressProblemList = set()
        self.chipNo = self.ParentObject.Attributes['ChipNo']
        self.cut = 0
        self.ResultData['KeyValueDictPairs']['thrCutBB2Map'] = {'Value': self.cut, 'Label': 'thrCutBB2'}


    def PopulateResultData(self):

        ROOT.gStyle.SetOptStat(0);
        ROOT.gPad.SetLogy(1);

        # TH2D
        ChipNo = self.ParentObject.Attributes['ChipNo']

        try:
            self.HistoDict = self.ParentObject.ParentObject.ParentObject.HistoDict
            #print '--- Inside HistoDict BareBBWidth: ', self.HistoDict
            histname = self.HistoDict.get(self.NameSingle,'BareBBWidth')
            object = HistoGetter.get_histo(self.ParentObject.ParentObject.FileHandle, histname, rocNo = ChipNo)
            
            if object:
                #print 'bbla'
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
            
                for ii in range (maxbin,1,-2):
                    jj = ii -2
                    if (self.ResultData['Plot']['ROOTObject'].GetBinContent(jj) < y50) and (self.ResultData['Plot']['ROOTObject'].GetBinContent(ii) >= y50):
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
                cut = x1 - sigma
                if cut > cutmax:
                    cut = cutmax
                if cut < 15:
                    cut = 35.

                self.ResultData['KeyValueDictPairs']['thrCutBB2Map']['Value'] = cut
                self.ResultData['KeyList'].append('thrCutBB2Map')
            
                if self.ResultData['Plot']['ROOTObject']:
                    self.ResultData['Plot']['ROOTObject'].SetTitle("")
                    self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Column No.")
                    self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Row No.")
                    self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
                    self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
                    self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
                    self.ResultData['Plot']['ROOTObject'].Draw()
                    
                    self.CutLine = ROOT.TCutG('bumpWidthCut',2)
                    self.CutLine.SetPoint(0,cut,-1e9)
                    self.CutLine.SetPoint(1,cut,+1e9)
                    self.CutLine.SetLineWidth(2)
                    self.CutLine.SetLineStyle(2)
                    self.CutLine.SetLineColor(ROOT.kRed)
                    self.CutLine.Draw('PL')

                    self.Title = 'Bare BBWidth: C{ChipNo}'.format(ChipNo=self.ParentObject.Attributes['ChipNo'])
                    self.SaveCanvas()



            else:
                self.DisplayOptions['Show'] = False
                self.ResultData['Plot']['ROOTObject'] = None
                self.ResultData['KeyList'] = []

        except:
            self.DisplayOptions['Show'] = False
            self.ResultData['Plot']['ROOTObject'] = None
            self.ResultData['KeyList'] = []
            pass
            
