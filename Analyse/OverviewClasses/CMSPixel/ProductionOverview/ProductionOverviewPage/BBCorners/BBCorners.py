import ROOT
import AbstractClasses
import glob
import os

from AbstractClasses.ModuleMap import ModuleMap

class ProductionOverview(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def CustomInit(self):
    	self.Name='CMSPixel_ProductionOverview_BBCorners'
    	self.NameSingle='BBCorners'
        self.Title = 'Pixel Defects (Bump+Dead)'
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
        self.IncludeGrades = ['A', 'B']
        self.SavePlotFile = True
        self.Canvas.SetCanvasSize(1784, 412)
        self.Canvas.Update()


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
                {'Class' : 'Header', 'Value' : 'I_leak ratio'}, 
                {'Class' : 'Header', 'Value' : 'Total'}, 
                {'Class' : 'Header', 'Value' : 'Bump'}, 
                {'Class' : 'Header', 'Value' : 'Dead'}, 
                {'Class' : 'Header', 'Value' : 'WorstROC'}, 
                {'Class' : 'Header', 'Value' : 'Map'}, 
            ]
        )

        try:
            IgnoreModules = [x.strip() for x in self.TestResultEnvironmentObject.Configuration['IgnoreInSelectionList'].split(',')]
            print "ignore modules:",IgnoreModules
        except:
            IgnoreModules = []

        # n defects -> category = floor(n/10)
        defectCategories = []
        nCategories = 20
        for i in range(nCategories):
            defectCategories.append([])

        nMod = 0
        for ModuleID in ModuleIDsList:

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


            if FinalGrade in self.IncludeGrades and ModuleID not in IgnoreModules:
                if len(matchRows) == 1:
                    RowTuple = matchRows[0]

                    countBBTotal = 0
                    countDeadTotal = 0
                    countBBROC = [0]*self.nROCs
                    countDeadROC = [0]*self.nROCs

                    # initialize module map
                    self.DefectsMap = ModuleMap(Name=self.GetUniqueID(), nChips=self.nROCs, StartChip=0)

                    # add dead pixels
                    for iRoc in range(self.nROCs):
                        Path = '/'.join([self.GlobalOverviewPath, RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'],"Chips", "Chip%d"%iRoc, "PixelMap", 'PixelMap.root'])
                        RootFiles = glob.glob(Path)
                        PixelMapROOTObject = self.GetHistFromROOTFile(RootFiles, "PixelMap")

                        for x in range(PixelMapROOTObject.GetNbinsX()):
                            for y in range(PixelMapROOTObject.GetNbinsY()):
                                BinContent = PixelMapROOTObject.GetBinContent(1 + x, 1 + y)
                                if BinContent < 1:
                                    self.DefectsMap.UpdatePlot(iRoc, x, y, 0.123)
                                    countDeadTotal += 1
                                    countDeadROC[iRoc] += 1

                    # add bump defects pixels
                    for iRoc in range(self.nROCs):
                        Path = '/'.join([self.GlobalOverviewPath, RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'],"Chips", "Chip%d"%iRoc, "BumpBondingMap", 'BumpBondingMap.root'])
                        RootFiles = glob.glob(Path)
                        PixelMapROOTObject = self.GetHistFromROOTFile(RootFiles, "BumpBondingMap")

                        for x in range(PixelMapROOTObject.GetNbinsX()):
                            for y in range(PixelMapROOTObject.GetNbinsY()):
                                BinContent = PixelMapROOTObject.GetBinContent(1 + x, 1 + y)
                                if BinContent > 0:
                                    self.DefectsMap.UpdatePlot(iRoc, x, y, 1)
                                    countBBTotal += 1
                                    countBBROC[iRoc] += 1

                    # combine maps, 0.12 means blue
                    self.DefectsMap.Map2D.GetZaxis().SetRangeUser(0.0, 1.0)
                    self.DefectsMap.Map2D.SetStats(ROOT.kFALSE)

                    self.Canvas.Clear()
                    self.DefectsMap.Draw(self.Canvas)
                    saveAsFileName = self.GlobalOverviewPath+'/'+self.Attributes['BasePath'] + 'defects_map_%s.png'%ModuleID
                    self.Canvas.SaveAs(saveAsFileName)

                    imgFile = self.GetStorageKey() + '/defects_map_%s.png'%ModuleID # '/'.join(['..','..',RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], "BumpBondingMap", 'BumpBondingMap.png'])
                    imgHTMLData = ("<a href='%s'><img src='%s' alt='Bump Bonding defects map' width=600></a>"%(imgFile,imgFile))

                    maxRocDefects = [countDeadROC[i] + countBBROC[i] for i in range(self.nROCs)]
                    if max(maxRocDefects) < 42:
                        MaxROC = "%d"%max(maxRocDefects)
                    elif max(maxRocDefects) < 167:
                        MaxROC = "<span style='color:#f70;font-weight:bold;'>%d</span>"%max(maxRocDefects)
                    else:
                        MaxROC = "<span style='color:red;font-weight:bold;'>%d</span>"%max(maxRocDefects)

                    totalDefects = countBBTotal + countDeadTotal

                    defectCategory = int(totalDefects/10)
                    if defectCategory > len(defectCategories) -1:
                        defectCategory = len(defectCategories) -1
                    defectCategories[defectCategory].append(ModuleID)

                    # LEAKAGE CURRENT RATIO
                    try:
                        lcRationNumber = float(self.GetJSONValue([RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'IVCurve', 'KeyValueDictPairs.json', 'CurrentRatio150V', 'Value']))
                        lcRatio = ("%1.2f"%lcRationNumber) if lcRationNumber > 0 else 'N/A'
                    except:
                        lcRatio = 'N/A'

                    TableData.append(
                        [
                            "<b>%s</b>"%ModuleID, FinalGradeFormatted, lcRatio, "%d"%totalDefects, "%d"%countBBTotal, "%d"%countDeadTotal, MaxROC, imgHTMLData
                        ]
                    )
                elif len(matchRows) < 1:
                    TableData.append(
                        [
                            "<b>%s</b>"%ModuleID, FinalGradeFormatted, 'N/A', '', '', '', '',  '-'
                        ])
                else:
                    TableData.append(
                        [
                            "<b>%s</b>"%ModuleID, FinalGradeFormatted, '?', '', '', '', '', '-'

                        ])
                    print "multiple rows found!:", matchRows
                nMod +=1 

        RowLimit = 500
        HTMLInfo = ""
        HTMLInfo += "<b>colors:</b> red = missing bump, blue = dead pixel<br>"
        #HTMLInfo += "<b>definitions:</b> corners are pixels with col less or equal than " + "%d"%self.marginX + " pix and row less or equal than " + "%d"%self.marginY + " pix away from edge. Borders include pixels with col less or equal than " + "%d"%self.marginX + " pix or row less or equal than " + "%d"%self.marginY + " pix away from edge, thus include corners.<br>"
        HTMLInfo += "<b>test:</b> " + self.Attributes['Test'] + "<br>"
        HTMLInfo += "<b>grades:</b> %s<br>"%(', '.join(self.IncludeGrades))
        HTMLInfo += "<b>ignored modules:</b> %s<br>"%(', '.join(IgnoreModules))
        HTMLInfo += "<b>features:</b> click on table header to sort table<br>"

        HTML = HTMLInfo + self.Table(TableData, RowLimit, TableClass='sortable', TableStyle='text-align:center;')

        TableData = []
        # second table
        TableData.append(    
            [
                {'Class' : 'Header', 'Value' : '# defects'}, 
                {'Class' : 'Header', 'Value' : '# cumulative'}, 
                {'Class' : 'Header', 'Value' : '# modules'}, 
                {'Class' : 'Header', 'Value' : 'ModuleIDs'}, 
            ]
        )

        catDefects = 0
        nModulesCumulative = 0
        for moduleIDs in defectCategories:
            catDefects += 10
            nModulesInCategory = len(moduleIDs)
            nModulesCumulative += nModulesInCategory
            categoryName = "<%d"%catDefects if catDefects < nCategories*10 else ">=%d"%(catDefects-10)

            TableData.append(    
                [
                    categoryName,
                    "%d"%nModulesCumulative,
                    "%d"%nModulesInCategory,
                    ", ".join(moduleIDs)
                ]
            )
        HTML += "<br><h4>List of modules less than n defects</h4>" 
        HTML += "<b>ignored modules:</b> %s<br>"%(', '.join(IgnoreModules))
        HTML += "<br>"  + self.Table(TableData, RowLimit, TableClass='', TableStyle='')

        return self.Boxed(HTML)

