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


    #Get Grading criteria
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
    year = strftime("%Y", d)

    filename = OutputDirectoryPath + "/ModuleProductionOverview_{year}_Week{week}.tex".format(year=year, week=week)
    
    #Fetch data

    #Values for slide 3
    nA = args['nA']
    nB = args['nB']
    nC = args['nC']
    nM = args['nM']
    nFirstModule = args['nFirstModule']
    nLastModule = args['nLastModule']

    #For summary table slide 4
    totIV = args['nIV'] + args['nIVP']
    totIVP = args['nIVP']
    totHDI = args['nHDIf']
    totDC = args['nDC']
    totLowEf = args['nLowHREf']
    totBB = args['nBB']
    totNP = args['nNP']
    totPD = args['ntotDefects']
    totOthers = args['nOthers']


    #Numbers for tables on slides 5 and 6
    lcstartupB = args['nlcstartupB']
    lcstartupC = args['nlcstartupC']
    IV150B = args['nIV150B']
    IV150C = args['nIV150C']
    IV150Bandm20 = args['nIV150B+']
    IV150Candm20 = args['nIV150C+']
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
    

    #Number and comments of manual regradings
    ntoB = args['ntoB']
    ntoC = args['ntoC']
    ntoA = args['ntoA']
    ntoBX = args['ntoBX']
    ntoCX = args['ntoCX']
    ntoAX = args['ntoAX']
    comments = args['commentsgradechange']
    commentsX = args['commentsgradechangeX']

 
    #Calculate values for slide 3
    nAB = int(nA) + int(nB)
    nT = nAB + int(nC) + int(nM)
    nQ = nAB + int(nC)
    Pass = round(float(nAB)/nQ*100,1) if nQ > 0 else 0

    #Get percentage of production for each defect - slide 4
    FHDI = round(float(totHDI)/nQ*100,1) if nQ > 0 else 0
    FIV = round(float(totIV)/nQ*100,1) if nQ > 0 else 0
    FIVP = round(float(totIVP)/nQ*100,1) if nQ > 0 else 0
    FDC = round(float(totDC)/nQ*100,1) if nQ > 0 else 0
    FPD = round(float(totPD)/nQ*100,1) if nQ > 0 else 0
    FLowEf = round(float(totLowEf)/nQ*100,1) if nQ > 0 else 0
    FOthers = round(float(totOthers)/nQ*100,1) if nQ > 0 else 0
    FBB = round(float(totBB)/nQ*100,1) if nQ > 0 else 0
    FNP = round(float(totNP)/nQ*100,1) if nQ > 0 else 0

    #Get percentage of production for each defect - slide 5 and 6
    lcstartup = round(float(lcstartupC)/nQ*100,1) if nQ > 0 else 0
    IV150 = round(float(IV150C)/nQ*100,1) if nQ > 0 else 0
    IV150andm20 = round(float(IV150Candm20)/nQ*100,1) if nQ > 0 else 0
    IV150m20 = round(float(IV150m20C)/nQ*100,1) if nQ > 0 else 0
    IVSlope = round(float(IVSlopeC)/nQ*100,1) if nQ > 0 else 0
    totDefects = round(float(totDefectsC)/nQ*100,1) if nQ > 0 else 0
    totDefectsXray = round(float(totDefectsXrayC)/nQ*100,1) if nQ > 0 else 0
    BBFull = round(float(BBFullC)/nQ*100,1) if nQ > 0 else 0
    BBXray = round(float(BBXrayC)/nQ*100,1) if nQ > 0 else 0
    Addressdef = round(float(AddressdefC)/nQ*100,1) if nQ > 0 else 0
    Trimbitdef = round(float(TrimbitdefC)/nQ*100,1) if nQ > 0 else 0
    Maskdef = round(float(MaskdefC)/nQ*100,1) if nQ > 0 else 0
    deadpix = round(float(deadpixC)/nQ*100,1) if nQ > 0 else 0
    Noise = round(float(NoiseC)/nQ*100,1) if nQ > 0 else 0
    NoiseXray = round(float(NoiseXrayC)/nQ*100,1)if nQ > 0 else 0
    PedSpread = round(float(PedSpreadC)/nQ*100,1) if nQ > 0 else 0
    RelGainW = round(float(RelGainWC)/nQ*100,1) if nQ > 0 else 0
    VcalThrW = round(float(VcalThrWC)/nQ*100,1) if nQ > 0 else 0
    LowHREf = round(float(LowHREfC)/nQ*100,1) if nQ > 0 else 0
    IRatio150 = round(float(IRatio150C)/nQ*100,1) if nQ > 0 else 0

    

    # Template for latex presentation
    template = ''
    try:
        with open('LaTeX/presentation.tex', 'r') as presentationTemplate:
            template = presentationTemplate.read()
    except:
        print "\x1b[31mCould not read template: LaTeX/presentation.tex\x1b[0m"

    # build module failure overview plots .tex code
    ModuleFailureOverviewFigureTemplate = ''
    try:
        with open('LaTeX/ModuleFailureOverviewFigure.tex', 'r') as presentationTemplate:
            ModuleFailureOverviewFigureTemplate = presentationTemplate.read()
    except:
        print "\x1b[31mCould not read template: LaTeX/ModuleFailureOverviewFigure.tex\x1b[0m"

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

    # build grade C table

    # get dictionary
    PrimaryFailureReasonDictionary = args['PrimaryFailureReason']

    # convert to list and order by number of modules affected
    PrimaryFailureReasonList = []
    for k,v in PrimaryFailureReasonDictionary.iteritems():
        PrimaryFailureReasonList.append({'Defect': k, 'Number': len(v)})
    PrimaryFailureReasonList.sort(key=lambda x: x['Number'], reverse=True)

    # create tex table
    PrimaryFailureReason = '\\\\\n'.join([' & '.join([x['Defect'].replace('_','\_'), str(x['Number']), '{0:1.2f}'.format(100*float(x['Number']) / nQ if nQ > 0 else 0)]) for x in PrimaryFailureReasonList if x['Number'] > 0])

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
        "IV150Bandm20" : IV150Bandm20,
        "IV150Candm20" : IV150Candm20,
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
        "IV150andm20" : IV150andm20,
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
        "Noise" : Noise,
        "NoiseXray" : NoiseXray,
        "PedSpread" : PedSpread,
        "RelGainW" : RelGainW,
        "VcalThrW" : VcalThrW,
        "LowHREf" : LowHREf,
        "FiguresPath" : FiguresPath,
        "ntoB" : ntoB,
        "ntoC" : ntoC,
        "ntoA" : ntoA,
        "ntoCX" : ntoCX,
        "ntoAX" : ntoAX,
        "ntoBX" : ntoBX,
        "ModuleFailureOverviewFigures": ModuleFailureOverviewFigures,
        "totIV" : totIV,
        "totIVP" : totIVP,
        "totHDI" : totHDI,
        "totDC" : totDC,
        "totBB" : totBB,
        "totNP" : totNP,
        "totPD" : totPD,
        "totLowEf" : totLowEf,
        "totOthers" : totOthers,
        "FIV" : FIV,
        "FIVP" : FIVP,
        "FHDI" : FHDI,
        "FDC" : FDC,
        "FPD" : FPD,
        "FBB" : FBB,
        "FNP" : FNP,
        "FLowEf" : FLowEf,
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
        'XRayHighRateEfficiency_max_allowed_loweff_B_Rate1' : XRayHighRateEfficiency_max_allowed_loweff_B_Rate1,
        'comments' : comments,
        'commentsX' : commentsX,
        'nFirstModule' : nFirstModule,
        'nLastModule' : nLastModule,
        'PrimaryFailureReason': PrimaryFailureReason,
    } 


    oldWorkingDirectory = os.getcwd()
    with open(filename,'w') as myfile:
        try:
            TeXCodeFormatted = template.format(**context)
        except:
            print "\x1b[31mcould not print formatted tex code for:\x1b[31m"
            print context
            TeXCodeFormatted = None

        if TeXCodeFormatted:
            try:
                myfile.write(TeXCodeFormatted)
            except:
                print "\x1b[31mcould not write to file: %s\x1b[31m"%filename


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

