import ROOT

def initialise_ROOT():
    # Suppress "info"-level notices from TCanvas that it has saved a .png
    # see root/core/base/inc/TError.h for information on error levels
    ROOT.gErrorIgnoreLevel = 1001
    ROOT.gROOT.SetStyle('Plain')
    ROOT.gStyle.SetPalette(1)
    ROOT.gROOT.SetBatch(True)
    ROOT.gStyle.SetFillColor(10);
    ROOT.gStyle.SetFrameFillColor(10);
    ROOT.gStyle.SetFrameFillStyle(0);
    ROOT.gStyle.SetFillStyle(0);
    ROOT.gStyle.SetCanvasColor(10);
    ROOT.gStyle.SetPadColor(10);
    ROOT.gStyle.SetTitleFillColor(0);
    ROOT.gStyle.SetStatColor(10);

    # Get rid of drop shadow on legends
    # This doesn't seem to work.  Call SetBorderSize(1) directly on your TLegends
    ROOT.gStyle.SetLegendBorderSize(1);

    # don't put a colored frame around the plots
    ROOT.gStyle.SetFrameBorderMode(0);
    ROOT.gStyle.SetCanvasBorderMode(0);
    ROOT.gStyle.SetPadBorderMode(0);

    # use the primary color palette
    ROOT.gStyle.SetPalette(1)#,int(0));

    # set the default line color for a histogram to be black
    ROOT.gStyle.SetHistLineColor(ROOT.kBlack);

    # set the default line color for a fit function to be red
    ROOT.gStyle.SetFuncColor(ROOT.kRed);

    # make the axis labels black
    ROOT.gStyle.SetLabelColor(ROOT.kBlack,"xyz");

    # set the default title color to be black
    ROOT.gStyle.SetTitleColor(ROOT.kBlack);

    # set the margins
    ROOT.gStyle.SetPadBottomMargin(0.15);
    ROOT.gStyle.SetPadLeftMargin(0.15);
    ROOT.gStyle.SetPadTopMargin(0.075);
    ROOT.gStyle.SetPadRightMargin(0.15);

    # set axis label and title text sizes
    ROOT.gStyle.SetLabelSize(0.03,"xyz");
    ROOT.gStyle.SetLabelOffset(0.01,"xyz");
    ROOT.gStyle.SetTitleSize(0.04,"xyz");
    ROOT.gStyle.SetTitleOffset(0.9,"x");
    ROOT.gStyle.SetTitleOffset(0.2,"yz");
    ROOT.gStyle.SetStatFontSize(0.03);
    ROOT.gStyle.SetTextSize(0.05);
    ROOT.gStyle.SetTitleBorderSize(0);

    # set line widths
    ROOT.gStyle.SetHistLineWidth(2);
    ROOT.gStyle.SetFrameLineWidth(2);
    ROOT.gStyle.SetFuncWidth(2);

    # Misc
    # align the titles to be centered
    ROOT.gStyle.SetTextAlign(22);

    #turn off xy grids
    ROOT.gStyle.SetPadGridX(0);
    ROOT.gStyle.SetPadGridY(0);

    # set the tick mark style
    ROOT.gStyle.SetPadTickX(1);
    ROOT.gStyle.SetPadTickY(1);

    # don't show the fit parameters in a box
    ROOT.gStyle.SetOptFit(0000);

    # set the default stats shown
    ROOT.gStyle.SetOptStat("eMR");

    # marker settings
    ROOT.gStyle.SetMarkerStyle(8);
    ROOT.gStyle.SetMarkerSize(0.7);

    # Fonts
#     ROOT.gStyle.SetStatFont(12);
#     ROOT.gStyle.SetLabelFont(12,"xyz");
#     ROOT.gStyle.SetTitleFont(12,"xyz");
#     ROOT.gStyle.SetTextFont(12);

    # done
    ROOT.gStyle.cd();

