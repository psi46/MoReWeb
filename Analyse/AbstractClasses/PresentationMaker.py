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
    'Configuration/GradingParameters.cfg',
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

    slopeivB = Configuration.get('GradingParameters','slopeivB')
    leakageCurrentRatioB = Configuration.get('GradingParameters','leakageCurrentRatioB')
    currentB = Configuration.get('GradingParameters','currentB')
    currentC = Configuration.get('GradingParameters','currentC')
    LeakageCurrentPON_B = Configuration.get('GradingParameters','LeakageCurrentPON_B')
    LeakageCurrentPON_C = Configuration.get('GradingParameters','LeakageCurrentPON_C')
    pedestalB = Configuration.get('GradingParameters','pedestalB')
    pedestalC = Configuration.get('GradingParameters','pedestalC')
    noiseB = Configuration.get('GradingParameters','noiseB')
    noiseC = Configuration.get('GradingParameters','noiseC')
    trimmingB = Configuration.get('GradingParameters','trimmingB')
    trimmingC = Configuration.get('GradingParameters','trimmingC')
    gainB = Configuration.get('GradingParameters','gainB')
    gainC = Configuration.get('GradingParameters','gainC')
    defectsB = Configuration.get('GradingParameters','defectsB')
    defectsC = Configuration.get('GradingParameters','defectsC')
    trimThr = Configuration.get('GradingParameters','trimThr')
    tthrTol = Configuration.get('GradingParameters','tthrTol')
    gainMin = Configuration.get('GradingParameters','gainMin')
    gainMax = Configuration.get('GradingParameters','gainMax')
    pixelNoiseMin = Configuration.get('GradingParameters','pixelNoiseMin')
    pixelNoiseMax = Configuration.get('GradingParameters','pixelNoiseMax')
    TrimBitDifference = Configuration.get('GradingParameters','TrimBitDifference')
    BumpBondThr  = Configuration.get('GradingParameters','BumpBondThr')
    XRayHighRate_SCurve_Noise_Threshold_B = Configuration.get('GradingParameters','XRayHighRate_SCurve_Noise_Threshold_B')
    XRayHighRate_SCurve_Noise_Threshold_C = Configuration.get('GradingParameters','XRayHighRate_SCurve_Noise_Threshold_C')
    XRayHighRateEfficiency_max_allowed_loweff_A_Rate1 = Configuration.get('GradingParameters','XRayHighRateEfficiency_max_allowed_loweff_A_Rate1')
    XRayHighRateEfficiency_max_allowed_loweff_B_Rate1 = Configuration.get('GradingParameters','XRayHighRateEfficiency_max_allowed_loweff_B_Rate1')

    pixelThrMin = int(trimThr) - int(tthrTol)
    pixelThrMax = int(trimThr) + int(tthrTol)


    FiguresPath = Configuration.get('Paths', 'GlobalOverviewPath')



    datenow = time.strftime("%d %m %Y")
    d = time.strptime(datenow, "%d %m %Y")
    week = strftime("%U", d)

    filename = OutputDirectoryPath + "/ModuleProductionOverview_Week{0}.tex".format(week)
    
    totIV = args['nIV']
    totHDI = args['nHDIf']
    totROC = args['nBrokenROC']
    totDC = args['nDC']
    totLowEf = args['nLowHREf']
    tot1PD = args['nSinglePixDefect']
    totPD = args['ntotDefects']
    totOthers = args['nOthers']
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

    FHDI = round(float(totHDI)/nQ*100,1)
    FIV = round(float(totIV)/nQ*100,1)
    FDC = round(float(totDC)/nQ*100,1)
    F1PD = round(float(tot1PD)/nQ*100,1)
    FPD = round(float(totPD)/nQ*100,1)
    FLowEf = round(float(totLowEf)/nQ*100,1)
    FROC = round(float(totROC)/nQ*100,1)
    FOthers = round(float(totOthers)/nQ*100,1)
    
 

    template = """
    \documentclass[xcolor=dvipsnames]{{beamer}}
    \usepackage{{booktabs}}
    \usepackage{{multirow}}
    %\usepackage{{siunitx}}
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

    \\begin{{frame}}[label=GradeCmodules]
    \\frametitle{{Defects of grade C modules}}
    \\begin{{table}}[]
\centering
\\begin{{tabular}}{{@{{}}lcc@{{}}}}
\\toprule
Defect               & \# modules graded C & C (\%$^*$) \\\\ \midrule
Leakage current      & {totIV}     & {FIV}       \\\\
HDI                  & {totHDI}    & {FHDI}      \\\\
Defective ROC        & {totROC}    & {FROC}      \\\\
DC defects           & {totDC}     & {FDC}       \\\\
Low HR Efficiency    & {totLowEf}  & {FLowEf}    \\\\
Single pixel defect  & {tot1PD}    & {F1PD}      \\\\
Sum of pixel defects & {totPD}     & {FPD}       \\\\ 
Others               & {totOthers} & {FOthers}   \\\\ \\bottomrule
\end{{tabular}}
\end{{table}}
    *of completely tested modules
   \end{{frame}}

    \\frame{{
    \\frametitle{{Detailed defects I}}
    \\begin{{table}}[]
    \centering
    \\begin{{tabular}}{{@{{}}llccc@{{}}}}
    \\toprule
                                    & Defects             & B & C &  C (\%$^*$)\\\\ \midrule
    \multirow{{5}}{{*}}{{Sensor}}   & $I_{{leak}}$ startup & {lcstartupB} & {lcstartupC} & {lcstartup}\\\\
                                    & $I_{{leak}}$ (+17)   & {IV150B}     & {IV150C}     & {IV150} \\\\
                                    & $I_{{leak}}$ (-20)   & {IV150m20B}  & {IV150m20C}  & {IV150m20} \\\\ 
                                    & I(+17)/I(-20)         & {IRatio150B} & {IRatio150C} & {IRatio150} \\\\ 
                                     & IV slope             & {IVSlopeB}   & {IVSlopeC}   & {IVSlope} \\\\ \midrule
    \multirow{{6}}{{*}}{{Chip performance}} & Noise         & {NoiseB}     & {NoiseC}     & {Noise} \\\\
                                    & Noise X-ray           & {NoiseXrayB} & {NoiseXrayC} & {NoiseXray} \\\\
                                    & Pedestal spread       & {PedSpreadB} & {PedSpreadC} & {PedSpread} \\\\
                                    & Rel. Gain Width       & {RelGainWB}  & {RelGainWC}  & {RelGainW} \\\\
                                    & VcalThr Width         & {VcalThrWB}  & {VcalThrWC}  & {VcalThrW} \\\\
                                    & Low HR Efficiency     & {LowHREfB}   & {LowHREfC}   & {LowHREf} \\\\ \\bottomrule 
    \end{{tabular}}
    \end{{table}}
    *of completely tested modules \\\\
    }}

    \\frame{{
    \\frametitle{{Detailed defects II}}
    \\begin{{table}}[]
    \centering
    \\begin{{tabular}}{{@{{}}llccc@{{}}}}
    \\toprule
                                          & Defects             & B                 & C                 &  C (\%$^*$)\\\\ \midrule
    \multirow{{12}}{{*}}{{Pixel defects}} & Total defects       & {totDefectsB}     & {totDefectsC}     & {totDefects} \\\\ 
                                          & Total defects X-ray & {totDefectsXrayB} & {totDefectsXrayC} & {totDefectsXray} \\\\
                                          & BB Fulltest         & {BBFullB}         & {BBFullC}         & {BBFull} \\\\
                                          & BB X-ray            & {BBXrayB}         & {BBXrayC}         & {BBXray} \\\\
                                          & Address defects     & {AddressdefB}     & {AddressdefC}     & {Addressdef} \\\\
                                          & Trimbit defects     & {TrimbitdefB}     & {TrimbitdefC}     & {Trimbitdef} \\\\
                                          & Mask defects        & {MaskdefB}        & {MaskdefC}        & {Maskdef} \\\\
                                          & Dead pixels         & {deadpixB}        & {deadpixC}        & {deadpix} \\\\
                                          & Defective ROC       & 0                 & {nBrokenROCs}     & {BrokenROC} \\\\
                                          & Defective ROC X-ray & 0                 & {nBrokenROCsX}    & {BrokenROCX} \\\\
                                          & HDI Problem         & 0                 & {nHDI}            & {HDI} \\\\
                                          & Uniformity problem  & {uniformityB}     & {uniformityC}     & {uniformity} \\\\ \\bottomrule 
    \end{{tabular}}
    \end{{table}}
    *of completely tested modules \\\\
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
  \caption{{50 MHz/cm2}}
\endminipage\hfill
\minipage{{0.49\\textwidth}}
  \includegraphics[width=\linewidth]{{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/Efficiency_120/Efficiency.pdf}}
  \caption{{120 MHz/cm2}}
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
Grades are taken from HR Qualification
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

\\begin{{frame}}[label=Pixeldefects]
\\frametitle{{Pixel defects}}
\\begin{{itemize}}
    \item Address defects
    \item BB defects
    \item Noise defects
    \item Pedestal Spread
    \item Relative Gain Width
    \item Vcal Threshold Width
    \item Trimbit defects
    \item Dead Pixels
    \item Mask defects
\end{{itemize}}
\end{{frame}}
    
    
\\frame{{
\\frametitle{{Explanation of defects of grade C modules (slide \\ref{{GradeCmodules}})}}
There is no double counting, if more than one grade C defect is present, only the first one in the list is considered.
\\begin{{itemize}}
    \item \\textbf{{Leakage current}}: $I_{{leak}}>10\mu$A at 17$^{{\circ}}$C or -20 $^{{\circ}}$C
    \item \\textbf{{HDI}}: Any HDI problem specified in the "comments.txt" file
    \item \\textbf{{Defective ROC}}: ROCs with more than 500 pixel defects or with more than 20 non-uniform columns in the X-ray qualification
    \item \\textbf{{Double column defects}}: ROCs with 1 or 2  non-uniform columns 
    \item \\textbf{{Low HR efficiency}}: columns where the efficiency is $<95\%$
    \item \\textbf{{Single pixel defect}}: ROCs where a single pixel defect (see list on slide \\ref{{Pixeldefects}}) leads to a grade C
    \item \\textbf{{Sum of pixel defects}}: ROCs where only the combination of different pixel defects leads to a grade C
    \item \\textbf{{Others - for now}}: Not programmable module (defective TBM?) 
\end{{itemize}}       
}}
    
\\frame{{
\\frametitle{{Grading criteria - Sensor grading}}
\\begin{{table}}[]
\centering
\\begin{{tabular}}{{@{{}}lcc@{{}}}}
\\toprule
                                             & B & C \\\\ \midrule
Measured $I_{{leak}}$ (17$^{{\circ}}$, 150V, pretest) [$\mu$A] &  $<{LeakageCurrentPON_B}$  & $<{LeakageCurrentPON_C}$ \\\\
Measured $I_{{leak}}$ (150V) [$\mu$A] & $>{currentB}$   &  $>{currentC}$ \\\\
Slope (T=17$^{{\circ}}$)                       &  $>{slopeivB}$  & - \\\\
I(17$^{{\circ}}$, 150V)/I(-20$^{{\circ}}$, 150V) &  $<{leakageCurrentRatioB}$  & - \\\\ \\bottomrule
\end{{tabular}}
\end{{table}}
}}

\\frame{{
\\frametitle{{Grading criteria - Electrical grading I}}
Performance parameters
\\begin{{table}}[]
\centering
\\begin{{tabular}}{{@{{}}lcc@{{}}}}
\\toprule
                                             & B & C \\\\ \midrule
Noise [e$^{{-}}$] & $>{noiseB}$   &  $>{noiseC}$ \\\\
Vcal Threshold Width     &  $>{trimmingB}$  & $>{trimmingC}$ \\\\
Pedestal Spread &  $>{pedestalB}$  & $>{pedestalC}$ \\\\
Relative Gain Width &  $>{gainB}$  & $>{gainC}$ \\\\ \\bottomrule
\end{{tabular}}
\end{{table}}
}}

\\frame{{
\\frametitle{{Grading criteria - Electrical grading II}}
Pixel defects per ROC ($\geq {defectsB} \Rightarrow$ B, $ \geq {defectsC} \Rightarrow $C)
\\begin{{table}}[]
\centering
\\begin{{tabular}}{{@{{}}lc@{{}}}}
\\toprule
                                            & defective pixel if: \\\\ \midrule
Bump defects  &  $<{BumpBondThr}$ \\\\
Dead/Ineffient pixel & $<$100\% \\\\
Mask defect & pixel not maskable ($\geq 1$ defect $\Rightarrow$ C) \\\\
Noise [e$^{{-}}$] & $<${pixelNoiseMin} or $>${pixelNoiseMax} \\\\
Threshold [Vcal] & $<${pixelThrMin} or $>{pixelThrMax}$ \\\\
Trimbit (3 most significant) & $\Delta$ Thr $<{TrimBitDifference}$ \\\\
Gain [Vcal/ADC] & $<${gainMin} or $>{gainMax}$ \\\\
Address defect & addr. read out $\\neq$ addr. cal. signal sent \\\\ \\bottomrule
\end{{tabular}}
\end{{table}}
}}

\\frame{{
\\frametitle{{Grading criteria - X-ray HR grading}}
Performance parameters
\\begin{{table}}[]
\centering
\\begin{{tabular}}{{@{{}}lcc@{{}}}}
\\toprule
                                             & B & C \\\\ \midrule
Noise [e$^{{-}}$] & $>{XRayHighRate_SCurve_Noise_Threshold_B}$   &  $>{XRayHighRate_SCurve_Noise_Threshold_C}$ \\\\
Efficiency 120 MHz/cm2   &  $>{XRayHighRateEfficiency_max_allowed_loweff_A_Rate1}\%$  & $>{XRayHighRateEfficiency_max_allowed_loweff_B_Rate1}\%$ \\\\
Column uniformity problems &  - & $\geq 1$ \\\\
Readout uniformity problems &  -  & $\geq 1$ \\\\ \\bottomrule
\end{{tabular}}
\end{{table}}

Pixel defects per ROC ($\geq {defectsB}  \Rightarrow$ B, $ \geq {defectsC} \Rightarrow $C)
\\begin{{table}}[]
\centering
\\begin{{tabular}}{{@{{}}lc@{{}}}}
\\toprule
                                            & defective pixel if: \\\\ \midrule
Bump defects  &  pixel is alive but no hits in hitmap \\\\
Noise [e$^{{-}}$] & $>${XRayHighRate_SCurve_Noise_Threshold_C} \\\\
Hot pixel & can't be re-trimmed and has to be masked \\\\ \\bottomrule
\end{{tabular}}
\end{{table}}
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
      "HDI" : HDI,
      "totIV" : totIV,
      "totHDI" : totHDI,
      "totDC" : totDC,
      "tot1PD" : tot1PD,
      "totPD" : totPD,
      "totLowEf" : totLowEf,
      "totROC" : totROC,
      "totOthers" : totOthers,
      "FIV" : FIV,
      "FHDI" : FHDI,
      "FDC" : FDC,
      "F1PD" : F1PD,
      "FPD" : FPD,
      "FLowEf" : FLowEf,
      "FROC" : FROC,
      "FOthers" : FOthers,
      "slopeivB" : slopeivB,
      "leakageCurrentRatioB" : leakageCurrentRatioB,
      "currentB" : currentB,
      "currentC" : currentC,
      "LeakageCurrentPON_B" : LeakageCurrentPON_B,
      "LeakageCurrentPON_C" : LeakageCurrentPON_C,
      "noiseB" : noiseB,
      "noiseC" : noiseC,
      "trimmingB" : trimmingB,
      "trimmingC" : trimmingC,
      "gainB" : gainB,
      "gainC" : gainC,
      "pedestalB" : pedestalB,
      "pedestalC" : pedestalC,
      "defectsB"  : defectsB,
      "defectsC" : defectsC,
      "gainMax" : gainMax,
      "gainMin" : gainMin,
      "TrimBitDifference" : TrimBitDifference,
      "pixelNoiseMin" : pixelNoiseMin,
      "pixelNoiseMax" : pixelNoiseMax,
      "pixelThrMin" : pixelThrMin,
      "pixelThrMax" : pixelThrMax,
      "BumpBondThr" : BumpBondThr,
      'XRayHighRate_SCurve_Noise_Threshold_B' : XRayHighRate_SCurve_Noise_Threshold_B,
      'XRayHighRate_SCurve_Noise_Threshold_C' : XRayHighRate_SCurve_Noise_Threshold_C,
      'XRayHighRateEfficiency_max_allowed_loweff_A_Rate1' : XRayHighRateEfficiency_max_allowed_loweff_A_Rate1,
      'XRayHighRateEfficiency_max_allowed_loweff_B_Rate1' : XRayHighRateEfficiency_max_allowed_loweff_B_Rate1

    } 


    oldWorkingDirectory = os.getcwd()
    with  open(filename,'w') as myfile:
      myfile.write(template.format(**context))

    print "compile tex file..."

    try:
      FNULL = open(os.devnull, 'w')
      os.chdir(OutputDirectoryPath)
      proc=subprocess.Popen(shlex.split("pdflatex '%s'"%filename), stdout=FNULL)
      proc.communicate()
      proc=subprocess.Popen(shlex.split("pdflatex '%s'"%filename), stdout=FNULL)
      proc.communicate()
      print "LaTeX compiler returned: %d"%proc.returncode
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

