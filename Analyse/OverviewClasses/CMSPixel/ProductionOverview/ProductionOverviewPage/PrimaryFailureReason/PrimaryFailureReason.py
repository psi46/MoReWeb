# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import array
import json

from AbstractClasses.Helper.SetEncoder import SetEncoder

class ProductionOverview(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def CustomInit(self):
        self.NameSingle = 'PrimaryFailureReason'
        self.Name = 'CMSPixel_ProductionOverview_%s'%self.NameSingle
        self.Title = 'Primary failure Reason'
        self.DisplayOptions = {
            'Width': 3,
        }
        if self.Attributes.has_key('Width'):
            self.DisplayOptions['Width'] = self.Attributes['Width']
        self.SubPages = []
        self.SavePlotFile = True
        self.Canvas.SetCanvasSize(800, 500)
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
        for k,v in self.ParentObject.SubtestResults.iteritems():
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
            'BumpBonding',
            'XrayDoubleColumnDefects',
            'XrayPixelDefects',
            'XrayEfficiency',
            'XrayPerformance',
            'Other']
        GradeCPrimaryReasons = {}
        for Reason in GradeCPrimaryReasonsList:
            GradeCPrimaryReasons[Reason] = []

        print "Grade C modules:", GradeCModules

        # now check for all grade C modules if they are in the list of ModuleFailuresOverview
        for ModuleID in GradeCModules:

            if ModuleID in DefectsDict:

                ModuleDefectGrades = DefectsDict[ModuleID]
                # check for primary reasons in given order

                HasUserSpecifiedDefects = False
                UserSpecifiedDefect = ''
                for k,v in ModuleDefectGrades.iteritems():
                    if k.upper().startswith('DEFECT_'):
                        HasUserSpecifiedDefects = True
                        # treat HDI defect with lower priority than other user specified defects
                        if UserSpecifiedDefect == '' or UserSpecifiedDefect.upper() == 'HDI':
                            UserSpecifiedDefect = '_'.join(k.split('_')[1:])
                        print "---->",UserSpecifiedDefect

                if type(UserSpecifiedDefect) == unicode:
                    UserSpecifiedDefect = UserSpecifiedDefect.encode('utf8')

                # user specified defects (via defects.txt) first!
                if HasUserSpecifiedDefects:
                    if UserSpecifiedDefect in GradeCPrimaryReasons:
                        GradeCPrimaryReasons[UserSpecifiedDefect].append(ModuleID)
                    else:
                        GradeCPrimaryReasons[UserSpecifiedDefect] = [ModuleID]
                # then manual grading
                elif self.TestFailed(ModuleDefectGrades['ManualGradeFT']) or self.TestFailed(ModuleDefectGrades['ManualGradeHR']):
                    GradeCPrimaryReasons['ManualGrading'].append(ModuleID)
                # leakage current
                elif self.TestFailed(ModuleDefectGrades['LCStartup']):
                    GradeCPrimaryReasons['LeakageCurrentPON'].append(ModuleID)
                elif self.TestFailed(ModuleDefectGrades['IV150']):
                    GradeCPrimaryReasons['LeakageCurrentFQ'].append(ModuleID)
                # dead ROCs
                elif self.TestFailed(ModuleDefectGrades['DeadROC']):
                    GradeCPrimaryReasons['DeadROC'].append(ModuleID)
                # Bump Bonding Defects
                elif self.TestFailed(ModuleDefectGrades['BB_Fulltest']) or self.TestFailed(ModuleDefectGrades['BB_X-ray']):
                    GradeCPrimaryReasons['BumpBonding'].append(ModuleID)
                # Other pixel Defects
                elif self.TestFailed(ModuleDefectGrades['TotalDefects']):
                    GradeCPrimaryReasons['FulltestPixelDefects'].append(ModuleID)
                elif self.TestFailed(ModuleDefectGrades['GradeFT']):
                    GradeCPrimaryReasons['FulltestPerformance'].append(ModuleID)
                # Double column defects
                elif self.TestFailed(ModuleDefectGrades['DoubleColumn']) or self.TestFailed(ModuleDefectGrades['UniformityProblems']):
                    GradeCPrimaryReasons['XrayDoubleColumnDefects'].append(ModuleID)
                elif self.TestFailed(ModuleDefectGrades['TotalDefects_X-ray']):
                    GradeCPrimaryReasons['XrayPixelDefects'].append(ModuleID)
                # efficiency
                elif self.TestFailed(ModuleDefectGrades['lowHREfficiency']):
                    GradeCPrimaryReasons['XrayEfficiency'].append(ModuleID)
                elif self.TestFailed(ModuleDefectGrades['GradeHR']):
                    GradeCPrimaryReasons['XrayPerformance'].append(ModuleID)
                else:
                    # otherwise add it to 'Other' category
                    GradeCPrimaryReasons['Other'].append(ModuleID)

            else:
                # otherwise add it to 'Other' category
                GradeCPrimaryReasons['Other'].append(ModuleID)

        # save defects dictionary as json file
        JsonFileName = ''
        try:
            JsonFileName = self.GlobalOverviewPath+'/'+self.Attributes['BasePath'] + '/KeyValueDictPairs.json'
            f = open(JsonFileName, 'w')
            f.write(json.dumps(GradeCPrimaryReasons, sort_keys=True, indent=4, separators=(',', ': '), cls=SetEncoder))
            f.close()
            print "    -> written to %s"%JsonFileName
        except:
            print "could not write json file: '%s'!"%JsonFileName

        print GradeCPrimaryReasons

        PieChartValsList = []
        PieChartLabelsList = []

        for Reason,v in GradeCPrimaryReasons.iteritems():
            if len(GradeCPrimaryReasons[Reason]) > 0:
                PieChartValsList.append(len(GradeCPrimaryReasons[Reason]))
                PieChartLabelsList.append(Reason)

        PieChartValsArray = array.array('d', PieChartValsList)
        ColorsArray = array.array('i', [2,3,4,5,6,7,9,40,41,42,38,28,49,36,29,12,21,46,16,17,18,19,11,10,13,14,15,20,21,22,23,24])
        PieChartLabelsArray = [ array.array( 'c', '%s\0'%x ) for x in PieChartLabelsList ]
        LabelsInTheUglyWayPyRootNeedsThem = array.array('l', map(lambda x: x.buffer_info()[0], PieChartLabelsArray))

        self.Canvas.Clear()
        try:
            PieChart = ROOT.TPie(self.GetUniqueID(), "Primary failure reason", len(PieChartValsList), PieChartValsArray, ColorsArray, LabelsInTheUglyWayPyRootNeedsThem)
            PieChart.SetLabelFormat("%val")
            PieChart.Draw("3d nol <")
            PieChart.MakeLegend(0.8, 0.65, 1.0, 0.95)
        except:
            pass
        self.SaveCanvas()
        ImageHTML = self.Boxed(self.Image(self.Attributes['ImageFile']))

        TextHTML = "<div style='height:20px;'></div>"

        # list all modules with certain defects

        # user specified defect (via defects.txt)
        for k,v in GradeCPrimaryReasons.iteritems():
            # check if it is a user specified defect which has priority!
            if k not in GradeCPrimaryReasonsList:
                TextHTML += "<b>%s (%d)</b>:<br>%s<br><br>"%(k, len(v), ', '.join(v))

        # all other defects
        for k in GradeCPrimaryReasonsList:
            if k in GradeCPrimaryReasons and len(GradeCPrimaryReasons[k]) > 0:
                v = GradeCPrimaryReasons[k]
                TextHTML += "<b>%s (%d)</b>:<br>%s<br><br>"%(k, len(v), ', '.join(v))

        HTML = "<div>%s<div><div style='float:left;width:400px;'>%s</div>"%(ImageHTML, TextHTML)

        AbstractClasses.GeneralProductionOverview.GeneralProductionOverview.GenerateOverview(self)

        self.DisplayErrorsList()
        return HTML
