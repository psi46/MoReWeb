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
        ROOT.gStyle.SetOptStat(0)

        ErrorObjects = []

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
        }

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
        }

        self.ResultData['KeyValueDictPairs'] = {}
        self.ResultData['KeyList'] = []

        with open(self.ParentObject.logfilePath, 'r') as logfile:
            for line in logfile:
                ErrorObject = {}

                if 'WARNING:' in line and not 'Not unmasking DUT' in line:
                    ErrorObject['type'] = 'warning'
                if 'ERROR:' in line:
                    ErrorObject['type'] = 'error'
                if 'CRITICAL:' in line:
                    ErrorObject['type'] = 'critical'

                ErrorObject['channel'] = None
                lineParts = line.strip().split()
                if 'Channel' in lineParts:
                    pos = lineParts.index('Channel')
                    if pos < len(lineParts) - 1:
                        try:
                            ErrorObject['channel'] = int(lineParts[pos+1])
                        except:
                            pass

                if ErrorObject.has_key('type'):
                    Found = False
                    for errorname, keywords in DetectMessages.iteritems():
                        for keyword in keywords:
                            if keyword in line:
                                ErrorObject['subtype'] = errorname
                                Found = True
                                break
                    if not Found:
                        ErrorObject['subtype'] = 'other'

                    ErrorObjects.append(ErrorObject)


        self.ResultData['KeyValueDictPairs']['nCriticals'] = {'Label': '# Criticals', 'Value': '%d'%len([True for ErrorObject in ErrorObjects if ErrorObject['type'] == 'critical'])}
        self.ResultData['KeyValueDictPairs']['nErrors'] = {'Label': '# Errors', 'Value': '%d'%len([True for ErrorObject in ErrorObjects if ErrorObject['type'] == 'error'])}
        self.ResultData['KeyValueDictPairs']['nWarnings'] = {'Label': '# Warnings', 'Value': '%d'%len([True for ErrorObject in ErrorObjects if ErrorObject['type'] == 'warning'])}

        for ch in range(4):
            self.ResultData['KeyValueDictPairs']['channel_%d_count'%ch] = {'Label': 'Channel %d'%ch, 'Value': '%d'%len([True for ErrorObject in ErrorObjects if ErrorObject['channel'] == ch])}

        for errorSubtype, keywords in DetectMessages.iteritems():
            self.ResultData['KeyValueDictPairs']['message_%s_count'%errorSubtype] = {'Label': ErrorNames[errorSubtype] if errorSubtype in ErrorNames else errorSubtype, 'Value': '%d'%len([True for ErrorObject in ErrorObjects if ErrorObject['subtype'] == errorSubtype])}

        self.ResultData['KeyList'] = (['nCriticals', 'nErrors', 'nWarnings', 'channel_0_count', 'channel_1_count', 'channel_2_count', 'channel_3_count', 'message_tokenchain_count', 
            'message_eventid_count', 'message_readback_count', 'message_notokenpass_count', 'message_datasize_count', 'message_missingevents_count', 'message_usbtimeout_count', 'message_deser400_count', 'message_daqerror_count'])

