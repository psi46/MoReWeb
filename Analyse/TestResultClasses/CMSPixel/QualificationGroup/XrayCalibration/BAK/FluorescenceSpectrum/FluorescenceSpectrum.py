# -*- coding: utf-8 -*-
'''
    Program: X-Ray Fluorescence Target Results
    Author: Paul Turner - pturne7@uic.edu
    Version: 1.0
    Release Date: 2013-07-18
'''
import ROOT
import os.path
import AbstractClasses
from ROOT import TFile,TF1,TH1F

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_ModuleTestGroup_Module_XRayCalibration_FluorescenceTarget_TestResult'
        self.NameSingle='FluorescenceTarget'
        self.Attributes['TestedObjectType'] = 'CMSPixel_ModuleTestGroup_Module_ROC'
        self.fitOption =''
        if not self.verbose:
            self.fitOption +='Q'

    def SetSoragePath(self):
        pass

    def OpenFileHandle(self):
        if self.verbose:
            print self.RawTestSessionDataPath
        fileHandleName =  self.RawTestSessionDataPath + '/commander_XraySpectrum.root'
        if self.verbose:
            print "Open File Handle: %s"%fileHandleName
        if os.path.isfile(fileHandleName):
            self.FileHandle = ROOT.TFile.Open(fileHandleName)
        else
            fileHandleName =  self.RawTestSessionDataPath +'/commander_XrayPxar.root'
            self.FileHandle = ROOT.TFile.Open(fileHandleName)

    # Hard coded initial guess for signal position based on element name
    def GetInitialEnergyGuess(self,elementName):
        if "Fe" in elementName:
            self.InitialEnergyGuess = 56.7
            return self.InitialEnergyGuess
        if "Ni" in elementName:
            self.InitialEnergyGuess = 63.7
            return self.InitialEnergyGuess
        if "Cu" in elementName:
            self.InitialEnergyGuess = 81.8
            return self.InitialEnergyGuess
        if "Br" in elementName:
            self.InitialEnergyGuess = 112.1
            return self.InitialEnergyGuess
        if "Mo" in elementName:
            self.InitialEnergyGuess = 138.9
            return self.InitialEnergyGuess
        if "Ag" in elementName:
            self.InitialEnergyGuess = 156.6
            return self.InitialEnergyGuess
        if "Sn" in elementName:
            self.InitialEnergyGuess = 198
            return self.InitialEnergyGuess
        self.InitialEnergyGuess = -1
        return self.InitialEnergyGuess

#'''
#    * Function to fit a histogram with a gaussian signal riding on top of
#    * a gaussian noise with constant and linear terms. Includes assumption
#    * of a turn on due to trimming via an error function
#    *
#    * f(x) = ([0]+[1]*x+gaus(2)+gaus(5))*(1+TMath::Erf((x-[8])/[9]))/2
#    *
#    * Parameter        Description
#    *    [0]           Constant background
#    *    [1]           Linear background
#    *    [2]           Height of the SIGNAL guassian
#    *    [3]           Center of the SIGNAL gaussian
#    *    [4]           Sigma of the SIGNAL gaussian
#    *    [5]           Height of the NOISE guassian
#    *    [6]           Center of the NOISE guassian
#    *    [7]           Sigma of the NOISE gaussian
#    *    [8]           Turn on point
#    *    [9]           Turn on speed (sigma of the integrated gaussian)
#'''
    def FitHisto(self,histo,min,max):
        name = "fit_{0}".format( histo.GetName() )
        gausfit = self.FitGaus(histo)
        gaus0 = gausfit.GetParameter(0)
        gaus1 = gausfit.GetParameter(1)
        gaus2 = gausfit.GetParameter(2)

        myfit = TF1(name,"([0]+[1]*x+gaus(2)+gaus(5))*(1+TMath::Erf((x-[8])/[9]))/2",min,max)

        #Find the overall average in the y-direction to define some good starting parameters
        y_avg = histo.Integral() / histo.GetNbinsX()

        maxbin = gaus1
        maximum = gaus0
        signalSigma = gaus2

        #Find the overall mean
        mean = histo.GetMean()

        #Hard coded limit on the slope of the linear part
        param1limit = 0.5

        #Hard coded guess at the noise spread
        noiseSigma = 30

        #Hard coded trimvalue for the Erf turn on
        trimvalue = 40

        #Initial guess of constant part is half of the overall y-average
        myfit.SetParameter(0,y_avg/2)

        #Limit on the constant part; it should be positive, and below the y-average because the y-average is biased above the noise by the signal peak
        myfit.SetParLimits(0,0,2*y_avg)

        #Initial guess of the linear part is flat
        myfit.SetParameter(1,0)

        #Limits on the linear part, from the hardcoded value above
        myfit.SetParLimits(1,-4*param1limit,4*param1limit)

        #Initial guess for the size of the signal is the maximum of the histogram
        myfit.SetParameter(2,maximum)
        myfit.SetParLimits(2,0.5*maximum,2*maximum)

        #Initial guess for the center of the signal to be where the maximum bin is located
        myfit.SetParameter(3,maxbin)

        low = maxbin-2*signalSigma

        if(low < trimvalue):
            low = trimvalue
        myfit.SetParLimits(3,low,maxbin+2*signalSigma)

        #Initial guess for the sigma of the signal, from the hardcoded value above
        myfit.SetParameter(4,signalSigma)

        myfit.SetParLimits(4,signalSigma-10,signalSigma+10)

        #Initial guess for the size of the guassian noise to be half of the overall y-average (other half is the constant term)
        myfit.SetParameter(5,y_avg*10)
        #Limits on the amount of gaussian noise, should be below y-average but above 0 for the same reasons as listed for Par0
        myfit.SetParLimits(5,0,y_avg*20)

        #Initial guess for gaussian noise at the mean of the histogram
        myfit.SetParameter(6,mean)
        #Limits on the location of the noise to be somewhere in the fit region
        myfit.SetParLimits(6,min,max)

        #Initial guess for the noise sigma, hardcoded above
        myfit.SetParameter(7,noiseSigma)
        #Limits on noise sigma, used to make sure the noise guassian doesn't accidentally try to fit the signal
        myfit.SetParLimits(7,1,10*noiseSigma)

        #Initial guess for the turn on is at the hardcorded trimvalue
        myfit.SetParameter(8,trimvalue)
        #Limits on where the turn on occurs are guessed at +-10 away from the given trim value
        #goes to very low values, but doesn't seem to affect the fit too much. Maybe a lower bound can be set to e-5
        myfit.SetParLimits(8,0,trimvalue+30)

        #Initial guess for the turn on speed is set to 5
        myfit.SetParameter(9,5)
        #Limit on turn on speed between 0.1 and 10. This value should be positive and shouldn't be much more below 0.1 otherwise it will affect the rest of the fit
        myfit.SetParLimits(9,0.01,20)

        histo.Fit(myfit,self.fitOption)
        if self.Attributes.has_key('TargetEnergy'):
            targetEnergy= self.Attributes['TargetEnergy']
        else:
            targetEnergy = 0
        if self.Attributes.has_key('TargetNElectrons'):
            targetNElectrons= self.Attributes['TargetNElectrons']
        else:
            targetNElectrons = 0
        if self.Attributes.has_key('Target'):
            target= self.Attributes['Target']
        else:
            target = 'unknown'
        self.ResultData['KeyValueDictPairs'] = {
            'Center': {
                'Value': round(myfit.GetParameter(3),2),
                'Label':'Center of Peak',
                'Unit': 'Vcal',
                'Sigma': round(myfit.GetParError(3),2),
            },
            'TargetEnergy': {
                'Value': round(targetEnergy,2),
                'Label':'Energy of target %s'%target,
                'Unit': 'eV',
            },
            'TargetNElectrons': {
                'Value': round(targetNElectrons,2),
                'Label':'Energy of target %s'%target,
                'Unit': 'nElectrons',
            },

        }
        self.ResultData['KeyList'] = ['Center','TargetEnergy','TargetNElectrons']
        if self.verbose: print self.ResultData
        if self.verbose: print self.ResultData['KeyValueDictPairs']

        return myfit

#'''
#    * Function that attempts to fit a simple gaussian to a spectra
#    *
#    * Used to find initial guess for signal in other fits
#'''
    def FitGaus(self,histo):
        min = histo.GetBinLowEdge(1)
        max = histo.GetBinLowEdge( histo.GetNbinsX() )
        fit = TF1("gausFit","gaus(0)",min,max)
        y_avg = histo.Integral()/histo.GetNbinsX()
        #Signal peak should be have a sigma of ~10
        signalSigma = 10
        #Try to get where the peak should be
        initguess = self.GetInitialEnergyGuess(histo.GetName())
        left = 0
        right = 0
        if(initguess < 0):
            #No predefined position, so guess in the middle and put limits and lower and upper bounds and the guess at the mean value
            initguess = histo.GetMean()
            left = min
            right = max
        else:
            left = initguess-40
            right = initguess+40

        fit.SetParameter(0,0.5*y_avg)
        fit.SetParLimits(0,0,histo.Integral())

        fit.SetParameter(1,initguess)
        fit.SetParLimits(1,left,right)
        fit.SetParameter(2,signalSigma)
        #Make sure we actually fit a 'signal like' peak, nothing too broad or narrow
        fit.SetParLimits(2,signalSigma-5,signalSigma+5)

        histo.Fit(fit,self.fitOption)
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
    def FitHistoSimple(self,histo,min,max):
        name = "fit_singleGaus_{0}".format(histo.GetName())


        gausfit = self.FitGaus(histo);
        gaus0 = gausfit.GetParameter(0)
        gaus1 = gausfit.GetParameter(1)
        gaus2 = gausfit.GetParameter(2)

        myfit = TF1(name,"[0]+[1]*x+gaus(2)",gaus1-5*gaus2,gaus1+5*gaus2)

        #Hard coded limit on the slope of the linear part
        param1limit = 0.25

        #Hard coded guess at the signal spread
        signalSigma = 10

        myfit.SetParameter(0,0)

        myfit.SetParameter(1,0)
        myfit.SetParLimits(1,-1*param1limit,param1limit)

        myfit.SetParameter(2,gaus0)
        myfit.SetParLimits(2,0,histo.Integral())

        myfit.SetParameter(3,gaus1)

        myfit.SetParLimits(3,min,max)

        #Initial guess for the sigma of the signal from the fit
        myfit.SetParameter(4,gaus2)
        #Make sure signal peak is reasonably narrow
        myfit.SetParLimits(4,signalSigma-5,signalSigma+5)
        
        histo.Fit(myfit,"R"+self.fitOption)
        return myfit

    def PopulateResultData(self):
        self.ResultData['Plot']['ROOTObject'] = self.FileHandle.Get("pulseheight_cal").Clone(self.GetUniqueID())
        if self.ResultData['Plot']['ROOTObject']:
            histo = self.ResultData['Plot']['ROOTObject']
            min = 0
            max = 255
            self.FitHisto(histo, min, max)
#            self.ResultData['Plot']['ROOTObject'].SetTitle("");
#            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetRangeUser(-50., 50.);
#            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetRangeUser(0.5, 5.0*self.ResultData['Plot']['ROOTObject'].GetMaximum());
#            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Threshold difference");
#            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("No. of Entries");
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle();
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle('Pulseheight / Vcal')
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5);
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle();
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle('number of entries #')
            self.ResultData['Plot']['ROOTObject'].Draw();

        self.SaveCanvas()
        if self.Attributes.has_key('Target'):
            self.Title = 'Fluorescence Spectrum for %s'%(self.Attributes['Target'])
        else:
            self.Title = 'Fluorescence Spectrum'
        
#        '''
#		#hg
#		self.ResultData['Plot']['ROOTObject_hGain'] = ROOT.TH1D(self.GetUniqueID(), "", 300, -2.0, 5.5)  # hGain
#
#		#hgm
#		self.ResultData['Plot']['ROOTObject_hGainMap'] = ROOT.TH2D(self.GetUniqueID(), "", self.nCols, 0, self.nCols, self.nRows, 0, self.nRows) # hGainMap
#
#		#hp
#		self.ResultData['Plot']['ROOTObject_hPedestal'] = ROOT.TH1D(self.GetUniqueID(), "", 900, -300., 600.) # hPedestal
#		self.ResultData['Plot']['ROOTObject_hPedestal'].StatOverflows(True)
#
#		#rp
#		self.ResultData['Plot']['ROOTObject_rPedestal'] = ROOT.TH1D(self.GetUniqueID(), "", 900, -300., 600.) # rPedestal
#		self.ResultData['Plot']['ROOTObject_rPedestal'].StatOverflows(False)
#
#		Parameters = [] # Parameters of Vcal vs. Pulse Height Fit
#
#
#		Directory = self.RawTestSessionDataPath
#		# originally: phCalibrationFit_C
#		PHCalibrationFitFileName = "{Directory}/phCalibrationFit_C{ChipNo}.dat".format(Directory=Directory,ChipNo=self.ParentObject.Attributes['ChipNo'])
#		PHCalibrationFitFile = open(PHCalibrationFitFileName, "r")
#		self.FileHandle = PHCalibrationFitFile #needed in summary
#
#		#PHCalibrationFitFile.seek(2*200) # omit the first 400 bytes
#
#		if PHCalibrationFitFile:
#			# for (int i = 0 i < 2 i++) fgets(string, 200, phLinearFile)
#			for i in range(4):
#				Line = PHCalibrationFitFile.readline() # Omit first four lines
#
#			for i in range(self.nCols): #Columns
#				for j in range(self.nRows): #Rows
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


