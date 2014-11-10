import ROOT
import AbstractClasses.Helper.HistoGetter as HistoGetter
import AbstractClasses
import AbstractClasses.Helper.ROOTConfiguration as ROOTConfiguration
from TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Chips.Chip.PixelMap import PixelMap
import TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Chips.Chip.PixelMap
#import TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Chips.Chip.PixelMap.PixelMap as PixelMap

#import TestResultClasses
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        ROOTConfiguration.initialise_ROOT()
        self.Name='CMSPixel_QualificationGroup_BareModuleTest_Chips_Chip_PixelMapNew_TestResult'
        self.NameSingle='PixelMapNew'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_BareModuleTest_ROC'
        self.verbose = True
        self.DeadPixelList = set()
        self.Noisy1PixelList = set()
        self.MaskDefectList = set()
        self.IneffPixelList = set()
        self.chipNo = self.ParentObject.Attributes['ChipNo']

#    def PixelMapLocal(self):
#        return PixelMap.TestResult(self)


    def PopulateResultData(self):
        print 'Hola'
        #aPixelMap = PixelMap(self);
        aPixelMapRes = PixelMap.TestResult(self);
        PixelMap.TestResult.PopulateResultData(aPixelMap);
#(PixelMap(self))
        
#return PixelMap.TestResult.PopulateResultData(self)
        
#return PixelMap.TestResult.PopulateResultData(self,self.Name, self.NameSingle)
        
#return PixelMap.TestResult.PopulateResultData()
        
#bla = PixelMap.TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult)
        
#bla = PixelMap.TestResult(self.Name, self.NameSingle,self.Attributes,self.DeadPixelList,self.Noisy1PixelList,self.MaskDefectList,self.IneffPixelList,self.chipNo)
        
#return PixelMap.TestResult.PopulateResultData()
