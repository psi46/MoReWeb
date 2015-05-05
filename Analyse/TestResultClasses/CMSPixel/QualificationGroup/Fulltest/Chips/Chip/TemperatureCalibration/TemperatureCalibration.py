import ROOT
import AbstractClasses
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):


    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_Fulltest_Chips_Chip_TemperatureCalibration_TestResult'
        self.NameSingle = 'TemperatureCalibration'
        self.Enabled = False
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'


    '''
    def PopulateResultData(self):

        TemperatureCalibrationFileName = "{Directory}/TemperatureCalibration_C{ChipNo}.dat".format(Directory,ChipNo=self.ParentObject.Attributes['ChipNo'])
        TemperatureCalibrationFile = open(TemperatureCalibrationFileName, "r")

        #sprintf(string, "%s/../T-calibration/TemperatureCalibration_C%i.dat", dirName, chipId);
        if ( TemperatureCalibrationFile ):
            self.analyse(Directory, self.ParentObject.Attributes['ChipNo']);

        # TGraph
        self.ResultData['Plot']['ROOTObject'] =  self.ParentObject.ParentObject.FileHandle.Get("TempCalibration_C{ChipNo}".format(ChipNo=self.ParentObject.Attributes['ChipNo']) ).Clone(self.GetUniqueID())


        if self.ResultData['Plot']['ROOTObject']:
            self.ResultData['Plot']['ROOTObject'].Draw("A*");


        self.SaveCanvas()
        self.Title = 'Address Levels: C{ChipNo}'.format(ChipNo=self.ParentObject.Attributes['ChipNo'])
        
    def analyse(self, directoryName, chipId)
        tl = ROOT.TLatex()

        numTempRanges   = 8;
        minADCvalue_graph =    0.;
        maxADCvalue_graph = 2000.;
        temperatureValues_target[numTemperatures] = [ -20, -15, -10, -5, 0, 5, 10, 15, 20, 25, 30 ]; # degrees C

        #--- initialize internal data-structures
        self.initialize();

        #--- read last DAC temperature information used as "training" data
        self.load(directoryName, chipId);

        #--- prepare output graphs

        for itemprange in range(numTempRanges):
            graph = self.ResultData['HiddenData']['gADCgraph']_Measurement[chipId][itemprange];

            numPoints = 0
            for itemperature in range(numTemperatures):
                adcValue     = self.ResultData['HiddenData']['gADCvalue']_Measurement[chipId][itemprange][itemperature];
                blackLevel = self.ResultData['HiddenData']['gADCvalue']_blackLevel[chipId][itemperature];
                #--- only include measurements that correspond to a positive voltage difference
                #(i.e. have an ADC value above the black level)
                #and are within the amplification linear range, below the amplifier saturation
                if ( adcValue > minADCvalue_graph and adcValue < maxADCvalue_graph ):
                    graph.SetPoint(numPoints, temperatureValues_target[itemperature], adcValue);
                    numPoints+=1




            for itemprange in range(numTempRanges):
                graph = self.ResultData['HiddenData']['gADCgraph']_Calibration[chipId][itemprange];

                numPoints = 0;
                for itemperature in range(numTemperatures):
                    adcValue = self.ResultData['HiddenData']['gADCvalue']_Calibration[chipId][itemprange][itemperature];
                    blackLevel = self.ResultData['HiddenData']['gADCvalue']_blackLevel[chipId][itemperature];
                    #--- only include measurements that correspond to a positive voltage difference
                    #(i.e. have an ADC value above the black level)
                    #and are within the amplification linear range, below the amplifier saturation
                    if ( adcValue > minADCvalue_graph && adcValue < maxADCvalue_graph ):
                        graph.SetPoint(numPoints, temperatureValues_target[itemperature], adcValue);
                        numPoints++;

            #--- initialise dummy histogram
            # (neccessary for drawing graphs)
            dummyHistogram = ROOT.TH1F("dummyHistogram", "dummyHistogram", numTemperatures, temperatureValues_target[0] - 1, temperatureValues_target[numTemperatures - 1] + 1);
            dummyHistogram.SetTitle("");
            dummyHistogram.SetStats(False);
            # dummyHistogram.GetXaxis().SetTitle("T / degrees");
            dummyHistogram.GetXaxis().SetTitleOffset(1.2);
            # dummyHistogram.GetYaxis().SetTitle("ADC");
            dummyHistogram.GetYaxis().SetTitleOffset(1.3);
            dummyHistogram.SetMaximum(1.25*maxADCvalue_graph);

            #--- prepare graph showing range in which the temperature has been measured
            #and the precision of the cooling-box of reaching the temperature setting
            dummyHistogram.GetXaxis().SetTitle("T/C");
            dummyHistogram.GetXaxis().SetTitleOffset(0.5);
            dummyHistogram.GetXaxis().SetTitleSize(0.06);
            # dummyHistogram.GetYaxis().SetTitle("T_{actual} / degrees");
            dummyHistogram.SetMinimum(minADCvalue_graph);
            dummyHistogram.SetMaximum(maxADCvalue_graph);

            #--- draw output graphs
            legendTempRanges = ROOT.TLegend(0.13, 0.47, 0.68, 0.87, NULL, "brNDC");
            legendTempRanges.SetFillColor(10);
            legendTempRanges.SetLineColor(10);

            #   TString title = Form("ADC Measurement for ROC%i", chipId);
            #   dummyHistogram.SetTitle(title);
            legendTempRanges.Clear();
            numGraphs = 0
            for itemprange in range(numTempRanges):
                if ( self.ResultData['HiddenData']['gADCgraph']_Measurement[chipId][itemprange].GetN() >= 2 ):
                    if ( numGraphs == 0 ) dummyHistogram.Draw();
                    self.ResultData['HiddenData']['gADCgraph']_Measurement[chipId][itemprange].SetLineColor((itemprange % 8) + 1);
                    self.ResultData['HiddenData']['gADCgraph']_Measurement[chipId][itemprange].SetLineStyle((itemprange / 8) + 1);
                    self.ResultData['HiddenData']['gADCgraph']_Measurement[chipId][itemprange].SetLineWidth(2);
                    self.ResultData['HiddenData']['gADCgraph']_Measurement[chipId][itemprange].Draw("L");
                    numGraphs+=1
                    label = "Vref = {:3.2f}".format( vReference[itemprange])
                    legendTempRanges.AddEntry(self.ResultData['HiddenData']['gADCgraph']_Measurement[chipId][itemprange], label, "l");



            tl.DrawLatex(0.12, 0.92, "ADC Measurement");
            if numGraphs > 0:
                legendTempRanges.Draw();

                # gCanvas.Update();
                # gPostScript.NewPage();
            }



            # TString title = Form("ADC Calibration for ROC%i", chipId);
            # dummyHistogram.SetTitle(title);
            legendTempRanges.Clear();
            numGraphs = 0;
            for itemprange in range(numTempRanges):
                if ( self.ResultData['HiddenData']['gADCgraph']_Calibration[chipId][itemprange].GetN() >= 2 ):
                    if ( numGraphs == 0 ) dummyHistogram.Draw();
                    self.ResultData['HiddenData']['gADCgraph']_Calibration[chipId][itemprange].SetLineColor((itemprange % 8) + 1);
                    self.ResultData['HiddenData']['gADCgraph']_Calibration[chipId][itemprange].SetLineStyle((itemprange / 8) + 1);
                    self.ResultData['HiddenData']['gADCgraph']_Calibration[chipId][itemprange].SetLineWidth(2);
                    self.ResultData['HiddenData']['gADCgraph']_Calibration[chipId][itemprange].Draw("L");
                    numGraphs+=1
                    label = "Vref = {:3.2f}".format( vReference[itemprange])
                    legendTempRanges.AddEntry(self.ResultData['HiddenData']['gADCgraph']_Calibration[chipId][itemprange], label, "l");



            tl.DrawLatex(0.12, 0.92, "ADC Calibration");
            if ( numGraphs > 0 ):
                legendTempRanges.Draw();
                # gCanvas.Update();
                # gPostScript.NewPage();

            #   delete gCanvas;
            #   delete gPostScript;

    def load(self, directoryName, iroc):

        #--- read last DAC temperature information from file

        #printf("chipSummary> Analysing last DAC temperature measurement for ROC %i\n", iroc);

        TemperatureCalibrationFileName = "{Directory}/TemperatureCalibration_C{ChipNo}.dat".format(Directory,ChipNo=self.ParentObject.Attributes['ChipNo'])
        TemperatureCalibrationFile = open(TemperatureCalibrationFileName, "r")

        for itemperature in range(numTemperatures):

            temperatureIndex = ((numTemperatures - 1) - itemperature);

            *inputFile >> dummyString;
            *inputFile >> dummyString;

            Char_t sign;
            *inputFile >> sign;
            if ( sign == '0' ){
                actualTemperature = 0;
            } else {
                *inputFile >> actualTemperature;
                if ( sign == '+' )
            actualTemperature *= +1;
                else if ( sign == '-' )
            actualTemperature *= -1;
                else
            cerr << "Warning in <analyse>: cannot parse file " << inputFileName << " !" << endl;
            }

            *inputFile >> dummyString;
            *inputFile >> dummyString;
            *inputFile >> dummyString;
            *inputFile >> self.ResultData['HiddenData']['gADCvalue']_blackLevel[iroc][temperatureIndex];
            *inputFile >> dummyString;

            *inputFile >> dummyString;
            *inputFile >> dummyString;
            *inputFile >> dummyString;

            for ( Int_t itemprange = 0; itemprange < numTempRanges; itemprange++ ){
                *inputFile >> self.ResultData['HiddenData']['gADCvalue']_Calibration[iroc][itemprange][temperatureIndex];
            }

            *inputFile >> dummyString;
            *inputFile >> dummyString;
            *inputFile >> dummyString;
            *inputFile >> dummyString;
            for ( Int_t itemprange = 0; itemprange < numTempRanges; itemprange++ ){
                *inputFile >> self.ResultData['HiddenData']['gADCvalue']_Measurement[iroc][itemprange][temperatureIndex];
            }

            *inputFile >> dummyString;


        delete inputFile;

    def initialize(self)
    {
        #--- initialise graphical output
        #    gROOT.SetStyle("Plain");
        #    gStyle.SetTitleBorderSize(0);
        #    gStyle.SetPalette(1,0);

        #    gCanvas.SetFillColor(10);
        #    gCanvas.SetBorderSize(2);

        #    gPostScript = new TPostScript("svTemperatureAnalysis.ps", 112);

        #--- initialise internal data structures
        for ( Int_t iroc = 0; iroc < numROCs; iroc++ ){
            for ( Int_t itemprange = 0; itemprange < numTempRanges; itemprange++ ){
                for ( Int_t itemperature = 0; itemperature < numTemperatures; itemperature++ ){
                    self.ResultData['HiddenData']['gADCvalue']_blackLevel[iroc][itemperature]                           = 0;
                    self.ResultData['HiddenData']['gADCvalue']_Measurement[iroc][itemprange][itemperature] = 0;
                    self.ResultData['HiddenData']['gADCvalue']_Calibration[iroc][itemprange][itemperature] = 0;
                }
            }
        }

        #--- initialise histograms and graphs for:
        #        o ADC value as function of calibration voltage
        #            (histogram shown for one ROC at at time only and fitted with a linear function)
        #        o ADC value as function of temperature
        #            (histogram shown for one ROC at at time only and fitted with a linear function)
        for ( Int_t iroc = 0; iroc < numROCs; iroc++ ){
            for ( Int_t itemprange = 0; itemprange < numTempRanges; itemprange++ ){
                self.ResultData['HiddenData']['gADCgraph']_Measurement[iroc][itemprange] = new TGraph();
                TString graphName = Form("self.ResultData['HiddenData']['gADCgraph']_Measurement_C%i_TempRange%i", iroc, itemprange);
                self.ResultData['HiddenData']['gADCgraph']_Measurement[iroc][itemprange].SetName(graphName);

                self.ResultData['HiddenData']['gADCgraph']_Calibration[iroc][itemprange] = new TGraph();
                TString graphName = Form("self.ResultData['HiddenData']['gADCgraph']_Calibration_C%i_TempRange%i", iroc, itemprange);
                self.ResultData['HiddenData']['gADCgraph']_Calibration[iroc][itemprange].SetName(graphName);
            }
        }
    }'''
