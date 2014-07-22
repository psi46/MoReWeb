import AbstractClasses
import ROOT
import array


class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = "CMSPixel_QualificationGroup_XrayCalibrationSpectrum_VcalCalibrationModule_VcalCalibrationROC_TestResult"
        self.NameSingle = "VcalCalibrationROC"
        self.Title = "Vcal Calibration ROC %i" % (self.Attributes['ChipNo'])
        self.ChipNo = self.Attributes['ChipNo']
        self.Method = self.Attributes['Method']
        self.verbose = False
        if self.verbose:
            tag = self.Name + ": Custom Init"
            print "".ljust(len(tag), '=')
            print tag
        self.Attributes['TestedObjectType'] = 'VcalCalibrationROC'

    def PopulateResultData(self):
        if self.verbose:
            tag = self.Name + ": Populate"
            print "".ljust(len(tag), '=')
            print tag

    def PopulateResultData(self):
        if self.verbose:
            tag = self.Name + ' - ROC ' + '%d' % self.Attributes['ChipNo'] + ": Populate"
            print "".ljust(len(tag), '=')
            print tag

        fitOption = "Q"
        if not self.verbose:
            fitOption += 'Q'
        PeakCenters = array.array('d', [])
        PeakErrors = array.array('d', [])
        NumElectrons = array.array('d', [])
        top_parent = self.ParentObject.ParentObject
        for test in top_parent.ResultData['SubTestResults']:
            if not "FluorescenceSpectrumModule" in test:
                continue
            module_results = top_parent.ResultData['SubTestResults'][test].ResultData['SubTestResults']
            roc_results = module_results['FluorescenceSpectrum_C%i' % (self.Attributes["ChipNo"])]
            keyValuePairs = roc_results.ResultData['KeyValueDictPairs']
            if self.verbose:
                print test, keyValuePairs['Center']['Value'], keyValuePairs['TargetNElectrons']['Value']
            PeakCenters.append(keyValuePairs['Center']['Value'])
            PeakErrors.append(keyValuePairs['Center']['Sigma'])
            NumElectrons.append(keyValuePairs['TargetNElectrons']['Value'])
        pointPairs = zip(PeakCenters, NumElectrons, PeakErrors)
        sortedPoints = sorted(pointPairs, key=lambda point: point[1])
        print sortedPoints
        prevPoint = sortedPoints[0][0]
        num = 0
        for e in sortedPoints:
            if e[0] < prevPoint:
                if self.verbose:
                    print "Error: Lower VCal for higher energy...possible fit error. Point in question: ", e
                sortedPoints.pop(num)
            num = num + 1
            prevPoint = e[0]
        newSortedPoints = sorted(sortedPoints, key=lambda point: point[0])
        sortedPeakCenters = array.array('d', [])
        sortedNumElectrons = array.array('d', [])
        sortedPeakErrors = array.array('d', [])
        sortedElectronError = array.array('d', [])
        for e in newSortedPoints:
            sortedPeakCenters.append(e[0])
            sortedNumElectrons.append(e[1])
            sortedPeakErrors.append(e[2])
            sortedElectronError.append(0.0)
        self.ResultData['Plot']['ROOTObject'] = ROOT.TGraphErrors(len(sortedPeakCenters), sortedPeakCenters,
                                                                  sortedNumElectrons, sortedPeakErrors,
                                                                  sortedElectronError)
        self.ResultData['Plot']['ROOTObject'].SetTitle(
            "Center of Pulse Height (Vcal units) vs number of electrons;Center of Pulse Height[Vcal];Number of Electrons")
        self.ResultData['Plot']['ROOTObject'].SetMarkerColor(4)
        self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.6)
        # self.ResultData['Plot']['ROOTObject'].SetMarkerStyle(21)

        #Fitting of Slope
        self.ResultData['Plot']['ROOTObject'].Fit("pol1", fitOption, "SAME", sortedPeakCenters[0],
                                                  sortedPeakCenters[len(sortedPeakCenters) - 1])
        chi2Total = self.ResultData['Plot']['ROOTObject'].GetFunction("pol1").GetChisquare()
        ndf_total = self.ResultData['Plot']['ROOTObject'].GetFunction("pol1").GetNDF()
        chi2Total /= ndf_total
        self.ResultData['Plot']['ROOTObject'].Fit("pol1", fitOption, "SAME", sortedPeakCenters[1],
                                                  sortedPeakCenters[len(sortedPeakCenters) - 1])
        chi2Right = self.ResultData['Plot']['ROOTObject'].GetFunction("pol1").GetChisquare()
        ndf_right = self.ResultData['Plot']['ROOTObject'].GetFunction("pol1").GetNDF()
        if ndf_right:
            chi2Right /= ndf_right
        self.ResultData['Plot']['ROOTObject'].Fit("pol1", fitOption, "SAME", sortedPeakCenters[0],
                                                  sortedPeakCenters[len(sortedPeakCenters) - 2])
        chi2Left = self.ResultData['Plot']['ROOTObject'].GetFunction("pol1").GetChisquare()
        ndf_left = self.ResultData['Plot']['ROOTObject'].GetFunction("pol1").GetNDF()
        if ndf_left:
            chi2Left /= ndf_left
        if self.verbose:
            print 'Comparing Chi^2 for different fit ranges:'
            print '\tchi2Total ', chi2Total, ' @ NDF ', ndf_total
            print '\tchi2Left  ', chi2Left, ' @ NDF ', ndf_left
            print '\tchi2Right ', chi2Right, ' @ NDF ', ndf_right
        if (((chi2Right < chi2Total) or (chi2Left < chi2Total)) and ndf_total > 1):
            if chi2Right < chi2Left:
                self.ResultData['Plot']['ROOTObject'].Fit("pol1", fitOption, "SAME", sortedPeakCenters[1],
                                                          sortedPeakCenters[len(sortedPeakCenters) - 1])
                if self.verbose:
                    print "Excluding Leftmost Point because chi2Total=", chi2Total, " and chi2Right=", chi2Right
            else:
                self.ResultData['Plot']['ROOTObject'].Fit("pol1", fitOption, "SAME", sortedPeakCenters[0],
                                                          sortedPeakCenters[len(sortedPeakCenters) - 2])
                if self.verbose:
                    print "Excluding Rightmost Point because chi2Total=", chi2Total, " and chi2Left=", chi2Left
        else:
            self.ResultData['Plot']['ROOTObject'].Fit("pol1", fitOption, "SAME", sortedPeakCenters[0],
                                                      sortedPeakCenters[len(sortedPeakCenters) - 1])

        fit = self.ResultData['Plot']['ROOTObject'].GetFunction("pol1")
        name = 'linFit_{Method}_C{ChipNo}'.format(Method = self.Method,ChipNo = self.ChipNo)
        self.ResultData['Plot']['ROOTObject'].GetListOfFunctions().Add(fit.Clone(name))
        self.ResultData['Plot']['ROOTObject'].GetFunction(name).SetRange(0,255)
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

        }
        self.ResultData['KeyList'] = ['Slope', 'Offset']
        self.ResultData['Plot']['ROOTObject'].Draw("APL")
        if self.SavePlotFile:
            self.Canvas.SaveAs(self.GetPlotFileName())
        self.ResultData['Plot']['Enabled'] = 1
        self.ResultData['Plot']['ImageFile'] = self.GetPlotFileName()
