# -*- coding: utf-8 -*-
import AbstractClasses
import os

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.NameSingle='Logfile'
        self.Name='CMSPixel_QualificationGroup_XRayHRQualification_%s_TestResult'%self.NameSingle
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'

        try:
            self.ParentObject.logfilePaths.sort(key=lambda x: int(x.replace('\\','/').strip('/').split('/')[-2].split('_')[0]))
        except:
            print "Logfiles can not be sorted, all subfolders should be named ***_Name with *** a number."

        for LogfilePath in self.ParentObject.logfilePaths:
            self.ResultData['SubTestResultDictList'] += [
                {
                    'Key': 'LogfileView',
                    'Module': 'LogfileView',
                    'InitialAttributes': {
                        'LogfilePath' : LogfilePath
                    },
                    'DisplayOptions': {
                        'Order': 100,
                        'Width': 5,
                        'Show': True,
                    }
                },
            ]

        self.ResultData['KeyValueDictPairs'] = {
            'DTB_FW': {'Value': '', 'Label': 'DTB FW'},
            'pXar': {'Value': '', 'Label': 'pXar version'}
        }

    def PopulateResultData(self):

        if len(self.ParentObject.logfilePaths) > 0:
            LogfileName = self.ParentObject.logfilePaths[0]

            if LogfileName:
                if os.path.isfile(LogfileName):
                    DTBSectionFound = False
                    FWFound = False
                    pXarFound = False

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
                                if posPxar >=0:
                                    try:
                                        self.ResultData['KeyValueDictPairs']['pXar']['Value'] = Line[posPxar + 5:] if len(Line) > posPxar + 5 else '?'
                                        pXarFound = True
                                    except:
                                        pass

                            if FWFound and pXarFound:
                                break
