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
        
    def TableData(self, ModuleID = None, TestDate = None):
        HtmlParser = self.TestResultEnvironmentObject.HtmlParser
        
        
        
        if self.TestResultEnvironmentObject.Configuration['Database']['UseGlobal']:
            Rows = {}
        else:
            AdditionalWhere = ''
            if ModuleID:
                AdditionalWhere += ' AND ModuleID=:ModuleID '
            if TestDate:
                AdditionalWhere += ' AND TestDate=:TestDate '
            Rows = self.TestResultEnvironmentObject.LocalDBConnectionCursor.execute(
                'SELECT * FROM ModuleTestResults '+
                'WHERE 1=1 '+
                AdditionalWhere+
                'ORDER BY ModuleID ASC,TestType ASC',
                {
                    'ModuleID':ModuleID,
                    'TestDate':TestDate
                }
            )
            
        TableHTMLTemplate = HtmlParser.getSubpart(self.TestResultEnvironmentObject.OverviewHTMLTemplate, '###OVERVIEWTABLE###')
        TableBodyHTMLTemplate = HtmlParser.getSubpart(TableHTMLTemplate, '###BODY###')
        CellLinkHTMLTemplate  = HtmlParser.getSubpart(TableBodyHTMLTemplate, '###LINK###')
        
        
        TableData = {
            'HEADER':[
                [
                    'Module ID',
                    'Test Date',
                    'Test Type',
                    'Grade',
                    'Pixel Defects',
                    'ROCs > 1%',
                    'Noise',
                    'Trimming',
                    'PHCalibration',
                    'I(150V)',
                    'IV Slope',
                    'Temperature',
                    'Comments',
                ]
            ],
            'BODY':[],
            'FOOTER':[],
        }
        
        for RowTuple in Rows:
            Row = list(RowTuple)
            ModuleGroupPath = 'FinalResults/ModuleTestGroup/ModuleFulltest_'+Row[2]
            ResultHTMLFileName = 'TestResult.html'
        
            Link = os.path.relpath(
                self.TestResultEnvironmentObject.OverviewPath+'/'+Row[12]+'/'+ModuleGroupPath+'/'+ResultHTMLFileName,
                self.StoragePath
            )
            
            #Link the module ID
            
            Row[0] = HtmlParser.substituteMarkerArray(
                CellLinkHTMLTemplate,
                {
                    '###URL###':HtmlParser.MaskHTML(Link),
                    '###LABEL###':HtmlParser.MaskHTML(Row[0])                   
                }
            )
            
            # Parse the date
            Row[1] = datetime.datetime.fromtimestamp(Row[1]).strftime("%Y-%m-%d %H:%m")
            
            
            # delete the storage folder
            del Row[12]
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
    
