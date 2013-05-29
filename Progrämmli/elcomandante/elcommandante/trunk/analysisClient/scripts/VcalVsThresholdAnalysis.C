#include <iostream>
#include <cstdio>
#include <getopt.h>

#include <TMath.h>
#include <TFile.h>
#include <TCanvas.h>
#include <TF1.h>
#include <TH1D.h>
#include <TGraphErrors.h>

using namespace std;

static const char * optString = "o:hv";

static const struct option longOpts[] = {
	{"output",	required_argument, 	NULL, 'o'},
	{"help",	no_argument,		NULL, 'h'},
	{"verbose",	no_argument,		NULL, 'v'},
	{NULL,		no_argument,		NULL, 0 }
};

void print_usage(const char * progname)
{
	cerr << "Usage: " << progname << "[--help|-h] [--verbose|-v] [--output=<file>|-o <file>] <input-directory>" << endl;
}

int error(int code, const char * message)
{
	cerr << "Error: " << message << endl;
	return code;
}

int main(int argc, char ** argv) {
	char * output_filename = (char *) "output.root";
	int verbose = 0;
	int steps = 1;

	int opt, longIndex;
	while ((opt = getopt_long( argc, argv, optString, longOpts, &longIndex )) != -1) {
		int ret;
		switch (opt) {
			case 'o':
				output_filename = optarg;
				break;
			case 'v':
				verbose = 1;
				break;
			case 'h':
				print_usage(argv[0]);
				break;
			default:
				print_usage(argv[0]);
				return 1;
		}
	}

	/* Check number of arguments and extract input file name */
	if (argc - optind != 1)
		return error(1, "No input ROOT file given.");
	const char * input_directory = argv[optind];
	char input_root_filename [1024];
	sprintf(input_root_filename, "%s/commander_VcalVsThreshold.root", input_directory);
	char input_log_filename [1024];
	sprintf(input_log_filename, "%s/commander_VcalVsThreshold.log", input_directory);

	/* Open the log file */
	/* TODO */

	/* Open the input file */
	TFile * file = new TFile(input_root_filename);
	if (!file || file->IsZombie())
		return error(1, Form("Unable to open file %s.", input_root_filename));

	/* Open the output file */
	TFile * output = new TFile(output_filename, "RECREATE");

	/* Get the relevant histograms from the ROOT file */
	TH1D * VcalThresholdDist [20] = {0};
	int N = 0;
	for (int i = 0; i < 20; i++) {
		VcalThresholdDist[i] = (TH1D *) file->Get(Form("VcalThresholdMap_C0Distribution;%i", i + 1));
		if (!VcalThresholdDist[i]) {
			N = i;
			break;
		}
		VcalThresholdDist[i]->SetDirectory(output);
	}
	if (N == 0)
		return error(1, Form("Could not find any histograms %s in ROOT file %s.", "VcalThresholdMap_C0Distribution", input_root_filename));

	/* Get the thresholds with which the distributions were measured */
	/* FIXME */
	int thresholds [] = {0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 90};

	/* Create a new histogram that contains only the relevant data */
	TGraphErrors * vcal_vs_thr = new TGraphErrors();
	vcal_vs_thr->SetNameTitle("vcal_vs_thr", "VCal vs threshold scan");

	/* Populate the histogram */
	int p = 0;
	for (int i = 0; i < N; i++) {
		int bin = VcalThresholdDist[i]->GetXaxis()->FindBin(255);
		/* Check for overflow (don't allow the bin 255 to be filled) */
		if (bin > 0 && bin <= VcalThresholdDist[i]->GetXaxis()->GetNbins() && VcalThresholdDist[i]->GetBinContent(bin) > 0) {
			continue;
		}
		vcal_vs_thr->SetPoint(p, thresholds[i], VcalThresholdDist[i]->GetMean());
		vcal_vs_thr->SetPointError(p, 1.0, VcalThresholdDist[i]->GetMeanError());
		p++;
	}

	if (p == 0)
		return error(1, "Insufficient data for analysis.");

	TCanvas * c = new TCanvas("bla");
	vcal_vs_thr->SetMarkerStyle(0);
	vcal_vs_thr->GetXaxis()->SetTitle("Threshold [VcThr DAC units]");
	vcal_vs_thr->GetYaxis()->SetTitle("Vcal [low range DAC units]");
	TF1 * f1 = new TF1("f1", "pol2");
	/* Magic initial parameters */
	f1->SetParameter(0, 300);
	f1->SetParameter(1, -4);
	f1->SetParameter(2, 0.01);
	int fit_result = vcal_vs_thr->Fit("f1", verbose ? "" : "Q");

	vcal_vs_thr->Write();
	output->Close();

	if (fit_result != 0)
		error(1, "Data fit failed.");

	return 0;
}
