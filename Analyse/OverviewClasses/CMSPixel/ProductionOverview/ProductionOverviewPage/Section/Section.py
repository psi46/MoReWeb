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
        HTML = "<div style='clear: both; width: 100%; padding-top:2px; margin-bottom: 5px; height: 22px; border-top:2px solid #BBC;z-index:-1;'>"
        if self.Attributes.has_key('Title'):
            HTML += "<div style='float:left;'><h3>{Title}</h3></div>".format(Title=self.Attributes['Title'])
        HTML += "<div style='float:right;width:20px;height:20px;font-size:20px;'><a href='#PageTop'>&#x25b2;</a></div></div>"
        if self.Attributes.has_key('Anchor'):
            HTML += "<a class='anchor' name='{Anchor}'></a>".format(Anchor=self.Attributes['Anchor'])
        HTML += "<div style='clear:both;'></div>"

        return HTML


