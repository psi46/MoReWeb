import AbstractClasses.Helper.HtmlParser
import re
import datetime
import os
class ModuleResultOverview:
    def __init__(self, TestResultEnvironmentObject):
        self.TestResultEnvironmentObject = TestResultEnvironmentObject
        self.GlobalOverviewPath = self.TestResultEnvironmentObject.GlobalOverviewPath

    def TableData(self, ModuleID = None, TestDate = None, GlobalOverviewList = True):
        HtmlParser = self.TestResultEnvironmentObject.HtmlParser

        if self.TestResultEnvironmentObject.Configuration['Database']['UseGlobal']:
            Rows = {}
        else:
            AdditionalWhere = ''
            if ModuleID:
                AdditionalWhere += ' AND ModuleID=:ModuleID '
            if TestDate:
                AdditionalWhere += ' AND TestDate=:TestDate '
            self.TestResultEnvironmentObject.LocalDBConnectionCursor.execute(
                'SELECT * FROM ModuleTestResults '+
                'WHERE 1=1 '+
                AdditionalWhere+
                'ORDER BY ModuleID ASC,TestType ASC,TestDate ASC ',
                {
                    'ModuleID':ModuleID,
                    'TestDate':TestDate
                }
            )
            Rows = self.TestResultEnvironmentObject.LocalDBConnectionCursor.fetchall()

        TableHTMLTemplate = HtmlParser.getSubpart(self.TestResultEnvironmentObject.OverviewHTMLTemplate, '###OVERVIEWTABLE###')
        TableBodyHTMLTemplate = HtmlParser.getSubpart(TableHTMLTemplate, '###BODY###')
        CellLinkHTMLTemplate  = HtmlParser.getSubpart(TableBodyHTMLTemplate, '###LINK###')

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
                'Label':'ROCs > 1%',
                'DBColumnName':'ROCsMoreThanOnePercent',
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
             },
             {
                'Label':'Comments',
                'DBColumnName':'Comments',
                'InGlobalOverviewList': True,
             },
             {
                'Label':'no of Cycles',
                'DBColumnName':'nCycles',
                'InGlobalOverviewList': True,
                'InFullList': False
             },
             {
                'Label':'CycleTempLow',
                'DBColumnName':'CycleTempLow',
                'InGlobalOverviewList': True,
                'InFullList': False,
             },
             {
                'Label':'CycleTempHigh',
                'DBColumnName':'CycleTempHigh',
                'InGlobalOverviewList': True,
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

                RowDict = FinalModuleRowsDict[Identificator]
                for Key in TableColumnList:
                    try:
                        RowDict[Key] = RowTuple[Key]
                    except IndexError as e:
                        print 'searched Key:  ',Key
                        print 'existing Keys: ',RowTuple.keys()
                        raise e

                ResultHTMLFileName = 'TestResult.html'
                QualificationGroupSubfolder = 'QualificationGroup'


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
                    RowDict['TestDate'] = datetime.datetime.fromtimestamp(time).strftime("%Y-%m-%d %H:%m")
                except TypeError as e:
                    print e,'\nerror',type(RowTuple['TestDate']),RowTuple['TestDate']
                    RowDict['TestDate'] = datetime.datetime.fromtimestamp(1).strftime("%Y-%m-%d %H:%m")
                    raise e

            else:
#                TestType
                 FinalModuleRowsDict[Identificator]['TestType'] += ' & %s'%RowTuple['TestType']
                 if ( FinalModuleRowsDict[Identificator]['Grade'] < RowTuple['Grade']):
                      FinalModuleRowsDict[Identificator]['Grade'] = RowTuple['Grade']
                 MaxCompareList = ['PixelDefects','ROCsMoreThanOnePercent','Noise','Trimming','PHCalibration']
                 for item in MaxCompareList:
                     FinalModuleRowsDict[Identificator][item] = max( FinalModuleRowsDict[Identificator][item],RowTuple[item])
                 if RowTuple['Temperature'] and FinalModuleRowsDict[Identificator].has_key('Temperature'):
                       if FinalModuleRowsDict[Identificator]['Temperature']:
                           FinalModuleRowsDict[Identificator]['Temperature'] += " / %s"%RowTuple['Temperature']
                       else:
                           FinalModuleRowsDict[Identificator]['Temperature'] = "%s" % RowTuple['Temperature']
                 if RowTuple['initialCurrent'] and FinalModuleRowsDict[Identificator].has_key('initialCurrent'):
                       if FinalModuleRowsDict[Identificator]['initialCurrent']:
                           FinalModuleRowsDict[Identificator]['initialCurrent'] += " / %s"%RowTuple['initialCurrent']
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

        for ModuleID in ModuleIDList:
            RowDict = FinalModuleRowsDict[ModuleID]
            Row = []
            for Key in TableColumnList:
                Row.append(RowDict[Key])
            TableData['BODY'].append(Row)


        return TableData

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

        TableData = self.TableData()
        TableHTMLTemplate = HtmlParser.getSubpart(self.TestResultEnvironmentObject.OverviewHTMLTemplate, '###OVERVIEWTABLE###')

        TableHTML = HtmlParser.GenerateTableHTML(TableHTMLTemplate, TableData, {
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

