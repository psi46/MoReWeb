# -*- coding: utf-8 -*-
import ROOT
import os.path

import AbstractClasses
from AbstractClasses.GeneralTestResult import GeneralTestResult
from ROOT import TFile, TF1, TH1F
import ConfigParser
import AbstractClasses.Helper.HistoGetter as HistoGetter
import math


class TestResult(GeneralTestResult):
    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_XRayCalibration'
        self.Name += '_{Method}_FluorescenceTargetROC_{Target}_C{ChipNo}_TestResult'.format(
            Method=self.Attributes['Method'],
            ChipNo=self.Attributes[
                'ChipNo'],
            Target=self.Attributes[
                "Target"])
        self.NameSingle = 'FluorescenceTarget'
        self.Attributes['TestedObjectType'] = 'CMSPixel_ModuleTestGroup_Module_ROC'
        if self.verbose:
            tag = self.Name + ": Custom Init"
            print "".ljust(len(tag), '=')
            print tag
        self.Attributes['fitOption'] = ''
        self.check_Test_Software()
        self.ReadModuleVersion()
        if not self.verbose:
            self.Attributes['fitOption'] += 'Q'
        if self.Attributes['ChipNo'] == 1 and 'Mo' in self.Attributes['Target']:
            # self.verbose = True
            # 'TargetEnergy': TargetEnergy,
            pass
        TargetEnergy = self.GetEnergy(self.Attributes['Target'])
        self.Attributes['TargetEnergy'] = TargetEnergy
        self.Attributes['TargetNElectrons'] = TargetEnergy / 3.6

    def GetEnergy(self, elementName):
        keys = self.HistoDict.options('XrayTargetEnergies')
        energy = 0
        for target in keys:
            if target in elementName:
                energy = self.HistoDict.getfloat('XrayTargetEnergies', target)
                return energy
        return energy

    def SetStoragePath(self):
        pass

    def OpenFileHandle(self):
        self.get_trim_configuration()
        if self.verbose: print self.RawTestSessionDataPath
        fileHandleName = self.RawTestSessionDataPath + '/commander_XraySpectrum.root'
        fileHandleName = os.path.abspath(fileHandleName)
        if self.verbose:
            print "Open File Handle: %s" % fileHandleName
        if os.path.isfile(fileHandleName):
            self.FileHandle = ROOT.TFile.Open(fileHandleName)
        else:
            fileHandleName = self.RawTestSessionDataPath + '/commander_XrayPxar.root'
            fileHandleName = os.path.abspath(fileHandleName)
            if os.path.exists(fileHandleName):
                if self.verbose:
                    print "Open File Handle: %s" % fileHandleName
                self.FileHandle = ROOT.TFile.Open(fileHandleName)
            elif self.verbose:
                print 'path does not exists ', fileHandleName
        if self.verbose:
            print "File Handle: %s" % self.FileHandle
        if not self.FileHandle:
            if self.verbose:
                print 'problem to find %s' % fileHandleName
            files = [f for f in os.listdir(self.RawTestSessionDataPath) if f.endswith('.root')]
            i = 0
            if len(files) > 1:
                print '\nPossible Candidates for ROOT files are:'
                for f in files:
                    print '\t[%3d]\t%s' % (i, f)
                    i += 1
                i = len(files)
                if self.HistoDict.has_option('RootFile', 'filename'):
                    print 'checking for backup rootfile name'
                    if self.HistoDict.get('RootFile', 'filename') in files:
                        i = files.index(self.HistoDict.get('RootFile', 'filename'))
                        print 'rootfile exists: index ', i
                while i < 0 or i >= len(files):
                    rawInput = ''
                    try:
                        # TODO: How to continue when it happens in automatic processing...

                        if self.verbose:
                            rawInput = raw_input(
                                'There are more than one possbile candidate for the ROOT file. Which file should be used? [0-%d]\t' % (
                                    len(files) - 1))
                            i = int(rawInput)
                        elif self.HistoDict.has_option('RootFile', 'filename'):
                            if self.HistoDict.get('RootFile', 'filename') in files:
                                i = files.index(self.HistoDict.get('RootFile', 'filename'))
                        else:
                            i = 0

                    except (ValueError,TypeError) as e:
                        print e
                        print '%s is not an integer, please enter a valid integer' % rawInput
                fileHandlePath = self.RawTestSessionDataPath + '/' + files[i]
                print "open '%s'" % fileHandlePath
                self.FileHandle = ROOT.TFile.Open(fileHandlePath)
            elif len(files) == 1:
                i = 0
                fileHandlePath = self.RawTestSessionDataPath + '/' + files[i]
                if self.verbose:
                    print "only one other ROOT file exists. Open '%s'" % fileHandlePath
                self.FileHandle = ROOT.TFile.Open(fileHandlePath)
            else:
                print 'There exist no ROOT file in "%s"' % self.RawTestSessionDataPath

    def get_trim_configuration(self):
        self.Attributes['TrimValue'] = 40

    # Hard coded initial guess for signal position based on element name
    def GetInitialEnergyGuess(self, elementName):
        if self.HistoDict.has_option(self.version, 'InitalXrayEnergyVcalFit'):
            fit_string = self.HistoDict.get(self.version, 'InitalXrayEnergyVcalFit')
        else:
            fit_string = self.HistoDict.get('psi46digv2.1', 'InitalXrayEnergyVcalFit')

        energy = self.Attributes['TargetEnergy']
        energy_conversion = ROOT.TFormula("fEnergyConversion", fit_string)
        vcal_guess = energy_conversion.Eval(energy)
        self.Attributes['InitialEnergyGuess'] = vcal_guess
        return vcal_guess

    # '''
    # * Function to fit a histogram with a gaussian signal riding on top of
    # * a gaussian noise with constant and linear terms. Includes assumption
    # * of a turn on due to trimming via an error function
    # *
    # * f(x) = ([0]+[1]*x+gaus(2)+gaus(5))*(1+TMath::Erf((x-[8])/[9]))/2
    # *
    # * Parameter        Description
    # *    [0]           Constant background
    # *    [1]           Linear background
    # *    [2]           Height of the SIGNAL guassian
    # *    [3]           Center of the SIGNAL gaussian
    # *    [4]           Sigma of the SIGNAL gaussian
    # *    [5]           Height of the NOISE guassian
    # *    [6]           Center of the NOISE guassian
    # *    [7]           Sigma of the NOISE gaussian
    # *    [8]           Turn on point
    # *    [9]           Turn on speed (sigma of the integrated gaussian)
    # '''
    def FitHistoSpectrum(self, histo, xmin, xmax):
        name = "fit_{0}".format(histo.GetName())

        maxbinabove = 0
        gausfit = self.FitGaus(histo, maxbinabove)
        gaus0 = gausfit.GetParameter(0)
        gaus1 = gausfit.GetParameter(1)
        gaus2 = gausfit.GetParameter(2)

        if self.HistoDict.getboolean('XrayCalibration','SpectrumFitImproveInitialGuess'):
            gaus2fit = self.Fit2Gaus(histo)

            # if peaks clearly separated, chose the higher one for initial parameter guess
            if (abs(gaus2fit.GetParameter(1)-gaus2fit.GetParameter(4)) > 40):
                if (gaus2fit.GetParameter(1) > gaus2fit.GetParameter(4)):
                    gaus0 = gaus2fit.GetParameter(0)
                    gaus1 = gaus2fit.GetParameter(1)
                    gaus2 = gaus2fit.GetParameter(2)
                else:
                    gaus0 = gaus2fit.GetParameter(3)
                    gaus1 = gaus2fit.GetParameter(4)
                    gaus2 = gaus2fit.GetParameter(5)


        if self.verbose:
            print 'Found Start parameter: ', gaus0, gaus1, gaus2

        myfit = TF1(name, "([0]+[1]*x+gaus(2)+gaus(5))*(1+TMath::Erf((x-[8])/[9]))/2", xmin, xmax)

        # Find the overall average in the y-direction to define some good starting parameters
        y_avg = histo.Integral() / histo.GetNbinsX()

        maxbin = gaus1
        maximum = gaus0
        signalSigma = gaus2

        # Find the overall mean
        mean = histo.GetMean()

        #Hard coded limit on the slope of the linear part
        param1limit = 0.5

        #Hard coded guess at the noise spread
        noiseSigma = 30

        #Hard coded trimvalue for the Erf turn on
        trimvalue = self.Attributes['TrimValue']

        #Initial guess of constant part is half of the overall y-average
        myfit.SetParameter(0, y_avg / 2)
        if self.verbose:
            print 'SetParameter0: ', myfit.GetParameter(0)

        # Limit on the constant part; it should be positive, and below the y-average
        # because the y-average is biased above the noise by the signal peak
        myfit.SetParLimits(0, 0, 2 * y_avg)
        if self.verbose:
            print 'SetParameterLimits0: ', 0, 2 * y_avg

        #Initial guess of the linear part is flat
        myfit.SetParameter(1, 0)
        if self.verbose:
            print 'SetParameter1: ', myfit.GetParameter(1)

        #Limits on the linear part, from the hardcoded value above
        myfit.SetParLimits(1, -4 * param1limit, 4 * param1limit)
        if self.verbose:
            print 'SetParameterLimits1: ', -4 * param1limit, 4 * param1limit

        #Initial guess for the size of the signal is the maximum of the histogram
        myfit.SetParameter(2, maximum)
        if self.verbose:
            print 'SetParameter2: ', myfit.GetParameter(2)
        myfit.SetParLimits(2, 0.5 * maximum, 2 * maximum)
        if self.verbose:
            print 'SetParameterLimits2: ', 0.5 * maximum, 2 * maximum

        #Initial guess for the center of the signal to be where the maximum bin is located
        myfit.SetParameter(3, maxbin)
        if self.verbose:
            print 'SetParameter3: ', myfit.GetParameter(3)

        low = maxbin - 2 * signalSigma

        #if low < trimvalue:
        #    low = trimvalue/2
        myfit.SetParLimits(3, low, maxbin + 2 * signalSigma)
        if self.verbose:
            print 'SetParameterLimits3: ', maxbin + 2 * signalSigma

        #Initial guess for the sigma of the signal, from the hardcoded value above
        myfit.SetParameter(4, signalSigma)
        if self.verbose:
            print 'SetParameter4: ', myfit.GetParameter(4)

        myfit.SetParLimits(4, signalSigma - 10, signalSigma + 10)
        if self.verbose:
            print 'SetParameterLimits4: ', signalSigma - 10, signalSigma + 10

        #Initial guess for the size of the guassian noise to be half of the overall y-average (other half is the constant term)
        myfit.SetParameter(5, y_avg * 10)

        if self.verbose:
            print 'SetParameter5: ', myfit.GetParameter(5)
        # Limits on the amount of gaussian noise, should be below y-average
        # but above 0 for the same reasons as listed for Par0
        myfit.SetParLimits(5, 0, y_avg * 20)
        if self.verbose:
            print 'SetParameterLimits4: ', 0, y_avg * 20

        #Initial guess for gaussian noise at the mean of the histogram
        myfit.SetParameter(6, mean)
        #Limits on the location of the noise to be somewhere in the fit region
        myfit.SetParLimits(6, xmin, xmax)

        #Initial guess for the noise sigma, hardcoded above
        myfit.SetParameter(7, noiseSigma)
        #Limits on noise sigma, used to make sure the noise guassian doesn't accidentally try to fit the signal
        myfit.SetParLimits(7, noiseSigma, 10 * noiseSigma)

        #Initial guess for the turn on is at the hardcorded trimvalue
        myfit.SetParameter(8, trimvalue)
        #Limits on where the turn on occurs are guessed at +-10 away from the given trim value
        #goes to very low values, but doesn't seem to affect the fit too much. Maybe a lower bound can be set to e-5
        myfit.SetParLimits(8, 0, trimvalue + 30)

        #Initial guess for the turn on speed is set to 5
        myfit.SetParameter(9, 5)
        #Limit on turn on speed between 0.1 and 10. This value should be positive and shouldn't be much more below 0.1 otherwise it will affect the rest of the fit
        myfit.SetParLimits(9, 0.01, 20)

        histo.Fit(myfit, self.Attributes['fitOption'])
        backgroundFit = TF1(name, "([0]+[1]*x+gaus(2))*(1+TMath::Erf((x-[5])/[6]))/2", xmin, xmax)
        backgroundFit.FixParameter(0, myfit.GetParameter(0))
        backgroundFit.FixParameter(1, myfit.GetParameter(1))
        backgroundFit.FixParameter(2, myfit.GetParameter(5))
        backgroundFit.FixParameter(3, myfit.GetParameter(6))
        backgroundFit.FixParameter(4, myfit.GetParameter(7))
        backgroundFit.FixParameter(5, myfit.GetParameter(8))
        backgroundFit.FixParameter(6, myfit.GetParameter(9))
        backgroundFit.SetLineColor(ROOT.kRed)
        backgroundFit.SetLineStyle(2)
        histo.Fit(backgroundFit, "+Q")

        if self.verbose:
            for i in range(10):
                a = ROOT.Double(0)
                b = ROOT.Double(0)
                myfit.GetParLimits(i, a, b)
                print i, '%8.2f [%6.2f,%6.2f]' % (myfit.GetParameter(i), a, b)

        if 'TargetEnergy' in self.Attributes:
            targetEnergy = self.Attributes['TargetEnergy']
        else:
            targetEnergy = 0
        if self.Attributes.has_key('TargetNElectrons'):
            targetNElectrons = self.Attributes['TargetNElectrons']
        else:
            targetNElectrons = 0
        if 'Target' in self.Attributes:
            target = self.Attributes['Target']
        else:
            target = 'unknown'
        chi2_per_ndf = myfit.GetChisquare() / max(myfit.GetNDF(), 1)

        NMinEntries = 99
        histoEntries = histo.GetEntries()
        try:
            binX1 = histo.GetXaxis().FindBin(10)
            binX2 = histo.GetXaxis().FindBin(250)
            histoIntegral = histo.Integral(binX1, binX2)
        except:
            histoIntegral = -1

        if histoEntries > NMinEntries and histoIntegral > NMinEntries:
            PeakCenter = round(myfit.GetParameter(3), 2)
            PeakSigma = round(myfit.GetParError(3), 2)
        else:
            print "\x1b[31mwarning: histogram with x-ray spectrum has less than 100 entries, no Vcal calibration possible. Dead ROC?\x1b[0m"
            print " -> #entries:", histoEntries
            print " -> integral(10-250):", histoIntegral
            PeakCenter = -1
            PeakSigma = -1

        self.ResultData['KeyValueDictPairs'].update(
            {
                'Center': {
                    'Value': PeakCenter,
                    'Label': 'Center of Peak',
                    'Unit': 'Vcal',
                    'Sigma': PeakSigma,
                },
                'TargetEnergy': {
                    'Value': round(targetEnergy, 2),
                    'Label': 'Energy of target %s' % target,
                    'Unit': 'eV',
                },
                'TargetNElectrons': {
                    'Value': round(targetNElectrons, 2),
                    'Label': 'Energy of target %s' % target,
                    'Unit': 'nElectrons',
                },
                'Chi2PerNDF': {
                    'Value': round(chi2_per_ndf, 2),
                    'Label': 'Chi^2 per NDF',
                    'Unit': ''
                },
                'Target': {
                    'Value': target,
                    'Label': 'Target',
                    'Unit': ''
                }
            }
        )
        self.ResultData['KeyList'].extend(['Target','Center', 'TargetEnergy', 'TargetNElectrons', 'Chi2PerNDF'])
        if self.verbose: print self.ResultData
        if self.verbose: print self.ResultData['KeyValueDictPairs']

        if self.verbose:
            print 'fitted parameters of SCurve fit:'
            for i in range(10):
                a = ROOT.Double(0)
                b = ROOT.Double(0)
                myfit.GetParLimits(i, a, b)
                print 'Par %2d:\t' % i, '%8.2f [%6.2f,%6.2f]' % (myfit.GetParameter(i), a, b)
        return myfit

    # '''
    # * Function that attempts to fit a sum of two gaussians to a spectra
    #    *
    #    * Used to check if shoulder + peak are separated or not
    #'''
    def Fit2Gaus(self, histo):
        xmin = histo.GetBinLowEdge(1)
        xmax = histo.GetBinLowEdge(histo.GetNbinsX())
        fit = TF1("gausFit", "gaus(0)+gaus(3)", xmin, xmax)
        y_avg = histo.Integral() / histo.GetNbinsX()
        #Signal peak should be have a sigma of ~10
        signalSigma = 10
        #Try to get where the peak should be
        initguess = self.GetInitialEnergyGuess(self.Attributes["Target"])
        left = 0
        right = 0
        if initguess < 0:
            #No predefined position, so guess in the middle and put limits and lower and upper bounds and the guess at the mean value
            initguess = histo.GetMean()
            left = xmin
            right = xmax
        else:
            left = initguess - 40
            right = initguess + 40

        fit.SetParameter(0, 0.5 * y_avg)
        fit.SetParLimits(0, 0, histo.Integral())

        fit.SetParameter(1, initguess)
        fit.SetParLimits(1, left, right)
        fit.SetParameter(2, signalSigma)
        #Make sure we actually fit a 'signal like' peak, nothing too broad or narrow
        fit.SetParLimits(2, signalSigma - 5, signalSigma + 5)

        fit.SetParameter(3, 0.5 * y_avg)
        fit.SetParLimits(3, 0, histo.Integral())

        fit.SetParameter(4, 50)
        fit.SetParLimits(4, 10, 75)
        fit.SetParameter(5, 20)
        #broad shoulder
        fit.SetParLimits(5, 0, 40)

        histo.Fit(fit, self.Attributes['fitOption'])
        return fit

    # '''
    # * Function that attempts to fit a simple gaussian to a spectra
    #    *
    #    * Used to find initial guess for signal in other fits
    #'''
    def FitGaus(self, histo, maxbinabove = 0):
        xmin = histo.GetBinLowEdge(1)
        xmax = histo.GetBinLowEdge(histo.GetNbinsX())
        fit = TF1("gausFit", "gaus(0)", xmin, xmax)
        y_avg = histo.Integral() / histo.GetNbinsX()
        #Signal peak should be have a sigma of ~10
        signalSigma = 10
        #Try to get where the peak should be
        initguess = self.GetInitialEnergyGuess(self.Attributes["Target"])
        left = 0
        right = 0
        if initguess < 0:
            #No predefined position, so guess in the middle and put limits and lower and upper bounds and the guess at the mean value
            initguess = histo.GetMean()
            left = xmin
            right = xmax
        else:
            left = initguess - 40
            right = initguess + 40

        fit.SetParameter(0, 0.5 * y_avg)
        fit.SetParLimits(0, 0, histo.Integral())

        fit.SetParameter(1, initguess)
        if self.HistoDict.getboolean('XrayCalibration','SpectrumFitAdditionalConstraints'):
            fit.SetParLimits(1, max(left, maxbinabove), right)
        else:
            fit.SetParLimits(1, left, right)

        fit.SetParameter(2, signalSigma)
        #Make sure we actually fit a 'signal like' peak, nothing too broad or narrow
        fit.SetParLimits(2, signalSigma - 5, signalSigma + 5)

        if (maxbinabove > 0 and self.HistoDict.getboolean('XrayCalibration','SpectrumFitAdditionalConstraints')):
            histo.GetXaxis().SetRange(int(max(left, maxbinabove)), int(right))

        histo.Fit(fit, self.Attributes['fitOption'])
        if self.HistoDict.getboolean('XrayCalibration','SpectrumFitAdditionalConstraints'):
            histo.GetXaxis().SetRange()

        return fit

    #'''
    #    * Function to fit a histogram with a gaussian signal with constant and linear terms.
    #    *  Uses FitGaus to find initial params for the gaussian and then restricts the
    #    *  fit to the region of the signal (instead of trying to fit the entire background,
    #                                        *  simply assume it is linear in the region of the signal)
    #    *
    #    * f(x) = [0]+[1]*x+gaus(2)
    #    *
    #    * Parameter        Description
    #    *    [0]           Constant background
    #    *    [1]           Linear background
    #    *    [2]           Height of the SIGNAL guassian
    #    *    [3]           Center of the SIGNAL gaussian
    #    *    [4]           Sigma of the SIGNAL gaussian
    #'''
    def FitHistoSimple(self, histo, xmin, xmax):
        name = "fit_singleGaus_{0}".format(histo.GetName())

        gausfit = self.FitGaus(histo)
        gaus0 = gausfit.GetParameter(0)
        gaus1 = gausfit.GetParameter(1)
        gaus2 = gausfit.GetParameter(2)

        myfit = TF1(name, "[0]+[1]*x+gaus(2)", gaus1 - 5 * gaus2, gaus1 + 5 * gaus2)

        #Hard coded limit on the slope of the linear part
        param1limit = 0.25

        #Hard coded guess at the signal spread
        signalSigma = 10

        myfit.SetParameter(0, 0)

        myfit.SetParameter(1, 0)
        myfit.SetParLimits(1, -1 * param1limit, param1limit)

        myfit.SetParameter(2, gaus0)
        myfit.SetParLimits(2, 0, histo.Integral())

        myfit.SetParameter(3, gaus1)

        myfit.SetParLimits(3, xmin, xmax)

        #Initial guess for the sigma of the signal from the fit
        myfit.SetParameter(4, gaus2)
        #Make sure signal peak is reasonably narrow
        myfit.SetParLimits(4, signalSigma - 5, signalSigma + 5)

        histo.Fit(myfit, "R" + self.Attributes['fitOption'])
        return myfit

    def FitHistoSCurve(self, histo, minX, maxX):
        if self.Attributes.has_key('TargetEnergy'):
            targetEnergy = self.Attributes['TargetEnergy']
        else:
            targetEnergy = 0
        if self.Attributes.has_key('TargetNElectrons'):
            targetNElectrons = self.Attributes['TargetNElectrons']
        else:
            targetNElectrons = 0
        if self.Attributes.has_key('Target'):
            target = self.Attributes['Target']
        else:
            target = 'unknown'
        self.ResultData['KeyValueDictPairs'].update(
            {
                'Center': {
                    'Value': round(histo.GetXaxis().GetBinCenter(histo.GetMaximumBin()), 2),
                    'Label': 'Center of Peak',
                    'Unit': 'Vcal',
                    'Sigma': round(histo.GetRMS(), 2),
                },
                'TargetEnergy': {
                    'Value': round(targetEnergy, 2),
                    'Label': 'Energy of target %s' % target,
                    'Unit': 'eV',
                },
                'TargetNElectrons': {
                    'Value': round(targetNElectrons, 2),
                    'Label': 'Energy of target %s' % target,
                    'Unit': 'nElectrons',
                },
                'Chi2PerNDF': {
                    'Value': round(0, 2),
                    'Label': 'Energy of target %s' % target,
                    'Unit': 'nElectrons',
                },

            }
        )
        self.ResultData['KeyList'].extend(['Center', 'TargetEnergy', 'TargetNElectrons'])
        if self.verbose: print self.ResultData
        if self.verbose: print self.ResultData['KeyValueDictPairs']
        pass

    def PopulateResultData(self):
        ROOT.gPad.SetLogy(0)
        ROOT.gPad.SetLogx(0)
        if self.verbose:
            tag = 'PopulateResultData', self.NameSingle, self.Attributes['Target'] + ": Custom Init"
            print "".ljust(len(tag), '=')
            print tag
        # self.check_Test_Software()
        HistoDict = self.HistoDict

        # print self.Name,'softwareVersion:',self.testSoftware
        try:
            histname = HistoDict.get(self.NameSingle, self.Attributes['Method'])
        except ConfigParser.NoOptionError as e:
            print HistoDict.sections()
            if HistoDict.has_section(self.NameSingle):
                for i in HistoDict.options(self.NameSingle):
                    print i, HistoDict.get(self.NameSingle, i)
            raise e
        my_object = HistoGetter.get_histo(self.FileHandle, histname, rocNo=self.Attributes["ChipNo"])
        if not my_object:
            if self.verbose:
                print "couldn't find histname %s" % histname
            histname = HistoDict.get(self.NameSingle, self.Attributes['Method'])
            #'PH_Calibration_ROC')
            if self.verbose:
                print ' try to find histname %s' % histname
            my_object = HistoGetter.get_histo(self.FileHandle, histname, rocNo=self.Attributes["ChipNo"])
        if not my_object:
            raise KeyError("couldn't find histname %s" % histname)
        self.ResultData['Plot']['ROOTObject'] = my_object.Clone(self.GetUniqueID())
        #Get Xray Hit Map
        try:
            if self.verbose: print '\nget Xray Hit Map'
            histname = HistoDict.get(self.NameSingle, 'XrayHitMap')
            if self.verbose: print histname
            my_object = HistoGetter.get_histo(self.FileHandle, histname, rocNo=self.Attributes["ChipNo"])
            if self.verbose: print my_object.GetName()
            if not my_object:
                raise KeyError("couldn't find histname %s" % histname)
            self.ResultData['Plot']['ROOTObjectHitMap'] = my_object.Clone(self.GetUniqueID())
            nhits = int(self.ResultData['Plot']['ROOTObjectHitMap'].GetEntries())
            if self.verbose: print self.ResultData['Plot']['ROOTObjectHitMap']
        except Exception as e:
            nhits = 0
        try:
            # if self.verbose:
            # print '\nget Xray number of triggers'
            histname = HistoDict.get(self.NameSingle, 'XrayNtrig')
            # if self.verbose:
            my_object = HistoGetter.get_histo(self.FileHandle, histname)
            if self.verbose: print my_object.GetName()
            if not my_object:
                raise KeyError("couldn't find histname %s" % histname)
            ntrig = int(my_object.Integral())
        except Exception as e:
            ntrig = 0
        if self.ResultData['Plot']['ROOTObject']:
            histo = self.ResultData['Plot']['ROOTObject']
            if self.verbose:
                print 'found Plot ', histo
            minX = 0
            maxX = 255
            if self.Attributes['Method'] == 'Spectrum':
                #todo define rebin condition in extrernal file
                while True:
                    maximum = histo.GetBinContent(histo.GetMaximumBin())
                    entries = histo.GetEntries()
                    ratio = float(maximum) / float(entries) if entries > 0 else 1
                    if ratio < .025:
                        BinsBefore = histo.GetXaxis().GetNbins()
                        histo.Rebin()
                        BinsAfter = histo.GetXaxis().GetNbins()
                        if BinsAfter < 20:
                            print "\x1b[31mStop rebinning of histogram at #bins = %d. This might be a due to a broken ROC or missing PH calibration data.\x1b[0m"%BinsAfter
                            break
                        elif BinsBefore == BinsAfter:
                            print "\x1b[31mRebinning of histogram failed\x1b[0m"
                            break
                    else:
                        break

                self.FitHistoSpectrum(histo, minX, maxX)
            else:
                self.FitHistoSCurve(histo, minX, maxX)
                pass
            self.ResultData['KeyValueDictPairs']['NHits'] = {'Value':'{0:d}'.format(nhits), 'Label':'N Hits','Unit':'Hits'}
            # self.ResultData['KeyList'].append('NHits')
            self.ResultData['KeyValueDictPairs']['NTrig'] = {'Value':'{0:d}'.format(ntrig), 'Label':'N Trig','Unit':'Trigger'}
            # self.ResultData['KeyList'].append('NTrig')
            area = HistoDict.getfloat('XrayCalibration','AreaPerROC')
            if area ==0 or ntrig == 0:
                rate = -1
            else:
                rate = nhits/(ntrig*25e-9*area)

            if rate>0:
                order = min(int(math.log10(rate))/3,3)
            else:
                order = 0

            rate_divider =  10**(3*order)
            rate2 = round(rate/rate_divider,1)
            if order == 0:
                unit = 'Hz'
            elif order == 1:
                unit = 'kHz'
            elif order == 2:
                unit = 'MHz'
            elif order == 3:
                unit = 'GHz'
            unit+='/cm²'
            self.ResultData['KeyValueDictPairs']['Rate'] = {'Value':'{0:1.2f}'.format(rate2), 'Label':'Rate','Unit': unit}
            self.ResultData['KeyList'].append('Rate')
            #            self.ResultData['Plot']['ROOTObject'].SetTitle("");
            #            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetRangeUser(-50., 50.);
            #            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetRangeUser(0.5, 5.0*self.ResultData['Plot']['ROOTObject'].GetMaximum());
            #            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Threshold difference");
            #            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("No. of Entries");
            first_bin = self.ResultData['Plot']['ROOTObject'].FindLastBinAbove(0)
            first_bin *= 1.2
            first_bin = int(first_bin)
            first_bin = min([first_bin, self.ResultData['Plot']['ROOTObject'].GetNbinsX()])
            xmax = self.ResultData['Plot']['ROOTObject'].GetXaxis().GetBinUpEdge(first_bin)
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetRangeUser(0, xmax)
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle('Pulseheight / Vcal')
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle('number of entries #')
            self.ResultData['Plot']['ROOTObject'].Draw()

        self.SaveCanvas()
        if self.Attributes.has_key('Target'):
            self.Title = '%s Spectrum ROC %i' % (self.Attributes['Target'], self.Attributes['ChipNo'])
        else:
            self.Title = 'Spectrum ROC %i' % (self.Attributes['ChipNo'])
        if self.verbose:
            print 'done'
        # print self.ResultData['KeyValueDictPairs']
        # print self.ResultData['KeyList']
        # raw_input()

# '''
# #hg
# self.ResultData['Plot']['ROOTObject_hGain'] = ROOT.TH1D(self.GetUniqueID(), "", 300, -2.0, 5.5)  # hGain
#
# #hgm
# self.ResultData['Plot']['ROOTObject_hGainMap'] = ROOT.TH2D(self.GetUniqueID(), "", 52, 0, 52, 80, 0, 80) # hGainMap
#
# #hp
# self.ResultData['Plot']['ROOTObject_hPedestal'] = ROOT.TH1D(self.GetUniqueID(), "", 900, -300., 600.) # hPedestal
# self.ResultData['Plot']['ROOTObject_hPedestal'].StatOverflows(True)
#
# #rp
# self.ResultData['Plot']['ROOTObject_rPedestal'] = ROOT.TH1D(self.GetUniqueID(), "", 900, -300., 600.) # rPedestal
# self.ResultData['Plot']['ROOTObject_rPedestal'].StatOverflows(False)
#
# Parameters = [] # Parameters of Vcal vs. Pulse Height Fit
#
#
# Directory = self.RawTestSessionDataPath
# # originally: phCalibrationFit_C
# PHCalibrationFitFileName = "{Directory}/phCalibrationFit_C{ChipNo}.dat".format(Directory=Directory,ChipNo=self.ParentObject.Attributes['ChipNo'])
# PHCalibrationFitFile = open(PHCalibrationFitFileName, "r")
# self.FileHandle = PHCalibrationFitFile #needed in summary
#
# #PHCalibrationFitFile.seek(2*200) # omit the first 400 bytes
#
# if PHCalibrationFitFile:
# # for (int i = 0 i < 2 i++) fgets(string, 200, phLinearFile)
# for i in range(4):
# Line = PHCalibrationFitFile.readline() # Omit first four lines
#
#			for i in range(52): #Columns
#				for j in range(80): #Rows
#					Line = PHCalibrationFitFile.readline()
#					if Line:
#
#						#Parameters[0], Parameters[1], Parameters[2], Parameters[3], Parameters[4], Parameters[5], d, a, b = line.strip().split()
#						Parameters = Line.strip().split()
#						try:
#							float(Parameters[2])
#							float(Parameters[3])
#
#							if abs(float(Parameters[2])) > 1e-10 : #dead pixels have par2 == 0.
#								Gain = 1./float(Parameters[2])
#								Pedestal = float(Parameters[3])
#
#								self.ResultData['Plot']['ROOTObject_hPedestal'].Fill(Pedestal)
#								self.ResultData['Plot']['ROOTObject_hGain'].Fill(Gain)
#								self.ResultData['Plot']['ROOTObject_hGainMap'].SetBinContent(i + 1, j + 1, Gain) # Column, Row, Gain
#
#						except (ValueError, TypeError, IndexError):
#							pass
#
#
#
#
#			# -- Gain
#
#			#mG
#			MeanGain = self.ResultData['Plot']['ROOTObject_hGain'].GetMean()
#			#sG
#			RMSGain = self.ResultData['Plot']['ROOTObject_hGain'].GetRMS()
#			#nG
#			IntegralGain = self.ResultData['Plot']['ROOTObject_hGain'].Integral(
#				self.ResultData['Plot']['ROOTObject_hGain'].GetXaxis().GetFirst(),
#				self.ResultData['Plot']['ROOTObject_hGain'].GetXaxis().GetLast()
#			)
#			#nG_entries
#			IntegralGain_Entries = self.ResultData['Plot']['ROOTObject_hGain'].GetEntries()
#
#			under = self.ResultData['Plot']['ROOTObject_hGain'].GetBinContent(0)
#			over = self.ResultData['Plot']['ROOTObject_hGain'].GetBinContent(self.ResultData['Plot']['ROOTObject_hGain'].GetNbinsX()+1)
#
#			ROOT.gPad.SetLogy(1)
#
#			self.ResultData['Plot']['ROOTObject_hGain'].GetYaxis().SetRangeUser(0.5, 5.0*self.ResultData['Plot']['ROOTObject_hGain'].GetMaximum())
#			self.ResultData['Plot']['ROOTObject_hGain'].SetLineColor(ROOT.kBlack)
#			self.ResultData['Plot']['ROOTObject_hGain'].GetXaxis().SetTitle("Gain [ADC/DAC]");
#			self.ResultData['Plot']['ROOTObject_hGain'].GetYaxis().SetTitle("No. of Entries");
#			self.ResultData['Plot']['ROOTObject_hGain'].GetXaxis().CenterTitle();
#			self.ResultData['Plot']['ROOTObject_hGain'].GetYaxis().SetTitleOffset(1.2);
#			self.ResultData['Plot']['ROOTObject_hGain'].GetYaxis().CenterTitle();
#			self.ResultData['Plot']['ROOTObject_hGain'].Draw()
#			self.ResultData['Plot']['ROOTObject'] = self.ResultData['Plot']['ROOTObject_hGain']
#
#
#
#
#			self.ResultData['KeyValueDictPairs'] = {
#				'N': {
#					'Value':'{0:1.0f}'.format(IntegralGain),
#					'Label':'N'
#				},
#				'mu': {
#					'Value':'{0:1.2f}'.format(MeanGain),
#					'Label':''
#				},
#				'sigma':{
#					'Value':'{0:1.2f}'.format(RMSGain),
#					'Label':'σ'
#				}
#			}
#			self.ResultData['KeyList'] = ['N','mu','sigma']
#			if under:
#				self.ResultData['KeyValueDictPairs']['under'] = {'Value':'{0:1.2f}'.format(under), 'Label':'<='}
#				self.ResultData['KeyList'].append('under')
#			if over:
#				self.ResultData['KeyValueDictPairs']['over'] = {'Value':'{0:1.2f}'.format(over), 'Label':'>='}
#				self.ResultData['KeyList'].append('over')
#
#			if self.ParentObject.Attributes['ModuleVersion'] == 1:
#				self.ParentObject.ResultData['SubTestResults']['PHCalibrationTan'].ResultData['Plot']['ROOTObject'].SetLineColor(ROOT.kBlue)
#				self.ParentObject.ResultData['SubTestResults']['PHCalibrationTan'].ResultData['Plot']['ROOTObject'].Draw('same')
#				self.ResultData['KeyValueDictPairs'].update({
#					'Par1N': {
#						'Value':self.ParentObject.ResultData['SubTestResults']['PHCalibrationTan'].ResultData['KeyValueDictPairs']['N']['Value'],
#						'Label':'Par1 N'
#					},
#					'Par1mu': {
#						'Value':self.ParentObject.ResultData['SubTestResults']['PHCalibrationTan'].ResultData['KeyValueDictPairs']['mu']['Value'],
#						'Label':'Par1 μ'
#					},
#					'Par1sigma':{
#						'Value':self.ParentObject.ResultData['SubTestResults']['PHCalibrationTan'].ResultData['KeyValueDictPairs']['sigma']['Value'],
#						'Label':'Par1 σ'
#					}
#				})
#				self.ResultData['KeyList'] += ['Par1N','Par1mu','Par1sigma']
#
#
#			if self.SavePlotFile:
#				self.Canvas.SaveAs(self.GetPlotFileName())
#			self.ResultData['Plot']['Enabled'] = 1
#			self.ResultData['Plot']['Caption'] = 'PH Calibration: Gain (ADC/DAC)'
#			self.ResultData['Plot']['ImageFile'] = self.GetPlotFileName()
#    '''


