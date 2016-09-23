import ROOT, Helper.HtmlParser, os
class TestResultEnvironment:
    # Configuration attributes
    Configuration = {
        'Database':{
            'UseGlobal':False,
            'Type':'',
            'Host':'',
            'User':'',
            'Password':'',
            'DatabaseName':'',
        },
        'DefaultValues':{
            'CanvasWidth': 300,
            'CanvasHeight': 300,
        },
        'ParameterFile':'',
        'GzipSVG':True,
        'DefaultImageFormat':'svg',
        'AbsoluteOverviewPage': None,
    }

    GradingParameters = {
        'trimThr':35,
        'tthrTol':10,
        'gainMin':1.,
        'gainMax': 4.5,
        'par1Min':0.,
        'par1Max':2.,
        'noiseB':200,
        'noiseC':300,
        'pixelNoiseMin':50,
        'pixelNoiseMax':400,
        'noiseDistribution': 1.0,
        'trimmingB':200,
        'trimmingC':400,
        'trmDistribution':1.0,
        'gainB': 0.1,
        'gainC': 0.2,
        'gainDistribution': 1.0,
        'pedestalB':2500,
        'pedestalC':5000,
        'pedDistribution': 0.96,
        'par1B':1000.,
        'par1C':2000.,
        'par1Distribution': 1.0,
        'defectsB':42,
        'defectsC':168,
        'maskDefectsB':1,
        'maskDefectsC':1,
        'currentB':2,
        'currentC':10,
        'leakageCurrentRatioB':20,
        'leakageCurrentRatioC':-999,
        'slopeivB': 2,
        'slopeivC': 999,
        'leakageCurrentPON_B': 5,
        'leakageCurrentPON_C': 15,
        'IanaLossThr': 15,
        # check
        'minThrDiff':-5,
        'maxThrDiff':5,
        'BumpBondThr': 150,
        'StandardVcal2ElectronConversionFactor':50,
        'IVCurrentFactor':-1e6,
        'TrimBitDifference':2.,
        'excludeTrimBit14':1,
        'PixelMapMaxValue':10,
        'PixelMapMinValue':0,
        'PixelMapMaskDefectUpperThreshold': 0,
        'BumpBondingProblemsNSigma': 5,
        'BumpBondingProblemsMinDistanceFromPeak': 5,
        'XRayHighRateEfficiency_NInterpolationRates': 2,
        'XRayHighRateEfficiency_InterpolationRate1': 50,
        'XRayHighRateEfficiency_InterpolationRate2': 120,
        'XRayHighRateEfficiency_max_allowed_loweff_A_Rate1':98,
        'XRayHighRateEfficiency_max_allowed_loweff_A_Rate2':98,
        'XRayHighRateEfficiency_max_allowed_loweff_B_Rate1':95,
        'XRayHighRateEfficiency_max_allowed_loweff_B_Rate2':95,
        'XRayHighRateEfficiency_max_bad_pixels_per_double_column':79,
        'XRayHighRateEfficiency_max_bad_pixels_cut_sigma':10,
        'XRayHighRateEfficiency_max_bad_pixels_cut_max':0.5,
        'XRayHighRateEfficiency_max_bad_pixels_cut_min':0.2,
        'XRayHighRateEfficiency_min_fiducial_dc_eff':0.85,
        'XRayHighRateEfficiency_min_edge_dc_eff':0.75,
        'XRayHighRateHotPixels_max_allowed_hot':100,
        'XRayHighRateHotPixels_Threshold':1,
        'XRayHighRate_factor_dcol_uniformity_low':0.5,
        'XRayHighRate_factor_dcol_uniformity_high':1.5,
        'XRayHighRate_factor_readout_uniformity':7,
        'XRayHighRate_SCurve_Noise_Threshold_B':300,
        'XRayHighRate_SCurve_Noise_Threshold_C':400,
        'XRayHighRate_missing_xray_pixels_B':42,
        'XRayHighRate_missing_xray_pixels_C':168,
        'XRayHighRate_pixel_defects_B':42,
        'XRayHighRate_pixel_defects_C':168,
        'OnShellQuickTest_LeakageCurrent_B': 2.0,
        'OnShellQuickTest_LeakageCurrent_C': 10.0
    }
    XRayHRQualificationConfiguration = {
        'OmitGradesInFinalGrading':'',
        'TimeConstant':1,
        'Area':1,
    }

    # Database connection
    GlobalDBConnection = None
    GlobalDBConnectionCursor = None

    # Database connection
    LocalDBConnection = None
    LocalDBConnectionCursor = None

    # Path to the test results
    ModuleDataDirectory = ''

    # path to folder with all test results
    GlobalDataDirectory = ''

    TestResultHTMLTemplate = ''

    TestResultStylesheetPath = ''

    # Path to temporary folder
    TempPath = '/tmp'

    # Path to the SQLite Database File for storing the test result
    SQLiteDBPath = ''

    # Path to the Overview
    GlobalOverviewPath = ''

    LastUniqueIDCounter = 0

    MoReWebVersion = 'MoReWeb v1.0.0'
    MoReWebBranch = 'unknown branch'

    IVCurveFiles = {}

    #Error Handling
    ErrorList = []
    ModulesAnalyzed = []
    ModulesInsertedIntoDB = []

    def __init__(self, Configuration = None):
        if Configuration:
            self.Configuration['Database'] = {
                'UseGlobal':int(Configuration.get('SystemConfiguration', 'UseGlobalDatabase')),
                'Type':Configuration.get('SystemConfiguration', 'DatabaseType'),
                'Host':Configuration.get('SystemConfiguration', 'DatabaseHost'),
                'User':Configuration.get('SystemConfiguration', 'DatabaseUser'),
                'Password':Configuration.get('SystemConfiguration', 'DatabasePassword'),
                'DatabaseName':Configuration.get('SystemConfiguration', 'DatabaseName'),
            }
            refit = True
            if Configuration.has_option('Fitting','refit'):
                refit = Configuration.getboolean('Fitting','refit')
            self.Configuration['Fitting'] = {
                'refit': refit
            }
            self.Configuration['GzipSVG'] = int(Configuration.get('SystemConfiguration', 'GzipSVG'))
            self.Configuration['DefaultImageFormat'] = Configuration.get('SystemConfiguration', 'DefaultImageFormat')
            self.Configuration['RequiredTestTypesForComplete'] = Configuration.get('ProductionOverview', 'RequiredTestTypesForComplete')
            try:
                self.Configuration['IgnoreInSelectionList'] = Configuration.get('ProductionOverview', 'IgnoreInSelectionList')
            except:
                self.Configuration['IgnoreInSelectionList'] = ''

            self.Configuration['QualificationOverviewSort'] = Configuration.get('SystemConfiguration', 'QualificationOverviewSort')

            for i in self.GradingParameters:
                self.GradingParameters[i] = float(Configuration.get('GradingParameters', i))
            if Configuration.has_option('XRayHRQualification','OmitGradesInFinalGrading'):
                self.XRayHRQualificationConfiguration['OmitGradesInFinalGrading'] = [x.strip() for x in Configuration.get('XRayHRQualification','OmitGradesInFinalGrading').split(',')]
            if Configuration.has_option('XRayHRQualification','TimeConstant'):
                self.XRayHRQualificationConfiguration['TimeConstant'] = float(Configuration.get('XRayHRQualification','TimeConstant').strip())
            if Configuration.has_option('XRayHRQualification','Area'):
                self.XRayHRQualificationConfiguration['Area'] = float(Configuration.get('XRayHRQualification','Area').strip())

        self.MainStylesheet = open('HTML/Main.css').read()

        self.TestResultHTMLTemplate = open('HTML/TestResult/TestResultTemplate.html').read()
        self.TestResultStylesheet = open('HTML/TestResult/TestResultTemplate.css').read()

        self.OverviewHTMLTemplate = open('HTML/Overview/OverviewTemplate.html').read()
        self.OverviewStylesheet = open('HTML/Overview/OverviewTemplate.css').read()
        self.ProductionOverviewHTMLTemplate = open('HTML/ProductionOverview/OverviewTemplate.html').read()
        self.ProductionOverviewTableHTMLTemplate = open('HTML/ProductionOverview/Table.html').read()
        self.ProductionOverviewPlotHTMLTemplate = open('HTML/ProductionOverview/Plot.html').read()
        self.ProductionOverviewStylesheet = open('HTML/ProductionOverview/OverviewTemplate.css').read()
        self.HtmlParser = Helper.HtmlParser.HtmlParser()

        ROOT.gEnv.GetValue("Canvas.SavePrecision", -1)
        ROOT.gEnv.SetValue('Canvas.SavePrecision', "30")
        self.Canvas = ROOT.TCanvas()#'c1', '', 900, 700

        # Prevent garbage collection
        ROOT.SetOwnership(self.Canvas,False)

    def OpenDBConnection(self):
        if self.Configuration['Database']['UseGlobal']:
            import MySQLdb
            try:
                self.GlobalDBConnection = MySQLdb.connect(self.Configuration['Database']['Host'], self.Configuration['Database']['User'], self.Configuration['Database']['Password'], self.Configuration['Database']['DatabaseName'])
                self.GlobalDBConnectionCursor = GlobalDBConnection.cursor()
            except:
                self.GlobalDBConnection = None;
        else:
            CreateDBStructure = False
            import sqlite3
            if not os.path.exists(self.SQLiteDBPath):
                Head, Tail = os.path.split(self.SQLiteDBPath)
                if not os.path.exists(Head):
                    os.makedirs(Head)

                f = open(self.SQLiteDBPath, 'w')
                f.close()
                CreateDBStructure = True

            self.LocalDBConnection = sqlite3.connect(self.SQLiteDBPath)
            self.LocalDBConnection.row_factory = sqlite3.Row
            self.LocalDBConnectionCursor =  self.LocalDBConnection.cursor()
            self.LocalDBConnection.text_factory = str

            if CreateDBStructure:
                self.LocalDBConnectionCursor.executescript('''
                     CREATE TABLE ModuleTestResults(
                        ModuleID TEXT,
                        TestDate INT,
                        TestType TEXT,
                        QualificationType TEXT,
                        Grade TEXT,
                        PixelDefects TEXT,
                        ROCsLessThanOnePercent INT,
                        ROCsMoreThanOnePercent INT,
                        ROCsMoreThanFourPercent INT,
                        Noise INT,
                        Trimming INT,
                        PHCalibration INT,
                        CurrentAtVoltage150V FLOAT,
                        RecalculatedVoltage FLOAT,
                        IVSlope FLOAT,
                        Temperature TEXT,
                        RelativeModuleFinalResultsPath TEXT,
                        FulltestSubfolder TEXT,
                        initialCurrent FLOAT,
                        Comments TEXT,
                        nCycles INT,
                        CycleTempLow FLOAT,
                        CycleTempHigh FLOAT
                    );
                ''')


    def GetUniqueID(self, Prefix = ''):
        self.LastUniqueIDCounter += 1
        return Prefix + '_' + str(self.LastUniqueIDCounter)

    def FetchOneAssoc(cursor) :
        data = cursor.fetchone()
        if data == None :
            return None
        desc = cursor.description

        retDict = {}

        for (name, value) in zip(desc, data) :
            retDict[name[0]] = value

        return retDict

    def __del__(self):
        if self.Configuration['Database']['UseGlobal']:
            pass
        else:
            self.LocalDBConnection.close()

    def existInDB(self,moduleID,QualificationType,TestDate=None):
        print 'check whether module %s with QualificationType %s exists in DB: '%(moduleID,QualificationType)
        AdditionalWhere =""
        AdditionalWhere += ' AND ModuleID=:ModuleID '
        AdditionalWhere += ' AND QualificationType=:QualificationType '
        AdditionalParameters = {
                    'ModuleID':moduleID,
                    'QualificationType':QualificationType
                    }
        if TestDate:
            AdditionalWhere += ' AND TestDate>=:TestDate '
            AdditionalParameters['TestDate'] = TestDate

        if self.LocalDBConnectionCursor:
            self.LocalDBConnectionCursor.execute(
                'SELECT * FROM ModuleTestResults '+
                'WHERE 1=1 '+
                AdditionalWhere+
                'ORDER BY ModuleID ASC,TestType ASC, TestDate ASC ',
                AdditionalParameters
            )
            Rows = self.LocalDBConnectionCursor.fetchall()
            return len(Rows)>0
        return False

