import ROOT
import json
import AbstractClasses.Helper.HistoGetter as HistoGetter
import AbstractClasses

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_BareModuleTest_Chips_Chip_BareBBMap_TestResult'
        self.NameSingle='BareBBMap'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_BareModuleTest_ROC'
        self.MissingBumpList = set()
        self.DeadBumpList = set()
        #self.DeadBumpList = set()
        #self.AddressProblemList = set()
        self.chipNo = self.ParentObject.Attributes['ChipNo']
        self.myBumpDict = {}

    def PopulateResultData(self):
        ROOT.gStyle.SetOptStat(0);
        ROOT.gPad.SetLogy(0);
        # TH2D
        ChipNo = self.ParentObject.Attributes['ChipNo']
        self.HistoDict = self.ParentObject.ParentObject.ParentObject.HistoDict
        print 'HistoDict BareBBMap: ', self.HistoDict
        histname = self.HistoDict.get(self.NameSingle,'BareBBMap')
        histname_Scan = self.HistoDict.get('BareBBScan','BareBBScan')
        
        print 'Inside BareBBMap ChipNo: ', ChipNo
        print 'and the histname: ', histname



        # Calculate the cut from BareBBwidth distribution
        #['KeyValueDictPairs']['thrCutBB2Map']['Value'] 
        #        self.ParentObject.ResultData['SubTestResults']['BumpBonding'].ResultData['KeyValueDictPairs']['Mean']['Value']
        #print '====Access: Cut Value from BBWidth',self.ParentObject.ResultData['SubTestResults']['BareBBWidth'].ResultData['KeyValueDictPairs']['thrCutBB2Map']['Value']
        plWidthCutVal = self.ParentObject.ResultData['SubTestResults']['BareBBWidth'].ResultData['KeyValueDictPairs']['thrCutBB2Map']['Value']
        print 'Used Width Cut ',plWidthCutVal


        #        histname = self.HistoDict.get(self.NameSingle,'BareBBScan')

        if self.HistoDict.has_option(self.NameSingle,'BareBBMap'):
            histname = self.HistoDict.get(self.NameSingle,'BareBBMap')  
            histname_Scan = self.HistoDict.get('BareBBScan','BareBBScan')
            object = HistoGetter.get_histo(self.ParentObject.ParentObject.FileHandle, histname, rocNo = ChipNo)
            object_scan =  HistoGetter.get_histo(self.ParentObject.ParentObject.FileHandle, histname_Scan, rocNo = ChipNo)

            self.ResultData['Plot']['ROOTObject']  = object.Clone(self.GetUniqueID())
            self.ResultData['Plot']['ROOTObject_Scan'] = HistoGetter.get_histo(self.ParentObject.ParentObject.FileHandle, histname_Scan, rocNo = ChipNo).Clone(self.GetUniqueID())

            nXbins = self.ResultData['Plot']['ROOTObject_Scan'].GetNbinsX()
            nYbins = self.ResultData['Plot']['ROOTObject_Scan'].GetNbinsY()

#
#  Find Plateau and count number of active/missing and inefficient bump-bonding
#

            nActive = 0;
            nMissing = 0;
            nIneff = 0;
            ibinCenter = 0;

            for xbin in range(1,nXbins+1):
                
                ibinCenter = self.ResultData['Plot']['ROOTObject_Scan'].GetXaxis().GetBinCenter( xbin );
                # Find the maximum
                imax = 0;
                for  jbin in range(1,nYbins+1):
                    cnt = self.ResultData['Plot']['ROOTObject_Scan'].GetBinContent( xbin, jbin );
                    # Find Maximum
                    if cnt > imax:
                        imax = cnt;
      
                if imax <  10 / 2: #hard-coded!!!!
                    ++nIneff;
                    print 'Dead pixel at raw col: ', int(ibinCenter/80), int(ibinCenter%80);
                    self.DeadBumpList.add((self.chipNo,int(ibinCenter/80)+1,int(ibinCenter%80)+1));
                else:
                    # search for the Plateau
                    iEnd = 0;
                    iBegin = 0;
                    for ybin in range(0,nYbins+1):
                        cnt = self.ResultData['Plot']['ROOTObject_Scan'].GetBinContent( xbin, ybin );
                        # Find Plateau
                        if cnt >= imax / 2 :
                            iEnd = ybin; # end of Plateua
                            if iBegin == 0:
                                iBegin = ybin; # begin of plateau
                        
                    endCont = self.ResultData['Plot']['ROOTObject_Scan'].GetYaxis().GetBinUpEdge(iEnd);
                    beginCont = self.ResultData['Plot']['ROOTObject_Scan'].GetYaxis().GetBinUpEdge(iBegin);

                    if endCont - beginCont < plWidthCutVal:
                    #if iEnd - iBegin < plWidthCutVal: #coming from the analysis of PlWidth distribution
                        ++nMissing;
                        print 'Missing Bump at raw col:', int(ibinCenter/80), int(ibinCenter%80);
                        # with weight 2 to draw it as red
                        self.ResultData['Plot']['ROOTObject'].SetBinContent( int(ibinCenter/80)+1, int(ibinCenter%80)+1, 2. );
                        self.MissingBumpList.add((self.chipNo,int(ibinCenter/80),int(ibinCenter%80)));
                        #self.ResultData['Plot']['ROOTObject'].SetBinContent( int(ibinCenter/80)+1, int(ibinCenter%80)+1, int(iEnd-iBegin) );
                        #print 'Content?',self.ResultData['Plot']['ROOTObject'].GetBinContent( int(ibinCenter/80), int(ibinCenter%80) );

                    else:
                        #self.ResultData['Plot']['ROOTObject'].SetBinContent( int(ibinCenter/80)+1, int(ibinCenter%80)+1, int(iEnd-iBegin) );
                        self.ResultData['Plot']['ROOTObject'].SetBinContent( int(ibinCenter/80)+1, int(ibinCenter%80)+1, 1. );                        
                        ++nActive;
    
            
        if self.ResultData['Plot']['ROOTObject']:
            self.ResultData['Plot']['ROOTObject'].SetTitle("")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Column No.")
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Row No.")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].GetZaxis().SetRangeUser(0.,2.);
            self.ResultData['Plot']['ROOTObject'].Draw('colz')
            self.ResultData['KeyValueDictPairs']['DeadBumps'] = { 'Value':self.DeadBumpList, 'Label':'Dead Bumps'}            
            self.ResultData['KeyValueDictPairs']['NDeadBumps'] = { 'Value':len(self.DeadBumpList), 'Label':'N Dead Bumps'}
            self.ResultData['KeyList'].append('NDeadBumps')            
            self.ResultData['KeyValueDictPairs']['MissingBumps'] = { 'Value':self.MissingBumpList, 'Label':'Missing Bumps'}            
            self.ResultData['KeyValueDictPairs']['NMissingBumps'] = { 'Value':len(self.MissingBumpList), 'Label':'N Missing Bumps'}
            self.ResultData['KeyList'].append('NMissingBumps')

            #print 'Binning: ',self.nCols,self.nRows
            #for column in range(self.nCols): #Column
            #    for row in range(self.nRows): #Row
            #print 'content', column, row, self.ResultData['Plot']['ROOTObject'].GetBinContent(column, row), self.ResultData['Plot']['ROOTObject'].GetXaxis().GetBinCenter( column ), self.ResultData['Plot']['ROOTObject'].GetYaxis().GetBinCenter( row );
            
            self.Title = 'Bare BBMap: C{ChipNo}'.format(ChipNo=self.ParentObject.Attributes['ChipNo'])
                
            self.SaveCanvas()    
            
