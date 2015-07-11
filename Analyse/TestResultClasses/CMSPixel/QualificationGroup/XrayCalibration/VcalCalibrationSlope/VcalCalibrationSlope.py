import warnings

import ROOT

from  AbstractClasses.GeneralTestResult import GeneralTestResult


class TestResult(GeneralTestResult):
    # AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = "CMSPixel_QualificationGroup_XrayCalibrationSpectrum_VcalCalibrationSlope_TestResult"
        self.NameSingle = "VcalCalibrationSlope"
        self.Title = "Slope of {Method} Vcal Calibration".format(Method=self.Attributes['Method'])
        if self.verbose:
            tag = self.Name + ": Custom Init"
            print "".ljust(len(tag), '=')
            print tag
        self.ResultData["SubTestResultDictList"] = []
        self.check_Test_Software()
        self.Attributes['TestedObjectType'] = 'VcalCalibrationSlope'

    @staticmethod
    def median(l):
        s = sorted(l)
        i = len(s)
        if not i % 2:
            return (s[(i / 2) - 1] + s[i / 2]) / 2.0
        return s[i / 2]

    def PopulateResultData(self):
        if self.verbose:
            tag = self.Name + ": Populate"
            print "".ljust(len(tag), '=')
            print tag
        self.Attributes['nRocs'] = self.ParentObject.nRocs
        slopes = []
        error_slopes = []
        for roc in range(self.Attributes['nRocs']):
            vcal_calibration_module = self.ParentObject.ResultData['SubTestResults']['VcalCalibrationModule']
            key = "VcalCalibration_{Method}_ROC{ROC}".format(Method=self.Attributes['Method'], ROC=roc)
            roc_results = vcal_calibration_module.ResultData['SubTestResults'][key].ResultData
            roc_slope = roc_results['KeyValueDictPairs']['Slope']['Value']
            roc_slope_error = roc_results['KeyValueDictPairs']['Slope']['Sigma']
            error_slopes.append(roc_slope_error)
            if self.verbose:
                print roc, roc_slope, roc_slope_error
            slopes.append(roc_slope)

        self.SpecialPopulateData(self, slopes, error_slopes, {'Key': 'Slope',
                                                              'MarkerColor': ROOT.kPink,
                                                              'LineColor': ROOT.kPink,
                                                              'MarkerStyle': 21,
                                                              'YaxisTitle': 'Slope [e- / Vcal]',
                                                              'MinY': 0,
                                                              'MaxY': 100, })

    def SpecialPopulateData(self, TestResultObject, array, error_array, Parameters):
        TestResultObject.ResultData['Plot']['ROOTObject'] = ROOT.TH1D(self.GetUniqueID(), '',
                                                                      TestResultObject.Attributes['nRocs'], 0,
                                                                      TestResultObject.Attributes['nRocs'])
        with_errors = (len(array) == len(error_array))
        for i in range(len(array)):
            TestResultObject.ResultData['Plot']['ROOTObject'].SetBinContent(i + 1, array[i])
            if with_errors:
                TestResultObject.ResultData['Plot']['ROOTObject'].SetBinError(i + 1, error_array[i])
        mapped_array = map(lambda x: Parameters['MinY'] < x < Parameters['MaxY'], array)
        filtered_array = filter(lambda x: Parameters['MinY'] < x < Parameters['MaxY'], array)
        if TestResultObject.verbose:
            print filtered_array, mapped_array
        invalid_filter = (len(filtered_array) == 0)
        if invalid_filter:
            filtered_array = array
        min_array = min(filtered_array)
        max_array = max(filtered_array)
        median_array = self.median(filtered_array)
        average_array = reduce(lambda x, y: x + y, filtered_array) / len(filtered_array)
        if not 'MinY' in Parameters or not 'MaxY' in Parameters:
            warnings.warn('Cannot find Key in Parameters: {Paras}'.format(Paras=Parameters.keys()))
            if self.verbose:
                raw_input()
        if invalid_filter:
            ymin = min_array
            ymax = max_array
        else:
            ymin = max(min_array, Parameters.get('MinY', -1e9))
            ymax = min(max_array, Parameters.get('MaxY', +1e9))
        if ymin > 0:
            ymin *= .8
        else:
            ymin *= 1.2
        if ymax > 0:
            ymax *= 1.2
        else:
            ymax *= .8

        ROOT.gStyle.SetOptStat(0)
        TestResultObject.ResultData['Plot']['ROOTObject'].SetMarkerColor(Parameters['MarkerColor'])
        TestResultObject.ResultData['Plot']['ROOTObject'].SetLineColor(Parameters['LineColor'])

        TestResultObject.ResultData['Plot']['ROOTObject'].SetMarkerStyle(Parameters['MarkerStyle'])
        TestResultObject.ResultData['Plot']['ROOTObject'].SetMarkerSize(0.5)
        TestResultObject.ResultData['Plot']['ROOTObject'].SetTitle("")
        TestResultObject.ResultData['Plot']['ROOTObject'].GetYaxis().SetRangeUser(ymin, ymax)
        TestResultObject.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("ROC No.")
        TestResultObject.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle(Parameters['YaxisTitle'])
        TestResultObject.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
        TestResultObject.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
        TestResultObject.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
        TestResultObject.ResultData['Plot']['ROOTObject'].Draw('LP')
        Line = ROOT.TLine()
        lineB = Line.DrawLine(0, average_array, TestResultObject.Attributes['nRocs'], average_array)
        lineB.SetLineWidth(2)
        lineB.SetLineStyle(2)
        lineB.SetLineColor(ROOT.kRed)

        TestResultObject.ResultData['KeyValueDictPairs'] = {
            'avrg%s' % Parameters['Key']: {
                "Value": average_array,
                # "Sigma": 0,
                "Label": 'avrg %s' % Parameters['Key'],
                "Unit": "",
            },
            'min%s' % Parameters['Key']: {
                "Value": min_array,
                # "Sigma": 0,
                "Label": 'min %s' % Parameters['Key'],
                "Unit": "",
            },
            'max%s' % Parameters['Key']: {
                "Value": max_array,
                # "Sigma": 0,
                "Label": 'max %s' % Parameters['Key'],
                "Unit": "",
            },
            'median%s' % Parameters['Key']: {
                "Value": median_array,
                # "Sigma": 0,
                "Label": 'median %s' % Parameters['Key'],
                "Unit": "",
            },
            '%ss' % Parameters['Key']: {
                "Value": array,
                "Label": '%ss' % Parameters['Key'],
                "Unit": "",
            }
        }
        TestResultObject.ResultData['KeyList'].append('avrg%s' % Parameters['Key'])
        TestResultObject.ResultData['KeyList'].append('median%s' % Parameters['Key'])
        TestResultObject.ResultData['KeyList'].append('min%s' % Parameters['Key'])
        TestResultObject.ResultData['KeyList'].append('max%s' % Parameters['Key'])

        TestResultObject.SaveCanvas()
        TestResultObject.ResultData['Plot']['Caption'] = Parameters['Key']
        
