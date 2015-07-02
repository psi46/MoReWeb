import AbstractClasses.Helper.HtmlParser
import re
import time
import datetime
import os
import ROOT
import glob
import json

class GeneralProductionOverview:
    def __init__(self, TestResultEnvironmentObject = None, InitialAttributes = None):
        if TestResultEnvironmentObject:
            self.TestResultEnvironmentObject = TestResultEnvironmentObject
            self.GlobalOverviewPath = self.TestResultEnvironmentObject.GlobalOverviewPath

        self.Name = 'AbstractClasses_GeneralProductionOverview'
        self.NameSingle = 'GeneralProductionOverview'
        self.SubPages = []
        self.HTMLFileName = ''
        self.SaveHTML = False
        self.SavePlotFile = False
        self.ImportPath = ''
        self.Title = ''
        self.DisplayOptions = {
            'Width': 2,
        }
        self.FileHandles = []
        self.LastUniqueIDCounter = 1
        self.Attributes = {
            'StorageKey': self.Name
        }
        if InitialAttributes:
            self.Attributes.update(InitialAttributes)

        self.DateTimeFormat = "%Y-%m-%d %H:%M"
        self.nCols = 52
        self.nRows = 80
        self.Canvas = ROOT.TCanvas()
        self.Canvas.Clear()
        self.Canvas.cd()
        self.CustomInit()

    def GetStorageKey(self):
        if self.Attributes.has_key('StorageKey') and len(self.Attributes['StorageKey']) > 0:
            return self.Attributes['StorageKey']
        else:
            return self.NameSingle

    def GetPlotFileName(self,Suffix='svg'):
        directory = self.GlobalOverviewPath + '/' + self.GetStorageKey() + '/'
        try:
            os.mkdir(directory)
        except:
            pass

        try:
            Name = self.NameSingle
        except:
            Name = 'plot'

        return directory + Name + '.' + Suffix

    def SaveCanvas(self):
        if self.SavePlotFile:
            if self.Canvas:
                self.Canvas.Update()
                # save svg
                PlotFileName = self.GetPlotFileName()
                self.Canvas.SaveAs(PlotFileName)
                self.Attributes['ImageFile'] = PlotFileName
                # save pdf
                PlotFileNamePDF = self.GetPlotFileName('pdf')
                self.Canvas.SaveAs(PlotFileNamePDF)
                # save root
                PlotFileNamePDF = self.GetPlotFileName('root')
                self.Canvas.SaveAs(PlotFileNamePDF)

    def dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def FetchData(self, ModuleID = None, DateBegin = None, DateEnd = True):
        HtmlParser = self.TestResultEnvironmentObject.HtmlParser

        if self.TestResultEnvironmentObject.Configuration['Database']['UseGlobal']:
            Rows = {}
        else:
            AdditionalWhere = ''
            if ModuleID:
                AdditionalWhere += ' AND ModuleID=:ModuleID '
            self.TestResultEnvironmentObject.LocalDBConnectionCursor.execute(
                'SELECT * FROM ModuleTestResults '+
                'WHERE 1=1 '+
                AdditionalWhere+
                'ORDER BY ModuleID ASC,TestType ASC,TestDate ASC ',
                {
                    'ModuleID':ModuleID
                }
            )
            self.TestResultEnvironmentObject.LocalDBConnectionCursor.row_factory = self.dict_factory
            Rows = self.TestResultEnvironmentObject.LocalDBConnectionCursor.fetchall()

        return Rows

    def GenerateOverviewHTML(self):

        ModuleData = self.FetchData()
        HtmlParser = self.TestResultEnvironmentObject.HtmlParser

        HTMLTemplate = self.TestResultEnvironmentObject.ProductionOverviewHTMLTemplate
        FinalHTML = HTMLTemplate

        # Stylesheet

        StylesheetHTMLTemplate = HtmlParser.getSubpart(HTMLTemplate, '###HEAD_STYLESHEET_TEMPLATE###')
        StylesheetHTML = HtmlParser.substituteMarkerArray(
            StylesheetHTMLTemplate,
            {
                '###STYLESHEET###':self.TestResultEnvironmentObject.MainStylesheet+
                    self.TestResultEnvironmentObject.ProductionOverviewStylesheet,
            }
        )
        FinalHTML = HtmlParser.substituteSubpart(
            FinalHTML,
            '###HEAD_STYLESHEETS###',
            StylesheetHTML
        )
        FinalHTML = HtmlParser.substituteSubpart(
            FinalHTML,
            '###HEAD_STYLESHEET_TEMPLATE###',
            ''
        )
        ContentHTML = ''

        ### load modules
        for SubPage in self.SubPages:
            SubModule = SubPage['Module']
            importdir = self.ImportPath + '.' + SubModule
            try:
                #print 'import ',importdir,SubModule
                f = __import__(importdir + '.' + SubModule, fromlist=[importdir + '.' + 'ProductionOverview'])
            except ImportError as inst:
                #print 'could not ',importdir+'.'+SubModule,SubModule
                #print 'type',type(inst)
                #print 'inst',inst
                f = __import__(importdir + '.ProductionOverview', fromlist=[''])
                #print 'imported', f, 'please change name of file'
            pass

            SubPage['ProductionOverview'] = f

        ### run submodules

        for SubPage in self.SubPages:

            InitialAttributes = {}
            if SubPage.has_key('InitialAttributes'):
                InitialAttributes = SubPage['InitialAttributes']
            SubPageClass = SubPage['ProductionOverview'].ProductionOverview(TestResultEnvironmentObject=self.TestResultEnvironmentObject, InitialAttributes = InitialAttributes)


            if InitialAttributes:
                self.Attributes.update(InitialAttributes)

            #try:
            SubPageContentHTML = SubPageClass.GenerateOverview()
            #except:
            #    SubPageContentHTML = "sub page module not found or 'SubPage['ProductionOverview'].GenerateOverview()' failed"

            ContentHTML += SubPageContentHTML

        FinalHTML = HtmlParser.substituteSubpart(
            FinalHTML,
            '###PRODUCTIONOVERVIEW###',
            ContentHTML
        )


        return FinalHTML


    def GenerateOverview(self):

        FinalHTML = self.GenerateOverviewHTML()

        if self.SaveHTML:
            print "create production overview page: '%s'"%self.HTMLFileName
            f = open(self.GlobalOverviewPath+'/'+self.HTMLFileName, 'w')
            f.write(FinalHTML)
            f.close()

        for FileHandle in self.FileHandles:
            if repr(FileHandle).find('ROOT.TFile') > -1:
                FileHandle.Close()
            else:
                FileHandle.close()


    def Image(self, URL):
        HtmlParser = self.TestResultEnvironmentObject.HtmlParser
        PlotTemplate = self.TestResultEnvironmentObject.ProductionOverviewPlotHTMLTemplate
        HTML = HtmlParser.substituteMarkerArray(
                    PlotTemplate,
                    {
                        '###IMAGELARGECONTAINERID###': self.Attributes['StorageKey'] + self.GetUniqueID(),
                        '###FILENAME###': URL,
                        '###PDFFILENAME###': URL[0:-3]+"pdf",
                        '###MARGIN_TOP###': str(int(-800. / float(
                            self.DisplayOptions['Width'] * self.TestResultEnvironmentObject.Configuration['DefaultValues'][
                                'CanvasWidth']) *
                                                    float(
                                                        self.TestResultEnvironmentObject.Configuration['DefaultValues'][
                                                            'CanvasHeight']) / 2.)),
                        '###WIDTH###': str(self.DisplayOptions['Width']),
                        '###HEIGHT###': str(1),
                    }
                )
        return HTML

    def Table(self, TableData, RowLimit = 999):

        HtmlParser = self.TestResultEnvironmentObject.HtmlParser
        TableHTMLTemplate = self.TestResultEnvironmentObject.ProductionOverviewTableHTMLTemplate

        # Key Value Dict Pairs
        TableColumnHTMLTemplate = HtmlParser.getSubpart(TableHTMLTemplate, '###TABLE_COLUMN###')
        TableRowHTMLTemplate = HtmlParser.getSubpart(TableHTMLTemplate, '###TABLE_ROW###')

        TableRows = ''
        HTML = ''
        TableID = "table_%s"%hash(str(TableData))
        HideRowsID = "hidebutton_%s"%hash(str(TableData))

        # fill rows
        NRows = 0
        NRowsHidden = 0
        RowLimitReached = False
        for Row in TableData:
            NRows += 1

            RowClass = ''
            if NRows > RowLimit:
                RowClass = 'hidden'
                NRowsHidden += 1

            TableRow = ''
            for Column in Row:

                if type(Column) is dict:
                    Class = Column['Class']
                    Value = Column['Value']
                else:
                    Class = 'Value'
                    Value = Column

                TableRow += HtmlParser.substituteMarkerArray(
                    TableColumnHTMLTemplate,
                    {
                        '###CLASS###': Class,
                        '###VALUE###': Value,
                    }
                )
            TableRows += HtmlParser.substituteMarkerArray(
                HtmlParser.substituteSubpart(TableRowHTMLTemplate, '###TABLE_COLUMN###', TableRow),
                {
                        '###CLASS###': RowClass,
                })

        # build table
        HTML += HtmlParser.substituteMarkerArray(
            HtmlParser.substituteSubpart(TableHTMLTemplate, '###TABLE_ROW###', TableRows),
                {
                        '###TABLEID###': TableID,
                })

        # button to show hidden rows
        if NRowsHidden > 0:
            HTML += "<div id='{HideRowsID}'><a href='#' onclick='var table=document.getElementById(\"{TableID}\");var len=table.childNodes[1].childNodes.length;for (var i=0;i<len;i++){{table.childNodes[1].childNodes[i].className=\" \";}};document.getElementById(\"{HideRowsID}\").style.display=\"none\";return false;'>show hidden {NRowsHidden} of {NRows} rows</a></div>".format(TableID=TableID,NRows=NRows,NRowsHidden=NRowsHidden,HideRowsID=HideRowsID)

        return HTML


    def Boxed(self, HTML, Width = -1):
        if Width < 1:
            Width = self.DisplayOptions['Width']
        HtmlParser = self.TestResultEnvironmentObject.HtmlParser
        SingleBoxWidth = 200
        SingleBoxHeight = 200
        ClearStyle = ''
        if self.DisplayOptions.has_key('Clear'):
            ClearStyle = "clear:%s;"%self.DisplayOptions['Clear']
        return HtmlParser.substituteSubpart(
            '<div style="' + ClearStyle + 'margin:3px;padding:2px;border:none;float:left;width:{BoxWidth}px;min-height:{BoxHeight}px;"><h4>{Title}</h4><!-- ###CONTENT### -->content<!-- ###CONTENT### --></div>'.format(BoxWidth = Width * SingleBoxWidth, BoxHeight=SingleBoxHeight, Title=self.Title),
            '###CONTENT###',
            HTML
        )

    def BoxFooter(self, HTML):
        return "<div style='height:auto'><div style='margin:5px;'>" + HTML + "</div></div>"

    def DateFromTimestamp(self, Timestamp):
        return datetime.datetime.fromtimestamp(Timestamp).strftime(self.DateTimeFormat)

    def GetHistFromROOTFile(self, RootFileName, HistName):
        RootFile = ROOT.TFile.Open(RootFileName)
        RootFileCanvas = RootFile.Get("c1")
        PrimitivesList = RootFileCanvas.GetListOfPrimitives()

        ClonedROOTObject = None
        for i in range(0, PrimitivesList.GetSize()):
            if PrimitivesList.At(i).GetName().find(HistName) > -1:
                ClonedROOTObject = PrimitivesList.At(i).Clone(self.GetUniqueID())
                break

        self.FileHandles.append(RootFile)
        self.Canvas.cd()
        return ClonedROOTObject

    def GetTestPlotColor(self, Test):
        if Test == 'm20_1':
            return ROOT.kRed+1
        elif Test == 'm20_2':
            return ROOT.kBlue+1
        else:
            return ROOT.kBlack
    def GetJSONValue(self, Keys):

        Path = self.GlobalOverviewPath + '/' + '/'.join(Keys[0:-2])
        JSONFiles = glob.glob(Path)
        if len(JSONFiles) > 1:
            print "WARNING: %s more than 1 file found '%s"%(self.Name, Path)
            return None
        elif len(JSONFiles) < 1:
            print "WARNING: %s json file not found: '%s"%(self.Name, Path)
            return None
        else:

            with open(JSONFiles[0]) as data_file:    
                JSONData = json.load(data_file)

        return JSONData[Keys[-2]][Keys[-1]]

    def GetUniqueID(self):
        self.LastUniqueIDCounter += 1
        return self.Name + '_' + str(self.LastUniqueIDCounter)

    def CustomInit(self):
        pass

    def CreatePlot(self):
        pass

