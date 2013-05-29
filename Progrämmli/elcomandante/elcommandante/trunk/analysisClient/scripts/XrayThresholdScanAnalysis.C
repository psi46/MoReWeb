#include <iostream>
#include <cstdio>
#include <getopt.h>

#include <TMath.h>
#include <TFile.h>
#include <TCanvas.h>
#include <TF1.h>
#include <TH1F.h>

using namespace std;

static const char * optString = "o:hv";

static const struct option longOpts[] = {
	{"output",	required_argument, 	NULL, 'o'},
	{"steps",	required_argument, 	NULL, 's'},
	{"help",	no_argument,		NULL, 'h'},
	{"verbose",	no_argument,		NULL, 'v'},
	{NULL,		no_argument,		NULL, 0 }
};

void print_usage(const char * progname)
{
	cerr << "Usage: " << progname << "[--help|-h] [--verbose|-v] [--output=<file>|-o <file>] [--steps=N|-s N] <input-file>" << endl;
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
			case 's':
				ret = sscanf(optarg, "%i", &steps);
				if (ret != 1 || steps < 1 || steps > 2) {
					print_usage(argv[0]);
					return 1;
				}
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
	const char * input_filename = argv[optind];

	/* Open the input file */
	TFile * file = new TFile(input_filename);
	if (!file || file->IsZombie())
		return error(1, Form("Unable to open file %s.", input_filename));

	/* Get the relevant histogram from the ROOT file */
	TH1F * XrayCal_C0 = (TH1F *) file->Get("XrayCal_C0");
	if (!XrayCal_C0)
		return error(1, Form("Could not find histogram %s in ROOT file %s.", "XrayCal_C0", input_filename));

	/* Determine the limits of the data in x */
	int a, b;
	double x, y;
	for (a = 0; a < 255; a++) {
		if (XrayCal_C0->GetBinContent(a + 1) > 0)
			break;
	}
	for (b = 255; b >= 0; b--) {
		if (XrayCal_C0->GetBinContent(b + 1) > 0)
			break;
	}

	/* Open the output file */
	TFile * output = new TFile(output_filename, "RECREATE");

	/* Create a new histogram that contains only the relevant data */
	TH1F * xcurve = new TH1F("xraythrscan", "X-ray threshold scan", (b - a + 1), a, b + 1);
	for (int i = a; i <= b; i++) {
		xcurve->SetBinContent(i - a + 1, XrayCal_C0->GetBinContent(i + 1));
	}

	/* Create the function used for fitting the data */
	char function_str [1024] = "(";
	strcat(function_str, "[2] * 0.5 * (TMath::Erf((x - [3]) / [4]) + 1)");
	if (steps == 2)
		strcat(function_str, " + (1 - [2]) * 0.5 * (TMath::Erf((x - [5]) / [6]) + 1)");
	strcat(function_str, ") * ([1] * (x - [3] - 2 * [4]) + [0])");
	TF1 * f = new TF1("scurve", function_str);

	/* Determine initial conditions for the fit */
	float ka_pos, ka_width, kb_pos, kb_width, ratio, slope, height;

	height = xcurve->GetBinContent(xcurve->GetXaxis()->GetNbins());
	slope = 0;
	ratio = steps == 2 ? 0.8 : 1.0;
	for (int i = a; i <= b; i++) {
		if (xcurve->GetBinContent(i - a + 1) > height / 2) {
			ka_pos = i;
			break;
		}
	}
	ka_width = 2;
	kb_pos = ka_pos - 0.1 * (b - a);
	kb_width = 2;

	if (steps == 1) {
		f->SetParName(3, "k_{#alpha,#beta} threshold");
		f->SetParameter(3, ka_pos);
		f->SetParName(4, "k_{#alpha,#beta} width");
		f->SetParameter(4, ka_width);
	} else if (steps == 2) {
		f->SetParName(3, "k_{#alpha} threshold");
		f->SetParameter(3, ka_pos);
		f->SetParName(4, "k_{#alpha} width");
		f->SetParameter(4, ka_width);

		f->SetParName(5, "k_{#beta} threshold");
		f->SetParameter(5, kb_pos);
		f->SetParName(6, "k_{#beta} width");
		f->SetParameter(6, kb_width);
	}

	if (steps == 1)
		f->FixParameter(2, 1.0);
	else
		f->SetParameter(2, ratio);

	f->SetParName(1, "Slope");
	f->SetParameter(1, slope);
	f->SetParName(0, "Intensity");
	f->SetParameter(0, height);

	TCanvas * c = new TCanvas("bla");
	xcurve->SetMarkerStyle(0);
	xcurve->GetXaxis()->SetTitle("Threshold [VcThr DAC units]");
	xcurve->GetYaxis()->SetTitle("Pixel hit count [1]");
	xcurve->Sumw2();
	xcurve->Fit("scurve", verbose ? "" : "Q", "", a, b + 1);

	cout << "Threshold: " << f->GetParameter(3) << " +/- " << f->GetParError(4) << endl;

	xcurve->Write();
	output->Close();

	return 0;
}
