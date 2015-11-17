import AbstractClasses.Helper.HtmlParser
import re
import time
import datetime
import os
import ROOT
import glob
import json
import copy

class GeneralProductionOverview:
    LastUniqueIDCounter = 1

    def __init__(self, TestResultEnvironmentObject = None, InitialAttributes = None, ParentObject=None):
        if TestResultEnvironmentObject:
            self.TestResultEnvironmentObject = TestResultEnvironmentObject
            self.GlobalOverviewPath = self.TestResultEnvironmentObject.GlobalOverviewPath

        self.Debug = False
        self.Verbose = False
        self.Name = 'AbstractClasses_GeneralProductionOverview'
        self.NameSingle = 'GeneralProductionOverview'
        self.SubPages = []
        self.HTMLFileName = ''
        self.BasePath = ''
        self.SaveHTML = False
        self.SavePlotFile = False
        self.ImportPath = ''
        self.Title = 'ProductionOverview'
        self.DisplayOptions = {
            'Width': 2,
        }
        self.FileHandles = []
        self.LastUniqueIDCounter = 1
        self.Attributes = {
            'StorageKey': self.Name,
            'BasePath': '',
        }
        self.Attributes['DateBegin'] = None
        self.Attributes['DateEnd'] = None
        self.Attributes['Title'] = 'ProductionOverview'
        if InitialAttributes:
            self.Attributes.update(InitialAttributes)

        self.DateTimeFormat = "%Y-%m-%d %H:%M"
        self.GradeColors = {
            'A': ROOT.kGreen+2,
            'B': ROOT.kOrange+1,
            'C': ROOT.kRed,
            'None': ROOT.kBlue,
        }
        self.nCols = 52
        self.nRows = 80
        self.Canvas = ROOT.TCanvas()
        self.Canvas.Clear()
        self.Canvas.cd()
        self.ParentObject = ParentObject
        self.ProblematicModulesList = []
        self.FullQualificationFullTests = ['m20_1', 'm20_2', 'p17_1']
        ### custom init
        self.CustomInit()

        try:
            TestName = self.NameSingle
            if 'Test' in self.Attributes:
                TestName += " %s"%self.Attributes['Test']
            if 'DAC' in self.Attributes:
                TestName += " %s"%self.Attributes['DAC']
            if 'Trim' in self.Attributes:
                TestName += " -T %s"%self.Attributes['Trim']
            print " ", TestName
        except:
            pass

        ### create submodule folder
        self.Attributes['BasePath'] += self.GetStorageKey() + '/'
        directory = self.GlobalOverviewPath + '/' + self.Attributes['BasePath']
        try:
            os.mkdir(directory)
        except:
            pass

    # http://stackoverflow.com/a/1700069
    def iso_year_start(self, iso_year):
        "The gregorian calendar date of the first day of the given ISO year"
        fourth_jan = datetime.date(iso_year, 1, 4)
        delta = datetime.timedelta(fourth_jan.isoweekday()-1)
        return fourth_jan - delta 
    def iso_to_gregorian(self, iso_year, iso_week, iso_day):
        "Gregorian calendar date for the given ISO year, week and day"
        year_start = self.iso_year_start(iso_year)
        return year_start + datetime.timedelta(days=iso_day-1, weeks=iso_week-1)

    def PrintInfo(self, Text, Color=4):
        print "\x1b[37m\x1b[%dm"%(40+Color) + Text + "\x1b[0m"

    def GetStorageKey(self):
        if self.Attributes.has_key('StorageKey') and len(self.Attributes['StorageKey']) > 0:
            return self.Attributes['StorageKey']
        else:
            return self.NameSingle

    def GetPlotFileName(self,Suffix='svg',Global=False):
        if Global:
            directory = self.GlobalOverviewPath + '/' + self.Attributes['BasePath']
        else:
            directory = self.GetStorageKey() + '/'

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
                self.Canvas.SaveAs(self.GetPlotFileName('svg', True))
                self.Attributes['ImageFile'] = self.GetPlotFileName('svg', False)
                # save pdf
                PlotFileNamePDF = self.GetPlotFileName('pdf', True)
                self.Canvas.SaveAs(PlotFileNamePDF)
                # save root
                PlotFileNamePDF = self.GetPlotFileName('root', True)
                self.Canvas.SaveAs(PlotFileNamePDF)

    def dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def FetchData(self, ModuleID = None):
        HtmlParser = self.TestResultEnvironmentObject.HtmlParser

        if self.TestResultEnvironmentObject.Configuration['Database']['UseGlobal']:
            Rows = {}
        else:
            AdditionalWhere = ''
            AdditionalParams = {}

            if ModuleID:
                AdditionalWhere += ' AND ModuleID=:ModuleID '
                AdditionalParams['ModuleID'] = ModuleID

            if self.Attributes['DateBegin']:
                AdditionalWhere += ' AND TestDate >= :DateBegin '
                AdditionalParams['DateBegin'] = time.mktime(self.Attributes['DateBegin'].timetuple())

            if self.Attributes['DateEnd']:
                AdditionalWhere += ' AND TestDate <= :DateEnd '
                AdditionalParams['DateEnd'] = time.mktime(self.Attributes['DateEnd'].timetuple())

            Query = 'SELECT * FROM ModuleTestResults WHERE 1=1 '+ AdditionalWhere + ' ORDER BY ModuleID ASC,TestType ASC,TestDate ASC '

            if self.Debug:
                self.PrintInfo("Query: %s"%Query)

            self.TestResultEnvironmentObject.LocalDBConnectionCursor.execute(Query, AdditionalParams)

            self.TestResultEnvironmentObject.LocalDBConnectionCursor.row_factory = self.dict_factory
            Rows = self.TestResultEnvironmentObject.LocalDBConnectionCursor.fetchall()
            if self.Debug:
                self.PrintInfo(" => %d rows returned"%len(Rows),3)

        return Rows

    def GetModuleIDsList(self, Rows, NumModules = 9999, Offset = 0):
        ModuleIDsList = []
        for RowTuple in Rows:
            if not RowTuple['ModuleID'] in ModuleIDsList:
                ModuleIDsList.append(RowTuple['ModuleID'])
        ModuleIDsList.sort()

        if Offset < len(ModuleIDsList):
            ModuleIDsList = ModuleIDsList[Offset::]

        if len(ModuleIDsList) > NumModules:
            ModuleIDsList = ModuleIDsList[0:NumModules]

        return ModuleIDsList

    def GetModuleQualificationRows(self, ModuleID):
        if self.TestResultEnvironmentObject.Configuration['Database']['UseGlobal']:
            Rows = {}
            print "-not implemented for global db-"
        else:
            AdditionalParams = {'ModuleID': ModuleID}
            Query = 'SELECT * FROM ModuleTestResults WHERE ModuleID=:ModuleID'
            if self.Debug:
                self.PrintInfo("Query: %s"%Query)

            self.TestResultEnvironmentObject.LocalDBConnectionCursor.execute(Query, AdditionalParams)
            self.TestResultEnvironmentObject.LocalDBConnectionCursor.row_factory = self.dict_factory
            Rows = self.TestResultEnvironmentObject.LocalDBConnectionCursor.fetchall()
        return Rows

    def ModuleQualificationIsComplete(self, ModuleID, Rows = None):

        if not Rows:
            Rows = self.GetModuleQualificationRows(ModuleID)
        RequiredQualificationTypes = self.TestResultEnvironmentObject.Configuration['RequiredTestTypesForComplete'].strip().split(',')
        FoundQualificationTypes = []
        for RowTuple in Rows:
            if RowTuple['ModuleID']==ModuleID:
                FoundQualificationTypes.append(RowTuple['TestType'])
                #exception: bad leakage current at startup!
                if RowTuple['TestType'] == 'LeakageCurrentPON' and RowTuple['Grade'] == 'C':
                    return True

        Complete = True
        for RequiredQualificationType in RequiredQualificationTypes:
            if RequiredQualificationType not in FoundQualificationTypes:
                Complete = False
                break

        return Complete

    def GetFinalGrade(self, ModuleID, Rows = None):
        if not Rows:
            Rows = self.GetModuleQualificationRows(ModuleID)
        if self.ModuleQualificationIsComplete(ModuleID, Rows):
            ModuleGrades = []
            GradedTestTypes = ['m20_1', 'm20_2', 'p17_1', 'XrayCalibration_Spectrum', 'XRayHRQualification']
            for RowTuple in Rows:
                if RowTuple['ModuleID']==ModuleID:
                    if RowTuple['TestType'] in GradedTestTypes:
                        ModuleGrades.append(RowTuple['Grade'])
                    elif RowTuple['TestType'] == 'LeakageCurrentPON' and RowTuple['Grade'] == 'C':
                        ModuleGrades.append(RowTuple['Grade'])

        FinalGrade = 'None'
        if 'C' in ModuleGrades:
            FinalGrade = 'C'
        elif 'B' in ModuleGrades:
            FinalGrade = 'B'
        elif 'A' in ModuleGrades:
            FinalGrade = 'A'
        
        return FinalGrade

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
        FinalHTML = HtmlParser.substituteMarkerArray(
            FinalHTML, { 
                '###PAGETITLE###': self.Attributes['Title'],
            }
        )
        
        ContentHTML = ''

        ### load modules
        for SubPage in self.SubPages:
            SubModule = SubPage['Module']
            importdir = self.ImportPath + '.' + SubModule
            try:
                f = __import__(importdir + '.' + SubModule, fromlist=[importdir + '.' + 'ProductionOverview'])
            except ImportError as inst:
                f = __import__(importdir + '.ProductionOverview', fromlist=[''])
            pass
            SubPage['ProductionOverview'] = f


        ### run submodules
        for SubPage in self.SubPages:

            InitialAttributes = {}
            if SubPage.has_key('InitialAttributes'):
                InitialAttributes = SubPage['InitialAttributes']

            InitialAttributes['BasePath'] = self.Attributes['BasePath']

            ### instanciate submodule
            SubPageClass = SubPage['ProductionOverview'].ProductionOverview(TestResultEnvironmentObject=self.TestResultEnvironmentObject, InitialAttributes = InitialAttributes, ParentObject = self)

            ### generate html overview of submodule
            #try:
            SubPageContentHTML = SubPageClass.GenerateOverview()
            #except:
            #    SubPageContentHTML = "sub page module not found or 'SubPage['ProductionOverview'].GenerateOverview()' failed"

            ### add to this module html page
            ContentHTML += SubPageContentHTML

        FinalHTML = HtmlParser.substituteSubpart(
            FinalHTML,
            '###PRODUCTIONOVERVIEW###',
            ContentHTML
        )


        # Clickpath
        Levels = self.Attributes['BasePath'][:].split('/')

        ClickPathEntries = []
        ClickPathEntryTemplate = HtmlParser.getSubpart(HTMLTemplate, '###CLICKPATH_ENTRY###')
        LevelPath = ''
        i = 0
        tmpTestResultObject = self
        for Level in Levels[2:]:
            LevelPath = '../' * i
            ClickPathEntries.append(HtmlParser.substituteMarkerArray(
                ClickPathEntryTemplate,
                {
                    '###URL###': HtmlParser.MaskHTML(LevelPath + self.HTMLFileName),
                    '###LABEL###': HtmlParser.MaskHTML(tmpTestResultObject.Attributes['Title'])
                }
            ))
            try:
                if self.ParentObject:
                    tmpTestResultObject = tmpTestResultObject.ParentObject
            except:
                pass 

            i += 1
       
        OverviewHTMLLink = '../../ProductionOverview/ProductionOverview.html'
        ClickPathEntries.append(HtmlParser.substituteMarkerArray(
            ClickPathEntryTemplate,
            {
                '###URL###': HtmlParser.MaskHTML(OverviewHTMLLink),
                '###LABEL###': 'Production Overview'
            }
        ))
        ClickPathEntries.reverse()
        CSSClasses = ''

        FinalHTML = HtmlParser.substituteSubpartArray(
            FinalHTML,
            {
                '###CLICKPATH_ENTRY###': ''.join(ClickPathEntries),
            }
        )

        return FinalHTML


    def GenerateOverview(self):

        FinalHTML = self.GenerateOverviewHTML()

        if self.SaveHTML:
            print "create production overview page: '%s'"%self.HTMLFileName
            f = open(self.GlobalOverviewPath+'/'+self.Attributes['BasePath'] + self.HTMLFileName, 'w')
            f.write(FinalHTML)
            f.close()

        self.CloseFileHandles()


    def Image(self, URL, Style = None):
        HtmlParser = self.TestResultEnvironmentObject.HtmlParser
        PlotTemplate = self.TestResultEnvironmentObject.ProductionOverviewPlotHTMLTemplate
        StyleCSS = ''
        if Style:
            for StyleElement in Style:
                StyleCSS += "%s:%s;"%(StyleElement, Style[StyleElement])
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
                        '###STYLE###': StyleCSS,
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

    def GetHistFromROOTFile(self, RootFileNames, HistName):
        if not type(RootFileNames) == list:
            RootFileNames = [RootFileNames]

        MultipleFilesWarning = False
        if len(RootFileNames) > 1:
            if self.Verbose:
                print "    More than 1 root file found! Using the first one which contains the histogram."
            MultipleFilesWarning = True
        elif len(RootFileNames) < 1:
            if self.Verbose:
                print "    .root file for histogram %s not found!"%HistName
            return None

        HistogramFound = False
        for RootFileName in RootFileNames:
            RootFile = ROOT.TFile.Open(RootFileName)
            RootFileCanvas = RootFile.Get("c1")
            PrimitivesList = RootFileCanvas.GetListOfPrimitives()

            ClonedROOTObject = None
            for i in range(0, PrimitivesList.GetSize()):
                if PrimitivesList.At(i).GetName().find(HistName) > -1:
                    ClonedROOTObject = PrimitivesList.At(i).Clone(self.GetUniqueID())
                    HistogramFound = True
                    break

            if HistogramFound:
                self.FileHandles.append(RootFile)
                if MultipleFilesWarning:
                    print "      => Histogram '%s' found in file '%s"%(HistName, RootFile)
                break
            else:
                RootFile.Close()

        if not HistogramFound:
            return None

        self.Canvas.cd()
        return ClonedROOTObject

    def GetTestPlotColor(self, Test):
        if Test == 'm20_1':
            return ROOT.kRed+1
        elif Test == 'm20_2':
            return ROOT.kBlue+1
        else:
            return ROOT.kBlack

    def GetGradeColor(self, Grade):
        if Grade in self.GradeColors:
            return self.GradeColors[Grade]
        else:
            return ROOT.kBlack

    def GetJSONValue(self, Keys):
        Path = self.GlobalOverviewPath + '/' + '/'.join(Keys[0:-2])

        try:
            with open(Path) as data_file:
                JSONData = json.load(data_file)
        except:
            JSONFiles = glob.glob(Path)
            if len(JSONFiles) > 1:
                if self.Verbose:
                    print "WARNING: %s more than 1 file found '%s"%(self.Name, Path)
                return None
            elif len(JSONFiles) < 1:
                # first Fulltest at -20 is allowed to not have IV curve, don't show warning in this case
                if not 'ModuleFulltestPxar_m20_1/IVCurve' in Path:
                    if self.Verbose:
                        print "WARNING: %s json file not found: '%s"%(self.Name, Path)
                return None
            else:
                try:
                    with open(JSONFiles[0]) as data_file:
                        JSONData = json.load(data_file)
                except:
                    JSONData = None

        try:
            value = JSONData[Keys[-2]][Keys[-1]]
        except:
            value = None
        return value

    def GetUniqueID(self):
        GeneralProductionOverview.LastUniqueIDCounter += 1
        return self.Name + '_' + str(GeneralProductionOverview.LastUniqueIDCounter)

    def CustomInit(self):
        pass

    def CreatePlot(self):
        pass

    def CloseFileHandles(self):
        for FileHandle in self.FileHandles:
            if FileHandle:
                if repr(FileHandle).find('ROOT.TFile') > -1:
                    FileHandle.Close()
                else:
                    FileHandle.close()

    def GetCumulative(self, ROOTHist):
        nbinsx = ROOTHist.GetNbinsX()
        THCumulative = ROOTHist.Clone(self.GetUniqueID())
        Sum = 0
        for binx in range(1, nbinsx+1):
            Sum += ROOTHist.GetBinContent(binx)
            THCumulative.SetBinContent(binx, Sum)
        return THCumulative

    def DisplayErrorsList(self):
        UniqueList = list(set(self.ProblematicModulesList))
        if len(UniqueList)>0:
            print("    \x1b[31m==> Problems with modules: %s\x1b[0m"%(', '.join(UniqueList)))


    def DrawPixelHistogram(self, Rows, ModuleIDsList, HistogramDict, HistogramOptions):
        ROOT.gPad.SetLogy(1)
        ROOT.gStyle.SetOptStat("")

        GradeDict = {
            'A':1,
            'B':2,
            'C':3,
        }

        NROCs = 0
        for RowTuple in Rows:
            ModuleID = RowTuple['ModuleID']
            if ModuleID in ModuleIDsList:
                if ('TestType' in HistogramOptions and HistogramOptions['TestType'] == RowTuple['TestType']) or ('Test' in self.Attributes and RowTuple['TestType'] == self.Attributes['Test']):
                    for Chip in range(0, 16):
                        GradeJsonPath = [x.format(Chip=Chip) if '{Chip}' in x else x for x in HistogramOptions['GradeJsonPath']]
                        RootFilePath = [x.format(Chip=Chip) if '{Chip}' in x else x for x in HistogramOptions['RootFilePath']]
                        GradeJsonPath[:0] = [RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder']]
                        RootFilePath[:0] = [self.GlobalOverviewPath, RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder']]

                        Grade = self.GetJSONValue(GradeJsonPath)
                        try:
                            if Grade and Grade in GradeDict:
                                Grade = GradeDict[Grade]

                            if Grade and '\n' in Grade:
                                Grade = Grade.split('\n')[0]
                        except:
                            pass

                        Path = '/'.join(RootFilePath)
                        RootFiles = glob.glob(Path)
                        ROOTObject = copy.copy(self.GetHistFromROOTFile(RootFiles, HistogramOptions['RootFileHistogramName'])) # (called PHCalibrationGain) todo: name consistently in creation of .root file

                        if ROOTObject:
                            NROCs += 1
                            for HistogramName, HistogramData in HistogramDict.items():
                                if 'Grades' not in HistogramData or (Grade and int(Grade) in HistogramData['Grades']):
                                    if HistogramData['Histogram']:
                                        try:
                                            HistogramDict[HistogramName]['Histogram'].Add(ROOTObject)
                                        except:
                                            print "histogram could not be added, (did you try to use results of different MoReWeb versions?)"
                                    else:
                                        HistogramDict[HistogramName]['Histogram'] = copy.copy(ROOTObject)
                            self.CloseFileHandles()
                        else:
                            self.ProblematicModulesList.append(ModuleID)


        if HistogramDict:
            stats = ROOT.TLatex()
            stats.SetNDC()
            stats.SetTextSize(0.025)
            stats.SetTextAlign(10)
            stats.SetTextFont(62)
            statsText = []

            First = True
            Counter = 0
            StatsTextCounter = 0
            for HistogramName, HistogramData in sorted(HistogramDict.items()):
                if HistogramData['Histogram'] and ('Show' not in HistogramData or HistogramData['Show']):

                    # draw histogram
                    HistogramData['Histogram'].SetLineColor(HistogramData['Color'] if 'Color' in HistogramData else ROOT.kBlack)
                    if First:
                        HistogramData['Histogram'].GetXaxis().SetRangeUser(HistogramOptions['Range'][0], HistogramOptions['Range'][1])
                        HistogramData['Histogram'].GetXaxis().CenterTitle()
                        HistogramData['Histogram'].GetXaxis().SetTitle(HistogramOptions['XTitle'])
                        HistogramData['Histogram'].GetYaxis().SetTitle(HistogramOptions['YTitle'])
                        HistogramData['Histogram'].GetYaxis().CenterTitle()
                        HistogramData['Histogram'].GetYaxis().SetTitleOffset(1.2)
                        HistogramData['Histogram'].Draw("hist")

                        First = False
                    else:
                        HistogramData['Histogram'].Draw("same;hist")


                    # add stats entry
                    mean = round(HistogramData['Histogram'].GetMean(), 2)
                    rms = round(HistogramData['Histogram'].GetRMS(), 2)
                    underflowCount = HistogramData['Histogram'].GetBinContent(0)
                    overflowCount = HistogramData['Histogram'].GetBinContent(HistogramData['Histogram'].GetSize())
                    
                    stats.SetTextColor(HistogramData['Color'] if 'Color' in HistogramData else ROOT.kBlack)
                    statsText = "{Name}: #mu={mu}, #sigma={sigma}".format(Name=HistogramData['Title'] if 'Title' in HistogramData else HistogramName, mu=mean, sigma=rms)
                    stats.DrawLatex(HistogramOptions['StatsPosition'][0], HistogramOptions['StatsPosition'][1] - StatsTextCounter*0.02, statsText)
                    StatsTextCounter += 1

                    statsText = "N={N} UF={uf:1.0f}, OF={of:1.0f}".format(N=HistogramData['Histogram'].GetEntries(), uf=underflowCount, of=overflowCount)
                    stats.DrawLatex(HistogramOptions['StatsPosition'][0], HistogramOptions['StatsPosition'][1] - StatsTextCounter*0.02, statsText)
                    StatsTextCounter += 1

                    Counter += 1

            ROOT.gPad.Update()

            # draw caption
            try:
                NPix = HistogramDict['0-All']['Histogram'].GetEntries()
            except:
                NPix = 0

            title = ROOT.TText()
            title.SetNDC()
            title.SetTextAlign(12)
            title.SetTextSize(0.03)
            title.DrawText(0.15, 0.96, "#roc: %d,  #pix: %d"%(NROCs, NPix))
