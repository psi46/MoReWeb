# -*- coding: utf-8 -*-
import AbstractClasses
import os
import cgi

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_Fulltest_Logfile_LogfileView_TestResult'
        self.NameSingle = 'LogfileView'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'
        self.sizeLimit = 5*1024*1024

    def PopulateResultData(self):
        LogfileName = self.ParentObject.ParentObject.logfilePath
        if LogfileName:
            if os.path.isfile(LogfileName):
                if os.path.getsize(LogfileName) < self.sizeLimit:
                    try:
                        with open(LogfileName) as Logfile:
                            Lines = Logfile.readlines()
                    except:
                        Lines = ["ERROR: could not open '%s'"%LogfileName]
                else:
                    Lines = ["ERROR: log file too large '%s'. Max allowed: %s Bytes"%(LogfileName, self.sizeLimit)]

                LinesFormatted = []
                for Line in Lines:
                    escapedLine = cgi.escape(Line)
                    if 'CRITICAL:' in Line:
                        escapedLine = "<div style='display:inline;background-color:#f66;'>" + escapedLine + "</div>"
                    if 'ERROR:' in Line:
                        escapedLine = "<div style='display:inline;background-color:#f96;'>" + escapedLine + "</div>"
                    if 'WARNING:' in Line:
                        escapedLine = "<div style='display:inline;background-color:#ff6;'>" + escapedLine + "</div>"
                    LinesFormatted.append(escapedLine)

                HTML = "<div style='font-family:\"Courier New\";'>" + '<br>'.join(LinesFormatted) + "</div>"
                self.ResultData['HTMLContent'] = HTML


