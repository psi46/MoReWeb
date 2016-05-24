import ROOT
import AbstractClasses
import glob

class ProductionOverview(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def CustomInit(self):
    	self.Name='CMSPixel_ProductionOverview_BBCorners'
    	self.NameSingle='BBCorners'
        self.Title = 'Bump Bonding quality'
        self.DisplayOptions = {
            'Width': 5,
        }
        self.SubPages = []
        self.nROCs = 16
        self.nCols = 52
        self.nRows = 80
        self.marginX = 10
        self.marginY = 10
        self.IncludeSorttable = True

    # taken from M. Donega. pickmodule.py
    def isBorder(self, x,y):
        if (x < self.marginX) or (x> self.nCols-self.marginX) or (y < self.marginY) or (y > self.nRows-self.marginY):
            return True
        return False

    def isCorner(self, x,y):
        # print x, y, self.marginX, self.marginY
        if ((x < self.marginX) and (y < self.marginY)) or ((x < self.marginX) and (y > self.nRows-self.marginY)) or ((x> self.nCols-self.marginX) and (y < self.marginY)) or ((x> self.nCols-self.marginX) and (y > self.nRows-self.marginY)):
            return True
        return False

    # Corners definition:
    #
    # C D | C D | C D | C D | C D | C D | C D | C D  
    # A B | A B | A B | A B | A B | A B | A B | A B 
    # - - | - - | - - | - - | - - | - - | - - | - - 
    # C D | C D | C D | C D | C D | C D | C D | C D 
    # A B | A B | A B | A B | A B | A B | A B | A B 
    #
    def isCornerA(self, x,y):
        # print x, y, self.marginX, self.marginY
        if ((x < self.marginX) and (y < self.marginY)):
            return True
        return False
    #
    def isCornerB(self, x,y):
        # print x, y, self.marginX, self.marginY
        if ((x> self.nCols-self.marginX) and (y < self.marginY)):
            return True
        return False
    #
    def isCornerC(self, x,y):
        # print x, y, self.marginX, self.marginY
        if ((x < self.marginX) and (y > self.nRows-self.marginY)):
            return True
        return False
    #
    def isCornerD(self, x,y):
        # print x, y, self.marginX, self.marginY
        if ((x> self.nCols-self.marginX) and (y > self.nRows-self.marginY)):
            return True
        return False

    def GenerateOverview(self):

        TableData = []
        Rows = self.FetchData()

        ModuleIDsList = []
        for RowTuple in Rows:
            if not RowTuple['ModuleID'] in ModuleIDsList:
                ModuleIDsList.append(RowTuple['ModuleID'])
        ModuleIDsList.sort(reverse=True)

        TableData.append(    
            [
                {'Class' : 'Header', 'Value' : 'Module'}, 
                {'Class' : 'Header', 'Value' : 'Grade'}, 
                {'Class' : 'Header', 'Value' : 'Total'}, 
                {'Class' : 'Header', 'Value' : 'Worst ROC'}, 
                {'Class' : 'Header', 'Value' : 'Borders'}, 
                {'Class' : 'Header', 'Value' : 'Corners'}, 
                {'Class' : 'Header', 'Value' : 'Center'}, 
                {'Class' : 'Header', 'Value' : 'Map'}, 
            ]
        )
        nMod = 0
        for ModuleID in ModuleIDsList:

            countTotBB = 0
            countROCBB = [0]*self.nROCs
            countBorderBB = [0]*self.nROCs
            countCenterBB = [0]*self.nROCs
            countCornerBB = [0]*self.nROCs

            matchRows = [x for x in Rows if x['ModuleID'] == ModuleID and x['TestType'] == self.Attributes['Test']]

            FinalGrade = self.GetFinalGrade(ModuleID, Rows)
            if FinalGrade == 'B':
                FinalGradeFormatted = "<span style='color:#f70;font-weight:bold;'>%s</span>"%FinalGrade
            elif FinalGrade == 'C':
                FinalGradeFormatted = "<span style='color:red;font-weight:bold;'>%s</span>"%FinalGrade
            elif FinalGrade == 'None':
                FinalGradeFormatted = "<span style='color:#777;font-weight:bold;'>%s</span>"%FinalGrade
            else:
                FinalGradeFormatted = FinalGrade

            if len(matchRows) == 1:
                RowTuple = matchRows[0]

                countTotBB = 0
                # get ROOT histogram corresponding to BB defects map
                Path = '/'.join([self.GlobalOverviewPath, RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], "BumpBondingMap", '*.root'])
                RootFiles = glob.glob(Path)
                ROOTObject = self.GetHistFromROOTFile(RootFiles, "BumpBonding")

                for r in range(0,2): # 2 rows per modules
                    for c in range(0,8): # 8 columns per modules                                
                        nROC = c
                        if r > 0: 
                            nROC += 8

                        localX = -1
                        for ic in range(0+c*self.nCols+1,self.nCols+c*self.nCols+1):
                            localX += 1
                            localY = -1
                            for ir in range(0+r*self.nRows+1,self.nRows+r*self.nRows+1):        
                                localY += 1
                                bb = ROOTObject.GetBinContent(ic,ir) 

                                #ntotPXL+=1

                                if bb > 0.5:
                                    # print nROC, localX, localY, bb                                                            
                                    countTotBB += 1
                                    countROCBB[nROC] += 1 # to plot all BB per ROC

                                    # definition of border includes corners!
                                    if self.isBorder(localX,localY):
                                        countBorderBB[nROC]+=1 # to plot all border BB per ROC
                                    else:
                                        countCenterBB[nROC]+=1 

                                    if self.isCorner(localX,localY):
                                        countCornerBB[nROC]+=1 # to plot all corners BB per ROC

                imgPath = '/'.join([self.GlobalOverviewPath, RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], "BumpBondingMap", '*.png'])
                imgFiles = glob.glob(imgPath)
                imgFiles[0] = imgFiles[0].replace('//', '/')
                imgHTMLData = ("<a href='%s'><img src='%s' alt='Bump Bonding defects map' width=600></a>"%(imgFiles[0],imgFiles[0])) if len(imgFiles) > 0 else "-"

                if max(countROCBB) < 42:
                    MaxROC = "%d"%max(countROCBB)
                elif max(countROCBB) < 167:
                    MaxROC = "<span style='color:#f70;font-weight:bold;'>%d</span>"%max(countROCBB)
                else:
                    MaxROC = "<span style='color:red;font-weight:bold;'>%d</span>"%max(countROCBB)

                TableData.append(
                    [
                        "<b>%s</b>"%ModuleID, FinalGradeFormatted, "%d"%countTotBB, MaxROC, "%d"%sum(countBorderBB), "%d"%sum(countCornerBB), "%d"%sum(countCenterBB), imgHTMLData
                    ]
                )
            elif len(matchRows) < 1:
                TableData.append(
                    [
                        "<b>%s</b>"%ModuleID, FinalGradeFormatted, 'N/A', '', '', '', '', '-'
                    ])
            else:
                TableData.append(
                    [
                        "<b>%s</b>"%ModuleID, FinalGradeFormatted, '?', '', '', '', '', '-'
                    ])
            nMod +=1 

        RowLimit = 500
        HTMLInfo = "<b>definitions:</b> corners are pixels with col less or equal than " + "%d"%self.marginX + " pix and row less or equal than " + "%d"%self.marginY + " pix away from edge. Borders include pixels with col less or equal than " + "%d"%self.marginX + " pix or row less or equal than " + "%d"%self.marginY + " pix away from edge, thus include corners.<br>"
        HTMLInfo += "<b>test:</b> " + self.Attributes['Test'] + "<br>"
        HTMLInfo += "<b>features:</b> click on table header to sort table<br>"
        HTML = HTMLInfo + self.Table(TableData, RowLimit, TableClass='sortable', TableStyle='text-align:center;')

        return self.Boxed(HTML)

