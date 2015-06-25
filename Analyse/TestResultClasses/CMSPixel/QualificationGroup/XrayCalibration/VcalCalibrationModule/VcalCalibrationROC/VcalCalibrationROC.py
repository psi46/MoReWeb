import AbstractClasses
import warnings
import ROOT
import array
from AbstractClasses.GeneralTestResult import GeneralTestResult


class TestResult(GeneralTestResult):
    def CustomInit(self):
        #self.verbose = True
        self.Name = "CMSPixel_QualificationGroup_XrayCalibration_{Method}".format(Method=self.Attributes['Method'])
        self.Name += "_VcalCalibrationModule_VcalCalibrationROC_TestResult"
        self.NameSingle = "VcalCalibrationROC"
        self.Title = "Vcal Calibration ROC {ROC} - Method {Method}".format(ROC=self.Attributes['ChipNo'],
                                                                           Method=self.Attributes['Method'])
        if self.verbose:
            tag = self.Name + ": Custom Init"
            print "".ljust(len(tag), '=')
            print tag
        self.Attributes['TestedObjectType'] = 'VcalCalibrationROC'
        self.check_Test_Software()

    def PopulateResultData(self):
        if self.verbose:
            tag = self.Name + ' - ROC ' + '%d' % self.Attributes['ChipNo'] + ": Populate"
            print "".ljust(len(tag), '=')
            print tag

        fit_option = "Q"

        if self.HistoDict.getboolean('XrayCalibration','LinearFitAdditionalConstraints'):
            fit_option += "B"

        peak_centers = array.array('d', [])
        peak_errors = array.array('d', [])
        n_electrons = array.array('d', [])
        top_parent = self.ParentObject.ParentObject
        trimming = []
        if self.HistoDict.has_option('XrayCalibration','IgnoredTarges'):
            ignored_targets = map(lambda x: x.strip().lower(),self.HistoDict.get('XrayCalibration','IgnoredTarges').split(','))
        else:
            ignored_targets = []
        # print 'Ignoring the following targets: ',ignored_targets
        for test in top_parent.ResultData['SubTestResults']:
            if not "FluorescenceTargetModule" in test:
                continue
            module_results = top_parent.ResultData['SubTestResults'][test].ResultData['SubTestResults']

            try:
                roc_results = module_results['FluorescenceTarget_C%i' % (self.Attributes["ChipNo"])]
            except KeyError as e:
                print 'Cannot find key FluorescenceTarget_C%i in %s'%(self.Attributes['ChipNo'],module_results.keys())
                raise e
            trim = roc_results.Attributes['TrimValue']
            trimming.append(trim)
            key_value_pairs = roc_results.ResultData['KeyValueDictPairs']
            target = key_value_pairs['Target']['Value']
            if target.lower() in ignored_targets:
                print 'ignoring Target: ', target
                continue
            if self.verbose:
                print test, trim, key_value_pairs['Center']['Value'], key_value_pairs['TargetNElectrons']['Value']
                print key_value_pairs.keys()
            peak_centers.append(key_value_pairs['Center']['Value'])
            peak_errors.append(key_value_pairs['Center']['Sigma'])
            n_electrons.append(key_value_pairs['TargetNElectrons']['Value'])
        point_pairs = zip(peak_centers, n_electrons, peak_errors)
        sorted_points = sorted(point_pairs, key=lambda point: point[1])
        # print sorted_points, trimming
        maxTrim = 0
        for e in sorted_points:
            num = sorted_points.index(e)
            trim = trimming[num]
            maxTrim = max(maxTrim, trim)
            if e[0] <= trim:
                # sorted_points.pop(num)
                warnings.warn('Datapoint #{num}, Vcal: {Vcal}, Energy: {Energy} close to Threshold'.format(num=num,
                                                                                                           Vcal=e[0],
                                                                                                           Energy=e[1]))

        new_sorted_points = sorted(sorted_points, key=lambda point: point[0])
        sorted_peak_centers = array.array('d', [])
        sorted_n_electrons = array.array('d', [])
        sorted_peak_errors = array.array('d', [])
        sorted_electron_error = array.array('d', [])
        for e in new_sorted_points:
            sorted_peak_centers.append(e[0])
            sorted_n_electrons.append(e[1])
            sorted_peak_errors.append(e[2])
            sorted_electron_error.append(0.0)

        self.ResultData['Plot']['ROOTObject'] = ROOT.TGraphErrors(len(sorted_peak_centers), sorted_peak_centers,
                                                                  sorted_n_electrons, sorted_peak_errors,
                                                                  sorted_electron_error)
        title = "Center of Pulse Height (Vcal units) vs number of electrons;"
        title += "Center of Pulse Height[Vcal];"
        title += "Number of Electrons"
        self.ResultData['Plot']['ROOTObject'].SetTitle(title)
        self.ResultData['Plot']['ROOTObject'].SetMarkerColor(4)
        self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.6)
        # self.ResultData['Plot']['ROOTObject'].SetMarkerStyle(21)

        # Fitting of Slope
        maxTrim *= 1.05  # todo: THink about a good value where you dont wanna fit...
        xmin = max(maxTrim, sorted_peak_centers[0])
        pol1TF1 = ROOT.TF1("pol1tf1","pol1", xmin, sorted_peak_centers[len(sorted_peak_centers) - 1]);

        pol1TF1.SetParameter(0, 0)
        pol1TF1.SetParameter(1, 50)

        if self.HistoDict.getboolean('XrayCalibration','LinearFitAdditionalConstraints'):
            pol1TF1.SetParLimits(0, -2000, 2000)
            pol1TF1.SetParLimits(1, 5, 500)

        self.ResultData['Plot']['ROOTObject'].Fit(pol1TF1, fit_option, "SAME", xmin,
                                                  sorted_peak_centers[len(sorted_peak_centers) - 1])
        chi2_total = pol1TF1.GetChisquare()
        ndf_total = pol1TF1.GetNDF()
        if ndf_total > 0:
            chi2_total /= ndf_total
        xmin = max(maxTrim, sorted_peak_centers[1])
        self.ResultData['Plot']['ROOTObject'].Fit(pol1TF1, fit_option, "SAME", xmin,
                                                  sorted_peak_centers[len(sorted_peak_centers) - 1])
        chi2_right = pol1TF1.GetChisquare()
        ndf_right = pol1TF1.GetNDF()
        if ndf_right > 0:
            chi2_right /= ndf_right
        xmin = max(maxTrim, sorted_peak_centers[0])
        self.ResultData['Plot']['ROOTObject'].Fit(pol1TF1, fit_option, "SAME", xmin,
                                                  sorted_peak_centers[len(sorted_peak_centers) - 2])
        chi2_left = pol1TF1.GetChisquare()
        ndf_left = pol1TF1.GetNDF()
        if ndf_left > 0:
            chi2_left /= ndf_left
        if self.verbose:
            print 'Comparing Chi^2 for different fit ranges:'
            print '\tchi2Total ', chi2_total, ' @ NDF ', ndf_total
            print '\tchi2Left  ', chi2_left, ' @ NDF ', ndf_left
            print '\tchi2Right ', chi2_right, ' @ NDF ', ndf_right
        if ((chi2_right < chi2_total) or (chi2_left < chi2_total)) and ndf_total > 1 and self.HistoDict.get('XrayCalibration','FitOption') != 'all':
            if chi2_right < chi2_left:
                xmin = max(maxTrim, sorted_peak_centers[1])
                self.ResultData['Plot']['ROOTObject'].Fit(pol1TF1, fit_option, "SAME", xmin,
                                                          sorted_peak_centers[len(sorted_peak_centers) - 1])
                if self.verbose:
                    print "Excluding Leftmost Point because chi2Total=", chi2_total, " and chi2Right=", chi2_right
            else:
                xmin = max(maxTrim, sorted_peak_centers[0])
                self.ResultData['Plot']['ROOTObject'].Fit(pol1TF1, fit_option, "SAME", xmin,
                                                          sorted_peak_centers[len(sorted_peak_centers) - 2])
                if self.verbose:
                    print "Excluding Rightmost Point because chi2Total=", chi2_total, " and chi2Left=", chi2_left
        else:
            xmin = max(maxTrim, sorted_peak_centers[0])
            self.ResultData['Plot']['ROOTObject'].Fit(pol1TF1, fit_option, "SAME", xmin,
                                                      sorted_peak_centers[len(sorted_peak_centers) - 1])

        fit = pol1TF1
        name = 'linFit_{Method}_C{ChipNo}'.format(Method=self.Attributes['Method'], ChipNo=self.Attributes['ChipNo'])
        self.ResultData['Plot']['ROOTObject'].GetListOfFunctions().Add(fit.Clone(name))
        self.ResultData['Plot']['ROOTObject'].GetFunction(name).SetRange(0, 255)
        self.ResultData['Plot']['ROOTObject'].GetFunction(name).SetLineStyle(2)

        self.ResultData['KeyValueDictPairs'] = {
            'Slope': {
                'Value': round(fit.GetParameter(1), 3),
                'Label': 'Slope',
                'Unit': 'nElectrons/VCal',
                'Sigma': round(fit.GetParError(1), 3),
            },
            'Offset': {
                'Value': round(fit.GetParameter(0), 3),
                'Label': 'Offset',
                'Unit': 'nElectrons',
                'Sigma': round(fit.GetParError(0), 3),
            },
            'chi2': {
                'Value': round(fit.GetChisquare() / fit.GetNDF(), 3),
                'Label': 'Chi2',
                'Unit': 'per NDF',
                'Sigma': 0,
            },

        }
        self.ResultData['KeyList'] = ['Slope', 'Offset']
        self.ResultData['Plot']['ROOTObject'].Draw("APL")
        self.SaveCanvas()
        