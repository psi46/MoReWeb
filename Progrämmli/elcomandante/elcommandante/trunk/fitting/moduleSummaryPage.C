#include <TMath.h>
#include <iostream>
using namespace std;

const char* fileName = "commander_Fulltest.root";
const char* adFileName = "adDec.root"; 

char fname[200];
FILE *inputFile, *critFile;

TCanvas *c1 = NULL;
TLatex *tl;     
TLatex *ts;
TLine *line;
TBox *box;

TString directory;

float defectsB, defectsC, maskdefC;
float currentB, currentC, slopeivB;

float noiseB,    noiseC,    noiseDistr;
float trimmingB, trimmingC, trmDistr;
float gainB,     gainC,     gainDistr; 
float pedestalB, pedestalC, pedDistr;
float par1B,     par1C,     par1Distr;

float gainMin, gainMax,  par1Min,    par1Max;  
float noiseMin, noiseMax,   tthrTol;

int vcalTrim(60);

int nChips(16);
int startChip(0);
int readVerbose(1);

int fitsProblemB[] = {0, 0, 0, 0 , 0 };
int fitsProblemC[] = {0, 0, 0, 0 , 0 };
int currentProblemB(0), currentProblemC(0);
int slopeProblemB(0),   slopeProblemC(0);
 


// ----------------------------------------------------------------------
void all() {

  // -- find all files matching pattern in the current directory
  void *dirp = gSystem->OpenDirectory(".");
  const char *afile;
  while(afile = gSystem->GetDirEntry(dirp)) {
    if (strstr(afile, "M")) {
      cout << afile << endl;
      moduleSummary(afile);
    }
  }

}


// ----------------------------------------------------------------------
void moduleSummary(const char *dirName = "", const char *module_type,const char *ivDirName = "") 
{

  directory = TString(dirName);
  ivDirectory = TString(ivDirName);

  printf("\nmoduleSummary> Starting ...\n");

  nChips = 16;
  startChip = 0;
	
  if ( !strcmp(module_type,"a") ) {
    
    nChips = 8; 
    startChip = 0; 
  }
  
  if ( !strcmp(module_type,"b") ) {
    
    nChips = 8; 
    startChip = 8; 
  }

  sprintf(fname, "%s/%s", dirName, fileName);
  inputFile = fopen(fname, "r");
  if (!inputFile) { 

    printf("\nmoduleSummary> ----> COULD NOT FIND %s IN DIRECTORY %s\n", fileName, dirName);
    printf("moduleSummary> ----> Aborting execution of moduleSummaryPage.C ... \n\n", fileName, dirName);   
    break; 
  }

  
  sprintf(fname, "%s/%s", dirName, adFileName);
  inputFile = fopen(fname, "r");
  if (!inputFile) {
    
    sprintf(adFileName,"%s", fileName); 
  }
  else {
    
    printf("moduleSummary> ----> found separate address decoding file: %s\n", adFileName); 
    fclose (inputFile); 
  }
  
  sprintf(fname, "%s/../../macros/criteria-full.dat", dirName);
  if ( !readCriteria(fname) ) {  
    
    printf("\nmoduleSummary> ----> COULD NOT READ GRADING CRITERIA !!!\n");
    printf("moduleSummary> ----> Aborting execution of moduleSummaryPage.C ... \n\n", fileName, dirName);  
    break;
  }

  TFile *f = new TFile(Form("%s/%s", dirName, fileName));

  gROOT->SetStyle("Plain");
  
  gStyle->SetPalette(1);
  gStyle->SetOptStat(0);
  gStyle->SetTitle(0);

  gStyle->SetStatFont(132);
  gStyle->SetTextFont(132);
  gStyle->SetLabelFont(132, "X");
  gStyle->SetLabelFont(132, "Y");
  gStyle->SetLabelSize(0.08, "X");
  gStyle->SetLabelSize(0.08, "Y");
  gStyle->SetTitleSize(0.08, "X");
  gStyle->SetTitleSize(0.08, "Y");
  gStyle->SetNdivisions(10, "X");
  gStyle->SetNdivisions(8, "Y");
  gStyle->SetTitleFont(132);
    
  gROOT->ForceStyle();
  
  tl = new TLatex;
  tl->SetNDC(kTRUE);
  tl->SetTextSize(0.1);
  
  ts = new TLatex;
  ts->SetNDC(kTRUE);
  ts->SetTextSize(0.09);

  line = new TLine;
  line->SetLineColor(kRed);
  line->SetLineStyle(kDashed);

  box = new TBox;
  box->SetFillColor(3);
  box->SetFillStyle(3004);
	
  c1 = new TCanvas("c1", "", 900, 700);
  c1->Clear();
  c1->Divide(1,4);
    
  int EColor[6]        = { 6, 8, 1, 2, 4};  
  int EMarkerStyle[10] = { 6, 24, 23, 26, 6, 21, 28, 20, 30, 29 };

  TH2D *mThreshold = new TH2D("mThreshold", "", 416, 0., 416., 160, 0., 160.);
  TH2D *mBumps     = new TH2D("mBumps",     "", 416, 0., 416., 160, 0., 160.);
  TH2D *mAddr      = new TH2D("mAddr",      "", 416, 0., 416., 160, 0., 160.);  

  double mThresholdmin(0.), mThresholdmax(255.);


  const int nfit = 5;  
  TString fitNames[] = {TString("Noise"), TString("Vcal Thr. Width"), TString("Rel. Gain Width"),
			TString("Pedestal Spread"), TString("Parameter1")};

  float limitB[] = { noiseB, trimmingB, gainB, pedestalB, par1B  };   // limit for grading
  float limitC[] = { noiseC, trimmingC, gainC, pedestalC, par1C };    // limit for grading
  float max[]    = { noiseB + 100., trimmingB + 100., gainB + 0.05, pedestalB + 1000., 4.5 }; // scaling of 
                                                                                              // histogram

  TH1D *fit[nfit];
  TH1D *fitEntries[nfit];

  for(int ifit = 0; ifit < nfit; ++ifit) {

    fit[ifit] = new TH1D(Form("%s", fitNames[ifit].Data()),"", nChips, float(startChip), float(startChip+nChips));
    fitEntries[ifit] = new TH1D(Form("n%s", fitNames[ifit].Data()),"", nChips, float(startChip), float(startChip+nChips));

    fit[ifit]->SetLineColor(EColor[ifit]);
    fit[ifit]->SetMarkerColor(EColor[ifit]);
    fit[ifit]->SetMarkerStyle(EMarkerStyle[ifit]);
    fit[ifit]->SetMarkerSize(0.5);
  }
 
  for (int i = startChip; i < startChip+nChips; i++) { addVcalThreshold(dirName, i, mThreshold); }
  for (int i = startChip; i < startChip+nChips; i++) { addChip("vcals_xtalk", i, mBumps); }

  TFile *f1 = new TFile(Form("%s/%s", dirName, adFileName));
  for (int i = startChip; i < startChip+nChips; i++) { addChip("AddressDecoding", i, mAddr);}
  
  if ( nChips < 16 && startChip == 0 ) { 
    for (int i = 8; i < nChips+8; i++) { removeChip(i, mThreshold, -99); }
    for (int i = 8; i < nChips+8; i++) { removeChip(i, mBumps, -99); }
    for (int i = 8; i < nChips+8; i++) { removeChip(i, mAddr, -99); }
  }

  if ( nChips < 16 && startChip == 8 ) { 
    for (int i = 0; i < nChips; i++) { removeChip(i, mThreshold, -99); }
    for (int i = 0; i < nChips; i++) { removeChip(i, mBumps, -99); }
    for (int i = 0; i < nChips; i++) { removeChip(i, mAddr, -99); }
  }

  TString noslash(dirName);
  noslash.ReplaceAll("/", "");
  noslash.ReplaceAll("..", "");
  
  c1->cd(1);

  if ( mThreshold->GetMaximum() < mThresholdmax ) { 
    mThresholdmax = mThreshold->GetMaximum();
  }
  if ( mThreshold->GetMinimum() > mThresholdmin ) {
    mThresholdmin = mThreshold->GetMinimum();
  }
  mThreshold->GetZaxis()->SetRangeUser(mThresholdmin,mThresholdmax);
  mThreshold->DrawCopy("colz");
  tl->DrawLatex(0.1, 0.92, "Vcal threshold");
  tl->DrawLatex(0.75, 0.92, Form("%s",noslash.Data()));

  if ( nChips < 16 && startChip == 0 ) { 
   
    box->SetFillColor(29);
    box->DrawBox( 0, 0,  416,  80);
  }

  if ( nChips < 16  && startChip == 8 ) { 
   
    box->SetFillColor(29);
    box->DrawBox( 0, 80,  416,  160);
  }



  c1->cd(2);
  mBumps->SetMaximum(2.);
  mBumps->SetMinimum(-2.);  
  mBumps->DrawCopy("colz");
  tl->DrawLatex(0.1, 0.92, "Bump bonding map");

  if ( nChips < 16 && startChip == 0 ) { 
   
    box->SetFillColor(29);
    box->DrawBox( 0, 0,  416,  80);
  }

  if ( nChips < 16 && startChip == 8 ) { 
   
    box->SetFillColor(29);
    box->DrawBox( 0, 80,  416,  160);
  }
  
  c1_3->Divide(3,1);
  c1_3->cd(1);
  gPad->SetBottomMargin(0.2);
  gPad->SetLogy(1);
  gPad->SetLeftMargin(0.20);
  gPad->SetRightMargin(0.01);
  
  float V, A;
  float x_V[250], y_A[250];
  int i(0); 
  float iv100(0.);
  float iv150(0.);
  float iv150_17(0.);
  float iv100_17(0.);
  float variation(0.);
  float variation_17(0.);
  
  FILE *ivFile, *sumWrite, *sumRead, *gradWrite; 
    
  sprintf(fname, "%s/ivCurve.log", ivDirName);
  ivFile = fopen(fname, "r");
  
  if (!ivFile)
  {
    printf("moduleSummary> !!!!!!!!!  ----> Could not open file %s to read data\n", fname);
  }
  
  else {
  
    fclose(ivFile);
    //
    //
    TNtuple *ivTuple = new TNtuple("ivTuple","ivTuple","timestamp:voltage:current");
    int inputs = ivTuple->ReadFile(fname);
    cout<<"read "<<inputs <<" lines into ivTuple..."<<endl;
    if (inputs==0){
        cerr<<"Error!!!!"<<endl;
        exit(-1);
    }
    
/*
    ifstream is(fname);
    
    char  buffer[200];
*/

  float I, V,TS;
  ivTuple->SetBranchAddress("voltage",&V);
  ivTuple->SetBranchAddress("current",&I);
  ivTuple->SetBranchAddress("timestamp",&TS);
  vector<Float_t> x_VV;
  vector<Float_t> y_I;
  TDatime time;
  for (int i =0; i<ivTuple->GetEntries()&&i<250;i++){
    ivTuple->GetEntry(i);
    cout<<i<<"-"<<TS<<"\t"<<V<<"-"<<I<<endl;
    if(i==1){
    time = int(TS);
    //cout<<time.GetYear()<<"-"<<time.GetMonth()<<"-"<<time.GetDay()<<endl;
    tday =time.GetDay();
    tmon =time.GetMonth();
    tyear=time.GetYear();
    }
    x_V[i]=-1.*V;
    y_A[i]=-1e6*I;
    if(I>-1e-10)
        continue;
    x_VV.push_back(-1.*V);
    y_I.push_back(-1e6*I);
    if ( i > 0 ) {
	    if ( x_V[i] >= 100. && x_V[i-1] <= 100. ) { iv100 = y_A[i-1] + (100. - x_V[i-1])*(y_A[i] - y_A[i-1])/(x_V[i] - x_V[i-1]); }
	    if ( x_V[i] >= 150. && x_V[i-1] <= 150. ) { iv150 = y_A[i-1] + (150. - x_V[i-1])*(y_A[i] - y_A[i-1])/(x_V[i] - x_V[i-1]); }
    }
  }
      /*
    while (is.getline(buffer, 200, '\n')) {
      
      // check that line starts with a number
      if (buffer[0] != '1' && buffer[0] != '2' && buffer[0] != '3' && buffer[0] != '4' && 
	  buffer[0] != '5' && buffer[0] != '6' && buffer[0] != '7' && buffer[0] != '8' && buffer[0] != '9'  )  {continue;} 
      
      sscanf(buffer, "%e %e", &V, &A);
      
      x_V[i] = V;
      y_A[i] = 1e6*A;
      
      if ( i > 0 ) {
	
        // check that voltage is increasing & find current at 150 V 
        if ( x_V[i] < x_V[i-1] ) { continue; } //REALLY??
	if ( x_V[i] >= 100. && x_V[i-1] <= 100. ) { iv100 = y_A[i-1] + (100. - x_V[i-1])*(y_A[i] - y_A[i-1])/(x_V[i] - x_V[i-1]); }
	if ( x_V[i] >= 150. && x_V[i-1] <= 150. ) { iv150 = y_A[i-1] + (150. - x_V[i-1])*(y_A[i] - y_A[i-1])/(x_V[i] - x_V[i-1]); }
	
      }
      
      i++;
      
    }
*/
     
 
    if ( iv100 != 0. ) { variation = iv150/iv100; }
    else               { variation = 0; }

    if ( i > 0 ) {
    
      TGraph *g1 = new TGraph(x_VV.size(),&x_VV.at(0),&y_I.at(0));

      g1->Draw("aC");
      g1->SetTitle("");
      g1->SetLineColor(4);
      g1->SetLineWidth(2);
    
      g1->GetXaxis()->SetTitle("Voltage [V]");
      g1->GetYaxis()->SetTitle("Current [#muA]");
      g1->GetYaxis()->SetDecimals();
      g1->GetYaxis()->SetTitleOffset(1.2);
      g1->GetYaxis()->CenterTitle();
  
      tl->DrawLatex(0.2, 0.92, "I-V-Curve");
      ts->DrawLatex(0.25, 0.78, Form("I(150 V) = %.2f #muA", iv150));
      ts->DrawLatex(0.25, 0.65, Form("I_{150}/I_{100} =  %.2f ", variation));

    }   
  }
    
  char mod[20] = noslash.Data(), waf[20] = "",  test[20] = "",tbla[20], trim[20], ph[20], cycl[20];
  int tday,tmon,tyear;
  int tbla1;
  int dp(0), dm(0), db(0), dt(0), da(0);
  int no(0), th(0), ga(0), pe(0), pa(0);
  int root(0), a(0), b(0), c(0); 
  int badRocs[3] = {0, 0, 0};
  char iv;
  float voltage, current; 
  float temp, tempSigma, sollTemp;
  float cyclMean, cyclSigma;
  char  string[1000];
  
  c1_3->cd(2);
  
  sprintf(fname, "%s/summaryTest.txt", dirName);
  sumRead = fopen(fname, "r");

  double y;
  if (!sumRead)
  {
    printf("\nmoduleSummary> !!!!!!!!!  ----> File %s does not exist yet...\n", fname);
    printf("moduleSummary> !!!!!!!!!  ----> Module summary not complete!\n\n");
  }
  else
  {
    fgets(string, 200, sumRead);
    //   fscanf(sumRead, "%s %s", string, mod);
    fscanf(sumRead, "%s %s %s %s", string, string, waf, test);
    fscanf(sumRead, "%s %i %i %i %i %i", string, &dp, &dm, &db, &dt, &da);
    fscanf(sumRead, "%s %i %i %i %i %i", string, &no, &th, &ga, &pe, &pa);
    fscanf(sumRead, "%s %s %s %s %s %i %i %i", string, string, string, string, string, &a, &b, &c);
    badRocs[0]=a;  badRocs[1]=b;  badRocs[2]=c;
    fscanf(sumRead, "%s %s %i", string, string, &root);
    fscanf(sumRead, "%s %s %s %s %s %i %s %s", string, string, string, string, tbla, &tbla1, string, string);

    fgets(string, 200, sumRead);
    fscanf(sumRead, "%s %s", string, trim);
    fgets(string, 200, sumRead); 
    fscanf(sumRead, "%s %s", string, ph);
    fgets(string, 200, sumRead);
    
    fscanf(sumRead, "%s %f %f %s %f", string, &temp, &tempSigma, string, &sollTemp); 
    fscanf(sumRead, "%s %s %s %f %f", string, string, cycl, &cyclMean, &cyclSigma);

    fclose(sumRead);
    
    tl->SetTextSize(0.09);
    tl->SetTextFont(22);
    y = 0.92;
    tl->DrawLatex(0.01, y, Form("Test Summary of %s     %s", waf, test));
    tl->SetTextFont(132); 
    tl->SetTextSize(0.09);

    y -= 0.16;
    tl->DrawLatex(0.01, y, "ROCs > 1% defects: ");
    tl->DrawLatex(0.5, y, Form("%i", badRocs[0]));
    
    y -= 0.12;
    tl->DrawLatex(0.01, y, Form("Dead Pixel: "));
    tl->DrawLatex(0.5, y, Form("%i", dp));

    y -= 0.11;
    tl->DrawLatex(0.01, y, "Mask Defects: ");
    tl->DrawLatex(0.5, y, Form("%i", dm));

    y -= 0.11;
    tl->DrawLatex(0.01, y, "Dead Bumps: ");
    tl->DrawLatex(0.5, y, Form("%i", db));

    y -= 0.11;
    tl->DrawLatex(0.01, y, "Noisy Pixel: ");
    tl->DrawLatex(0.5, y, Form("%i", no));

    y -= 0.11;
    tl->DrawLatex(0.01, y, "Trim Problems: ");
    tl->DrawLatex(0.5, y, Form("%i", th));

    y -= 0.11;
    tl->DrawLatex(0.01, y, Form("PH Defects: "));
    tl->DrawLatex(0.3, y, Form("%i/", ga));
    
    tl->SetTextColor(kRed);
    tl->DrawLatex(0.4, y, Form("%i/",pe));
    tl->SetTextColor(kBlack);
    
    tl->SetTextColor(kBlue);
    tl->DrawLatex(0.5, y, Form("%i",pa));
    tl->SetTextColor(kBlack);

    y = 0.76;
    tl->DrawLatex(0.72, y, Form("Tested on:"));
    y -= 0.11;
    tl->DrawLatex(0.72, y, "Temp. [^{o}C]:  ");
    y -= 0.11;
    tl->DrawLatex(0.72, y, "Trim / phCal: ");
    y -= 0.11;
    tl->DrawLatex(0.72, y, "Therm. cycl.: ");
    y -= 0.11;
    tl->DrawLatex(0.72, y, "TBM1: ");
    y -= 0.11;
    tl->DrawLatex(0.72, y, "TBM2: ");

    c1_3->cd(3);
    y = 0.76;
    tl->DrawLatex(0.01, y, Form("%i %i %i", tday, tmon,tyear));
    
    y -= 0.11;
    tl->DrawLatex(0.01, y, Form("%.1f +- %.1f", temp, tempSigma));
              
    y -= 0.11;
    
    tl->DrawLatex(0.01, y, Form("%3s / %3s", trim, ph));

    y -= 0.11;
    tl->DrawLatex(0.01, y, Form("%s", cycl));

  }

  int result;
  int tbm1(1), tbm2(1);
  TParameter<int>* par;
  
  y -= 0.11;
  par = (TParameter<int>*)f->Get("TBM1");
  if (par)
  {
  	tbm1 = par->GetVal();
  	if (tbm1 == 0) tl->DrawLatex(0.01, y, "ok");   
  	else tl->DrawLatex(0.01, y, Form("Err%i", tbm1));   
  }

  y -= 0.11;
  par = (TParameter<int>*)f->Get("TBM2");
  if (par)
  {
	tbm2 = par->GetVal();
	if (tbm2 == 0) tl->DrawLatex(0.01, y, "ok");   
	else tl->DrawLatex(0.01, y, Form("Err%i", tbm2));   
  }


  // Convert current to currents at room temperature
  double Tk = 273.15;
  double egap = 1.12;
  double kB = 8.617343E-5;
  double tTest;
  // tTest = temp;  // --> averaged temperature
  tTest = sollTemp;
  
  double expnt  = egap*(1/(Tk+tTest) - 1/(Tk+17))/(2*kB);
  double fctr   = (Tk+17)*(Tk+17)/((Tk+tTest)*(Tk+tTest));
  
  iv150_17 = iv150*fctr*TMath::Exp(expnt);
  iv100_17 = iv100*fctr*TMath::Exp(expnt);
  if ( iv100_17 != 0 ) variation_17 = iv150_17/iv100_17;
    
  printf("\nmoduleSummary> converted I(150 V, %.0f C)    = %.4f       to  I(150 V, 17 C)    = %.4f \n", tTest, iv150, iv150_17);
  printf("moduleSummary> converted I(100 V, %.0f C)    = %.4f       to  I(100 V, 17 C)    = %.4f \n\n", tTest, iv100, iv100_17);

  
  if ( iv150_17 != 0 ) {
    c1_3->cd(3);
    y = 0.21;
    tl->DrawLatex(0.25, y, "I(150 V) [T = 17 ^{o}C]");
    tl->DrawLatex(0.72, y, Form("%.2f #muA", iv150_17));
    c1_3->cd(2);
    
  }

  if ( iv100_17 != 0 ) {
    c1_3->cd(3);
    y = 0.10;
    tl->DrawLatex(0.25, y, "I_{150}/I_{100}   [T = 17 ^{o}C]");
    tl->DrawLatex(0.72, y, Form("%.2f", variation_17));
    c1_3->cd(2);
  }


  sprintf(fname, "%s/summaryTest.txt", dirName);
  cout<<"CREATE FILE"<<fname<<endl;
  
  sumWrite = fopen(fname, "a");
  fputs(Form("TBM1 %i\n", tbm1), sumWrite);
  fputs(Form("TBM2 %i\n", tbm2), sumWrite);
  fputs(Form("I 150 %f \n", iv150_17), sumWrite);
  fputs(Form("I150/I100 %f \n", variation_17), sumWrite);
  fputs(Form("iv datapoints %i \n", i), sumWrite);

//   c1->cd(4);
//   mAddr->DrawCopy("colz");
//   mAddr->SetMaximum(1.);
//   mAddr->SetMinimum(0.);
//   tl->DrawLatex(0.1, 0.92, "Address decoding map");



  c1_4->Divide(nfit,1);
  qualification(dirName, fit, fitEntries);
  
 printf("Test\n"); 

  for (int i = 0; i < nfit; i++) {

  // makePlot(TH1 *h, const char *title, int pad, double Ymin, double Ymax, double Ylimit)
    makePlot(fit[i], fitNames[i].Data(), i+1, 0, max[i], limitB[i], limitC[i]); 
  
  }

 printf("debug\n");
  int grad(0);

  FILE *missingData; 
  sprintf(fname, "%s/comment_3.txt", dirName);
  missingData = fopen(fname, "r");

  if ( missingData ) {

    printf("\nmoduleSummary> !!!!!!!!!  ----> Found file for missing data: comment_3.txt => GRADE C!\n\n");
    grad = 3;
    fclose(missingData);

  } else {
  
    grad = grading(badRocs, iv150_17, variation_17, fit, fitEntries, limitB, limitC, test);
  }
  
  c1_3->cd(3);    
  tl->SetTextSize(0.09);
  tl->SetTextFont(22);
 
  if (grad == 1) {  tl->DrawLatex(0.6, 0.92, "GRADE:  A");  fputs("Grade A\n", sumWrite); }
  if (grad == 2) {  tl->DrawLatex(0.6, 0.92, "GRADE:  B");  fputs("Grade B\n", sumWrite); }
  if (grad == 3) {  tl->DrawLatex(0.6, 0.92, "GRADE:  C");  fputs("Grade C\n", sumWrite); }  


  sprintf(fname, "%s/gradingTest.txt", dirName);
  gradWrite = fopen(fname, "a");
 
  if (!gradWrite)
  {
    printf("\nmoduleSummary> !!!!!!!!!  ----> File %s does not exist yet...\n", fname);
    printf("moduleSummary> !!!!!!!!!  ----> Grading data could not be written to file!\n\n");
  }
  else
  {

    fputs(Form("Noise %i %i\n", fitsProblemB[0], fitsProblemC[0]), gradWrite);
    fputs(Form("VcalThrWidth %i %i\n", fitsProblemB[1], fitsProblemC[1]), gradWrite);
    fputs(Form("RelGainWidth %i %i\n", fitsProblemB[2], fitsProblemC[2]), gradWrite);
    fputs(Form("PedSpread %i %i\n", fitsProblemB[3], fitsProblemC[3]), gradWrite);
    fputs(Form("MeanParameter1 %i %i\n", fitsProblemB[4], fitsProblemC[4]), gradWrite);
    fputs(Form("I150V %i %i\n", currentProblemB, currentProblemC), gradWrite);
    fputs(Form("Iratio %i 0\n",  slopeProblemB), gradWrite);
  }
  
  c1->SaveAs(Form("%s/moduleSummary_%s%s.ps", dirName, waf, test));
  c1->SaveAs(Form("%s/%s%s.png", dirName, waf, test));
  
  // -- Address level plots
  FILE *psFile;
  char alvl_plot[200];
  sprintf(alvl_plot, "%s/AddressLevelFits_%s%s.ps", dirName, waf, test);
  
  printf("moduleSummary> Looking for address level: %s\n", alvl_plot);
  psFile = fopen(alvl_plot, "r");
  
  if (psFile) { 
    
    printf("moduleSummary> ----> Address level plot %s already exists\n", alvl_plot);
    fclose(psFile);
    
    printf("\nmoduleSummary> ................................................ finished\n");
    return;
  }
  
  c1->Clear();
  c1->Divide(4,4);


  for (int i = startChip; i < startChip+nChips; i++) { 

    c1->cd(i+1);    

    h1 = (TH1D*)gFile->Get(Form("AddressLevels_C%i", i));
    if (h1) {
      h1->SetTitle("");
      h1->GetXaxis()->SetRangeUser(-1500., 1500.);
      h1->DrawCopy();
      fitPeaks(h1, dirName, i);
      tl->DrawLatex(0.1, 0.92, Form("Address Levels: C%i", i));
    }
  }

  c1->SaveAs(Form("%s/AddressLevelFits_%s%s.ps", dirName, waf, test));
  c1->SaveAs(Form("%s/alvl_%s%s.png", dirName, waf, test));

  printf("\nmoduleSummary> ................................................ finished\n");
}




// ----------------------------------------------------------------------
void addChip(const char *hist, int chip, TH2D *h3) {
 
  int icol, irow, value;

  TH2D *h2 = (TH2D*)gFile->Get(Form("%s_C%d", hist, chip));
  
  if ( h2 ) {
    for (icol = 0; icol < 52; icol++) {
      for (irow = 0; irow < 80; irow++)  {

	value = h2->GetBinContent(icol+1, irow+1);

	if (chip < 8) {h3->SetBinContent(415-(chip*52+icol)+1, 159-irow+1, value);}
	if (chip > 7) {h3->SetBinContent((chip-8)*52+icol+1, irow+1, value);}
      }
    }
  }
 
}

// ----------------------------------------------------------------------
void removeChip(int chip, TH2D *h3, int value) {
 
  int icol, irow;
  
  for (icol = 0; icol < 52; icol++) {
    for (irow = 0; irow < 80; irow++)  {
      
      if (chip < 8) {h3->SetBinContent(415-(chip*52+icol)+1, 159-irow+1, value);}
      if (chip > 7) {h3->SetBinContent((chip-8)*52+icol+1, irow+1, value);}
    }
  }
}

// ----------------------------------------------------------------------
void addVcalThreshold(char *dirName, int chip, TH2D *h3) 
{
 
  int icol, irow, value;

  float thr, sig;
  int a,b;
  int VcalOut = 0;
  FILE *inputFile;
  char string[200];
  sprintf(string, "%s/SCurve_C%i.dat", dirName, chip);
  inputFile = fopen(string, "r");
  if (!inputFile)
  {
	 printf("moduleSummary> !!!!!!!!!  ----> SCurve: Could not open file %s to read fit results\n", string);
  }
  else {
    for (int i = 0; i < 2; i++) fgets(string, 200, inputFile);
    
    for (icol = 0; icol < 52; icol++) {
      for (irow = 0; irow < 80; irow++)  {
	
	fscanf(inputFile, "%e %e %s %2i %2i\n", &thr, &sig, string, &a, &b); 
	value = thr / 65;
	
	if (chip < 8) {h3->SetBinContent(415-(chip*52+icol)+1, 159-irow+1, value);}
	if (chip > 7) {h3->SetBinContent((chip-8)*52+icol+1, irow+1, value);}

      }
    }
  }
}
//-----------------------------------------------------------------------------------------
void makePlot(TH1 *h, const char *title, int pad, float Ymin, float Ymax, float YlimitB, float YlimitC) {

  double mean, rms, y(0.76);
  c1_4->cd(pad);
  gPad->SetLeftMargin(0.15);

  for (int i = startChip; i < startChip+nChips; i++) {
    if ( h->GetBinContent(i+1) > Ymax ) {
      Ymax = h->GetBinContent(i+1)+0.2* h->GetBinContent(i+1);
    }
    if ( h->GetBinContent(i+1) < Ymin ) {

      Ymin = h->GetBinContent(i+1)-0.2* h->GetBinContent(i+1);
    }
  }
 
  h->GetYaxis()->SetRangeUser(Ymin, Ymax);
  h->DrawCopy("LP");
  
  if (YlimitB < Ymax) {
    line->DrawLine(startChip,YlimitB,startChip+nChips,YlimitB);
  }

  if ( YlimitC < Ymax ) {
    line->DrawLine(startChip,YlimitC,startChip+nChips,YlimitC);
  }
  
  mean = calcMean(h);
  rms = calcRMS(h, mean);
  
  tl->DrawLatex(0.2, 0.93, Form("%s", title));
  char title2[200];
  if (pad == 3) { sprintf(title2, "%s [\%]", title);  mean = 100*mean; rms = 100*rms; }
  else if (pad == 5) { sprintf(title2, "%s []", title);}
  else  { sprintf(title2, "%s [e]", title); }
  y -= 0.11*(pad-1); 
  c1_3->cd(3);
  tl->DrawLatex(0.25, y, Form("%s",title2));
  //  tl->DrawLatex(0.72, y, Form("%.1f +- %.1f", mean, rms));
  tl->DrawLatex(0.72, y, Form("%.1f", mean));
  
}



//-----------------------------------------------------------------------------------------
int grading(int *rocs, double i150, double ratio, TH1D *h1[5], TH1D *h2[5],
	    float *criteriaB, float *criteriaC, const char *testNr) {

  double value(0.), nValue(0.);
  int gr(1); 
  int jbin(0);
   
  for (int i = 0; i < 5; i++) {
    for (int j = startChip; j < startChip+nChips; j++) {
      
      jbin = j - startChip;
      value  = h1[i]->GetBinContent(jbin+1); 
      nValue = h2[i]->GetBinContent(jbin+1); 

      // Grading 
      if ( (gr == 1) && (value > criteriaB[i]) ) { gr = 2; }
      if ( (value > criteriaC[i]) )              { gr = 3; }
      if ( (gr == 1) && (nValue < (4160 - defectsB)) )    { gr = 2; }
      if ( (nValue < (4160 - defectsC)) )                 { gr = 3; }
      
      // Failures reasons...
      if ( (value > criteriaB[i]) && (value < criteriaC[i]) ) { fitsProblemB[i]++; }
      if ( (value > criteriaC[i]) )                           { fitsProblemC[i]++; }

    }
  }

  if ( !strcmp(testNr,"T+17a") ) { 

    // Grading
    if( (gr == 1) && (rocs[1] > 0       ) )  { gr = 2; }
    if( (gr == 1) && (i150    > currentB) )  { gr = 2; }
    if( (gr == 1) && (ratio   > slopeivB) )  { gr = 2; }
    
    if( (rocs[2] > 0       ) )  { gr = 3; }
    if( (i150    > currentC) )  { gr = 3; }
    
    // Failures reasons...
    if( (i150  > currentB) && (i150 < currentC) )  { currentProblemB++; }
    if( (i150  > currentC) )  { currentProblemC++;}
    if( (ratio > slopeivB) )  { slopeProblemB++;}
  }
  
  
  if ( !strcmp(testNr,"T-10b") ||  !strcmp(testNr,"T-10a") ) {
    
    // Grading
    if( (gr == 1) && (rocs[1] > 0           ) )  { gr = 2; }
    if( (gr == 1) && (i150    > 1.5*currentB) )  { gr = 2; }
    if( (gr == 1) && (ratio   > slopeivB    ) )  { gr = 2; }
    
    if( (rocs[2] > 0           ) )  { gr = 3; }
    if( (i150    > 1.5*currentC) )  { gr = 3; }
    
    // Failures reasons...
    if( (i150  > 1.5*currentB) && (i150 < 1.5*currentC) )  { currentProblemB++; }
    if( (i150  > 1.5*currentC) )    { currentProblemC++;}
    if( (ratio > slopeivB    ) )    { slopeProblemB++;}
    
    
  }
  
  return gr;
  
  
}

//-----------------------------------------------------------------------------------------
void qualification(const char *dir, TH1D *h1[5], TH1D *h2[5]) {
  
  float nN(0.),  mN(0.),  sN(0.),  nV(0.), mV(0.), sV(0.);
  float nG(0.),  mG(0.),  sG(0.),  nP(0.), mP(0.), sP(0.);
  float nP1(0.), mP1(0.), sP1(0.);
  float relGainWidth(0.), PedSpread(0.); 
  char string[2000];
  int ibin(0);
  
 printf("Test1\n"); 
  for ( int i = startChip; i < startChip+nChips; i++ ) {
    
    nN = 0.;  mN = 0.;  sN = 0.; 
    nV = 0.;  mV = 0.;  sV = 0.; 
    nG = 0.;  mG = 0.;  sG = 0.; 
    nP = 0.;  mP = 0.;  sP = 0.;
    nP1 = 0.; mP1 = 0.; sP1 = 0.;

    FILE *fitFile;
    sprintf(fname, "%s/summary_C%i.txt", dir, i);    
    fitFile = fopen(fname, "r");
    
    if ( !fitFile ) {
      
      printf("moduleSummary> !!!!!!!!!  ----> FITS: Could not find %s in %s\n", fname, dir);
      continue;
    }
    else {
      
      relGainWidth = 0;
      PedSpread    = 0;
              
      fclose(fitFile);
      ifstream is(fname);
	 
      char  buffer[200];
      float m(0.), s(0.);
      int n(0);
     	 
      while (is.getline(buffer, 200, '\n')) {
	   
	if (buffer[0] == 'n' )  {continue;}
	   
	sscanf(buffer,"%s %i %f %f",string, &n, &m, &s);  

	if ( !strcmp(string, "SCurve") )    { nN = n;  mN = m;  sN = s; }
	if ( !strcmp(string, "Threshold") ) { nV = n;  mV = m;  sV = s; printf("threshold yes \n"); }
	if ( !strcmp(string, "Gain") )      { nG = n;  mG = m;  sG = s; }
	if ( !strcmp(string, "Pedestal") )  { nP = n;  mP = m;  sP = s; }
	if ( !strcmp(string, "Parameter1")) { nP1 = n; mP1 = m; sP1 = s;}

      }
	 
 
      // Noise
      ibin = i - startChip;
      h1[0]->SetBinContent(ibin+1, mN);
      h1[0]->SetBinError(ibin+1, sN);
      h2[0]->SetBinContent(ibin+1, nN);
      
      printf("sV %f nV %f \n", 65*sV, nV);

      // Threshold Vcal Width
      h1[1]->SetBinContent(ibin+1, 65*sV);
      h2[1]->SetBinContent(ibin+1, nV);
      
      // Gain
            if ( mG!=0 ) { if ( sG/mG < 4 ) { relGainWidth = sG/mG; } }
      h1[2]->SetBinContent(ibin+1, relGainWidth);
      h2[2]->SetBinContent(ibin+1, nG);
      
      // Pedestal
      //if ( mG!=0 ) { if ( sG/mG < 4 ) { PedSpread = 65*sP; } }
      if ( mG!=0 ) { if ( sG/mG < 100 ) { PedSpread = 65*sP; } }
      h1[3]->SetBinContent(ibin+1, PedSpread);
      h2[3]->SetBinContent(ibin+1, nP);
      
      // Parameter1
      h1[4]->SetBinContent(ibin+1, mP1);
      h1[4]->SetBinError(ibin+1, sP1);
      h2[4]->SetBinContent(ibin+1, nP1);
      
    }


  }

printf("YES\n");

}
//-----------------------------------------------------------------
void fitPeaks(TH1D *h, const char *d, int chipId) {  

  cout << " ---> Searching for peaks for chip " << chipId << endl;
  const int npeaks = 10;

//   TSpectrum *s    = new TSpectrum(14); // 2*NrOfPeaks = 14
//   Int_t nfound    = s->Search(h,10,"new",0.1);
//   Float_t *peaks  = s->GetPositionX();
//   Float_t *peaksY = s->GetPositionY();

//   Float_t first_peak =  peaks[0];  
//   Float_t last_peak =  peaks[0];  

//   Int_t nexp(7), cnt1(0), cnt2(0), tried(0);
//   bool bad_peaks;

//   bad_peaks = (peaks[0] < -1000) || (peaks[0] > 200) || (peaks[nfound-1] > 1000);

//   // -- Validate peaks
//   if ( nfound != nexp || bad_peaks ) {
        
//     while ( (nfound != nexp || bad_peaks )  && (cnt1 < 10) ) { 
      
//       cnt1++; cnt2 = 0;
      
//       while ( (nfound != nexp || bad_peaks )  && (cnt2 < 10) ) {
	
// 	cnt2++; tried++;
	
// 	if(nfound != nexp) cout << " --> " << tried << ". try: Not enough peaks (" << nfound << " of 7) ..."<< endl;
// 	if( bad_peaks ) cout << " --> " << tried << ". try: Bad peak position ..." << endl;
	
// 	nfound    = s->Search(h,10-cnt1,"new",cnt2*0.05);
// 	peaks     = &(s->GetPositionX());
// 	peaksY    = &(s->GetPositionY());
	
// 	bad_peaks = (peaks[0] < -1000) || (peaks[0] > 200) || (peaks[nfound-1] > 1000);
//       }	  
//     }
//   }

  Float_t start[npeaks];
  Float_t stop[npeaks];

  Float_t alvlStart[npeaks];
  Float_t alvlStop[npeaks];

  Float_t alvlMean[npeaks];
  Float_t alvlWidth[npeaks];
  Float_t alvlRMS[npeaks];

  Float_t mean;
  Float_t rms;
  Float_t total(0);

  int nfound(0);

  TH1D *hpeak = new TH1D("peaks", "", 3000, -1500, 1500);
  hpeak->SetMarkerStyle(29); 
  hpeak->SetMarkerSize(1.5);
  hpeak->SetMarkerColor(kRed);

  for ( int i = h->GetXaxis()->GetFirst(); i < h->GetXaxis()->GetLast() && nfound <= npeaks; i++ ) {

    if ( h->GetBinContent(i) > 10 ) {

      start[nfound] = i;

      mean = 0;
      rms  = 0;
      total = 0;

      while ( h->GetBinContent(i) > 10 
	      || h->GetBinContent(i+10) > 10 ) { // Fluctuation at the beginning of the peaks ...

	mean += i*h->GetBinContent(i);
	total  += h->GetBinContent(i);
	i++;
      }

      stop[nfound]  = i;

      mean = int(mean/total);
      alvlMean[nfound] = h->GetBinCenter(mean);
      hpeak->SetBinContent(hpeak->FindBin(alvlMean[nfound]), h->GetBinContent(mean));

      alvlStart[nfound] = h->GetBinCenter(start[nfound]);
      alvlStop[nfound]  = h->GetBinCenter(stop[nfound]);
      alvlWidth[nfound] = h->GetBinCenter(stop[nfound]) - h->GetBinCenter(start[nfound]);

      for ( int j =  start[nfound]; j < stop[nfound]; j++ ) {
	
	rms += (mean - j)*(mean - j)*h->GetBinContent(j);
      }
      
      alvlRMS[nfound] =  h->GetBinWidth(mean)*TMath::Sqrt(rms/total);

      nfound++;

      while (h->GetBinContent(i) >  2) i++;
    }
  }

//   return; 

  if ( nfound != 7 ) {
    
    cout << "Could not find address levels ..." << endl;
    fillEmptyAL(d, chipId);
    return;
  }

  cout << "Found " << nfound << " candidate peaks to fit" << endl;

  Double_t ranges[14];

  for (int k = 0; k < nfound; k++) {
      
    ranges[k]   = alvlMean[k] - 25. ;
    ranges[k+1] = alvlMean[k] + 25. ;
    printf("%i. peak at %d (fit range [%d, %d])\n",k, alvlMean[k], ranges[k], ranges[k+1]);
  }

  Double_t prob[7];
  Double_t chi2[7];
  Double_t ndof[7];
  Double_t par[21];
  Double_t parE[21];

  Int_t cnt3(0), cnt4(0);
  Double_t width_error(100);

  for (int k = 0; k < nfound; k++) {

    cnt3 = 0; cnt4 = 0;

    h->Fit("gaus","Q","same", ranges[k], ranges[k+1]);
    width_error= h->GetFunction("gaus")->GetParError(2);
    
    // -- reduce fit range
    while ( width_error > 5 && cnt3 < 20 ) {
      
      cout << " --> high sigma error, reduce fit range ... " << endl;
      cnt3++;
      
      h->Fit("gaus","Q","same", ranges[k]+cnt3, ranges[k+1]-cnt3);
      width_error = h->GetFunction("gaus")->GetParError(2);
    }
    
    // -- enlarge fit range
    while ( width_error > 5 && cnt4 < 20 ) {
      
      cout << " --> high sigma error, enlarge fit  range ... " << endl;
      cnt4++;
      
      h->Fit("gaus","Q","same", ranges[k]-cnt4, ranges[k+1]+cnt4);
      width_error = h->GetFunction("gaus")->GetParError(2);
    }
    

    if ( width_error > 5 ) {

      cout << "Could not fit address levels ..." << endl;
      fillEmptyAL(d, chipId);
      return;
    }


    h->GetFunction("gaus")->SetLineColor(kBlue);
    h->GetFunction("gaus")->SetLineWidth(0.2);

    chi2[k]  = h->GetFunction("gaus")->GetChisquare();
    prob[k]  = h->GetFunction("gaus")->GetProb();
    ndof[k]  = h->GetFunction("gaus")->GetNDF();
    
    for (int m = 0; m < 3; m++) {
      par[3*k + m]  = h->GetFunction("gaus")->GetParameter(m);
      parE[3*k + m] = h->GetFunction("gaus")->GetParError(m);
    }
  }
  
  for (int k = 0; k < 7; k++) { 
    drawFit(par[3*k], par[3*k + 1], par[3*k + 2])->Draw();     
  }
  
  cout << " Saving it to " << Form("%s/addlevels_C%i.txt", d, chipId) << endl;
  ofstream ADD(Form("%s/addlevels_C%i.txt", d, chipId));
  ADD << "\t mean\t  rms\t start\t width\t mean\t\t sigma\t\t const\t\t prob\t chi2/ndof\t ndof" << endl;
  
  for (int k = 0; k < 7; k++) {
    
    if (k == 0) {
      ADD << Form("UB \t%4.0f\t %4.1f\t %4.0f\t %4.0f\t %4.0f +- %4.2f\t %4.1f +- %4.2f\t %4.0f +- %4.2f\t %2.2e\t %4.2f\t %4.0f",
		  alvlMean[k], alvlRMS[k], alvlStart[k], alvlWidth[k], 
		  par[3*k + 1], parE[3*k + 1], par[3*k + 2], 
		  parE[3*k + 2], par[3*k], parE[3*k],
		  prob[k], chi2[k]/ndof[k], ndof[k]) << endl;
    } else {
      ADD <<Form("AL%i \t%4.0f\t %4.1f\t %4.0f\t %4.0f\t  %4.0f +- %4.2f\t %4.1f +- %4.2f\t %4.0f +- %4.2f\t %2.2e\t %4.2f\t %4.0f",
		 k, alvlMean[k], alvlRMS[k], alvlStart[k], alvlWidth[k], 
		 par[3*k + 1], parE[3*k + 1], par[3*k + 2], 
		 parE[3*k + 2], par[3*k], parE[3*k],
		 prob[k], chi2[k]/ndof[k], ndof[k]) << endl;
    }
  }
  
  ADD.close();
  
  printf("Fit parameter\t mean\t rms\t start\t width\t mean\t\t sigma\t\t const\t\t prob\t chi2/ndof\t ndof\n");    
  for (int k = 0; k < 7; k++) {
    
    printf("\t%i.\t %4.0f\t %4.1f\t %4.0f\t %4.0f\t %4.0f+-%4.2f\t %4.1f+-%4.2f\t %4.0f+-%4.2f\t %2.2e\t %4.2f\t %4.0f\n",
	   k, alvlMean[k], alvlRMS[k], alvlStart[k], alvlWidth[k], 
	   par[3*k + 1], parE[3*k + 1], par[3*k + 2], 
	   parE[3*k + 2], par[3*k], parE[3*k],
	   prob[k], chi2[k]/ndof[k], ndof[k]);
    
  }
  
  hpeak->DrawCopy("PESAME");
  
  delete hpeak;


}

//-----------------------------------------------------------------

void fillEmptyAL(const char *directory, int chip) {

  ofstream ADD(Form("%s/addlevels_C%i.txt", directory, chip));

  ADD << "\t mean\t  rms\t start\t width\t mean\t\t sigma\t\t const\t\t prob\t chi2/ndof\t ndof" << endl;
  for (int i = 0; i < 7; i++) {
    
    if (i == 0) {
      ADD << Form("UB \t%4.0f\t %4.1f\t %4.0f\t %4.0f\t %4.0f +- %4.2f\t %4.1f +- %4.2f\t %4.0f +- %4.2f\t %2.2e\t %4.2f\t %4.0f", -9999, -1, -1,-1, -1, -1, -1, -1, -1, -1, -1, -1, -1) << endl;
    } else {
      ADD <<Form("AL%i \t%4.0f\t %4.1f\t %4.0f\t %4.0f\t  %4.0f +- %4.2f\t %4.1f +- %4.2f\t %4.0f +- %4.2f\t %2.2e\t %4.2f\t %4.0f",i, -9999, -1, -1,-1, -1, -1, -1, -1, -1, -1, -1, -1, -1) << endl;
    }
  }
  
  ADD.close();
}


//-----------------------------------------------------------------

TGraph* drawFit(Double_t p0, Double_t p1, Double_t p2) {

   const Int_t n = 50;
   Double_t x[n], y[n];
   for (Int_t i=0;i<n;i++) {
     x[i] = (p1 - 25) + i;
     y[i] = p0*exp(-0.5*pow((x[i]-p1)/p2,2));
   }
   gr = new TGraph(n,x,y);
   gr->SetLineColor(kBlue);
   gr->SetLineWidth(1);

   return gr;

}


//-----------------------------------------------------------------------------------------
double calcMean(TH1 *h) {

  double mean(0.); 

  for (int m = startChip; m < startChip+nChips; m++) {
    
    mean += h->GetBinContent(m+1);
    
  }

  mean = mean/ nChips;

  return mean;
}
//-----------------------------------------------------------------------------------------
double calcRMS(TH1 *h, double mean) {

  double rms(0.);
 
  for (int m = startChip; m < startChip+nChips; m++) {

    rms = rms + (mean - h->GetBinContent(m+1))*(mean - h->GetBinContent(m+1));
  }

  rms = TMath::Sqrt(rms) / nChips ;

  return rms;
}


//-----------------------------------------------------------------------------------------
int readCriteria(const char *fcriteria) {
  
  defectsB = -99;   defectsC = -99; maskdefC = -99;
  currentB = -99;   currentC = -99; slopeivB = -99;
  noiseMin = -99;   noiseMax = 999; tthrTol = -99;
  gainMin  = -99;   gainMax  = -99;   par1Min = -99;  par1Max  = 999;
  noiseB = -99.;     noiseC = -99.;   trimmingB = -99.; trimmingC = -99.;
  gainB = -99.;      gainC = -99.;    pedestalB = -99.; pedestalC = -99.;
  noiseDistr = -99; trmDistr = -99; gainDistr = -99; 
  pedDistr = -99;   par1Distr = -99; 
  
  sprintf(fname, "%s", fcriteria);
  critFile = fopen(fname, "r");   
  
  if ( !critFile ) {
    
    printf("chipSummary> !!!!!!!!!  ----> GRADING: Could not find %s in directory macros\n", fname);
    return 0;
  }
  else {

    printf(Form("Reading grading criteria from %s ...\n\n",fname));      
    
    fclose(critFile);
    ifstream is(fname);
    
    char  buffer[200];    
    char  CritName[200];
    float CritValue(0.);
    int ok(0);

    while (is.getline(buffer, 200, '\n')) {
      
      ok = 1;
      
      if (buffer[0] == '#' )  {continue;}
      
      sscanf(buffer,"%s %f",CritName, &CritValue); 
      
      if (!strcmp(CritName, "maskdefC")) {
	maskdefC = int(CritValue); ok = 1;
	if ( readVerbose ) printf("MASK DEF. C:         %4.0f\n", maskdefC);
      } 

      if (!strcmp(CritName, "noiseMin")) {
	noiseMin = CritValue; ok = 1;
	if ( readVerbose ) printf("MIN PX NOISE :       %4.0f\n", noiseMin);
      }

      if (!strcmp(CritName, "noiseMax")) {
	noiseMax = CritValue; ok = 1;
	if ( readVerbose ) printf("MAX PX NOISE :       %4.0f\n", noiseMax);
      }

      if (!strcmp(CritName, "tthrTol")) {
	tthrTol = CritValue; ok = 1;
	if ( readVerbose ) printf("PX THR TOLERANCE :   %4.0f\n", tthrTol);
      }

      if (!strcmp(CritName, "gainMin")) {
	gainMin = CritValue; ok = 1;
	if ( directory.Contains("T-10") ) { gainMin /= 2.; }
	if ( readVerbose ) printf("MIN PX GAIN :       %4.1f\n", gainMin);
      }

      if (!strcmp(CritName, "gainMax")) {
	gainMax = CritValue; ok = 1;
	if ( directory.Contains("T-10") ) { gainMax /= 0.75; }
	if ( readVerbose ) printf("MAX PX GAIN :       %4.1f\n", gainMax);
      }

      if (!strcmp(CritName, "par1Min")) {
	par1Min = CritValue; ok = 1;
	if ( readVerbose ) printf("MIN PX PAR1 :       %4.1f\n", par1Min);
      }

      if (!strcmp(CritName, "par1Max")) {
	par1Max = CritValue; ok = 1;
	if ( readVerbose ) printf("MAX PX PAR1 :       %4.1f\n", par1Max);
      }

      if (!strcmp(CritName, "noiseB")) {
	noiseB = CritValue; ok = 1;
	if ( readVerbose ) printf("NOISE B:             %4.0f\n", noiseB);
      }

      if (!strcmp(CritName, "noiseC")) {
	noiseC = CritValue; ok = 1;
	if ( readVerbose ) printf("NOISE C:             %4.0f\n", noiseC);
      }

      if (!strcmp(CritName, "trimmingB")) {
	trimmingB = CritValue; ok = 1;
	if ( readVerbose ) printf("TRIMMING B:          %4.0f\n", trimmingB);
      }

      if (!strcmp(CritName, "trimmingC")) {
	trimmingC = CritValue; ok = 1;
	if ( readVerbose ) printf("TRIMMING C:          %4.0f\n", trimmingC);
      }

      if (!strcmp(CritName, "gainB")) {
	gainB = CritValue; ok = 1;
	if ( readVerbose ) printf("GAIN B:              %4.2f\n", gainB);
      }

      if (!strcmp(CritName, "gainC")) {
	gainC = CritValue; ok = 1;
	if ( readVerbose ) printf("GAIN C:              %4.2f\n", gainC);
      }

      if (!strcmp(CritName, "pedestalB")) {
	pedestalB = CritValue; ok = 1;
	if ( readVerbose ) printf("PEDESTAL B:          %4.0f\n", pedestalB);
      }
      
      if (!strcmp(CritName, "pedestalC")) {
	pedestalC = CritValue; ok = 1;
	if ( readVerbose ) printf("PEDESTAL C:          %4.0f\n", pedestalC);
      }
      
      if (!strcmp(CritName, "pedDistribution")) {
	pedDistr = CritValue; ok = 1;
	if ( readVerbose ) printf("PED. DISTR.:         %4.2f\n", pedDistr);
      }

      if (!strcmp(CritName, "par1B")) {
	par1B = CritValue; ok = 1;
	if ( readVerbose ) printf("PAR1 B:          %4.1f\n", par1B);
      }
      
      if (!strcmp(CritName, "par1C")) {
	par1C = CritValue; ok = 1;
	if ( readVerbose ) printf("PAR1 C:          %4.1f\n", par1C);
      }

      if (!strcmp(CritName, "defectsB")) {
	defectsB = int(CritValue); ok = 1;
	if ( readVerbose ) printf("DEFECTS B:           %4.0f\n", defectsB);
      }

      if (!strcmp(CritName, "defectsC")) {
	defectsC = int(CritValue); ok = 1;
	if ( readVerbose ) printf("DEFECTS C:           %4.0f\n", defectsC);
      }
  
      if (!strcmp(CritName, "currentB")) {
	currentB = int(CritValue); ok = 1;
	if ( readVerbose ) printf("CURRENT B:           %4.0f\n", currentB);
      }

      if (!strcmp(CritName, "currentC")) {
	currentC = int(CritValue); ok = 1;
	if ( readVerbose ) printf("CURRENT C:           %4.0f\n", currentC);
      }

      if (!strcmp(CritName, "slopeivB")) {
	slopeivB = int(CritValue); ok = 1;
	if ( readVerbose ) printf("SLOPEIV B:           %4.0f\n", slopeivB);
      }    
    }

    printf("\n");
    readVerbose = 0;

    return 1;
  }
}

