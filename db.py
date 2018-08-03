import arcpy
import args
import common
import os
import fields
class scdb(object):
    def __init__(self,path,name):
        # GDB:
        self.gdbpath = path
        self.gdbname = name
        self.gdb = self.gdbpath + '\\' + self.gdbname
        i = 1
        while os.path.exists(self.gdb):
            self.gdbname = name[:-4] + str(i) + '.gdb'
            self.gdb = self.gdbpath + '\\' + self.gdbname
            i += 1
        
        # Network Dataset:
        self.route   = 'Routes'
        self.routeFC = self.gdb + '\\' + self.route

        self.MedType = 'R_MedType'
        self.MedWid  = 'R_MedWid'
        self.Lanes   = 'R_Lanes'
        self.LaneWid = 'R_LaneWid'
        self.SurWid  = 'R_SurWid'
        self.ShWid   = 'R_ShWid'
        self.ShTrt   = 'R_ShTrt'
        self.Curb    = 'R_Curb'
        self.SwTrt   = 'R_SwTrt'
        self.Other   = 'R_Other'
        self.RailC   = 'R_RailCross'
        self.Bridges = 'R_Bridges'

        self.MedTypeFC = self.gdb + '\\' + self.MedType
        self.MedWidFC  = self.gdb + '\\' + self.MedWid
        self.LanesFC   = self.gdb + '\\' + self.Lanes
        self.LaneWidFC = self.gdb + '\\' + self.LaneWid
        self.SurWidFC  = self.gdb + '\\' + self.SurWid
        self.ShWidFC   = self.gdb + '\\' + self.ShWid
        self.ShTrtFC   = self.gdb + '\\' + self.ShTrt
        self.CurbFC    = self.gdb + '\\' + self.Curb
        self.SwTrtFC   = self.gdb + '\\' + self.SwTrt
        self.OtherFC   = self.gdb + '\\' + self.Other
        self.RailCFC   = self.gdb + '\\' + self.RailC
        self.BridgesFC = self.gdb + '\\' + self.Bridges

        # Crash Dataset:
        self.loc  = 'Loc'
        self.unit = 'Unit'
        self.occ  = 'Occ'
        
        # Counties:
        self.county = 'County'
        self.countyFC = self.gdb + '\\' + self.county

        # Jurisdiction
        self.jur = 'Jurisdiction'
        self.jurFC = self.gdb + '\\' + self.jur

        self.CreateGDB()
    def CreateGDB(self):
        #
        arcpy.CreateFileGDB_management(self.gdbpath,self.gdbname)
    def AddCounty(self,county):
        #
        arcpy.FeatureClassToFeatureClass_conversion(county, self.gdb, self.county)
    def AddJur(self,jur):
        #
        arcpy.FeatureClassToFeatureClass_conversion(jur, self.gdb, self.jur)
    def AddRoutes(self,routes):
        #
        arcpy.FeatureClassToFeatureClass_conversion(routes, self.gdb, self.route)
    def AddMedTyp(self,AttrTab):
        #
        arcpy.TableToTable_conversion(AttrTab, self.gdb, self.MedType)
    def AddMedWid(self,AttrTab):
        #
        arcpy.TableToTable_conversion(AttrTab, self.gdb, self.MedWid)
    def AddLanes(self,AttrTab):
        #
        arcpy.TableToTable_conversion(AttrTab, self.gdb, self.Lanes)
    def AddLaneWid(self,AttrTab):
        #
        arcpy.TableToTable_conversion(AttrTab, self.gdb, self.LaneWid)
    def AddSurWid(self,AttrTab):
        #
        arcpy.TableToTable_conversion(AttrTab, self.gdb, self.SurWid)
    def AddShWid(self,AttrTab):
        #
        arcpy.TableToTable_conversion(AttrTab, self.gdb, self.ShWid)
    def AddShTrt(self,AttrTab):
        #
        arcpy.TableToTable_conversion(AttrTab, self.gdb, self.ShTrt)
    def AddCurb(self,AttrTab):
        #
        arcpy.TableToTable_conversion(AttrTab, self.gdb, self.Curb)
    def AddSwTrt(self,AttrTab):
        #
        arcpy.TableToTable_conversion(AttrTab, self.gdb, self.SwTrt)
    def AddOther(self,AttrTab):
        #
        arcpy.TableToTable_conversion(AttrTab, self.gdb, self.Other)
    def AddRailCross(self,RailCross):
        #
        arcpy.FeatureClassToFeatureClass_conversion(RailCross, self.gdb, self.RailC)
    def AddLoc(self,Loc,Year):
        #
        arcpy.FeatureClassToFeatureClass_conversion(Loc, self.gdb, self.loc + str(Year))
    def AddUnit(self,Unit,Year):
        #
        arcpy.TableToTable_conversion(Unit, self.gdb, self.unit + str(Year))
    def AddOcc(self,Occ,Year):
        #
        arcpy.TableToTable_conversion(Occ, self.gdb, self.occ + str(Year))
    def AddDomains(self):
        ListDomains = [getattr(fields.domains,domain) for domain in dir(fields.domains) if not domain[0:2] == '__']
        for domain in ListDomains:
            print(domain['name'])
            arcpy.CreateDomain_management(self.gdb, domain['name'], domain['alias'], domain['type'], "CODED")
            for code in domain['codes'].keys():
                arcpy.AddCodedValueToDomain_management(self.gdb, domain['name'], code, domain['codes'][code])
    def AssignDomain(self,FC,FieldClass):
        for field in arcpy.ListFields(FC):
            if hasattr(FieldClass,field.name):
                attr = getattr(FieldClass,field.name)
                if attr['domain']<>None:
                    arcpy.AssignDomainToField_management(FC, attr['name'], attr['domain']['name'])
    def AddRelationships(self,locyears,unityears,occyears):
        # Route - County
        arcpy.CreateRelationshipClass_management(self.countyFC,self.routeFC,self.gdb+'\\Coun_Route',
            "SIMPLE","Route","County","NONE","ONE_TO_MANY","NONE",fields.route.County['name'],fields.route.County['name'])
        # Route - Attributes
        arcpy.CreateRelationshipClass_management(self.routeFC,self.CurbFC,self.gdb+'\\Route_Curb',
            "SIMPLE","Curb","Route","NONE","ONE_TO_MANY","NONE",fields.route.Route_LRS['name'],fields.route.Route_LRS['name'])
        arcpy.CreateRelationshipClass_management(self.routeFC,self.LanesFC,self.gdb+'\\Route_Lane',
            "SIMPLE","Lane","Route","NONE","ONE_TO_MANY","NONE",fields.route.Route_LRS['name'],fields.route.Route_LRS['name'])
        arcpy.CreateRelationshipClass_management(self.routeFC,self.LaneWidFC,self.gdb+'\\Route_LaneWid',
            "SIMPLE","LaneWid","Route","NONE","ONE_TO_MANY","NONE",fields.route.Route_LRS['name'],fields.route.Route_LRS['name'])
        arcpy.CreateRelationshipClass_management(self.routeFC,self.MedTypeFC,self.gdb+'\\Route_MedType',
            "SIMPLE","MedTyp","Route","NONE","ONE_TO_MANY","NONE",fields.route.Route_LRS['name'],fields.route.Route_LRS['name'])
        arcpy.CreateRelationshipClass_management(self.routeFC,self.MedWidFC,self.gdb+'\\Route_MedWid',
            "SIMPLE","MedWid","Route","NONE","ONE_TO_MANY","NONE",fields.route.Route_LRS['name'],fields.route.Route_LRS['name'])
        arcpy.CreateRelationshipClass_management(self.routeFC,self.OtherFC,self.gdb+'\\Route_Other',
            "SIMPLE","Other","Route","NONE","ONE_TO_MANY","NONE",fields.route.Route_LRS['name'],fields.route.Route_LRS['name'])
        arcpy.CreateRelationshipClass_management(self.routeFC,self.ShTrtFC,self.gdb+'\\Route_ShTrt',
            "SIMPLE","ShTrt","Route","NONE","ONE_TO_MANY","NONE",fields.route.Route_LRS['name'],fields.route.Route_LRS['name'])
        arcpy.CreateRelationshipClass_management(self.routeFC,self.ShWidFC,self.gdb+'\\Route_ShWid',
            "SIMPLE","ShWid","Route","NONE","ONE_TO_MANY","NONE",fields.route.Route_LRS['name'],fields.route.Route_LRS['name'])
        arcpy.CreateRelationshipClass_management(self.routeFC,self.SurWidFC,self.gdb+'\\Route_SurWid',
            "SIMPLE","SurWid","Route","NONE","ONE_TO_MANY","NONE",fields.route.Route_LRS['name'],fields.route.Route_LRS['name'])
        arcpy.CreateRelationshipClass_management(self.routeFC,self.SwTrtFC,self.gdb+'\\Route_SwTrt',
            "SIMPLE","SwTrt","Route","NONE","ONE_TO_MANY","NONE",fields.route.Route_LRS['name'],fields.route.Route_LRS['name'])
        arcpy.CreateRelationshipClass_management(self.routeFC,self.RailCFC,self.gdb+'\\Route_Rail',
            "SIMPLE","RailC","Route","NONE","ONE_TO_MANY","NONE",fields.route.Route_LRS['name'],fields.route.Route_LRS['name'])
        
        # Loc - County
        for y in locyears:
            arcpy.CreateRelationshipClass_management(self.countyFC,self.gdb+'\\'+self.loc+str(y),self.gdb+'\\Coun_Loc' + str(y),
                "SIMPLE","Loc" + str(y),"County","NONE","ONE_TO_MANY","NONE",fields.route.County['name'],fields.loc.CTY['name'])
        # Loc - Route
        for y in locyears:
            arcpy.CreateRelationshipClass_management(self.routeFC,self.gdb+'\\'+self.loc+str(y),self.gdb+'\\Route_Loc' + str(y),
                "SIMPLE","Loc" + str(y),"Route","NONE","ONE_TO_MANY","NONE",fields.route.Name['name'],fields.loc.MLRS['name'])
        # Loc - Jurisdiction
        for y in locyears:
            arcpy.CreateRelationshipClass_management(self.jurFC,self.gdb+'\\'+self.loc+str(y),self.gdb+'\\Jur_Loc' + str(y),
                "SIMPLE","Loc" + str(y),"Jur","NONE","ONE_TO_MANY","NONE",'JUR',fields.loc.JUR['name'])
        # Loc - Unit
        for y in list(set(locyears).intersection(unityears)):
            arcpy.CreateRelationshipClass_management(self.gdb+'\\'+self.loc+str(y),self.gdb+'\\'+self.unit+str(y),self.gdb+'\\Loc_Unit' + str(y),
                "SIMPLE","Unit","Loc","NONE","ONE_TO_MANY","NONE",fields.loc.ANO['name'],fields.loc.ANO['name'])
        # Unit - Occ
        for y in list(set(unityears).intersection(occyears)):
            arcpy.CreateRelationshipClass_management(self.gdb+'\\'+self.unit+str(y),self.gdb+'\\'+self.occ+str(y),self.gdb+'\\Unit_Occ' + str(y),
                "SIMPLE","Occ","Unit","NONE","ONE_TO_MANY","NONE",fields.unit.ID['name'],fields.unit.ID['name'])

