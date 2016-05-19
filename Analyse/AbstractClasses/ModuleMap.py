import ROOT

class ModuleMap:
    ModuleMapIDCounter = 0

    def __init__(self, Name='', nChips = 16, StartChip = 1, nCols = 8, nRows = 2, nColsRoc = 52, nRowsRoc = 80, nPixelsX = 1784, nPixelsY = 412):
        self.Name = Name
        self.nCols = nCols
        self.nRows = nRows # has to be equal to 2
        self.nColsRoc = nColsRoc
        self.nRowsRoc = nRowsRoc
        self.nPixelsX = nPixelsX
        self.nPixelsY = nPixelsY
        self.nChips = nChips
        self.StartChip = StartChip

        self.nBinsX = self.nCols * self.nColsRoc
        self.nBinsY = self.nRows * self.nRowsRoc
        self.Map2D = ROOT.TH2D(self.GetUniqueID(), "", self.nBinsX, 0., self.nBinsX, self.nBinsY, 0., self.nBinsY)

    def UpdatePlot(self, chipNo, col, row, value):
        if chipNo < self.nCols:
            tmpCol = self.nCols * self.nColsRoc - 1 - chipNo * self.nColsRoc - col
            tmpRow = self.nRows * self.nRowsRoc - 1 - row
        else:
            tmpCol = (chipNo % self.nCols * self.nColsRoc + col)
            tmpRow = row

        if self.Map2D:
            self.Map2D.Fill(tmpCol, tmpRow, value)

    def GetUniqueID(self):
        self.ModuleMapIDCounter += 1
        return "ModuleMap_%s%d"%(self.Name, self.ModuleMapIDCounter)

    def GetHistogram(self):
        return self.Map2D

    def SetContour(self, NContours):
        if self.Map2D:
            self.Map2D.SetContour(NContours)

    def SetRangeUser(self, rangeMin, rangeMax):
        if self.Map2D:
            self.Map2D.GetZaxis().SetRangeUser(rangeMin, rangeMax)

    def AddTH2D(self, ROOTObject, CountMissing=False, GoodRange=None):
        if ROOTObject.GetXaxis().GetNbins() != self.nBinsX or ROOTObject.GetYaxis().GetNbins() != self.nBinsY:
            if self.verbose:
                print "cannot copy directly because of different #bins:"
                print " self: ", self.nBinsX,"x",self.nBinsY
                print " add: ", ROOTObject.GetXaxis().GetNbins(),"x",ROOTObject.GetYaxis().GetNbins()
            for x in range(self.nBinsX):
                for y in range(self.nBinsY):
                    BinContent = ROOTObject.GetBinContent(1 + x, 1 + y)
                    if CountMissing:
                        if BinContent < 1:
                            self.Map2D.Fill(x, y, 1)
                    elif GoodRange is not None:
                        if BinContent < GoodRange[0] or BinContent > GoodRange[1]:
                            self.Map2D.Fill(x, y, 1)
                    else:
                        self.Map2D.Fill(x, y, ROOTObject.GetBinContent(1 + x, 1 + y))

        else:
            self.Map2D.Add(ROOTObject)

    def AddTH2DChip(self, ROOTObject, Chip, FillFunction):
        ROOTObjectNbinsX = ROOTObject.GetXaxis().GetNbins()
        ROOTObjectNbinsY = ROOTObject.GetYaxis().GetNbins()
        for x in range(ROOTObjectNbinsX):
            for y in range(ROOTObjectNbinsY):
                self.UpdatePlot(Chip, x, y, FillFunction(ROOTObject.GetBinContent(1 + x, 1 + y)))

    def GetNbinsX(self):
        return self.nBinsX

    def GetNbinsY(self):
        return self.nBinsY

    def Draw(self, Canvas, TitleZ = None):

        ROOT.gPad.SetLogy(0)
        ROOT.gPad.SetLogx(0)

        try:
            self.Map2D.GetXaxis().SetTickLength(0.015)
            self.Map2D.GetYaxis().SetTickLength(0.012)
            self.Map2D.GetXaxis().SetAxisColor(1, 0.4)
            self.Map2D.GetYaxis().SetAxisColor(1, 0.4)
            Canvas.SetFrameLineStyle(0)
            Canvas.SetFrameLineWidth(1)
            Canvas.SetFrameBorderMode(0)
            Canvas.SetFrameBorderSize(1)
            Canvas.SetCanvasSize(self.nPixelsX, self.nPixelsY)
        except:
            pass

        try:
            self.Map2D.SetTitle("")
            self.Map2D.GetXaxis().SetTitle("Column No.")
            self.Map2D.GetYaxis().SetTitle("Row No.")
            self.Map2D.GetXaxis().CenterTitle()
            self.Map2D.GetYaxis().SetTitleOffset(0.5)
            self.Map2D.GetYaxis().CenterTitle()
            if TitleZ:
                self.Map2D.GetZaxis().SetTitle(TitleZ)
                self.Map2D.GetZaxis().SetTitleOffset(0.5)
                self.Map2D.GetZaxis().CenterTitle()
            self.Map2D.Draw('colz')
        except:
            pass

        boxes = []
        startChip = self.StartChip
        endChip = self.nChips + startChip - 1

        for i in range(0,16):
            if i < startChip or endChip < i:
                if i < self.nCols:
                    j = self.nCols*self.nRows - 1 - i
                else:
                    j = i - self.nCols
                beginX = (j % self.nCols) * self.nColsRoc
                endX = beginX + self.nColsRoc
                beginY = int(j / self.nCols) * self.nRowsRoc
                endY = beginY + self.nRowsRoc
                newBox = ROOT.TPaveText(beginX, beginY, endX, endY)
                newBox.SetFillColor(29)
                newBox.SetLineColor(29)
                newBox.SetFillStyle(3004)
                newBox.SetShadowColor(0)
                newBox.SetBorderSize(1)
                newBox.Draw()
                boxes.append(newBox)

    def DrawCaption(self, Options, posX = 0.15, posY = 0.965):
        CaptionParts = []

        if 'Caption' in Options:
            CaptionParts.append(Options['Caption'])

        if 'Test' in Options:
            TestNames = {'m20_1' : 'Fulltest -20#circC BTC', 'm20_2': 'Fulltest -20#circC ATC', 'p17_1': 'Fulltest +17#circC'}
            if Options['Test'] in TestNames:
                CaptionParts.append(TestNames[Options['Test']])
            else:
                CaptionParts.append(Options['Test'])

        if 'NModules' in Options:
            CaptionParts.append("modules: %d"%Options['NModules'])
        if 'NROCs' in Options:
            CaptionParts.append("ROCs: %d"%Options['NROCs'])
        if 'NPixels' in Options:
            CaptionParts.append("pixels: %d"%Options['NPixels'])
        if 'NDefects' in Options:
            CaptionParts.append("defects: %d"%Options['NDefects'])
        if 'Grades' in Options:
            CaptionParts.append("Grades: %s"%Options['Grades'])

        Caption = ', '.join(CaptionParts)

        title = ROOT.TLatex()
        title.SetNDC()
        title.SetTextAlign(12)

        title.DrawLatex(posX, posY, Caption)