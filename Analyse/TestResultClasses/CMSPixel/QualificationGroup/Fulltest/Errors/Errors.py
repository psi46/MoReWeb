# -*- coding: utf-8 -*-
import ROOT
import array
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter

import ROOT
import datetime
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.NameSingle='Errors'
        self.Name='CMSPixel_QualificationGroup_Fulltest_Chips_Chip_%s_TestResult'%self.NameSingle
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'

    def PopulateResultData(self):

        # lists of strings to search for in .log file
        DetectMessages = {
            'tokenchain': ['Token Chain Length'],
            'eventid': ['Event ID mismatch'],
            'readback': ['Readback start marker'],
            'notokenpass': ['has NoTokenPass but'],
            'datasize': ['Data size does not correspond to'],
            'missingevents': ['Incomplete DAQ data readout'],
            'usbtimeout': ['Timeout reading from USB buffer after'],
            'deser400': ['header reports DESER400 failure'],
            'daqerror': ['Error in DAQ. Aborting test.'],
            'deser400_no_data': ['Detected DESER400 trailer error bits: "NO DATA"'],
            'deser400_idle_data': ['Detected DESER400 trailer error bits: "IDLE DATA"'],
            'deser400_code_error': ['Detected DESER400 trailer error bits: "CODE ERROR"'],
            'deser400_frame_error': ['Detected DESER400 trailer error bits: "FRAME ERROR"'],
            'pkam': ['detected a PKAM reset, event cleared'],
        }

        # optional: name dictionary of the errors displayed in the summary
        ErrorNames = {
            'tokenchain': 'Token Chain Length',
            'eventid': 'Event ID mismatch',
            'readback': 'Readback start marker',
            'notokenpass': 'has NoTokenPass',
            'datasize': 'Data size criticals',
            'missingevents': 'Missing Event criticals ',
            'usbtimeout': 'USB criticals',
            'deser400': 'DESER400 failure',
            'daqerror': 'DAQ error',
            'deser400_no_data': 'DESER400 NO DATA',
            'deser400_idle_data': 'DESER400 IDLE DATA',
            'deser400_code_error': 'DESER400 CODE ERROR',
            'deser400_frame_error': 'DESER400 FRAME ERROR',
            'pkam': 'PKAM reset',
        }

        LogfileErrors = self.AnalyzeLogfiles(self.ParentObject.logfilePath, DetectMessages, ErrorNames)
        self.ResultData['KeyValueDictPairs'] = LogfileErrors['KeyValueDictPairs']
        self.ResultData['KeyList'] = LogfileErrors['KeyList']
