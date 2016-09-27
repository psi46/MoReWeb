# -*- coding: utf-8 -*-
import AbstractClasses
import os

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.NameSingle = 'Logfile'
        self.Name = 'CMSPixel_QualificationGroup_OnShellQuickTest_Chips_Chip_%s_TestResult'%self.NameSingle
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
        self.ResultData['SubTestResultDictList'] += [
            {
                'Key': 'LogfileView',
                'Module': 'LogfileView',
                'InitialAttributes': {
                },
                'DisplayOptions': {
                    'Order': 100,
                    'Width': 5,
                    'Show': True,
                }
            },
        ]
        self.ResultData['KeyValueDictPairs'] = {'DTB_FW': {'Value': '', 'Label': 'DTB FW'}, 'pXar': {'Value': '', 'Label': 'pXar version'}}
        self.ResultData['KeyList'] = []

        self.ResultData['HiddenData']['IanaProblem'] = False

    def PopulateResultData(self):

        LogfileName = self.ParentObject.logfilePath
        if LogfileName:
            if os.path.isfile(LogfileName):
                DTBSectionFound = False
                FWFound = False
                pXarFound = False
                IanaLossFound = False

                with open(LogfileName) as Logfile:
                    for Line in Logfile:
                        if 'DTB info' in Line:
                            DTBSectionFound = True
                        if DTBSectionFound and 'SW version' in Line:
                            try:
                                self.ResultData['KeyValueDictPairs']['DTB_FW']['Value'] = Line.split(':')[-1].strip()
                                FWFound = True
                            except:
                                pass

                        if 'Instanciating API for pxar' in Line:
                            posPxar = Line.find('pxar')
                            if posPxar >= 0:
                                try:
                                    self.ResultData['KeyValueDictPairs']['pXar']['Value'] = Line[posPxar + 5:] if len(Line) > posPxar + 5 else '?'
                                    pXarFound = True
                                except:
                                    pass

                        if 'i(loss) [mA/ROC]' in Line:
                            pos = Line.rfind(':')
                            currentLossRoc = [float(x.replace('->','').replace('<-','')) for x in Line[pos+1:].split(' ') if len(x.strip()) > 0]
                            if '->' in Line[pos+1:]:
                                self.ResultData['HiddenData']['IanaProblem'] = True
                            self.ResultData['HiddenData']['IanaLossRoc'] = currentLossRoc

                        if FWFound and pXarFound and IanaLossFound:
                            break


