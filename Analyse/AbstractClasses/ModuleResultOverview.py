'''
Program : MORE-Web 
 Author : Esteban Marin - estebanmarin@gmx.ch
 Version    : 2.1
 Release Date   : 2013-05-30
'''
import AbstractClasses.Helper.HtmlParser
import datetime
import os
class ModuleResultOverview:
    def __init__(self, TestResultEnvironmentObject):
        self.TestResultEnvironmentObject = TestResultEnvironmentObject
        self.StoragePath = self.TestResultEnvironmentObject.OverviewPath
        
    def TableData(self, ModuleID = None, TestDate = None, ShrinkedList = True):
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
                'ORDER BY ModuleID ASC,TestType ASC ',
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
                'InShrinkedList': True
             },
             {
                'Label':'Test Date',
                'DBColumnName':'TestDate',
                'InShrinkedList': True
             },
             {
                'Label':'Qualification Type',
                'DBColumnName':'QualificationType',
                'InShrinkedList': True,
                'InFullList': False
             },
             {
                'Label':'Test Type',
                'DBColumnName':'TestType',
                'InShrinkedList': True
             },
             {
                'Label':'Grade',
                'DBColumnName':'Grade',
                'InShrinkedList': True
             },
             {
                'Label': 'Pixel Defects',
                'DBColumnName':'PixelDefects',
                'InShrinkedList': True
             },
             {
                'Label':'ROCs > 1%',
                'DBColumnName':'ROCsMoreThanOnePercent',
                'InShrinkedList': True
             },
             {
                'Label':'Noise',
                'DBColumnName':'Noise',
                'InShrinkedList': True
             },
             {
                'Label':'Trimming',
                'DBColumnName':'Trimming',
                'InShrinkedList': True
             },
             {
                'Label':'PHCalibration',
                'DBColumnName':'PHCalibration',
                'InShrinkedList': True
             },
             {
                'Label':'I(150V)',
                'DBColumnName':'CurrentAtVoltage150'
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
                'InShrinkedList': True,
             },
             {
                'Label':'no of Cycles',
                'DBColumnName':'nCycles',
                'InShrinkedList': True,
                'InFullList': False
             },
             {
                'Label':'CycleTempLow',
                'DBColumnName':'CycleTempLow',
                'InShrinkedList': True,
                'InFullList': False,
             },    
             {
                'Label':'CycleTempHigh',
                'DBColumnName':'CycleTempHigh',
                'InShrinkedList': True,
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
            if ((not ShrinkedList and ColumnDict.has_key('InFullList')  and ColumnDict['InFullList'] == True)
                or
                (not ShrinkedList and not ColumnDict.has_key('InFullList'))
                or 
                (ShrinkedList and ColumnDict.has_key('InShrinkedList') and ColumnDict['InShrinkedList'] == True)):
                TableData['HEADER'][0].append(ColumnDict['Label'])
                TableColumnList.append(ColumnDict['DBColumnName'])
        
        FinalModuleRowsDict = {}
        ModuleIDList = []
            
        for RowTuple in Rows:
            Identificator = RowTuple['ModuleID']
            if not ShrinkedList:
                Identificator+='_%s'%RowTuple['TestType']
                if RowTuple['TestType'] == 'TemperatureCycle':
                    continue
            else:
                Identificator+='_%s'%RowTuple['QualificationType']
#            Identificator+='_%s'%RowTuple['TestDate']
            print Identificator
            if not FinalModuleRowsDict.has_key(Identificator):
                FinalModuleRowsDict[Identificator] = {}
                ModuleIDList.append(Identificator)    
                print 'added'
    
                RowDict = FinalModuleRowsDict[Identificator]
                for Key in TableColumnList:
                    RowDict[Key] = RowTuple[Key]
                    
                ModuleGroupPath =  'FinalResults/ModuleTestGroup/'
                if not ShrinkedList:
                    print RowTuple['RelativeModuleFulltestStoragePath']
                    ModuleGroupPath = RowTuple['RelativeModuleFulltestStoragePath']
                if not ModuleGroupPath:
                    print 'Problem with',RowTuple
                    
                ResultHTMLFileName = 'TestResult.html'
   
                Link = os.path.relpath(
                    self.TestResultEnvironmentObject.OverviewPath+'/'+RowTuple['StorageFolder']+'/'+ModuleGroupPath+'/'+ResultHTMLFileName,
                    self.StoragePath
                )
                
                #Link the module ID
                
                RowDict['ModuleID'] = HtmlParser.substituteMarkerArray(
                        CellLinkHTMLTemplate,
                        {
                            '###URL###':HtmlParser.MaskHTML(Link),
                            '###LABEL###':HtmlParser.MaskHTML(RowTuple['ModuleID'])                   
                        }
                    )
                
                
                # Parse the date
                RowDict['TestDate'] = datetime.datetime.fromtimestamp(RowTuple['TestDate']).strftime("%Y-%m-%d %H:%m")
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
                           FinalModuleRowsDict[Identificator]['Temperature'] = "%s"%RowTuple['Temperature'] 
                 if RowTuple['initialCurrent'] and FinalModuleRowsDict[Identificator].has_key('initialCurrent'):
                       if FinalModuleRowsDict[Identificator]['initialCurrent']:      
                           FinalModuleRowsDict[Identificator]['initialCurrent'] += " / %s"%RowTuple['initialCurrent']
                       else:
                           FinalModuleRowsDict[Identificator]['initialCurrent'] = "%s"%RowTuple['initialCurrent'] 
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
        
        f = open(self.StoragePath+'/'+HTMLFileName, 'w')
        f.write(FinalHTML)
        f.close()
    
