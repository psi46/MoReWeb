#include <iostream>
#include <cstdio>
#include <vector>
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
	{"targets",	required_argument, 	NULL, 't'},
	{"help",	no_argument,		NULL, 'h'},
	{"verbose",	no_argument,		NULL, 'v'},
	{NULL,		no_argument,		NULL, 0 }
};

void print_usage(const char * progname)
{
	cerr << "Usage: " << progname << " [--help|-h] [--verbose|-v] [--output=<file>|-o <file>] --targets=<list> <vcal-vs-thr-file> <s-curve-file> ... <s-curve-file>" << endl;
}

int error(int code, const char * message)
{
	cerr << "Error: " << message << endl;
	return code;
}

vector<float> parse_targets(const char * targets)
{
	vector<float> target_energy;

	if (!targets)
		return target_energy;

	int ret = 1;
	const char * ptr = targets;
	while (ret == 1 && ptr) {
		float energy;
		ret = sscanf(ptr, "%f", &energy);
		if (ret != 1)
			break;
		target_energy.push_back(energy);
		ptr = strchr(ptr, ':');
		if (ptr)
			ptr += 1;
	}

	return target_energy;
}

int main(int argc, char ** argv) {
	char * output_filename = (char *) "output.root";
	char * targets = 0;
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
			case 't':
				targets = optarg;
				break;
			case 'h':
				print_usage(argv[0]);
				break;
			default:
				print_usage(argv[0]);
				return 1;
		}
	}

	/* Check targets argument */
	if (!targets)
		return error(1, "No targets specified.");

	/* Parse targets */
	vector<float> target_energy = parse_targets(targets);
	if (target_energy.size() < 1)
		return error(1, "Invalid target specifications.");

	if (verbose) {
		for (int i = 0; i < target_energy.size(); i++)
			cout << "Target " << i + 1 << " energy: " << target_energy[i] << endl;
	}

	/* Check number of arguments and extract input file names */
	if (argc - optind != 1 + target_energy.size())
		return error(1, "Not enough input ROOT files given.");
	const char * vcal_vs_thr_filename = argv[optind];
	char ** scurve_filename = new char * [target_energy.size()];
	for (int i = 0; i < target_energy.size(); i++) {
		scurve_filename[i] = argv[optind + i + 1];
	}

	/* Open the vcal vs threshold input file */
	TFile * vcal_vs_thr_file = new TFile(vcal_vs_thr_filename);
	if (!vcal_vs_thr_file || vcal_vs_thr_file->IsZombie())
		return error(1, Form("Unable to open file %s.", vcal_vs_thr_filename));

	/* Open the scurve input files */
	TFile ** scurve_file = new TFile * [target_energy.size()];
	for (int i = 0; i < target_energy.size(); i++) {
		scurve_file[i] = new TFile(scurve_filename[i]);
		if (!scurve_file[i] || scurve_file[i]->IsZombie())
			return error(1, Form("Unable to open file %s.", scurve_filename));
	}

	/* Open the output file */
	TFile * output = new TFile(output_filename, "RECREATE");

	/* Get the histogram from the vcal vs threshold ROOT file */
	TGraphErrors * vcal_vs_thr = (TGraphErrors *) vcal_vs_thr_file->Get("vcal_vs_thr");
	if (!vcal_vs_thr)
		return error(1, Form("Could not find histogram %s in ROOT file %s.", "vcal_vs_thr", vcal_vs_thr_filename));
	//vcal_vs_thr->SetDirectory(output);

	/* Get the histograms from the scurve ROOT files */
	TH1F ** scurve = new TH1F * [target_energy.size()];
	for (int i = 0; i < target_energy.size(); i++) {
		scurve[i] = (TH1F *) scurve_file[i]->Get("xraythrscan");
		if (!scurve[i])
			return error(1, Form("Could not find histogram %s in ROOT file %s.", "xraythrscan", scurve_filename));
		scurve[i]->SetDirectory(output);
	}

	/* Create a new histogram that contains only the relevant data */
	TGraphErrors * electrons_vs_vcal = new TGraphErrors();
	electrons_vs_vcal->SetNameTitle("electrons_vs_vcal", "VCal Calibration");

	/* Populate the histogram */
	int p = 0;
	float a = vcal_vs_thr->GetFunction("f1")->GetParameter(2);
	float b = vcal_vs_thr->GetFunction("f1")->GetParameter(1);
	float c = vcal_vs_thr->GetFunction("f1")->GetParameter(0);
	float da = vcal_vs_thr->GetFunction("f1")->GetParError(2);
	float db = vcal_vs_thr->GetFunction("f1")->GetParError(1);
	float dc = vcal_vs_thr->GetFunction("f1")->GetParError(0);
	for (int i = 0; i < target_energy.size(); i++) {
		float energy = target_energy[i];
		energy = (energy < 100) ? energy * 1000 : energy;
		float threshold = scurve[i]->GetFunction("scurve")->GetParameter(3);
		float threshold_error = scurve[i]->GetFunction("scurve")->GetParError(3);
		float vcal = a * TMath::Power(threshold, 2) + b * threshold + c;
		if (verbose) {
			cout << "Energy: " << energy << "eV,\t";
			cout << "carge: " << energy / 3.62 << " e-,\t";
			cout << "threshold: " << threshold << ",\t";
			cout << "Vcal: " << vcal << endl;
		}
		electrons_vs_vcal->SetPoint(p, vcal, energy / 3.62);
		float err = 0;
		err += TMath::Power(TMath::Power(threshold, 2) * da, 2);
		err += TMath::Power(threshold * db, 2);
		err += TMath::Power(dc, 2);
		err += TMath::Power((2 * a * threshold + b) * threshold_error, 2);
		err = TMath::Sqrt(err);
		/* FIXME: Set Errors */
		//electrons_vs_vcal->SetPointError(p, err, 1);
		p++;
	}

	if (p == 0)
		return error(1, "All data unusable.");

	TCanvas * canvas = new TCanvas("bla");
	electrons_vs_vcal->SetMarkerStyle(0);
	electrons_vs_vcal->GetXaxis()->SetTitle("Vcal [low range DAC units]");
	electrons_vs_vcal->GetYaxis()->SetTitle("Equivalent charge [electrons]");
	int fit_result = electrons_vs_vcal->Fit("pol1", verbose ? "" : "Q");
	//fit_result = electrons_vs_vcal->Fit("pol1", verbose ? "" : "Q");

	electrons_vs_vcal->Write();
	output->Close();

	if (fit_result != 0)
		error(1, "Data fit failed.");

	return 0;
}
