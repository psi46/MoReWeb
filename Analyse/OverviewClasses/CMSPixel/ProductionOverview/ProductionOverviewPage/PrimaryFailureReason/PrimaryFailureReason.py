# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import array

class ProductionOverview(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def CustomInit(self):
        self.NameSingle = 'PrimaryFailureReason'
        self.Name = 'CMSPixel_ProductionOverview_%s'%self.NameSingle
        self.Title = 'Primary failure Reason'
        self.DisplayOptions = {
            'Width': 2,
        }
        if self.Attributes.has_key('Width'):
            self.DisplayOptions['Width'] = self.Attributes['Width']
        self.SubPages = []
        self.SavePlotFile = True
        self.Canvas.SetCanvasSize(500, 500)
        self.Canvas.SetFrameLineStyle(0)
        self.Canvas.SetFrameLineWidth(1)
        self.Canvas.SetFrameBorderMode(0)
        self.Canvas.SetFrameBorderSize(1)
        self.Canvas.Update()

    def TestFailed(self, Failures):
        Failed = False
        if type(Failures) == dict:
            for k,v in Failures.iteritems():
                if v == 'C':
                    Failed=True
        else:
            if Failures == 'C':
                    Failed=True
        return Failed


    def GenerateOverview(self):

        # get all defects from ModuleFailuresOverview table
        DefectsDict = {}
        for k,v in  self.ParentObject.SubtestResults.iteritems():
            if k.startswith('ModuleFailuresOverview'):
                try:
                    DefectsDict.update(v['HiddenData']['DefectsDict'])
                except:
                    pass

        # find all grade C modules
        GradeCModules = []
        Rows = self.FetchData()
        ModuleIDsList = self.GetModuleIDsList(Rows)
        for ModuleID in ModuleIDsList:
            if self.ModuleQualificationIsComplete(ModuleID, Rows):
                FinalGrade = self.GetFinalGrade(ModuleID, Rows)
                if FinalGrade == 'C':
                    GradeCModules.append(ModuleID)

        # define order of primary reasons and initialize dictionary
        GradeCPrimaryReasonsList = [
            'ManualGrading',
            'LeakageCurrentPON',
            'LeakageCurrentFQ',
            'NotProgrammable',
            'BadHDI',
            'DeadROC',
            'FulltestPixelDefects',
            'FulltestPerformance',
            'XrayDoubleColumnDefects',
            'XrayPixelDefects',
            'XrayEfficiency',
            'XrayPerformance',
            'Other']
        GradeCPrimaryReasons = {}
        for Reason in GradeCPrimaryReasonsList:
            GradeCPrimaryReasons[Reason] = 0

        print "Grade C modules:",GradeCModules

        # now check for all grade C modules if they are in the list of ModuleFailuresOverview
        for ModuleID in GradeCModules:

            if ModuleID in DefectsDict:

                ModuleDefectGrades = DefectsDict[ModuleID]
                # check for primary reasons in given order, manual grading first!

                if self.TestFailed(ModuleDefectGrades['ManualGradeFT']) or self.TestFailed(ModuleDefectGrades['ManualGradeHR']):
                    GradeCPrimaryReasons['ManualGrading'] += 1
                elif self.TestFailed(ModuleDefectGrades['LCStartup']):
                    GradeCPrimaryReasons['LeakageCurrentPON'] += 1
                elif self.TestFailed(ModuleDefectGrades['IV150']):
                    GradeCPrimaryReasons['LeakageCurrentFQ'] += 1
                elif self.TestFailed(ModuleDefectGrades['DeadROC']):
                    GradeCPrimaryReasons['DeadROC'] += 1
                elif self.TestFailed(ModuleDefectGrades['TotalDefects']):
                    GradeCPrimaryReasons['FulltestPixelDefects'] += 1
                elif self.TestFailed(ModuleDefectGrades['GradeFT']):
                    GradeCPrimaryReasons['FulltestPerformance'] += 1
                elif self.TestFailed(ModuleDefectGrades['DoubleColumn']) or self.TestFailed(ModuleDefectGrades['UniformityProblems']):
                    GradeCPrimaryReasons['XrayDoubleColumnDefects'] += 1
                elif self.TestFailed(ModuleDefectGrades['TotalDefects_X-ray']):
                    GradeCPrimaryReasons['XrayPixelDefects'] += 1
                elif self.TestFailed(ModuleDefectGrades['lowHREfficiency']):
                    GradeCPrimaryReasons['XrayEfficiency'] += 1
                elif self.TestFailed(ModuleDefectGrades['GradeHR']):
                    GradeCPrimaryReasons['XrayPerformance'] += 1
                else:
                    # otherwise add it to 'Other' category
                    GradeCPrimaryReasons['Other'] += 1

            else:
                # otherwise add it to 'Other' category
                GradeCPrimaryReasons['Other'] += 1

        print GradeCPrimaryReasons

        PieChartValsList = []
        PieChartLabelsList = []
        PieChartColorsList = []

        for Reason in GradeCPrimaryReasonsList:
            if GradeCPrimaryReasons[Reason] > 0:
                PieChartValsList.append(GradeCPrimaryReasons[Reason])
                PieChartLabelsList.append(Reason)

        PieChartValsArray = array.array('d', PieChartValsList)
        ColorsArray = array.array('i',[2,3,4,5,6,7,8,9,10,11,12,13,14,15])
        PieChartLabelsArray = [ array.array( 'c', '%s\0'%x ) for x in PieChartLabelsList ]
        LabelsInTheUglyWayPyRootNeedsThem = array.array( 'l', map( lambda x: x.buffer_info()[0], PieChartLabelsArray ) )

        PieChart = ROOT.TPie(self.GetUniqueID(), "TEST! still work in progress!", len(PieChartValsList), PieChartValsArray, ColorsArray, LabelsInTheUglyWayPyRootNeedsThem)
        PieChart.SetLabelFormat("%val")
        PieChart.Draw("3d nol")

        Legend = PieChart.MakeLegend(0.8,0.65,1.0,0.95)
        self.SaveCanvas()
        HTML = self.Image(self.Attributes['ImageFile'])

        AbstractClasses.GeneralProductionOverview.GeneralProductionOverview.GenerateOverview(self)

        self.DisplayErrorsList()
        return self.Boxed(HTML)
