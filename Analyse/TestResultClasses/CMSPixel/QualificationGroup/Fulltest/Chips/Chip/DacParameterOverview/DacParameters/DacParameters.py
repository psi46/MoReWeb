# -*- coding: utf-8 -*-
import AbstractClasses


class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_Fulltest_Chips_Chip_DacParameterOverview_DacParameters_TrimBitParameters' + str(
            self.Attributes['DacParameterTrimValue']) + '_TestResult'
        self.NameSingle = 'DacParameters' + str(self.Attributes['DacParameterTrimValue'])
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'
        if self.Attributes['DacParameterTrimValue'] != '':
            self.Title = 'DacParameters - Trim ' + str(self.Attributes['DacParameterTrimValue'])
        else:
            self.Title = 'DacParameters - Raw'
        self.FileHandle = self.Attributes['DacParametersFile']

    def PopulateResultData(self):
        ChipNo = self.ParentObject.ParentObject.Attributes['ChipNo']
        DacParametersFile = self.Attributes['DacParametersFile']

        if not DacParametersFile:
            raise Exception('Cannot find DacParametersFile')
        else:
            trim = self.Attributes['DacParameterTrimValue']
            if trim == '':
                trim = -1
            self.ResultData['KeyValueDictPairs']['TrimValue'] = {
                'Value': '{0:}'.format(trim),
                'Label': 'TrimValue'
            }
            self.ResultData['KeyList'] += ['TrimValue']
            for Line in DacParametersFile:
                LineArray = Line.strip().split()
                DacParameterName = LineArray[1]

                DacParameterValue = int(LineArray[2])
                self.ResultData['KeyValueDictPairs'][DacParameterName.lower()] = {
                    'Value': '{0:1.0f}'.format(DacParameterValue),
                    'Label': DacParameterName
                }
                self.ResultData['KeyList'] += [DacParameterName.lower()]
            key = 'TrimBitParameters' + self.Attributes['DacParameterTrimValue']
            object = \
                self.ParentObject.ParentObject.ResultData['SubTestResults']['TrimBits'].ResultData['SubTestResults'][
                    key]
            self.ResultData['KeyValueDictPairs']['TrimBits_mu'] = object.ResultData['KeyValueDictPairs']['mu']
            self.ResultData['KeyValueDictPairs']['TrimBits_mu']['Label'] = 'TrimBit Mean'
            self.ResultData['KeyValueDictPairs']['TrimBits_sigma'] = object.ResultData['KeyValueDictPairs']['sigma']
            self.ResultData['KeyValueDictPairs']['TrimBits_sigma']['Label'] = 'TrimBit sigma'
            self.ResultData['KeyList'] += ['TrimBits_mu', 'TrimBits_sigma']
