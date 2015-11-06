from sys import argv
import time
from time import gmtime, strftime
import os
import ConfigParser
import subprocess
import shlex
import glob

class MakeProductionSummary:

  def MakeTexFile(self, args):

    Configuration = ConfigParser.ConfigParser()
    Configuration.read([
    'Configuration/Paths.cfg',
    ])
    try:
      OutputDirectoryPath = Configuration.get('Paths', 'GlobalPresentationPath')
    except:
      OutputDirectoryPath = Configuration.get('Paths', 'GlobalOverviewPath')

    if not os.path.exists(OutputDirectoryPath):
      try:
        os.makedirs(OutputDirectoryPath)
      except:
        print "could not create presentation output directory!"

    FiguresPath = Configuration.get('Paths', 'GlobalOverviewPath')



    datenow = time.strftime("%d %m %Y")
    d = time.strptime(datenow, "%d %m %Y")
    week = strftime("%U", d)

    filename = OutputDirectoryPath + "/ModuleProductionOverview_Week{0}.tex".format(week)
    

    nA = args['nA']
    nB = args['nB']
    nC = args['nC']
    nM = args['nM']
    nBrokenROCs = args['BrokenROC']
    nBrokenROCsX = args['BrokenROCX']
    nAtoB = args['nAtoB']
    nAtoC = args['nAtoC']
    nBtoA = args['nBtoA']
    nBtoC = args['nBtoC']
    nCtoA = args['nCtoA']
    nCtoB = args['nCtoB']
    nAtoBX = args['nAtoBX']
    nAtoCX = args['nAtoCX']
    nBtoAX = args['nBtoAX']
    nBtoCX = args['nBtoCX']
    nCtoAX = args['nCtoAX']
    nCtoBX = args['nCtoBX']
    nHDI = args['nHDI']
    lcstartupB = args['nlcstartupB']
    lcstartupC = args['nlcstartupC']
    IV150B = args['nIV150B']
    IV150C = args['nIV150C']
    IV150m20B = args['nIV150m20B']
    IV150m20C = args['nIV150m20C']
    IRatio150B = args['nCurrentRatioB']
    IRatio150C = args['nCurrentRatioC']
    IVSlopeB = args['nIVSlopeB']
    IVSlopeC = args['nIVSlopeC']
    totDefectsB = args['ntotDefectsB']
    totDefectsC = args['ntotDefectsC']
    totDefectsXrayB = args['ntotDefectsXrayB']
    totDefectsXrayC = args['ntotDefectsXrayC']
    BBFullB = args['nBBFullB']
    BBFullC = args['nBBFullC']
    BBXrayB = args['nBBXrayB']
    BBXrayC = args['nBBXrayC']
    AddressdefB = args['nAddressdefB']
    AddressdefC = args['nAddressdefC']
    TrimbitdefB = args['nTrimbitdefB']
    TrimbitdefC = args['nTrimbitdefC']
    MaskdefB = args['nMaskdefB']
    MaskdefC = args['nMaskdefC']
    deadpixB = args['ndeadpixB']
    deadpixC = args['ndeadpixC']
    uniformityB = args['nuniformityB']
    uniformityC = args['nuniformityC']
    NoiseB = args['nNoiseB']
    NoiseC = args['nNoiseC']
    NoiseXrayB = args['nNoiseXrayB']
    NoiseXrayC = args['nNoiseXrayC']
    PedSpreadB = args['nPedSpreadB']
    PedSpreadC = args['nPedSpreadC']
    RelGainWB = args['nRelGainWB']
    RelGainWC = args['nRelGainWC']
    VcalThrWB = args['nVcalThrWB']
    VcalThrWC = args['nVcalThrWC']
    LowHREfB = args['nLowHREfB']
    LowHREfC = args['nLowHREfC']

 

    nAB = int(nA) + int(nB)
    nT = nAB + int(nC) + int(nM)
    nQ = nAB + int(nC)
    Pass = round(float(nAB)/nQ*100,1)

    lcstartup = round(float(lcstartupC)/nQ*100,1)
    IV150 = round(float(IV150C)/nQ*100,1)
    IV150m20 = round(float(IV150m20C)/nQ*100,1)
    IVSlope = round(float(IVSlopeC)/nQ*100,1)
    totDefects = round(float(totDefectsC)/nQ*100,1)
    totDefectsXray = round(float(totDefectsXrayC)/nQ*100,1)
    BBFull = round(float(BBFullC)/nQ*100,1)
    BBXray = round(float(BBXrayC)/nQ*100,1)
    Addressdef = round(float(AddressdefC)/nQ*100,1)
    Trimbitdef = round(float(TrimbitdefC)/nQ*100,1)
    Maskdef = round(float(MaskdefC)/nQ*100,1)
    deadpix = round(float(deadpixC)/nQ*100,1)
    uniformity = round(float(uniformityC)/nQ*100,1)
    Noise = round(float(NoiseC)/nQ*100,1)
    NoiseXray = round(float(NoiseXrayC)/nQ*100,1)
    PedSpread = round(float(PedSpreadC)/nQ*100,1)
    RelGainW = round(float(RelGainWC)/nQ*100,1)
    VcalThrW = round(float(VcalThrWC)/nQ*100,1)
    LowHREf = round(float(LowHREfC)/nQ*100,1)
    IRatio150 = round(float(IRatio150C)/nQ*100,1)
    BrokenROC = round(float(nBrokenROCs)/nQ*100,1)
    BrokenROCX = round(float(nBrokenROCsX)/nQ*100,1)
    HDI = round(float(nHDI)/nQ*100,1)
    
 

    template = """
    \documentclass[xcolor=dvipsnames]{{beamer}}
    \usepackage{{booktabs}}
    \usepackage{{multirow}}
    \usepackage{{siunitx}}
    \setbeamertemplate{{footline}}[frame number]
    \setbeamercolor{{frametitle}}{{fg=Black,bg=White}}
    \setbeamercolor{{title}}{{fg=Black,bg=White}}
    \usepackage{{lipsum}}
    \setbeamertemplate{{itemize item}}[circle]
    \setbeamertemplate{{caption}}{{\\raggedright\insertcaption\par}}
    \setbeamertemplate{{navigation symbols}}{{}}
    \\newenvironment{{changemargin}}[2]{{
    \\begin{{list}}{{}}{{
    \setlength{{\\topsep}}{{0pt}}
    \setlength{{\leftmargin}}{{#1}}
    \setlength{{\\rightmargin}}{{#2}}
    \setlength{{\listparindent}}{{\parindent}}
    \setlength{{\itemindent}}{{\parindent}}
    \setlength{{\parsep}}{{\parskip}}
    }}
    \item[]}}
    {{\end{{list}}}} 

    \setbeamertemplate{{footline}}
{{
  \leavevmode%
  \hbox{{%
  \\begin{{beamercolorbox}}[wd=.333333\paperwidth,ht=2.25ex,dp=1ex,center]{{author in head/foot}}%
  \end{{beamercolorbox}}%
  \\begin{{beamercolorbox}}[wd=.333333\paperwidth,ht=2.25ex,dp=1ex,center]{{title in head/foot}}%
  \end{{beamercolorbox}}%
  \\begin{{beamercolorbox}}[wd=.333333\paperwidth,ht=2.25ex,dp=1ex,right]{{date in head/foot}}%
    \insertframenumber\hspace*{{2ex}} 
  \end{{beamercolorbox}}}}%
  \\vskip0pt%
}}

    \\begin{{document}}

    \\title{{\\textbf{{Status of module qualification}}}}   
    
    \date{{\\today}} 

    \\frame{{
    \maketitle
    }}

    \\frame{{
    \\frametitle{{Production overview}}
    \\begin{{figure}} [h!] \centering \\advance\leftskip-0.9cm
    \\vspace{{-6mm}}
    \includegraphics[width=0.58\\textwidth, angle=0] {{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/WeeklyProduction/WeeklyProduction.pdf}}
    \includegraphics[width=0.58\\textwidth, angle=0] {{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/CumulativeProductionGraph/CumulativeProductionGraph.pdf}}
    \end{{figure}}
    }}

    \\frame{{
    \\frametitle{{Production overview}}
    \\begin{{table}}[h]
    \centering
    \\begin{{tabular}}{{@{{}}ccccc@{{}}}}
    \\toprule
    A & B & A+B & C & Not complete \\\ \midrule
    {nA} & {nB} & {nAB} & {nC} & {nM} \\\  \\bottomrule
    \end{{tabular}}
    \end{{table}}
    \\vspace{{1cm}}
    $\Rightarrow$ {Pass} \% yield \\\\
    $\Rightarrow$ {nQ} modules out of {nT} are completely tested.
    }}

    \\frame{{
    \\frametitle{{Defects I}}
    \\begin{{table}}[]
    \centering
    \\begin{{tabular}}{{@{{}}llccc@{{}}}}
    \\toprule
                                    & Defects             & B & C &  C (\%  of production)\\\\ \midrule
    \multirow{{5}}{{*}}{{Sensor}}   & $I_{{biais}}$ startup          & {lcstartupB} & {lcstartupC} &  {lcstartup}\\\\
                                    & IV 150 (+17)        & {IV150B} & {IV150C} & {IV150} \\\\
                                    & IV 150 (-20)        & {IV150m20B} & {IV150m20C} & {IV150m20} \\\\ 
                                    & I(+17)/I(-20)       & {IRatio150B} & {IRatio150C} & {IRatio150} \\\\ 
                                     & IV slope           & {IVSlopeB} & {IVSlopeC} & {IVSlope} \\\\ \midrule
    \multirow{{6}}{{*}}{{Chip performance}} & Noise       & {NoiseB} & {NoiseC} & {Noise} \\\\
                                    & Noise X-ray         & {NoiseXrayB} & {NoiseXrayC} & {NoiseXray} \\\\
                                    & Pedestal spread     & {PedSpreadB} & {PedSpreadC} & {PedSpread} \\\\
                                    & Rel. Gain Width     & {RelGainWB} & {RelGainWC} & {RelGainW} \\\\
                                    & VcalThr Width       & {VcalThrWB} & {VcalThrWC} & {VcalThrW} \\\\
                                    & Low HR Efficiency   & {LowHREfB} & {LowHREfC} & {LowHREf} \\\\ \\bottomrule 
    \end{{tabular}}
    \end{{table}}
    }}

    \\frame{{
    \\frametitle{{Defects II}}
    \\begin{{table}}[]
    \centering
    \\begin{{tabular}}{{@{{}}llccc@{{}}}}
    \\toprule
                                    & Defects             & B & C &  C (\%  of production)\\\\ \midrule
    \multirow{{12}}{{*}}{{Pixel defects}} & Total defects  & {totDefectsB} & {totDefectsC} & {totDefects} \\\\ 
                                    & Total defects X-ray & {totDefectsXrayB} & {totDefectsXrayC} & {totDefectsXray} \\\\
                                    & BB Fulltest         & {BBFullB} & {BBFullC} & {BBFull} \\\\
                                    & BB X-ray            & {BBXrayB} & {BBXrayC} & {BBXray} \\\\
                                    & Address defects     & {AddressdefB} & {AddressdefC} & {Addressdef} \\\\
                                    & Trimbit defects     & {TrimbitdefB} & {TrimbitdefC} & {Trimbitdef} \\\\
                                    & Mask defects        & {MaskdefB} & {MaskdefC} & {Maskdef} \\\\
                                    & Dead pixels         & {deadpixB} & {deadpixC} & {deadpix} \\\\
                                    & Broken ROC          & 0 & {nBrokenROCs} & {BrokenROC} \\\\
                                    & Broken ROC X-ray    & 0 & {nBrokenROCsX} & {BrokenROCX} \\\\
                                    & HDI Problem    & 0 & {nHDI} & {HDI} \\\\
                                    & Uniformity problem  & {uniformityB} & {uniformityC} & {uniformity} \\\\ \\bottomrule 
    \end{{tabular}}
    \end{{table}}
    }}


    \\frame{{
    \\frametitle{{Defects overview}}
    \\vspace{{-1cm}}
    {ModuleFailureOverviewFigures}
    }}

    \\frame{{
    \\frametitle{{Manual regradings}}
    \\begin{{table}}[]
    \\begin{{minipage}}[b]{{0.45\linewidth}}
    \centering
    \\begin{{tabular}}{{@{{}}llll@{{}}}}
    \\toprule
    initial/final  & A & B & C \\\\ \midrule
    A & / & {nAtoB}  &  {nAtoC} \\\\
    B &  {nBtoA} & / &  {nBtoC} \\\\
    C &  {nCtoA} & {nCtoB}  & / \\\\ \\bottomrule
    \end{{tabular}} \caption{{Full qualification}}
\end{{minipage}}
\hspace{{0.5cm}}
\\begin{{minipage}}[b]{{0.45\linewidth}}
\centering
\\begin{{tabular}}{{@{{}}llll@{{}}}}
    \\toprule
    initial/final  & A & B & C \\\\ \midrule
    A & / & {nAtoBX}  &  {nAtoCX} \\\\
    B &  {nBtoAX} & / &  {nBtoCX} \\\\
    C &  {nCtoAX} & {nCtoBX}  & / \\\\ \\bottomrule
    \end{{tabular}} \caption{{X-ray qualification}}
    \end{{minipage}}
    \end{{table}}
    }}


    \\frame{{
    \\frametitle{{Fulltest duration}}
    \\vspace{{-1cm}}
    \\begin{{figure}} \centering \\advance\leftskip-0.9cm
    \includegraphics[width=1.14\\textwidth, angle=0] {{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/AbstractClasses_GeneralProductionOverview/Duration.pdf}}
    \end{{figure}}
    }}

    \\frame{{
    \\begin{{center}}
    \\textbf{{Results from electrical tests}}
    \\end{{center}}
    }}

    \\frame{{
    \\frametitle{{Overlay of Bump Bonding defects}}
    \\vspace{{-1cm}}
    \\begin{{figure}} \centering \\advance\leftskip-0.9cm
    \includegraphics[width=1.14\\textwidth, angle=0] {{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/BumpBondingOverlay_All/BumpBondingOverlay.pdf}}
    \end{{figure}}
    }}


    \\frame{{
    \\frametitle{{Overlay of Dead Pixels}}
    \\vspace{{-1cm}}
    \\begin{{figure}} \centering \\advance\leftskip-0.9cm
    \includegraphics[width=1.14\\textwidth, angle=0] {{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/DeadPixelOverlay_m20_2/DeadPixelOverlay.pdf}}
    \end{{figure}}
    }}

    \\frame{{
    \\frametitle{{Mean Noise per ROC}}
    \\vspace{{-1cm}}
    \\begin{{figure}}\centering
\minipage{{0.32\\textwidth}}
  \includegraphics[width=\linewidth]{{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/MeanNoise_m20_1/MeanNoiseROC.pdf}}
  \caption{{T=-20$^{{\circ}}$C BTC}}
\endminipage\hfill
\minipage{{0.32\\textwidth}}
  \includegraphics[width=\linewidth]{{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/MeanNoise_m20_2/MeanNoiseROC.pdf}}
  \caption{{T=-20$^{{\circ}}$C ATC}}
\endminipage\hfill
\minipage{{0.32\\textwidth}}%
  \includegraphics[width=\linewidth]{{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/MeanNoise_p17_1/MeanNoiseROC.pdf}}
  \caption{{T=+17$^{{\circ}}$C}}
\endminipage
\end{{figure}}
    }}

     \\frame{{
    \\frametitle{{Relative Gain Width}}
    \\vspace{{-1cm}}
    \\begin{{figure}}\centering
\minipage{{0.32\\textwidth}}
  \includegraphics[width=\linewidth]{{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/RelativeGainWidth_m20_1/RelativeGainWidth.pdf}}
  \caption{{T=-20$^{{\circ}}$C BTC}}
\endminipage\hfill
\minipage{{0.32\\textwidth}}
  \includegraphics[width=\linewidth]{{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/RelativeGainWidth_m20_2/RelativeGainWidth.pdf}}
  \caption{{T=-20$^{{\circ}}$C ATC}}
\endminipage\hfill
\minipage{{0.32\\textwidth}}%
  \includegraphics[width=\linewidth]{{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/RelativeGainWidth_p17_1/RelativeGainWidth.pdf}}
  \caption{{T=+17$^{{\circ}}$C}}
\endminipage
\end{{figure}}
    }}

     \\frame{{
    \\frametitle{{Pedestal Spread}}
    \\vspace{{-1cm}}
    \\begin{{figure}}\centering
\minipage{{0.32\\textwidth}}
  \includegraphics[width=\linewidth]{{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/PedestalSpread_m20_1/PedestalSpread.pdf}}
  \caption{{T=-20$^{{\circ}}$C BTC}}
\endminipage\hfill
\minipage{{0.32\\textwidth}}
  \includegraphics[width=\linewidth]{{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/PedestalSpread_m20_2/PedestalSpread.pdf}}
  \caption{{T=-20$^{{\circ}}$C ATC}}
\endminipage\hfill
\minipage{{0.32\\textwidth}}%
  \includegraphics[width=\linewidth]{{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/PedestalSpread_p17_1/PedestalSpread.pdf}}
  \caption{{T=+17$^{{\circ}}$C}}
\endminipage
\end{{figure}}
    }}

     \\frame{{
    \\frametitle{{Vcal Threshold Width}}
    \\vspace{{-1cm}}
    \\begin{{figure}}\centering
\minipage{{0.32\\textwidth}}
  \includegraphics[width=\linewidth]{{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/VcalThresholdWidth_m20_1/VcalThresholdWidth.pdf}}
  \caption{{T=-20$^{{\circ}}$C BTC}}
\endminipage\hfill
\minipage{{0.32\\textwidth}}
  \includegraphics[width=\linewidth]{{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/VcalThresholdWidth_m20_2/VcalThresholdWidth.pdf}}
  \caption{{T=-20$^{{\circ}}$C ATC}}
\endminipage\hfill
\minipage{{0.32\\textwidth}}%
  \includegraphics[width=\linewidth]{{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/VcalThresholdWidth_p17_1/VcalThresholdWidth.pdf}}
  \caption{{T=+17$^{{\circ}}$C}}
\endminipage
\end{{figure}}
    }}

     \\frame{{
    \\frametitle{{Gain per Pixel}}
    \\vspace{{-1cm}}
    \\begin{{figure}}\centering
\minipage{{0.32\\textwidth}}
  \includegraphics[width=\linewidth]{{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/GainPerPixel__m20_1/GainPerPixel.pdf}}
  \caption{{T=-20$^{{\circ}}$C BTC}}
\endminipage\hfill
\minipage{{0.32\\textwidth}}
  \includegraphics[width=\linewidth]{{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/GainPerPixel__m20_2/GainPerPixel.pdf}}
  \caption{{T=-20$^{{\circ}}$C ATC}}
\endminipage\hfill
\minipage{{0.32\\textwidth}}%
  \includegraphics[width=\linewidth]{{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/GainPerPixel__p17_1/GainPerPixel.pdf}}
  \caption{{T=+17$^{{\circ}}$C}}
\endminipage
\end{{figure}}
    }}

       \\frame{{
    \\frametitle{{Pedestal per Pixel}}
    \\vspace{{-1cm}}
    \\begin{{figure}}\centering
\minipage{{0.32\\textwidth}}
  \includegraphics[width=\linewidth]{{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/PedestalPerPixel__m20_1/PedestalPerPixel.pdf}}
  \caption{{T=-20$^{{\circ}}$C BTC}}
\endminipage\hfill
\minipage{{0.32\\textwidth}}
  \includegraphics[width=\linewidth]{{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/PedestalPerPixel__m20_2/PedestalPerPixel.pdf}}
  \caption{{T=-20$^{{\circ}}$C ATC}}
\endminipage\hfill
\minipage{{0.32\\textwidth}}%
  \includegraphics[width=\linewidth]{{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/PedestalPerPixel__p17_1/PedestalPerPixel.pdf}}
  \caption{{T=+17$^{{\circ}}$C}}
\endminipage
\end{{figure}}
    }}

        \\frame{{
    \\frametitle{{Noise per Pixel}}
    \\vspace{{-1cm}}
    \\begin{{figure}}\centering
\minipage{{0.32\\textwidth}}
  \includegraphics[width=\linewidth]{{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/SCurveWidthsPerPixel__m20_1/SCurveWidthsPerPixel.pdf}}
  \caption{{T=-20$^{{\circ}}$C BTC}}
\endminipage\hfill
\minipage{{0.32\\textwidth}}
  \includegraphics[width=\linewidth]{{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/SCurveWidthsPerPixel__m20_2/SCurveWidthsPerPixel.pdf}}
  \caption{{T=-20$^{{\circ}}$C ATC}}
\endminipage\hfill
\minipage{{0.32\\textwidth}}%
  \includegraphics[width=\linewidth]{{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/SCurveWidthsPerPixel__p17_1/SCurveWidthsPerPixel.pdf}}
  \caption{{T=+17$^{{\circ}}$C}}
\endminipage
\end{{figure}}
    }}

      \\frame{{
    \\frametitle{{Trimmed Threshold per Pixel}}
    \\vspace{{-1cm}}
    \\begin{{figure}}\centering
\minipage{{0.32\\textwidth}}
  \includegraphics[width=\linewidth]{{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/VcalThresholdTrimmedPerPixel__m20_1/VcalThresholdTrimmedPerPixel.pdf}}
  \caption{{T=-20$^{{\circ}}$C BTC}}
\endminipage\hfill
\minipage{{0.32\\textwidth}}
  \includegraphics[width=\linewidth]{{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/VcalThresholdTrimmedPerPixel__m20_2/VcalThresholdTrimmedPerPixel.pdf}}
  \caption{{T=-20$^{{\circ}}$C ATC}}
\endminipage\hfill
\minipage{{0.32\\textwidth}}%
  \includegraphics[width=\linewidth]{{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/VcalThresholdTrimmedPerPixel__p17_1/VcalThresholdTrimmedPerPixel.pdf}}
  \caption{{T=+17$^{{\circ}}$C}}
\endminipage
\end{{figure}}
    }}

    \\frame{{
    \\begin{{center}}
    \\textbf{{Results from leakage current tests}}
    \\end{{center}}
    }}

  \\frame{{
    \\frametitle{{Overlay of IV Curves}}
    \\begin{{figure}}\centering
\minipage{{0.49\\textwidth}}
  \includegraphics[width=\linewidth]{{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/IVCurveOverlay_m20_2/IVCurveOverlay.pdf}}
  \caption{{T=-20$^{{\circ}}$C BTC}}
\endminipage\hfill
\minipage{{0.49\\textwidth}}
  \includegraphics[width=\linewidth]{{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/IVCurveOverlay_p17_1/IVCurveOverlay.pdf}}
  \caption{{T=+17$^{{\circ}}$C}}
\endminipage
\end{{figure}}
    }}


  \\frame{{
    \\frametitle{{Leakage current at 150V}}
    \\begin{{figure}}\centering
\minipage{{0.49\\textwidth}}
  \includegraphics[width=\linewidth]{{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/LeakageCurrent_m20_2/LeakageCurrent.pdf}}
  \caption{{T=-20$^{{\circ}}$C BTC}}
\endminipage\hfill
\minipage{{0.49\\textwidth}}
  \includegraphics[width=\linewidth]{{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/LeakageCurrent_p17_1/LeakageCurrent.pdf}}
  \caption{{T=+17$^{{\circ}}$C}}
\endminipage
\end{{figure}}
    }}

   \\frame{{
    \\frametitle{{Leakage current slopes}}
    \\begin{{figure}}\centering
\minipage{{0.49\\textwidth}}
  \includegraphics[width=\linewidth]{{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/LeakageCurrentSlope_m20_2/LeakageCurrentSlope.pdf}}
  \caption{{T=-20$^{{\circ}}$C BTC}}
\endminipage\hfill
\minipage{{0.49\\textwidth}}
  \includegraphics[width=\linewidth]{{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/LeakageCurrentSlope_p17_1/LeakageCurrentSlope.pdf}}
  \caption{{T=+17$^{{\circ}}$C}}
\endminipage
\end{{figure}}
    }}

    

    \\frame{{
    \\begin{{center}}
    \\textbf{{Results from X-ray qualification}}
    \\end{{center}}
    }}


   \\frame{{
    \\frametitle{{HR Efficiency}}
    \\begin{{figure}}\centering
\minipage{{0.49\\textwidth}}
  \includegraphics[width=\linewidth]{{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/Efficiency_50/Efficiency.pdf}}
  \caption{{\SI{{50}}{{\mega\hertz\per\square\centi\metre}}}}
\endminipage\hfill
\minipage{{0.49\\textwidth}}
  \includegraphics[width=\linewidth]{{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/Efficiency_120/Efficiency.pdf}}
  \caption{{\SI{{120}}{{\mega\hertz\per\square\centi\metre}}}}
\endminipage
\end{{figure}}
    }}

     \\frame{{
    \\frametitle{{Vcal Calibration}}
    \\begin{{figure}}\centering
\minipage{{0.49\\textwidth}}
  \includegraphics[width=\linewidth]{{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/VcalSlope_Spectrum/VcalSlope.pdf}}
  \caption{{Slope}}
\endminipage\hfill
\minipage{{0.49\\textwidth}}
  \includegraphics[width=\linewidth]{{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/VcalOffset_Spectrum/VcalOffset.pdf}}
  \caption{{Offset}}
\endminipage
\end{{figure}}
    }}



    \\frame{{
    \\begin{{center}}
    \\textbf{{Selection of DAC parameters after trimming}}
    \\end{{center}}
    }}
 

   \\frame{{
    \\frametitle{{V$_{{ana}}$}}
    \\vspace{{-1cm}}
    \\begin{{figure}}\centering
\minipage{{0.32\\textwidth}}
  \includegraphics[width=\linewidth]{{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/DACDistribution_m20_1_vana_35/DACDistribution.pdf}}
  \caption{{T=-20$^{{\circ}}$C BTC}}
\endminipage\hfill
\minipage{{0.32\\textwidth}}
  \includegraphics[width=\linewidth]{{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/DACDistribution_m20_2_vana_35/DACDistribution.pdf}}
  \caption{{T=-20$^{{\circ}}$C ATC}}
\endminipage\hfill
\minipage{{0.32\\textwidth}}%
  \includegraphics[width=\linewidth]{{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/DACDistribution_p17_1_vana_35/DACDistribution.pdf}}
  \caption{{T=+17$^{{\circ}}$C}}
\endminipage
\end{{figure}}
    }}


     \\frame{{
    \\frametitle{{CalDel}}
    \\vspace{{-1cm}}
    \\begin{{figure}}\centering
\minipage{{0.32\\textwidth}}
  \includegraphics[width=\linewidth]{{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/DACDistribution_m20_1_caldel_35/DACDistribution.pdf}}
  \caption{{T=-20$^{{\circ}}$C BTC}}
\endminipage\hfill
\minipage{{0.32\\textwidth}}
  \includegraphics[width=\linewidth]{{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/DACDistribution_m20_2_caldel_35/DACDistribution.pdf}}
  \caption{{T=-20$^{{\circ}}$C ATC}}
\endminipage\hfill
\minipage{{0.32\\textwidth}}%
  \includegraphics[width=\linewidth]{{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/DACDistribution_p17_1_caldel_35/DACDistribution.pdf}}
  \caption{{T=+17$^{{\circ}}$C}}
\endminipage
\end{{figure}}
    }}

     \\frame{{
    \\frametitle{{VthrComp}}
    \\vspace{{-1cm}}
    \\begin{{figure}}\centering
\minipage{{0.32\\textwidth}}
  \includegraphics[width=\linewidth]{{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/DACDistribution_m20_1_vthrcomp_35/DACDistribution.pdf}}
  \caption{{T=-20$^{{\circ}}$C BTC}}
\endminipage\hfill
\minipage{{0.32\\textwidth}}
  \includegraphics[width=\linewidth]{{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/DACDistribution_m20_2_vthrcomp_35/DACDistribution.pdf}}
  \caption{{T=-20$^{{\circ}}$C ATC}}
\endminipage\hfill
\minipage{{0.32\\textwidth}}%
  \includegraphics[width=\linewidth]{{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/DACDistribution_p17_1_vthrcomp_35/DACDistribution.pdf}}
  \caption{{T=+17$^{{\circ}}$C}}
\endminipage
\end{{figure}}
    }}


      \\frame{{
    \\frametitle{{PH\_offset}}
    \\vspace{{-1cm}}
    \\begin{{figure}}\centering
\minipage{{0.32\\textwidth}}
  \includegraphics[width=\linewidth]{{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/DACDistribution_m20_1_phoffset_35/DACDistribution.pdf}}
  \caption{{T=-20$^{{\circ}}$C BTC}}
\endminipage\hfill
\minipage{{0.32\\textwidth}}
  \includegraphics[width=\linewidth]{{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/DACDistribution_m20_2_phoffset_35/DACDistribution.pdf}}
  \caption{{T=-20$^{{\circ}}$C ATC}}
\endminipage\hfill
\minipage{{0.32\\textwidth}}%
  \includegraphics[width=\linewidth]{{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/DACDistribution_p17_1_phoffset_35/DACDistribution.pdf}}
  \caption{{T=+17$^{{\circ}}$C}}
\endminipage
\end{{figure}}
    }}


  \\frame{{
    \\frametitle{{PH\_scale}}
    \\vspace{{-1cm}}
    \\begin{{figure}}\centering
\minipage{{0.32\\textwidth}}
  \includegraphics[width=\linewidth]{{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/DACDistribution_m20_1_phscale_35/DACDistribution.pdf}}
  \caption{{T=-20$^{{\circ}}$C BTC}}
\endminipage\hfill
\minipage{{0.32\\textwidth}}
  \includegraphics[width=\linewidth]{{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/DACDistribution_m20_2_phscale_35/DACDistribution.pdf}}
  \caption{{T=-20$^{{\circ}}$C ATC}}
\endminipage\hfill
\minipage{{0.32\\textwidth}}%
  \includegraphics[width=\linewidth]{{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/DACDistribution_p17_1_phscale_35/DACDistribution.pdf}}
  \caption{{T=+17$^{{\circ}}$C}}
\endminipage
\end{{figure}}
    }}

      \\frame{{
    \\frametitle{{Vtrim}}
    \\vspace{{-1cm}}
    \\begin{{figure}}\centering
\minipage{{0.32\\textwidth}}
  \includegraphics[width=\linewidth]{{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/DACDistribution_m20_1_vtrim_35/DACDistribution.pdf}}
  \caption{{T=-20$^{{\circ}}$C BTC}}
\endminipage\hfill
\minipage{{0.32\\textwidth}}
  \includegraphics[width=\linewidth]{{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/DACDistribution_m20_2_vtrim_35/DACDistribution.pdf}}
  \caption{{T=-20$^{{\circ}}$C ATC}}
\endminipage\hfill
\minipage{{0.32\\textwidth}}%
  \includegraphics[width=\linewidth]{{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/DACDistribution_p17_1_vtrim_35/DACDistribution.pdf}}
  \caption{{T=+17$^{{\circ}}$C}}
\endminipage
\end{{figure}}
    }}

       \\frame{{
    \\frametitle{{Trimbits ($\mu$)}}
    \\vspace{{-1cm}}
    \\begin{{figure}}\centering
\minipage{{0.32\\textwidth}}
  \includegraphics[width=\linewidth]{{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/DACDistribution_m20_1_TrimBits_mu_35/DACDistribution.pdf}}
  \caption{{T=-20$^{{\circ}}$C BTC}}
\endminipage\hfill
\minipage{{0.32\\textwidth}}
  \includegraphics[width=\linewidth]{{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/DACDistribution_m20_2_TrimBits_mu_35/DACDistribution.pdf}}
  \caption{{T=-20$^{{\circ}}$C ATC}}
\endminipage\hfill
\minipage{{0.32\\textwidth}}%
  \includegraphics[width=\linewidth]{{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/DACDistribution_p17_1_TrimBits_mu_35/DACDistribution.pdf}}
  \caption{{T=+17$^{{\circ}}$C}}
\endminipage
\end{{figure}}
    }}

          \\frame{{
    \\frametitle{{Trimbits ($\sigma$)}}
    \\vspace{{-1cm}}
    \\begin{{figure}}\centering
\minipage{{0.32\\textwidth}}
  \includegraphics[width=\linewidth]{{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/DACDistribution_m20_1_TrimBits_sigma_35/DACDistribution.pdf}}
  \caption{{T=-20$^{{\circ}}$C BTC}}
\endminipage\hfill
\minipage{{0.32\\textwidth}}
  \includegraphics[width=\linewidth]{{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/DACDistribution_m20_2_TrimBits_sigma_35/DACDistribution.pdf}}
  \caption{{T=-20$^{{\circ}}$C ATC}}
\endminipage\hfill
\minipage{{0.32\\textwidth}}%
  \includegraphics[width=\linewidth]{{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/DACDistribution_p17_1_TrimBits_sigma_35/DACDistribution.pdf}}
  \caption{{T=+17$^{{\circ}}$C}}
\endminipage
\end{{figure}}
    }}



    \end{{document}}

    """ 

    ModuleFailureOverviewFigureTemplate = """
      \\begin{{figure}} \centering \\advance\leftskip-0.9cm
      \includegraphics[width=1.14\\textwidth, angle=0] {{{GlobalOverviewPath}/ProductionOverview/ProductionOverviewPage_Total/{ModuleFailuresOverviewFolder}/ModuleFailuresOverview.pdf}}
      \end{{figure}}
      """

    GlobalOverviewPath = Configuration.get('Paths', 'GlobalOverviewPath')
    ModuleFailuresOverviewPath = GlobalOverviewPath + "/ProductionOverview/ProductionOverviewPage_Total/ModuleFailuresOverview_*"
    ModuleFailuresOverviewFolders = glob.glob(ModuleFailuresOverviewPath)
    try:
      ModuleFailuresOverviewFolders.sort(key=lambda x: int(x.strip('/').split('_')[-1]))
    except:
      pass

    ModuleFailureOverviewFigures = ""
    for ModuleFailuresOverviewFolder in ModuleFailuresOverviewFolders:

        FolderName = ModuleFailuresOverviewFolder.replace('\\','/').split('/')[-1]
        ModuleFailureOverviewFigures += ModuleFailureOverviewFigureTemplate.format(GlobalOverviewPath=GlobalOverviewPath, ModuleFailuresOverviewFolder=FolderName)


    context = {
      "nA":nA, 
      "nB":nB,
      "nC": nC,
      "nM" : nM,
      "nAB": nAB,
      "nT" : nT,
      "nQ" : nQ,
      "Pass" : Pass,
      "lcstartupB" : lcstartupB,
      "lcstartupC" : lcstartupC,
      "IV150B" : IV150B,
      "IV150C" : IV150C,
      "IV150m20B" : IV150m20B,
      "IV150m20C" : IV150m20C,
      "IRatio150B" : IRatio150B,
      "IRatio150C" : IRatio150C,
      "IRatio150" : IRatio150,
      "IVSlopeB" : IVSlopeB,
      "IVSlopeC" : IVSlopeC,
      "totDefectsB" : totDefectsB,
      "totDefectsC" : totDefectsC,
      "totDefectsXrayB" : totDefectsXrayB,
      "totDefectsXrayC" : totDefectsXrayC,
      "BBFullB" : BBFullB,
      "BBFullC" : BBFullC,
      "BBXrayB" : BBXrayB,
      "BBXrayC" : BBXrayC,
      "AddressdefB" : AddressdefB,
      "AddressdefC" : AddressdefB,
      "TrimbitdefB" : TrimbitdefB,
      "TrimbitdefC" : TrimbitdefC,
      "MaskdefB" : MaskdefB,
      "MaskdefC" : MaskdefC,
      "deadpixB" : deadpixB,
      "deadpixC" : deadpixC,
      "uniformityB" : uniformityB,
      "uniformityC" : uniformityC,
      "NoiseB" : NoiseB,
      "NoiseC" : NoiseC,
      "NoiseXrayB" : NoiseXrayB,
      "NoiseXrayC" : NoiseXrayC,
      "PedSpreadB" : PedSpreadB,
      "PedSpreadC" : PedSpreadC,
      "RelGainWB" : RelGainWB,
      "RelGainWC" : RelGainWC,
      "VcalThrWB" : VcalThrWB,
      "VcalThrWC" : VcalThrWC,
      "LowHREfB" : LowHREfB,
      "LowHREfC" : LowHREfC,
      "lcstartup" : lcstartup,
      "IV150" : IV150,
      "IV150m20" : IV150m20,
      "IVSlope" : IVSlope,
      "totDefects" : totDefects,
      "totDefectsXray" : totDefectsXray,
      "BBFull" : BBFull,
      "BBXray" : BBXray,
      "Addressdef" : Addressdef,
      "Trimbitdef" : Trimbitdef,
      "Maskdef" : Maskdef,
      "deadpix" : deadpix,
      "uniformity" : uniformity,
      "Noise" : Noise,
      "NoiseXray" : NoiseXray,
      "PedSpread" : PedSpread,
      "RelGainW" : RelGainW,
      "VcalThrW" : VcalThrW,
      "LowHREf" : LowHREf,
      "FiguresPath" : FiguresPath,
      "nBrokenROCs" : nBrokenROCs,
      "BrokenROC" : BrokenROC,
      "nBrokenROCsX" : nBrokenROCsX,
      "BrokenROCX" : BrokenROCX,
      "nAtoB" : nAtoB,
      "nAtoC" : nAtoC,
      "nBtoA" : nBtoA,
      "nBtoC" : nBtoC,
      "nCtoA" : nCtoA,
      "nCtoB" : nCtoB,
      "nAtoBX" : nAtoBX,
      "nAtoCX" : nAtoCX,
      "nBtoAX" : nBtoAX,
      "nBtoCX" : nBtoCX,
      "nCtoAX" : nCtoAX,
      "nCtoBX" : nCtoBX,
      "ModuleFailureOverviewFigures": ModuleFailureOverviewFigures,
      "nHDI" : nHDI,
      "HDI" : HDI
    } 


    oldWorkingDirectory = os.getcwd()
    with  open(filename,'w') as myfile:
      myfile.write(template.format(**context))

    print "compile tex file..."

    try:
      os.chdir(OutputDirectoryPath)
      proc=subprocess.Popen(shlex.split("pdflatex '%s'"%filename))
      proc.communicate()
      for extension in ['aux', 'nav', 'snm', 'toc', 'out']:
        auxFile = filename[0:-4]+"."+extension
        if os.path.isfile(auxFile):
          try:
            os.remove(auxFile)
          except:
            print "could not remove auxiliary file: %s"%auxFile
    except:
      print "could not compile tex file, pdflatex installed?"
      raise
    os.chdir(oldWorkingDirectory)

