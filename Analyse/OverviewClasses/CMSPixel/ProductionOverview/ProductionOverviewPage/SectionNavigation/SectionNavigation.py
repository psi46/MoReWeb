import ROOT
import AbstractClasses
import glob
import json

class ProductionOverview(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def CustomInit(self):
        self.NameSingle='Section'
    	self.Name='CMSPixel_ProductionOverview_%s'%self.NameSingle
        self.Title = ''
        self.DisplayOptions = {
            'Width': 1,
        }
        self.SubPages = []
        self.SavePlotFile = False

    def GenerateOverview(self):
        HTML = "<b>Navigation: </b>"
        for Anchor in self.Attributes['Sections']:
            HTML += "<a href='#{Anchor}' style='margin-right:5px;'>{Anchor}</a> ".format(Anchor=Anchor)

        HTML += "<div style='clear: both; width: 100%; margin-bottom: 5px; height: 2px; background-color: #BBC;'></div>"


        return HTML


