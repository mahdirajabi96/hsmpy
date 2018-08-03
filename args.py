import os
import arcpy
class inp(object):
    def __init__(self):
        self.tolerance   = 500
        self.subsetEntries = 10000

        self.scratch  = os.path.abspath('C:\Users\Mahdi\Downloads\Scratch')
        if not os.path.exists(self.scratch):
            os.makedirs(self.scratch)
        self.download    = os.path.join(self.scratch,'Download')
        if not os.path.exists(self.download):
            os.makedirs(self.download)
        self.Box      = os.path.abspath('C:\Users\Mahdi\Box Sync')
        self.hsmpy    = os.path.join(self.Box,'SC Data\Python Tools')

        self.JUR     = os.path.join(self.Box,'SC Data\SC Crashes\Documents\Jurisdictions.mdb\Jurisdiction')
        self.locdir  = os.path.join(self.Box,'SC Data\SC Crashes\Text Files\Loc')
        self.unitdir = os.path.join(self.Box,'SC Data\SC Crashes\Text Files\Unit')
        self.occdir  = os.path.join(self.Box,'SC Data\SC Crashes\Text Files\Occ')
        self.locYears  = range(2004,2016)
        self.unitYears = range(2007,2016)
        self.occYears  = range(2007,2016)
        self.setCrash()#.locdir,self.unitdir,self.occdir,self.locYears,self.unitYears,self.occYears)

        self.STATE       = os.path.join(self.Box,'SC Data\SC Boundaries\SC Boundaries.gdb\SC_State')
        self.COUNTY      = os.path.join(self.Box,'SC Data\SC Boundaries\SC Boundaries.gdb\SC_Counties')
        self.DEM         = os.path.join(self.Box,'SC Data\SC Digital Elevation Model\statewidedem.rrd')
        self.RIMS        = os.path.join(self.Box,'SC Data\SC Roadways\RIMS.mdb\RIMS')
        self.HIGHWAYS    = os.path.join(self.Box,'SC Data\SC Roadways\HIGHWAYS.mdb\Highways')
        self.OTHERS      = os.path.join(self.Box,'SC Data\SC Roadways\OTHERS.mdb\Others')
        self.BRIDGES     = os.path.join(self.Box,'SC Data\SC Roadways\BRIDGES.mdb\SC_Bridges')
        self.RAILROAD    = os.path.join(self.Box,'SC Data\SC Roadways\RailRoads.mdb\RailRoad')
    def setCrash(self):#,locdir,unitdir,occdir,locYears,unitYears,occYears):
        self.loc = {y:os.path.join(self.locdir ,'SC_Crash_{}_Loc.txt'.format(y))  for y in self.locYears}
        self.unit = {y:os.path.join(self.unitdir,'SC_Crash_{}_Unit.txt'.format(y)) for y in self.unitYears}
        self.occ = {y:os.path.join(self.occdir ,'SC_Crash_{}_Occ.txt'.format(y))  for y in self.occYears}
class out(object):
    def __init__(self,inp):
        self.MedType = 'MedType'
        self.MedWid  = 'MedWid'
        self.Lanes   = 'Lanes'
        self.LaneWid = 'LaneWid'
        self.SurWid  = 'SurWid'
        self.ShWid   = 'ShWid'
        self.ShTrt   = 'ShTrt'
        self.Curb    = 'Curb'
        self.SwTrt   = 'SwTrt'
        self.Other   = 'Other'
        self.RailRoad= 'RailRoadCrossing'
        self.Bridges = 'Bridges'

        self.gdbpath   = inp.scratch
        self.locgdbname   = 'Loc.gdb'
        self.unitgdbname  = 'Unit.gdb'
        self.occgdbname   = 'Occ.gdb'
        self.routegdbname = 'Route.gdb'
        self.locgdb       = os.path.join(self.gdbpath, self.locgdbname)
        self.unitgdb      = os.path.join(self.gdbpath, self.unitgdbname)
        self.occgdb       = os.path.join(self.gdbpath, self.occgdbname)
        self.routegdb     = os.path.join(self.gdbpath, self.routegdbname)
        self.route    = self.routegdb + '\\Routes'
        self.highways = self.routegdb + '\\Highways'
        self.others   = self.routegdb + '\\Others'
        self.loc  = {y:self.locgdb   + '\\Loc'   + str(y) for y in inp.locYears}
        self.unit = {y:self.unitgdb  + '\\Unit'  + str(y) for y in inp.unitYears}
        self.occ  = {y:self.occgdb   + '\\Occ'   + str(y) for y in inp.occYears}
        self.createOutput()
    def createGDB(self,gdb,path,name):
        if not os.path.exists(gdb):
            arcpy.CreateFileGDB_management(path,name)
    def createOutput(self):
        self.createGDB(self.locgdb  ,self.gdbpath,self.locgdbname)
        self.createGDB(self.unitgdb ,self.gdbpath,self.unitgdbname)
        self.createGDB(self.occgdb  ,self.gdbpath,self.occgdbname)
        self.createGDB(self.routegdb,self.gdbpath,self.routegdbname)
class web(object):
    def __init__(self):
        self.HIGHWAYS    = "http://info.scdot.org/sites/GIS/GISMapdl/Statewide_Highways.zip"
        self.OTHERS      = "http://info.scdot.org/sites/GIS/GISMapdl/Statewide_Other_Roads.zip"
        self.BRIDGES     = "http://info.scdot.org/sites/GIS/GISMapdl/Statewide_Bridges.zip"
        self.RAILROAD    = "http://info.scdot.org/sites/GIS/GISMapdl/Statewide_Railroads.zip"
        self.DEM         = "ftp://ftpdata.dnr.sc.gov/gisdata/dnrdata/statedem.zip"
        self.STATE       = "ftp://ftp2.census.gov/geo/tiger/TIGER2017/STATE/tl_2017_us_state.zip"
        self.COUNTY      = "ftp://ftp2.census.gov/geo/tiger/TIGER2017/COUNTY/tl_2017_us_county.zip"
        self.TRACTS      = "ftp://ftp2.census.gov/geo/tiger/TIGER2017/TTRACT/tl_2017_us_ttract.zip"
        self.BLOCKGROUP  = "ftp://ftp2.census.gov/geo/tiger/TIGER2017/BG/tl_2017_45_bg.zip"
        self.BLOCKS      = "ftp://ftp2.census.gov/geo/tiger/TIGER2017/TABBLOCK/tl_2017_45_tabblock10.zip"
