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
            #print 'histname ',  histname
            object = HistoGetter.get_histo(self.ParentObject.ParentObject.FileHandle, histname, rocNo = ChipNo)
                         
            if object:
                self.ResultData['Plot']['ROOTObject']  = object.Clone(self.GetUniqueID())       
#
#  Find PlateauSize cut to define the number of active/missing/inefficient bump-bonding
#            
                #cutmax = 45
                maxbin = self.ResultData['Plot']['ROOTObject'].GetMaximumBin()                
                ibinxCut0 = maxbin
                yCut0 = self.ResultData['Plot']['ROOTObject'].GetBinContent( maxbin )
                #print ' Recalculate the cut using maximun at : ', maxbin
                #print ' ---- cut: ',cut 
                #print ' --ycut0 ', yCut0
                #print ' --ibinxCut0 ', ibinxCut0
                yCut0Next = yCut0


                lCheck = True
                icount = 0

                # going lower

                while ( lCheck and icount < 5): 
                    #print 'inside condition'
                    if yCut0 > 0 :
                        #print 'inside Next Condition running lower'
                        ibinxCut0Next = ibinxCut0 -1
                        yCut0Next = self.ResultData['Plot']['ROOTObject'].GetBinContent(ibinxCut0Next)
                        #print 'yCutNext, xCutNext ',yCut0Next,' -- ',ibinxCut0Next
                        
                        # now check 
                        
                        yCut0 = yCut0Next
                        ibinxCut0 = ibinxCut0Next
                        #++icount
                    
                        #print 'Reset yCut0, ibinxCut0 ',yCut0,' -- ',ibinxCut0, icount, ibinxCut0+icount
                        cut = self.ResultData['Plot']['ROOTObject'].GetBinCenter(ibinxCut0)

                    elif yCut0 == 0:
                        icount = icount + 1
                        ibinxCut0Next = ibinxCut0 -1
                        yCut0Next = self.ResultData['Plot']['ROOTObject'].GetBinContent(ibinxCut0Next)
                        #print 'condition cero yCutNext, xCutNext ',yCut0Next,' -- ',ibinxCut0Next
                        yCut0 = yCut0Next
                        ibinxCut0 = ibinxCut0Next
                        cut = self.ResultData['Plot']['ROOTObject'].GetBinCenter(ibinxCut0)
                        #print '---- icount: ', icount, ' ibinxCut0 ', ibinxCut0
                        
                    else:
                        lCheck = False
                        
                

                #print 'New Cut at bin : ', ibinxCut0 , ' with entries: ', yCut0, ' x value : ', self.ResultData['Plot']['ROOTObject'].GetBinCenter(ibinxCut0)

                #reset the cut value in casae is negative(!)
                if (cut < 0):
                    cut = 20.


                self.ResultData['KeyValueDictPairs']['thrCutBB2Map']['Value'] = cut
                self.ResultData['KeyList'].append('thrCutBB2Map')
            
                #print 'THE CUT ',cut

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
            
