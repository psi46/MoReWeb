import AbstractClasses.Helper.HtmlParser
import re
import datetime
import os
import json
import glob

class ModuleResultOverview:
    def __init__(self, TestResultEnvironmentObject):
        self.TestResultEnvironmentObject = TestResultEnvironmentObject
        self.GlobalOverviewPath = self.TestResultEnvironmentObject.GlobalOverviewPath

    def TableData(self, ModuleID = None, TestDate = None, GlobalOverviewList = True):
        HtmlParser = self.TestResultEnvironmentObject.HtmlParser

        if self.TestResultEnvironmentObject.Configuration['Database']['UseGlobal']:
            Rows = {}
        else:
            SortMode = self.TestResultEnvironmentObject.Configuration['QualificationOverviewSort'].strip().split(',')
            SortClause = ''
            if len(SortMode) > 0:
                for i in range(0, len(SortMode)):
                    parts = SortMode[i].strip().split(' ')
                    if len(parts) > 0:
                        if parts[0] in ['ModuleID', 'TestType', 'TestDate']:
                            SortClause = SortClause + parts[0]
                        if len(parts) > 1:
                            if parts[1].upper() in ['ASC', 'DESC']:
                                SortClause = SortClause + ' ' + parts[1]
                        SortClause = SortClause + ','
                SortClause = SortClause.strip(',')
            else:
                SortClause = 'ModuleID ASC,TestType ASC,TestDate ASC'

            AdditionalWhere = ''
            if ModuleID:
                AdditionalWhere += ' AND ModuleID=:ModuleID '
            if TestDate:
                AdditionalWhere += ' AND TestDate=:TestDate '
            self.TestResultEnvironmentObject.LocalDBConnectionCursor.execute(
                'SELECT * FROM ModuleTestResults '+
                'WHERE 1=1 '+
                AdditionalWhere+
                'ORDER BY ' + SortClause,
                {
                    'ModuleID':ModuleID,
                    'TestDate':TestDate
                }
            )
            Rows = self.TestResultEnvironmentObject.LocalDBConnectionCursor.fetchall()

        TableHTMLTemplate = HtmlParser.getSubpart(self.TestResultEnvironmentObject.OverviewHTMLTemplate, '###OVERVIEWTABLE###')
        TableBodyHTMLTemplate = HtmlParser.getSubpart(TableHTMLTemplate, '###BODY###')
        CellLinkHTMLTemplate  = HtmlParser.getSubpart(TableBodyHTMLTemplate, '###LINK###')

        ShowTestCenter = self.TestResultEnvironmentObject.Configuration['SystemConfiguration']['show_test_center']

        TableColumns = [
            {
                'Label':'Module ID',
                'DBColumnName':'ModuleID',
                'InGlobalOverviewList': True
             },
             {
                'Label':'Test Date',
                'DBColumnName':'TestDate',
                'InGlobalOverviewList': True
             },
             {
                'Label':'Analysis',
                'DBColumnName':'KeyValueDictPairs/AnalysisDate',
                'InGlobalOverviewList': True
             },
             {
                'Label':'TestCenter',
                'DBColumnName':'KeyValueDictPairs/TestCenter',
                'InGlobalOverviewList': ShowTestCenter,
                'InFullList': ShowTestCenter,
             },
             {
                'Label':'Qualification Type',
                'DBColumnName':'QualificationType',
                'InGlobalOverviewList': True,
                'InFullList': False
             },
             {
                'Label':'Test Type',
                'DBColumnName':'TestType',
                'InGlobalOverviewList': True
             },
             {
                'Label':'Grade',
                'DBColumnName':'Grade',
                'InGlobalOverviewList': True
             },
             {
                'Label': 'Pixel Defects',
                'DBColumnName':'PixelDefects',
                'InGlobalOverviewList': True
             },
             {
                'Label':'ROCs < 1%',
                'DBColumnName':'ROCsLessThanOnePercent',
                'InGlobalOverviewList': True
             },
             {
                'Label':'ROCs > 1%',
                'DBColumnName':'ROCsMoreThanOnePercent',
                'InGlobalOverviewList': True
             },
             {
                'Label':'ROCs > 4%',
                'DBColumnName':'ROCsMoreThanFourPercent',
                'InGlobalOverviewList': True
             },
             {
                'Label':'Noise',
                'DBColumnName':'Noise',
                'InGlobalOverviewList': True
             },
             {
                'Label':'Trimming',
                'DBColumnName':'Trimming',
                'InGlobalOverviewList': True
             },
             {
                'Label':'PHCalibration',
                'DBColumnName':'PHCalibration',
                'InGlobalOverviewList': True
             },
             {
                'Label':'I(150V)',
                'DBColumnName':'CurrentAtVoltage150V'
             },
             {
                'Label':'I_rec(150V)',
                'DBColumnName':'RecalculatedVoltage'
             },
             {
                'Label':'IV Slope',
                'DBColumnName':'IVSlope'
             },
             {
                'Label':'Temperature',
                'DBColumnName':'Temperature'
             },
             {
                'Label':'initial Current',
                'DBColumnName':'initialCurrent',
                'InGlobalOverviewList': True,
             },
             {
                'Label':'Comments',
                'DBColumnName':'Comments',
                'InGlobalOverviewList': True,
             },
             {
                'Label':'no of Cycles',
                'DBColumnName':'nCycles',
                'InGlobalOverviewList': False,
                'InFullList': False
             },
             {
                'Label':'CycleTempLow',
                'DBColumnName':'CycleTempLow',
                'InGlobalOverviewList': False,
                'InFullList': False,
             },
             {
                'Label':'CycleTempHigh',
                'DBColumnName':'CycleTempHigh',
                'InGlobalOverviewList': False,
                'InFullList': False,
             },

        ]


        TableData = {
            'HEADER':[[]],
            'BODY':[],
            'FOOTER':[],
        }
        TableColumnList = []


        for ColumnDict in TableColumns:
            if ((not GlobalOverviewList and ColumnDict.has_key('InFullList')  and ColumnDict['InFullList'] == True)
                or
                (not GlobalOverviewList and not ColumnDict.has_key('InFullList'))
                or
                (GlobalOverviewList and ColumnDict.has_key('InGlobalOverviewList') and ColumnDict['InGlobalOverviewList'] == True)):
                TableData['HEADER'][0].append(ColumnDict['Label'])
                TableColumnList.append(ColumnDict['DBColumnName'])

        FinalModuleRowsDict = {}
        ModuleIDList = []

        for RowTuple in Rows:
            Identificator = RowTuple['ModuleID']
            if not GlobalOverviewList:
                Identificator+='_%s'%RowTuple['TestType']
                if RowTuple['TestType'] == 'TemperatureCycle':
                    continue
            else:
                Identificator+='_%s'%RowTuple['QualificationType']
#            Identificator+='_%s'%RowTuple['TestDate']
#            print Identificator
            if not FinalModuleRowsDict.has_key(Identificator):
                FinalModuleRowsDict[Identificator] = {}
                ModuleIDList.append(Identificator)
#                print 'added'

                ResultHTMLFileName = 'TestResult.html'
                QualificationGroupSubfolder = 'QualificationGroup'

                RowDict = FinalModuleRowsDict[Identificator]
                for Key in TableColumnList:
                    try:
                        if Key.startswith('KeyValueDictPairs/'):
                            try:
                                KeyValueDictPairsFileName = self.TestResultEnvironmentObject.GlobalOverviewPath+'/'+RowTuple['RelativeModuleFinalResultsPath']+'/'+QualificationGroupSubfolder+'/KeyValueDictPairs.json'
                                with open(KeyValueDictPairsFileName) as data_file:    
                                    KeyValueDictPairs = json.load(data_file)
                                RowDict[Key] = KeyValueDictPairs[Key.split('/')[1]]['Value']
                            except:
                                RowDict[Key] = ''
                        else:
                            RowDict[Key] = RowTuple[Key]
                    except IndexError as e:
                        print 'searched Key:  ',Key
                        print 'existing Keys: ',RowTuple.keys()
                        raise e


                if GlobalOverviewList:
                    Link = os.path.relpath(
                        self.TestResultEnvironmentObject.GlobalOverviewPath+'/'+RowTuple['RelativeModuleFinalResultsPath']+'/'+QualificationGroupSubfolder+'/'+ResultHTMLFileName,
                        self.TestResultEnvironmentObject.GlobalOverviewPath
                        )
                else:
                    CurrentBasePath = self.GlobalOverviewPath + '/' +RowTuple['FulltestSubfolder']
                    # change directory one level up since we are in QualificationGroup folder and FulltestSubfolder is relative to ModuleFinalResultsPath...
                    Link = '../'+RowTuple['FulltestSubfolder'] + '/' + ResultHTMLFileName

                #Link the module ID

                RowDict['ModuleID'] = HtmlParser.substituteMarkerArray(
                        CellLinkHTMLTemplate,
                        {
                            '###URL###':HtmlParser.MaskHTML(Link),
                            '###LABEL###':HtmlParser.MaskHTML(RowTuple['ModuleID'])
                        }
                    )


                # Parse the date
                try:
                    if  type(RowTuple['TestDate']) == str:
                        time = int(re.match(r'\d+', RowTuple['TestDate']).group())
                    else:
                        time = RowTuple['TestDate']
                    RowDict['TestDate'] = datetime.datetime.fromtimestamp(time).strftime("%Y-%m-%d %H:%M")
                except TypeError as e:
                    print e,'\nerror',type(RowTuple['TestDate']),RowTuple['TestDate']
                    RowDict['TestDate'] = datetime.datetime.fromtimestamp(1).strftime("%Y-%m-%d %H:%M")
                    raise e

                try:
                    time = float(RowDict['KeyValueDictPairs/AnalysisDate'])
                    RowDict['KeyValueDictPairs/AnalysisDate'] = datetime.datetime.fromtimestamp(time).strftime("%Y-%m-%d %H:%M")
                except:
                    pass

                if ShowTestCenter:
                    try:
                        RowDict['KeyValueDictPairs/TestCenter'] = "<div style='text-align:center'>" + RowDict['KeyValueDictPairs/TestCenter'] + "</div>"
                    except:
                        pass

            else:
                #TestType
                FinalModuleRowsDict[Identificator]['TestType'] += ' & %s'%RowTuple['TestType']
                if (FinalModuleRowsDict[Identificator]['Grade'] < RowTuple['Grade']):
                    FinalModuleRowsDict[Identificator]['Grade'] = RowTuple['Grade']
                MaxCompareList = ['PixelDefects','Noise','Trimming','PHCalibration']
                for item in MaxCompareList:
                    RowValue = RowTuple[item]
                    FinalValue = FinalModuleRowsDict[Identificator][item]
                    try:
                        RowValue = int(RowValue)
                    except:
                        pass
                    try:
                        FinalValue = int(FinalValue)
                    except:
                        pass
                    FinalModuleRowsDict[Identificator][item] = max(FinalValue, RowValue)

                # ROCsMoreThanFourPercent

                if ((RowTuple['ROCsMoreThanFourPercent'] > FinalModuleRowsDict[Identificator]['ROCsMoreThanFourPercent']) or
                    (RowTuple['ROCsMoreThanFourPercent'] == FinalModuleRowsDict[Identificator]['ROCsMoreThanFourPercent'] and
                        RowTuple['ROCsMoreThanOnePercent'] > FinalModuleRowsDict[Identificator]['ROCsMoreThanOnePercent'])):
                    FinalModuleRowsDict[Identificator]['ROCsMoreThanFourPercent'] = RowTuple['ROCsMoreThanFourPercent']
                    FinalModuleRowsDict[Identificator]['ROCsMoreThanOnePercent'] = RowTuple['ROCsMoreThanOnePercent']
                    FinalModuleRowsDict[Identificator]['ROCsLessThanOnePercent'] = RowTuple['ROCsLessThanOnePercent']


                if RowTuple['Temperature'] and FinalModuleRowsDict[Identificator].has_key('Temperature'):
                   if FinalModuleRowsDict[Identificator]['Temperature']:
                       FinalModuleRowsDict[Identificator]['Temperature'] += " / %s"%RowTuple['Temperature']
                   else:
                       FinalModuleRowsDict[Identificator]['Temperature'] = "%s" % RowTuple['Temperature']
                if RowTuple['initialCurrent'] and FinalModuleRowsDict[Identificator].has_key('initialCurrent'):
                   if FinalModuleRowsDict[Identificator]['initialCurrent']:
                       FinalModuleRowsDict[Identificator]['initialCurrent'] = "%s / %s"%(str(FinalModuleRowsDict[Identificator]['initialCurrent']), RowTuple['initialCurrent'])
                   else:
                       FinalModuleRowsDict[Identificator]['initialCurrent'] = "%s" % RowTuple['initialCurrent']
                if RowTuple['Comments'] and FinalModuleRowsDict[Identificator].has_key('Comments'):
                   if FinalModuleRowsDict[Identificator]['Comments']:
                       FinalModuleRowsDict[Identificator]['Comments'] += " / %s"%RowTuple['Comments']
                   else:
                       FinalModuleRowsDict[Identificator]['Comments'] = "%s"%RowTuple['Comments']
                if RowTuple['nCycles'] and FinalModuleRowsDict[Identificator].has_key('nCycles'):
                   FinalModuleRowsDict[Identificator]['nCycles'] = RowTuple['nCycles']
                   FinalModuleRowsDict[Identificator]['CycleTempLow'] = RowTuple['CycleTempLow']
                   FinalModuleRowsDict[Identificator]['CycleTempHigh'] = RowTuple['CycleTempHigh']

        mapModules = []
        try:
            mapFilePattern = self.TestResultEnvironmentObject.GlobalDataDirectory + '/mount*.txt'
            mapFileNames = glob.glob(mapFilePattern)
            mapName = ''
            if len(mapFileNames) == 1:
                #mapName = mapFileNames[0].split('/').replace('mount_','')[0:-4]
                mapLines = []
                with open(mapFileNames[0], 'r') as mapFile:
                    mapLines = mapFile.readlines()
                mapModuleIDs = [[y.strip() for y in x.split(';')] for x in mapLines if len(x.strip()) > 1]

                LadderNumber = 1
                for mapLine in mapModuleIDs:
                    moduleLinksRow = ['%d'%LadderNumber]
                    for moduleID in mapLine:
                        matchingRows = []
                        for k,v in FinalModuleRowsDict.items():
                            if k.startswith(moduleID):
                                matchingRows.append(v)
                        try:
                            RowDict = matchingRows[0]
                            ModuleLink = RowDict['ModuleID']
                            if 'Grade' in RowDict:
                                if RowDict['Grade'] == 'A':
                                    ModuleLink = "<div style='background-color:#aaffaa'>" + ModuleLink + "</div>"
                                elif RowDict['Grade'] == 'B':
                                    ModuleLink = "<div style='background-color:#eeff99'>" + ModuleLink + "</div>"
                                elif RowDict['Grade'] == 'C':
                                    ModuleLink = "<div style='background-color:#ff8888'>" + ModuleLink + "</div>"

                            moduleLinksRow.append(ModuleLink)

                        except:
                            moduleLinksRow.append(moduleID)
                    mapModules.append(moduleLinksRow)
                    LadderNumber += 1

        except:
            pass

        for ModuleID in ModuleIDList:
            RowDict = FinalModuleRowsDict[ModuleID]

            # if comment for all 3 fulltests is the same, show it only once
            if RowDict['Comments']:
                CommentItems = [x.strip() for x in RowDict['Comments'].split('/')]
                if len(CommentItems) == 3 and CommentItems[0]==CommentItems[1] and CommentItems[1]==CommentItems[2]:
                    RowDict['Comments'] = CommentItems[0]
                elif len(CommentItems) == 2 and CommentItems[0]==CommentItems[1]:
                    RowDict['Comments'] = CommentItems[0]

            Row = []
            for Key in TableColumnList:
                Row.append(RowDict[Key])

            TableData['BODY'].append(Row)

        TableDataObject = {'List': TableData, 'Map': {'BODY': mapModules, 'HEADER': [['','-4','-3','-2','-1','+1','+2','+3','+4']]}}
        return TableDataObject

    def GenerateOverviewHTML(self):
        HtmlParser = self.TestResultEnvironmentObject.HtmlParser

        HTMLTemplate = self.TestResultEnvironmentObject.OverviewHTMLTemplate
        FinalHTML = HTMLTemplate



        # Stylesheet

        StylesheetHTMLTemplate = HtmlParser.getSubpart(HTMLTemplate, '###HEAD_STYLESHEET_TEMPLATE###')
        StylesheetHTML = HtmlParser.substituteMarkerArray(
            StylesheetHTMLTemplate,
            {
                '###STYLESHEET###':self.TestResultEnvironmentObject.MainStylesheet+
                    self.TestResultEnvironmentObject.OverviewStylesheet,
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

        TableHTMLTemplate = HtmlParser.getSubpart(self.TestResultEnvironmentObject.OverviewHTMLTemplate, '###OVERVIEWTABLE###')
        TableDataObject = self.TableData()
        TableHTML = ''
        TableMap = TableDataObject['Map']
        if TableMap:
            TableHTML += HtmlParser.GenerateTableHTML(TableHTMLTemplate, TableMap, {
                '###ADDITIONALCSSCLASS###': '',
                '###ID###': 'OverviewTableMap',
            })
            TableHTML += "<br><br>"

        TableData = TableDataObject['List']
        TableHTML += HtmlParser.GenerateTableHTML(TableHTMLTemplate, TableData, {
                '###ADDITIONALCSSCLASS###':'',
                '###ID###':'OverviewTable',
        })
        FinalHTML = HtmlParser.substituteSubpart(
            FinalHTML,
            '###OVERVIEWTABLE###',
            TableHTML
        )


        return FinalHTML


    def GenerateOverviewHTMLFile(self):
        HTMLFileName = 'Overview.html'
        FinalHTML = self.GenerateOverviewHTML()

        f = open(self.GlobalOverviewPath+'/'+HTMLFileName, 'w')
        f.write(FinalHTML)
        f.close()

