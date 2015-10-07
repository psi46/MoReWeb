from sys import argv
import time
from time import gmtime, strftime
import os
import ConfigParser
import subprocess
import shlex

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
    lcstartupB = args['nlcstartupB']
    lcstartupC = args['nlcstartupC']
    IV150B = args['nIV150B']
    IV150C = args['nIV150C']
    IRatio150B = args['nCurrentRatioB']
    IRatio150C = args['nCurrentRatioC']
    IVSlopeB = args['nIVSlopeB']
    IVSlopeC = args['nIVSlopeC']
    RecCurrentB = args['nRecCurrentB']
    RecCurrentC = args['nRecCurrentC']
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
    IV150 = round(float(IV150C)/nQ*100,1)
    IVSlope = round(float(IVSlopeC)/nQ*100,1)
    RecCurrent = round(float(RecCurrentC)/nQ*100,1)
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
    
 

    template = """
    \documentclass[xcolor=dvipsnames]{{beamer}}
    \usepackage{{booktabs}}
    \usepackage{{multirow}}
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

    \\begin{{document}}

    \\title{{\\textbf{{Status of module qualification}}}}   
    \\author{{\\textbf{{ETH Pixel Group}}}} 
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
    \multirow{{2}}{{*}}{{Sensor}}     & LC startup        & {lcstartupB} & {lcstartupC} &  {lcstartup}\\\\
                                    & IV 150              & {IV150B} & {IV150C} & {IV150} \\\\
                                    & I(+17)/I(-20)       & {IRatio150B} & {IRatio150C} & {IRatio150} \\\\ \midrule
    \multirow{{2}}{{*}}{{Sensor m20}} & IV slope          & {IVSlopeB} & {IVSlopeC} & {IVSlope} \\\\
                                    & Rec current         & {RecCurrentB} & {RecCurrentC} & {RecCurrent} \\\\ \midrule
    \multirow{{9}}{{*}}{{Pixel defects}} & Total defects  & {totDefectsB} & {totDefectsC} & {totDefects} \\\\ 
                                    & Total defects X-ray & {totDefectsXrayB} & {totDefectsXrayC} & {totDefectsXray} \\\\
                                    & BB Fulltest         & {BBFullB} & {BBFullC} & {BBFull} \\\\
                                    & BB X-ray            & {BBXrayB} & {BBXrayC} & {BBXray} \\\\
                                    & Address defects      & {AddressdefB} & {AddressdefC} & {Addressdef} \\\\
                                    & Trimbit defects     & {TrimbitdefB} & {TrimbitdefC} & {Trimbitdef} \\\\
                                    & Mask defects        & {MaskdefB} & {MaskdefC} & {Maskdef} \\\\
                                    & Dead pixels         & {deadpixB} & {deadpixC} & {deadpix} \\\\
                                    & Uniformity problem  & {uniformityB} & {uniformityC} & {uniformity} \\\\ \\bottomrule 
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
    \\frametitle{{Defects overview}}
    \\vspace{{-1cm}}
    \\begin{{figure}} \centering \\advance\leftskip-0.9cm
    \includegraphics[width=1.14\\textwidth, angle=0] {{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/ModuleFailuresOverview/ModuleFailuresOverview.pdf}}
    \end{{figure}}
    }}

    \\frame{{
    \\frametitle{{Fulltest duration}}
    \\vspace{{-1cm}}
    \\begin{{figure}} \centering \\advance\leftskip-0.9cm
    \includegraphics[width=1.14\\textwidth, angle=0] {{{FiguresPath}/ProductionOverview/ProductionOverviewPage_Total/AbstractClasses_GeneralProductionOverview/Duration.pdf}}
    \end{{figure}}
    }}



    \end{{document}}

    """ 

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
      "IRatio150B" : IRatio150B,
      "IRatio150C" : IRatio150C,
      "IRatio150" : IRatio150,
      "IVSlopeB" : IVSlopeB,
      "IVSlopeC" : IVSlopeC,
      "RecCurrentB" : RecCurrentB,
      "RecCurrentC" : RecCurrentC,
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
      "IVSlope" : IVSlope,
      "RecCurrent" : RecCurrent,
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
      "FiguresPath" : FiguresPath
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

