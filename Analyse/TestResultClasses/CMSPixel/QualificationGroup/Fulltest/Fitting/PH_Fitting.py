import ROOT
import sys, os
import math
import time
import functools
from multiprocessing import Pool, Process, Queue, Pipe
import multiprocessing
import time
import random

class PH_Fitting():
    FitfcnTanName = "FitfcnTanName"
    FitfcnName = "FitfcnName"
    nCols = 52
    nRows = 80
    vcalSteps = 5
    rangeConversion = 7
    SaturationPH = 250
    ErrorVcal = 2.0
    ErrorPH = 8.0

    def __init__(self, fitMode, refit=True, HistoDict = None, ParallelProcessing = False, LimitProcesses = None):
        self.k = 0
        # ROOT.gStyle
        self.verbose = False
        self.fitMode = fitMode
        self.refit = refit
        self.DrawHistos = False
        self.HistoDict = HistoDict
        self.ParallelProcessing = ParallelProcessing
        if LimitProcesses and LimitProcesses < 1:
            LimitProcesses = 1
        self.LimitProcesses = LimitProcesses
        print "  parallel processing ".ljust(30), self.ParallelProcessing
        if self.ParallelProcessing and LimitProcesses:
            print "  max number of subprocesses: ".ljust(30), self.LimitProcesses

        self.InitFit()
        self.InitResultHistos()

    def getUniqueID(self, name):
        ts = int(time.time() * 1e3)
        return'%s_%d_%d' % (name, self.k, ts)

    def convertStringToPH(self,i):
        try:
            retVal = int(i)
        except ValueError:
            retVal = -99999
        return retVal

    def InitResultHistos(self):
        self.histoFits = [None]*6
        self.histoFits[0] = ROOT.TH1D(self.getUniqueID("histoFit1"), "histoFit1", 200, 0.0001, 0.0003)
        self.histoFits[1] = ROOT.TH1D(self.getUniqueID("histoFit2"), "histoFit2", 400, 0, 2)
        self.histoFits[2] = ROOT.TH1D(self.getUniqueID("histoFit3"), "histoFit3", 300, 0.4, 0.7)
        self.histoFits[3] = ROOT.TH1D(self.getUniqueID("histoFit4"), "histoFit4", 160, 180., 340.)
        self.histoFits[4] = ROOT.TH1D(self.getUniqueID("histoFit5"), "histoFit5", 200, -1.5, -1.3)
        self.histoFits[5] = ROOT.TH1D(self.getUniqueID("histoFit6"), "histoFit6", 400, -4.e-4, 0.)
        self.histoChi = ROOT.TH1D(self.getUniqueID("histoChi"), "histoChi", 1000, 0., 10.)
        pass

    def ClearResultHistos(self):
        for histo in self.histoFits:
            histo.Reset()
        self.histoChi.Reset()

    def SaveResultHistos(self):
        if not self.DrawHistos:
            return
        self.c1 = ROOT.TCanvas()
        self.c1.Divide(3, 2)

        self.c1.cd(1)
        self.histoFits[0].Draw()

        self.c1.cd(2)
        self.histoFits[1].Draw()

        self.c1.cd(3)
        self.histoFits[2].Draw()

        self.c1.cd(4)
        self.histoFits[3].Draw()

        self.c1.cd(5)
        self.histoFits[4].Draw()

        self.c1.cd(6)
        self.histoChi.Draw()

    def FillResultHistos(self,results):

        self.histoChi.Fill(results[-1])
        i = 0
        for value in results[:-1]:
            if i < len(self.histoFits):
                self.histoFits[i].Fill(value)
            i += 1

    def AddToHistos(self,histos):
        if len(histos)!=2:
            raise Exception
        self.histoChi.Add(histos[0])
        for i in range(len(histos[1])):
            self.histoFits[i].Add(histos[1][i])

    def FitAllPHCurves(self, dir, nRocs):

        print "Fitting PH Curves %s"%dir
        maxChi2 = [-1]*4
        results = []

        if self.ParallelProcessing:
            Processes = []
            q = Queue()

            if self.LimitProcesses:
                FullRocRange = range(0,nRocs)
                RocRanges = [FullRocRange[x:x+self.LimitProcesses] for x in xrange(0, len(FullRocRange), self.LimitProcesses)]
                pass
            else:
                RocRanges = [range(0,nRocs)]

            for RocRange in RocRanges:
                # start n processes
                for chip in RocRange:
                    p = Process(target=self.FitPHCurve, args=(dir, chip, q,))
                    p.start()
                    Processes.append(p)

                # read back data
                for chip in RocRange:
                    results.append(q.get())

                # wait for all to finish
                for chip in RocRange:
                    Processes[chip].join()

        else:
            # use old way for compatibility
            threads = []
            result = Queue()
            for chip in range (0,nRocs):
                self.FitPHCurve(dir, chip, result)
                p = chip
                threads.append(p)

            results = [result.get() for p in threads]

        for chi2,histos in results :
            if chi2[0] ==-1:
                print 'Failed to fit in chip %s'%chi2[1]
            elif chi2[2] == -2:
                pass
                #print 'File already exists in chip %s'%chi2[1]
            else:
                if chi2[0] > maxChi2[0]:
                    maxChi2 = chi2
                self.AddToHistos(histos)

        if maxChi2[1] > -1:
            print "Total Max Chi^2 for chip %s: %s chi^2/NDF at %s/%s"%(maxChi2[1],maxChi2[0],maxChi2[2],maxChi2[3])
        self.SaveResultHistos()


    def FitPHCurve(self,dirName,chip,result):
        print "Fitting pulse height curves for chip %i"%chip

        inputFileName = '%s/'%dirName
        if self.HistoDict:
            dir = self.HistoDict.get('PHCalibrationFitting','dir')
            filename = self.HistoDict.get('PHCalibrationFitting','inputFileName')
            inputFileName += dir+'/'
            inputFileName += filename%chip
        else:
            inputFileName += 'phCalibration_C%i.dat'%(chip)
        inputFileName = os.path.abspath(inputFileName)

        try:
            inputFile = open(inputFileName,'r')
        except IOError as e:
            print "!!!!!!!!!  ----> PHCalibration: Could not open file %s to read pulse height calibration\n"%inputFileName
            print 'IOError: ',e
            retVal =[-1]*4
            retVal[1]=chip
            retVal = [retVal,[]]
            if result: result.put(retVal)
            return

        if self.fitMode ==3:
            outputFileName = '%s//phCalibrationFitTan_C%i.dat'%(dirName, chip)
        else:
            outputFileName = "%s/phCalibrationFit_C%i.dat"%( dirName, chip)
        if os.path.isfile(outputFileName) and not self.refit:
            print 'file "%s" already exists --> no fiting'%outputFileName
            retVal =[-2]*4
            retVal[1]=chip
            retVal = [retVal,[]]
            if result: result.put(retVal)
            return

        dataSet = inputFile.readlines()
        if self.verbose:
            print '\tLength of Dataset: %s'%len(dataSet)
        # remove header
        header = dataSet[:4]
        low_range = [int(i) for i in header[1].strip('\n').split(':')[1].strip().split()]
        high_range = [int(i) for i in header[2].strip('\n').split(':')[1].strip().split()]
        high_range_in_low_range = [i* self.rangeConversion for i in high_range]
        low_range.extend(high_range_in_low_range)
        self.vcalLow = low_range
        dataSet = dataSet[4:]

        outputFile = open(outputFileName, "w")

        outputFile.write("Parameters of the vcal vs. pulse height fits\n")
        if 3 == self.fitMode:
            outputFile.write("%s\n"%self.FitfcnTanName)
        else:
            outputFile.write("%s\n"%self.FitfcnName)
        outputFile.write("\n")

        maxChi2 = [-1]*4
        for data in dataSet:
                calibration = data.split()

                row = int(calibration[-1])
                column = int(calibration[-2])
                calibration = calibration[:-3]
                calibration = [self.convertStringToPH(i) for i in calibration]
                if len(calibration) != len(low_range):
                    raise Exception ('Length of PHCalibration file does not fit! %s' % calibration)
                if self.verbose:
                    print '\t',chip, column,row,":",calibration
                fitResult = self.Fit(calibration)
                isDead = False
                chi2 = fitResult[-1]
                if not isDead:
                    if chi2 > maxChi2[0]:
                        maxChi2 = [chi2, chip, column, row]
                self.FillOutputFile(outputFile,fitResult,column,row)
                self.FillResultHistos(fitResult)
        inputFile.close()
        outputFile.close()
        retVal = [maxChi2,[self.histoChi,self.histoFits]]
        print "\tMax Chi^2 for chip %s: %s chi^2/NDF at %s/%s"%(maxChi2[1],maxChi2[0],maxChi2[2],maxChi2[3])
        if result: result.put(retVal)
        return

    def FillOutputFile(self,outputFile,fitResult,column,row):
        for i in fitResult[:-1]:
            outputFile.write('%s\t'%i)
        outputFile.write('Pix %2d %2d\n'%(column,row))
        pass

    def Fit(self,calibration):
        if 0 == self.fitMode:
            return self.FitLin(calibration)
        elif 1 == self.fitMode:
            return self.FitTanPol(calibration)
        elif 3 == self.fitMode:
            return self.FitTanh(calibration)

    def InitFit(self):
        if 3 == self.fitMode:
            self.nFitParams = 4
        else:
            self.nFitParams = 6
        if 3 == self.fitMode:
            self.phFit = ROOT.TF1("phFit", "[3] + [2] * TMath::TanH([0]*x - [1])", 0, 1500.)
        else:
            self.phFit = ROOT.TF1("phFit", "TMath::Tan([0]*x - [4]) + [1]*x**3+ [5]*x[0]**2 + [2]*x[0] + [3]", -400., 1000.)
        self.phFit.SetNpx(1000)

    def getArrayOfCalibrationPoints(self, calibration, excludeLast=False, excludeSaturated=False):
        n = 0
        phs =[]
        vcals = []
        eph = []
        evcal = []
        i = 0
        for ph in calibration:
            IsLast = i > (len(calibration)-2)
            IsSaturated = ph > (self.SaturationPH - 1)
            if ph > 0 and (not IsSaturated or not excludeSaturated) and (not IsLast or not excludeLast):
                n += 1
                phs.append(ph)
                vcals.append(self.vcalLow[i])
                eph.append(self.ErrorPH)
                evcal.append(self.ErrorVcal)
            i += 1
        return  [n, phs, vcals, eph, evcal]

    def GetGraph(self,calibrationPoints):
        if self.verbose:
            print 'create graph with %s points '%calibrationPoints[0]
        graph = ROOT.TGraphErrors(calibrationPoints[0])
        for i in range(0,calibrationPoints[0]):
            i = int(i)
            graph.SetPoint(i,calibrationPoints[2][i],calibrationPoints[1][i])
            graph.SetPointError(i,calibrationPoints[4][i],calibrationPoints[3][i])
        return graph

    def FitTanh(self,calibration):
        calibrationPoints = self.getArrayOfCalibrationPoints(calibration, False, True)
        n = calibrationPoints[0]
        phs = calibrationPoints[1]
        vcals = calibrationPoints[2]
        graph = self.GetGraph(calibrationPoints)
        phFitClone = self.phFit
        phFitClone.SetParameter(0, 0.004)
        phFitClone.SetParameter(1, 1.4)
        phFitClone.SetParameter(2, 1000)
        phFitClone.SetParameter(3, 0)

        # set start parameters for fit
        upperPoint = n-1
        lowerPoint = 0

        try:
            MinVcal = vcals[lowerPoint]
            MaxVcal = vcals[upperPoint]

            phFitClone.SetRange(MinVcal, MaxVcal)

            if self.verbose:
                graph.Fit(phFitClone, "R", "")
            else:
                graph.Fit(phFitClone, "RQ")

            retVal = [phFitClone.GetParameter(i) for i in range(0,self.nFitParams)]
        except:
            retVal = [-1 for i in range(0,self.nFitParams)]

        try:
            retVal.append(phFitClone.GetChisquare() / phFitClone.GetNDF())
        except:
            retVal.append(0)
        if self.verbose:
            print retVal
        return retVal
        pass

    def FitTanPol(self,calibration):

        n,x,y,ex,ey = self.getArrayOfCalibrationPoints(calibration, True, False)
        graph = self.GetGraph([n,x,y,ex,ey])
        phFitClone = self.phFit

        # set start parameters for fit
        upperPoint = n-1
        lowerPoint = 0

        MinVcal = y[lowerPoint]
        MaxVcal = y[upperPoint]

        phFitClone.SetRange(MinVcal, MaxVcal)

        if (upperPoint in range (0,n)) and (lowerPoint in range(0,n)) and ((y[upperPoint] - y[lowerPoint]) != 0):
            slope = float(x[upperPoint] - x[lowerPoint]) / (y[upperPoint] - y[lowerPoint]) #really!
        else:
            slope = 0.5

        phFitClone.SetParameter(2, slope)
        phFitClone.SetParameter(3, y[upperPoint] - slope * x[upperPoint])
        par0 = (math.pi / 2. - 1.4) / x[-1];
        phFitClone.SetParameter(0, par0)
        phFitClone.SetParameter(1, 5.e-7)
        phFitClone.SetParameter(4, -1.4)
        if x[upperPoint] != 0.:
            #woher?
            par5 = (y[upperPoint]
                     - math.tan(phFitClone.GetParameter(0) * x[upperPoint] - phFitClone.GetParameter(4))
                     - phFitClone.GetParameter(1) * x[upperPoint] * x[upperPoint] * x[upperPoint]
                     - slope * x[upperPoint]
                     - phFitClone.GetParameter(3))
            par5 /=   (x[upperPoint]*x[upperPoint])
            phFitClone.SetParameter(5, par5)
        else:
            phFitClone.SetParameter(5, 0.)

        if self.verbose:
            graph.Fit("phFit", "R", "")
        else:
            graph.Fit("phFit", "RQ", "")

        retVal =  [phFitClone.GetParameter(i) for i in range(0,self.nFitParams)]
        retVal.append(phFitClone.GetChisquare() / phFitClone.GetNDF() if phFitClone.GetNDF() > 0 else 0)
        if self.verbose:
            print retVal
        return retVal

    def FitLin(self,calibration):
        n,phs,vcals,eph,evcal = self.getArrayOfCalibrationPoints(calibration, False, True)
        graph = self.GetGraph([n,phs,vcals,eph,evcal])

        phFitClone = self.phFit

        # set start parameters for fit
        upperPoint = n-1
        lowerPoint = 0

        try:
            MinVcal = vcals[lowerPoint]
            MaxVcal = vcals[upperPoint]

            phFitClone.SetRange(MinVcal, MaxVcal)

            if (upperPoint in range (0,n)) and (lowerPoint in range(0,n)) and ((vcals[upperPoint] - vcals[lowerPoint]) != 0):
                slope = float(phs[upperPoint] - phs[lowerPoint]) / (vcals[upperPoint] - vcals[lowerPoint])
            else:
                slope = 0.5

            phFitClone.SetParameter(2, slope)
            phFitClone.SetParameter(3, vcals[upperPoint] - slope * phs[upperPoint])
        except:
            #data is missing, or N/A
            return [0] * (self.nFitParams + 1)

        phFitClone.FixParameter(0, 0.)
        phFitClone.FixParameter(1, 0.)
        phFitClone.FixParameter(4, 0.)
        phFitClone.FixParameter(5, 0.)

        if self.verbose:
            graph.Fit("phFit", "R", "")
        else:
            graph.Fit("phFit", "RQ", "")

        retVal = [phFitClone.GetParameter(i) for i in range(0,self.nFitParams)]
        retVal.append(phFitClone.GetChisquare() / phFitClone.GetNDF() if phFitClone.GetNDF() > 0 else 0)
        return retVal

if __name__=='__main__':
    fitter = PH_Fitting(3)
    fitter.FitAllPHCurves('.',16)

