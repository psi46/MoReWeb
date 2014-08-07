
import ROOT
from multiprocessing import Pool, Process, Queue, Pipe
import sys,os
import math
import time

class SCurve_Fitting():
    nCols = 52
    nRows = 80
    def __init__(self, refit = True, HistoDict = None, chi2Limit = 2.0, ePerVcal = 50.0, verbose = False):
        print 'SCURVE Fitting'
        ROOT.gStyle
        self.verbose = verbose
        self.refit = refit
        self.DrawHistos = False
        self.HistoDict = HistoDict
        if self.HistoDict and self.HistoDict.has_option('SCurveFitting','nTrigs'):
            self.nReadouts = self.HistoDict.getint('SCurveFitting','nTrigs')
        else:
            self.nReadouts = 50
        self.chiLimit = chi2Limit
        self.ePerVcal = ePerVcal
        self.slope = self.getVcal(0,255)/256
        print "ePerVcal ",self.ePerVcal
        print 'slope: ',self.slope
        print 'nTrigs',self.nReadouts
        self.InitFit()
#         self.InitResultHistos()

    #todo/fixme: calibration How should that data be stored?
    def getVcal(self,mode,i):
        vcal0 = [0.0000, 0.0015, 0.0028, 0.0042, 0.0053, 0.0053, 0.0080, 0.0094, 0.0089, 0.0103, 0.0116, 0.0130, 0.0141, 0.0156, 0.0169, 0.0183, 0.0205, 0.0219, 0.0232, 0.0246, 0.0256, 0.0269, 0.0283, 0.0296, 0.0292, 0.0305, 0.0319, 0.0332, 0.0343, 0.0357, 0.0371, 0.0384, 0.0404, 0.0417, 0.0430, 0.0444, 0.0454, 0.0467, 0.0481, 0.0494, 0.0489, 0.0503, 0.0516, 0.0530, 0.0541, 0.0555, 0.0568, 0.0582, 0.0604, 0.0617, 0.0630, 0.0643, 0.0653, 0.0667, 0.0680, 0.0693, 0.0688, 0.0702, 0.0715, 0.0728, 0.0739, 0.0753, 0.0766, 0.0780, 0.0805, 0.0818, 0.0831, 0.0844, 0.0854, 0.0867, 0.0880, 0.0894, 0.0889, 0.0902, 0.0915, 0.0929, 0.0940, 0.0953, 0.0967, 0.0967, 0.1002, 0.1015, 0.1028, 0.1041, 0.1051, 0.1064, 0.1077, 0.1090, 0.1085, 0.1099, 0.1112, 0.1125, 0.1136, 0.1149, 0.1163, 0.1176, 0.1196, 0.1209, 0.1221, 0.1235, 0.1244, 0.1257, 0.1270, 0.1283, 0.1278, 0.1291, 0.1304, 0.1318, 0.1329, 0.1342, 0.1355, 0.1369, 0.1391, 0.1404, 0.1417, 0.1430, 0.1439, 0.1452, 0.1465, 0.1478, 0.1472, 0.1486, 0.1499, 0.1512, 0.1523, 0.1536, 0.1550, 0.1563, 0.1569, 0.1582, 0.1594, 0.1607, 0.1616, 0.1629, 0.1642, 0.1655, 0.1649, 0.1662, 0.1675, 0.1689, 0.1700, 0.1713, 0.1726, 0.1740, 0.1762, 0.1775, 0.1787, 0.1800, 0.1809, 0.1822, 0.1834, 0.1848, 0.1841, 0.1854, 0.1867, 0.1881, 0.1891, 0.1905, 0.1918, 0.1933, 0.1952, 0.1965, 0.1977, 0.1991, 0.2001, 0.2011, 0.2021, 0.2031, 0.2031, 0.2041, 0.2051, 0.2071, 0.2081, 0.2091, 0.2111, 0.2121, 0.2141, 0.2161, 0.2171, 0.2181, 0.2191, 0.2201, 0.2211, 0.2231, 0.2221, 0.2231, 0.2241, 0.2261, 0.2271, 0.2281, 0.2301, 0.2311, 0.2341, 0.2341, 0.2361, 0.2371, 0.2381, 0.2391, 0.2411, 0.2421, 0.2411, 0.2421, 0.2441, 0.2451, 0.2461, 0.2471, 0.2491, 0.2491, 0.2531, 0.2541, 0.2551, 0.2561, 0.2571, 0.2581, 0.2591, 0.2611, 0.2601, 0.2611, 0.2621, 0.2641, 0.2651, 0.2661, 0.2681, 0.2691, 0.2721, 0.2731, 0.2741, 0.2751, 0.2761, 0.2771, 0.2781, 0.2791, 0.2781, 0.2801, 0.2811, 0.2821, 0.2831, 0.2851, 0.2861, 0.2881, 0.2901, 0.2921, 0.2931, 0.2941, 0.2941, 0.2951, 0.2961, 0.2981, 0.2971, 0.2981, 0.2991, 0.3011, 0.3021, 0.3031, 0.3051, 0.3071]
        vcal1 = [0.0000, 0.0093, 0.0183, 0.0274, 0.0344, 0.0436, 0.0525, 0.0616, 0.0586, 0.0678, 0.0767, 0.0859, 0.0933, 0.1025, 0.1114, 0.1207, 0.1355, 0.1444, 0.1531, 0.1620, 0.1689, 0.1689, 0.1865, 0.1955, 0.1924, 0.2017, 0.2097, 0.2197, 0.2267, 0.2357, 0.2447, 0.2537, 0.2667, 0.2757, 0.2837, 0.2927, 0.2997, 0.3087, 0.3167, 0.3257, 0.3227, 0.3317, 0.3407, 0.3497, 0.3567, 0.3657, 0.3747, 0.3837, 0.3977, 0.4067, 0.4157, 0.4237, 0.4307, 0.4397, 0.4487, 0.4567, 0.4537, 0.4627, 0.4717, 0.4807, 0.4877, 0.4967, 0.5047, 0.5137, 0.5307, 0.5397, 0.5477, 0.5567, 0.5627, 0.5717, 0.5797, 0.5887, 0.5857, 0.5947, 0.6027, 0.6117, 0.6187, 0.6277, 0.6367, 0.6457, 0.6597, 0.6687, 0.6767, 0.6857, 0.6917, 0.7007, 0.7087, 0.7177, 0.7147, 0.7227, 0.7317, 0.7397, 0.7477, 0.7557, 0.7647, 0.7737, 0.7867, 0.7947, 0.8027, 0.8117, 0.8177, 0.8267, 0.8347, 0.8427, 0.8397, 0.8487, 0.8567, 0.8657, 0.8727, 0.8817, 0.8897, 0.8897, 0.9137, 0.9217, 0.9297, 0.9377, 0.9447, 0.9527, 0.9607, 0.9697, 0.9657, 0.9747, 0.9827, 0.9917, 0.9987, 1.0067, 1.0157, 1.0247, 1.0277, 1.0367, 1.0447, 1.0527, 1.0587, 1.0667, 1.0747, 1.0837, 1.0797, 1.0877, 1.0967, 1.1047, 1.1117, 1.1207, 1.1297, 1.1377, 1.1527, 1.1607, 1.1687, 1.1767, 1.1817, 1.1907, 1.1977, 1.2067, 1.2027, 1.2107, 1.2187, 1.2277, 1.2347, 1.2427, 1.2517, 1.2607, 1.2727, 1.2807, 1.2887, 1.2967, 1.3017, 1.3097, 1.3177, 1.3257, 1.3207, 1.3297, 1.3377, 1.3457, 1.3527, 1.3607, 1.3697, 1.3787, 1.3917, 1.3997, 1.4067, 1.4147, 1.4187, 1.4267, 1.4337, 1.4417, 1.4367, 1.4447, 1.4527, 1.4597, 1.4657, 1.4737, 1.4817, 1.4897, 1.5027, 1.5097, 1.5147, 1.5207, 1.5237, 1.5297, 1.5347, 1.5407, 1.5367, 1.5427, 1.5477, 1.5537, 1.5567, 1.5627, 1.5677, 1.5727, 1.5797, 1.5837, 1.5867, 1.5897, 1.5917, 1.5947, 1.5977, 1.6017, 1.5987, 1.6027, 1.6057, 1.6087, 1.6107, 1.6147, 1.6177, 1.6177, 1.6247, 1.6267, 1.6287, 1.6307, 1.6317, 1.6337, 1.6357, 1.6377, 1.6367, 1.6387, 1.6407, 1.6427, 1.6447, 1.6467, 1.6487, 1.6517, 1.6547, 1.6567, 1.6577, 1.6587, 1.6597, 1.6607, 1.6627, 1.6637, 1.6627, 1.6647, 1.6657, 1.6677, 1.6687, 1.6707, 1.6717, 1.6737]
        if mode == 0 and i in range(len(vcal0)):
            return vcal0[i]
        if mode == 1 and i in range(len(vcal1)):
            return vcal1[i]
        return -1

    def InitFit(self):
        self.scurveFit = ROOT.TF1("Fit","[0]*TMath::Erf([2] * (x-[1])) + [3]",0,.230)


    def FitAllSCurve(self,dir,nRocs):
        print "Fitting SCurves %s"%dir
        maxChi2 = [-1]*4
        results = []
#             p = Process(target=self.FitPHCurve, args=(dir,chip,result))
        for chip in range(0,nRocs):
            results.append(self.FitSCurve(dir, chip))
            #
        for chi2,histos in results :
            if chi2[0] ==-1:
                print 'Failed to to fit in chip %s'%chi2[1]
            elif chi2[2] == -2:
                print 'File already exists in chip %s'%chi2[1]
            else:
                if chi2[0] > maxChi2[0]:
                    maxChi2 = chi2
                self.AddToHistos(histos)

        print "Total Max Chi^2 for chip %s: %s chi^2/NDF at %s/%s"%(maxChi2[1],maxChi2[0],maxChi2[2],maxChi2[3])
        self.SaveResultHistos()
        if self.verbose:
            raw_input('done with SCurve fitting for all ROCs. Press enter.')

    def AddToHistos(self,histos):
        pass

    def SaveResultHistos(self):
        pass

    def getInputFile(self,dirName,chip):
        inputFileName = '%s/'%dirName
        if self.HistoDict:
            dir = self.HistoDict.get('SCurveFitting','dir')
            filename = self.HistoDict.get('SCurveFitting','inputFileName')
            inputFileName += dir+'/'
            inputFileName += filename%chip
        else:
            inputFileName += 'SCurveData_C%i.dat'%(chip)
        inputFileName = os.path.abspath(inputFileName)
        print inputFileName
        try:
            inputFile = open(inputFileName,'r')
        except IOError as e:
            print "!!!!!!!!!!  ----> SCurve: Could not open file %s to read the SCurve data results\n"%inputFileName
            print 'IOError: ',e
            retVal =[-1]*4
            retVal[1]=chip
            retVal = [retVal,[]]
            return retVal
        return inputFile

    def getOutputFile(self,dirName,chip):
        outputFileName = '%s//SCurve_C%i.dat'%(dirName, chip)
        if os.path.isfile(outputFileName) and not self.refit:
            print 'file "%s" already exists --> no fiting'%outputFileName
            retVal =[-2]*4
            retVal[1]=chip
            retVal = [retVal,[]]
            return retVal
        outputFile = open(outputFileName, "w")
        outputFile.write("Threshold Sigma\n\n")
        return outputFile

    def FitSCurve(self,dirName,chip):
        print "Fitting SCurve for chip %i"%chip
        inputFile = self.getInputFile(dirName,chip)
        if type(inputFile)==list:
            return inputFile
        outputFile = self.getOutputFile(dirName,chip)
        if type(outputFile) == list: return outputFile

        dataSet = inputFile.readlines()
        if self.verbose:
            print '\tLength of Dataset: %s'%len(dataSet)
        # remove header
        header = dataSet[0].split()
        for i in header:
            if 'mode' in i.lower():
                index = header.index(i)
                if len(header) > index + 1:
                    self.mode = int(header[index + 1])
#                     raw_input('Mode: %d' % self.mode)
            if 'ntrig' in i.lower():
                index = header.index(i)
                print index, len(header), index + 1,
                if len(header) > index + 1:
                    self.nReadouts = int(header[index + 1])
#                     raw_input('Ntrig: %d' % self.nReadouts)
        dataSet = dataSet[1:]

#         maxChi2 = [-1]*4
        assert len(dataSet)== self.nCols*self.nRows
        badPixels = []
        for col in range(self.nCols):
            for row in range(self.nRows):
                data = [int(i) for i in  dataSet[col*self.nRows+row].split()]
                [chi2, fitResults] = self.fitSCurveData(data,chip,row,col)
                if fitResults:
                    outputFile.write("%+.3e %+.3e   Pix %2i %2i\n"%(fitResults[0],fitResults[1],col,row))
                else:
                    outputFile.write("NAN NAN   Pix %2i %2i\n"%(col,row))
                    badPixels.append((chip,col,row))
                    if self.verbose:
                        print 'problem with chip %s, col %s, row %s'%(chip,col,row)
        print 'Problem with %s / %s Pixels: '%(len(badPixels),self.nRows*self.nCols)
        print badPixels
        inputFile.close()
        outputFile.close()
        return [chi2,[]]


    def fitSCurveData(self,data,chip,row,col):
        if self.verbose:
            print 'fit Scurve data ROC %d %2d/%2d' % (chip, row, col)
        isValid, calibrationPoints = self.extractSCurveData(data)
        if not isValid:
            print '\tnot Valid'
            return [[-3,chip,row,col],[]]
        graph = self.GetGraph(calibrationPoints)

        self.scurveFit.SetParameters(self.nReadouts/2., graph.GetMean(), 167., self.nReadouts/2.)         #// half amplitude, threshold (50% point), width, offset
        graph.Fit(self.scurveFit, "Q", "", 0.0, 0.3);
#         if row ==0 and col == 0:
#             graph.Draw('APL')
        chi2 = self.scurveFit.GetChisquare() / self.scurveFit.GetNDF();

        notConverged = ("FAILED    " in ROOT.gMinuit.fCstatu) or (ROOT.gMinuit.fEDM > 1.e-4)    #//if fEDM very small, convergence failed only due to limited machine accuracy
        fitFailed = notConverged or chi2> self.chiLimit
        thr = -1.
        sig = -1.
        if not fitFailed: #  if not failed
            thr = self.scurveFit.GetParameter(1) * self.ePerVcal / self.slope  #// conversion Vcal voltage -> Vcal DACs -> electrons
            sig = 1. / (math.sqrt(2.) * self.scurveFit.GetParameter(2)) * self.ePerVcal / self.slope  # conversion Vcal voltage -> Vcal DACs -> electrons
#             if self.verbose: print 'Threshold: ',thr,'sigma: ',sig
        else:
            if self.verbose:
                if (chi2 > self.chiLimit):
                    print "Chi %e"%chi2
                else:
                    print "not converged"
        return [[chi2,chip,row,col],[thr,sig]]
        pass

    def extractSCurveData(self,data):
        n = data[0]
        start = data[1]
        data = data[2:]
        assert len(data) == n
        isDeadPixel = True
        isBadPixel = False
        plateau = False
        zeroLevel = False
        x = []
        y = []
        ex = []
        ey = []
        if self.verbose:
            print data,self.nReadouts
        for i in range(n):
            value = data[i]
            isDeadPixel= isDeadPixel and value == 0
            if plateau and value ==0:
                value = self.nReadouts
            if value<0 or value > self.nReadouts: isBadPixel = True
            if value == self.nReadouts: plateau = True
            zeroLevel = zeroLevel or value == 0
            x.append(self.getVcal(0,start+i))
            ex.append(0)
            eff = (value+1)/(self.nReadouts +2.)
            y.append(self.nReadouts*eff)
            if self.nReadouts + 3. == 0:
                eq.append(0)
            ey.append(self.nReadouts * math.sqrt(abs((eff * (1 - eff)) / (self.nReadouts + 3.))))
        if not plateau or not zeroLevel:
            if self.verbose:
                if not plateau:
                    print 'Plateau: ',plateau
                if not zeroLevel:
                    print 'ZeroLevel: ',zeroLevel
            isBadPixel = True

        if self.verbose:
            if isDeadPixel: print 'dead Pixel'
            if isBadPixel:  print 'bad Pixel'
        isValidPixel = not (isBadPixel or isDeadPixel)
        return isValidPixel,[n,x, y, ex, ey]


    def GetGraph(self,calibrationPoints):
        if self.verbose:
#             print calibrationPoints
            print 'create graph with %s points '%calibrationPoints[0]
        graph = ROOT.TGraphErrors(calibrationPoints[0])
        for i in range(0,calibrationPoints[0]):
            i = int(i)
            graph.SetPoint(i,calibrationPoints[1][i],calibrationPoints[2][i])
            graph.SetPointError(i,calibrationPoints[3][i],calibrationPoints[4][i])
        return graph

if __name__=='__main__':
    fitter = SCurve_Fitting()
    fitter.FitAllSCurve('/Users/peller/pixel/TestModuleData/storage/test/',16)
