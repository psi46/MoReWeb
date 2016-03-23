import math

from AbstractClasses.GeneralTestResult import GeneralTestResult


class TestResult(GeneralTestResult):
    def CustomInit(self):
        self.Name = "CMSPixel_QualificationGroup_XrayCalibration_{Method}_VcalCalibrationModule_TestResult".format(
            Method=self.Attributes['Method'])
        self.NameSingle = "VcalCalibrationModule"
        self.Title = 'Vcal Calibration Module - {Method}'.format(Method=self.Attributes['Method'])
        if self.verbose:
            tag = self.Name + ": Custom Init"
            print "".ljust(len(tag), '=')
            print tag

        # Determine the number or ROCs
        self.nRocs = self.ParentObject.nRocs
        self.ResultData["SubTestResultDictList"] = []

        for roc in range(self.nRocs):
            if self.verbose:
                print 'add subtest for Roc ', roc, "VcalCalibrationROC" + str(roc)
            self.ResultData["SubTestResultDictList"].append(
                {
                    "Key": "VcalCalibration_{Method}_ROC{ROC}".format(Method=self.Attributes['Method'], ROC=roc),
                    "Module": "VcalCalibrationROC",
                    "InitialAttributes": {
                        "StorageKey": "VcalCalibration_{Method}_ROC{ROC}".format(Method=self.Attributes['Method'],
                                                                                 ROC=roc),
                        "TestResultSubDirectory": ".",
                        "IncludeIVCurve": False,
                        "ModuleID": self.Attributes["ModuleID"],
                        "ModuleVersion": self.Attributes["ModuleVersion"],
                        "ModuleType": self.Attributes["ModuleType"],
                        "TestType": "Chips",
                        "TestTemperature": self.Attributes["TestTemperature"],
                        "ChipNo": roc,
                        "Method": self.Attributes['Method'],
                    },
                    "DisplayOptions": {
                        "Order": 1,
                        "Width": 1
                    }
                }
            )
        self.Attributes['TestedObjectType'] = "VcalCalibrationModule"

    def PopulateResultData(self):
        if self.verbose:
            tag = self.Name + ": Populate"
            print "".ljust(len(tag), '=')
            print tag

        self.ResultData['Table'] = {
            'HEADER': [
                [
                    'ROC', 'Slope', 'Slope Error', 'Offset', 'Offset Error'
                ]
            ],
            'BODY': [],
            'FOOTER': [],
        }

        slopes = []
        offsets = []
        error_slopes = []
        error_offsets = []

        slopesGood = []
        offsetsGood = []

        for roc in range(self.nRocs):
            key = "VcalCalibration_{Method}_ROC{ROC}".format(Method=self.Attributes['Method'], ROC=roc)
            roc_results = self.ResultData['SubTestResults'][key].ResultData

            slopes.append(roc_results['KeyValueDictPairs']['Slope']['Value'])
            offsets.append(roc_results['KeyValueDictPairs']['Offset']['Value'])

            error_slopes.append(roc_results['KeyValueDictPairs']['Slope']['Sigma'])
            error_offsets.append(roc_results['KeyValueDictPairs']['Offset']['Sigma'])

            try:
                if float(roc_results['KeyValueDictPairs']['Slope']['Value']) > 0:
                    slopesGood.append(roc_results['KeyValueDictPairs']['Slope']['Value'])
                    offsetsGood.append(roc_results['KeyValueDictPairs']['Offset']['Value'])
            except:
                pass


        for roc in range(self.nRocs):
            if slopes[roc] < 0:
                table_line = ["<span style='color:red'>%d</span>"%roc, "<span style='color:red'>%.1f e- / Vcal</span>" % (slopes[roc]), "<span style='color:red'>%.1f e- / Vcal" % (error_slopes[roc]),
                              "<span style='color:red'>%.1f e-" % (offsets[roc]), "<span style='color:red'>%.1f e-" % (error_offsets[roc])]
            else:
                table_line = [roc, "%.1f e- / Vcal" % (slopes[roc]), "%.1f e- / Vcal" % (error_slopes[roc]),
                              "%.1f e-" % (offsets[roc]), "%.1f e-" % (error_offsets[roc])]

            self.ResultData['Table']['BODY'].append(table_line)

        if self.verbose:
            print self.nRocs
            print 'offset', offsets
            print 'slope', slopes

        if len(slopesGood) == 0:
            average_offset = -1e9
            average_slope = -1e9
            sigma_slope = -1e9
            sigma_offset = -1e9
        else:
            average_offset = reduce(lambda x, y: x + y, offsetsGood)
            average_slope = reduce(lambda x, y: x + y, slopesGood)
            average_slope /= len(slopesGood)
            sigma_slope = math.sqrt(
                reduce(lambda x, y: x + y, map(lambda x: x ** 2, slopesGood)) / len(slopesGood) - average_slope ** 2)
            average_offset /= len(slopesGood)
            sigma_offset = math.sqrt(
                reduce(lambda x, y: x + y, map(lambda x: x ** 2, offsetsGood)) / len(slopesGood) - average_offset ** 2)

        table_line = ["Average", "%.1f e- / Vcal" % average_slope, "", "%.1f e-" % average_offset, ""]
        self.ResultData['Table']['FOOTER'].append(table_line)

        if len(slopesGood) == 0:
            median_slope = -1
            median_offset = -1
        else:
            slopesGood.sort()
            offsetsGood.sort()
            NGoodRocs = len(slopesGood)
            if NGoodRocs % 2 == 1:
                median_slope = slopes[int(NGoodRocs / 2)]
                median_offset = offsets[int(NGoodRocs / 2)]
            elif NGoodRocs > 1:
                median_slope = slopes[int(NGoodRocs / 2)] + slopes[int(NGoodRocs / 2) - 1]
                median_offset = offsets[int(NGoodRocs / 2)] + offsets[int(NGoodRocs / 2) - 1]
            else:
                median_slope = slopes[0]
                median_offset = offsets[0]

        table_line = ["Median", "%.1f e- / Vcal" % median_slope, "", "%.1f e-" % median_offset, ""]
        self.ResultData['Table']['FOOTER'].append(table_line)

        self.ResultData['KeyValueDictPairs'] = {
            'avrg_Slope': {
                'Value': round(average_slope, 3),
                'Label': 'avrg. Slope',
                'Unit': 'nElectrons/VCal',
                'Sigma': round(sigma_slope, 3),
            },
            'avrg_Offset': {
                'Value': round(average_offset, 3),
                'Label': 'avrg. Offset',
                'Unit': 'nElectrons',
                'Sigma': round(sigma_offset, 3),
            },

        }
        # self.ResultData['KeyList'] = ['avrg_Slope', 'avrg_Offset']