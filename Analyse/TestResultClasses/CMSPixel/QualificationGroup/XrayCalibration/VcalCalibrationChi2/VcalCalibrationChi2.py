import AbstractClasses
import ROOT


class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.method = self.Attributes['Method']
        self.Name = "CMSPixel_QualificationGroup_XrayCalibrationSpectrum_VcalCalibrationChi2_TestResult"
        self.NameSingle = "VcalCalibrationChi2"
        self.Title = "Chi2 of {Method} Vcal Calibration".format(Method=self.method)
        if self.verbose:
            tag = self.Name + ": Custom Init"
            print "".ljust(len(tag), '=')
            print tag
        self.ResultData["SubTestResultDictList"] = []
        self.check_Test_Software()
        self.Attributes['TestedObjectType'] = 'VcalCalibrationModule'

    def PopulateResultData(self):
        if self.verbose:
            tag = self.Name + ": Populate"
            print "".ljust(len(tag), '=')
            print tag
        self.Attributes['nRocs'] = self.ParentObject.nRocs
        chi2s = []
        error_chi2s = []
        for roc in range(self.Attributes['nRocs']):
            vcal_calibration_module = self.ParentObject.ResultData['SubTestResults']['VcalCalibrationModule']
            key = "VcalCalibration_{Method}_ROC{ROC}".format(Method=self.Attributes['Method'], ROC=roc)
            roc_results = vcal_calibration_module.ResultData['SubTestResults'][key].ResultData
            roc_chi2 = roc_results['KeyValueDictPairs']['chi2']['Value']
            roc_chi2_error = roc_results['KeyValueDictPairs']['chi2']['Sigma']
            if self.verbose:
                print roc, roc_chi2, roc_chi2_error
            chi2s.append(roc_chi2)
            error_chi2s.append(roc_chi2_error)
        vcal_calibration = self.ParentObject.ResultData['SubTestResults']['VcalCalibrationSlope_' + self.method]
        vcal_calibration.SpecialPopulateData(self, chi2s, error_chi2s, {'Key': 'chi2',
                                                                        'MarkerColor': ROOT.kPink,
                                                                        'LineColor': ROOT.kPink,
                                                                        'MarkerStyle': 21,
                                                                        'YaxisTitle': 'chi2/ NDF]',
                                                                        'MinY': 0,
                                                                        'MaxY': +10000, })