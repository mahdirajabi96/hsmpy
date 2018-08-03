import arcpy
import sys
import os

CoordSystemSC   = arcpy.SpatialReference(102733)
CoordSystemNC   = arcpy.SpatialReference(2264)
RunLimit      = 50

#   Fields Dictionary
##  Facility Types
FRTypes= ['U4F', 'U6F', 'R4F']
RTypes = ['R2U', 'R4U', 'R4D', 'U2U', 'U3T', 'U4D', 'U4U', 'U5T']
ITypes = ['R3ST' ,'R4ST' , 'R4SG', 'RM3ST', 'RM4ST', 'RM4SG', 'U3ST', 'U4ST', 'U3SG', 'U4SG']
FTypes = RTypes + ITypes + FRTypes

#  Arcpy Functions
## First Group of Classes
def CreateFeatureclass(outLayer, Dic = {'geometry_type':'POINT','has_m':'ENABLED','has_z':'ENABLED'}):
    OutDic = OutputParser(outLayer, 'shp')
    i = 0
    Flag = False
    while not Flag and i <= RunLimit:
        try:
            arcpy.CreateFeatureclass_management(OutDic['folder'], OutDic['name'] + String(i), Dic['geometry_type'],'', Dic['has_m'],Dic['has_z'])
            Flag = True
            break
        except Exception, e:
            import sys
            tb = sys.exc_info()[2]
            arcpy.AddWarning("Line %i" % tb.tb_lineno)
            arcpy.AddWarning(e.message)
            i += 1

    if not Flag: arcpy.AddWarning('Failed to Create feature class for  ' + OutDic['folder'] + "\\" + outLayer)
    if OutDic['folder'] == arcpy.env.workspace:
        return OutDic['file'] + String(i)
    else:
        return OutDic['folder'] + "\\" + OutDic['name'] + String(i) + '.shp'
def MakeFeatureLayer(inLayer,outLayer,Selection = None):
    i = 0
    Flag = False
    while not Flag and i <= RunLimit:
        try:
            arcpy.MakeFeatureLayer_management(inLayer, outLayer + String(i), Selection)
            Flag = True
            break
        except Exception, e:
            import sys
            tb = sys.exc_info()[2]
            arcpy.AddWarning("Line %i" % tb.tb_lineno)
            arcpy.AddWarning(e.message)
            i += 1
    if not Flag: arcpy.AddWarning('Failed to Make Feature from Layer ' + inLayer)
    return outLayer + String(i)
def CopyFeatures(inLayer, outLayer):
    i = 0
    Flag = False
    while not Flag and i <= RunLimit:
        try:
            arcpy.CopyFeatures_management(inLayer, outLayer + String(i))
            Flag = True
            break
        except Exception, e:
            import sys
            tb = sys.exc_info()[2]
            arcpy.AddWarning("Line %i" % tb.tb_lineno)
            arcpy.AddWarning(e.message)
            i += 1
    if not Flag: arcpy.AddWarning('Failed to Copy Feature from Layer ' + inLayer)
    return outLayer + String(i)
def SaveToLayerFile(inLayer):
    i = 0
    Flag = False
    while not Flag and i <= RunLimit:
        try:
            arcpy.SaveToLayerFile_management (inLayer, inLayer + String(i),"RELATIVE","CURRENT")
            Flag = True
            break
        except Exception, e:
            import sys
            tb = sys.exc_info()[2]
            arcpy.AddWarning("Line %i" % tb.tb_lineno)
            arcpy.AddWarning(e.message)
            i += 1
    if not Flag: arcpy.AddWarning('Failed to Save the layer file from Layer ' + inLayer)
    return inLayer + String(i)
## Second Group of Classes
def Project(inLayer,CdSys = CoordSystemSC):
    i = 0
    Flag = False
    while not Flag and i <= RunLimit:
        try:
            arcpy.Project_management(inLayer, inLayer + "_Projected" + String(i), CdSys)
            Flag = True
            break
        except Exception, e:
            import sys
            tb = sys.exc_info()[2]
            arcpy.AddWarning("Line %i" % tb.tb_lineno)
            arcpy.AddWarning(e.message)
            i += 1
    if not Flag: arcpy.AddWarning('Failed to Project Layer ' + inLayer)
    return inLayer + "_Projected" + String(i)
def FeatureToLine(inLayer, outLayer,tolerance = ''):
    i = 0
    Flag = False
    while not Flag and i <= RunLimit:
        try:
            arcpy.FeatureToLine_management(inLayer, outLayer + String(i),tolerance)
            Flag = True
            break
        except Exception, e:
            import sys
            tb = sys.exc_info()[2]
            arcpy.AddWarning("Line %i" % tb.tb_lineno)
            arcpy.AddWarning(e.message)
            i += 1
    if not Flag: arcpy.AddWarning('Failed to Do Feature to Line for Layer ' + inLayer)
##    return MakeFeatureLayer(outLayer + String(i),outLayer)
    return outLayer + String(i)
def Intersect(inLayer, outLayer, Dic):
    i = 0
    Flag = False
    while not Flag and i <= RunLimit:
        try:
            arcpy.Intersect_analysis(inLayer, outLayer + String(i), Dic['join_attributes'], Dic['cluster_tolerance'], Dic['output_type'])
            Flag = True
            break
        except Exception, e:
            import sys
            tb = sys.exc_info()[2]
            arcpy.AddWarning("Line %i" % tb.tb_lineno)
            arcpy.AddWarning(e.message)
            i += 1
    if not Flag: arcpy.AddWarning('Failed to Do Intersect for Layer ' + str(inLayer))
    #return MakeFeatureLayer(outLayer + String(i),outLayer)
    return outLayer + String(i)
def SplitAtPoints(Lines, Points, outLayer,Radius):
    i = 0
    Flag = False
    while not Flag and i <= RunLimit:
        try:
            arcpy.SplitLineAtPoint_management(Lines,Points, outLayer + String(i), Radius)
            Flag = True
            break
        except Exception, e:
            import sys
            tb = sys.exc_info()[2]
            arcpy.AddWarning("Line %i" % tb.tb_lineno)
            arcpy.AddWarning(e.message)
            i += 1
    if not Flag: arcpy.AddWarning('Failed to Do Split Line At Point for Layer ' + Lines)
    #return MakeFeatureLayer(outLayer + String(i),outLayer)
    return outLayer + String(i)
def Merge(inLayers, outLayer):
    i = 0
    Flag = False
    while not Flag and i <= RunLimit:
        try:
            arcpy.Merge_management(inLayers, outLayer + String(i))
            Flag = True
            break
        except Exception, e:
            import sys
            tb = sys.exc_info()[2]
            arcpy.AddWarning("Line %i" % tb.tb_lineno)
            arcpy.AddWarning(e.message)
            i += 1
    if not Flag: arcpy.AddWarning('Failed to Do Merge for Layer(s) ' + LayerList2str(inLayers) + str(m))
    #return MakeFeatureLayer(outLayer + String(i),outLayer)
    return outLayer + String(i)
def SpatialJoin(targetLayer, joinLayer, outLayer,Dic = {'join_operation':"JOIN_ONE_TO_ONE",'join_type':"KEEP_ALL",'field_mapping':'','match_option':'INTERSECT','search_radius':0,'distance_field_name':''}):
    i = 0
    Flag = False
    while not Flag and i <= RunLimit:
        try:
            arcpy.SpatialJoin_analysis(targetLayer, joinLayer, outLayer + String(i), Dic['join_operation'], Dic['join_type'], Dic['field_mapping'], Dic['match_option'], Dic['search_radius'], Dic['distance_field_name'])
            Flag = True
            break
        except Exception, e:
            import sys
            tb = sys.exc_info()[2]
            arcpy.AddWarning("Line %i" % tb.tb_lineno)
            arcpy.AddWarning(e.message)
            i += 1
    if not Flag: arcpy.AddWarning('Failed to Do Spatial Join for Layer(s) ' + targetLayer + ';' + joinLayer)
    #return MakeFeatureLayer(outLayer + String(i),outLayer)
    return outLayer + String(i)
def Buffer(inLayer, outLayer, Dic = {'distance': 0, 'line_side': 'FULL', 'line_end_type': 'FLAT', 'dissolve_option': 'NONE', 'dissolve_field': '#'}):
    i = 0
    Flag = False
    while not Flag and i <= RunLimit:
        try:
            arcpy.Buffer_analysis(inLayer, outLayer + String(i), Dic['distance'], Dic['line_side'], Dic['line_end_type'], Dic['dissolve_option'], Dic['dissolve_field'])
            Flag = True
            break
        except Exception, e:
            import sys
            tb = sys.exc_info()[2]
            arcpy.AddWarning("Line %i" % tb.tb_lineno)
            arcpy.AddWarning(e.message)
            i += 1
    if not Flag: arcpy.AddWarning('Failed to Do Buffer for Layer ' + inLayer)
    #return MakeFeatureLayer(outLayer + String(i),outLayer)
    return outLayer + String(i)
def SplitLineAtPoint(LineLayer, PointLayer, outLayer, search_radius):
    i = 0
    Flag = False
    while not Flag and i <= RunLimit:
        try:
            arcpy.SplitLineAtPoint_management(LineLayer, PointLayer,outLayer + String(i), search_radius)
            Flag = True
            break
        except Exception, e:
            import sys
            tb = sys.exc_info()[2]
            arcpy.AddWarning("Line %i" % tb.tb_lineno)
            arcpy.AddWarning(e.message)
            i += 1
    if not Flag: arcpy.AddWarning('Failed to Do Split Line at Point for Layer ' + LineLayer)
    #return MakeFeatureLayer(outLayer + String(i),outLayer)
    return outLayer + String(i)
def Sort(inLayer, outLayer, SortFields):
    i = 0
    Flag = False
    while not Flag and i <= RunLimit:
        try:
            arcpy.Sort_management(inLayer, outLayer + String(i), SortFields)
            Flag = True
            break
        except Exception, e:
            import sys
            tb = sys.exc_info()[2]
            arcpy.AddWarning("Line %i" % tb.tb_lineno)
            arcpy.AddWarning(e.message)
            i += 1
    if not Flag: arcpy.AddWarning('Failed to Do Sort for Layer ' + inLayer)
    #return MakeFeatureLayer(outLayer + String(i),outLayer)
    return outLayer + String(i)
def VerticesToPoints(inLayer,outLayer,Type = "BOTH_ENDS"):
    i = 0
    Flag = False
    while not Flag and i <= RunLimit:
        try:
            arcpy.FeatureVerticesToPoints_management(inLayer, outLayer + String(i), Type)
            Flag = True
            break
        except Exception, e:
            import sys
            tb = sys.exc_info()[2]
            arcpy.AddWarning("Line %i" % tb.tb_lineno)
            arcpy.AddWarning(e.message)
            i += 1
    if not Flag: arcpy.AddWarning('Failed to Do Vertices to Points for Layer ' + str(inLayer))
    #return MakeFeatureLayer(outLayer + String(i),outLayer)
    return outLayer + String(i)
def LocateFeaturesAlongRoutes(inFeatureLayer, inLayer, RID, Radius, outLayer, outputProp):
    i = 0
    Flag = False
    while not Flag and i <= RunLimit:
        try:
            arcpy.LocateFeaturesAlongRoutes_lr(inFeatureLayer, inLayer, RID, Radius, outLayer + String(i), outputProp, "ALL", "DISTANCE", "ZERO", "FIELDS", "M_DIRECTON")
            Flag = True
            break
        except Exception, e:
            import sys
            tb = sys.exc_info()[2]
            arcpy.AddWarning("Line %i" % tb.tb_lineno)
            arcpy.AddWarning(e.message)
            i += 1
    if not Flag: arcpy.AddWarning('Failed to Do Locate Features Along Routes for Layer ' + str(inLayer))
    #return MakeFeatureLayer(outLayer + String(i),outLayer)
    return outLayer + String(i)
def MakeRouteEventLayer(inLayer, RID, inFeatureLayer, outputProp, outLayer):
    i = 0
    Flag = False
    while not Flag and i <= RunLimit:
        try:
            arcpy.MakeRouteEventLayer_lr(inLayer, RID, inFeatureLayer, outputProp, outLayer,"#","ERROR_FIELD","ANGLE_FIELD","NORMAL","ANGLE","RIGHT","POINT")
            Flag = True
            break
        except Exception, e:
            import sys
            tb = sys.exc_info()[2]
            arcpy.AddWarning("Line %i" % tb.tb_lineno)
            arcpy.AddWarning(e.message)
            i += 1
    if not Flag: arcpy.AddWarning('Failed to Do Make Route Event Layer for Layer ' + str(inLayer))
    #return MakeFeatureLayer(outLayer + String(i),outLayer)
    return outLayer + String(i)
def TableToTable(inLayer, Folder, outLayer):
    i = 0
    Flag = False
    while not Flag and i <= RunLimit:
        try:
            arcpy.arcpy.TableToTable_conversion(inLayer, Folder, outLayer)
            Flag = True
            break
        except Exception, e:
            import sys
            tb = sys.exc_info()[2]
            arcpy.AddWarning("Line %i" % tb.tb_lineno)
            arcpy.AddWarning(e.message)
            i += 1
    if not Flag: arcpy.AddWarning('Failed to Do Make Route Event Layer for Layer ' + str(inLayer))
    #return MakeFeatureLayer(outLayer + String(i),outLayer)
    return outLayer + String(i)
def Dissolve(inLayer, outLayer,dissolve_field, statistics_fields="", multi_part="MULTI_PART", unsplit_lines="DISSOLVE_LINES"):
    i = 0
    Flag = False
    while not Flag and i <= RunLimit:
        try:
            arcpy.Dissolve_management(inLayer, outLayer, dissolve_field, statistics_fields, multi_part, unsplit_lines)
            Flag = True
            break
        except Exception, e:
            import sys
            tb = sys.exc_info()[2]
            arcpy.AddWarning("Line %i" % tb.tb_lineno)
            arcpy.AddWarning(e.message)
            i += 1
    if not Flag: arcpy.AddWarning('Failed to Dissolve for Layer ' + str(inLayer))
    return outLayer + String(i)
def CopyRows(inLayer, outLayer):
    i = 0
    Flag = False
    while not Flag and i <= RunLimit:
        try:
            arcpy.CopyRows_management(inLayer, outLayer)
            Flag = True
            break
        except Exception, e:
            import sys
            tb = sys.exc_info()[2]
            arcpy.AddWarning("Line %i" % tb.tb_lineno)
            arcpy.AddWarning(e.message)
            i += 1
    if not Flag: arcpy.AddWarning('Failed to CopyRows for Layer ' + str(inLayer))
    return outLayer + String(i)
def CreateTable(Path, outLayer):
    i = 0
    Flag = False
    while not Flag and i <= RunLimit:
        try:
            arcpy.CreateTable_management(Path, outLayer)
            Flag = True
            break
        except Exception, e:
            import sys
            tb = sys.exc_info()[2]
            arcpy.AddWarning("Line %i" % tb.tb_lineno)
            arcpy.AddWarning(e.message)
            i += 1
    if not Flag: arcpy.AddWarning('Failed to Create Table for Layer ' + str(Path))
    return outLayer + String(i)
def CreateRoute_lr(InLayer,FieldName, outLayer,copr="UPPER_LEFT", mfactor="0.000189393939393939", moffset="0", gaps="NO_IGNORE", bindex="INDEX"):
    i = 0
    Flag = False
    while not Flag and i <= RunLimit:
        try:
            arcpy.CreateRoutes_lr(InLayer, FieldName, outLayer,
                                  measure_source="LENGTH", from_measure_field="", to_measure_field="",
                                  coordinate_priority=copr, measure_factor=mfactor,
                                  measure_offset=moffset, ignore_gaps=gaps, build_index=bindex)
            Flag = True
            break
        except Exception, e:
            import sys
            tb = sys.exc_info()[2]
            arcpy.AddWarning("Line %i" % tb.tb_lineno)
            arcpy.AddWarning(e.message)
            i += 1
    if not Flag: arcpy.AddWarning('Failed to Create Route for Layer ' + str(Path))
    return outLayer + String(i)
## Third Group of Classes
def AddField(inLayer, FieldDic, Mode = 'replace'):
    R = ''
    if Mode == 'replace':
        try:
            arcpy.DeleteField_management(inLayer,FieldDic['name'])
            R += 'D'
        except:
            R += 'N'
    else:
        R = '-'
    try:
        arcpy.AddField_management(inLayer,FieldDic['name'],FieldDic['type'],FieldDic['precision'],FieldDic['scale'],FieldDic['length'],FieldDic['alias'],FieldDic['nullable'],FieldDic['required'])
        R += 'A'
    except:
        R += 'N'
    
    if R == 'DN' or R == 'NN':
        #arcpy.AddWarning(str(arcpy.GetMessages()))
        arcpy.AddWarning('Failed to add field ' + FieldDic['name'] + ' to layer ' + inLayer)
def CalField(inLayer, Field, Exp, CodeBlock = ''):
    try:
        arcpy.CalculateField_management(inLayer,Field['name'],Exp,"PYTHON_9.3",CodeBlock)
    except:
        arcpy.AddWarning('Failed to calculate field ' + Field['name'] + ' in layer ' + inLayer)
def String(i):
    if i == 0:
        return ''
    else:
        return str(i)
def ClearFields(inLayer,FieldstoKeep = []):
    FieldObjList = arcpy.ListFields(inLayer)
    FieldNameList = []
    for Field in FieldObjList:
        if not Field.required and not Field.name in FieldstoKeep:
            FieldNameList.append(Field.name)
    for Field in FieldNameList:
        try:
            arcpy.DeleteField_management(inLayer,Field)
        except:
            Failed.append(Field)
    return inLayer
def LayerList2str(inLayerList):
    if type(inLayerList) == list:
        outString = ''
        for Layer in inLayerList:
            outString = outString + Layer + ';'
        return outString[0:len(outString)-1]
    else:
        return inLayerList
## Forth Group of Function
def GetFID(Row):
    FID = ''
    try:
        FID = Row.getValue('FID')
    except:
        try:
            FID = Row.getValue('OBJECTID')
        except:
            arcpy.AddWarning("FID or OBJECTID not Found")
    return FID
def GetVal(Row, Field, Default=0, AddWarning=False):
    try:
        Val = Row.getValue(Field)
        if not Val is None:
            return Val
        else:
            if AddWarning: arcpy.AddMessage('Failed to read: ' + Field + ', Default value Assigned')
            return Default
    except:
        if AddWarning: arcpy.AddMessage('Failed to read: ' + Field + ', Default value Assigned')
        return Default
def GetIntVal(Row, Field, Default=0, AddWarning=False):
        try:
            Val = int(Row.getValue(Field))
            if not Val is None:
                return Val
            else:
                if AddWarning: arcpy.AddMessage('Failed to read: ' + Field + ', Default value Assigned')
                return Default
        except:
            if AddWarning: arcpy.AddMessage('Failed to read: ' + Field + ', Default value Assigned')
            return Default
def GetFloatVal(Row, Field, Default=0.0, AddWarning=False):
        try:
            Val = float(Row.getValue(Field))
            if not Val is None:
                return Val
            else:
                if AddWarning: arcpy.AddMessage('Failed to read: ' + Field + ', Default value Assigned')
                return Default
        except:
            if AddWarning: arcpy.AddMessage('Failed to read: ' + Field + ', Default value Assigned')
            return Default
def MaximumValue(Layer,FieldName):
    SC = arcpy.SearchCursor(Layer)
    SRow = SC.next()
    if SRow:
        Maximum = GetVal(SRow,FieldName)
    else:
        Maximum = None
    for SRow in SC:
        Val = GetVal(SRow,FieldName)
        if Val > Maximum:
            Maximum = Val
    return Maximum

#  Crash Analysis
## SPF
def NaturalLog(A):
        import math
        if A > 0:
            return math.log1p(A - 1)
        else:
            return 0
def SPF_Module(URow):
    import math

    # Define SPF Dictionary
    SPF = {
        'TOT'       : 0,        'TCk'       : 0,

        'FI'        : 0,        'FIk'       : 0,
        'FIKAB'     : 0,        'FIKABk'    : 0,

        'MVC'       : 0,        'MVCk'      : 0,
        'MVFIC'     : 0,        'MVFICk'    : 0,
        'MVPDOC'    : 0,        'MVPDOCk'   : 0,

        'MVndC'     : 0,        'MVndCk'    : 0,
        'MVFIndC'   : 0,        'MVFIndCk'  : 0,
        'MVPDOndC'  : 0,        'MVPDOndCk' : 0,

        'MVdC'      : 0,        'MVdCk'     : 0,
        'MVFIdC'    : 0,        'MVFIdCk'   : 0,
        'MVPDOdC'   : 0,        'MVPDOdCk'  : 0,

        'SVC'       : 0,        'SVCk'      : 0,
        'SVFIC'     : 0,        'SVFICk'    : 0,
        'SVPDOC'    : 0,        'SVPDOCk'   : 0,

        'Ped'       : 0,        'Pedk'      : 0}

    # Flag for Warning Message(WM)       
    Flag = False
    WM   = 'SPF Intersections ' 

    # Supported Facility Types in this Function
    SPFTypes = ['R3ST' ,'R4ST' , 'R4SG', 'RM3ST', 'RM4ST', 'RM4SG', 'U3ST', 'U4ST', 'U3SG', 'U4SG', 'U2U', 'U3T', 'U4U', 'U4D', 'U5T']

    # Reading & Checking the type
    iType    = GetVal(URow,F_FType['name'],'')
    if not iType in FTypes:
        Flag = True; WM += ', Type(' + str(iType) + ') not supported'

    # Reading Input Info: AADT, Segment Length, Driveway Info, ...
    AADT_Major = GetVal(URow,F_AADT_Major['name'])
    AADT_Minor = GetVal(URow,F_AADT_Minor['name'])
    AADT       = GetVal(URow,F_AADT      ['name'])
    Length     = URow.getValue('Shape').length

    dMjC       = GetVal(URow,F_dMjC['name'])
    dMnC       = GetVal(URow,F_dMnC['name'])
    dMjI       = GetVal(URow,F_dMjI['name'])
    dMnI       = GetVal(URow,F_dMnI['name'])
    dMjR       = GetVal(URow,F_dMjR['name'])
    dMnR       = GetVal(URow,F_dMnR['name'])
    dO         = GetVal(URow,F_dO  ['name'])

    PedVol     = GetVal(URow,'Ped_Vol', 1)
    PedVol     = GetVal(URow,F_PED_VOL['name'],PedVol)

    LanesX     = GetVal(URow,'Lanesx', 2)
    LanesX     = GetVal(URow,F_LANESX['name'],LanesX)

    # Checking AADT
    if AADT_Major == 0 and AADT_Minor == 0 and AADT == 0:
        Flag = True; WM += ', Zero AADT'

    # Checking Length
    if Length == 0 and not iType in ITypes:
        Flag = True; WM += ', Zero segment Length'

    # Ln's and Ped Volumes conversion

    a   = NaturalLog(AADT_Major)
    b   = NaturalLog(AADT_Minor)
    ab  = NaturalLog(AADT_Major + AADT_Minor)
    if AADT_Major <> 0:
        boa = NaturalLog(float(AADT_Minor) / AADT_Major)
    else:
        boa = 0
    c   = NaturalLog(AADT)
    d   = NaturalLog(Length/5280)

    p = 0
    if PedVol == 1: p = 20
    if PedVol == 2: p = 120
    if PedVol == 3: p = 400
    if PedVol == 4: p = 7500
    if PedVol == 5: p = 1700
    if p <> 0: p = NaturalLog(p)

    # SPF Calculations based on types
    if iType ==  "R3ST":
        if AADT_Major > 19500 or AADT_Major <= 0: Flag = True; WM += ', AADT Major(' + str(AADT_Major) + ') for FID = ' + str(GetVal(URow,"FID")) + ' not in range'
        if AADT_Minor > 4300  or AADT_Minor <= 0: Flag = True; WM += ', AADT Minor(' + str(AADT_Minor) + ') for FID = ' + str(GetVal(URow,"FID")) + ' not in range'
        SPF['TOT']  = math.exp(-9.86 + 0.79 * a + 0.49 * b)
        SPF['TCk'] = 0.54    

    if iType ==  "R4ST":
        if AADT_Major > 14700 or AADT_Major <= 0: Flag = True; WM += ', AADT Major(' + str(AADT_Major) + ') for FID = ' + str(GetVal(URow,"FID")) + ' not in range'
        if AADT_Minor > 3500  or AADT_Minor <= 0: Flag = True; WM += ', AADT Minor(' + str(AADT_Minor) + ') for FID = ' + str(GetVal(URow,"FID")) + ' not in range'
        SPF['TOT']  = math.exp(-8.56 + 0.6 * a + 0.61 * b)
        SPF['TCk'] = 0.24    

    if iType ==  "R4SG":
        if AADT_Major > 25200 or AADT_Major <= 0: Flag = True; WM += ', AADT Major(' + str(AADT_Major) + ') for FID = ' + str(GetVal(URow,"FID")) + ' not in range'
        if AADT_Minor > 12500 or AADT_Minor <= 0: Flag = True; WM += ', AADT Minor(' + str(AADT_Minor) + ') for FID = ' + str(GetVal(URow,"FID")) + ' not in range'
        SPF['TOT']  = math.exp(-5.13 + 0.6 * a + 0.2 * b)
        SPF['TCk'] = 0.11    

    if iType ==  "RM3ST":
        if AADT_Major > 78300 or AADT_Major <= 0: Flag = True; WM += ', AADT Major(' + str(AADT_Major) + ') for FID = ' + str(GetVal(URow,"FID")) + ' not in range'
        if AADT_Minor > 23000 or AADT_Minor <= 0: Flag = True; WM += ', AADT Minor(' + str(AADT_Minor) + ') for FID = ' + str(GetVal(URow,"FID")) + ' not in range'
        SPF['TOT']     = math.exp(-12.526 + 1.204 * a + 0.236 * b)
        SPF['TCk']    = 0.46    
        SPF['FI']     = math.exp(-12.664 + 1.107 * a + 0.272 * b)
        SPF['FIk']    = 0.569
        SPF['FIKAB']  = math.exp(-11.989 + 1.013 * a + 0.228 * b)
        SPF['FIKABk'] = 0.566    
   
    if iType ==  "RM4ST":
        if AADT_Major > 78300 or AADT_Major <= 0: Flag = True; WM += ', AADT Major(' + str(AADT_Major) + ') for FID = ' + str(GetVal(URow,"FID")) + ' not in range'
        if AADT_Minor > 7400  or AADT_Minor <= 0: Flag = True; WM += ', AADT Minor(' + str(AADT_Minor) + ') for FID = ' + str(GetVal(URow,"FID")) + ' not in range'
        SPF['TOT']     = math.exp(-10.008 + 0.848 * a + 0.448 * b)
        SPF['TCk']    = 0.494    
        SPF['FI']     = math.exp(-11.554 + 0.888 * a + 0.525 * b)
        SPF['FIk']    = 0.742
        SPF['FIKAB']  = math.exp(-10.734 + 0.828 * a + 0.412 * b)
        SPF['FIKABk'] = 0.655  

    if iType ==  "RM4SG":
        if AADT_Major > 43500 or AADT_Major <= 0: Flag = True; WM += ', AADT Major(' + str(AADT_Major) + ') for FID = ' + str(GetVal(URow,"FID")) + ' not in range'
        if AADT_Minor > 18500 or AADT_Minor <= 0: Flag = True; WM += ', AADT Minor(' + str(AADT_Minor) + ') for FID = ' + str(GetVal(URow,"FID")) + ' not in range'
        SPF['TOT']     = math.exp(-7.182 + 0.722 * a + 0.337 * b)
        SPF['TCk']    = 0.277    
        SPF['FI']     = math.exp(-6.393 + 0.638 * a + 0.232 * b)
        SPF['FIk']    = 0.218
        SPF['FIKAB']  = math.exp(-12.011 + 1.279 * ab)
        SPF['FIKABk'] = 0.566  
    
    if iType ==  "U3ST":
        if AADT_Major > 45700 or AADT_Major <= 0: Flag = True; WM += ', AADT Major(' + str(AADT_Major) + ') for FID = ' + str(GetVal(URow,"FID")) + ' not in range'
        if AADT_Minor > 9300  or AADT_Minor <= 0: Flag = True; WM += ', AADT Minor(' + str(AADT_Minor) + ') for FID = ' + str(GetVal(URow,"FID")) + ' not in range'
        SPF['MVC']     = math.exp(-13.36 + 1.11 * a + 0.41 * b)
        SPF['MVCk']    = 0.8
        SPF['MVFIC']   = math.exp(-14.01 + 1.16 * a + 0.3 * b)
        SPF['MVFICk']  = 0.69
        SPF['MVPDOC']  = math.exp(-15.38 + 1.2 * a + 0.51 * b)
        SPF['MVPDOCk'] = 0.77
        SPF['MVFIC']   = SPF['MVC'] * SPF['MVFIC'] / (SPF['MVFIC'] + SPF['MVPDOC'])
        SPF['MVPDOC']  = SPF['MVC'] - SPF['MVFIC']

        SPF['SVC']     = math.exp(-6.81 + 0.16 * a + 0.51 * b)
        SPF['SVCk']    = 1.14
        SPF['SVFIC']   = 0.31 * SPF['SVC']
        SPF['SVFICk']  = SPF['SVCk']
        SPF['SVPDOC']  = math.exp(-8.36 + 0.25 * a + 0.55 * b)
        SPF['SVPDOCk'] = 1.29
        SPF['SVFIC']   = SPF['SVC'] * SPF['SVFIC'] / (SPF['SVFIC'] + SPF['SVPDOC'])
        SPF['SVPDOC']  = SPF['SVC'] - SPF['SVFIC']
        
    if iType == "U4ST":
        if AADT_Major > 58100 or AADT_Major <= 0: Flag = True; WM += ', AADT Major(' + str(AADT_Major) + ') for FID = ' + str(GetVal(URow,"FID")) + ' not in range'
        if AADT_Minor > 16400 or AADT_Minor <= 0: Flag = True; WM += ', AADT Minor(' + str(AADT_Minor) + ') for FID = ' + str(GetVal(URow,"FID")) + ' not in range'
        
        SPF['MVC']     = math.exp(-8.9 + 0.82 * a + 0.25 * b)
        SPF['MVCk']    = 0.4
        SPF['MVFIC']   = math.exp(-11.13 + 0.93 * a + 0.28 * b)
        SPF['MVFICk']  = 0.48
        SPF['MVPDOC']  = math.exp(-8.74 + 0.77 * a + 0.23 * b)
        SPF['MVPDOCk'] = 0.4
        SPF['MVFIC']   = SPF['MVC'] * SPF['MVFIC'] / (SPF['MVFIC'] + SPF['MVPDOC'])
        SPF['MVPDOC']  = SPF['MVC'] - SPF['MVFIC']

        SPF['SVC']     = math.exp(-5.33 + 0.33 * a + 0.12 * b)
        SPF['SVCk']    = 0.65
        SPF['SVFIC']   = 0.28 * SPF['SVC']
        SPF['SVFICk']  = SPF['SVCk']
        SPF['SVPDOC']  = math.exp(-7.04 + 0.36 * a + 0.25 * b)
        SPF['SVPDOCk'] = 0.54
        SPF['SVFIC']   = SPF['SVC'] * SPF['SVFIC'] / (SPF['SVFIC'] + SPF['SVPDOC'])
        SPF['SVPDOC']  = SPF['SVC'] - SPF['SVFIC']
       
    if iType == "U3SG":
        if AADT_Major > 46800 or AADT_Major <= 0: Flag = True; WM += ', AADT Major(' + str(AADT_Major) + ') for FID = ' + str(GetVal(URow,"FID")) + ' not in range'
        if AADT_Minor > 5900  or AADT_Minor <= 0: Flag = True; WM += ', AADT Minor(' + str(AADT_Minor) + ') for FID = ' + str(GetVal(URow,"FID")) + ' not in range'
        
        SPF['MVC']     = math.exp(-12.13 + 1.11 * a + 0.26 * b)
        SPF['MVCk']    = 0.33
        SPF['MVFIC']   = math.exp(-11.58 + 1.02 * a + 0.17 * b)
        SPF['MVFICk']  = 0.3
        SPF['MVPDOC']  = math.exp(-13.24 + 1.14 * a + 0.3 * b)
        SPF['MVPDOCk'] = 0.36
        SPF['MVFIC']   = SPF['MVC'] * SPF['MVFIC'] / (SPF['MVFIC'] + SPF['MVPDOC'])
        SPF['MVPDOC']  = SPF['MVC'] - SPF['MVFIC']

        SPF['SVC']     = math.exp(-9.02 + 0.42 * a + 0.4 * b)
        SPF['SVCk']    = 0.36
        SPF['SVFIC']   = math.exp(-9.75 + 0.27 * a + 0.51 * b)
        SPF['SVFICk']  = 0.24
        SPF['SVPDOC']  = math.exp(-9.08 + 0.45 * a + 0.33 * b)
        SPF['SVPDOCk'] = 0.53
        SPF['SVFIC']   = SPF['SVC'] * SPF['SVFIC'] / (SPF['SVFIC'] + SPF['SVPDOC'])
        SPF['SVPDOC']  = SPF['SVC'] - SPF['SVFIC']

        SPF['Ped']     = math.exp(-6.6 + 0.05 * ab + 0.24 * boa + 0.41 * p + 0.09 * LanesX)
        SPF['Pedk']    = 0.52
    
    if iType == "U4SG":
        if AADT_Major > 67700 or AADT_Major <= 0: Flag = True; WM += ', AADT Major(' + str(AADT_Major) + ') for FID = ' + str(GetVal(URow,"FID")) + ' not in range'
        if AADT_Minor > 33400 or AADT_Minor <= 0: Flag = True; WM += ', AADT Minor(' + str(AADT_Minor) + ') for FID = ' + str(GetVal(URow,"FID")) + ' not in range'
        
        SPF['MVC']     = math.exp(-10.99 + 1.07 * a + 0.23 * b)
        SPF['MVCk']    = 0.39
        SPF['MVFIC']   = math.exp(-13.14 + 1.18 * a + 0.22 * b)
        SPF['MVFICk']  = 0.33
        SPF['MVPDOC']  = math.exp(-11.02 + 1.02 * a + 0.24 * b)
        SPF['MVPDOCk'] = 0.44
        SPF['MVFIC']   = SPF['MVC'] * SPF['MVFIC'] / (SPF['MVFIC'] + SPF['MVPDOC'])
        SPF['MVPDOC']  = SPF['MVC'] - SPF['MVFIC']

        SPF['SVC']     = math.exp(-10.21 + 0.68 * a + 0.27 * b)
        SPF['SVCk']    = 0.36
        SPF['SVFIC']   = math.exp(-9.25 + 0.43 * a + 0.29 * b)
        SPF['SVFICk']  = 0.09
        SPF['SVPDOC']  = math.exp(-11.34 + 0.78 * a + 0.25 * b)
        SPF['SVPDOCk'] = 0.44
        SPF['SVFIC']   = SPF['SVC'] * SPF['SVFIC'] / (SPF['SVFIC'] + SPF['SVPDOC'])
        SPF['SVPDOC']  = SPF['SVC'] - SPF['SVFIC']

        SPF['Ped']     = math.exp(-9.53 + 0.4 * ab + 0.26 * boa + 0.45 * p + 0.04 * LanesX)
        SPF['Pedk']    = 0.24

    if iType == "R2U":
        if AADT > 17800 or AADT <= 0: Flag = True; WM += ', AADT (' + str(AADT) + ') for FID = ' + str(GetVal(URow,"FID")) + ' not in range'
        SPF['TOT'] = AADT * Length/5280 * 365 * math.exp(-0.312) / 1000000.0
        SPF['TCk'] = 0.236/(Length/5280)

    if iType == "R4U":
        if AADT > 33200 or AADT <= 0: Flag = True; WM += ', AADT (' + str(AADT) + ') for FID = ' + str(GetVal(URow,"FID")) + ' not in range'
        SPF['TOT'] = math.exp(-9.653 + 1.176 * c + d)
        SPF['TCk'] = 1/math.exp(1.675 + d)
        SPF['FI']  = math.exp(-9.410 + 1.094 * c + d)
        SPF['FIk'] = 1/math.exp(1.796 + d)

    if iType == "R4D":
        if AADT > 89300 or AADT <= 0: Flag = True; WM += ', AADT (' + str(AADT) + ') for FID = ' + str(GetVal(URow,"FID")) + ' not in range'
        SPF['TOT'] = math.exp(-9.025 + 1.049 * c + d)
        SPF['TCk'] = 1/math.exp(1.549 + d)
        SPF['FI']  = math.exp(-8.837 + 0.958 * c + d)
        SPF['FIk'] = 1/math.exp(1.687 + d)

    if iType == "U2U":
        if AADT > 32600 or AADT <= 0: Flag = True; WM += ', AADT (' + str(AADT) + ') for FID = ' + str(GetVal(URow,"FID")) + ' not in range'

        SPF['MVndC']     = math.exp(-15.22 + 1.68 * c + d)
        SPF['MVndCk']    = 0.84
        SPF['MVFIndC']   = math.exp(-16.22 + 1.66 * c + d)
        SPF['MVFIndCk']  = 0.65
        SPF['MVPDOndC']  = math.exp(-15.62 + 1.69 * a + d)
        SPF['MVPDOndCk'] = 0.87
        SPF['MVFIndC']   = SPF['MVndC'] * SPF['MVFIndC'] / (SPF['MVFIndC'] + SPF['MVPDOndC'])
        SPF['MVPDOndC']  = SPF['MVndC'] - SPF['MVFIndC']

        SPF['SVC']      = math.exp(-5.47 + 0.56 * c + d)
        SPF['SVCk']     = 0.81
        SPF['SVFIC']    = math.exp(-3.96 + 0.23 * c + d)
        SPF['SVFICk']   = 0.50
        SPF['SVPDOC']   = math.exp(-6.51 + 0.64 * c + d)
        SPF['SVPDOCk']  = 0.87
        SPF['SVFIC']    = SPF['SVC'] * SPF['SVFIC'] / (SPF['SVFIC'] + SPF['SVPDOC'])
        SPF['SVPDOC']   = SPF['SVC'] - SPF['SVFIC']

        SPF['MVdC']     = ((0.158 * dMjC) + (0.050 * dMnC) + (0.172 * dMjI) + (0.023 * dMnI) + (0.083 * dMjR) + (0.016 * dMnR) + (0.025 * dO)) * (AADT/15000)**1.00 
        SPF['MVdCk']    = 0.81
        SPF['MVFIdC']   = 0.323 * SPF['MVdC']
        SPF['MVFIdCk']  = SPF['MVdCk']
        SPF['MVPDOdC']  = 0.677 * SPF['MVdC']
        SPF['MVPDOdCk'] = SPF['MVdCk']

        SPF['TOT']     = SPF['MVndC']    + SPF['MVdC']    + SPF['SVC']
        SPF['FI']      = SPF['MVFIndC']  + SPF['MVFIdC']  + SPF['SVFIC']

        SPF['MVC']     = SPF['MVndC']    + SPF['MVdC']
        SPF['MVFIC']   = SPF['MVFIndC']  + SPF['MVFIdC']
        SPF['MVPDOC']  = SPF['MVPDOndC'] + SPF['MVPDOdC']

    if iType == "U3T":
        if AADT > 32900 or AADT <= 0: Flag = True; WM += ', AADT (' + str(AADT) + ') for FID = ' + str(GetVal(URow,"FID")) + ' not in range'

        SPF['MVndC']     = math.exp(-12.40 + 1.41 * c + d)
        SPF['MVndCk']    = 0.66
        SPF['MVFIndC']   = math.exp(-16.45 + 1.69 * c + d)
        SPF['MVFIndCk']  = 0.59
        SPF['MVPDOndC']  = math.exp(-11.95 + 1.33 * a + d)
        SPF['MVPDOndCk'] = 0.59
        SPF['MVFIndC']   = SPF['MVndC'] * SPF['MVFIndC'] / (SPF['MVFIndC'] + SPF['MVPDOndC'])
        SPF['MVPDOndC']  = SPF['MVndC'] - SPF['MVFIndC']

        SPF['SVC']     = math.exp(-5.74 + 0.54 * c + d)
        SPF['SVCk']    = 1.37
        SPF['SVFIC']   = math.exp(-6.37 + 0.47 * c + d)
        SPF['SVFICk']  = 1.06
        SPF['SVPDOC']  = math.exp(-6.29 + 0.56 * c + d)
        SPF['SVPDOCk'] = 1.93
        SPF['SVFIC']   = SPF['SVC'] * SPF['SVFIC'] / (SPF['SVFIC'] + SPF['SVPDOC'])
        SPF['SVPDOC']  = SPF['SVC'] - SPF['SVFIC']

        SPF['MVdC']     = ((0.102 * dMjC) + (0.032 * dMnC) + (0.110 * dMjI) + (0.015 * dMnI) + (0.053 * dMjR) + (0.010 * dMnR) + (0.016 * dO)) * (AADT/15000)**1.000 
        SPF['MVdCk']    = 1.10
        SPF['MVFIdC']   = 0.243 * SPF['MVdC']
        SPF['MVFIdCk']  = SPF['MVdCk']
        SPF['MVPDOdC']  = 0.757 * SPF['MVdC']
        SPF['MVPDOdCk'] = SPF['MVdCk']

        SPF['TOT']     = SPF['MVndC']    + SPF['MVdC']    + SPF['SVC']
        SPF['FI']      = SPF['MVFIndC']  + SPF['MVFIdC']  + SPF['SVFIC']

        SPF['MVC']     = SPF['MVndC']    + SPF['MVdC']
        SPF['MVFIC']   = SPF['MVFIndC']  + SPF['MVFIdC']
        SPF['MVPDOC']  = SPF['MVPDOndC'] + SPF['MVPDOdC']

    if iType == "U4U":
        if AADT > 40100 or AADT <= 0: Flag = True; WM += ', AADT (' + str(AADT) + ') for FID = ' + str(GetVal(URow,"FID")) + ' not in range'

        SPF['MVndC']     = math.exp(-11.63 + 1.33 * c + d)
        SPF['MVndCk']    = 1.01
        SPF['MVFIndC']   = math.exp(-12.08 + 1.25 * c + d)
        SPF['MVFIndCk']  = 0.99
        SPF['MVPDOndC']  = math.exp(-12.53 + 1.38 * a + d)
        SPF['MVPDOndCk'] = 1.08
        SPF['MVFIndC']   = SPF['MVndC'] * SPF['MVFIndC'] / (SPF['MVFIndC'] + SPF['MVPDOndC'])
        SPF['MVPDOndC']  = SPF['MVndC'] - SPF['MVFIndC']

        SPF['SVC']     = math.exp(-7.99 + 0.81 * c + d)
        SPF['SVCk']    = 0.91
        SPF['SVFIC']   = math.exp(-7.37 + 0.61 * c + d)
        SPF['SVFICk']  = 0.54
        SPF['SVPDOC']  = math.exp(-8.50 + 0.84 * c + d)
        SPF['SVPDOCk'] = 0.97
        SPF['SVFIC']   = SPF['SVC'] * SPF['SVFIC'] / (SPF['SVFIC'] + SPF['SVPDOC'])
        SPF['SVPDOC']  = SPF['SVC'] - SPF['SVFIC']

        SPF['MVdC']     = ((0.182 * dMjC) + (0.058 * dMnC) + (0.198 * dMjI) + (0.026 * dMnI) + (0.096 * dMjR) + (0.018 * dMnR) + (0.029 * dO)) * (AADT/15000)**1.172 
        SPF['MVdCk']    = 0.81
        SPF['MVFIdC']   = 0.342 * SPF['MVdC']
        SPF['MVFIdCk']  = SPF['MVdCk']
        SPF['MVPDOdC']  = 0.658 * SPF['MVdC']
        SPF['MVPDOdCk'] = SPF['MVdCk']

        SPF['TOT']     = SPF['MVndC']    + SPF['MVdC']    + SPF['SVC']
        SPF['FI']      = SPF['MVFIndC']  + SPF['MVFIdC']  + SPF['SVFIC']

        SPF['MVC']     = SPF['MVndC']    + SPF['MVdC']
        SPF['MVFIC']   = SPF['MVFIndC']  + SPF['MVFIdC']
        SPF['MVPDOC']  = SPF['MVPDOndC'] + SPF['MVPDOdC']

    if iType == "U4D":
        if AADT > 66000 or AADT <= 0: Flag = True; WM += ', AADT (' + str(AADT) + ') for FID = ' + str(GetVal(URow,"FID")) + ' not in range'

        SPF['MVndC']     = math.exp(-12.34 + 1.36 * c + d)
        SPF['MVndCk']    = 1.32
        SPF['MVFIndC']   = math.exp(-12.76 + 1.28 * c + d)
        SPF['MVFIndCk']  = 1.31
        SPF['MVPDOndC']  = math.exp(-12.81 + 1.38 * a + d)
        SPF['MVPDOndCk'] = 1.34
        SPF['MVFIndC']   = SPF['MVndC'] * SPF['MVFIndC'] / (SPF['MVFIndC'] + SPF['MVPDOndC'])
        SPF['MVPDOndC']  = SPF['MVndC'] - SPF['MVFIndC']

        SPF['SVC']     = math.exp(-5.05 + 0.47 * c + d)
        SPF['SVCk']    = 0.86
        SPF['SVFIC']   = math.exp(-8.71 + 0.66 * c + d)
        SPF['SVFICk']  = 0.28
        SPF['SVPDOC']  = math.exp(-5.04 + 0.45 * c + d)
        SPF['SVPDOCk'] = 1.06
        SPF['SVFIC']   = SPF['SVC'] * SPF['SVFIC'] / (SPF['SVFIC'] + SPF['SVPDOC'])
        SPF['SVPDOC']  = SPF['SVC'] - SPF['SVFIC']

        SPF['MVdC']     = ((0.033 * dMjC) + (0.011 * dMnC) + (0.036 * dMjI) + (0.005 * dMnI) + (0.018 * dMjR) + (0.003 * dMnR) + (0.005 * dO)) * (AADT/15000)**1.106 
        SPF['MVdCk']    = 1.39
        SPF['MVFIdC']   = 0.284 * SPF['MVdC']
        SPF['MVFIdCk']  = SPF['MVdCk']
        SPF['MVPDOdC']  = 0.716 * SPF['MVdC']
        SPF['MVPDOdCk'] = SPF['MVdCk']

        SPF['TOT']     = SPF['MVndC']    + SPF['MVdC']    + SPF['SVC']
        SPF['FI']      = SPF['MVFIndC']  + SPF['MVFIdC']  + SPF['SVFIC']

        SPF['MVC']     = SPF['MVndC']    + SPF['MVdC']
        SPF['MVFIC']   = SPF['MVFIndC']  + SPF['MVFIdC']
        SPF['MVPDOC']  = SPF['MVPDOndC'] + SPF['MVPDOdC']

    if iType == "U5T":
        if AADT > 53800 or AADT <= 0: Flag = True; WM += ', AADT (' + str(AADT) + ') for FID = ' + str(GetVal(URow,"FID")) + ' not in range'

        SPF['MVndC']     = math.exp(-9.70 + 1.17 * c + d)
        SPF['MVndCk']    = 0.81
        SPF['MVFIndC']   = math.exp(-10.47 + 1.12 * c + d)
        SPF['MVFIndCk']  = 0.62
        SPF['MVPDOndC']  = math.exp(-9.97 + 1.17 * a + d)
        SPF['MVPDOndCk'] = 0.88
        SPF['MVFIndC']   = SPF['MVndC'] * SPF['MVFIndC'] / (SPF['MVFIndC'] + SPF['MVPDOndC'])
        SPF['MVPDOndC']  = SPF['MVndC'] - SPF['MVFIndC']

        SPF['SVC']     = math.exp(-4.82 + 0.54 * c + d)
        SPF['SVCk']    = 0.52
        SPF['SVFIC']   = math.exp(-4.43 + 0.35 * c + d)
        SPF['SVFICk']  = 0.36
        SPF['SVPDOC']  = math.exp(-5.83 + 0.61 * c + d)
        SPF['SVPDOCk'] = 0.55
        SPF['SVFIC']   = SPF['SVC'] * SPF['SVFIC'] / (SPF['SVFIC'] + SPF['SVPDOC'])
        SPF['SVPDOC']  = SPF['SVC'] - SPF['SVFIC']

        SPF['MVdC']     = ((0.165 * dMjC) + (0.053 * dMnC) + (0.181 * dMjI) + (0.024 * dMnI) + (0.087 * dMjR) + (0.016 * dMnR) + (0.027 * dO)) * (AADT/15000)**1.172 
        SPF['MVdCk']    = 0.10
        SPF['MVFIdC']   = 0.269 * SPF['MVdC']
        SPF['MVFIdCk']  = SPF['MVdCk']
        SPF['MVPDOdC']  = 0.731 * SPF['MVdC']
        SPF['MVPDOdCk'] = SPF['MVdCk']

        SPF['TOT']     = SPF['MVndC']    + SPF['MVdC']    + SPF['SVC']
        SPF['FI']      = SPF['MVFIndC']  + SPF['MVFIdC']  + SPF['SVFIC']

        SPF['MVC']     = SPF['MVndC']    + SPF['MVdC']
        SPF['MVFIC']   = SPF['MVFIndC']  + SPF['MVFIdC']
        SPF['MVPDOC']  = SPF['MVPDOndC'] + SPF['MVPDOdC']

    if iType == "R4F":
        if AADT > 73000 or AADT <= 0: Flag = True; WM += ', AADT (' + str(AADT) + ') for FID = ' + str(GetVal(URow,"FID")) + ' not in range'
        el = Length/5280
        SPF['MVFIC']   = el * math.exp(-5.975 + 1.492 * NaturalLog(AADT/1000))
        SPF['MVFICk']  = 1/(17.6*el)
        SPF['MVPDOC']  = el * math.exp(-6.880 + 1.936 * NaturalLog(AADT/1000))
        SPF['MVPDOCk'] = 1/(18.8*el)
        SPF['MVC']     = SPF['MVFIC'] + SPF['MVPDOC']

        SPF['SVFIC']   = el * math.exp(-2.126 + 0.646 * NaturalLog(AADT/1000))
        SPF['SVFICk']  = 1/(30.1*el)
        SPF['SVPDOC']  = el * math.exp(-2.235 + 0.876 * NaturalLog(AADT/1000))
        SPF['SVPDOCk'] = 1/(20.7*el)
        SPF['SVC']     = SPF['SVFIC'] + SPF['SVPDOC']

        SPF['TOT']     = SPF['MVC']    + SPF['SVC']
        SPF['FI']      = SPF['MVFIC']  + SPF['SVFIC']

    if iType == "U4F":
        if AADT > 110000 or AADT <= 0: Flag = True; WM += ', AADT (' + str(AADT) + ') for FID = ' + str(GetVal(URow,"FID")) + ' not in range'
        el = Length/5280

        SPF['MVFIC']   = el * math.exp(-5.470 + 1.492 * NaturalLog(AADT/1000))
        SPF['MVFICk']  = 1/(17.6*el)
        SPF['MVPDOC']  = el * math.exp(-6.548 + 1.936 * NaturalLog(AADT/1000))
        SPF['MVPDOCk'] = 1/(18.8*el)
        SPF['MVC']     = SPF['MVFIC'] + SPF['MVPDOC']

        SPF['SVFIC']   = el * math.exp(-2.126 + 0.646 * NaturalLog(AADT/1000))
        SPF['SVFICk']  = 1/(30.1*el)
        SPF['SVPDOC']  = el * math.exp(-2.235 + 0.876 * NaturalLog(AADT/1000))
        SPF['SVPDOCk'] = 1/(20.7*el)
        SPF['SVC']     = SPF['SVFIC'] + SPF['SVPDOC']

        SPF['TOT']     = SPF['MVC']    + SPF['SVC']
        SPF['FI']      = SPF['MVFIC']  + SPF['SVFIC']

    if iType == "U6F":
        if AADT > 180000 or AADT <= 0: Flag = True; WM += ', AADT (' + str(AADT) + ') for FID = ' + str(GetVal(URow,"FID")) + ' not in range'
        el = Length/5280

        SPF['MVFIC']   = el * math.exp(-5.587 + 1.492 * NaturalLog(AADT/1000))
        SPF['MVFICk']  = 1/(17.6*el)
        SPF['MVPDOC']  = el * math.exp(-6.809 + 1.936 * NaturalLog(AADT/1000))
        SPF['MVPDOCk'] = 1/(18.8*el)
        SPF['MVC']     = SPF['MVFIC'] + SPF['MVPDOC']

        SPF['SVFIC']   = el * math.exp(-2.055 + 0.646 * NaturalLog(AADT/1000))
        SPF['SVFICk']  = 1/(30.1*el)
        SPF['SVPDOC']  = el * math.exp(-2.274 + 0.876 * NaturalLog(AADT/1000))
        SPF['SVPDOCk'] = 1/(20.7*el)
        SPF['SVC']     = SPF['SVFIC'] + SPF['SVPDOC']

        SPF['TOT']     = SPF['MVC']    + SPF['SVC']
        SPF['FI']      = SPF['MVFIC']  + SPF['SVFIC']

    # Warning Message if flagged
    if Flag: arcpy.AddWarning(WM)
    return SPF
## CMFs
def CMFSkew(URow):
    import math

    Flag = False
    WM   = 'CMF Skew Angle ' 

    CMF_Skew = {"TOT": 1,"FI": 1}

    iType    = GetVal(URow,F_FType['name'])
    if not iType in FTypes:
        Flag = True; WM += ', Type(' + str(iType) + ') not supported'

    Skew1 = GetVal(URow,'Skew1')
    Skew1 = GetVal(URow,F_SKEW1['name'],Skew1)

    Skew2 = GetVal(URow,'Skew2')
    Skew2 = GetVal(URow,F_SKEW2['name'],Skew2)


    if iType == "R3ST":
        if Skew1 >= 90 or Skew1 < 0: Flag = True; WM += ', Skew Angle(' + str(Skew1) + ') for FID = ' + str(GetVal(URow,"FID")) + ' not in range'
        CMF_Skew['TOT'] = math.exp(0.004 * Skew1)
        
    if iType == "R4ST":
        if Skew2 >= 90 or Skew2 < 0: Flag = True; WM += ', Skew Angle(' + str(Skew2) + ') for FID = ' + str(GetVal(URow,"FID")) + ' not in range'
        a = math.exp(0.0054 * Skew1)
        b = math.exp(0.0054 * Skew2)
        CMF_Skew['TOT'] = (a + b) / 2
        
    if iType == "RM3ST":
        if Skew1 >= 90 or Skew1 < 0: Flag = True; WM += ', Skew Angle(' + str(Skew1) + ') for FID = ' + str(GetVal(URow,"FID")) + ' not in range'
        CMF_Skew['TOT'] = 0.016 * Skew1 / (0.98 + 0.016 * Skew1) + 1
        CMF_Skew['FI' ] = 0.017 * Skew1 / (0.52 + 0.017 * Skew1) + 1
        
    if iType == "RM4ST":
        if Skew2 >= 90 or Skew2 < 0: Flag = True; WM += ', Skew Angle(' + str(Skew2) + ') for FID = ' + str(GetVal(URow,"FID")) + ' not in range'
        a = 0.053 * Skew1 / (1.43 + 0.053 * Skew1) + 1
        b = 0.053 * Skew1 / (1.43 + 0.053 * Skew1) + 1
        CMF_Skew['TOT'] = (a + b) / 2
        a = 0.048 * Skew1 / (0.72 + 0.048 * Skew1) + 1
        b = 0.048 * Skew1 / (0.72 + 0.048 * Skew1) + 1
        CMF_Skew['FI'] = (a + b) / 2

    if Flag: arcpy.AddWarning(WM)
    return CMF_Skew
def CMFLTL(URow):

    Flag = False
    WM   = 'CMF LT Lane ' 

    iType    = GetVal(URow,F_FType['name'])
    if not iType in FTypes:
        Flag = True; WM += ', Type(' + str(iType) + ') not supported'

    LTL = GetVal(URow,F_LTL['name'])

    CMF_LTL = {
        "TOT": 1,
        "FI": 1}

    if iType == "R3ST":
        if LTL > 1 or LTL < 0: Flag = True; WM += ', LTL (' + str(LTL) + ') for FID = ' + str(GetVal(URow,"FID")) + ' not in range'
        CMF_LTL['TOT'] = 0.56 ** LTL
    
    if iType == "R4ST":
        if LTL > 2 or LTL < 0: Flag = True; WM += ', LTL (' + str(LTL) + ') for FID = ' + str(GetVal(URow,"FID")) + ' not in range'
        CMF_LTL['TOT'] = 0.72 ** LTL
    
    if iType == "R4SG":
        if LTL > 4 or LTL < 0: Flag = True; WM += ', LTL (' + str(LTL) + ') for FID = ' + str(GetVal(URow,"FID")) + ' not in range'
        CMF_LTL['TOT'] = 0.82 ** LTL
    
    if iType == "RM3ST":
        if LTL > 1 or LTL < 0: Flag = True; WM += ', LTL (' + str(LTL) + ') for FID = ' + str(GetVal(URow,"FID")) + ' not in range'
        CMF_LTL['TOT'] = 0.56 ** LTL
        CMF_LTL['FI' ] = 0.45 ** LTL

    if iType == "RM4ST":
        if LTL > 2 or LTL < 0: Flag = True; WM += ', LTL (' + str(LTL) + ') for FID = ' + str(GetVal(URow,"FID")) + ' not in range'
        CMF_LTL['TOT'] = 0.72 ** LTL
        CMF_LTL['FI' ] = 0.65 ** LTL

    if iType == "U3ST":
        if LTL > 1 or LTL < 0: Flag = True; WM += ', LTL (' + str(LTL) + ') for FID = ' + str(GetVal(URow,"FID")) + ' not in range'
        CMF_LTL['TOT'] = 0.67 ** LTL

    if iType == "U3SG":
        if LTL > 2 or LTL < 0: Flag = True; WM += ', LTL (' + str(LTL) + ') for FID = ' + str(GetVal(URow,"FID")) + ' not in range'
        CMF_LTL['TOT'] = 0.93 ** LTL

    if iType == "U4ST":
        if LTL > 2 or LTL < 0: Flag = True; WM += ', LTL (' + str(LTL) + ') for FID = ' + str(GetVal(URow,"FID")) + ' not in range'
        CMF_LTL['TOT'] = 0.73 ** LTL

    if iType == "U4SG":
        if LTL > 4 or LTL < 0: Flag = True; WM += ', LTL (' + str(LTL) + ') for FID = ' + str(GetVal(URow,"FID")) + ' not in range'
        CMF_LTL['TOT'] = 0.9 ** LTL

    if Flag: arcpy.AddWarning(WM)
    return CMF_LTL
def CMFRTL(URow):

    Flag = False
    WM   = 'CMF RT Lane ' 

    iType    = GetVal(URow,F_FType['name'])
    if not iType in FTypes:
        Flag = True; WM += ', Type(' + str(iType) + ') not supported'

    RTL = GetVal(URow,F_RTL['name'])

    CMF_RTL = {
        "TOT": 1,
        "FI" : 1}

    if iType == "R3ST":
        if RTL > 2 or RTL < 0: Flag = True; WM += ', RTL (' + str(RTL) + ') for FID = ' + str(GetVal(URow,"FID")) + ' not in range'
        CMF_RTL['TC'] = 0.86 ** RTL
    
    if iType == "R4ST":
        if RTL > 4 or RTL < 0: Flag = True; WM += ', RTL (' + str(RTL) + ') for FID = ' + str(GetVal(URow,"FID")) + ' not in range'
        CMF_RTL['TOT'] = 0.86 ** RTL
    
    if iType == "R4SG":
        if RTL > 4 or RTL < 0: Flag = True; WM += ', RTL (' + str(RTL) + ') for FID = ' + str(GetVal(URow,"FID")) + ' not in range'
        CMF_RTL['TOT'] = 0.96 ** RTL
    
    if iType == "RM3ST":
        if RTL > 2 or RTL < 0: Flag = True; WM += ', RTL (' + str(RTL) + ') for FID = ' + str(GetVal(URow,"FID")) + ' not in range'
        CMF_RTL['TOT'] = 0.86 ** RTL
        CMF_RTL['FI' ] = 0.77 ** RTL

    if iType == "RM4ST":
        if RTL > 4 or RTL < 0: Flag = True; WM += ', RTL (' + str(RTL) + ') for FID = ' + str(GetVal(URow,"FID")) + ' not in range'
        CMF_RTL['TOT'] = 0.86 ** RTL
        CMF_RTL['FI' ] = 0.77 ** RTL
    
    if iType == "U3ST":
        if RTL > 2 or RTL < 0: Flag = True; WM += ', RTL (' + str(RTL) + ') for FID = ' + str(GetVal(URow,"FID")) + ' not in range'
        CMF_RTL['TOT'] = 0.86 ** RTL

    if iType == "U3SG":
        if RTL > 2 or RTL < 0: Flag = True; WM += ', RTL (' + str(RTL) + ') for FID = ' + str(GetVal(URow,"FID")) + ' not in range'
        CMF_RTL['TOT'] = 0.96 ** RTL

    if iType == "U4ST":
        if RTL > 4 or RTL < 0: Flag = True; WM += ', RTL (' + str(RTL) + ') for FID = ' + str(GetVal(URow,"FID")) + ' not in range'
        CMF_RTL['TOT'] = 0.86 ** RTL

    if iType == "U4SG":
        if RTL > 4 or RTL < 0: Flag = True; WM += ', RTL (' + str(RTL) + ') for FID = ' + str(GetVal(URow,"FID")) + ' not in range'
        CMF_RTL['TOT'] = 0.96 ** RTL

    if Flag: arcpy.AddWarning(WM)
    return CMF_RTL
def CMFLighting(URow = '', iType = '', Lighting = 0):

    Flag = False
    WM   = 'CMF Lighting ' 

    if URow:
        iType = GetVal(URow,F_FType['name'])
        Lighting = GetVal(URow,'Lighting')
        Lighting = GetVal(URow,F_LIGHTING['name'],Lighting)
    if not iType in FTypes:
        Flag = True; WM += ', Type(' + str(iType) + ') not supported'

    

    Pni = 0
    CMF_Lighting = 1

    if Lighting <> 1 and Lighting <> 0: Flag = True; WM += ', Lighting (' + str(Lighting) + ') for FID = ' + str(GetVal(URow,"FID")) + ' not in range'

    if Lighting == 1:
        if iType == "R3ST":
            Pni = 0.26
            CMF_Lighting = 1.0 - 0.38 * Pni

        if iType == "R4ST":
            Pni = 0.244
            CMF_Lighting = 1.0 - 0.38 * Pni
    
        if iType == "R4SG":
            Pni = 0.286
            CMF_Lighting = 1.0 - 0.38 * Pni
    
        if iType == "RM3ST":
            Pni = 0.276
            CMF_Lighting = 1.0 - 0.38 * Pni

        if iType == "RM4ST":
            Pni = 0.273
            CMF_Lighting = 1.0 - 0.38 * Pni
        
        if iType == "U3ST":
            Pni = 0.238
            CMF_Lighting = 1.0 - 0.38 * Pni
        
        if iType == "U3SG":
            Pni = 0.229
            CMF_Lighting = 1.0 - 0.38 * Pni
        
        if iType == "U4ST":
            Pni = 0.235
            CMF_Lighting = 1.0 - 0.38 * Pni
        
        if iType == "U4SG":
            Pni = 0.235
            CMF_Lighting = 1.0 - 0.38 * Pni

        if iType == "U2U":
            Pinr = 0.424
            Ppnr = 0.576
            Pnr  = 0.316
            CMF_Lighting = 1.0 - (Pnr * (1.0 - 0.72 * Pinr - 0.83 * Ppnr))

        if iType == "U3T":
            Pinr = 0.429
            Ppnr = 0.571
            Pnr  = 0.304
            CMF_Lighting = 1.0 - (Pnr * (1.0 - 0.72 * Pinr - 0.83 * Ppnr))

        if iType == "U4U":
            Pinr = 0.517
            Ppnr = 0.483
            Pnr  = 0.365
            CMF_Lighting = 1.0 - (Pnr * (1.0 - 0.72 * Pinr - 0.83 * Ppnr))

        if iType == "U4D":
            Pinr = 0.364
            Ppnr = 0.636
            Pnr  = 0.410
            CMF_Lighting = 1.0 - (Pnr * (1.0 - 0.72 * Pinr - 0.83 * Ppnr))

        if iType == "U5T":
            Pinr = 0.432
            Ppnr = 0.568
            Pnr  = 0.274
            CMF_Lighting = 1.0 - (Pnr * (1.0 - 0.72 * Pinr - 0.83 * Ppnr))

        if iType == "R2U":
            Pinr = 0.382
            Ppnr = 0.618
            Pnr  = 0.370
            CMF_Lighting = 1.0 - (Pnr * (1.0 - 0.72 * Pinr - 0.83 * Ppnr))

        if iType == "R4U":
            Pinr = 0.361
            Ppnr = 0.639
            Pnr  = 0.255
            CMF_Lighting = 1.0 - (Pnr * (1.0 - 0.72 * Pinr - 0.83 * Ppnr))

        if iType == "R4D":
            Pinr = 0.323
            Ppnr = 0.677
            Pnr  = 0.426
            CMF_Lighting = 1.0 - (Pnr * (1.0 - 0.72 * Pinr - 0.83 * Ppnr))
    
    if Flag: arcpy.AddWarning(WM)
    return CMF_Lighting
def CMFLTP(URow):

    Flag = False
    WM   = 'CMF LT Phasing ' 

    iType    = GetVal(URow,F_FType['name'])
    if not iType in FTypes:
        Flag = True; WM += ', Type(' + str(iType) + ') not supported'

    LTPList = [
        GetVal(URow,F_LTP1['name']),
        GetVal(URow,F_LTP2['name']),
        GetVal(URow,F_LTP3['name']),
        GetVal(URow,F_LTP4['name'])]
    
    T = []
    for LTP in LTPList:
        if   LTP == 0: T.append(1.00)
        elif LTP == 1: T.append(0.99)
        elif LTP == 2: T.append(0.94)
        else: WM += ', LTP (' + str(i) + ') for FID = ' + str(GetVal(URow,"FID")) + ' not in range'

    CMF_LTP = 1
    for i in T:
        CMF_LTP = CMF_LTP * i

    if Flag: arcpy.AddWarning(WM)
    return CMF_LTP
def CMFNoRTR(URow):

    Flag = False
    WM   = 'CMF NoRTR ' 

    iType    = GetVal(URow,F_FType['name'])
    if not iType in FTypes:
        Flag = True; WM += ', Type(' + str(iType) + ') not supported'

    NoRTR    = GetVal(URow,F_No_RTOR['name'])

    CMF_NoRTR = 1
    if iType == "U3SG":
        if NoRTR > 2 or NoRTR < 0: Flag = True; WM += ', NoRTR (' + str(NoRTR) + ') for FID = ' + str(GetVal(URow,"FID")) + ' not in range'
        CMF_NoRTR = 0.98 ** NoRTR

    if iType == "U4SG":
        if NoRTR > 4 or NoRTR < 0: Flag = True; WM += ', NoRTR (' + str(NoRTR) + ') for FID = ' + str(GetVal(URow,"FID")) + ' not in range'
        CMF_NoRTR = 0.98 ** NoRTR

    if Flag: arcpy.AddWarning(WM)
    return CMF_NoRTR
def CMFBus(URow):

    Flag = False
    WM   = 'CMF Bus ' 

    iType    = GetVal(URow,F_FType['name'])
    if not iType in FTypes:
        Flag = True; WM += ', Type(' + str(iType) + ') not supported'

    Bus    = GetVal(URow,'Bus_Stops')
    Bus    = GetVal(URow,F_BUS_STOPS['name'],Bus)

    CMF_Bus = 1

    if iType <> "U3SG" and iType <> "U4SG": Flag = True; WM += ', Type(' + str(iType) + ') not appropriate'

    if Bus ==0:
        CMF_Bus = 1

    elif Bus == 1 or Bus == 2:
        CMF_Bus = 2.78
        
    elif Bus >= 3:
        CMF_Bus = 4.15

    else:
        Flag = True; WM += ', Bus(' + str(Bus) + ') not supported'
    
    if Flag: arcpy.AddWarning(WM)
    return CMF_Bus            
def CMFSchool(URow):

    Flag = False
    WM   = 'CMF School ' 

    iType    = GetVal(URow,F_FType['name'])
    if not iType in FTypes:
        Flag = True; WM += ', Type(' + str(iType) + ') not supported'

    School    = GetVal(URow,'Schools')
    School    = GetVal(URow,F_SCHOOLS['name'],School)

    CMF_School = 1

    if iType <> "U3SG" and iType <> "U4SG": Flag = True; WM += ', Type(' + str(iType) + ') not appropriate'

    if School == 0:
        CMF_School = 1

    if School >= 1:
        CMF_School = 1.35
        
    if Flag: arcpy.AddWarning(WM)
    return CMF_School
def CMFAlco(URow):

    Flag = False
    WM   = 'CMF Alco ' 

    iType    = GetVal(URow,F_FType['name'])
    if not iType in FTypes:
        Flag = True; WM += ', Type(' + str(iType) + ') not supported'

    Alco    = GetVal(URow,'Alco_Sales')
    Alco    = GetVal(URow,F_ALCO_SALES['name'],Alco)
    
    CMF_Alco = 1
    if iType <> "U3SG" and iType <> "U4SG": Flag = True; WM += ', Type(' + str(iType) + ') not appropriate'

    if Alco == 0:
        CMF_Alco = 1

    elif Alco == 1:
        CMF_Alco = 1.12
        
    elif Alco == 2:
        CMF_Alco = 1.56

    else:
        Flag = True; WM += ', Alco(' + str(Alco) + ') not supported'
        

    if Flag: arcpy.AddWarning(WM)
    return CMF_Alco        
def CMFLaneWidth(iType,LaneWidth,AADT):
    import math 
    Flag = False
    WM   = 'CMF LaneWidth ' 

    if not iType in ['R2U', 'R4U', 'R4D', 'U2U', 'U3T', 'U4D', 'U4U', 'U5T','R4F','U4F','U6F']: Flag = True; WM += ', Type(' + str(iType) + ') not appropriate'
    
    CMF_LaneWidth = 1

    if iType in ['R2U']:
        if LaneWidth >= 12:
                CMF_LaneWidth = 1
        
        if LaneWidth >= 11 and LaneWidth < 12:
            if   AADT <= 400:
                CMF_LaneWidth = 1 + 0.01 * (12-LaneWidth)/1.0
            elif AADT > 400 and AADT <= 2000:
                CMF_LaneWidth = 1 + (0.01 + 2.5 * 10**(-5) * (AADT-400)) * (12-LaneWidth)/1.0
            elif AADT > 2000:
                CMF_LaneWidth = 1 + 0.05 * (12-LaneWidth)/1.0

        if LaneWidth >= 10 and LaneWidth < 11:
            if   AADT <= 400:
                CMF_LaneWidth = 1.01 + 0.01 * (11-LaneWidth)/1.0
            elif AADT > 400 and AADT <= 2000:
                CMF_LaneWidth = 1.01 + (0.01 + 1.75 * 10**(-4) * (AADT-400)) * (11-LaneWidth)/1.0
            elif AADT > 2000:
                CMF_LaneWidth = 1.05 + 0.25 * (11-LaneWidth)/1.0

        if LaneWidth <= 9:
            if   AADT <= 400:
                CMF_LaneWidth = 1.05
            elif AADT > 400 and AADT <= 2000:
                CMF_LaneWidth = 1.05 + 2.81 * 10**(-4) * (AADT-400)
            elif AADT > 2000:
                CMF_LaneWidth = 1.50

    if iType in ['R4U']:
        Pra = 0.582
        if LaneWidth >= 12:
                CMF_LaneWidth = 1
        
        if LaneWidth >= 11 and LaneWidth < 12:
            if   AADT <= 400:
                CMF_LaneWidth = 1 + 0.01 * (12-LaneWidth)/1.0
            elif AADT > 400 and AADT <= 2000:
                CMF_LaneWidth = 1 + (0.01 + 1.88 * 10**(-5) * (AADT-400)) * (12-LaneWidth)/1.0
            elif AADT > 2000:
                CMF_LaneWidth = 1 + 0.04 * (12-LaneWidth)/1.0

        if LaneWidth >= 10 and LaneWidth < 11:
            if   AADT <= 400:
                CMF_LaneWidth = 1.01 + 0.01 * (11-LaneWidth)/1.0
            elif AADT > 400 and AADT <= 2000:
                CMF_LaneWidth = 1.01 + (0.01 + 1.31 * 10**(-4) * (AADT-400)) * (11-LaneWidth)/1.0
            elif AADT > 2000:
                CMF_LaneWidth = 1.04 + 0.19 * (11-LaneWidth)/1.0

        if LaneWidth <= 9:
            if   AADT <= 400:
                CMF_LaneWidth = 1.04
            elif AADT > 400 and AADT <= 2000:
                CMF_LaneWidth = 1.04 + 2.13 * 10**(-4) * (AADT-400)
            elif AADT > 2000:
                CMF_LaneWidth = 1.38
        CMF_LaneWidth = (CMF_LaneWidth-1) * Pra + 1

    if iType in ['R4D']:
        Pra = 0.768
        if LaneWidth >= 12:
                CMF_LaneWidth = 1
        
        if LaneWidth >= 11 and LaneWidth < 12:
            if   AADT <= 400:
                CMF_LaneWidth = 1 + 0.01 * (12-LaneWidth)/1.0
            elif AADT > 400 and AADT <= 2000:
                CMF_LaneWidth = 1 + (0.01 + 1.25 * 10**(-5) * (AADT-400)) * (12-LaneWidth)/1.0
            elif AADT > 2000:
                CMF_LaneWidth = 1 + 0.03 * (12-LaneWidth)/1.0

        if LaneWidth >= 10 and LaneWidth < 11:
            if   AADT <= 400:
                CMF_LaneWidth = 1.01 + 0.00 * (11-LaneWidth)/1.0
            elif AADT > 400 and AADT <= 2000:
                CMF_LaneWidth = 1.01 + (0.01 + 8.75 * 10**(-5) * (AADT-400)) * (11-LaneWidth)/1.0
            elif AADT > 2000:
                CMF_LaneWidth = 1.03 + 0.12 * (11-LaneWidth)/1.0

        if LaneWidth <= 9:
            if   AADT <= 400:
                CMF_LaneWidth = 1.03
            elif AADT > 400 and AADT <= 2000:
                CMF_LaneWidth = 1.03 + 1.38 * 10**(-4) * (AADT-400)
            elif AADT > 2000:
                CMF_LaneWidth = 1.25
        CMF_LaneWidth = (CMF_LaneWidth-1) * Pra + 1

    if iType in ['R4F','U4F','U6F']:
        a = -0.0376
        b =  0.963
        if LaneWidth >= 13:
            CMF_LaneWidth = b
        if LaneWidth < 13:
            CMF_LaneWidth = math.exp(a*(LaneWidth-12))
    if Flag: arcpy.AddWarning(WM)
    return CMF_LaneWidth
def CMFShoulderWidthType(iType,ShWidth,ShType,AADT):

    Flag = False
    WM   = 'CMF ShoulderWidth ' 

    if not iType in ['R2U', 'R4U', 'R4D', 'U2U', 'U3T', 'U4D', 'U4U', 'U5T']: Flag = True; WM += ', Type(' + str(iType) + ') not appropriate'

    CMF_ShWidth = 1
    CMF_ShType  = 1
    Output      = 1
    Pra         = 0.617
    if iType in ['R2U','R4U']:
        if ShWidth >= 0 and ShWidth < 1:
            if   AADT <= 400:
                CMF_ShWidth = 1.1
            elif AADT > 400 and AADT <= 2000:
                CMF_ShWidth = 1.1 + (2.5 * 10**(-4) * (AADT-400))
            elif AADT > 2000:
                CMF_ShWidth = 1.5 - (1.5-1.4) * (ShWidth-0)

        if ShWidth >= 1 and ShWidth < 3:
            if   AADT <= 400:
                CMF_ShWidth = 1.07
            elif AADT > 400 and AADT <= 2000:
                CMF_ShWidth = 1.07 + (1.43 * 10**(-4) * (AADT-400))
            elif AADT > 2000:
                CMF_ShWidth = 1.4 - (1.4-1.23) * (ShWidth-1)/(3-1)

        if ShWidth >= 3 and ShWidth < 5:
            if   AADT <= 400:
                CMF_ShWidth = 1.02
            elif AADT > 400 and AADT <= 2000:
                CMF_ShWidth = 1.02 + (8.125 * 10**(-5) * (AADT-400))
            elif AADT > 2000:
                CMF_ShWidth = 1.23 - (1.23-1.08) * (ShWidth-3)/(5-3)

        if ShWidth >= 5 and ShWidth < 7:
                CMF_ShWidth = 1.08 - (1.08-0.94) * (ShWidth-5)/(5-7)

        if ShWidth <= 7:
            if   AADT <= 400:
                CMF_ShWidth = 0.98
            elif AADT > 400 and AADT <= 2000:
                CMF_ShWidth = 0.98 - 6.875 * 10**(-5) * (AADT-400)
            elif AADT > 2000:
                CMF_ShWidth = 0.87

        if ShType == 1: #'Paved':
            CMF_ShType = 1

        if ShType == 2: #'Gravel':
            if ShWidth < 2:
                CMF_ShType = 1
            if ShWidth >= 2 and ShWidth < 6:
                CMF_ShType = 1.01
            if ShWidth >= 6:
                CMF_ShType = 1.02

        if ShType == 3: #'Composite':
            if ShWidth < 1:
                CMF_ShType = 1
            if ShWidth >= 1 and ShWidth < 2:
                CMF_ShType = 1.01
            if ShWidth >= 2 and ShWidth < 4:
                CMF_ShType = 1.02
            if ShWidth >= 4 and ShWidth < 6:
                CMF_ShType = 1.03
            if ShWidth >= 6 and ShWidth < 8:
                CMF_ShType = 1.04
            if ShWidth >= 8:
                CMF_ShType = 1.06

        if ShType == 4: #'Turf':
            if ShWidth < 1:
                CMF_ShType = 1
            if ShWidth >= 1 and ShWidth < 2:
                CMF_ShType = 1.01
            if ShWidth >= 2 and ShWidth < 3:
                CMF_ShType = 1.03
            if ShWidth >= 3 and ShWidth < 4:
                CMF_ShType = 1.04
            if ShWidth >= 4 and ShWidth < 6:
                CMF_ShType = 1.05
            if ShWidth >= 6 and ShWidth < 8:
                CMF_ShType = 1.08
            if ShWidth >= 6:
                CMF_ShType = 1.11
        Output = (CMF_ShWidth * CMF_ShType - 1) * Pra + 1
    
    if iType in ['R4D']:
        if ShWidth >= 8:
            Output = 1.00

        if ShWidth >= 6 and ShWidth < 8:
            Output = 1.04

        if ShWidth >= 4 and ShWidth < 6:
            Output = 1.09

        if ShWidth >= 2 and ShWidth < 4:
            Output = 1.13

        if ShWidth >= 0 and ShWidth < 2:
            Output = 1.18

    if Flag: arcpy.AddWarning(WM)
    return Output
def CMFInsideShoulderW(iType,ShWidth):
    import math
    Flag = False
    WM   = 'CMF Inside ShoulderWidth ' 

    if not iType in ['R4F','U4F','U6F']: Flag = True; WM += ', Type(' + str(iType) + ') not appropriate'

    CMF_ShWidth = {'FI':1,'PDO':1}
    CMF_ShWidth['FI' ] = math.exp(-0.0172*(ShWidth-6))
    CMF_ShWidth['PDO'] = math.exp(-0.0153*(ShWidth-6))

    if Flag: arcpy.AddWarning(WM)
    return CMF_ShWidth
def CMFOutsideShoulderW(iType,ShWidth):
    import math
    Flag = False
    WM   = 'CMF Outside ShoulderWidth ' 

    if not iType in ['R4F','U4F','U6F']: Flag = True; WM += ', Type(' + str(iType) + ') not appropriate'

    CMF_ShWidth = {'FI':1,'PDO':1}
    CMF_ShWidth['FI' ] = math.exp(-0.0897*(ShWidth-10))
    CMF_ShWidth['PDO'] = math.exp(-0.0840*(ShWidth-10))

    if Flag: arcpy.AddWarning(WM)
    return CMF_ShWidth
def CMFHorCurve(iType,Lc,R,S):

    Flag = False
    WM   = 'CMF Hor Curvature ' 

    if not iType in ['R2U', 'R4U', 'R4D', 'U2U', 'U3T', 'U4D', 'U4U', 'U5T','R4F','U4F','U6F']: Flag = True; WM += ', Type(' + str(iType) + ') not appropriate'

    Lc = Lc / 5280.0
    if Lc < 100/5280: Lc = 100/5280
    R = 1/R*5280
    if R < 100: R = 100
    S = 0
    
    CMF_HorCur = {'TOT':1,'MVFI':1,'MVPDO':1,'SVFI':1,'SVPDO':1}
    def FreewayCMF(a,R,P):
        return(1+a*((5730.0/R)**2)*P)

    if iType in ['R2U']:
        CMF_HorCur['TOT'] = (1.55*Lc + 80.2/R - 0.012 * S)/(1.55*Lc)
        if CMF_HorCur['TOT'] < 1: CMF_HorCur['TOT'] = 1
    if iType in ['R4F','U4F','U6F']:
        if R < 1000: R = 1000
        CMF_HorCur['MVFI' ] = FreewayCMF(0.0172,R,1)
        CMF_HorCur['MVPDO'] = FreewayCMF(0.0340,R,1)
        CMF_HorCur['SVFI' ] = FreewayCMF(0.0179,R,1)
        CMF_HorCur['SVPDO'] = FreewayCMF(0.0626,R,1)

    if Flag: arcpy.AddWarning(WM)
    return CMF_HorCur
def CMFGrade(iType,G):

    Flag = False
    WM   = 'CMF Grade' 

    if not iType in ['R2U', 'R4U', 'R4D', 'U2U', 'U3T', 'U4D', 'U4U', 'U5T']: Flag = True; WM += ', Type(' + str(iType) + ') not appropriate'

    
    CMF_Grade = 1

    if iType in ['R2U']:
        if G <= 0.03:
            CMF_Grade = 1.00
        if G > 0.03 and G <= .06:
            CMF_Grade = 1.10
        if G > 0.06:
            CMF_Grade = 1.16

    if Flag: arcpy.AddWarning(WM)
    return CMF_Grade
def CMFDrivewayDensity(iType,DD,AADT):
    import math

    def NaturalLog(A):
        if A > 0:
            return math.log1p(A - 1)
        else:
            return 0
    Flag = False
    WM   = 'CMF Driveway Density ' 

    if not iType in ['R2U', 'R4U', 'R4D', 'U2U', 'U3T', 'U4D', 'U4U', 'U5T']: Flag = True; WM += ', Type(' + str(iType) + ') not appropriate'
    AADT = NaturalLog(AADT)
    CMF_DrwDens = 1

    if iType in ['R2U']:
        CMF_DrwDens = (0.322 + DD*(0.05 - .005*AADT))/(0.322 + 5*(0.05 - .005*AADT))
        if CMF_DrwDens < 1: CMF_DrwDens = 1
    if Flag: arcpy.AddWarning(WM)
    return CMF_DrwDens
def CMFRHR(iType,RHR):
    import math 
    Flag = False
    WM   = 'CMF RHR' 

    if not iType in ['R2U', 'R4U', 'R4D', 'U2U', 'U3T', 'U4D', 'U4U', 'U5T']: Flag = True; WM += ', Type(' + str(iType) + ') not appropriate'

    CMF_RHR = 1

    if iType in ['R2U']:
        CMF_RHR = math.exp(-0.6869+0.0668*RHR)/math.exp(-0.4865)

    if Flag: arcpy.AddWarning(WM)
    return CMF_RHR
def CMFOnStreetParking(iType,OSPParkT,OSPAreaT,OSPPropor):
    # Code Dictionary:
    # 1.	Type : Type of parking (1= Angle Parking; 2= Parallel Parking)
    # 2.	Area_Type: (1=Residential; 2=Industrial; 3=Commercial; 4=Institutional; 5=Other)
    # Fields to read from:
    # F_OSPPropor: Proporsion (ParkL/SegL)
    # F_OSPParkT: Parking type
    # F_OSPAreaT: Area Type
    
    Flag = False
    WM   = 'CMF On Street Parking' 

    #iType    = GetVal(URow,F_FType['name'])
    if not iType in ['R2U', 'R4U', 'R4D', 'U2U', 'U3T', 'U4D', 'U4U', 'U5T']:
        Flag = True; WM += ', Type(' + str(iType) + ') not supported'

    #OSPPropor  = GetVal(URow,F_OSPPropor['name'])
    #OSPParkT   = GetVal(URow,F_OSPParkT ['name'])
    #OSPAreaT   = GetVal(URow,F_OSPAreaT ['name'])

    Factor        = 1
    if iType in ['U2U']:
        if OSPParkT in [2]: # Parallel
            if OSPAreaT in [1,5]: # Resi Other
                Factor = 1.465
            if OSPAreaT in [2,3,4]: # Comm Indus Instit
                Factor = 2.074

        if OSPParkT in [1]: # Angle
            if OSPAreaT in [1,5]: # Resi Other
                Factor = 3.428
            if OSPAreaT in [2,3,4]: # Comm Indus Instit
                Factor = 4.853

    if iType in ['U3T']:
        if OSPParkT in [2]: # Parallel
            if OSPAreaT in [1,5]: # Resi Other
                Factor = 1.465
            if OSPAreaT in [2,3,4]: # Comm Indus Instit
                Factor = 2.074

        if OSPParkT in [1]: # Angle
            if OSPAreaT in [1,5]: # Resi Other
                Factor = 3.428
            if OSPAreaT in [2,3,4]: # Comm Indus Instit
                Factor = 4.853

    if iType in ['U4U']:
        if OSPParkT in [2]: # Parallel
            if OSPAreaT in [1,5]: # Resi Other
                Factor = 1.100
            if OSPAreaT in [2,3,4]: # Comm Indus Instit
                Factor = 2.709

        if OSPParkT in [1]: # Angle
            if OSPAreaT in [1,5]: # Resi Other
                Factor = 2.574
            if OSPAreaT in [2,3,4]: # Comm Indus Instit
                Factor = 3.999

    if iType in ['U4D']:
        if OSPParkT in [2]: # Parallel
            if OSPAreaT in [1,5]: # Resi Other
                Factor = 1.100
            if OSPAreaT in [2,3,4]: # Comm Indus Instit
                Factor = 2.709

        if OSPParkT in [1]: # Angle
            if OSPAreaT in [1,5]: # Resi Other
                Factor = 2.574
            if OSPAreaT in [2,3,4]: # Comm Indus Instit
                Factor = 3.999

    if iType in ['U5T']:
        if OSPParkT in [2]: # Parallel
            if OSPAreaT in [1,5]: # Resi Other
                Factor = 1.100
            if OSPAreaT in [2,3,4]: # Comm Indus Instit
                Factor = 2.709

        if OSPParkT in [1]: # Angle
            if OSPAreaT in [1,5]: # Resi Other
                Factor = 2.574
            if OSPAreaT in [2,3,4]: # Comm Indus Instit
                Factor = 3.999

    CMF_OnStrPark = 1 + OSPPropor * (Factor - 1.0)

    if Flag: arcpy.AddWarning(WM)
    return CMF_OnStrPark
def CMFMedianWidth(iType,MW):
   
    Flag = False
    WM   = 'CMF Median Width' 

    #iType    = GetVal(URow,F_FType['name'])
    if not iType in ['R2U', 'R4U', 'R4D', 'U2U', 'U3T', 'U4D', 'U4U', 'U5T','R4F','U4F','U6F']:
        #Flag = True; 
        WM += ', Type(' + str(iType) + ') not supported'

    CMF_MW        = 1
    if iType in ['R4D']:
        if MW <= 10:
            CMF_MW = 1.04
        if MW > 10  and MW <= 20:
            CMF_MW = (1.04-1.02)/(10-20)*(MW-20)+1.02
        if MW > 20  and MW <= 30:
            CMF_MW = (1.02-1.00)/(20-30)*(MW-30)+1.00
        if MW > 30  and MW <= 40:
            CMF_MW = (1.00-0.99)/(30-40)*(MW-40)+0.99
        if MW > 40  and MW <= 50:
            CMF_MW = (0.99-0.97)/(40-50)*(MW-50)+0.97
        if MW > 50  and MW <= 60:
            CMF_MW = (0.97-0.96)/(50-60)*(MW-60)+0.96
        if MW > 60  and MW <= 70:
            CMF_MW = 0.96
        if MW > 70  and MW <= 80:
            CMF_MW = (0.96-0.95)/(70-80)*(MW-80)+0.95
        if MW > 90  and MW <= 100:
            CMF_MW = 0.94
        if MW > 100: 
            CMF_MW = 0.94

    if iType in ['U4D']:
        if MW <= 10:
            CMF_MW = 1.01
        if MW > 10  and MW <= 15:
            CMF_MW = (1.01-1.00)/(10-15)*(MW-15)+1.00
        if MW > 15  and MW <= 20:
            CMF_MW = (1.00-0.99)/(15-20)*(MW-20)+0.99
        if MW > 20  and MW <= 80:
            CMF_MW = (0.99-0.93)/(20-80)*(MW-80)+0.93
        if MW > 80  and MW <= 90:
            CMF_MW = 0.93
        if MW > 90  and MW <= 100:
            CMF_MW = (0.93-0.92)/(90-100)*(MW-100)+0.92
        if MW > 100: 
            CMF_MW = 0.92

    if iType in ['R4F','U4F','U6F']:
        CMF_MV = 1
    if Flag: arcpy.AddWarning(WM)
    if CMF_MW == 1:
        if MW <> 0:
           CMF_MW = 1.0001
        else:
            CMF_MW = 1
    return CMF_MW
def CMFMedianBarrier(iType,MW,MType,SWi):
    import math
    Flag = False
    WM   = 'CMF Median Width and Median Barrier ' 

    if not iType in ['R4F','U4F','U6F']: Flag = True; WM += ', Type(' + str(iType) + ') not appropriate'

    CMF_MB = {'MVFI':1,'MVPDO':1,'SVFI':1,'SVPDO':1}
    if MW>90: MW=90
    if MW<9: MW = 9
    if SWi<2: SWi = 2
    if SWi>12: SWi = 12

    if MType in [1,2,3]:
        CMF_MB['MVFI' ] = math.exp(-0.00302*(MW-2*SWi-48))
        CMF_MB['MVPDO'] = math.exp(-0.00291*(MW-2*SWi-48))
        CMF_MB['SVFI' ] = math.exp(+0.00102*(MW-2*SWi-48))
        CMF_MB['SVPDO'] = math.exp(-0.00289*(MW-2*SWi-48))
    if MType in [4,5,6]:
        if MW>34: MW=34
        if MW<9: MW = 9
        CMF_MB['MVFI' ] = math.exp(-0.00302*(MW-48)) * math.exp(0.131/(MW/2))
        CMF_MB['MVPDO'] = math.exp(-0.00291*(MW-48)) * math.exp(0.169/(MW/2))
        CMF_MB['SVFI' ] = math.exp(+0.00102*(MW-48)) * math.exp(0.131/(MW/2))
        CMF_MB['SVPDO'] = math.exp(-0.00289*(MW-48)) * math.exp(0.169/(MW/2))

    if Flag: arcpy.AddWarning(WM)
    return CMF_MB
def CMFFixedObjects(iType,Density,Offset):
   
    Flag = False
    WM   = 'CMF Fixed Objects'

    #iType    = GetVal(URow,F_FType['name'])
    if not iType in ['R2U', 'R4U', 'R4D', 'U2U', 'U3T', 'U4D', 'U4U', 'U5T']:
        #Flag = True; 
        WM += ', Type(' + str(iType) + ') not supported'

    #OSPPropor  = GetVal(URow,F_OSPPropor['name'])
    #OSPParkT   = GetVal(URow,F_OSPParkT ['name'])
    #OSPAreaT   = GetVal(URow,F_OSPAreaT ['name'])

    Pfo    = 0
    if iType in ['U2U']:
        Pfo = 0.059
    if iType in ['U3T']:
        Pfo = 0.034
    if iType in ['U4U']:
        Pfo = 0.037
    if iType in ['U4D']:
        Pfo = 0.036
    if iType in ['U5T']:
        Pfo = 0.016

    Foffset = 0
    if Offset <= 2:
        Foffset = 0.232
    if Offset > 2 and Offset <= 5:
        Foffset = (0.133 - 0.232) / (5 - 2) * (Offset - 5) + 0.133
    if Offset > 5 and Offset <= 10:
        Foffset = (0.087 - 0.133) / (10 - 5) * (Offset - 10) + 0.087
    if Offset > 10 and Offset <= 15:
        Foffset = (0.068 - 0.087) / (15 - 10) * (Offset - 15) + 0.068
    if Offset > 15 and Offset <= 20:
        Foffset = (0.057 - 0.068) / (20 - 15) * (Offset - 20) + 0.057
    if Offset > 20 and Offset <= 25:
        Foffset = (0.049 - 0.057) / (25 - 20) * (Offset - 25) + 0.049
    if Offset > 25 and Offset <= 30:
        Foffset = (0.044 - 0.049) / (30 - 25) * (Offset - 30) + 0.044
    if Offset > 30: 
        Foffset = 0.044

    CMF_FO = Foffset * Density * Pfo + (1-Pfo)
    if CMF_FO < 1: 
        if Density <> 0: 
            CMF_FO = 1.00001
        else:
            CMF_FO = 1
    if Flag: arcpy.AddWarning(WM)
    return CMF_FO
def CMFLaneChange(iType,Dict):
    import math
    Flag = False
    WM   = 'CMF Lane Change'

    #iType    = GetVal(URow,F_FType['name'])
    if not iType in ['R4F', 'U4F', 'U6F']:
        #Flag = True; 
        WM += ', Type(' + str(iType) + ') not supported'

    a=0.175;b=12.56;c=0.001;d=-0.272
    Pwevinc = Dict['LsWevInc']/Dict['Ls']
    Pwevdec = Dict['LsWevDec']/Dict['Ls']
    fwevinc = 1-Pwevinc+Pwevinc*math.exp(a/Dict['LWevInc'])
    fwevdec = 1-Pwevdec+Pwevdec*math.exp(a/Dict['LWevDec'])
    A = -b*Dict['XbEnt']+d*NaturalLog(c*Dict['AADTbEnt'])
    flcinc1 = 1 + math.exp(A)/b/Dict['Ls']*(1-math.exp(-b*Dict['Ls']))
    A = -b*Dict['XeExt']+d*NaturalLog(c*Dict['AADTeExt'])
    flcinc2 = 1 + math.exp(A)/b/Dict['Ls']*(1-math.exp(-b*Dict['Ls']))
    flcinc = flcinc1*flcinc2

    A = -b*Dict['XeEnt']+d*NaturalLog(c*Dict['AADTeEnt'])
    flcdec1 = 1 + math.exp(A)/b/Dict['Ls']*(1-math.exp(-b*Dict['Ls']))
    A = -b*Dict['XbExt']+d*NaturalLog(c*Dict['AADTbExt'])
    flcdec2 = 1 + math.exp(A)/b/Dict['Ls']*(1-math.exp(-b*Dict['Ls']))
    flcdec = flcdec1*flcdec2

    CMF_LC_FI = 0.5*fwevinc*flcinc + 0.5*fwevdec*flcdec

    a=0.123;b=13.46;c=0.001;d=-0.283
    fwevinc = 1-Pwevinc+Pwevinc*math.exp(a/Dict['LWevInc'])
    fwevdec = 1-Pwevdec+Pwevdec*math.exp(a/Dict['LWevDec'])
    A = -b*Dict['XbEnt']+d*NaturalLog(c*Dict['AADTbEnt'])
    flcinc1 = 1 + math.exp(A)/b/Dict['Ls']*(1-math.exp(-b*Dict['Ls']))
    A = -b*Dict['XeExt']+d*NaturalLog(c*Dict['AADTeExt'])
    flcinc2 = 1 + math.exp(A)/b/Dict['Ls']*(1-math.exp(-b*Dict['Ls']))
    flcinc = flcinc1*flcinc2

    A = -b*Dict['XeEnt']+d*NaturalLog(c*Dict['AADTeEnt'])
    flcdec1 = 1 + math.exp(A)/b/Dict['Ls']*(1-math.exp(-b*Dict['Ls']))
    A = -b*Dict['XbExt']+d*NaturalLog(c*Dict['AADTbExt'])
    flcdec2 = 1 + math.exp(A)/b/Dict['Ls']*(1-math.exp(-b*Dict['Ls']))
    flcdec = flcdec1*flcdec2

    CMF_LC_PDO = 0.5*fwevinc*flcinc + 0.5*fwevdec*flcdec
    
    CMF_LC = {'FI':1,'PDO':1}
    CMF_LC['FI' ] = CMF_LC_FI
    CMF_LC['PDO'] = CMF_LC_PDO
    if Flag: arcpy.AddWarning(WM)
    return CMF_LC
def CMFCZandOB(iType,Pob,Whc,Wocb,Ws):
    import math
    Flag = False
    WM   = 'CMF Outside Clearance'

    #iType    = GetVal(URow,F_FType['name'])
    if not iType in ['R4F', 'U4F', 'U6F']:
        #Flag = True; 
        WM += ', Type(' + str(iType) + ') not supported'

    
    CMF_OC_FI = (1-Pob)*math.exp(-0.00451*(Whc-Ws-20))+Pob*math.exp(-.00451*(Wocb-20))

    a=0.131
    CMF_OB_FI  = (1-Pob)+Pob*math.exp(a/Wocb)
    a=0.169
    CMF_OB_PDO = (1-Pob)+Pob*math.exp(a/Wocb)
    
    CMF_OB = {'FI':1,'PDO':1}
    CMF_OB['FI' ] = CMF_OB_FI
    CMF_OB['PDO'] = CMF_OB_PDO
    if Flag: arcpy.AddWarning(WM)
    return [CMF_OC_FI,CMF_OB]
def CMFHighVolume(iType,Phv):
    import math
    Flag = False
    WM   = 'CMF Outside Clearance'

    #iType    = GetVal(URow,F_FType['name'])
    if not iType in ['R4F', 'U4F', 'U6F']:
        #Flag = True; 
        WM += ', Type(' + str(iType) + ') not supported'

    if Phv<0:Phv=0
    if Phv>1:Phv=1
    a=0.350
    CMF_HV_MVFI  = math.exp(a*Phv)
    a=0.283
    CMF_HV_MVPDO = math.exp(a*Phv)
    a=-0.0675
    CMF_HV_SVFI  = math.exp(a*Phv)
    a=-0.611
    CMF_HV_SVPDO = math.exp(a*Phv)
    
    CMF_HV = {'MVFI':CMF_HV_MVFI,'MVPDO':CMF_HV_MVPDO,'SVFI':CMF_HV_SVFI,'SVPDO':CMF_HV_SVPDO}

    if Flag: arcpy.AddWarning(WM)
    return CMF_HV
def CompareRCT(CrashRCT,RIMSRCT):
        ConvertDic = {1:1,2:2,3:4,4:7,5:9}
        Flag = False
        if CrashRCT in ConvertDic.keys():
            if RIMSRCT == ConvertDic[CrashRCT]:
                Flag = True
        return Flag

## General Functions
def ExpectedCrash(OC, Sel_PC, PCList, k):
    if not OC: OC = 0
    PC_Sum = 0
    for PC in PCList:
        PC_Sum += PC 
    w = 1 / (1 + k * PC_Sum)
    return w * Sel_PC + (1 - w) * OC
def GetANO(Row, IntErr=-1, RowErr=99999999):
        if Row:
            ANO = Row.getValue('ANO')
            try:
                ANO = int(ANO)
            except:
                ANO = IntErr
        else:
            ANO = RowErr
        return ANO
def ConvertType(Value, Type):
        if   Type in ['TEXT']:
            try:
                fval = str(Value)
            except:
                fval = None
        elif Type in ['SHORT', 'LONG']:
            try:
                fval = int(Value)
            except:
                fval = None
        elif Type in ['DOUBLE']:
            try:
                fval = float(Value)
            except:
                fval = None
        return fval
def SOEExtract(SOE):
        Flag = False
        if not SOE:
            Flag = True
        if type(SOE) <> str:
            SOE = str(SOE)
        try:
            a = int(SOE)
        except:
            Flag = True
        SOE1 = 0
        SOE2 = 0
        SOE3 = 0
        SOE4 = 0
        if not Flag:
            n = len(SOE)
            if   n in [1,2]:
                SOE1 = int(SOE)
            elif n == 3:
                c1 = int(SOE[0])
                c23 = int(SOE[1:3])
                SOE1 = c1
                SOE2 = c23
            elif n == 4:
                c12 = int(SOE[0:2])
                c34 = int(SOE[2:4])
                SOE1 = c12
                SOE2 = c34
            elif n == 5:
                c1 = int(SOE[0])
                c23 = int(SOE[1:3])
                c45 = int(SOE[3:5])
                SOE1 = c1
                SOE2 = c23
                SOE3 = c45
            elif n == 6:
                c12 = int(SOE[0:2])
                c34 = int(SOE[2:4])
                c56 = int(SOE[4:6])
                SOE1 = c12
                SOE2 = c34
                SOE3 = c56
            elif n == 7:
                c1 = int(SOE[0])
                c23 = int(SOE[1:3])
                c45 = int(SOE[3:5])
                c67 = int(SOE[5:7])
                SOE1 = c1
                SOE2 = c23
                SOE3 = c45
                SOE4 = c67
            elif n == 8:
                c12 = int(SOE[0:2])
                c34 = int(SOE[2:4])
                c56 = int(SOE[4:6])
                c78 = int(SOE[6:8])
                SOE1 = c12
                SOE2 = c34
                SOE3 = c56
                SOE4 = c78
        return [SOE1,SOE2,SOE3,SOE4]

## Tool Scripts
def ImpotCrashAttributes(CrashInput,LocInput,Output):
    arcpy.AddMessage("    ")
    arcpy.AddMessage("    Import Crash Attributes")

    OutDic = OutputParser(Output, 'shp')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("    Copy: Crash Layer")
    arcpy.Delete_management('CAtt_Sort_Crash')
    if arcpy.Describe(CrashInput).dataType in ['FeatureLayer','FeatureClass']:
        CrashLayer = CopyFeatures(CrashInput,'CAtt_Sort_Crash')
    else:
        arcpy.Delete_management('CAtt_Sort_Crash')
        CrashLayer = arcpy.CopyRows_management(CrashInput,'CAtt_Sort_Crash')

    C = arcpy.GetCount_management(CrashLayer)
    arcpy.AddMessage("     - Total Items Found: " + str(C))

    arcpy.AddMessage("    Count: Location File")
    LocFile = LocInput
    U = arcpy.GetCount_management(LocFile)
    arcpy.AddMessage("     - Total Items Found: " + str(U))

    arcpy.AddMessage("    Add Field: Crash Layer")
    CrashTypeDic = [F_CT_CTY, F_CT_RCT, F_CT_RTN, F_CT_ALS, F_CT_RAI, F_CT_LOA, F_CT_ART, F_CT_DLR,
                    F_CT_BIR, F_CT_BRN, F_CT_ALSB, F_CT_BRA,
                    F_CT_SIC, F_CT_SRN, F_CT_ALSS, F_CT_SRA, F_CT_BDI, F_CT_BDO, F_CT_ODR,
                    F_CT_DAT, F_CT_DAY, F_CT_TIM, F_CT_PNT, F_CT_PAT, 
                    F_CT_ALC, F_CT_WCC, F_CT_RSC, F_CT_AHC,F_CT_TWAY, F_CT_TCT, F_CT_JCT,
                    F_CT_UNT, F_CT_FHE, F_CT_HEL, F_CT_XWK, F_CT_PRC, F_CT_OCF1, F_CT_OCF2, F_CT_OCF3, F_CT_OCF4, F_CT_MAC,  
                    F_CT_FAT, F_CT_INJ,
                    F_CT_JUR,
                    F_CT_WZN, F_CT_WZT, F_CT_WZL, F_CT_WPR,
                    F_CT_REPORT]
    for Field in CrashTypeDic:
        arcpy.DeleteField_management(CrashLayer,Field['name'])
    AddField(CrashLayer,F_CT_Label)
    CalField(CrashLayer,F_CT_Label,'!ANO!')
    for Field in CrashTypeDic:
        AddField(CrashLayer,Field)

    arcpy.AddMessage("    Search Cursor: Location File")
    LocDic = {GetANO(SRow):{} for SRow in arcpy.SearchCursor(LocFile)}
    SC = arcpy.SearchCursor(LocFile)
    for SRow in SC:
        ANO = GetANO(SRow)
        for Field in CrashTypeDic:
            try:
                if Field['name']=='DAY_':
                    Val = SRow.getValue('DAY')
                else:
                    Val = SRow.getValue(Field['name'])
            except:
                Val = ''
            LocDic[ANO].update({Field['name']:Val})

    arcpy.AddMessage("    Update Cursor: Crash Layer")
    UC = arcpy.UpdateCursor(CrashLayer)

    arcpy.SetProgressor("step","Import Crash Attributes - Location File",0,100,1)
    arcpy.SetProgressorLabel("Update Crash Layer:")
    arcpy.SetProgressorPosition(0)
    PP = 0
    i = 0
    for URow in UC:
        FID = GetFID(URow)
        ANO = GetANO(URow)
        if ANO in LocDic.keys():
            i += 1
            for Field in CrashTypeDic:
                URow.setValue(Field['name'],ConvertType(LocDic[ANO][Field['name']],Field['type']))
                #arcpy.AddMessage(str([Field['name'],ConvertType(LocDic[ANO][Field['name']],Field['type'])]))
        UC.updateRow(URow)
        NewPP = (100 * FID) / int(str(C))
        if NewPP > PP:
            arcpy.SetProgressorPosition(NewPP)
            PP = NewPP

    arcpy.AddMessage("    Total Crashes Updated: " + str(i))
    if arcpy.Describe(CrashInput).dataType in ['FeatureLayer','FeatureClass']:
        Output = arcpy.CopyFeatures_management(CrashLayer,Output)
    else:
        Output = arcpy.CopyRows_management(CrashLayer,Output)
    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")
def ImpotUnitAttributes(UnitInput,CrashYear,Output):
    arcpy.AddMessage("    ")
    arcpy.AddMessage("    Import Unit Crash Attributes")
    CrashYear = int(CrashYear)

    OutDic = OutputParser(Output, 'shp')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("    Create Table")
    arcpy.Delete_management('UTable')
    Tab = CreateTable(arcpy.env.workspace,"UTable")

    UnitDic1 = [F_CT_AUN,
               F_CT_DOB, F_CT_DSEX, F_CT_DRAC, 
               F_CT_VMK, F_CT_VYR, F_CT_RPS, F_CT_VRY, F_CT_RPN, F_CT_NOC, F_CT_UTC, F_CT_VUC, F_CT_VAT, F_CT_VEW, F_CT_VIN,
               F_CT_MHE, F_CT_MAN,F_CT_CTA, F_CT_SOE]
    UnitDic2 = [F_CT_API,
                F_CT_DLN, F_CT_DLC, F_CT_DLS,
                F_CT_VLC1, F_CT_VLC2, F_CT_VLC3, F_CT_DTG, F_CT_DTT, F_CT_DTR, F_CT_UOR,
                F_CT_EDAM, F_CT_EAD, F_CT_MDA, F_CT_FDA, F_CT_EDP, F_CT_PD2,
                F_CT_ECS, F_CT_SPL, F_CT_DOT]
    UTC   = {1:"AUTOMOBILE",
            12:	"PICKUP TRUCK",
            13:	"TRUCK TRACTOR",
            14:	"OTHER TRUCK",
            15:	"FULL SIZE VAN",
            16:	"MINI-VAN",
            17:	"SPORT UTILITY",
            25:	"MOTORCYCLE",
            26:	"OTHER MOTOR BIKE",
            27:	"PEDALCYCLE",
            38:	"ANIMAL DRAWN VEHICLE",
            39:	"ANIMAL (RIDDEN)",
            41:	"PEDESTRIAN",
            51:	"TRAIN",
            61:	"SCHOOL BUS",
            62:	"PASSENGER BUS",
            98:	"OTHER",
            99:	"UNKNOWN (HIT AND RUN ONLY)"}


    arcpy.AddMessage("    Add Field: Crash Layer")
    AddField(Tab,F_CT_Label)
    AddField(Tab,F_CT_ID)
    AddField(Tab,F_CT_ANO)
    for Field in UnitDic1:
        AddField(Tab,Field)
    for Field in [F_CT_SOE1,F_CT_SOE2,F_CT_SOE3,F_CT_SOE4]:
        AddField(Tab,Field)
    for Field in UnitDic2:
        AddField(Tab,Field)
    UnitDic = UnitDic1 + UnitDic2

    arcpy.AddMessage("    Search Cursor: Unit File")
    Dic = []
    SC = arcpy.SearchCursor(UnitInput)
    for SRow in SC:
        ANO = GetANO(SRow)
        if ANO>=(CrashYear-2000)*10**6 and ANO<(CrashYear-2000)*10**6+999999 and ANO<>99999999:
            s={'ANO':ANO}
            for Field in UnitDic:
                #arcpy.AddMessage(Field['name'])
                val = SRow.getValue(Field['name'])
                s.update({Field['name']:ConvertType(val,Field['type'])})
            Dic.append(s)
    arcpy.AddMessage("    Insert Cursor: Unit Table")
    IC = arcpy.InsertCursor(Tab)
    for Rec in Dic:
        ANO = Rec['ANO']
        if ANO<>99999999:
            IRow = IC.newRow()
            IRow.setValue('ANO',ANO)
            if Rec['AUN']>0:
                IRow.setValue('ID',long(str(ANO)+str(Rec['AUN'])))
            else:
                IRow.setValue('ID',long(str(ANO)+str(0)))
            if Rec['UTC'] in UTC.keys():
                IRow.setValue(F_CT_Label['name'],str(Rec['AUN'])+": "+UTC[Rec['UTC']])
            else:
                IRow.setValue(F_CT_Label['name'],str(Rec['AUN'])+": "+str(Rec['UTC']))

            for Field in UnitDic:
                IRow.setValue(Field['name'],Rec[Field['name']])
            SOEs = SOEExtract(Rec[F_CT_SOE['name']])
            IRow.setValue(F_CT_SOE1['name'],SOEs[0])
            IRow.setValue(F_CT_SOE2['name'],SOEs[1])
            IRow.setValue(F_CT_SOE3['name'],SOEs[2])
            IRow.setValue(F_CT_SOE4['name'],SOEs[3])

            IC.insertRow(IRow)

    arcpy.Delete_management('UTableS')
    Tab = Sort(Tab,'UTableS','ANO;AUN')

    Output = arcpy.CopyRows_management(Tab,Output)
    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")
def ImpotOccAttributes(UnitInput,CrashYear,Output):
    arcpy.AddMessage("    ")
    arcpy.AddMessage("    Import Occ Crash Attributes")
    CrashYear = int(CrashYear)

    OutDic = OutputParser(Output, 'shp')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("    Create Table")
    arcpy.Delete_management('UTable')
    Tab = CreateTable(arcpy.env.workspace,"UTable")

    UnitDic = [F_CT_AUN,
               F_CT_OCCZIP, F_CT_OSEX, F_CT_ORAC, F_CT_AGE, F_CT_DBIR,
               F_CT_SEV, F_CT_MHI,
               F_CT_OSL, F_CT_REU, F_CT_LAI, F_CT_EJE,F_CT_AIR, F_CT_SWT
               ]
    OSL =  {1:	'Driver Seat',
            2:	'Front Seat - Middle',
            3:	'Front Seat - Far Right',
            4:	'2nd Row - Behind Driver',
            5:	'2nd Row - Middle',
            6:	'2nd Row - Far Right',
            7:	'3rd Row - Behind Driver',
            8:	'3rd Row - Middle',
            9:	'3rd Row - Far Right',
            20:	'Pedestrian',
            30:	'Trailing Unit',
            40:	'4th Row or Higher',
            50:	'Enclosed Passenger',
            51:	'Unenclosed Passenger',
            60:	'Sleeper Birth',
            70:	'Vehicle Exterior',
            80:	'Lap',
            99:	'Unknown'}

    arcpy.AddMessage("    Add Field: Crash Layer")
    AddField(Tab,F_CT_Label)
    AddField(Tab,F_CT_ID)
    AddField(Tab,F_CT_ANO)
    for Field in UnitDic:
        AddField(Tab,Field)

    arcpy.AddMessage("    Search Cursor: Occ File")
    Dic = []
    SC = arcpy.SearchCursor(UnitInput)
    i = 0
    for SRow in SC:
        i = i + 1
        ANO = GetANO(SRow)
        if ANO>=(CrashYear-2000)*10**6 and ANO<(CrashYear-2000)*10**6+999999 and ANO<>99999999:
            s={'ANO':ANO}
            for Field in UnitDic:
                val = SRow.getValue(Field['name'])
                s.update({Field['name']:ConvertType(val,Field['type'])})
            Dic.append(s)
    arcpy.AddMessage("    Insert Cursor: Occ Table")
    IC = arcpy.InsertCursor(Tab)
    for Rec in Dic:
        ANO = Rec['ANO']
        if ANO<>99999999:
            IRow = IC.newRow()
            IRow.setValue('ANO',ANO)
            if Rec['AUN']>0:
                IRow.setValue('ID',long(str(ANO)+str(Rec['AUN'])))
            else:
                IRow.setValue('ID',ANO)
            if Rec['OSL'] in OSL.keys():
                IRow.setValue(F_CT_Label['name'],OSL[Rec['OSL']])
            else:
                IRow.setValue(F_CT_Label['name'],str(Rec['OSL']))
            for Field in UnitDic:
                IRow.setValue(Field['name'],Rec[Field['name']])
            IC.insertRow(IRow)

    arcpy.Delete_management('UTableS')
    Tab = Sort(Tab,'UTableS','ANO;AUN')
    Output = arcpy.CopyRows_management(Tab,Output)
    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")
def CreateGeodatabase(Loc,Unit,Occ,Out,Year,Output):
    arcpy.AddMessage("    ")
    arcpy.AddMessage("    Create Geodatabase")
    Year = long(Year)
    OutDic = OutputParser(Output, 'mdb')

    GDB = arcpy.CreatePersonalGDB_management(OutDic['folder'], OutDic['file'])
    arcpy.AddMessage("    Import Location Features")
    LocTable = arcpy.FeatureClassToFeatureClass_conversion(Loc, GDB, "Loc" + str(Year))

    arcpy.AddMessage("    Import Unit Table")
    UnitTable = arcpy.TableToTable_conversion(Unit, GDB, "Unit" + str(Year))

    arcpy.AddMessage("    Import Occ Table")
    OccTable = arcpy.TableToTable_conversion(Occ, GDB, "Occ" + str(Year))

    arcpy.AddMessage("    Import Out Table")
    OutTable = arcpy.TableToTable_conversion(Out, GDB, "Out" + str(Year))

    arcpy.AddMessage("    Create Relationships")
    #arcpy.AddMessage(str([LocTable, UnitTable, OutDic['folder']+OutDic['file']+"\\Loc-Unit"]))
    arcpy.CreateRelationshipClass_management(LocTable, UnitTable, OutDic['folder']+OutDic['file']+"\\Loc-Unit", "SIMPLE", "Unit Table", "Loc Table"         , "FORWARD", "ONE_TO_MANY", "NONE", "ANO", "ANO")    
    arcpy.CreateRelationshipClass_management(OutTable, UnitTable, OutDic['folder']+OutDic['file']+"\\Out-Unit", "SIMPLE"   , "Unit Table", "Out of State Table", "FORWARD", "ONE_TO_MANY", "NONE", "ANO", "ANO")    
    arcpy.CreateRelationshipClass_management(UnitTable, OccTable, OutDic['folder']+OutDic['file']+"\\Unit-Occ", "SIMPLE", "Occ Table" , "Unit Table"        , "FORWARD", "ONE_TO_MANY", "NONE", "ID", "ID")    
    
    arcpy.AddMessage("    Assign Domains")
    Domains     = {
    'RCT':{1: "Interstate",
        2: "US Route",
        3: "SC Route",
        4: "Secondary Route",
        5: "Local Route"},
    'RAI':{0:	'Main Line',
    2:	'Alternate Route',
    5:	'Spur',
    6:	'Connection',
    7:	'Business',
    9:	'Other'},
    'DLR':{'N':'North',
           'E':'East',
           'W':'West',
           'S':'South'},
    'ART':{0:	'Exit',        1:	'Entrance',        -1:'Blank'},
    'BDI':{'M':	'Mile',        'F':	'Feet'},
    'DAY_':{1:'Sunday',
        2:'Monday',
        3:'Tuesday',
        4:'Wednesday',
        5:'Thursday',
        6:'Friday',
        7:'Saturday'},
    'ALC':{1:'DAYLIGHT (Full daylight)',
    2:'DAWN (Early morning light)',
    3:'DUSK (Early evening light)',
    4:'DARK (Lighting unspecified)',
    5:'DARK (Street lamp lit)',
    6:'DARK (Street lamp not lit)',
    7:'DARK (No lights)'},
    'WCC':{1:'CLEAR (NO ADVERSE CONDITIONS)',
2:'RAIN',
3:'CLOUDY',
4:'SLEET/HAIL',
5:'SNO ',
6:'FOG, SMOG, SMOKE',
7:'BLOWING SAND, OIL, DIRT, OR SNOW',
8:'SEVERE CROSSWINDS',
9:'UNKNOWN'},
    'RSC':{1:'DRY',
2:'WET',
3:'SNOW',
4:'SLUSH',
5:'ICE',
6:'CONTAMINATE',
7:'WATER (STANDING, ETC.)',
8:'OTHER',
9:'UNKNOWN'},
    'AHC':{1:'STRAIGHT-LEVEL',
2:'STRAIGHT-ON GRADE',
3:'STRAIGHT-HILLCREST',
4:'CURVE-LEVEL',
5:'CURVE- ON GRADE',
6:'CURVE-HILLCREST'},
    'TWAY':{1:'TWO-WAY, NOT DIVIDED',
2:'TWO-WAY, DIVIDED, UNPROTECTED MEDIAN',
3:'TWO-WAY, DIVIDED, BARRIER',
4:'ONE-WAY',
8:'OTHER'},
    'TCT':{1:'STOP AND GO LIGHT',
2:'FLASHING TRAFFIC SIGNAL',
11:'RAILROAD (CROSS BUCKS, LIGHTS AND GATES)',
12:'RAILROAD (CROSS BUCKS AND LIGHTS)',
13:'CROSS BUCKS ONLY',
21:'OFFICER OR FLAGMAN',
22:'ONCOMING EMERGENCY VEHICLE',
31:'PAVEMENT MARKINGS (ONLY)',
41:'STOP SIGN',
42:'SCHOOL SIGN',
43:'YIELD SIGN',
44:'WORK ZONE',
45:'OTHER WARNING SIGNS',
51:'FLASHING BEACON',
98:'NONE',
99:'UNKNOWN'},
    'JCT':{1:'CROSSOVER',
2:'DRIVEWAY',
3:'FIVE OR MORE POINTS',
4:'FOUR WAY INTERSECTION',
5:'RAILWAY GRADE CROSSING',
7:'SHARED USE PATH OR TRAILS',
8:'T-INTERSECTION',
9:'TRAFFIC CIRCLE',
12:'Y INTERSECTION',
13:'NON JUNCTION',
99:'UNKNOWN'},
    'CTY':{1:'Abbeville',
2:'Aiken',
3:'Allendale',
4:'Anderson',
5:'Bamberg',
6:'Barnwell',
7:'Beaufort',
8:'Berkeley',
9:'Calhoun',
10:'Charleston',
11:'Cherokee',
12:'Chester',
13:'Chesterfield',
14:'Clarendon',
15:'Colleton',
16:'Darlington',
17:'Dillon',
18:'Dorchester',
19:'Edgefield',
20:'Fairfield',
21:'Florence',
22:'Georgetown',
23:'Greenville',
24:'Greenwood',
25:'Hampton',
26:'Horry',
27:'Jasper',
28:'Kershaw',
29:'Lancaster',
30:'Laurens',
31:'Lee',
32:'Lexington',
33:'Mccormick',
34:'Marion',
35:'Marlboro',
36:'Newberry',
37:'Oconee',
38:'Orangeburg',
39:'Pickens',
40:'Richland',
41:'Saluda',
42:'Spartanburg',
43:'Sumter',
44:'Union',
45:'Williamsburg',
46:'York'},
    'FHE':{1:'CARGO/EQUIPMENT LOSS OR SHIFT',
2:'CROSS MEDIAN/CENTER LINE',
3:'DOWNHILL RUNAWAY',
4:'EQUIPMENT FAILURE',
5:'FIRE/EXPLOSION',
6:'IMMERSION',
7:'JACKKNIFE',
8:'OVERTURN/ROLLOVER',
9:'RAN OFF ROAD LEFT',
10:'RAN OFF ROAD RIGHT',
11:'SEPARATION OF UNITS (ARITCULATED VEHICLES ONLY)',
12:'SPILL (TWO WHEELED VEHICLES ONLY)',
18:'OTHER NON COLLISION',
19:'UNKNOWN NON-COLLISION',
20:'ANIMAL (DEER ONLY)',
21:'ANIMAL (ALL OTHERS)',
22:'MOTOR VEHICLE (IN TRANSIT)',
23:'MOTOR VEHICLE (STOPPED)',
24:'MOTOR VEHICLE (OTHER ROADWAY)',
25:'MOTOR VEHICLE (PARKED)',
26:'PEDALCYCLE',
27:'PEDESTRIAN',
28:'RAILWAY VEHICLE',
29:'WORK ZONE MAINTENANCE EQUIPMENT',
38:'OTHER MOVABLE OBJECT',
39:'UNKNOWN MOVABLE OBJECT',
40:'BRIDGE OVERHEAD STRUCTURE',
41:'BRIDGE PARAPET END',
42:'BRIDGE PIER OR ABUTMENT',
43:'BRIDGE RAIL',
44:'CULVERT',
45:'CURB',
46:'DITCH',
47:'EMBANKMENT',
48:'EQUIPMENT',
49:'FENCE',
50:'GUARDRAIL END',
51:'GUARDRAIL FACE',
52:'HIGHWAY TRAFFIC SIGN POST',
53:'IMPACT ATTENUATOR/CRASH CUSHION',
54:'LIGHT/LUMINAIRE SUPPORT',
55:'MAILBOX',
56:'MEDIAN BARRIER',
57:'OVERHEAD SIGN, SUPPORT',
58:'OTHER (POST, POLE, SUPPORT, ETC.)',
59:'OTHER (WALL, BUILDING, TUNNELL, ETC.)',
60:'TREE',
61:'UTILITY POLE',
62:'WORK ZONE MAINTENANCE EQUIPMENT',
68:'OTHER',
69:'UNKNOWN'},
    'HEL':{1:'GORE',
2:'ISLAND',
3:'MEDIAN',
4:'ROADSIDE',
5:'ROADWAY',
6:'SHOULDER',
7:'SIDEWALK',
8:'OUTSIDE TRAFFICWAY',
9:'UNKNOWN'},
    'PRC':{1:'DISREGARDED SIGN,SIGNALS, ETC.',
2:'DISTRACTED/INATTENTION',
3:'DRIVING TOO FAST FOR CONDITIONS',
4:'EXCEEDED AUTHORIZED SPEED LIMITS',
5:'FAILED TO YIELD RIGHT OF WAY',
6:'RAN OFF ROAD',
7:'FATIGUED/ASLEEP',
8:'FOLLOWED TOO CLOSELY',
9:'MADE AN IMPROPER TURN',
10:'MEDICAL RELATED',
12:'AGGRESSIVE OPERATION OF VEHICLE',
13:'OVER-CORRECTING/OVER STEERING',
14:'SWERVING TO AVOID OBJECT',
15:'WRONG SIDE OR WRONG WAY',
16:'UNDER THE INFLUENCE',
17:'VISION OBSCURED (WITHIN UNIT)',
18:'IMPROPER LANE USAGE/CHANGE',
19:'CELL PHONE',
20:'TEXTING',
28:'OTHER IMPROPER ACTION',
29:'UNKNOWN',
30:'DEBRIS',
31:'NON-HIGHWAY WORK',
32:'OBSTRUCTION IN ROADWAY',
33:'ROAD SURFACE CONDITION (I.E.,WET)',
34:'RUT, HOLES, BUMPS',
35:'SHOULDERS (NONE, LOW, SOFT, HIGH)',
36:'TRAFFIC CONTROL DEVICE (I.E., MISSING)',
37:'WORK ZONE (CONSTRUCTION/MAINTNEANCE/UTILITY)',
38:'WORN, TRAVEL, POLISHED SURFACE',
48:'OTHER',
49:'UNKOWN',
50:'INNATTENTIVE',
51:'LYING AND/OR ILLEGALLY IN ROADWAY',
52:'FAILURE TO YIELD RIGHT OF WAY',
53:'NOT VISIBLE (DARK CLOTHING)',
54:'DISREGARDED SIGNS, SIGNALS, ETC.',
55:'IMPROPER CROSSING',
56:'DARTING',
57:'WRONG SIDE OF ROAD',
58:'OTHER',
59:'UNKNOWN',
66:'PEDESTRIAN/BICYCLIST UNDER THE INFLUENCE',
67:'PASSENGER UNDER INFLUENCE',
60:'ANIMAL IN ROAD',
61:'GLARE',
62:'OBSTRUCTION',
63:'WEATHER CONDITION',
68:'OTHER',
69:'UNKNOWN',
70:'BRAKES',
71:'STEERING',
72:'POWER PLANT',
73:'TIRES/WHEELS',
74:'LIGHTS',
75:'SIGNALS',
76:'WINDOWS/SHIELD',
77:'RESTRAINT SYSTEM',
78:'TRUCK COUPLING',
79:'CARGO',
80:'FUEL SYSTEM',
88:'OTHER',
89:'UNKNOWN'},
    'MAC':{0:'NOT COLLISION WITH MOTOR VEHICLE IN TRANSPORT',
10:'REAR END',
20:'HEAD-ON',
30:'REAR-TO-REAR',
41:'ANGLE',
42:'ANGLE',
43:'ANGLE',
50:'SIDESWIPE, SAME DIRECTION',
60:'SIDESWIPE, OPPOSITE DIRECTION',
70:'BACKED INTO',
99:'UNKNOWN'},
    'JUR':{'HP01':'S.C. HIGHWAY PATROL DISTRICT 1',
'HP02':'S.C. HIGHWAY PATROL DISTRICT 2',
'HP03':'S.C. HIGHWAY PATROL DISTRICT 3',
'HP04':'S.C. HIGHWAY PATROL DISTRICT 4',
'HP05':'S.C. HIGHWAY PATROL DISTRICT 5',
'HP06':'S.C. HIGHWAY PATROL DISTRICT 6',
'HP07':'S.C. HIGHWAY PATROL DISTRICT 7',
'0100':'ABBEVILLE COUNTY SHERIFFS OFFICE',
'0101':'ABBEVILLE POLICE DEPARTMENT',
'0102':'CALHOUN FALLS POLICE DEPARTMENT',
'0103':'DONALDS POLICE DEPARTMENT',
'0104':'DUE WEST POLICE DEPARTMENT',
'0105':'ERSKINE COLLEGE PUBLIC SAFETY',
'0200':'AIKEN COUNTY SHERIFFS OFFICE',
'0201':'AIKEN POLICE DEPARTMENT',
'0203':'NORTH AUGUSTA DEPARTMENT OF PUBLIC SAFETY',
'0204':'BURNETTOWN POLICE DEPARTMENT',
'0205':'JACKSON POLICE DEPARTMENT',
'0206':'NEW ELLENTON POLICE DEPARTMENT',
'0207':'SALLEY POLICE DEPARTMENT',
'0208':'WAGENER POLICE DEPARTMENT',
'0209':'WAKENHUT SECURITY',
'0210':'USC AIKEN CAMPUS POLICE DEPARTMENT',
'0211':'PERRY POLICE DEPARTMENT',
'0300':'ALLENDALE COUNTY SHERIFFS OFFICE',
'0301':'ALLENDALE POLICE DEPARTMENT',
'0302':'FAIRFAX POLICE DEPARTMENT',
'0400':'ANDERSON COUNTY SHERIFFS OFFICE',
'0401':'ANDERSON POLICE DEPARTMENT',
'0402':'BELTON POLICE DEPARTMENT',
'0403':'HONEA PATH POLICE DEPARTMENT',
'0404':'PENDLETON POLICE DEPARTMENT',
'0405':'WILLIAMSTON POLICE DEPARTMENT',
'0406':'IVA POLICE DEPARTMENT',
'0407':'PELZER POLICE DEPARTMENT',
'0408':'PIEDMONT POLICE DEPARTMENT',
'0409':'STARR POLICE DEPARTMENT',
'0410':'WEST PELZER POLICE DEPARTMENT',
'0500':'BAMBERG COUNTY SHERIFFS OFFICE',
'0501':'BAMBERG POLICE DEPARTMENT',
'0502':'DENMARK POLICE DEPARTMENT',
'0503':'EHRHARDT POLICE DEPARTMENT',
'0504':'OLAR POLICE DEPARTMENT',
'0505':'DENMARK TECHNICAL COLLEGE POLICE DEARTMENT',
'0600':'BARNWELL COUNTY SHERIFFS OFFICE',
'0601':'BARNWELL POLICE DEPARTMENT',
'0603':'WILLISTON POLICE DEPARTMENT',
'0604':'BLACKVILLE POLICE DEPARTMENT',
'0700':'BEAUFORT COUNTY SHERIFFS OFFICE',
'0701':'BEAUFORT POLICE DEPARTMENT',
'0702':'BLUFFTON POLICE DEPARTMENT',
'0703':'PORT ROYAL POLICE DEPARTMENT',
'0704':'SEA PINES SECURITY',
'0705':'HILTON HEAD PLANTATION SECURITY',
'0706':'PORT ROYAL PLANTATION SECURITY',
'0707':'MELROSE PLANTATION SECURITY',
'0708':'SHIPYARD PLANTATION SECURITY',
'0709':'GREENWOOD DEVELOPMENT CORPORATION',
'0710':'LONG COVE CLUB SECURITY',
'0800':'BERKELEY COUNTY SHERIFFS OFFICE',
'0801':'MONCKS CORNER POLICE DEPARTMENT',
'0802':'BONNEAU POLICE DEPARTMENT',
'0803':'GOOSE CREEK POLICE DEPARTMENT',
'0804':'JAMESTOWN POLICE DEPARTMENT',
'0805':'ST STEPHENS POLICE DEPARTMENT',
'0806':'HANAHAN POLICE DEPERTMENT',
'0900':'CALHOUN COUNTY SHERIFFS OFFICE',
'0901':'CAMERON POLICE DEPARTMENT',
'0902':'ST MATTHEWS POLICE DEPARTMENT',
'1000':'CHARLESTON COUNTY SHERIFFS OFFICE',
'1001':'CHARLESTON POLICE DEPARTMENT',
'1003':'MT PLEASANT POLICE DEPARTMENT',
'1004':'FOLLY BEACH POLICE DEPARTMENT',
'1005':'LINCOLNVILLE POLICE DEPARTMENT',
'1006':'ISLE OF PALMS POLICE DEPARTMENT',
'1007':'SULLIVANS ISLAND POLICE DEPARTMENT',
'1008':'NORTH CHARLESTON POLICE DEPARTMENT',
'1009':'MEDICAL UNIVERSITY POLICE DEPARTMENT',
'1015':'CHARLESTON COUNTY AVIATION AUTHORITY',
'1010':'RAVENEL POLICE DEPARTMENT',
'1020':'THE CITADEL DEPARTMENT OF PUBLIC SAFETY',
'1030':'SC STATE PORTS AUTHORITY',
'1040':'SEABROOK ISLAND SECURITY DEPARTMENT',
'1050':'KIAWAH ISLAND SECURITY DEPARTMENT',
'1060':'TRIDENT TECHNICAL COLLEGE SECURITY',
'1070':'COLLEGE OF CHARLESTON PUBLIC SAFETY',
'1100':'CHEROKEE COUNTY SHERIFFS OFFICE',
'1101':'BLACKSBURG POLICE DEPARTMENT',
'1102':'GAFFNEY POLICE DEPARMTMENT',
'1103':'KING MOUNTAIN NATIONAL PARK SECURITY',
'1200':'CHESTER COUNTY SHERIFFS OFFICE',
'1201':'CHESTER POLICE DEPARTMENT',
'1202':'GREAT FALLS POLICE DEPARTMENT',
'1203':'FORT LAWN POLICE DEPARTMENT',
'1300':'CHESTERFIELD COUNTY SHERIFFS OFFICE',
'1301':'CHERAW POLICE DEPARTMENT',
'1302':'CHESTERFIELD POLICE DEPARTMENT',
'1303':'JEFFERSON POLICE DEPARTMENT',
'1304':'MCBEE POLICE DEPARTMENT',
'1305':'PAGELAND POLICE DEPARTMENT',
'1306':'PATRICK POLICE DEPARTMENT',
'1400':'CLARENDON COUNTY SHERIFFS OFFICE',
'1401':'MANNING POLICE DEPARTMENT',
'1402':'SUMMERTON POLICE DEPARTMENT',
'1403':'TURBEVILLE POLICE DEPARTMENT',
'1500':'COLLETON COUNTY SHERIFFS OFFICE',
'1501':'WALTERBORO POLICE DEPARTMENT',
'1502':'COTTAGEVILLE POLICE DEPARTMENT',
'1503':'EDISTO BEACH POLICE DEPARTMENT',
'1600':'DARLINGTON COUNTY SHERIFFS OFFICE',
'1601':'DARLINGTON POLICE DEPARTMENT',
'1602':'HARTSVILLE POLICE DEPARTMENT',
'1603':'LAMAR POLICE DEPARTMENT',
'1604':'SOCIETY HILL POLICE DEPARTMENT',
'1700':'DILLON COUNTY SHERIFFS OFFICE',
'1701':'DILLON POLICE DEPARTMENT',
'1702':'LAKEVIEW POLICE DEPARTMENT',
'1703':'LATTA POLICE DEPARTMENT',
'1800':'DORCHESTER COUNTY SHERIFFS OFFICE',
'1801':'ST GEORGE POLICE DEPARTMENT',
'1802':'SUMMERVILLE POLICE DEPARTMENT',
'1803':'HARLEYVILLE POLICE DEPARTMENT',
'1804':'RIDGEVILLE POLICE DEPARTMENT',
'1900':'EDGEFIELDCOUNTY SHERIFFSOFFICE',
'1901':'EDGEFIELD POLICE DEPARTMENT',
'1902':'JOHNSTON POLICE DEPARTMENT',
'1903':'TRENTON POLICE DEPARTMENT',
'2000':'FARIFIELD COUNTY SHERIFFS OFFICE',
'2001':'WINNSBORO POLICE DEPARTMENT',
'2002':'RIDGEWAY POLICE DEPARTMENT',
'2100':'FLORENCE COUNTY SHERIFFS OFFICE',
'2101':'FLORENCE POLICE DEPARTMENT',
'2102':'LAKE CITY POLICE DEPARTMENT',
'2103':'COWARD POLICE DEPARTMENT',
'2104':'JOHNSONVILLE POLICE DEPARTMENT',
'2105':'OLANTA POLICE DEPARTMENT',
'2106':'PAMPLICO POLICE DEPARTMENT',
'2107':'QUINBY POLICE DEPARTMENT',
'2108':'SCRANTON POLICE DEPARTMENT',
'2109':'TIMMONSVILLE POLICE DEPARTMENT',
'2110':'FRANCIS MARION COLLEGE POLICE DEPARTMENT',
'2200':'GEORGETOWN COUNTY SHERIFFS OFFICE',
'2201':'ANDREWS POLICE DEPARTMENT',
'2202':'GEORGETOWN POLICE DEPARTMENT',
'2203':'PAWLERYS ISLAND POLICE DEPARTMENT',
'2300':'GREENVILLE COUNTY SHERIFFS OFFICE',
'2301':'FOUNTAIN INN POLICE DEPARTMENT',
'2302':'GREENVILLE POLICE DEPARTMENT',
'2303':'GREER POLICE DEPARTMENT',
'2304':'MAULDIN POLICE DEPARTMENT',
'2305':'SIMPSONVILLE POLICE DEPARTMENT',
'2306':'TRAVELERS REST POLICE DEPARTMENT',
'2308':'CITY VIEW POLICE DEPARTMENT',
'2309':'FURMAN UNIVERSITY POLICE DEPARTMENT',
'2310':'BOB JONES UNIVERSITY POLICE DEPARTMENT',
'2311':'GREENVILLE TECHNICAL COLLEGE CAMPUS POLICE',
'2400':'GREENWOOD COUNTY SHERIFFS OFFICE',
'2401':'GREENWOOD POLICE DEPARTMENT',
'2402':'WARE SHOALS POLICE DEPARTMENT',
'2500':'HAMPTON COUNTY SHERIFFS OFFICE',
'2501':'BRUNSON POLICE DEPARTMENT',
'2502':'ESTILL POLICE DEPARTMENT',
'2503':'HAMPTON POLICE DEPARTMENT',
'2504':'VARNVILLE POLICE DEPARTMENT',
'2505':'GIFFORD POLICE DEPARTMENT',
'2506':'YEMASSEE POLICE DEPARTMENT',
'2600':'HORRY COUNTY SHERIFFS OFFICE',
'2601':'ATLANTIC BEACH POLICE DEPARTMENT',
'2602':'CONWAY POLICE DEPARTMENT',
'2603':'AYNOR POLICE DEPARTMENT',
'2604':'HORRY COUNTY POLICE DEPARTMENT',
'2605':'LORIS POLICE DEPARTMENT',
'2606':'MYRTLE BEACH POLICE DEPARTMENT',
'2607':'NORTH MYRTLE BEACH POLICE DEPARTMENT',
'2608':'SURFSIDE BEACH POLICE DEPARTMENT',
'2609':'USC-COASTAL CAROLINA POLICE DEPARTMENT',
'2610':'BRIARCLIFF ACRES POLICE DEPARTMENT',
'2700':'JASPERCOUNTY SHERIFFS OFFICE',
'2701':'HARDEEVILLE POLICE DEPARTMENT',
'2702':'RIDGELAND POLICE DEPARTMENT',
'2800':'KERSHAW COUNTY SHERIFFS OFFICE',
'2801':'CAMDEN POLICE DEPARTMENT',
'2802':'BETHUME POLICE DEPARTMENT',
'2803':'ELGIN POLICE DEPARTMENT',
'2900':'LANCASTER COUNTY SHERIFFS OFFICE',
'2901':'LANCASTER POLICE DEPARTMENT',
'2902':'HEATH SPRINGS POLICE DEPARTMENT',
'2903':'KERSHAW POLICE DEPARTMENT',
'3000':'LAURENS COUNTY SHERIFFS OFFICE',
'3001':'LAURENS POLICE DEPARTMENT',
'3002':'CLINTON POLICE DEPARTMENT',
'3003':'CROSS HILL POLICE DEPARTMENT',
'3004':'GRAY COURT POLICE DEPARTMENT',
'3100':'LEE COUNTY SHERIFFS OFFICE',
'3101':'BISHOPVILLE POLICE DEPARTMENT',
'3102':'LYNCHBURG POLICE DEPARTMENT',
'3200':'LEXINGTON COUNTY SHERIFFS OFFICE',
'3201':'BATESBURG POLICE DEPARTMENT',
'3202':'CAYCE POLICE DEPARTMENT',
'3204':'LEXINGTON POLICE DEPARTMENT',
'3205':'WEST COLUMBIA POLICE DEPARTMENT',
'3206':'CHAPIN POLICE DEPARTMENT',
'3207':'IRMO POLICE DEPARTMENT',
'3208':'PELION POLICE DEPARTMENT',
'3209':'PINE RIDGE POLICE DEPARTMENT',
'3210':'SOUTH CONGAREE POLICE DEPARTMENT',
'3211':'SPRINGDALE POLICE DEPARTMENT',
'3212':'SWANSEA POLICE DEPARTMENT',
'3213':'COLUMBIA METRPOLOTAN AIRPORT POLICE DEPT',
'3214':'GASTON POLICE DEPARTMENT',
'3300':'MCCORMICK COUNTY SHERIFFS OFFICE',
'3301':'MCCORMICK POLICE DEPARTMENT',
'3400':'MARION COUNTY SHERIFFS OFFICE',
'3401':'MARION POLICE DEPARTMENT',
'3402':'MULLINS POLICE DEPARTMENT',
'3403':'NICHOLS POLICE DEPARTMENT',
'3404':'SELLERS POLICE DEPARTMENT',
'3500':'MARLBORO COUNTY SHERIFFS OFFICE',
'3501':'BENNETTSVILLE POLICE DEPARTMENT',
'3502':'MCCOLL POLICE DEPARTMENT',
'3503':'CLIO POLICE DEPARTMENT',
'3600':'NEWBERRY COUNTY SHERIFFS OFFICE',
'3601':'NEWBERRY POLICE DEPARTMENT',
'3602':'WHITMIRE POLICE DEPARTMENT',
'3603':'CHAPPELS POLICE DEPARTMENT',
'3604':'LITTLE MOUNTAIN POLICE DEPARTMENT',
'3605':'PROSPERITY POLICE DEPARTMENT',
'3606':'SILVERSTREET POLICE DEPARTMENT',
'3607':'WHITTEN VILLAGE POLICE DEPARTMENT',
'3700':'OCONEE COUNTY SHERIFFS OFFICE',
'3701':'SENECA POLICE DEPARTMENT',
'3702':'WALHALLA POLICE DEPARTMENT',
'3703':'WESTMINSTER POLICE DEPARTMENT',
'3704':'WEST UNION POLICE DEPARTMENT',
'3705':'SALEM POLICE DEPARTMENT',
'3800':'ORANGEBURG COUNTY SHERIFFS OFFICE',
'3801':'ORANGEBURG POLICE DEPARTMENT',
'3802':'BRANCHVILLE POLICE DEPARTMENT',
'3803':'BOWMAN POLICE DEPARTMENT',
'3804':'CORDOVA POLICE DEPARTMENT',
'3805':'ELLOREE PPOLICE DEPARTMENT',
'3806':'EUTAWVILLE POLICE DEPARTMENT',
'3807':'HOLLY HILL POLICE DEPARTMENT',
'3808':'NORTH POLICE DEPARTMENT',
'3809':'NORWAY POLICE DEPARTMENT',
'3810':'SPRINGFIELD POLICE DEPARTMENT',
'3811':'SANTEE POLICE DEPARTMENT',
'3812':'SOUTH CAROLINA STATE COLLEGE POLICE DEPT',
'3813':'VANCE POLICE DEPARTMENT',
'3900':'PICKENS COUNTY SHERIFFS OFFICE',
'3901':'CENTRAL POLICE DEPARTMENT',
'3902':'CLEMSON POLICE DEPARTMENT',
'3903':'EASLEY POLICE DEPARTMENT',
'3904':'LIBERTY POLICE DEPARTMENT',
'3905':'PICKENS POLICE DEPARTMENT',
'3906':'CLEMSON UNIVERSITY POLICE DEPARTMENT',
'3907':'NORRIS POLICE DEPARTMENT',
'4000':'RICHLAND COUNTY SHERIFFS OFFICE',
'4001':'COLUMBIA POLICE DEPARTMENT',
'4003':'EASTOVER POLICE DEPARTMENT',
'4004':'FOREST ACRES POLICE DEPARTMENT',
'4005':'MIDLANDS CENTER POLICE DEPARTMENT',
'4006':'DEPARTMENT OF YOUTH SERVICES',
'4007':'CAPITOL COMPLEX POLICE DEPARTMENT',
'4008':'USC CAMPUS POLICE DEPARTMENT',
'4009':'DEPARTMENT OF MENTAL HEALTH',
'4010':'MIDLANDS TECHNICAL COLLEGE',
'4011':'EMPLOYMENT SECURITY COMMISSION',
'4012':'DEPARTMENT OF HEALTH/ENVIRONMENTAL CONTROL',
'4013':'COLUMBIA COLLEGE POLICE DEPARTMENT',
'4100':'SALUDA COUNTY SHERIFFS OFFICE',
'4101':'SALUDA POLICE DEPARTMENT',
'4102':'RIDGE SPRING POLICE DEPARTMENT',
'4200':'SPARTANBURG COUNTY SHERIFFS OFFICE',
'4201':'SPARTANURG POLICE DEPARTMENT',
'4202':'WOODRUFF POLICE DEPARTMENT',
'4203':'DUNCAN POLICE DEPARTMENT',
'4205':'CAMPOBELLO POLICE DEPARTMENT',
'4206':'CHESNEE POLICE DEPARTMENT',
'4207':'COWPENS POLICE DEPARTMENT',
'4208':'ENOREE POLICE DEPARTMENT',
'4209':'INMAN POLICE DEPARTMENT',
'4210':'LANDRUM POLICE DEPARTMENT',
'4211':'LYMAN POLICE DEPARTMENT',
'4212':'PACOLET POLICE DEPARTMENT',
'4213':'WELLFORD POLICE DEPARTMENT',
'4214':'USC-SPARTANBURG CAMPUS POLICE DEPARTMENT',
'4215':'PACOLET MILLS POLICE DEPARTMENT',
'4216':'GREENVILLE/SPARTANBURG AIRPORT POLICE DEPT',
'4300':'SUMTER COUNTY SHERIFFS OFFICE',
'4301':'SUMTER POLICE DEPARTMENT',
'4302':'MAYESVILLE POLICE DEPARTMENT',
'4303':'PINEWOOD POLICE DEPARTMENT',
'4400':'UNION COUNTY SHERIFFS OFFICE',
'4401':'UNION POLICE DEPARTMENT',
'4402':'CARLISLE POLICE DEPARTMENT',
'4403':'JONESVILLE POLICE DEPARTMENT',
'4500':'WILLIAMSBURG COUNTY SHERIFFS OFFICE',
'4501':'HEMINGWAY POLICE DEPARTMENT',
'4502':'KINGSTREE POLICE DEPARTMENT',
'4503':'STUCKEY POLICE DEPARTMENT',
'4504':'GREELEYVILLE POLICE DEPARTMENT',
'4600':'YORK COUNTY SHERIFFS OFFICE',
'4601':'CLOVER POLICE DEPARTMENT',
'4602':'FORT MILL POLICE DEPARTMENT',
'4603':'ROCK HILL POLICE DEPARTMENT',
'4604':'YORK POLICE DEPARTMENT',
'4605':'TEGA CAY POLICE DEPARTMENT',
'4606':'WINTHROP COLLEGE POLICE DEPARTMENT',
'4609':'RIVERHILLS PLANTATION SECURITY'},
    'WZN':{1:	'Yes',2:	'No'},
    'WZT':{1:	'Shoulder/Median Work',
			2:	'Lane Shift/Crossover',
			3:	'Intermittent/Moving Work',
			4:	'Lane Closure',
			8:	'Other',
			9:	'Unknown'},
    'WZL':{1:	'BEFORE FIRST SIGN',
			2:	'ADVANCED WARNING',
			3:	'TRANSITION AREA',
			4:	'ACTIVITY AREA',
			5:	'TERMINATION AREA'},
    'UTC':{1:"AUTOMOBILE",
            12:	"PICKUP TRUCK",
            13:	"TRUCK TRACTOR",
            14:	"OTHER TRUCK",
            15:	"FULL SIZE VAN",
            16:	"MINI-VAN",
            17:	"SPORT UTILITY",
            25:	"MOTORCYCLE",
            26:	"OTHER MOTOR BIKE",
            27:	"PEDALCYCLE",
            38:	"ANIMAL DRAWN VEHICLE",
            39:	"ANIMAL (RIDDEN)",
            41:	"PEDESTRIAN",
            51:	"TRAIN",
            61:	"SCHOOL BUS",
            62:	"PASSENGER BUS",
            98:	"OTHER",
            99:	"UNKNOWN (HIT AND RUN ONLY)"},
    'DRAC':{'A':'Asian',
'B':'African American',
'I':'American Indian',
'H':'Hispanic',
'W':'White',
'O':'Other',
'U':'Unknown'},
    'VUC':{1:'PERSONAL',
2:'DRIVING TRAINING',
3:'CONSTRUCTION/MAINTENANCE',
4:'AMBULANCE',
5:'MILITARY',
6:'TRANSPORT PASSENGERS',
7:'TRANSPORT PROPERTY',
8:'FARM USE',
9:'WRECKER OR TOW TRUCK',
10:'POLICE',
11:'GOVERNMENT',
12:'FIRE FIGHTING',
13:'LOGGING',
18:'OTHER',
41:'PEDESTRIAN'},
    'API':{1:'BACKING',
2:'CHANGING LANES',
3:'ENTERING TRAFFIC LANE',
4:'LEAVING TRAFFIC LANE',
5:'MAKING U-TURN',
6:'MOVEMENTS ESSENTIALLY STRAIGHT AHEAD',
7:'OVERTAKING/PASSING',
8:'PARKED',
9:'SLOWING OR STOPPED IN TRAFFIC',
10:'TURNING LEFT',
11:'TURNING RIGHT',
21:'APPROACHING/LEAVING VEHICLE',
22:'ENTER/CROSSING LOCATION',
23:'PLAYING/WORKING ON VEHICLE',
24:'PUSHING VEHICLE',
25:'STANDING',
26:'WALKING, PLAYING, CYCLING',
27:'WORKING',
88:'OTHER',
99:'UNKNOWN'},
    'DTG':{1:	'Given Known Results',
			2:	'Given - Unusable',
			3:	'Given-Pending',
			4:	'None',
			5:	'Refused'},
    'DTT':{1:	'Breath',
			2:	'Blood',
			3:	'Urine',
			4:	'Serum',
			8:	'Other'},
    'DTR':{1:	'Amphetamines',
			2:	'Cocaine',
			3:	'Marijuana',
			4:	'Opiates',
			7:	'PCP',
			8:	'Other'},
    'UOR':{1:	'UNDER-COMPARTMENT INTRUSION',
			2:	'UNDER-NO INTRUSION',
			3:	'UNDER-UNKNOWN',
			4:	'OVER-MOTOR VEHICLE IN TRANSPORT',
			5:	'OVER-OTHER MOTOR VEHICLE',
			6:	'NONE',
			9:	'UNKNOWN'},
    'DSEX':{'M':'Male','F':'Female','U':'Unknown'},
    'LAI':{1:	'NOT TRAPPED',
			2:	'EXTRICATED (MECHANICAL MEANS)',
			3:	'FREED (NON-MECHANICAL)',
			4:	'NOT APPLICABLE',
			9:	'UNKNOWN'},
    'EJE':{1:	'NOT EJECTED',
			2:	'PARTIALLY EJECTE',
			3:	'TOTALLY EJECTEN',
			7:	'NOT APPLICABLE',
			9:	'UNKNOWN'},
    'AIR':{1:	'DEPLOYED FRONT',
			2:	'DEPLOYED SIDE',
			3:	'DEPLOYED BOTH (Front and Side)',
			4:	'NOT DEPLOYED',
			7:	'NOT APPLICABLE',
			9:	'DEPLOYMENT UNKNOWN'},
    'SWT':{1:	'SWITCH IN ON POSITIO',
			2:	'SWITCH IN OFF POSITION',
			3:	'NO SWITCH',
			9:	'UNKNOWN'},
    'SEV':{0:'No Injury',
1:'Poss Inj',
2:'Non Incapacitating Inj',
3:'Incapacitating Inj',
4:'Fatal'},
    'REU':{0:'NONE USED',
11:'SHOULDER BELT',
12:'LAP BELT ONLY',
13:'SHOULDER AND LAP BELT',
21:'CHILD SAFETY SEAT',
88:'OTHER',
99:'UNKNOWN',
31:'HELMET',
41:'PROTECTIVE PADS',
51:'REFLECTIVE CLOTHING',
61:'LIGHTING'},
    'OSL':{
        1:	'Driver Seat',
            2:	'Front Seat - Middle',
            3:	'Front Seat - Far Right',
            4:	'2nd Row - Behind Driver',
            5:	'2nd Row - Middle',
            6:	'2nd Row - Far Right',
            7:	'3rd Row - Behind Driver',
            8:	'3rd Row - Middle',
            9:	'3rd Row - Far Right',
            20:	'Pedestrian',
            30:	'Trailing Unit',
            40:	'4th Row or Higher',
            50:	'Enclosed Passenger',
            51:	'Unenclosed Passenger',
            60:	'Sleeper Birth',
            70:	'Vehicle Exterior',
            80:	'Lap',
            99:	'Unknown'},
    'EDAM':{0:	'NONE/MINOR',
2:	'FUNCTIONAL DAMAGE',
3:	'DISABLING DAMAGE',
4:	'SEVERE/TOTALED',
5:	'NOT APPLICABLE',
9:	'UNKNOWN'},
    'MDA':{21:'Pedestrian',
           81:'None',
           92:'Rollover',
           93:'Total',
           94:'Under Carriage',
           98:'Other',
           99:'Unknown'},
    'VAT':{'1':	'NONE',
			'2':	'MOBILE HOME',
			'3':'SEMI-TRAILER',
			'4':	'UTILITY TRAILER',
			'5':	'FARM TRAILER',
			'6':	'TRAILER WITH BOAT',
			'7':	'CAMPER TRAILER',
			'8':	'TOWED MOTOR VEHICLE',
			'9':	'PETROLEUM TANKER',
			'A':	'LOW BOY TRAILER',
			'B':	'AUTOCARRIER TRAILER',
			'C':	'OTHER TANKER',
			'D':	'FLAT BED',
			'E':	'TWIN TRAILERS',
			'F':	'OTHER'},
    'VEW':{1:	'Less than 10000 pounds',
			2:	'10001-26000',
			3:	'More than 26000',
			99:	'Unknown'}}
    Assignments = [ {'Domain':F_CT_CTY,'Assign':[{'Table':LocTable,'Fields':[F_CT_CTY]}]},
                    {'Domain':F_CT_RCT,'Assign':[{'Table':LocTable,'Fields':[F_CT_RCT,F_CT_BIR,F_CT_SIC]}]},
                    {'Domain':F_CT_RAI,'Assign':[{'Table':LocTable,'Fields':[F_CT_RAI]}]},
                    {'Domain':F_CT_DLR,'Assign':[{'Table':LocTable,'Fields':[F_CT_DLR,F_CT_ODR]},{'Table':UnitTable,'Fields':[F_CT_DOT]}]},
                    {'Domain':F_CT_ART,'Assign':[{'Table':LocTable,'Fields':[F_CT_ART,F_CT_BRA,F_CT_SRA]}]},
                    {'Domain':F_CT_BDI,'Assign':[{'Table':LocTable,'Fields':[F_CT_BDI]}]},
                    {'Domain':F_CT_DAY,'Assign':[{'Table':LocTable,'Fields':[F_CT_DAY]}]},
                    {'Domain':F_CT_ALC,'Assign':[{'Table':LocTable,'Fields':[F_CT_ALC]}]},
                    {'Domain':F_CT_WCC,'Assign':[{'Table':LocTable,'Fields':[F_CT_WCC]}]},
                    {'Domain':F_CT_RSC,'Assign':[{'Table':LocTable,'Fields':[F_CT_RSC]}]},
                    {'Domain':F_CT_AHC,'Assign':[{'Table':LocTable,'Fields':[F_CT_AHC]}]},
                    {'Domain':F_CT_TWAY,'Assign':[{'Table':LocTable,'Fields':[F_CT_TWAY]}]},
                    {'Domain':F_CT_TCT,'Assign':[{'Table':LocTable,'Fields':[F_CT_TCT]}]},
                    {'Domain':F_CT_JCT,'Assign':[{'Table':LocTable,'Fields':[F_CT_JCT]}]},
                    {'Domain':F_CT_FHE,'Assign':[{'Table':LocTable,'Fields':[F_CT_FHE]},{'Table':UnitTable,'Fields':[F_CT_MHE,F_CT_SOE1,F_CT_SOE2,F_CT_SOE3,F_CT_SOE4]}]},
                    {'Domain':F_CT_HEL,'Assign':[{'Table':LocTable,'Fields':[F_CT_HEL]}]},
                    {'Domain':F_CT_PRC,'Assign':[{'Table':LocTable,'Fields':[F_CT_PRC,F_CT_OCF1,F_CT_OCF2,F_CT_OCF3,F_CT_OCF4]}]},
                    {'Domain':F_CT_MAC,'Assign':[{'Table':LocTable,'Fields':[F_CT_MAC]},{'Table':UnitTable,'Fields':[F_CT_MAN]}]},
                    {'Domain':F_CT_JUR,'Assign':[{'Table':LocTable,'Fields':[F_CT_JUR]}]},
                    {'Domain':F_CT_WZN,'Assign':[{'Table':LocTable,'Fields':[F_CT_WZN,F_CT_WPR]},{'Table':UnitTable,'Fields':[F_CT_CTA]},{'Table':OccTable,'Fields':[F_CT_MHI]}]},
                    {'Domain':F_CT_WZT,'Assign':[{'Table':LocTable,'Fields':[F_CT_WZT]}]},
                    {'Domain':F_CT_WZL,'Assign':[{'Table':LocTable,'Fields':[F_CT_WZL]}]},
                    {'Domain':F_CT_UTC,'Assign':[{'Table':UnitTable,'Fields':[F_CT_UTC]}]},
                    {'Domain':F_CT_DSEX,'Assign':[{'Table':UnitTable,'Fields':[F_CT_DSEX]},{'Table':OccTable,'Fields':[F_CT_OSEX]}]},
                    {'Domain':F_CT_DRAC,'Assign':[{'Table':UnitTable,'Fields':[F_CT_DRAC]},{'Table':OccTable,'Fields':[F_CT_ORAC]}]},
                    {'Domain':F_CT_VUC,'Assign':[{'Table':UnitTable,'Fields':[F_CT_VUC]}]},
                    {'Domain':F_CT_API,'Assign':[{'Table':UnitTable,'Fields':[F_CT_API]}]},
                    {'Domain':F_CT_DTG,'Assign':[{'Table':UnitTable,'Fields':[F_CT_DTG]}]},
                    {'Domain':F_CT_DTT,'Assign':[{'Table':UnitTable,'Fields':[F_CT_DTT]}]},
                    {'Domain':F_CT_DTR,'Assign':[{'Table':UnitTable,'Fields':[F_CT_DTR]}]},
                    {'Domain':F_CT_UOR,'Assign':[{'Table':UnitTable,'Fields':[F_CT_UOR]}]},
                    {'Domain':F_CT_VAT,'Assign':[{'Table':UnitTable,'Fields':[F_CT_VAT]}]},
                    {'Domain':F_CT_VEW,'Assign':[{'Table':UnitTable,'Fields':[F_CT_VEW]}]},
                    {'Domain':F_CT_EDAM,'Assign':[{'Table':UnitTable,'Fields':[F_CT_EDAM]}]},
                    {'Domain':F_CT_MDA,'Assign':[{'Table':UnitTable,'Fields':[F_CT_MDA,F_CT_FDA]}]},
                    {'Domain':F_CT_LAI,'Assign':[{'Table':OccTable,'Fields':[F_CT_LAI]}]},
                    {'Domain':F_CT_EJE,'Assign':[{'Table':OccTable,'Fields':[F_CT_EJE]}]},
                    {'Domain':F_CT_AIR,'Assign':[{'Table':OccTable,'Fields':[F_CT_AIR]}]},
                    {'Domain':F_CT_SWT,'Assign':[{'Table':OccTable,'Fields':[F_CT_SWT]}]},
                    {'Domain':F_CT_SEV,'Assign':[{'Table':OccTable,'Fields':[F_CT_SEV]}]},
                    {'Domain':F_CT_REU,'Assign':[{'Table':OccTable,'Fields':[F_CT_REU]}]},
                    {'Domain':F_CT_OSL,'Assign':[{'Table':OccTable,'Fields':[F_CT_OSL]}]}
                    ]
    for rec in Assignments:
        try:
            arcpy.AddMessage("     - " + rec['Domain']['name'])
            arcpy.CreateDomain_management(OutDic['folder']+'\\'+OutDic['file'], rec['Domain']['name'], rec['Domain']['alias'], rec['Domain']['type'], "CODED")
            for code in Domains[rec['Domain']['name']].keys():
                #arcpy.AddMessage(str(code)+':'+Domains[rec['Domain']['name']][code])
                arcpy.AddCodedValueToDomain_management(OutDic['folder']+'\\'+OutDic['file'], rec['Domain']['name'], code, Domains[rec['Domain']['name']][code])
            for assign in rec['Assign']:
                for field in assign['Fields']:
                    #arcpy.AddMessage(str(assign['Table'])+','+field['name']+','+rec['Domain']['name'])
                    arcpy.AssignDomainToField_management(assign['Table'], field['name'], rec['Domain']['name'])
                    if assign['Table'] == LocTable:
                        arcpy.AssignDomainToField_management(OutTable, field['name'], rec['Domain']['name'])
        except Exception, e:
            import sys
            tb = sys.exc_info()[2]
            arcpy.AddMessage(field['name'])
            arcpy.AddWarning("Line %i" % tb.tb_lineno)
            arcpy.AddWarning(e.message)
    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")
def PredictedCrash(Input, Expected, Output):
    arcpy.AddMessage(" ")
    arcpy.AddMessage("    Import Predicted Crash")

    OutDic = OutputParser(Output, 'shp')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("    Copy Features: Sites Layer")
    SitesLayer = CopyFeatures(Input,'PCSites')
    TotalSites = int(str(arcpy.GetCount_management(SitesLayer)))
    arcpy.AddMessage("     - Total number of Items Found: " + str(TotalSites))

    arcpy.AddMessage("    Add Fields: Sites Layer")
    PreCrashDic = {
        'R3ST':  [F_CMFSkew, F_CMFLTL, F_CMFRTL, F_CMFLight, F_TOT_PC, F_TOTk_PC],
        'R4ST':  [F_CMFSkew, F_CMFLTL, F_CMFRTL, F_CMFLight, F_TOT_PC, F_TOTk_PC],
        'R4SG':  [           F_CMFLTL, F_CMFRTL, F_CMFLight, F_TOT_PC, F_TOTk_PC],
        'RM3ST': [F_CMFSkew, F_CMFLTL, F_CMFRTL, F_CMFLight, F_TOT_PC, F_TOTk_PC, F_FI_PC, F_FIk_PC, F_FIKAB_PC, F_FIKABk_PC],
        'RM4ST': [F_CMFSkew, F_CMFLTL, F_CMFRTL, F_CMFLight, F_TOT_PC, F_TOTk_PC, F_FI_PC, F_FIk_PC, F_FIKAB_PC, F_FIKABk_PC],
        'RM4SG': [                                           F_TOT_PC, F_TOTk_PC, F_FI_PC, F_FIk_PC, F_FIKAB_PC, F_FIKABk_PC],
        'U3ST' : [F_CMFLTL, F_CMFRTL, F_CMFLight,                                                         F_MV_PC, F_MVk_PC, F_MVFI_PC, F_MVFIk_PC, F_MVPDO_PC, F_MVPDOk_PC, F_SV_PC, F_SVk_PC, F_SVFI_PC, F_SVFIk_PC, F_SVPDO_PC, F_SVPDOk_PC],
        'U4ST' : [F_CMFLTL, F_CMFRTL, F_CMFLight,                                                         F_MV_PC, F_MVk_PC, F_MVFI_PC, F_MVFIk_PC, F_MVPDO_PC, F_MVPDOk_PC, F_SV_PC, F_SVk_PC, F_SVFI_PC, F_SVFIk_PC, F_SVPDO_PC, F_SVPDOk_PC],
        'U3SG' : [F_CMFLTL, F_CMFRTL, F_CMFLight, F_CMFLTP, F_CMFNoRTR,                                   F_MV_PC, F_MVk_PC, F_MVFI_PC, F_MVFIk_PC, F_MVPDO_PC, F_MVPDOk_PC, F_SV_PC, F_SVk_PC, F_SVFI_PC, F_SVFIk_PC, F_SVPDO_PC, F_SVPDOk_PC],
        'U4SG' : [F_CMFLTL, F_CMFRTL, F_CMFLight, F_CMFLTP, F_CMFNoRTR, F_CMFBus, F_CMFSchool, F_CMFAlco, F_MV_PC, F_MVk_PC, F_MVFI_PC, F_MVFIk_PC, F_MVPDO_PC, F_MVPDOk_PC, F_SV_PC, F_SVk_PC, F_SVFI_PC, F_SVFIk_PC, F_SVPDO_PC, F_SVPDOk_PC, F_Ped_PC, F_Pedk_PC],
        'R2U':   [F_TOT_PC, F_CMFGrade],
        'R4U':   [F_TOT_PC],
        'R4D':   [F_TOT_PC],
        'U2U':   [F_TOT_PC, F_FI_PC, F_MV_PC, F_MVFI_PC, F_MVPDO_PC, F_MVd_PC, F_MVdk_PC, F_MVFId_PC, F_MVPDO_PC, F_MVnd_PC, F_MVndk_PC, F_MVFInd_PC, F_MVFIndk_PC, F_MVPDOnd_PC, F_MVPDOndk_PC, F_SV_PC, F_SVk_PC, F_SVFI_PC, F_SVFIk_PC, F_SVPDO_PC, F_SVPDOk_PC],
        'U3T':   [F_TOT_PC, F_FI_PC, F_MV_PC, F_MVFI_PC, F_MVPDO_PC, F_MVd_PC, F_MVdk_PC, F_MVFId_PC, F_MVPDO_PC, F_MVnd_PC, F_MVndk_PC, F_MVFInd_PC, F_MVFIndk_PC, F_MVPDOnd_PC, F_MVPDOndk_PC, F_SV_PC, F_SVk_PC, F_SVFI_PC, F_SVFIk_PC, F_SVPDO_PC, F_SVPDOk_PC],
        'U4D':   [F_TOT_PC, F_FI_PC, F_MV_PC, F_MVFI_PC, F_MVPDO_PC, F_MVd_PC, F_MVdk_PC, F_MVFId_PC, F_MVPDO_PC, F_MVnd_PC, F_MVndk_PC, F_MVFInd_PC, F_MVFIndk_PC, F_MVPDOnd_PC, F_MVPDOndk_PC, F_SV_PC, F_SVk_PC, F_SVFI_PC, F_SVFIk_PC, F_SVPDO_PC, F_SVPDOk_PC],
        'U4U':   [F_TOT_PC, F_FI_PC, F_MV_PC, F_MVFI_PC, F_MVPDO_PC, F_MVd_PC, F_MVdk_PC, F_MVFId_PC, F_MVPDO_PC, F_MVnd_PC, F_MVndk_PC, F_MVFInd_PC, F_MVFIndk_PC, F_MVPDOnd_PC, F_MVPDOndk_PC, F_SV_PC, F_SVk_PC, F_SVFI_PC, F_SVFIk_PC, F_SVPDO_PC, F_SVPDOk_PC],
        'U5T':   [F_TOT_PC, F_FI_PC, F_MV_PC, F_MVFI_PC, F_MVPDO_PC, F_MVd_PC, F_MVdk_PC, F_MVFId_PC, F_MVPDO_PC, F_MVnd_PC, F_MVndk_PC, F_MVFInd_PC, F_MVFIndk_PC, F_MVPDOnd_PC, F_MVPDOndk_PC, F_SV_PC, F_SVk_PC, F_SVFI_PC, F_SVFIk_PC, F_SVPDO_PC, F_SVPDOk_PC],
        'R4F':   [F_TOT_PC, F_FI_PC, F_MV_PC, F_MVFI_PC, F_MVPDO_PC, F_SV_PC , F_SVFI_PC, F_SVPDO_PC, F_CMFLW, F_CMFMWBMFI, F_CMFMWBMPD, F_CMFMWBSFI, F_CMFMWBSPD, F_CMFInSWFI, F_CMFInSWPD, F_CMFOutSWFI, F_CMFOutSWPD, F_CMFCZFI, F_CMFOBFI, F_CMFOBPDO, F_CMFRSSVFI, F_CMFHVMVFI, F_CMFHVMVPDO, F_CMFHVSVFI, F_CMFHVSVPDO],
        'U4F':   [F_TOT_PC, F_FI_PC, F_MV_PC, F_MVFI_PC, F_MVPDO_PC, F_SV_PC , F_SVFI_PC, F_SVPDO_PC, F_CMFLW, F_CMFMWBMFI, F_CMFMWBMPD, F_CMFMWBSFI, F_CMFMWBSPD, F_CMFInSWFI, F_CMFInSWPD, F_CMFOutSWFI, F_CMFOutSWPD, F_CMFCZFI, F_CMFOBFI, F_CMFOBPDO, F_CMFRSSVFI, F_CMFHVMVFI, F_CMFHVMVPDO, F_CMFHVSVFI, F_CMFHVSVPDO],
        'U6F':   [F_TOT_PC, F_FI_PC, F_MV_PC, F_MVFI_PC, F_MVPDO_PC, F_SV_PC , F_SVFI_PC, F_SVPDO_PC, F_CMFLW, F_CMFMWBMFI, F_CMFMWBMPD, F_CMFMWBSFI, F_CMFMWBSPD, F_CMFInSWFI, F_CMFInSWPD, F_CMFOutSWFI, F_CMFOutSWPD, F_CMFCZFI, F_CMFOBFI, F_CMFOBPDO, F_CMFRSSVFI, F_CMFHVMVFI, F_CMFHVMVPDO, F_CMFHVSVFI, F_CMFHVSVPDO]
        }
    
    Dic = {}
    for L in PreCrashDic.values():
        Dic.update({K['name']:'' for K in L})
    for Field in Dic.keys():
        arcpy.DeleteField_management(SitesLayer,Field)

    Flag          = {Type: False for Type in PreCrashDic.keys()}
    ExistingTypes = {GetVal(SRow, F_FType['name']): True for SRow in arcpy.SearchCursor(SitesLayer)}
    for Type in ExistingTypes.keys():
        if Type in Flag.keys():
            Flag[Type] = True

    for Type in Flag.keys():
        if Flag[Type]:
            for Field in PreCrashDic[Type]:
                AddField (SitesLayer,Field,'append')
                if Field in [F_CMFGrade]:
                    CalField(SitesLayer,Field,1)

    arcpy.AddMessage("    Update Cursor: Sites Layer")
    UC = arcpy.UpdateCursor(SitesLayer)
    for URow in UC:

        Type        = GetVal(URow,F_FType['name'])

        if Type in Flag.keys():

            SPF = SPF_Module(URow)

            if Type == 'R3ST':

                CMF_Lighting = CMFLighting(URow)
                CMF_Skew     = CMFSkew(URow)
                CMF_LTL      = CMFLTL(URow)
                CMF_RTL      = CMFRTL(URow)

                TOT_PC = SPF['TOT'] * CMF_Skew['TOT'] * CMF_LTL['TOT'] * CMF_RTL['TOT'] * CMF_Lighting


                URow.setValue(F_CMFLight['name'], CMF_Lighting)
                URow.setValue(F_CMFSkew ['name'], CMF_Skew['TOT'])
                URow.setValue(F_CMFLTL  ['name'], CMF_LTL['TOT'])
                URow.setValue(F_CMFRTL  ['name'], CMF_RTL['TOT'])
                URow.setValue(F_TOT_PC  ['name'], TOT_PC * GetVal(URow,'CCMF',1))
                URow.setValue(F_TOTk_PC ['name'], SPF['TCk'])

            if Type == 'R4ST':

                CMF_Lighting = CMFLighting(URow)
                CMF_Skew     = CMFSkew(URow)
                CMF_LTL      = CMFLTL(URow)
                CMF_RTL      = CMFRTL(URow)

                TOT_PC = SPF['TOT'] * CMF_Skew['TOT'] * CMF_LTL['TOT'] * CMF_RTL['TOT'] * CMF_Lighting

                URow.setValue(F_CMFLight['name'], CMF_Lighting)
                URow.setValue(F_CMFSkew ['name'], CMF_Skew['TOT'])
                URow.setValue(F_CMFLTL  ['name'], CMF_LTL['TOT'])
                URow.setValue(F_CMFRTL  ['name'], CMF_RTL['TOT'])
                URow.setValue(F_TOT_PC  ['name'], TOT_PC * GetVal(URow,'CCMF',1))
                URow.setValue(F_TOTk_PC ['name'], SPF['TCk'])

            if Type == 'R4SG':

                CMF_Lighting = CMFLighting(URow)
                CMF_LTL      = CMFLTL(URow)
                CMF_RTL      = CMFRTL(URow)

                TOT_PC    = SPF['TOT'] * CMF_LTL['TOT'] * CMF_RTL['TOT'] * CMF_Lighting

                URow.setValue(F_CMFLight['name'], CMF_Lighting)
                URow.setValue(F_CMFLTL  ['name'], CMF_LTL['TOT'])
                URow.setValue(F_CMFRTL  ['name'], CMF_RTL['TOT'])
                URow.setValue(F_TOT_PC  ['name'], TOT_PC * GetVal(URow,'CCMF',1))
                URow.setValue(F_TOTk_PC ['name'], SPF['TCk'])

            if Type == 'RM3ST':

                CMF_Lighting = CMFLighting(URow)
                CMF_Skew     = CMFSkew(URow)
                CMF_LTL      = CMFLTL(URow)
                CMF_RTL      = CMFRTL(URow)

                TOT_PC   = SPF['TOT'  ] * CMF_Skew['TOT'] * CMF_LTL['TOT'] * CMF_RTL['TOT'] * CMF_Lighting
                FI_PC    = SPF['FI'   ] * CMF_Skew['FI' ] * CMF_LTL['FI' ] * CMF_RTL['FI' ] * CMF_Lighting
                FIKAB_PC = SPF['FIKAB'] * CMF_Skew['FI' ] * CMF_LTL['FI' ] * CMF_RTL['FI' ] * CMF_Lighting

                URow.setValue(F_CMFLight['name'], CMF_Lighting)
                URow.setValue(F_CMFSkew ['name'], CMF_Skew['TOT'])
                URow.setValue(F_CMFLTL  ['name'], CMF_LTL['TOT'])
                URow.setValue(F_CMFRTL  ['name'], CMF_RTL['TOT'])
                URow.setValue(F_TOT_PC   ['name'], TOT_PC  )
                URow.setValue(F_TOTk_PC  ['name'], SPF['TCk'])
                URow.setValue(F_FI_PC    ['name'], FI_PC   )
                URow.setValue(F_FIk_PC   ['name'], SPF['FIk'])
                URow.setValue(F_FIKAB_PC ['name'], FIKAB_PC)
                URow.setValue(F_FIKABk_PC['name'], SPF['FIKABk'])

            if Type == 'RM4ST':

                CMF_Lighting = CMFLighting(URow)
                CMF_Skew     = CMFSkew(URow)
                CMF_LTL      = CMFLTL(URow)
                CMF_RTL      = CMFRTL(URow)

                TOT_PC   = SPF['TOT'  ] * CMF_Skew['TOT'] * CMF_LTL['TOT'] * CMF_RTL['TOT'] * CMF_Lighting
                FI_PC    = SPF['FI'   ] * CMF_Skew['FI' ] * CMF_LTL['FI' ] * CMF_RTL['FI' ] * CMF_Lighting
                FIKAB_PC = SPF['FIKAB'] * CMF_Skew['FI' ] * CMF_LTL['FI' ] * CMF_RTL['FI' ] * CMF_Lighting

                URow.setValue(F_CMFLight['name'], CMF_Lighting)
                URow.setValue(F_CMFSkew ['name'], CMF_Skew['TOT'])
                URow.setValue(F_CMFLTL  ['name'], CMF_LTL['TOT'])
                URow.setValue(F_CMFRTL  ['name'], CMF_RTL['TOT'])
                URow.setValue(F_TOT_PC   ['name'], TOT_PC  )
                URow.setValue(F_TOTk_PC  ['name'], SPF['TCk'])
                URow.setValue(F_FI_PC    ['name'], FI_PC   )
                URow.setValue(F_FIk_PC   ['name'], SPF['FIk'])
                URow.setValue(F_FIKAB_PC ['name'], FIKAB_PC)
                URow.setValue(F_FIKABk_PC['name'], SPF['FIKABk'])

            if Type == 'RM4SG':

                TOT_PC   = SPF['TOT'  ]
                FI_PC    = SPF['FI'   ]
                FIKAB_PC = SPF['FIKAB']

                URow.setValue(F_TOT_PC   ['name'], TOT_PC  )
                URow.setValue(F_TOTk_PC  ['name'], SPF['TCk'])
                URow.setValue(F_FI_PC    ['name'], FI_PC   )
                URow.setValue(F_FIk_PC   ['name'], SPF['FIk'])
                URow.setValue(F_FIKAB_PC ['name'], FIKAB_PC)
                URow.setValue(F_FIKABk_PC['name'], SPF['FIKABk'])

            if Type == 'U3ST':

                CMF_Lighting = CMFLighting(URow)
                CMF_LTL = CMFLTL(URow)
                CMF_RTL = CMFRTL(URow)

                MV_PC    = SPF['MVC'   ] * CMF_LTL['TOT'] * CMF_RTL['TOT'] * CMF_Lighting
                MVFI_PC  = SPF['MVFIC' ] * CMF_LTL['TOT'] * CMF_RTL['TOT'] * CMF_Lighting
                MVPDO_PC = SPF['MVPDOC'] * CMF_LTL['TOT'] * CMF_RTL['TOT'] * CMF_Lighting
                SV_PC    = SPF['SVC'   ] * CMF_LTL['TOT'] * CMF_RTL['TOT'] * CMF_Lighting
                SVFI_PC  = SPF['SVFIC' ] * CMF_LTL['TOT'] * CMF_RTL['TOT'] * CMF_Lighting
                SVPDO_PC = SPF['SVPDOC'] * CMF_LTL['TOT'] * CMF_RTL['TOT'] * CMF_Lighting
                TOT_PC   = MV_PC   + SV_PC
                FI_PC    = MVFI_PC + SVFI_PC

                URow.setValue(F_CMFLight['name'], CMF_Lighting)
                URow.setValue(F_CMFLTL  ['name'], CMF_LTL['TOT'])
                URow.setValue(F_CMFRTL  ['name'], CMF_RTL['TOT'])
                URow.setValue(F_TOT_PC    ['name'], TOT_PC * GetVal(URow,'CCMF',1))
                URow.setValue(F_FI_PC     ['name'], FI_PC)
                URow.setValue(F_MV_PC     ['name'], MV_PC)
                URow.setValue(F_MVk_PC    ['name'], SPF['MVCk'])
                URow.setValue(F_MVFI_PC   ['name'], MVFI_PC)
                URow.setValue(F_MVFIk_PC  ['name'], SPF['MVFICk'])
                URow.setValue(F_MVPDO_PC  ['name'], MVPDO_PC)
                URow.setValue(F_MVPDOk_PC ['name'], SPF['MVPDOCk'])
                URow.setValue(F_SV_PC     ['name'], SV_PC)
                URow.setValue(F_SVk_PC    ['name'], SPF['SVCk'])
                URow.setValue(F_SVFI_PC   ['name'], SVFI_PC)
                URow.setValue(F_SVFIk_PC  ['name'], SPF['SVFICk'])
                URow.setValue(F_SVPDO_PC  ['name'], SVPDO_PC)
                URow.setValue(F_SVPDOk_PC ['name'], SPF['SVPDOCk'])

            if Type == 'U4ST':

                CMF_Lighting = CMFLighting(URow)
                CMF_LTL = CMFLTL(URow)
                CMF_RTL = CMFRTL(URow)

                MV_PC    = SPF['MVC'   ] * CMF_LTL['TOT'] * CMF_RTL['TOT'] * CMF_Lighting
                MVFI_PC  = SPF['MVFIC' ] * CMF_LTL['TOT'] * CMF_RTL['TOT'] * CMF_Lighting
                MVPDO_PC = SPF['MVPDOC'] * CMF_LTL['TOT'] * CMF_RTL['TOT'] * CMF_Lighting
                SV_PC    = SPF['SVC'   ] * CMF_LTL['TOT'] * CMF_RTL['TOT'] * CMF_Lighting
                SVFI_PC  = SPF['SVFIC' ] * CMF_LTL['TOT'] * CMF_RTL['TOT'] * CMF_Lighting
                SVPDO_PC = SPF['SVPDOC'] * CMF_LTL['TOT'] * CMF_RTL['TOT'] * CMF_Lighting
                TOT_PC   = MV_PC   + SV_PC
                FI_PC    = MVFI_PC + SVFI_PC

                URow.setValue(F_CMFLight['name'], CMF_Lighting)
                URow.setValue(F_CMFLTL  ['name'], CMF_LTL['TOT'])
                URow.setValue(F_CMFRTL  ['name'], CMF_RTL['TOT'])
                URow.setValue(F_TOT_PC    ['name'], TOT_PC * GetVal(URow,'CCMF',1))
                URow.setValue(F_FI_PC     ['name'], FI_PC)
                URow.setValue(F_MV_PC     ['name'], MV_PC)
                URow.setValue(F_MVk_PC    ['name'], SPF['MVCk'])
                URow.setValue(F_MVFI_PC   ['name'], MVFI_PC)
                URow.setValue(F_MVFIk_PC  ['name'], SPF['MVFICk'])
                URow.setValue(F_MVPDO_PC  ['name'], MVPDO_PC)
                URow.setValue(F_MVPDOk_PC ['name'], SPF['MVPDOCk'])
                URow.setValue(F_SV_PC     ['name'], SV_PC)
                URow.setValue(F_SVk_PC    ['name'], SPF['SVCk'])
                URow.setValue(F_SVFI_PC   ['name'], SVFI_PC)
                URow.setValue(F_SVFIk_PC  ['name'], SPF['SVFICk'])
                URow.setValue(F_SVPDO_PC  ['name'], SVPDO_PC)
                URow.setValue(F_SVPDOk_PC ['name'], SPF['SVPDOCk'])

            if Type == 'U3SG':

                CMF_Lighting = CMFLighting(URow)
                CMF_LTL = CMFLTL(URow)
                CMF_RTL = CMFRTL(URow)
                CMF_LTP = CMFLTP(URow)
                CMF_No_RTR = CMFNoRTR(URow)
    
                MV_PC    = SPF['MVC'   ] * CMF_LTL['TOT'] * CMF_RTL['TOT'] * CMF_Lighting * CMF_LTP * CMF_No_RTR
                MVFI_PC  = SPF['MVFIC' ] * CMF_LTL['TOT'] * CMF_RTL['TOT'] * CMF_Lighting * CMF_LTP * CMF_No_RTR
                MVPDO_PC = SPF['MVPDOC'] * CMF_LTL['TOT'] * CMF_RTL['TOT'] * CMF_Lighting * CMF_LTP * CMF_No_RTR
                SV_PC    = SPF['SVC'   ] * CMF_LTL['TOT'] * CMF_RTL['TOT'] * CMF_Lighting * CMF_LTP * CMF_No_RTR
                SVFI_PC  = SPF['SVFIC' ] * CMF_LTL['TOT'] * CMF_RTL['TOT'] * CMF_Lighting * CMF_LTP * CMF_No_RTR
                SVPDO_PC = SPF['SVPDOC'] * CMF_LTL['TOT'] * CMF_RTL['TOT'] * CMF_Lighting * CMF_LTP * CMF_No_RTR
                TOT_PC   = MV_PC   + SV_PC
                FI_PC    = MVFI_PC + SVFI_PC

                URow.setValue(F_CMFLight['name'], CMF_Lighting)
                URow.setValue(F_CMFLTL  ['name'], CMF_LTL['TOT'])
                URow.setValue(F_CMFRTL  ['name'], CMF_RTL['TOT'])
                URow.setValue(F_CMFLTP  ['name'], CMF_LTP)
                URow.setValue(F_CMFNoRTR['name'], CMF_No_RTR)
                URow.setValue(F_TOT_PC    ['name'], TOT_PC * GetVal(URow,'CCMF',1))
                URow.setValue(F_FI_PC     ['name'], FI_PC)
                URow.setValue(F_MV_PC     ['name'], MV_PC)
                URow.setValue(F_MVk_PC    ['name'], SPF['MVCk'])
                URow.setValue(F_MVFI_PC   ['name'], MVFI_PC)
                URow.setValue(F_MVFIk_PC  ['name'], SPF['MVFICk'])
                URow.setValue(F_MVPDO_PC  ['name'], MVPDO_PC)
                URow.setValue(F_MVPDOk_PC ['name'], SPF['MVPDOCk'])
                URow.setValue(F_SV_PC     ['name'], SV_PC)
                URow.setValue(F_SVk_PC    ['name'], SPF['SVCk'])
                URow.setValue(F_SVFI_PC   ['name'], SVFI_PC)
                URow.setValue(F_SVFIk_PC  ['name'], SPF['SVFICk'])
                URow.setValue(F_SVPDO_PC  ['name'], SVPDO_PC)
                URow.setValue(F_SVPDOk_PC ['name'], SPF['SVPDOCk'])

            if Type == 'U4SG':

                CMF_Lighting = CMFLighting(URow)
                CMF_LTL = CMFLTL(URow)
                CMF_RTL = CMFRTL(URow)
                CMF_LTP = CMFLTP(URow)
                CMF_No_RTR = CMFNoRTR(URow)
                CMF_Bus = CMFBus(URow)
                CMF_School = CMFSchool(URow)
                CMF_Alco = CMFAlco(URow)

                MV_PC    = SPF['MVC'   ] * CMF_LTL['TOT'] * CMF_RTL['TOT'] * CMF_Lighting * CMF_LTP * CMF_No_RTR
                MVFI_PC  = SPF['MVFIC' ] * CMF_LTL['TOT'] * CMF_RTL['TOT'] * CMF_Lighting * CMF_LTP * CMF_No_RTR
                MVPDO_PC = SPF['MVPDOC'] * CMF_LTL['TOT'] * CMF_RTL['TOT'] * CMF_Lighting * CMF_LTP * CMF_No_RTR
                SV_PC    = SPF['SVC'   ] * CMF_LTL['TOT'] * CMF_RTL['TOT'] * CMF_Lighting * CMF_LTP * CMF_No_RTR
                SVFI_PC  = SPF['SVFIC' ] * CMF_LTL['TOT'] * CMF_RTL['TOT'] * CMF_Lighting * CMF_LTP * CMF_No_RTR
                SVPDO_PC = SPF['SVPDOC'] * CMF_LTL['TOT'] * CMF_RTL['TOT'] * CMF_Lighting * CMF_LTP * CMF_No_RTR
                Ped_PC   = SPF['Ped'   ] * CMF_Bus * CMF_School * CMF_Alco
                TOT_PC   = MV_PC   + SV_PC   + Ped_PC
                FI_PC    = MVFI_PC + SVFI_PC

                URow.setValue(F_CMFLight['name'], CMF_Lighting)
                URow.setValue(F_CMFLTL  ['name'], CMF_LTL['TOT'])
                URow.setValue(F_CMFRTL  ['name'], CMF_RTL['TOT'])
                URow.setValue(F_CMFLTP  ['name'], CMF_LTP)
                URow.setValue(F_CMFNoRTR['name'], CMF_No_RTR)
                URow.setValue(F_CMFBus  ['name'], CMF_Bus)
                URow.setValue(F_CMFSchool['name'], CMF_School)
                URow.setValue(F_CMFAlco  ['name'], CMF_Alco)
                URow.setValue(F_TOT_PC    ['name'], TOT_PC * GetVal(URow,'CCMF',1))
                URow.setValue(F_FI_PC     ['name'], FI_PC)
                URow.setValue(F_MV_PC     ['name'], MV_PC)
                URow.setValue(F_MVk_PC    ['name'], SPF['MVCk'])
                URow.setValue(F_MVFI_PC   ['name'], MVFI_PC)
                URow.setValue(F_MVFIk_PC  ['name'], SPF['MVFICk'])
                URow.setValue(F_MVPDO_PC  ['name'], MVPDO_PC)
                URow.setValue(F_MVPDOk_PC ['name'], SPF['MVPDOCk'])
                URow.setValue(F_SV_PC     ['name'], SV_PC)
                URow.setValue(F_SVk_PC    ['name'], SPF['SVCk'])
                URow.setValue(F_SVFI_PC   ['name'], SVFI_PC)
                URow.setValue(F_SVFIk_PC  ['name'], SPF['SVFICk'])
                URow.setValue(F_SVPDO_PC  ['name'], SVPDO_PC)
                URow.setValue(F_SVPDOk_PC ['name'], SPF['SVPDOCk'])
                URow.setValue(F_Ped_PC    ['name'], Ped_PC)
                URow.setValue(F_Pedk_PC   ['name'], SPF['Pedk'])
        
            if Type in ['R2U']:

                CMF_Grade = CMFGrade('R2U',GetVal(URow,F_Grade['name'],0))

                CMF_LW    = GetVal(URow,F_CMFLW['name'],1)
                CMF_SW    = GetVal(URow,F_CMFSW['name'],1)
                CMF_HurC  = GetVal(URow,F_CMFHorCur['name'],1)
                CMF_DD    = GetVal(URow,F_CMFDrwDens['name'],1)
                CMF_RHR   = GetVal(URow,F_CMFRHR['name'],1)
                CMF_Light = GetVal(URow,F_CMFLight['name'],1)
                
                URow.setValue(F_TOT_PC     ['name'], SPF['TOT']      * CMF_LW * CMF_SW * CMF_HurC * CMF_Grade * CMF_DD * CMF_RHR * CMF_Light)

                URow.setValue(F_CMFGrade['name'], CMF_Grade)

            if Type in ['R4D']:

                CMF_LW    = GetVal(URow,F_CMFLW['name'],1)
                CMF_SW    = GetVal(URow,F_CMFSW['name'],1)
                CMF_MW    = GetVal(URow,F_CMFMW['name'],1)
                CMF_Light = GetVal(URow,F_CMFLight['name'],1)
                
                URow.setValue(F_TOT_PC     ['name'], SPF['TOT']      * CMF_LW * CMF_SW * CMF_MW * CMF_Light)
                URow.setValue(F_FI_PC      ['name'], SPF['FI' ]      * CMF_LW * CMF_SW * CMF_MW * CMF_Light)

            if Type in ['R4U']:

                CMF_LW    = GetVal(URow,F_CMFLW['name'],1)
                CMF_SW    = GetVal(URow,F_CMFSW['name'],1)
                CMF_Light = GetVal(URow,F_CMFLight['name'],1)
                
                URow.setValue(F_TOT_PC     ['name'], SPF['TOT']      * CMF_LW * CMF_SW * CMF_Light)
                URow.setValue(F_FI_PC      ['name'], SPF['FI' ]      * CMF_LW * CMF_SW * CMF_Light)

            if Type in ['U2U', 'U3T', 'U4D', 'U4U', 'U5T']:

                CMF_OSP   = GetVal(URow,F_CMFOSP['name'],1)
                CMF_MW    = GetVal(URow,F_CMFMW['name'],1)
                CMF_Light = GetVal(URow,F_CMFLight['name'],1)
                CMF_FO    = GetVal(URow,F_CMFFO['name'],1)

                URow.setValue(F_TOT_PC     ['name'], SPF['TOT']      * CMF_OSP * CMF_FO * CMF_MW * CMF_Light * GetVal(URow,'CCMF',1))
                URow.setValue(F_FI_PC      ['name'], SPF['FI']       * CMF_OSP * CMF_FO * CMF_MW * CMF_Light)
                URow.setValue(F_MV_PC      ['name'], SPF['MVC']      * CMF_OSP * CMF_FO * CMF_MW * CMF_Light)
                URow.setValue(F_MVFI_PC    ['name'], SPF['MVFIC']    * CMF_OSP * CMF_FO * CMF_MW * CMF_Light)
                URow.setValue(F_MVPDO_PC   ['name'], SPF['MVPDOC']   * CMF_OSP * CMF_FO * CMF_MW * CMF_Light)

                URow.setValue(F_MVd_PC     ['name'], SPF['MVdC']     * CMF_OSP * CMF_FO * CMF_MW * CMF_Light)
                URow.setValue(F_MVFId_PC   ['name'], SPF['MVFIdC']   * CMF_OSP * CMF_FO * CMF_MW * CMF_Light)
                URow.setValue(F_MVPDOd_PC  ['name'], SPF['MVPDOdC']  * CMF_OSP * CMF_FO * CMF_MW * CMF_Light)
                URow.setValue(F_MVdk_PC    ['name'], SPF['MVdCk'])

                URow.setValue(F_MVnd_PC    ['name'], SPF['MVndC']    * CMF_OSP * CMF_FO * CMF_MW * CMF_Light)
                URow.setValue(F_MVFInd_PC  ['name'], SPF['MVFIndC']  * CMF_OSP * CMF_FO * CMF_MW * CMF_Light)
                URow.setValue(F_MVPDOnd_PC ['name'], SPF['MVPDOndC'] * CMF_OSP * CMF_FO * CMF_MW * CMF_Light)
                URow.setValue(F_MVndk_PC   ['name'], SPF['MVndCk'])
                URow.setValue(F_MVFIndk_PC ['name'], SPF['MVFIndCk'])
                URow.setValue(F_MVPDOndk_PC['name'], SPF['MVPDOndCk'])

                URow.setValue(F_SV_PC      ['name'], SPF['SVC']      * CMF_OSP * CMF_FO * CMF_MW * CMF_Light)
                URow.setValue(F_SVFI_PC    ['name'], SPF['SVFIC']    * CMF_OSP * CMF_FO * CMF_MW * CMF_Light)
                URow.setValue(F_SVPDO_PC   ['name'], SPF['SVPDOC']   * CMF_OSP * CMF_FO * CMF_MW * CMF_Light)
                URow.setValue(F_SVk_PC     ['name'], SPF['SVCk'])
                URow.setValue(F_SVFIk_PC   ['name'], SPF['SVFICk'])
                URow.setValue(F_SVPDOk_PC  ['name'], SPF['SVPDOCk'])

            if Type in ['R4F', 'U4F', 'U6F']:
                CMFHC = {'MVFI' :GetVal(URow,F_CMFHCMVFI ['name'],1),
                         'MVPDO':GetVal(URow,F_CMFHCMVPD ['name'],1),
                         'SVFI' :GetVal(URow,F_CMFHCSVFI ['name'],1),
                         'SVPDO':GetVal(URow,F_CMFHCSVPD ['name'],1)}

                LaneWidth = GetVal(URow,F_Lane_Width['name'],12)
                InShWidth  = (GetVal(URow,F_Sh_Wid_RI['name'],6 )+GetVal(URow,F_Sh_Wid_LI['name'],6 ))/2
                OutShWidth = (GetVal(URow,F_Sh_Wid_RO['name'],10)+GetVal(URow,F_Sh_Wid_LO['name'],10))/2

                CMFLW = CMFLaneWidth(Type,LaneWidth,0)
                URow.setValue(F_CMFLW['name'],CMFLW) 

                CMFMWB = CMFMedianBarrier(Type,GetVal(URow,'MEDIAN_WID',60),GetVal(URow,'MEDIAN_ID',1),InShWidth)
                URow.setValue(F_CMFMWBMFI['name'],CMFMWB['MVFI' ]) 
                URow.setValue(F_CMFMWBMPD['name'],CMFMWB['MVPDO']) 
                URow.setValue(F_CMFMWBSFI['name'],CMFMWB['SVFI' ]) 
                URow.setValue(F_CMFMWBSPD['name'],CMFMWB['SVPDO']) 

                CMFInSW  = CMFInsideShoulderW (Type,InShWidth )
                CMFOutSW = CMFOutsideShoulderW(Type,OutShWidth)
                URow.setValue(F_CMFInSWFI['name'],CMFInSW['FI' ]) 
                URow.setValue(F_CMFInSWPD['name'],CMFInSW['PDO']) 
                URow.setValue(F_CMFOutSWFI['name'],CMFOutSW['FI' ]) 
                URow.setValue(F_CMFOutSWPD['name'],CMFOutSW['PDO']) 

                #Clearzone
                CMFCZ = GetVal(URow,F_CMFCZFI ['name'],1)
                CMFOB = {'SVFI' :GetVal(URow,F_CMFOBFI ['name'],1),
                         'SVPDO':GetVal(URow,F_CMFOBPDO['name'],1)}
                CMFRS = 0.923
                URow.setValue(F_CMFRSSVFI['name'],CMFRS) 


                Phv = GetVal(URow,F_PHighVol['name'],0)
                CMF_HV = CMFHighVolume(Type,Phv)
                URow.setValue(F_CMFHVSVFI ['name'],CMF_HV['SVFI' ]) 
                URow.setValue(F_CMFHVSVPDO['name'],CMF_HV['SVPDO']) 
                URow.setValue(F_CMFHVMVFI ['name'],CMF_HV['MVFI' ]) 
                URow.setValue(F_CMFHVMVPDO['name'],CMF_HV['MVPDO']) 


                SPF_MVFI  = SPF['MVFIC' ]*CMFHC['MVFI' ]*CMFLW*CMFInSW['FI' ]                *CMFMWB['MVFI' ] * CMF_HV['MVFI' ]
                SPF_MVPDO = SPF['MVPDOC']*CMFHC['MVPDO']      *CMFInSW['PDO']                *CMFMWB['MVPDO'] * CMF_HV['MVPDO']
                SPF_SVFI  = SPF['SVFIC' ]*CMFHC['SVFI' ]*CMFLW*CMFInSW['FI' ]*CMFOutSW['FI' ]*CMFMWB['SVFI' ]*CMFOB['SVFI' ]*CMFCZ*CMFRS * CMF_HV['SVFI' ]
                SPF_SVPDO = SPF['SVPDOC']*CMFHC['SVPDO']      *CMFInSW['PDO']*CMFOutSW['PDO']*CMFMWB['SVPDO']*CMFOB['SVPDO']             * CMF_HV['SVPDO']
                URow.setValue(F_MVFI_PC    ['name'], SPF_MVFI)
                URow.setValue(F_MVPDO_PC   ['name'], SPF_MVPDO)

                URow.setValue(F_SVFI_PC    ['name'], SPF_SVFI)
                URow.setValue(F_SVPDO_PC   ['name'], SPF_SVPDO)

                URow.setValue(F_MV_PC      ['name'], SPF_MVFI+SPF_MVPDO)
                URow.setValue(F_SV_PC      ['name'], SPF_SVFI+SPF_SVPDO)
                URow.setValue(F_TOT_PC     ['name'], SPF_MVFI+SPF_MVPDO+SPF_SVFI+SPF_SVPDO)
                URow.setValue(F_FI_PC      ['name'], SPF_SVFI+SPF_MVFI)

        UC.updateRow(URow)

    Output = arcpy.CopyFeatures_management(SitesLayer,Output)

    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")
def CrashCode(CrashInput, UnitInput,Output):
    arcpy.AddMessage(" ")
    arcpy.AddMessage("    Crash Code")

    OutDic = OutputParser(Output, 'shp')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("   Sort: Crash Layer")
    CrashLayer = Sort(CrashInput,'CCSortedCrash','ANO')
    C = arcpy.GetCount_management(CrashLayer)
    arcpy.AddMessage("     - Total Items Found: " + str(C))

    #arcpy.AddMessage(" Sort Unit File")
    #UnitFile = Sort(UnitInput,'SOE_Sort_Unit','ANO')
    #a = MakeFeatureLayer(UnitInput,'aa')
    #UnitFile = CopyFeatures(UnitInput,'SOE_Unit_Copy')
    arcpy.AddMessage("   Assuming Unit File is already sorted by ANO")
    UnitFile = UnitInput
    U = arcpy.GetCount_management(UnitFile)
    arcpy.AddMessage("     - Total Items Found: " + str(U))

    arcpy.AddMessage("   Add Fields: Crash Layer")
    CrashTypeDic = [F_CT_SOE1, F_CT_SOE2, F_CT_SOE3, F_CT_SOE4, F_CT_MHE, F_CT_UNF, F_CT_NV, F_CT_Code, F_CT_FO]
    for Field in CrashTypeDic:
        AddField(CrashLayer,Field,'append')

    arcpy.AddMessage("   Update Cursor: Crash Layer")

    def CCode(NV,Events,MACList):
        C1 = '0'
        C2 = '0'
        C3 = '0'
        MAC = -1
        for mac in MACList:
            if mac <> -1:
                MAC = mac
        if NV == 1:
            C1 = '1'
    #    if NV >= 2 and MAC <> -1:   #Less Multi
        if NV >= 2: #More Multi
            C1 = '2'
        MHE = MHEList(Events)
        if C1 == '1':
            C2 = '4'
            if AnyofList1inList2(MHE,range(0,20)):
                C2 = '1'
            if AnyofList1inList2(MHE,range(40,69)):
                C2 = '2'
            if AnyofList1inList2(MHE,range(20,40)):
                C2 = '3'
            ExpEvents = ExplodeSubLists(Events)
            Animal = False
            Bicycle = False
            Pedestrian = False
            Overturn = False
            RanOffRoad = False
            Parked = False
            if 27 in ExpEvents:
                Pedestrian = True
            if 20 in ExpEvents or 21 in ExpEvents:
                Animal = True
            if 26 in ExpEvents:
                Bicycle = True
            if 8 in ExpEvents:
                Overturn = True
            if 9 in ExpEvents or 10 in ExpEvents:
                RanOffRoad = True
            if 25 in ExpEvents:
                Parked = True
            if C2 == '1':
                if RanOffRoad:
                    C3 = '1'
                if Overturn:
                    C3 = '2'
            if C2 == '2':
                if RanOffRoad:
                    C3 = '1'
                if Overturn:
                    C3 = '2'
            if C2 == '3':
                if RanOffRoad:
                    C3 = '5'
                if Overturn:
                    C3 = '6'
                if Animal:
                    C3 = '1'
                if Parked:
                    C3 = '3'
                if Bicycle:
                    C3 = '2'
                if Pedestrian:
                    C3 = '4'
        elif C1 == '2':
            C2 = '5'
            if MAC in [41,42,43]:
                C2 = '1'
            if MAC in [20]:
                C2 = '2'
            if MAC in [10]:
                C2 = '3'
            if MAC in [50]:
                C2 = '4'
                C3 = '1'
            if MAC in [60]:
                C2 = '4'
                C3 = '2'
        return int(C1 + C2 + C3)
    def NumberOfVehicles(inList, Events=[]):
        if type(inList) <> list:
            arcpy.AddWarning('Input is not list: ' + str(inList))
            inList = [inList]
        NV = 0
        for UTC in inList:
            try:
                utc = int(UTC)
            except:
                #arcpy.AddWarning('Input is not integer, ' + str(UTC))
                utc = 0
            if utc in [1,12,13,14,15,16,17,25,26,38,39,51,61,62,98,99]:
                NV += 1
        Events = ExplodeSubLists(Events)
        if 25 in Events: #Parked Vehicles
            NV -= 1
            if NV < 1:
                NV = 1
        return NV
    def AnyofList1inList2(List1,List2):
        for item1 in List1:
            if item1 in List2:
                return True
        return False
    def ExplodeSubLists(inList):
        outList = []
        if type(inList) == list:
            for item in inList:
                if type(item) <> list:
                    outList.append(item)
                else:
                    outList.extend(item)
        else:
            outList.append(inList)
        return outList
    def MHEList(Events):
        outList = []
        i = 0
        for item in Events:
             i += 1
             if float(i) / 2 == i / 2:
                 outList.append(item)
        return outList              

    #arcpy.SetProgressor("step","Import Crash Attributes - Unit File",0,100,1)
    #arcpy.SetProgressorLabel("Update Crash Layer:")
    #arcpy.SetProgressorPosition(0)
    #PP = 0

    UC = arcpy.UpdateCursor(CrashLayer)
    SC = arcpy.SearchCursor(UnitFile)
    SRow = SC.next()
    ANOU = GetIntVal(SRow,'ANO')
    for URow in UC:
        ANOC = GetIntVal(URow,'ANO',-1)
        UNT  = GetIntVal(URow,'UNT',-1)
        FHE  = GetIntVal(URow,'FHE',-1)
        MAC  = GetIntVal(URow,'MAC',-1)
        while ANOU < ANOC:
            SRow = SC.next()
            if not SRow:
                ANOU = 999999999
            else:
                ANOU = GetIntVal(SRow,'ANO',-2)
        if ANOC == ANOU:
            SOE = str(GetIntVal(SRow,'SOE'))
            MHE = GetIntVal(SRow,'MHE',-1)
            MAN = GetIntVal(SRow,'MAN',-1)
            MACList = [MAC, MAN]
            SOEList = SOEExtract(SOE)
            Events = [FHE, MHE]
            Events.append(SOEList)
            URow.setValue(F_CT_SOE1['name'],SOEList[0])
            URow.setValue(F_CT_SOE2['name'],SOEList[1])
            URow.setValue(F_CT_SOE3['name'],SOEList[2])
            URow.setValue(F_CT_SOE4['name'],SOEList[3])
            URow.setValue(F_CT_MHE['name'],MHE)
            k = 0
            UTCList = []
            while ANOC == ANOU:
                k += 1
                temp = SRow.getValue('UTC')
                UTCList.append(temp)
                SOE = str(GetIntVal(SRow,'SOE'))
                MHE = GetIntVal(SRow,'MHE',-1)
                MAN = GetIntVal(SRow,'MAN',-1)
                MACList.append(MAN)
                SOEList = SOEExtract(SOE)
                Events.append(MHE)
                Events.append(SOEList)
                SRow = SC.next()
                if not SRow:
                    ANOU = 999999999
                else:
                    ANOU = GetIntVal(SRow,'ANO',-2)
            URow.setValue(F_CT_UNF['name'],k)
            NV = NumberOfVehicles(UTCList, Events)
            URow.setValue(F_CT_NV['name'],NV)
            URow.setValue(F_CT_Code['name'],CCode(NV,Events,MACList))
            FO = 0
            if AnyofList1inList2(range(40,69),ExplodeSubLists(Events)):
                FO = 1
            URow.setValue(F_CT_FO['name'],FO)
            UC.updateRow(URow)
        elif ANOU > ANOC:
            arcpy.AddMessage("ANO: " + str(ANOC) + " Not Found in Unit File")


    Output = arcpy.CopyFeatures_management(CrashLayer,Output)
    for Field in [F_CT_SOE1, F_CT_SOE2, F_CT_SOE3, F_CT_SOE4, F_CT_MHE, F_CT_UNF, F_CT_NV]:
        arcpy.DeleteField_management(Output,Field['name'])

    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")
def CrashSplitter(CrashInput,IntersectionsLayer,RoadsLayer,Output):
    arcpy.AddMessage("   ")
    arcpy.AddMessage("   Crash Split")

    OutDic = OutputParser(Output, 'shp')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("   Copy: Crash Layer")
    CrashLayer = CopyFeatures(CrashInput,'CSplit_Temp')
    TotalCrashes = int(str(arcpy.GetCount_management(CrashLayer)))
    arcpy.AddMessage("    - " + str(TotalCrashes))

    arcpy.AddMessage("   Adding XY: Crash Layer")
    arcpy.DeleteField_management(CrashLayer,'POINT_X')
    arcpy.DeleteField_management(CrashLayer,'POINT_Y')
    arcpy.AddXY_management(CrashLayer)

    arcpy.AddMessage("   Add Field: Crash Layer")
    CrashFieldDic = [F_TargetFID, F_RCrash, F_ICrash, F_RFType, F_RFID, F_CI_X, F_CI_Y, F_Dist2CF]
    for Field in CrashFieldDic:
        AddField(CrashLayer,Field)

    def ReadCrash(Row,Field,Default=-1):
        try:
            return int(Row.getValue(Field))
        except:
            return Default
    def CalRatio(Dist,ABuffer,BBuffer,AADTMajor,AADTMinor,JCT,MAC):
            Ratio = 0
            if Dist <= ABuffer:
                Ratio = 500000 + AADTMajor + AADTMinor
            elif Dist > ABuffer and Dist <= BBuffer:
                if (JCT in [1,3,4,7,8,12] or MAC in [10]) and JCT <> 2:
                    Ratio = AADTMajor + AADTMinor + 1
            return Ratio

    UC = arcpy.UpdateCursor(CrashLayer)
    FID = 0
    for URow in UC:
        URow.setValue(F_TargetFID['name'],FID)
        FID += 1
        UC.updateRow(URow)

    arcpy.AddMessage("   Read Crash Data")
    CrashDic = {SRow.getValue(F_TargetFID['name']):{'MAC':ReadCrash(SRow,F_CT_MAC['name']),'JCT':ReadCrash(SRow,F_CT_JCT['name']),'RCT':ReadCrash(SRow,F_CT_RCT['name']),'C_X': SRow.getValue("POINT_X"),'C_Y': SRow.getValue("POINT_Y"),'IList':[],'RList':[]} for SRow in arcpy.SearchCursor(CrashLayer)}

    arcpy.AddMessage("   Spatial Join: Crash Layer + Intersections Layer")
    IMaxBuffer = max(MaximumValue(IntersectionsLayer,F_ABuffer['name']),MaximumValue(IntersectionsLayer,F_BBuffer['name']))
    SPJI = SpatialJoin(CrashLayer, IntersectionsLayer,"SPJI" , {'join_operation': "JOIN_ONE_TO_MANY", 'join_type': "KEEP_COMMON",'field_mapping': "",'match_option': "WITHIN_A_DISTANCE",'search_radius': str(IMaxBuffer) + " Feet",'distance_field_name': "distance"})

    arcpy.AddMessage("   Append Intersection Data")
    for SRow in arcpy.SearchCursor(SPJI):
        X = SRow.getValue(F_X['name'])
        Y = SRow.getValue(F_Y['name'])
        FID   = SRow.getValue(F_TargetFID['name'])
        Dist  = ((CrashDic[FID]['C_X'] - X) ** 2 + (CrashDic[FID]['C_Y'] - Y) ** 2) ** 0.5
        Ratio = CalRatio(Dist,SRow.getValue(F_ABuffer['name']),SRow.getValue(F_BBuffer['name']),SRow.getValue(F_AADT_Major['name']),SRow.getValue(F_AADT_Minor['name']),CrashDic[FID]['JCT'],CrashDic[FID]['MAC'])
        if Ratio > 0:
            CrashDic[FID]['IList'].append({'Dist': Dist, 'Type': SRow.getValue(F_FType['name']),'X':X,'Y':Y,'Ratio': Ratio})

    arcpy.AddMessage("   Spatial Join: Crash Layer + Roads Layer")
    RMaxBuffer = MaximumValue(RoadsLayer ,F_RBuffer['name'])
    SPJR = SpatialJoin(CrashLayer, RoadsLayer,"SPJR" , {'join_operation': "JOIN_ONE_TO_ONE" , 'join_type': "KEEP_COMMON",'field_mapping': "",'match_option': "CLOSEST"          ,'search_radius': str(RMaxBuffer) + " Feet" ,'distance_field_name': "distance"})

    arcpy.AddMessage("   Append Roadway Data")
    for SRow in arcpy.SearchCursor(SPJR):
        Dist = SRow.getValue("distance")
        FID  = SRow.getValue(F_TargetFID['name'])
        if Dist <= SRow.getValue(F_RBuffer['name']):
            CrashDic[FID]['RList'].append({'Dist': Dist, 'Type': SRow.getValue(F_FType['name']),'RFID':SRow.getValue(F_RouteFID['name'])})

    arcpy.AddMessage("   Update Cursor: Crash Layer")
    
    UC = arcpy.UpdateCursor(CrashLayer)
    arcpy.SetProgressor("step"," ",0,TotalCrashes,1)
    arcpy.SetProgressorLabel("Update Crash Layer:")
    arcpy.SetProgressorPosition(0)
    for URow in UC:
        FID = ReadCrash(URow,F_TargetFID['name'])
        MaxRatio = 0
        MaxIndex = 0
        for i in range(0,len(CrashDic[FID]['IList'])):
            Ratio = CrashDic[FID]['IList'][i]['Ratio']
            if Ratio > MaxRatio:
                MaxRatio = Ratio
                MaxIndex = i
        if MaxRatio > 0:
            if len(CrashDic[FID]['RList']) > 0 or MaxRatio >= 500000:
                URow.setValue(F_ICrash ['name'], 1)
                URow.setValue(F_CI_X   ['name'], CrashDic[FID]['IList'][MaxIndex]['X'])
                URow.setValue(F_CI_Y   ['name'], CrashDic[FID]['IList'][MaxIndex]['Y'])
                URow.setValue(F_Dist2CF['name'], CrashDic[FID]['IList'][MaxIndex]['Dist'])
                URow.setValue(F_RFType ['name'], CrashDic[FID]['IList'][MaxIndex]['Type'])
                #arcpy.AddMessage("   FID = " + str(FID) + ', Intersection at ' + str(int(CrashDic[FID]['IList'][MaxIndex]['Dist'])) + ' Feet')
        else:
            if len(CrashDic[FID]['RList']) > 0 and CrashDic[FID]['JCT'] in [13,2,7]:
                URow.setValue(F_RCrash ['name'], 1)
                URow.setValue(F_RFType ['name'], CrashDic[FID]['RList'][0]['Type'])
                URow.setValue(F_RFID   ['name'], CrashDic[FID]['RList'][0]['RFID'])
                URow.setValue(F_Dist2CF['name'], CrashDic[FID]['RList'][0]['Dist'])
                #arcpy.AddMessage("   FID = " + str(FID) + ", Roadway at " + str(int(CrashDic[FID]['RList'][0]['Dist'])) + ' Feet')
        UC.updateRow(URow)
        arcpy.SetProgressorPosition(FID)

    arcpy.AddMessage("   Copy: Output")
    arcpy.DeleteField_management(CrashLayer, F_TargetFID['name'])
    arcpy.CopyFeatures_management(CrashLayer, Output)

    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")
def CrashFilter(CrashInput,RoadsLayer,Output):
    arcpy.AddMessage("   ")
    arcpy.AddMessage("   Crash Split")

    OutDic = OutputParser(Output, 'shp')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("   Copy: Crash Layer")
    CrashLayer = CopyFeatures(CrashInput,'CSplit_Temp')

    arcpy.AddMessage("   Get Count: Crash Layer")
    TotalCrashes = int(str(arcpy.GetCount_management(CrashLayer)))
    arcpy.AddMessage("    - " + str(TotalCrashes))

    arcpy.AddMessage("   Adding XY: Crash Layer")
    arcpy.DeleteField_management(CrashLayer,'POINT_X')
    arcpy.DeleteField_management(CrashLayer,'POINT_Y')
    arcpy.AddXY_management(CrashLayer)

    arcpy.AddMessage("   Add Field: Crash Layer")
    CrashFieldDic = [F_TargetFID,F_Selected]
    for Field in CrashFieldDic:
        AddField(CrashLayer,Field)

    UC = arcpy.UpdateCursor(CrashLayer)
    for URow in UC:
        FID = GetFID(URow)
        URow.setValue(F_TargetFID['name'],FID)
        UC.updateRow(URow)

    def ReadCrash(Row,Field,Default=-1):
        try:
            return int(Row.getValue(Field))
        except:
            return Default

    arcpy.AddMessage("   Read Crash Data")
    CrashDic = {SRow.getValue(F_TargetFID['name']):{'CTY':ReadCrash(SRow,'CTY'),'RCT':ReadCrash(SRow,F_CT_RCT['name']),'RTN':ReadCrash(SRow,'RTN'),'RList':[]} for SRow in arcpy.SearchCursor(CrashLayer)}

    arcpy.AddMessage("   Buffer: Road Layer")
    RB = Buffer(RoadsLayer,'CFRoads',{'distance': 'RBuffer', 'line_side': 'FULL', 'line_end_type': 'FLAT', 'dissolve_option': 'NONE', 'dissolve_field': '#'})

    arcpy.AddMessage("   Spatial Join: Crash Layer + Buffer Layer")
    SPJI = SpatialJoin(CrashLayer, RB,"SPJI" , {'join_operation': "JOIN_ONE_TO_MANY", 'join_type': "KEEP_COMMON",'field_mapping': "",'match_option': "INTERSECT",'search_radius': "",'distance_field_name': ""})

    arcpy.AddMessage("   Search Cursor: Spatial Join Layer")
    for SRow in arcpy.SearchCursor(SPJI):
        FID   = SRow.getValue(F_TargetFID['name'])
        CrashDic[FID]['RList'].append({'CTY': int(SRow.getValue(F_County['name'])),'RCT':int(SRow.getValue(F_Route_Type['name'])),'RTN':int(SRow.getValue(F_Route_Numb['name']))})

    arcpy.AddMessage("   Update Cursor: Crash Layer")
    
    UC = arcpy.UpdateCursor(CrashLayer)
    arcpy.SetProgressor("step"," ",0,TotalCrashes,1)
    arcpy.SetProgressorLabel("Update Crash Layer:")
    arcpy.SetProgressorPosition(0)
    Correct = 0
    for URow in UC:
        FID = ReadCrash(URow,F_TargetFID['name'])
        CTY = ReadCrash(URow,'CTY',0)
        RCT = ReadCrash(URow,'RCT',0)
        RTN = ReadCrash(URow,'RTN',0)
        Flag = False
        for i in range(0,len(CrashDic[FID]['RList'])):
            if CrashDic[FID]['RList'][i]['CTY']<>0 and CrashDic[FID]['RList'][i]['CTY']==CTY:
                if CrashDic[FID]['RList'][i]['RCT']<>0 and CompareRCT(RCT,CrashDic[FID]['RList'][i]['RCT']):
                    if CrashDic[FID]['RList'][i]['RTN']<>0 and RTN==CrashDic[FID]['RList'][i]['RTN']:
                        Flag = True

        if Flag:
            URow.setValue(F_Selected['name'], 1)
        else:
            Correct = Correct + 1    
            URow.setValue(F_Selected['name'], 0)

        UC.updateRow(URow)
        arcpy.SetProgressorPosition(FID)
    arcpy.AddMessage("    - False Crashes: "+str(Correct))

    arcpy.AddMessage("   Copy: Output")
    arcpy.DeleteField_management(CrashLayer, F_TargetFID['name'])
    arcpy.CopyFeatures_management(CrashLayer, Output)

    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")
def ObservedCrash(SitesInput, CrashLayer, Output):
    arcpy.AddMessage("    ")
    arcpy.AddMessage("    Add Observed Crashes")

    OutDic = OutputParser(Output, 'shp')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("    Copy Features: Sites Layer")
    SitesLayer = CopyFeatures(SitesInput,'OCSites')
    TotalSites = int(str(arcpy.GetCount_management(SitesLayer)))
    arcpy.AddMessage("     - Total number of Items Found: " + str(TotalSites))
    Shape = arcpy.Describe(SitesInput).shapetype

    arcpy.AddMessage("    Adding Fields")
    CrashFieldDic = [F_TargetFID, F_OC_FIDs, F_TOT_OC, F_FI_OC, F_MV_OC, F_MVFI_OC, F_MVPDO_OC, F_SV_OC, F_SVFI_OC, F_SVPDO_OC, F_Ped_OC]
    for Field in CrashFieldDic:
        arcpy.DeleteField_management(SitesLayer,Field['name'])
    for Field in CrashFieldDic:
        AddField(SitesLayer,Field)
    CalField(SitesLayer,F_TargetFID,'!OBJECTID! - 1')

    arcpy.AddMessage("    Reading Sites Information")
    if Shape=='Polyline':
        IntDic = {SRow.getValue('DISSOLVEID'):{'CList':[]} for SRow in arcpy.SearchCursor(SitesLayer)}
    if Shape=='Point':
        IntDic = {SRow.getValue(F_TargetFID['name']):{'CList':[]} for SRow in arcpy.SearchCursor(SitesLayer)}

    arcpy.AddMessage("    Buffer: SitesLayer")
    if Shape=='Polyline':
        BF = Buffer(SitesLayer,'BUF',{'distance': "RBuffer", 'line_side': 'FULL', 'line_end_type': 'FLAT', 'dissolve_option': 'LIST', 'dissolve_field': 'DISSOLVEID'})
    if Shape=='Point':
        BF = Buffer(SitesLayer,'BUF',{'distance': "BBuffer", 'line_side': 'FULL', 'line_end_type': 'FLAT', 'dissolve_option': 'NONE', 'dissolve_field': '#'})

    arcpy.AddMessage("    Spatial Join: CrashLayer + SitesLayer")
    SPJ = SpatialJoin(CrashLayer, BF, "SPJ" , {'join_operation': "JOIN_ONE_TO_ONE", 'join_type': "KEEP_COMMON",'field_mapping': "",'match_option': "INTERSECT",'search_radius': "0",'distance_field_name':'Dist'})
    TotalMatches = int(str(arcpy.GetCount_management(SPJ)))
    arcpy.AddMessage("     - Total number of Items Found: " + str(TotalMatches))

    arcpy.AddMessage("    Appending Crash Information")
    for SRow in arcpy.SearchCursor(SPJ):
        if Shape=='Polyline':
            FID     = SRow.getValue('DISSOLVEID')
            if ((GetVal(SRow, F_ICrash['name'], 0) == 1 and Shape == 'Point') or (GetVal(SRow, F_RCrash['name'], 0) == 1 and Shape == 'Polyline')):
                IntDic[FID]['CList'].append({'FAT':GetVal(SRow,F_CT_FAT['name']), 'INJ':GetVal(SRow,F_CT_INJ['name']), 'UNT':GetVal(SRow,F_CT_UNT['name']),'FID':GetVal(SRow,"FID"), 'FHE':GetVal(SRow,F_CT_FHE['name'])})
        if Shape=='Point':
            FID     = SRow.getValue(F_TargetFID['name'])
            if ((GetVal(SRow, F_ICrash['name'], 0) == 1 and Shape == 'Point') or (GetVal(SRow, F_RCrash['name'], 0) == 1 and Shape == 'Polyline')):
                IntDic[FID]['CList'].append({'FAT':GetVal(SRow,F_CT_FAT['name']), 'INJ':GetVal(SRow,F_CT_INJ['name']), 'UNT':GetVal(SRow,F_CT_UNT['name']),'FID':GetVal(SRow,"FID"), 'FHE':GetVal(SRow,F_CT_FHE['name'])})

    arcpy.AddMessage("    Update Cursor: Sites Layer")
    def AddCrash(TargetRow,CrashDic):
        FAT = CrashDic['FAT']
        INJ = CrashDic['INJ']
        UNT = CrashDic['UNT']
        FID = CrashDic['FID']
        FHE = CrashDic['FHE']

        b = TargetRow.getValue(F_OC_FIDs['name'])
        if not b:
            b = ''
        if b == '':
            s = str(FID)
        else:
            if len(b + ',' + str(FID)) < F_OC_FIDs['length']:
                s = b + ',' + str(FID)
            else:
                s = b
        TargetRow.setValue(F_OC_FIDs['name'], s)
    
        b = TargetRow.getValue(F_TOT_OC['name'])
        if not b:
            b = 0
        TargetRow.setValue(F_TOT_OC['name'], b + 1)
        if (FAT > 0 or INJ > 0):
            b = TargetRow.getValue(F_FI_OC['name'])
            if not b:
                b = 0
            TargetRow.setValue(F_FI_OC['name'], b + 1)

        if UNT > 1:
            b = TargetRow.getValue(F_MV_OC['name'])
            if not b:
                b = 0
            TargetRow.setValue(F_MV_OC['name'], b + 1)
            if (FAT > 0 or INJ > 0):
                b = TargetRow.getValue(F_MVFI_OC['name'])
                if not b:
                    b = 0
                TargetRow.setValue(F_MVFI_OC['name'], b + 1)
            else:
                b = TargetRow.getValue(F_MVPDO_OC['name'])
                if not b:
                    b = 0
                TargetRow.setValue(F_MVPDO_OC['name'], b + 1)
        if UNT <= 1:
            b = TargetRow.getValue(F_SV_OC['name'])
            if not b:
                b = 0
            TargetRow.setValue(F_SV_OC['name'], b + 1)
            if (FAT > 0 or INJ > 0):
                b = TargetRow.getValue(F_SVFI_OC['name'])
                if not b:
                    b = 0
                TargetRow.setValue(F_SVFI_OC['name'], b + 1)
            else:
                b = TargetRow.getValue(F_SVPDO_OC['name'])
                if not b:
                    b = 0
                TargetRow.setValue(F_SVPDO_OC['name'], b + 1)
        if FHE == 27:
                b = TargetRow.getValue(F_Ped_OC['name'])
                if not b:
                    b = 0
                TargetRow.setValue(F_Ped_OC['name'], b + 1)        
        return TargetRow
    Tot_OC = 0
    UC = arcpy.UpdateCursor(SitesLayer)
    for URow in UC:
        if Shape=='Polyline':
            RFID     = URow.getValue('DISSOLVEID')
        if Shape=='Point':
            RFID    = URow.getValue(F_TargetFID['name'])
        CrashesFound = 0
        for Crash in IntDic[RFID]['CList']:
            URow = AddCrash(URow,Crash)
            CrashesFound += 1
            UC.updateRow(URow)
        #if CrashesFound >= 1:
        #    arcpy.AddMessage("     %5.0f" % RFID + " out of %5.0f" % TotalSites + ", Crashes Found: " + str(CrashesFound))
        Tot_OC += CrashesFound

    arcpy.AddMessage("     - Total Observed Crashes Matched: " + str(Tot_OC))
    arcpy.CopyFeatures_management(SitesLayer, Output)

    for Field in [F_TargetFID, F_OC_FIDs]:
        arcpy.DeleteField_management(Output,Field['name'])

    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")
def CrashType(CrashLayer, Output):
    arcpy.AddMessage(" ")
    arcpy.AddMessage("   Crash Types")

    arcpy.SelectLayerByAttribute_management(CrashLayer,'CLEAR_SELECTION')

    OutDic = OutputParser(Output, 'xls')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("   Reading Crash Information")
    CrashDic = {FType:[] for FType in FTypes}
    for FType in FTypes:
        for SRow in arcpy.SearchCursor(CrashLayer,'"' + F_RFType['name'] + """" = '""" + FType + "'"):
            CrashDic[FType].append({'INJ':SRow.getValue(F_CT_INJ['name']),'Code':SRow.getValue(F_CT_Code['name']),'TIM':SRow.getValue(F_CT_TIM['name']),'FO':SRow.getValue(F_CT_FO['name'])})

    arcpy.AddMessage("   Creating the Output Table")
    tempTable = CreateFeatureclass('Temp_CrashTypes',{'geometry_type':"POINT",'has_m':'ENABLED','has_z':'ENABLED'})
    

    arcpy.AddMessage("   Adding Required Fields")
    CrashTypeDic = [F_FType, F_CT_Night, F_CT_Units, F_CT_ColTyp, F_CT_Fatal, F_CT_IncInj, F_CT_NInInj, F_CT_PosInj, F_CT_TotFI, F_CT_PDO, F_CT_Total] 
    for Field in CrashTypeDic:
        AddField(tempTable,Field)

    arcpy.AddMessage("   Insert Cursor: Output")
    def AddCrashTypes(CL, IC, NewRow):
        Tot = len(CL)
        NewRow.setValue(F_CT_Total['name'],Tot)

        Fatal = len([Dic for Dic in CL if Dic['INJ']==4])
        NewRow.setValue(F_CT_Fatal['name'],Fatal)

        IncInj = len([Dic for Dic in CL if Dic['INJ']==3])
        NewRow.setValue(F_CT_IncInj['name'],IncInj)

        NInInj = len([Dic for Dic in CL if Dic['INJ']==2])
        NewRow.setValue(F_CT_NInInj['name'],NInInj)

        PosInj = len([Dic for Dic in CL if Dic['INJ']==1])
        NewRow.setValue(F_CT_PosInj['name'],PosInj)

        TotFI = Fatal + IncInj + NInInj + PosInj
        NewRow.setValue(F_CT_TotFI['name'],TotFI)

        PDO = Tot - TotFI
        NewRow.setValue(F_CT_PDO['name'],PDO)
    
        IC.insertRow(NewRow)
        return IC

    IC = arcpy.InsertCursor(tempTable)

    for FType in FTypes:    #FacilityTypes:
        #2 Total
        NewRow = IC.newRow()
        NewRow.setValue(F_FType['name'],FType)
        NewRow.setValue(F_CT_Night['name'],'Both')
        NewRow.setValue(F_CT_Units['name'],'All')
        NewRow.setValue(F_CT_ColTyp['name'],'All')
        IC = AddCrashTypes([Dic for Dic in CrashDic[FType] if Dic['Code']>=100], IC, NewRow)
    
        #3 Night Time
        NewRow = IC.newRow()
        NewRow.setValue(F_FType['name'],FType)
        NewRow.setValue(F_CT_Night['name'],'Night')
        NewRow.setValue(F_CT_Units['name'],'All')
        NewRow.setValue(F_CT_ColTyp['name'],'All')
        IC = AddCrashTypes([Dic for Dic in CrashDic[FType] if Dic['Code']>=100 and (Dic['TIM']<=599 or Dic['TIM']>=1800)], IC, NewRow)

        #Single Vehicle
        #4 Total
        NewRow = IC.newRow()
        NewRow.setValue(F_FType['name'],FType)
        NewRow.setValue(F_CT_Night['name'],'Both')
        NewRow.setValue(F_CT_Units['name'],'Single Vehicle')
        NewRow.setValue(F_CT_ColTyp['name'],'All')
        IC = AddCrashTypes([Dic for Dic in CrashDic[FType] if Dic['Code']>=100 and Dic['Code']<200], IC, NewRow)
        #5 Collision with Animals
        NewRow = IC.newRow()
        NewRow.setValue(F_FType['name'],FType)
        NewRow.setValue(F_CT_Night['name'],'Both')
        NewRow.setValue(F_CT_Units['name'],'Single Vehicle')
        NewRow.setValue(F_CT_ColTyp['name'],'Animals')
        IC = AddCrashTypes([Dic for Dic in CrashDic[FType] if Dic['Code']==131], IC, NewRow)
        #7 Parked Vehicle
        NewRow = IC.newRow()
        NewRow.setValue(F_FType['name'],FType)
        NewRow.setValue(F_CT_Night['name'],'Both')
        NewRow.setValue(F_CT_Units['name'],'Single Vehicle')
        NewRow.setValue(F_CT_ColTyp['name'],'Parked Vehicle')
        IC = AddCrashTypes([Dic for Dic in CrashDic[FType] if Dic['Code']==133], IC, NewRow)
        #6 Bicycle
        NewRow = IC.newRow()
        NewRow.setValue(F_FType['name'],FType)
        NewRow.setValue(F_CT_Night['name'],'Both')
        NewRow.setValue(F_CT_Units['name'],'Single Vehicle')
        NewRow.setValue(F_CT_ColTyp['name'],'Bicycle')
        IC = AddCrashTypes([Dic for Dic in CrashDic[FType] if Dic['Code']==132], IC, NewRow)
        #7 Pedestrian
        NewRow = IC.newRow()
        NewRow.setValue(F_FType['name'],FType)
        NewRow.setValue(F_CT_Night['name'],'Both')
        NewRow.setValue(F_CT_Units['name'],'Single Vehicle')
        NewRow.setValue(F_CT_ColTyp['name'],'Pedestrian')
        IC = AddCrashTypes([Dic for Dic in CrashDic[FType] if Dic['Code']==134], IC, NewRow)
        #8 Turn over
        NewRow = IC.newRow()
        NewRow.setValue(F_FType['name'],FType)
        NewRow.setValue(F_CT_Night['name'],'Both')
        NewRow.setValue(F_CT_Units['name'],'Single Vehicle')
        NewRow.setValue(F_CT_ColTyp['name'],'Turnover')
        IC = AddCrashTypes([Dic for Dic in CrashDic[FType] if Dic['Code'] in [112,122,136]], IC, NewRow)
        #9 Ran offroad
        NewRow = IC.newRow()
        NewRow.setValue(F_FType['name'],FType)
        NewRow.setValue(F_CT_Night['name'],'Both')
        NewRow.setValue(F_CT_Units['name'],'Single Vehicle')
        NewRow.setValue(F_CT_ColTyp['name'],'Ran offroad')
        IC = AddCrashTypes([Dic for Dic in CrashDic[FType] if Dic['Code'] in [111,121,135]], IC, NewRow)
        #10 Collision with Fixed Objects
        NewRow = IC.newRow()
        NewRow.setValue(F_FType['name'],FType)
        NewRow.setValue(F_CT_Night['name'],'Both')
        NewRow.setValue(F_CT_Units['name'],'Single Vehicle')
        NewRow.setValue(F_CT_ColTyp['name'],'Fixed Objects')
        IC = AddCrashTypes([Dic for Dic in CrashDic[FType] if Dic['Code'] >= 120 and Dic['Code'] < 130], IC, NewRow)
        #11 Collision with Other Objects
        NewRow = IC.newRow()
        NewRow.setValue(F_FType['name'],FType)
        NewRow.setValue(F_CT_Night['name'],'Both')
        NewRow.setValue(F_CT_Units['name'],'Single Vehicle')
        NewRow.setValue(F_CT_ColTyp['name'],'Other Objects')
        IC = AddCrashTypes([Dic for Dic in CrashDic[FType] if Dic['Code'] >= 130 and Dic['Code'] < 140], IC, NewRow)
        #11 NonCollision
        NewRow = IC.newRow()
        NewRow.setValue(F_FType['name'],FType)
        NewRow.setValue(F_CT_Night['name'],'Both')
        NewRow.setValue(F_CT_Units['name'],'Single Vehicle')
        NewRow.setValue(F_CT_ColTyp['name'],'NonCollision')
        IC = AddCrashTypes([Dic for Dic in CrashDic[FType] if Dic['Code'] >= 110 and Dic['Code'] < 120], IC, NewRow)

        #Multi Vehicle
        #12 Total
        NewRow = IC.newRow()
        NewRow.setValue(F_FType['name'],FType)
        NewRow.setValue(F_CT_Night['name'],'Both')
        NewRow.setValue(F_CT_Units['name'],'Multi Vehicle')
        NewRow.setValue(F_CT_ColTyp['name'],'All')
        IC = AddCrashTypes([Dic for Dic in CrashDic[FType] if Dic['Code'] >= 200], IC, NewRow)
        #13 Angle Collision
        NewRow = IC.newRow()
        NewRow.setValue(F_FType['name'],FType)
        NewRow.setValue(F_CT_Night['name'],'Both')
        NewRow.setValue(F_CT_Units['name'],'Multi Vehicle')
        NewRow.setValue(F_CT_ColTyp['name'],'Angle')
        IC = AddCrashTypes([Dic for Dic in CrashDic[FType] if Dic['Code'] == 210], IC, NewRow)
        #14 Head-on Collision
        NewRow = IC.newRow()
        NewRow.setValue(F_FType['name'],FType)
        NewRow.setValue(F_CT_Night['name'],'Both')
        NewRow.setValue(F_CT_Units['name'],'Multi Vehicle')
        NewRow.setValue(F_CT_ColTyp['name'],'Head-on')
        IC = AddCrashTypes([Dic for Dic in CrashDic[FType] if Dic['Code'] == 220], IC, NewRow)
        #15 Rear-end Collisions
        NewRow = IC.newRow()
        NewRow.setValue(F_FType['name'],FType)
        NewRow.setValue(F_CT_Night['name'],'Both')
        NewRow.setValue(F_CT_Units['name'],'Multi Vehicle')
        NewRow.setValue(F_CT_ColTyp['name'],'Rear-end')
        IC = AddCrashTypes([Dic for Dic in CrashDic[FType] if Dic['Code'] == 230], IC, NewRow)
        # Sideswipe Same Direction
        NewRow = IC.newRow()
        NewRow.setValue(F_FType['name'],FType)
        NewRow.setValue(F_CT_Night['name'],'Both')
        NewRow.setValue(F_CT_Units['name'],'Multi Vehicle')
        NewRow.setValue(F_CT_ColTyp['name'],'Sideswipe Same Direction')
        IC = AddCrashTypes([Dic for Dic in CrashDic[FType] if Dic['Code'] == 241], IC, NewRow)
        # Sideswipe Opposite Direction
        NewRow = IC.newRow()
        NewRow.setValue(F_FType['name'],FType)
        NewRow.setValue(F_CT_Night['name'],'Both')
        NewRow.setValue(F_CT_Units['name'],'Multi Vehicle')
        NewRow.setValue(F_CT_ColTyp['name'],'Sideswipe Opposite Direction')
        IC = AddCrashTypes([Dic for Dic in CrashDic[FType] if Dic['Code'] == 242], IC, NewRow)
        #16 Sideswipe All
        NewRow = IC.newRow()
        NewRow.setValue(F_FType['name'],FType)
        NewRow.setValue(F_CT_Night['name'],'Both')
        NewRow.setValue(F_CT_Units['name'],'Multi Vehicle')
        NewRow.setValue(F_CT_ColTyp['name'],'Sideswipe')
        IC = AddCrashTypes([Dic for Dic in CrashDic[FType] if Dic['Code'] >= 240 and Dic['Code'] < 250], IC, NewRow)
        #17 Other Multi Vehicle
        NewRow = IC.newRow()
        NewRow.setValue(F_FType['name'],FType)
        NewRow.setValue(F_CT_Night['name'],'Both')
        NewRow.setValue(F_CT_Units['name'],'Multi Vehicle')
        NewRow.setValue(F_CT_ColTyp['name'],'Other')
        IC = AddCrashTypes([Dic for Dic in CrashDic[FType] if Dic['Code'] == 250], IC, NewRow)
        #18 Collision with Fixed Objects
        NewRow = IC.newRow()
        NewRow.setValue(F_FType['name'],FType)
        NewRow.setValue(F_CT_Night['name'],'Both')
        NewRow.setValue(F_CT_Units['name'],'All')
        NewRow.setValue(F_CT_ColTyp['name'],'Fixed Objects')
        IC = AddCrashTypes([Dic for Dic in CrashDic[FType] if Dic['FO'] == 1], IC, NewRow)
  
        arcpy.AddMessage("    - Type " + FType + " Done.")
    arcpy.TableToExcel_conversion(tempTable, Output)
    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")
def SecondaryCrashes(CrashInput,TimeInt,Distance,Output):
    import datetime
    arcpy.AddMessage(" ")
    arcpy.AddMessage("   Secondary Crashes")

    OutDic = OutputParser(Output, 'shp')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("   Copy: Crash Layer")
    arcpy.Delete_management('ERCrash')
    arcpy.Delete_management('ERCrash2')
    CrashLayer = CopyFeatures(CrashInput,'ERCrash')
    CrashLayer2 = CopyFeatures(CrashInput,'ERCrash2')
    C = arcpy.GetCount_management(CrashLayer)
    arcpy.AddMessage("     - Total Items Found: " + str(C))

    arcpy.AddMessage("   Search Cursor: Crash Layer")
    
    CDic = {SRow.getValue('ANO'):{'P'   :SRow.getValue('Shape'),
                                  'Time':SRow.getValue(F_CT_TIM['name']),
                                  'Date':SRow.getValue(F_CT_DAT['name']),
                                  'RCT' :SRow.getValue(F_CT_RCT['name']),
                                  'RTN' :SRow.getValue(F_CT_RTN['name']),
                                  'DIR' :SRow.getValue(F_CT_DLR['name'])} for SRow in arcpy.SearchCursor(CrashLayer)}

    ClearFields(CrashLayer2,["ANO"])
    arcpy.AddMessage("   Spatial Join: Crash Layer + Crash Layer")
    SPJ = SpatialJoin(CrashLayer2, CrashLayer2, "SecSPJ", {'join_operation':"JOIN_ONE_TO_MANY",'join_type':"KEEP_ALL", 'field_mapping':'', 'match_option':"WITHIN_A_DISTANCE",'search_radius':str(Distance)+" Feet",'distance_field_name':''})
    
    arcpy.AddMessage("   Finding Crash Pairs ...")
    SortedANO = sorted(CDic.keys())
    Pairs   = {ANO:[] for ANO in SortedANO}
    FPair   = {ANO:-1 for ANO in SortedANO}
    Primary = []
    Secondary = []
    for SRow in arcpy.SearchCursor(SPJ):
        ANO1 = SRow.getValue("ANO")
        ANO2 = SRow.getValue("ANO_1")
        if ANO2>ANO1:
            Pairs[ANO1].append(ANO2)
    def GetDistance(P1,P2):
        X1 = P1.firstPoint.X
        X2 = P2.firstPoint.X
        Y1 = P1.firstPoint.Y
        Y2 = P2.firstPoint.Y
        return(((X1-X2)**2+(Y1-Y2)**2)**0.5)
    def DateDecompose(Date,Time):
            Date = str(Date)
            D = 0
            M = 0
            Y = 0
            if len(Date) == 7:
                M = (Date[0])
                D = (Date[1:3])
                Y = (Date[3:7])
            if len(Date) == 8:
                M = (Date[0:2])
                D = (Date[2:4])
                Y = (Date[4:8])

            h = 0
            m = 0
            Time = str(Time)
            if len(Time) <= 2:
                h = '0'
                m = (Time)
            if len(Time) == 3:
                h = (Time[0])
                m = (Time[1:3])
            if len(Time) == 4:
                h = (Time[0:2])
                m = (Time[2:4])
            
            flag = False
            try:
                m = int(m)
            except:
                flag = True
                m = 0
            try:
                h = int(h)
            except:
                flag = True
                h = 0
            try:
                M = int(M)
            except:
                flag = True
                M = 1
            try:
                D = int(D)
            except:
                flag = True
                D = 1
            try:
                Y = int(Y)
            except:
                flag = True
                Y = 2007
            if m>59: flag = True;m = 59
            if m<0 : flag = True;m = 0
            if h>23: flag = True;h = 23;m = 59
            if h<0 : flag = True;h = 0
            if M>12: flag = True;M = 12
            if M<0 : flag = True;M = 0
            if D>31: flag = True;D = 31
            if D<0 : flag = True;D = 0
            try:
                out = datetime.datetime(int(Y),int(M),int(D),int(h),int(m))
            except:
                falg = True
                out = datetime.datetime(2007,1,1,0,0)
            #if flag:
            #    arcpy.AddWarning('     - Out of range date: ' + Date + ', ' + Time + ' => ' + str(out))

            return(out)
    Prg = 0.1
    for ANO1 in SortedANO:
        if float(SortedANO.index(ANO1))/float(str(C)) >= Prg:
            arcpy.AddMessage("    - " + str(int(Prg*100)) + "% Completed")
            Prg = Prg + 0.1
        for ANO2 in Pairs[ANO1]:
            if CDic[ANO1]['RCT'] == CDic[ANO2]['RCT']:
                if CDic[ANO1]['RTN'] == CDic[ANO2]['RTN']:
                    D1 = DateDecompose(CDic[ANO1]['Date'],CDic[ANO1]['Time'])
                    D2 = DateDecompose(CDic[ANO2]['Date'],CDic[ANO2]['Time'])
                    if abs(D1-D2).total_seconds()/3600<=float(TimeInt):
                        if (D2-D1).total_seconds() > 0 and not (ANO1 in Secondary):
                            FPair[ANO2]=(ANO1)
                            Primary.append(ANO1)
                            Secondary.append(ANO2)
                            #arcpy.AddMessage(str(ANO1)+', ' + str(ANO2)+','+str(abs(D1-D2).total_seconds()/3600))
                        if (D1-D2).total_seconds() > 0 and not (ANO2 in Secondary):
                            FPair[ANO1]=(ANO2)
                            Primary.append(ANO2)
                            Secondary.append(ANO1)
                            #arcpy.AddMessage(str(ANO2)+', ' + str(ANO1)+','+str(abs(D1-D2).total_seconds()/3600))
    
    arcpy.AddMessage("   Add Field: Crash Layer")
    for Field in [F_CT_PrmSec,F_CT_Tempor,F_CT_Spatio]:
        AddField(CrashLayer,Field)
    arcpy.AddMessage("   Update Cursor: Crash Layer")
    i = 0
    UC = arcpy.UpdateCursor(CrashLayer)
    for URow in UC:
        ANO = URow.getValue("ANO")
        if ANO in Primary:
            URow.setValue(F_CT_PrmSec['name'],'Primary')
        if ANO in Secondary:
            URow.setValue(F_CT_PrmSec['name'],FPair[ANO])
            D1 = DateDecompose(CDic[ANO       ]['Date'],CDic[ANO       ]['Time'])
            D2 = DateDecompose(CDic[FPair[ANO]]['Date'],CDic[FPair[ANO]]['Time'])
            URow.setValue(F_CT_Tempor['name'],abs(D1-D2).total_seconds()/60)
            URow.setValue(F_CT_Spatio['name'],GetDistance(CDic[ANO]['P'],CDic[FPair[ANO]]['P']))

        UC.updateRow(URow)
    
    arcpy.CopyFeatures_management(CrashLayer, Output)
    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")
def CrashGeocode(LocFile,LatField,LonField,ANOField,CrashYear,StateLayer,Output,OutOfState):
    arcpy.AddMessage(" ")
    arcpy.AddMessage("   Geocode Crashes")
    CrashYear = int(CrashYear)
    OutDic = OutputParser(Output, 'shp')
    Output = OutDic['folder'] + '\\' + OutDic['file']
    OutDic = OutputParser(OutOfState, 'shp')
    OutTab = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("   Copy: Location File")
    arcpy.Delete_management('CG_Table')
    LocTable = TableToTable(LocFile,arcpy.env.workspace,'CG_Table')
    C = arcpy.GetCount_management(LocFile)
    arcpy.AddMessage("     - Total Items Found: " + str(C))

    arcpy.AddMessage("   Search Cursor: Location File")
    def Deg2Dec(S):
        Deg = 0
        Min = 0
        Sec = 0
        if len(S)==8:
            Deg = S[0:2]
            Min = S[2:4]
            Sec = S[4:8]
        try:
            Dec = float(Deg) + float(Min)/60 +  float(Sec)/100/3600
            if Dec>70: Dec = -Dec
        except:
            Dec = 0
        return(Dec)
    CDic = {GetANO(SRow):{'Lat':Deg2Dec(str(SRow.getValue(LatField))),
                                     'Lon':Deg2Dec(str(SRow.getValue(LonField)))} for SRow in arcpy.SearchCursor(LocFile)}
    Tot = len(CDic)
    arcpy.AddMessage("   Create Feature Class: Crash Layer")
    arcpy.Delete_management('CG_Crash')
    CrashLayer = CreateFeatureclass('CG_Crash',{'geometry_type':"POINT",'has_m':'DISABLED','has_z':'DISABLED'})

    arcpy.AddMessage("    Create Out of State Table")
    arcpy.Delete_management('OTable')
    Tab = CreateTable(arcpy.env.workspace,"OTable")

    arcpy.AddMessage("   Add Fields: Crash Layer")
    FieldDic = [F_CT_Label,F_CT_ANO]
    for rec in FieldDic:
        AddField(CrashLayer,rec)
        AddField(Tab,rec)

    arcpy.AddMessage("   Define Projection: Crash Layer")
    arcpy.DefineProjection_management(CrashLayer,arcpy.SpatialReference(4326))

    arcpy.AddMessage("   Insert Cursor: Crash Layer")
    Pt = arcpy.Point()
    IC = arcpy.InsertCursor(CrashLayer) 
    ANOList = CDic.keys()
    ANOList.sort()
    j = 0
    for ANO in ANOList:
        if ANO >= (CrashYear - 2000) * 10 ** 6 and ANO < (CrashYear - 2000) * 10 ** 6 + 999999 and ANO <> 99999999:
            j = j + 1
            IRow = IC.newRow() 
            Pt.X = CDic[ANO]['Lon']
            Pt.Y = CDic[ANO]['Lat']
            IRow.setValue(F_CT_ANO['name'],ANO)
            IRow.shape = Pt
            IC.insertRow(IRow)      

    arcpy.AddMessage("   Project: Crash Layer")
    CrashLayer = Project(CrashLayer,CoordSystemSC)
    
    arcpy.AddMessage("   Spatial Join: Crash Layer + State Layer")
    arcpy.Delete_management('CGSPJ')
    SPJ = SpatialJoin(CrashLayer,StateLayer,'CGSPJ',{'join_operation':"JOIN_ONE_TO_ONE",'join_type':"KEEP_COMMON", 'field_mapping':'', 'match_option':"INTERSECT",'search_radius':'','distance_field_name':''})
    InState = [SRow.getValue('ANO') for SRow in arcpy.SearchCursor(SPJ)]


    arcpy.AddMessage("   Update Cursor: Crash Layer")
    UC = arcpy.UpdateCursor(CrashLayer) 
    for URow in UC:
        ANO = GetANO(URow) 
        if not ANO in InState:
            UC.deleteRow(URow)      
    
    t = float(str(C))
    i = float(len(InState))
    ip = i/t
    ip = int(ip*10000)/100.0

    arcpy.AddMessage("   Total: %d, False ANOs: %d, In-state(percentage): %d, %r" %(t, (t-j), i, ip))
    CalField(CrashLayer,F_CT_Label,'!ANO!')
    arcpy.CopyFeatures_management(CrashLayer, Output)

    arcpy.AddMessage("   Insert Cursor: Out of State Crash Table")
    IC = arcpy.InsertCursor(Tab) 
    ANOList = CDic.keys()
    ANOList.sort()
    j = 0
    for ANO in ANOList:
        if not ANO in InState:
            if ANO >= (CrashYear - 2000) * 10 ** 6 and ANO < (CrashYear - 2000) * 10 ** 6 + 999999 and ANO <> 99999999:
                j = j + 1
                IRow = IC.newRow() 
                IRow.setValue(F_CT_ANO['name'],ANO)
                IC.insertRow(IRow)      
    arcpy.AddMessage("   Out-state: %d" %(j))
    CalField(Tab,F_CT_Label,'!ANO!')
    arcpy.CopyRows_management(Tab, OutTab)

    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")
def FindDBClusters(CrashInput,Eps,MinPts,Output):
    Eps = float(Eps)
    MinPts = int(MinPts)
    arcpy.AddMessage(" ")
    arcpy.AddMessage("   Find Density Base Clusters")

    OutDic = OutputParser(Output, 'shp')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("   Copy: Crash Layer")
    CrashLayer = CopyFeatures(CrashInput,'ERCrash')
    TotalSites = int(str(arcpy.GetCount_management(CrashLayer)))
    arcpy.AddMessage("     - Total number of Items Found: " + str(TotalSites))

    arcpy.AddMessage("   Spatial Join: Crash Layer + Crash Layer")
    CList = [{'visited':'N','Noise':'N','Neigh':[],'CNum':0} for SRow in arcpy.SearchCursor(CrashLayer)]
    SPJ = SpatialJoin(CrashLayer, CrashLayer, "DBSPJ", {'join_operation':"JOIN_ONE_TO_MANY",'join_type':"KEEP_ALL", 'field_mapping':'', 'match_option':"WITHIN_A_DISTANCE",'search_radius':str(Eps)+" Feet",'distance_field_name':''})

    arcpy.AddMessage("   Search Cursor: Spatial Join Layer")
    for SRow in arcpy.SearchCursor(SPJ):
        i = SRow.getValue('TARGET_FID')-1
        j = SRow.getValue('JOIN_FID')-1
        if j>i:
            CList[i]['Neigh'].append(j)
    #for c in CList:
        #arcpy.AddMessage(str(c['Neigh']))
    arcpy.AddMessage("   DBSCAN")
    def DBSCAN(D,MinPts):
        def expandCluster(D, i, C, MinPts):
            D[i]['CNum'] = C
            V = [i]
            NV = [t for t in P['Neigh']]
            while len(NV)>0: 
                j = NV[0]
                if not j in V:
                    V.append(j)
                    D[j]['visited']='Y'
                    NV.remove(j)
                    if len(D[j]['Neigh']) >= MinPts:
                        L = [t for t in D[j]['Neigh'] if t not in V and t not in NV] 
                        NV.extend(L)
                    if D[j]['CNum']==0:
                        D[j]['CNum'] = C
            return (D)
        C = 0
        for i in range(0,len(D)):
            P = D[i]
            if D[i]['visited']=='N':
                D[i]['visited']='Y'
                if len(P['Neigh']) < MinPts:
                    P['Noise'] = 'Y'
                else:
                    C = C + 1
                    D = expandCluster(D, i, C, MinPts)
        return (D)
    CList = DBSCAN(CList,MinPts)
    CSize = {C['CNum']:0 for C in CList}
    for c in CList:
        CID = c['CNum']
        CSize[CID]=CSize[CID]+1


    arcpy.AddMessage("   Add Field: Crash Layer")
    for Field in [F_CNum,F_CSize]:
        AddField(CrashLayer,Field)

    arcpy.AddMessage("   Update Cursor: Crash Layer")
    UC = arcpy.UpdateCursor(CrashLayer)
    i = 0
    for URow in UC:
        if CList[i]['CNum' ]>0:
            URow.setValue(F_CNum ['name'],CList[i]['CNum' ])
            URow.setValue(F_CSize['name'],CSize[CList[i]['CNum']])
            UC.updateRow(URow)
        i = i+1

    arcpy.CopyFeatures_management(CrashLayer, Output)
    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")
def BatchGDB(Locs,Units,Occs,StateBoundary,Jur,Years,OutputPath):
    import os
    # Add jurisdiction
    # Add route LRS for all 3 routes described in crash database
    #arcpy.env.workspace = os.path.dirname(Locs.split(';')[0])
    Years = [int(y) for y in Years.split(';')]
    #arcpy.AddMessage(arcpy.env.workspace)
    Loc  = [l[1:-1] for l in Locs.split(';')]
    Unit = [l[1:-1] for l in Units.split(';')]
    Occ  = [l[1:-1] for l in Occs.split(';')]

    for i in range(0,len(Years)):
        arcpy.AddMessage(Years[i])
        arcpy.AddMessage(Loc[i])
        arcpy.AddMessage(Unit[i])
        arcpy.AddMessage(Occ[i])

        arcpy.Delete_management('Geo'+str(Years[i]))
        arcpy.Delete_management('Out'+str(Years[i]))
        Geo = CrashGeocode(Loc[i],"LAT","LON","ANO",Years[i],StateBoundary,'Geo'+str(Years[i]),'Out'+str(Years[i]))

        arcpy.Delete_management('Att'+str(Years[i]))
        Att = ImpotCrashAttributes('Geo'+str(Years[i]),Loc[i],'Att'+str(Years[i]))
        arcpy.Delete_management('OutAtt'+str(Years[i]))
        OutAtt = ImpotCrashAttributes('Out'+str(Years[i]),Loc[i],'OutAtt'+str(Years[i]))

        AddField('Att'+str(Years[i]),F_CT_Symbol)
        CalField('Att'+str(Years[i]),F_CT_Symbol,'fval(!UNT!,!FAT!,!INJ!)',"""def fval(unt,fat,inj):
        s1 = 'MV'
        if unt<2:
            s1 = 'SV'
        s2 = 'PDO'
        if inj>0:
            s2 = 'Inj'
        if fat>0:
            s2 = 'Fat'
        code = {'MVFat':1,'MVInj':2,'MVPDO':3,'SVFat':4,'SVInj':5,'SVPDO':6}
        return(code[s1+s2])""")
        AddField('Att'+str(Years[i]),F_Route_LRS)
        CalField('Att'+str(Years[i]),F_Route_LRS,'fval( !CTY!, !RCT!, !RTN!, !RAI!, !DLR!, !TWAY!)',"""def fval(cnty,rt,rn,aux,dir,oneway):
            rtdict = {1:1,2:2,3:4,4:7,5:9}
            if rt in rtdict.keys():
                rt = rtdict[rt]
            if not dir in ['E','W','N','S']:
                dir = 'T'
            if oneway in [2,3]:
                dir = 'T'
            if not rn>0:
                rn=0
            return('{:02.0f}{:02.0f}{:05.0f}{:02.0f}{}'.format(cnty,rt,rn,aux,dir))""")
        AddField('OutAtt'+str(Years[i]),F_Route_LRS)
        CalField('OutAtt'+str(Years[i]),F_Route_LRS,'fval( !CTY!, !RCT!, !RTN!, !RAI!, !DLR!, !TWAY!)',"""def fval(cnty,rt,rn,aux,dir,oneway):
            rtdict = {1:1,2:2,3:4,4:7,5:9}
            if rt in rtdict.keys():
                rt = rtdict[rt]
            if not dir in ['E','W','N','S']:
                dir = 'T'
            if oneway in [2,3]:
                dir = 'T'
            if not rn>0:
                rn=0
            return('{:02.0f}{:02.0f}{:05.0f}{:02.0f}{}'.format(cnty,rt,rn,aux,dir))""")

        arcpy.Delete_management('Sec'+str(Years[i]))
        Sec = SecondaryCrashes('Att'+str(Years[i]),2,2500,'Sec'+str(Years[i]))
        SecL = MakeFeatureLayer('Sec'+str(Years[i]),'SecL'+str(Years[i]))
        arcpy.SelectLayerByAttribute_management(SecL,'NEW_SELECTION',"PrmSec IS NOT NULL AND PrmSec <> 'Primary'")
        Sec = CopyFeatures(SecL,'SelSecL')
        ClearFields(Sec,[F_CT_ANO['name'],F_CT_Label['name'],F_CT_PrmSec['name'],F_CT_Tempor['name'],F_CT_Spatio['name']])
        CalField(Sec,F_CT_Label,"'{:3.0f}{}{:4.0f}{}'.format(!"+F_CT_Tempor['name']+"!,' Min, ',!"+F_CT_Spatio['name']+"!,' Feet')")
        AddField(Sec,F_CT_PrmANO)
        CalField(Sec,F_CT_PrmANO,'!'+F_CT_PrmSec['name']+'!')
        arcpy.DeleteField_management(Sec,F_CT_PrmSec['name'])

        arcpy.Delete_management('Unit'+str(Years[i]))
        UTb = ImpotUnitAttributes(Unit[i],Years[i],'Unit'+str(Years[i]))

        arcpy.Delete_management('Occ'+str(Years[i]))
        OTb = ImpotOccAttributes(Occ[i],Years[i],'Occ'+str(Years[i]))

        GDB = CreateGeodatabase('Att'+str(Years[i]),'Unit'+str(Years[i]),'Occ'+str(Years[i]),'OutAtt'+str(Years[i]),Years[i],OutputPath+'\\SC_Crash_'+str(Years[i])+'.mdb')
        
        arcpy.AddMessage('    Add Secondary Table')
        Sec = arcpy.TableToTable_conversion(Sec,OutputPath+'\\SC_Crash_'+str(Years[i])+'.mdb','Sec'+str(Years[i]))
        arcpy.AddMessage('    Add Jurisdiction Feature Class')
        JurTab = arcpy.FeatureClassToFeatureClass_conversion(Jur,OutputPath+'\\SC_Crash_'+str(Years[i])+'.mdb','Jur')
        
        L   = OutputPath+'\\SC_Crash_'+str(Years[i])+'.mdb\\'+'Loc'+str(Years[i])
        Sec = OutputPath+'\\SC_Crash_'+str(Years[i])+'.mdb\\'+'Sec'+str(Years[i])
        Out = OutputPath+'\\SC_Crash_'+str(Years[i])+'.mdb\\'+'Out'+str(Years[i])
        UTb = OutputPath+'\\SC_Crash_'+str(Years[i])+'.mdb\\'+'Unit'+str(Years[i])
        JUR = OutputPath+'\\SC_Crash_'+str(Years[i])+'.mdb\\'+'Jur'

        arcpy.AddMessage('    Create Relationships')
        arcpy.CreateRelationshipClass_management(L, Sec, OutputPath+'\\SC_Crash_'+str(Years[i])+'.mdb'+"\\PriCrash-SecTable", "SIMPLE", "Secondary Table", "Primary Crash"  , "NONE", "ONE_TO_MANY", "NONE", "ANO", F_CT_PrmANO['name'])    
        arcpy.CreateRelationshipClass_management(Sec, L, OutputPath+'\\SC_Crash_'+str(Years[i])+'.mdb'+"\\SecTable-SecCrash", "SIMPLE", "Secondary Crash", "Secondary Table", "NONE", "ONE_TO_ONE" , "NONE", "ANO", "ANO")    
        arcpy.CreateRelationshipClass_management(L, JUR, OutputPath+'\\SC_Crash_'+str(Years[i])+'.mdb'+"\\Loc-Jur"          , "SIMPLE", "Jur Table"      , "Loc Table"      , "NONE", "ONE_TO_MANY", "NONE", "JUR", "JUR")    
        
        arcpy.AddMessage('    Add Representation')
        try:
            arcpy.AddRepresentation_cartography(L,"CrashType","NU_Sev","Override","STORE_CHANGE_AS_OVERRIDE","C:\\Users\\mrajabi\\Dropbox\\GDB Crash layer.lyr","ASSIGN")
        except:
            DoNothing = True        
        try:
            arcpy.CalculateField_management(L,'NU_Sev','!'+F_CT_Symbol['name']+'!',"PYTHON_9.3")
        except:
            DoNothing = True
        try:
            arcpy.AddMessage('    Compact the Database')
            arcpy.Compact_management(OutputPath+'\\SC_Crash_'+str(Years[i])+'.mdb')
            #arcpy.CompressFileGeodatabaseData_management (OutputPath+'\\SC_Crash_'+str(Years[i])+'.mdb', "Lossless compression")
        except:
            DoNothing = True



# Roadway segment analysis
def HorCurvature(Dic):
    import math
    Inf = 10**10 
    def Radius(P1,P2,P3):
        Inf = 10**10
        x1 = P1[0];x2 = P2[0];x3 = P3[0]
        y1 = P1[1];y2 = P2[1];y3 = P3[1]
        if y1==y2 and y2==y3:
            R = Inf
        elif y1==y2 and y2<>y3:
            m2 = -(x3-x2)/(y3-y2)
            xm1 = (x1+x2)/2
            ym1 = (y1+y2)/2
            xm2 = (x3+x2)/2
            ym2 = (y3+y2)/2
            xc = xm1
            yc = m2*(xc-xm2)+ym2
            R  = math.sqrt((xc-x1)**2+(yc-y1)**2)
        elif y2==y3 and y1<>y2:
            m1 = -(x2-x1)/(y2-y1)
            xm1 = (x1+x2)/2
            ym1 = (y1+y2)/2
            xm2 = (x3+x2)/2
            ym2 = (y3+y2)/2
            xc = xm2
            yc = m1*(xc-xm1)+ym1
            R  = math.sqrt((xc-x1)**2+(yc-y1)**2)
        elif y1<>y2 and y3<>y2:
            if y3 == y1:
                R = Inf
            elif y3<>y1:
                if (x3-x1)/(y3-y1) == (x2-x1)/(y2-y1):
                    R = Inf
                else:
                    m1 = -(x2-x1)/(y2-y1)
                    m2 = -(x3-x2)/(y3-y2)
                    xm1 = (x1+x2)/2
                    ym1 = (y1+y2)/2
                    xm2 = (x3+x2)/2
                    ym2 = (y3+y2)/2
                    xc = (ym1-ym2+m2*xm2-m1*xm1)/(m2-m1)
                    yc = m1*(xc-xm1)+ym1
                    R  = math.sqrt((xc-x1)**2+(yc-y1)**2)
        return(R)
    def Length(P1,P2):
        return(math.sqrt((P2[0]-P1[0])**2+(P2[1]-P1[1])**2))
    Vertices = Dic['Path']
    R = []
    L = Dic['Length']
    for i in range(2,len(Vertices)):
        l1 = Length(Vertices[i-2],Vertices[i-1])
        l2 = Length(Vertices[i-1],Vertices[i  ])
        R.append(Radius(Vertices[i-2],Vertices[i-1],Vertices[i]))
    if L<0.05*5280:
        R = []
    if len(R) == 0:
        R.append(Inf)
    return(R)
def VerCurvature(Dic):
    L = Dic['Length']
    Z = Dic['MeanZ' ]
    Lf = 0
    Zf = 0
    for List in Dic['FirstPoint']:
        Lf += List[0]/len(Dic['FirstPoint'])
        Zf += List[1]/len(Dic['FirstPoint'])
    Ll = 0
    Zl = 0
    for List in Dic['LastPoint']:
        Ll += List[0]/len(Dic['LastPoint'])
        Zl += List[1]/len(Dic['LastPoint'])
    if Lf==0 and Ll==0:
        G = 0
    if Lf<>0 and Ll<>0:
        G = max([abs(Z-Zf)/(L+Lf)*2,abs(Z-Zl)/(L+Ll)*2])
    if Lf==0 and Ll<>0:
        G = abs(Z-Zl)/(L+Ll)*2
    if Lf<>0 and Ll==0:
        G = abs(Z-Zf)/(L+Lf)*2
    if G>1:
        arcpy.AddMessage(str([L,Z,Ll,Zl,Lf,Zf,G]))
    return(G)
def Resegment2(Att,Road):
    OutField = []
    OutPath = []
    MMP = MergeMileposts(Att['MP'],Road['MP'])
    NullField = []
    for mp in MMP:
        Flag = False
        for amp in Road['MP']:
            i = Road['MP'].index(amp)
            if mp[0]>=amp[0] and mp[1]<= amp[1]:
                OutField.append(Road['Fields'][i])
                Flag = True
                break
        if not Flag: OutField.append(NullField)
        for rmp in Road['MP']:
            if rmp[0]<=mp[0] and rmp[1]>=mp[1]:
                i = Road['MP'].index(rmp)
                OutPath.append(DivideSegment(rmp,Road['Path'][i],mp))
                break
    return {'MP':MMP,'Fields':OutField,'Path':OutPath}
## CheckCollectedData
def MedianWidth(M_Width_ft,Median_Wid, Median_Typ):
    M1 = M_Width_ft
    M2 = Median_Wid
    T = Median_Typ
    MW = 0 
    if M1 == 0 and M2 <> 0:
        MW = M2 
    elif M1 <> 0 and M2 == 0:
        MW = M1
    elif M1 <> 0 and M2 <> 0:
        MW = max(M1, M2)
    elif M1 == 0 and M2 == 0:
        i = 0 
        for i in range(0,len(T)):
            if not T[len(T) - i - 1] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']:
                break
        try:
            MW = float(T[len(T) - i:])
        except:
            MW = 0
    return MW
def CheckOnStreetParking(DataInput, PTField, ATField, DBuffer, Output):
    arcpy.AddMessage(" ")
    arcpy.AddMessage("    On Street Parking Check For Duplicates")

    #DataInput = sys.argv[1]
    #PTField = sys.argv[2]
    #ATField = sys.argv[3]
    #DBuffer = sys.argv[4]
    #Output = sys.argv[5]

    OutDic = OutputParser(Output, 'shp')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("    Copy OSP Layer")
    DataLayer = CopyFeatures(DataInput,'OSPInput')
    TotalSites = arcpy.GetCount_management(DataLayer)
    arcpy.AddMessage("     - Total number of OSPs Found: " + str(TotalSites))

    arcpy.AddMessage("    Saving Target FID: OSP Layer")
    FieldList1 = [F_TargetFID]
    FieldList2 = [F_JoinFID, F_RefFID, F_SimSites]

    for Field in FieldList1:
        AddField(DataLayer,Field)

    UC = arcpy.UpdateCursor(DataLayer)
    for URow in UC:
        FID = GetFID(URow)
        URow.setValue(F_TargetFID['name'],FID)
        UC.updateRow(URow)
    FIDIntersect = {SRow.getValue(F_TargetFID['name']):[] for SRow in arcpy.SearchCursor(DataLayer)}

    arcpy.AddMessage("    Buffer: OSP Layer")
    SBuffer = Buffer(DataLayer, "OSPBuffer",{'distance': DBuffer, 'line_side': 'FULL', 'line_end_type': 'FLAT', 'dissolve_option': 'NONE', 'dissolve_field': '#'})

    arcpy.AddMessage("    Saving Join FID: Point Layer")
    for Field in FieldList2:
        AddField(DataLayer,Field)

    UC = arcpy.UpdateCursor(DataLayer)
    for URow in UC:
        FID = GetFID(URow)
        URow.setValue(F_JoinFID['name'],FID)
        UC.updateRow(URow)

    arcpy.AddMessage("    Intersect: Buffer + Point Layer")
    BI = Intersect(SBuffer + ';' + DataLayer,"PDIntersect",{'join_attributes': "ALL", 'cluster_tolerance': '', 'output_type': "LINE"})

    arcpy.AddMessage("    Finding Duplicates")
    for SRow in arcpy.SearchCursor(BI):
        FIDIntersect[SRow.getValue(F_TargetFID['name'])].append(SRow.getValue(F_JoinFID['name']))
    FIDInt = FIDIntersect.values()

    FIDInt.sort()
    for i in FIDInt:
        i.sort()

    def PopDuplicate(List):
	    Flag = False
	    i = -1
	    while not Flag and i < len(List) - 2:
		    i += 1
		    if List[i] == List[i + 1] and not Flag:
			    Flag = True
			    List.pop(i)
	    return {'List': List, 'Status': Flag}

    InitLen = len(FIDInt)
    T = PopDuplicate(FIDInt)
    while T['Status']:
        T = PopDuplicate(FIDInt)
    FinalLen = len(FIDInt)
    arcpy.AddMessage("     - " + str(InitLen) + " to " + str(FinalLen) + ", " + str(InitLen - FinalLen) + " Duplicates Found")

    PTList = []
    ATList = []
    for FIDL in FIDInt:
        T = []
        for FID in FIDL:
            T.append(0)
        PTList.append(T)
        ATList.append(T)

    SC = arcpy.SearchCursor(DataLayer)
    for SRow in SC:
        SFID = SRow.getValue(F_TargetFID['name'])
        PType = SRow.getValue(PTField)
        AType = SRow.getValue(ATField)
        i = 0
        for FIDL in FIDInt:
            try:
                j = FIDL.index(SFID)
                break
            except:
                j = -1
            i += 1
        if j <> -1:
            PTList[i][j] = PType
            ATList[i][j] = AType
        else:
            arcpy.AddError("OSPs without geospatial coordinations")

    SelFID = []
    RefFID = []
    for i in range(0,len(FIDInt)):
        if len(FIDInt[i]) > 1:
            if PTList[i].count(PTList[i][0]) <> len(PTList[i]) or ATList[i].count(ATList[i][0]) <> len(ATList[i]):
                Seli = 0
                MinAT = 7
                MinPT = 3
                for at in ATList[i]:
                    if at < MinAT and at <> 0:
                        MinAT = at
                        Seli = ATList[i].index(at)
                if Seli >= len(FIDInt[i]):Seli = 0
                for j in range(0,len(FIDInt[i])):
                    if j <> Seli:
                        SelFID.append(FIDInt[i][j])
                        RefFID.append(FIDInt[i][Seli])
                arcpy.AddWarning("     - FIDs: " + str(FIDInt[i]) + ", AreaType: " + str(ATList[i]) + ", ParkingType: " + str(PTList[i]) + ", Sel: " + str({FIDInt[i][Seli]:DWList[i][Seli]}))
            else:
                for j in range(1,len(FIDInt[i])):
                    SelFID.append(FIDInt[i][j])
                    RefFID.append(FIDInt[i][0])
    arcpy.AddMessage("     - # of FIDs to remove: " + str(len(SelFID)))

    arcpy.AddMessage("    Delete Duplicates: OSP Layer")
    UC = arcpy.UpdateCursor(DataLayer)
    for URow in UC:
        SFID = URow.getValue(F_TargetFID['name'])
        URow.setValue(F_SimSites['name'],RefFID.count(SFID))
        if SFID in SelFID:
            URow.setValue(F_RefFID['name'],RefFID[SelFID.index(SFID)])
        else:
            URow.setValue(F_RefFID['name'],SFID)
        UC.updateRow(URow)

    temp = arcpy.CopyFeatures_management(DataLayer, Output)

    UC = arcpy.UpdateCursor(temp)
    for URow in UC:
        SFID = URow.getValue(F_TargetFID['name'])
        RFID = URow.getValue(F_RefFID['name'])
        if SFID <> RFID:
            UC.deleteRow(URow)

    for Field in [F_TargetFID, F_JoinFID, F_RefFID]:
        arcpy.DeleteField_management(temp,Field['name'])

    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")
def CheckFixedObjects(DataInput,FOField,DCField,DBuffer,Output):
    arcpy.AddMessage(" ")
    arcpy.AddMessage("    Fixed Object Check For Duplicates")

    #DataInput = sys.argv[1]
    #FOField = sys.argv[2]
    #DCField = sys.argv[3]
    #DBuffer = sys.argv[4]
    #Output = sys.argv[5]

    OutDic = OutputParser(Output, 'shp')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("    Copy FO Layer")
    DataLayer = CopyFeatures(DataInput,'FOInput')
    TotalSites = arcpy.GetCount_management(DataLayer)
    arcpy.AddMessage("     - Total number of items Found: " + str(TotalSites))

    arcpy.AddMessage("    Saving Target FID: FO Layer")
    FieldList1 = [F_TargetFID]
    FieldList2 = [F_JoinFID, F_RefFID, F_SimSites]

    for Field in FieldList1:
        AddField(DataLayer,Field)

    UC = arcpy.UpdateCursor(DataLayer)
    for URow in UC:
        FID = GetFID(URow)
        URow.setValue(F_TargetFID['name'],FID)
        UC.updateRow(URow)
    FIDIntersect = {SRow.getValue(F_TargetFID['name']):[] for SRow in arcpy.SearchCursor(DataLayer)}

    arcpy.AddMessage("    Buffer: FO Layer")
    SBuffer = Buffer(DataLayer, "FOBuffer",{'distance': DBuffer, 'line_side': 'FULL', 'line_end_type': 'FLAT', 'dissolve_option': 'NONE', 'dissolve_field': '#'})

    arcpy.AddMessage("    Saving Join FID: Point Layer")
    for Field in FieldList2:
        AddField(DataLayer,Field)

    UC = arcpy.UpdateCursor(DataLayer)
    for URow in UC:
        FID = GetFID(URow)
        URow.setValue(F_JoinFID['name'],FID)
        UC.updateRow(URow)

    arcpy.AddMessage("    Intersect: Buffer + Point Layer")
    BI = Intersect(SBuffer + ';' + DataLayer,"FOIntersect",{'join_attributes': "ALL", 'cluster_tolerance': '', 'output_type': "LINE"})

    arcpy.AddMessage("    Finding Duplicates")
    for SRow in arcpy.SearchCursor(BI):
        FIDIntersect[SRow.getValue(F_TargetFID['name'])].append(SRow.getValue(F_JoinFID['name']))
    FIDInt = FIDIntersect.values()

    FIDInt.sort()
    for i in FIDInt:
        i.sort()

    def PopDuplicate(List):
	    Flag = False
	    i = -1
	    while not Flag and i < len(List) - 2:
		    i += 1
		    if List[i] == List[i + 1] and not Flag:
			    Flag = True
			    List.pop(i)
	    return {'List': List, 'Status': Flag}

    InitLen = len(FIDInt)
    T = PopDuplicate(FIDInt)
    while T['Status']:
        T = PopDuplicate(FIDInt)
    FinalLen = len(FIDInt)
    arcpy.AddMessage("     - " + str(InitLen) + " to " + str(FinalLen) + ", " + str(InitLen - FinalLen) + " Duplicates Found")

    DCList = []
    FOList = []
    for FIDL in FIDInt:
        T = []
        for FID in FIDL:
            T.append(0)
        DCList.append(T)
        FOList.append(T)

    SC = arcpy.SearchCursor(DataLayer)
    for SRow in SC:
        SFID = SRow.getValue(F_TargetFID['name'])
        DC = SRow.getValue(DCField)
        FO = SRow.getValue(FOField)
        i = 0
        for FIDL in FIDInt:
            try:
                j = FIDL.index(SFID)
                break
            except:
                j = -1
            i += 1
        if j <> -1:
            DCList[i][j] = DC
            FOList[i][j] = FO
        else:
            arcpy.AddError("Item without geospatial coordinations")

    SelFID = []
    RefFID = []
    for i in range(0,len(FIDInt)):
        if len(FIDInt[i]) > 1:
            if DCList[i].count(DCList[i][0]) <> len(DCList[i]) or FOList[i].count(FOList[i][0]) <> len(FOList[i]):
                Seli = 0
                #MinAT = 7
                #MinPT = 3
                #for at in ATList[i]:
                #    if at < MinAT and at <> 0:
                #        MinAT = at
                #        Seli = ATList[i].index(at)
                #if Seli >= len(FIDInt[i]):Seli = 0
                for j in range(0,len(FIDInt[i])):
                    if j <> Seli:
                        SelFID.append(FIDInt[i][j])
                        RefFID.append(FIDInt[i][Seli])
                arcpy.AddWarning("     - FIDs: " + str(FIDInt[i]) + ", DCType: " + str(DCList[i]) + ", Number of FO: " + str(FOList[i]) + ", Sel: " + str({FIDInt[i][Seli]}))
            else:
                for j in range(1,len(FIDInt[i])):
                    SelFID.append(FIDInt[i][j])
                    RefFID.append(FIDInt[i][0])
    arcpy.AddMessage("     - # of FIDs to remove: " + str(len(SelFID)))

    arcpy.AddMessage("    Delete Duplicates: OSP Layer")
    UC = arcpy.UpdateCursor(DataLayer)
    for URow in UC:
        SFID = URow.getValue(F_TargetFID['name'])
        URow.setValue(F_SimSites['name'],RefFID.count(SFID))
        if SFID in SelFID:
            URow.setValue(F_RefFID['name'],RefFID[SelFID.index(SFID)])
        else:
            URow.setValue(F_RefFID['name'],SFID)
        UC.updateRow(URow)

    temp = arcpy.CopyFeatures_management(DataLayer, Output)

    UC = arcpy.UpdateCursor(temp)
    for URow in UC:
        SFID = URow.getValue(F_TargetFID['name'])
        RFID = URow.getValue(F_RefFID['name'])
        if SFID <> RFID:
            UC.deleteRow(URow)

    for Field in [F_TargetFID, F_JoinFID, F_RefFID]:
        arcpy.DeleteField_management(temp,Field['name'])

    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")
def CheckMedianWidth(DataInput, MWField, MTField, DBuffer, Output):  
    arcpy.AddMessage(" ")
    arcpy.AddMessage("    Median Width Check For Duplicates")

    #DataInput = sys.argv[1]
    #MWField = sys.argv[2]
    #MTField = sys.argv[3]
    #DBuffer = sys.argv[4]
    #Output = sys.argv[5]

    OutDic = OutputParser(Output, 'shp')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("    Copy Point Layer")
    DataLayer = CopyFeatures(DataInput,'PDInput')
    TotalSites = arcpy.GetCount_management(DataLayer)
    arcpy.AddMessage("     - Total number of Points Found: " + str(TotalSites))

    arcpy.AddMessage("    Saving Target FID: Point Layer")
    FieldList1 = [F_TargetFID]
    FieldList2 = [F_JoinFID, F_RefFID, F_SimSites]

    for Field in FieldList1:
        AddField(DataLayer,Field)

    UC = arcpy.UpdateCursor(DataLayer)
    for URow in UC:
        FID = GetFID(URow)
        URow.setValue(F_TargetFID['name'],FID)
        UC.updateRow(URow)
    FIDIntersect = {SRow.getValue(F_TargetFID['name']):[] for SRow in arcpy.SearchCursor(DataLayer)}

    arcpy.AddMessage("    Buffer: DataLayer")
    SBuffer = Buffer(DataLayer, "PDBuffer",{'distance': DBuffer, 'line_side': 'FULL', 'line_end_type': 'FLAT', 'dissolve_option': 'NONE', 'dissolve_field': '#'})

    arcpy.AddMessage("    Saving Join FID: Point Layer")
    for Field in FieldList2:
        AddField(DataLayer,Field)

    UC = arcpy.UpdateCursor(DataLayer)
    for URow in UC:
        FID = GetFID(URow)
        URow.setValue(F_JoinFID['name'],FID)
        UC.updateRow(URow)

    arcpy.AddMessage("    Intersect: Buffer + Point Layer")
    BI = Intersect(SBuffer + ';' + DataLayer,"PDIntersect",{'join_attributes': "ALL", 'cluster_tolerance': '', 'output_type': "POINT"})

    arcpy.AddMessage("    Finding Duplicates")
    for SRow in arcpy.SearchCursor(BI):
        FIDIntersect[SRow.getValue(F_TargetFID['name'])].append(SRow.getValue(F_JoinFID['name']))
    FIDInt = FIDIntersect.values()

    FIDInt.sort()
    for i in FIDInt:
        i.sort()

    def PopDuplicate(List):
	    Flag = False
	    i = -1
	    while not Flag and i < len(List) - 2:
		    i += 1
		    if List[i] == List[i + 1] and not Flag:
			    Flag = True
			    List.pop(i)
	    return {'List': List, 'Status': Flag}

    InitLen = len(FIDInt)
    T = PopDuplicate(FIDInt)
    while T['Status']:
        T = PopDuplicate(FIDInt)
    FinalLen = len(FIDInt)
    arcpy.AddMessage("     - " + str(InitLen) + " to " + str(FinalLen) + ", " + str(InitLen - FinalLen) + " Duplicates Found")

    MWList = []
    for FIDL in FIDInt:
        T = []
        for FID in FIDL:
            T.append(0)
        MWList.append(T)

    MTList = []
    for FIDL in FIDInt:
        T = []
        for FID in FIDL:
            T.append(0)
        MTList.append(T)

    SC = arcpy.SearchCursor(DataLayer)
    for SRow in SC:
        SFID = SRow.getValue(F_TargetFID['name'])
        MWidth = SRow.getValue(MWField)
        MType = SRow.getValue(MTField)
        i = 0
        for FIDL in FIDInt:
            try:
                j = FIDL.index(SFID)
                break
            except:
                j = -1
            i += 1
        if j <> -1:
            MWList[i][j] = MWidth
            MTList[i][j] = MType
        else:
            arcpy.AddError("Points without geospatial coordinations")

    SelFID = []
    RefFID = []
    for i in range(0,len(FIDInt)):
        if len(FIDInt[i]) > 1:
            if MWList[i].count(MWList[i][0]) <> len(MWList[i]):
                Seli = 0
                MaxMW = 0
                for mw in MWList[i]:
                    if mw > MaxMW:
                        MaxMW = mw
                        Seli = MWList[i].index(mw)
                if Seli >= len(FIDInt[i]):Seli = 0
                for j in range(0,len(FIDInt[i])):
                    if j <> Seli:
                        SelFID.append(FIDInt[i][j])
                        RefFID.append(FIDInt[i][Seli])
                arcpy.AddWarning("     - FIDs: " + str(FIDInt[i]) + ", Med Type: " + str(MTList[i]) + ", Med Width: " + str(MWList[i]) + ", Sel: " + str({FIDInt[i][Seli]:MWList[i][Seli]}))
            else:
                for j in range(1,len(FIDInt[i])):
                    SelFID.append(FIDInt[i][j])
                    RefFID.append(FIDInt[i][0])
    arcpy.AddMessage("     - # of FIDs to remove: " + str(len(SelFID)))

    arcpy.AddMessage("    Delete Duplicates: Site Layer")
    UC = arcpy.UpdateCursor(DataLayer)
    for URow in UC:
        SFID = URow.getValue(F_TargetFID['name'])
        URow.setValue(F_SimSites['name'],RefFID.count(SFID))
        if SFID in SelFID:
            URow.setValue(F_RefFID['name'],RefFID[SelFID.index(SFID)])
        else:
            URow.setValue(F_RefFID['name'],SFID)
        UC.updateRow(URow)

    temp = arcpy.CopyFeatures_management(DataLayer, Output)

    UC = arcpy.UpdateCursor(temp)
    for URow in UC:
        SFID = URow.getValue(F_TargetFID['name'])
        RFID = URow.getValue(F_RefFID['name'])
        if SFID <> RFID:
            UC.deleteRow(URow)

    for Field in [F_TargetFID, F_JoinFID, F_RefFID]:
        arcpy.DeleteField_management(temp,Field['name'])

    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")
def CheckDriveway(DataInput,DWField,DBuffer,Output):
    arcpy.AddMessage(" ")
    arcpy.AddMessage("    Driveway Check For Duplicates")

    OutDic = OutputParser(Output, 'shp')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("    Copy Point Layer")
    DataLayer = CopyFeatures(DataInput,'PDInput')
    TotalSites = arcpy.GetCount_management(DataLayer)
    arcpy.AddMessage("     - Total number of Points Found: " + str(TotalSites))

    arcpy.AddMessage("    Saving Target FID: Point Layer")
    FieldList1 = [F_TargetFID]
    FieldList2 = [F_JoinFID, F_RefFID, F_SimSites]

    for Field in FieldList1:
        AddField(DataLayer,Field)

    UC = arcpy.UpdateCursor(DataLayer)
    for URow in UC:
        FID = GetFID(URow)
        URow.setValue(F_TargetFID['name'],FID)
        UC.updateRow(URow)
    FIDIntersect = {SRow.getValue(F_TargetFID['name']):[] for SRow in arcpy.SearchCursor(DataLayer)}

    arcpy.AddMessage("    Buffer: DataLayer")
    SBuffer = Buffer(DataLayer, "PDBuffer",{'distance': DBuffer, 'line_side': 'FULL', 'line_end_type': 'FLAT', 'dissolve_option': 'NONE', 'dissolve_field': '#'})

    arcpy.AddMessage("    Saving Join FID: Point Layer")
    for Field in FieldList2:
        AddField(DataLayer,Field)

    UC = arcpy.UpdateCursor(DataLayer)
    for URow in UC:
        FID = GetFID(URow)
        URow.setValue(F_JoinFID['name'],FID)
        UC.updateRow(URow)

    arcpy.AddMessage("    Intersect: Buffer + Point Layer")
    BI = Intersect(SBuffer + ';' + DataLayer,"PDIntersect",{'join_attributes': "ALL", 'cluster_tolerance': '', 'output_type': "POINT"})

    arcpy.AddMessage("    Finding Duplicates")
    for SRow in arcpy.SearchCursor(BI):
        FIDIntersect[SRow.getValue(F_TargetFID['name'])].append(SRow.getValue(F_JoinFID['name']))
    FIDInt = FIDIntersect.values()

    FIDInt.sort()
    for i in FIDInt:
        i.sort()

    def PopDuplicate(List):
	    Flag = False
	    i = -1
	    while not Flag and i < len(List) - 2:
		    i += 1
		    if List[i] == List[i + 1] and not Flag:
			    Flag = True
			    List.pop(i)
	    return {'List': List, 'Status': Flag}

    InitLen = len(FIDInt)
    T = PopDuplicate(FIDInt)
    while T['Status']:
        T = PopDuplicate(FIDInt)
    FinalLen = len(FIDInt)
    arcpy.AddMessage("     - " + str(InitLen) + " to " + str(FinalLen) + ", " + str(InitLen - FinalLen) + " Duplicates Found")

    DWList = []
    for FIDL in FIDInt:
        T = []
        for FID in FIDL:
            T.append(0)
        DWList.append(T)

    SC = arcpy.SearchCursor(DataLayer)
    for SRow in SC:
        SFID = SRow.getValue(F_TargetFID['name'])
        DWType = SRow.getValue(DWField)
        i = 0
        for FIDL in FIDInt:
            try:
                j = FIDL.index(SFID)
                break
            except:
                j = -1
            i += 1
        if j <> -1:
            DWList[i][j] = DWType
        else:
            arcpy.AddError("Driveways without geospatial coordinations")

    SelFID = []
    RefFID = []
    for i in range(0,len(FIDInt)):
        if len(FIDInt[i]) > 1:
            if DWList[i].count(DWList[i][0]) <> len(DWList[i]):
                Seli = 0
                MinDW = 7
                for dw in DWList[i]:
                    if dw < MinDW and dw <> 0:
                        MinDW = dw
                        Seli = DWList[i].index(dw)
                if Seli >= len(FIDInt[i]):Seli = 0
                for j in range(0,len(FIDInt[i])):
                    if j <> Seli:
                        SelFID.append(FIDInt[i][j])
                        RefFID.append(FIDInt[i][Seli])
                arcpy.AddWarning("     - FIDs: " + str(FIDInt[i]) + ", DwType: " + str(DWList[i]) + ", Sel: " + str({FIDInt[i][Seli]:DWList[i][Seli]}))
            else:
                for j in range(1,len(FIDInt[i])):
                    SelFID.append(FIDInt[i][j])
                    RefFID.append(FIDInt[i][0])
    arcpy.AddMessage("     - # of FIDs to remove: " + str(len(SelFID)))

    arcpy.AddMessage("    Delete Duplicates: Site Layer")
    UC = arcpy.UpdateCursor(DataLayer)
    for URow in UC:
        SFID = URow.getValue(F_TargetFID['name'])
        URow.setValue(F_SimSites['name'],RefFID.count(SFID))
        if SFID in SelFID:
            URow.setValue(F_RefFID['name'],RefFID[SelFID.index(SFID)])
        else:
            URow.setValue(F_RefFID['name'],SFID)
        UC.updateRow(URow)

    temp = arcpy.CopyFeatures_management(DataLayer, Output)

    UC = arcpy.UpdateCursor(temp)
    for URow in UC:
        SFID = URow.getValue(F_TargetFID['name'])
        RFID = URow.getValue(F_RefFID['name'])
        if SFID <> RFID:
            UC.deleteRow(URow)

    for Field in [F_TargetFID, F_JoinFID, F_RefFID]:
        arcpy.DeleteField_management(temp,Field['name'])

    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")
def CheckRHR(DataInput,RHRField,DBuffer,Output):
    arcpy.AddMessage(" ")
    arcpy.AddMessage("    RHR Check For Duplicates")

    OutDic = OutputParser(Output, 'shp')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("    Copy Point Layer")
    DataLayer = CopyFeatures(DataInput,'PDInput')
    TotalSites = arcpy.GetCount_management(DataLayer)
    arcpy.AddMessage("     - Total number of Points Found: " + str(TotalSites))

    arcpy.AddMessage("    Saving Target FID: Point Layer")
    FieldList1 = [F_TargetFID]
    FieldList2 = [F_JoinFID, F_RefFID, F_SimSites]

    for Field in FieldList1:
        AddField(DataLayer,Field)

    UC = arcpy.UpdateCursor(DataLayer)
    for URow in UC:
        FID = GetFID(URow)
        URow.setValue(F_TargetFID['name'],FID)
        UC.updateRow(URow)
    FIDIntersect = {SRow.getValue(F_TargetFID['name']):[] for SRow in arcpy.SearchCursor(DataLayer)}

    arcpy.AddMessage("    Buffer: DataLayer")
    SBuffer = Buffer(DataLayer, "PDBuffer",{'distance': DBuffer, 'line_side': 'FULL', 'line_end_type': 'FLAT', 'dissolve_option': 'NONE', 'dissolve_field': '#'})

    arcpy.AddMessage("    Saving Join FID: Point Layer")
    for Field in FieldList2:
        AddField(DataLayer,Field)

    UC = arcpy.UpdateCursor(DataLayer)
    for URow in UC:
        FID = GetFID(URow)
        URow.setValue(F_JoinFID['name'],FID)
        UC.updateRow(URow)

    arcpy.AddMessage("    Intersect: Buffer + Point Layer")
    BI = Intersect(SBuffer + ';' + DataLayer,"PDIntersect",{'join_attributes': "ALL", 'cluster_tolerance': '', 'output_type': "POINT"})

    arcpy.AddMessage("    Finding Duplicates")
    for SRow in arcpy.SearchCursor(BI):
        FIDIntersect[SRow.getValue(F_TargetFID['name'])].append(SRow.getValue(F_JoinFID['name']))
    FIDInt = FIDIntersect.values()

    FIDInt.sort()
    for i in FIDInt:
        i.sort()

    def PopDuplicate(List):
	    Flag = False
	    i = -1
	    while not Flag and i < len(List) - 2:
		    i += 1
		    if List[i] == List[i + 1] and not Flag:
			    Flag = True
			    List.pop(i)
	    return {'List': List, 'Status': Flag}

    InitLen = len(FIDInt)
    T = PopDuplicate(FIDInt)
    while T['Status']:
        T = PopDuplicate(FIDInt)
    FinalLen = len(FIDInt)
    arcpy.AddMessage("     - " + str(InitLen) + " to " + str(FinalLen) + ", " + str(InitLen - FinalLen) + " Duplicates Found")

    DWList = []
    for FIDL in FIDInt:
        T = []
        for FID in FIDL:
            T.append(0)
        DWList.append(T)

    SC = arcpy.SearchCursor(DataLayer)
    for SRow in SC:
        SFID = SRow.getValue(F_TargetFID['name'])
        DWType = SRow.getValue(RHRField)
        i = 0
        for FIDL in FIDInt:
            try:
                j = FIDL.index(SFID)
                break
            except:
                j = -1
            i += 1
        if j <> -1:
            DWList[i][j] = DWType
        else:
            arcpy.AddError("RHR without geospatial coordinations")

    SelFID = []
    RefFID = []
    for i in range(0,len(FIDInt)):
        if len(FIDInt[i]) > 1:
            if DWList[i].count(DWList[i][0]) <> len(DWList[i]):
                Seli = 0
                MaxDW = 1
                for dw in DWList[i]:
                    if dw > MaxDW and dw <> 0:
                        MaxDW = dw
                        Seli = DWList[i].index(dw)
                if Seli >= len(FIDInt[i]):Seli = 0
                for j in range(0,len(FIDInt[i])):
                    if j <> Seli:
                        SelFID.append(FIDInt[i][j])
                        RefFID.append(FIDInt[i][Seli])
                arcpy.AddWarning("     - FIDs: " + str(FIDInt[i]) + ", RHR Value: " + str(DWList[i]) + ", Sel: " + str({FIDInt[i][Seli]:DWList[i][Seli]}))
            else:
                for j in range(1,len(FIDInt[i])):
                    SelFID.append(FIDInt[i][j])
                    RefFID.append(FIDInt[i][0])
    arcpy.AddMessage("     - # of FIDs to remove: " + str(len(SelFID)))

    arcpy.AddMessage("    Delete Duplicates: Site Layer")
    UC = arcpy.UpdateCursor(DataLayer)
    for URow in UC:
        SFID = URow.getValue(F_TargetFID['name'])
        URow.setValue(F_SimSites['name'],RefFID.count(SFID))
        if SFID in SelFID:
            URow.setValue(F_RefFID['name'],RefFID[SelFID.index(SFID)])
        else:
            URow.setValue(F_RefFID['name'],SFID)
        UC.updateRow(URow)

    temp = arcpy.CopyFeatures_management(DataLayer, Output)

    UC = arcpy.UpdateCursor(temp)
    for URow in UC:
        SFID = URow.getValue(F_TargetFID['name'])
        RFID = URow.getValue(F_RefFID['name'])
        if SFID <> RFID:
            UC.deleteRow(URow)

    for Field in [F_TargetFID, F_JoinFID, F_RefFID]:
        arcpy.DeleteField_management(temp,Field['name'])

    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")
def CheckShoulderWidth(DataInput,ShWField,DBuffer,Output):
    arcpy.AddMessage(" ")
    arcpy.AddMessage("    Shoulder Width Check For Duplicates")

    OutDic = OutputParser(Output, 'shp')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("    Copy Point Layer")
    DataLayer = CopyFeatures(DataInput,'PDInput')
    TotalSites = arcpy.GetCount_management(DataLayer)
    arcpy.AddMessage("     - Total number of Points Found: " + str(TotalSites))

    arcpy.AddMessage("    Saving Target FID: Point Layer")
    FieldList1 = [F_TargetFID]
    FieldList2 = [F_JoinFID, F_RefFID, F_SimSites]

    for Field in FieldList1:
        AddField(DataLayer,Field)

    UC = arcpy.UpdateCursor(DataLayer)
    for URow in UC:
        FID = GetFID(URow)
        URow.setValue(F_TargetFID['name'],FID)
        UC.updateRow(URow)
    FIDIntersect = {SRow.getValue(F_TargetFID['name']):[] for SRow in arcpy.SearchCursor(DataLayer)}

    arcpy.AddMessage("    Buffer: DataLayer")
    SBuffer = Buffer(DataLayer, "PDBuffer",{'distance': DBuffer, 'line_side': 'FULL', 'line_end_type': 'FLAT', 'dissolve_option': 'NONE', 'dissolve_field': '#'})

    arcpy.AddMessage("    Saving Join FID: Point Layer")
    for Field in FieldList2:
        AddField(DataLayer,Field)

    UC = arcpy.UpdateCursor(DataLayer)
    for URow in UC:
        FID = GetFID(URow)
        URow.setValue(F_JoinFID['name'],FID)
        UC.updateRow(URow)

    arcpy.AddMessage("    Intersect: Buffer + Point Layer")
    BI = Intersect(SBuffer + ';' + DataLayer,"PDIntersect",{'join_attributes': "ALL", 'cluster_tolerance': '', 'output_type': "POINT"})

    arcpy.AddMessage("    Finding Duplicates")
    for SRow in arcpy.SearchCursor(BI):
        FIDIntersect[SRow.getValue(F_TargetFID['name'])].append(SRow.getValue(F_JoinFID['name']))
    FIDInt = FIDIntersect.values()

    FIDInt.sort()
    for i in FIDInt:
        i.sort()

    def PopDuplicate(List):
	    Flag = False
	    i = -1
	    while not Flag and i < len(List) - 2:
		    i += 1
		    if List[i] == List[i + 1] and not Flag:
			    Flag = True
			    List.pop(i)
	    return {'List': List, 'Status': Flag}

    InitLen = len(FIDInt)
    T = PopDuplicate(FIDInt)
    while T['Status']:
        T = PopDuplicate(FIDInt)
    FinalLen = len(FIDInt)
    arcpy.AddMessage("     - " + str(InitLen) + " to " + str(FinalLen) + ", " + str(InitLen - FinalLen) + " Duplicates Found")

    DWList = []
    for FIDL in FIDInt:
        T = []
        for FID in FIDL:
            T.append(0)
        DWList.append(T)

    SC = arcpy.SearchCursor(DataLayer)
    for SRow in SC:
        SFID = SRow.getValue(F_TargetFID['name'])
        DWType = SRow.getValue(ShWField)
        i = 0
        for FIDL in FIDInt:
            try:
                j = FIDL.index(SFID)
                break
            except:
                j = -1
            i += 1
        if j <> -1:
            DWList[i][j] = DWType
        else:
            arcpy.AddError("Data without geospatial coordinations")

    SelFID = []
    RefFID = []
    for i in range(0,len(FIDInt)):
        if len(FIDInt[i]) > 1:
            if DWList[i].count(DWList[i][0]) <> len(DWList[i]):
                Seli = 0
                MaxDW = 1
                for dw in DWList[i]:
                    if dw > MaxDW and dw <> 0:
                        MaxDW = dw
                        Seli = DWList[i].index(dw)
                if Seli >= len(FIDInt[i]):Seli = 0
                for j in range(0,len(FIDInt[i])):
                    if j <> Seli:
                        SelFID.append(FIDInt[i][j])
                        RefFID.append(FIDInt[i][Seli])
                arcpy.AddWarning("     - FIDs: " + str(FIDInt[i]) + ", ShW Value: " + str(DWList[i]) + ", Sel: " + str({FIDInt[i][Seli]:DWList[i][Seli]}))
            else:
                for j in range(1,len(FIDInt[i])):
                    SelFID.append(FIDInt[i][j])
                    RefFID.append(FIDInt[i][0])
    arcpy.AddMessage("     - # of FIDs to remove: " + str(len(SelFID)))

    arcpy.AddMessage("    Delete Duplicates: Site Layer")
    UC = arcpy.UpdateCursor(DataLayer)
    for URow in UC:
        SFID = URow.getValue(F_TargetFID['name'])
        URow.setValue(F_SimSites['name'],RefFID.count(SFID))
        if SFID in SelFID:
            URow.setValue(F_RefFID['name'],RefFID[SelFID.index(SFID)])
        else:
            URow.setValue(F_RefFID['name'],SFID)
        UC.updateRow(URow)

    temp = arcpy.CopyFeatures_management(DataLayer, Output)

    UC = arcpy.UpdateCursor(temp)
    for URow in UC:
        SFID = URow.getValue(F_TargetFID['name'])
        RFID = URow.getValue(F_RefFID['name'])
        if SFID <> RFID:
            UC.deleteRow(URow)

    for Field in [F_TargetFID, F_JoinFID, F_RefFID]:
        arcpy.DeleteField_management(temp,Field['name'])

    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")
def CheckLaneWidth(DataInput,LnWField,DBuffer,Output):
    arcpy.AddMessage(" ")
    arcpy.AddMessage("    Lane Width Check For Duplicates")

    OutDic = OutputParser(Output, 'shp')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("    Copy Point Layer")
    DataLayer = CopyFeatures(DataInput,'PDInput')
    TotalSites = arcpy.GetCount_management(DataLayer)
    arcpy.AddMessage("     - Total number of Points Found: " + str(TotalSites))

    arcpy.AddMessage("    Saving Target FID: Point Layer")
    FieldList1 = [F_TargetFID]
    FieldList2 = [F_JoinFID, F_RefFID, F_SimSites]

    for Field in FieldList1:
        AddField(DataLayer,Field)

    UC = arcpy.UpdateCursor(DataLayer)
    for URow in UC:
        FID = GetFID(URow)
        URow.setValue(F_TargetFID['name'],FID)
        UC.updateRow(URow)
    FIDIntersect = {SRow.getValue(F_TargetFID['name']):[] for SRow in arcpy.SearchCursor(DataLayer)}

    arcpy.AddMessage("    Buffer: DataLayer")
    SBuffer = Buffer(DataLayer, "PDBuffer",{'distance': DBuffer, 'line_side': 'FULL', 'line_end_type': 'FLAT', 'dissolve_option': 'NONE', 'dissolve_field': '#'})

    arcpy.AddMessage("    Saving Join FID: Point Layer")
    for Field in FieldList2:
        AddField(DataLayer,Field)

    UC = arcpy.UpdateCursor(DataLayer)
    for URow in UC:
        FID = GetFID(URow)
        URow.setValue(F_JoinFID['name'],FID)
        UC.updateRow(URow)

    arcpy.AddMessage("    Intersect: Buffer + Point Layer")
    BI = Intersect(SBuffer + ';' + DataLayer,"PDIntersect",{'join_attributes': "ALL", 'cluster_tolerance': '', 'output_type': "POINT"})

    arcpy.AddMessage("    Finding Duplicates")
    for SRow in arcpy.SearchCursor(BI):
        FIDIntersect[SRow.getValue(F_TargetFID['name'])].append(SRow.getValue(F_JoinFID['name']))
    FIDInt = FIDIntersect.values()

    FIDInt.sort()
    for i in FIDInt:
        i.sort()

    def PopDuplicate(List):
	    Flag = False
	    i = -1
	    while not Flag and i < len(List) - 2:
		    i += 1
		    if List[i] == List[i + 1] and not Flag:
			    Flag = True
			    List.pop(i)
	    return {'List': List, 'Status': Flag}

    InitLen = len(FIDInt)
    T = PopDuplicate(FIDInt)
    while T['Status']:
        T = PopDuplicate(FIDInt)
    FinalLen = len(FIDInt)
    arcpy.AddMessage("     - " + str(InitLen) + " to " + str(FinalLen) + ", " + str(InitLen - FinalLen) + " Duplicates Found")

    DWList = []
    for FIDL in FIDInt:
        T = []
        for FID in FIDL:
            T.append(0)
        DWList.append(T)

    SC = arcpy.SearchCursor(DataLayer)
    for SRow in SC:
        SFID = SRow.getValue(F_TargetFID['name'])
        DWType = SRow.getValue(LnWField)
        i = 0
        for FIDL in FIDInt:
            try:
                j = FIDL.index(SFID)
                break
            except:
                j = -1
            i += 1
        if j <> -1:
            DWList[i][j] = DWType
        else:
            arcpy.AddError("Data without geospatial coordinations")

    SelFID = []
    RefFID = []
    for i in range(0,len(FIDInt)):
        if len(FIDInt[i]) > 1:
            if DWList[i].count(DWList[i][0]) <> len(DWList[i]):
                Seli = 0
                MaxDW = 1
                for dw in DWList[i]:
                    if dw > MaxDW and dw <> 0:
                        MaxDW = dw
                        Seli = DWList[i].index(dw)
                if Seli >= len(FIDInt[i]):Seli = 0
                for j in range(0,len(FIDInt[i])):
                    if j <> Seli:
                        SelFID.append(FIDInt[i][j])
                        RefFID.append(FIDInt[i][Seli])
                arcpy.AddWarning("     - FIDs: " + str(FIDInt[i]) + ", ShW Value: " + str(DWList[i]) + ", Sel: " + str({FIDInt[i][Seli]:DWList[i][Seli]}))
            else:
                for j in range(1,len(FIDInt[i])):
                    SelFID.append(FIDInt[i][j])
                    RefFID.append(FIDInt[i][0])
    arcpy.AddMessage("     - # of FIDs to remove: " + str(len(SelFID)))

    arcpy.AddMessage("    Delete Duplicates: Site Layer")
    UC = arcpy.UpdateCursor(DataLayer)
    for URow in UC:
        SFID = URow.getValue(F_TargetFID['name'])
        URow.setValue(F_SimSites['name'],RefFID.count(SFID))
        if SFID in SelFID:
            URow.setValue(F_RefFID['name'],RefFID[SelFID.index(SFID)])
        else:
            URow.setValue(F_RefFID['name'],SFID)
        UC.updateRow(URow)

    temp = arcpy.CopyFeatures_management(DataLayer, Output)

    UC = arcpy.UpdateCursor(temp)
    for URow in UC:
        SFID = URow.getValue(F_TargetFID['name'])
        RFID = URow.getValue(F_RefFID['name'])
        if SFID <> RFID:
            UC.deleteRow(URow)

    for Field in [F_TargetFID, F_JoinFID, F_RefFID]:
        arcpy.DeleteField_management(temp,Field['name'])

    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")

## Import Data Elements
def ImportGrade(SiteInput,MeanZField,Output):
    import json

    arcpy.AddMessage(" ")
    arcpy.AddMessage("    Import Grade")

    OutDic = OutputParser(Output, 'shp')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("    Copy Features: Roads Layer")
    SiteLayer = CopyFeatures(SiteInput,'CURVEInput')
    JoinLayer = CopyFeatures(SiteLayer,'CURVEJoin')
    TotalSites = arcpy.GetCount_management(SiteLayer)
    arcpy.AddMessage("     - Total number of Items Found: " + str(TotalSites))
    
    arcpy.AddMessage("    Add Fields: Roads Layer")
    FieldList1 = [F_TargetFID,F_Grade]
    for field in FieldList1:
        AddField(SiteLayer,field)

    FieldList2 = [F_JoinFID]
    for field in FieldList2:
        AddField(JoinLayer,field)

    arcpy.AddMessage("    Calculate Fields: Roads Layer")
    i = 0
    UC = arcpy.UpdateCursor(SiteLayer)
    for URow in UC:
        URow.setValue(F_TargetFID['name'],i)
        i += 1
        UC.updateRow(URow)

    i = 0
    UC = arcpy.UpdateCursor(JoinLayer)
    for URow in UC:
        URow.setValue(F_JoinFID['name'],i)
        i += 1
        UC.updateRow(URow)

    arcpy.AddMessage("    Spatial Join: Sites Layer")
    USPJ = SpatialJoin(SiteLayer, JoinLayer, 'CurveSPJ', {'join_operation': "JOIN_ONE_TO_MANY", 'join_type': "KEEP_ALL", 'field_mapping': '', 'match_option': 'INTERSECT', 'search_radius': '', 'distance_field_name': ''})


    arcpy.AddMessage("    Search Cursor: Roads Layer")
    ConnDic  = {SRow.getValue(F_TargetFID['name']):[] for SRow in arcpy.SearchCursor(USPJ)}
    SC = arcpy.SearchCursor(USPJ)
    for SRow in SC:
        TFID = SRow.getValue(F_TargetFID['name'])
        JFID = SRow.getValue(F_JoinFID  ['name'])
        if (not JFID in ConnDic[TFID]) and (JFID<>TFID):
           ConnDic[TFID].append(JFID)

    PointDic = {SRow.getValue(F_TargetFID['name']):{'FirstPoint':SRow.getValue('Shape').firstPoint,'LastPoint':SRow.getValue('Shape').lastPoint                        } for SRow in arcpy.SearchCursor(SiteLayer)}
    FinalDic = {SRow.getValue(F_TargetFID['name']):{'Length'    :SRow.getValue('Shape').length    ,'MeanZ'    :SRow.getValue(MeanZField),'Path': json.loads(SRow.getValue('Shape').JSON)['paths'][0],'FirstPoint':[],'LastPoint':[]} for SRow in arcpy.SearchCursor(SiteLayer)}


    for TFID in FinalDic.keys():
        for JFID in ConnDic[TFID]:
            if PointDic[TFID]['FirstPoint'].equals(PointDic[JFID]['FirstPoint']) or PointDic[TFID]['FirstPoint'].equals(PointDic[JFID]['LastPoint']):
                FinalDic[TFID]['FirstPoint'].append([FinalDic[JFID]['Length'],FinalDic[JFID]['MeanZ']])
            if PointDic[TFID]['LastPoint'].equals(PointDic[JFID]['FirstPoint']) or PointDic[TFID]['LastPoint'].equals(PointDic[JFID]['LastPoint']):
                FinalDic[TFID]['LastPoint'].append([FinalDic[JFID]['Length'],FinalDic[JFID]['MeanZ']])

    arcpy.AddMessage("    Update Cursor: Roads Layer")
    UC = arcpy.UpdateCursor(SiteLayer)
    for URow in UC:
        TFID = URow.getValue(F_TargetFID['name'])        
        G = VerCurvature(FinalDic[TFID])
        URow.setValue(F_Grade ['name'],G)
        
        UC.updateRow(URow)
    arcpy.DeleteField_management(SiteLayer,F_TargetFID['name'])

    arcpy.CopyFeatures_management(SiteLayer, Output)
    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")
def ImportCurvature(SiteInput,Output):
    import json

    arcpy.AddMessage(" ")
    arcpy.AddMessage("    Import Curvature")

    OutDic = OutputParser(Output, 'shp')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("    Copy Features: Roads Layer")
    SiteLayer = CopyFeatures(SiteInput,'CURVEInput')
    JoinLayer = CopyFeatures(SiteLayer,'CURVEJoin')
    TotalSites = arcpy.GetCount_management(SiteLayer)
    arcpy.AddMessage("     - Total number of Items Found: " + str(TotalSites))
    
    arcpy.AddMessage("    Add Fields: Roads Layer")
    FieldList1 = [F_TargetFID,F_HorCur,F_CMFHorCur, F_CMFHCMVFI, F_CMFHCMVPD, F_CMFHCSVFI, F_CMFHCSVPD]
    for field in FieldList1:
        AddField(SiteLayer,field)

    FieldList2 = [F_JoinFID]
    for field in FieldList2:
        AddField(JoinLayer,field)

    arcpy.AddMessage("    Calculate Fields: Roads Layer")
    i = 0
    UC = arcpy.UpdateCursor(SiteLayer)
    for URow in UC:
        URow.setValue(F_TargetFID['name'],i)
        i += 1
        UC.updateRow(URow)

    i = 0
    UC = arcpy.UpdateCursor(JoinLayer)
    for URow in UC:
        URow.setValue(F_JoinFID['name'],i)
        i += 1
        UC.updateRow(URow)

    arcpy.AddMessage("    Spatial Join: Sites Layer")
    USPJ = SpatialJoin(SiteLayer, JoinLayer, 'CurveSPJ', {'join_operation': "JOIN_ONE_TO_MANY", 'join_type': "KEEP_ALL", 'field_mapping': '', 'match_option': 'INTERSECT', 'search_radius': '', 'distance_field_name': ''})


    arcpy.AddMessage("    Search Cursor: Roads Layer")
    ConnDic  = {SRow.getValue(F_TargetFID['name']):[] for SRow in arcpy.SearchCursor(USPJ)}
    SC = arcpy.SearchCursor(USPJ)
    for SRow in SC:
        TFID = SRow.getValue(F_TargetFID['name'])
        JFID = SRow.getValue(F_JoinFID  ['name'])
        if (not JFID in ConnDic[TFID]) and (JFID<>TFID):
           ConnDic[TFID].append(JFID)

    PointDic = {SRow.getValue(F_TargetFID['name']):{'FirstPoint':SRow.getValue('Shape').firstPoint,'LastPoint':SRow.getValue('Shape').lastPoint                        } for SRow in arcpy.SearchCursor(SiteLayer)}
    FinalDic = {SRow.getValue(F_TargetFID['name']):{'Length'    :SRow.getValue('Shape').length    ,'Path': json.loads(SRow.getValue('Shape').JSON)['paths'][0],'FirstPoint':[],'LastPoint':[]} for SRow in arcpy.SearchCursor(SiteLayer)}


    for TFID in FinalDic.keys():
        for JFID in ConnDic[TFID]:
            if PointDic[TFID]['FirstPoint'].equals(PointDic[JFID]['FirstPoint']) or PointDic[TFID]['FirstPoint'].equals(PointDic[JFID]['LastPoint']):
                FinalDic[TFID]['FirstPoint'].append([FinalDic[JFID]['Length'],1])
            if PointDic[TFID]['LastPoint'].equals(PointDic[JFID]['FirstPoint']) or PointDic[TFID]['LastPoint'].equals(PointDic[JFID]['LastPoint']):
                FinalDic[TFID]['LastPoint'].append([FinalDic[JFID]['Length'],1])

    arcpy.AddMessage("    Update Cursor: Roads Layer")
    UC = arcpy.UpdateCursor(SiteLayer)
    for URow in UC:
        TFID = URow.getValue(F_TargetFID['name'])        
        R = HorCurvature(FinalDic[TFID])
        URow.setValue(F_HorCur['name'],1/(float(sum(R)/max(len(R),1)))*5280)
        CMF = CMFHorCurve(URow.getValue(F_FType['name']),URow.getValue('Shape').length,1/(float(sum(R)/max(len(R),1)))*5280,0)
        URow.setValue(F_CMFHorCur['name'],CMF['TOT'])
        URow.setValue(F_CMFHCMVFI['name'],CMF['MVFI'])
        URow.setValue(F_CMFHCMVPD['name'],CMF['MVPDO'])
        URow.setValue(F_CMFHCSVFI['name'],CMF['SVFI'])
        URow.setValue(F_CMFHCSVPD['name'],CMF['SVPDO'])

        UC.updateRow(URow)
    arcpy.DeleteField_management(SiteLayer,F_TargetFID['name'])

    arcpy.CopyFeatures_management(SiteLayer, Output)
    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")
def ImportDriveway(SiteInput,CMFInput,DWField,DBuffer,Output):
    arcpy.AddMessage(" ")
    arcpy.AddMessage("    Import Driveway")

    OutDic = OutputParser(Output, 'shp')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("    Copy Features: Sites Layer")
    SiteLayer = CopyFeatures(SiteInput,'DWSite')
    TotalSites = arcpy.GetCount_management(SiteLayer)
    arcpy.AddMessage("     - Total number of Sites Found: " + str(TotalSites))

    arcpy.AddMessage("    Copy Features: Driveway Layer")
    CMFLayer = CopyFeatures(CMFInput,'DWCMF')
    TotalCMF = arcpy.GetCount_management(CMFLayer)
    arcpy.AddMessage("     - Total number of Driveway Items Found: " + str(TotalCMF))

    arcpy.AddMessage("    Add Fields: Sites Layer")
    FieldList1 = [F_RouteFID, F_dMjC   , F_dMnC, F_dMjI, F_dMnI, F_dMjR, F_dMnR, F_dO, F_DrwDens, F_CMFDrwDens]
    for Field in FieldList1:
        AddField(SiteLayer,Field)
    # Save FIDs in RouteFID
    UC = arcpy.UpdateCursor(SiteLayer)
    for URow in UC:
        FID = GetFID(URow)
        URow.setValue(F_RouteFID['name'],FID)
        UC.updateRow(URow)
    # Creating a dictionary with keys = Sites FIDs
    FIDIntersect = {SRow.getValue(F_RouteFID['name']):[] for SRow in arcpy.SearchCursor(SiteLayer)}

    arcpy.AddMessage("    Add Fields: Driveway Layer")
    FieldList2 = [F_RouteFID, F_JoinFID]
    for Field in FieldList2:
        AddField(CMFLayer,Field)
    # Save Driveway FIDs in JoinFID
    UC = arcpy.UpdateCursor(CMFLayer)
    for URow in UC:
        FID = GetFID(URow)
        URow.setValue(F_JoinFID['name'],FID)
        UC.updateRow(URow)

    arcpy.AddMessage("    Buffer: Sites Layer")
    SBuffer = Buffer(SiteLayer,"DWBuffer",{'distance': DBuffer, 'line_side': 'FULL', 'line_end_type': 'FLAT', 'dissolve_option': 'NONE', 'dissolve_field': '#'})

    arcpy.AddMessage("    Intersect: Buffer + Driveway Layer")
    BI = Intersect(SBuffer + ';' + CMFLayer, "DWIntersect", {'join_attributes': "ALL", 'cluster_tolerance': '', 'output_type': "POINT"})
    # Save Intersecting driveways for each Site
    for SRow in arcpy.SearchCursor(BI):
        FIDIntersect[SRow.getValue(F_RouteFID['name'])].append(SRow.getValue(F_JoinFID['name']))

    arcpy.AddMessage("    Update Cursor: Site Layer & Driveway Layer")
    # Updates Sites layer for number of driveways for each type; and updates
    # driveways layer with corresponding site layer
    SitesWithData = 0
    UC1 = arcpy.UpdateCursor(SiteLayer)
    for URow1 in UC1:
        SFID = URow1.getValue(F_RouteFID['name'])
        T = {'dMjC': 0, 'dMnC': 0, 'dMjI': 0, 'dMnI': 0, 'dMjR': 0, 'dMnR': 0, 'dO': 0}
        Flag = True
        for CMFFID in FIDIntersect[SFID]:
            UC2 = arcpy.UpdateCursor(CMFLayer,'"' + F_JoinFID['name'] + '" = ' + str(CMFFID))
            URow2 = UC2.next()                
            URow2.setValue(F_RouteFID['name'], SFID)
            try:
                DW = int(URow2.getValue(DWField))
            except:
                arcpy.AddWarning("    Could not change " + DWField + ' = ' + str(URow2.getValue(DWField)) + ' to integer; Default value assumed: 7')
                DW = 7

            if   DW == 1:
                T['dMjC'] += 1
            elif DW == 2:
                T['dMnC'] += 1
            elif DW == 3:
                T['dMjI'] += 1
            elif DW == 4:
                T['dMnI'] += 1
            elif DW == 5:
                T['dMjR'] += 1
            elif DW == 6:
                T['dMnR'] += 1
            else:
                T['dO']   += 1
            if Flag:
                SitesWithData += 1
                Flag = False
            UC2.updateRow(URow2)
            del UC2
        Length = URow1.getValue('Shape').length/5280
        URow1.setValue(F_dMjC['name'],T['dMjC'])
        URow1.setValue(F_dMnC['name'],T['dMnC'])
        URow1.setValue(F_dMjI['name'],T['dMjI'])
        URow1.setValue(F_dMnI['name'],T['dMnI'])
        URow1.setValue(F_dMjR['name'],T['dMjR'])
        URow1.setValue(F_dMnR['name'],T['dMnR'])
        URow1.setValue(F_dO['name'],T['dO'])
        URow1.setValue(F_DrwDens['name'],sum(T.values())/Length)
        URow1.setValue(F_CMFDrwDens['name'],CMFDrivewayDensity(URow1.getValue(F_FType['name']),sum(T.values())/Length,URow1.getValue(F_AADT['name'])))
        
        UC1.updateRow(URow1)
        if not Flag:
            arcpy.AddMessage('     - FID: ' + str(SFID) + ', Tot Driveways: ' + str(sum(T.values())))
    arcpy.AddMessage("    Total Sites with Data: " + str(SitesWithData))

    for Field in [F_RouteFID]:
        arcpy.DeleteField_management(SiteLayer,Field['name'])

    for Field in [F_JoinFID]:
        arcpy.DeleteField_management(CMFLayer,Field['name'])

    arcpy.CopyFeatures_management(SiteLayer, Output)
    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")
def ImportFixedObjects(SiteInput, CMFDataInput, DCField, FOField, OffsetField, Output):
    arcpy.AddMessage(" ")
    arcpy.AddMessage("    Import Fixed Objects")

    OutDic = OutputParser(Output, 'shp')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("    Copy Features: Sites Layer")
    SiteLayer = CopyFeatures(SiteInput,'SiteInput')
    TotalSites = arcpy.GetCount_management(SiteLayer)
    arcpy.AddMessage("     - Total number of Sites Found: " + str(TotalSites))

    arcpy.AddMessage("    Copy Features: Fixed Object Data Layer")
    CMFDataLayer = CopyFeatures(CMFDataInput,'FOInput')
    TotalCMF = arcpy.GetCount_management(CMFDataLayer)
    arcpy.AddMessage("     - Total number of Fixed Objects Found: " + str(TotalCMF))

    arcpy.AddMessage("    Add Fields: Sites Layer")
    FieldList1 = [F_RouteFID, F_CMFFO, F_FODensity, F_FOOffset]
    for Field in FieldList1:
        AddField(SiteLayer,Field,'append')
    UC = arcpy.UpdateCursor(SiteLayer)
    for URow in UC:
        FID = GetFID(URow)
        URow.setValue(F_RouteFID['name'],FID)
        UC.updateRow(URow)

    arcpy.AddMessage("    Add Fields: Fixed Objects Layer")
    FieldList2 = [F_RouteFID, F_SegLength, F_CMFFID, F_CMFLength]
    for Field in FieldList2:
        AddField(CMFDataLayer,Field)
    UC = arcpy.UpdateCursor(CMFDataLayer)
    for URow in UC:
        FID = GetFID(URow)
        URow.setValue(F_CMFFID['name'],FID)
        UC.updateRow(URow)

    arcpy.AddMessage("    Buffer: Sites Layer")
    FBuffer = 30 + 1.1 * MaximumValue(SiteLayer, F_RBuffer['name'])
    if FBuffer<250: FBuffer = 250
    LeftBuffer = Buffer(SiteLayer,"FOLeftBuffer" ,{'distance': FBuffer, 'line_side': 'LEFT' , 'line_end_type': 'FLAT', 'dissolve_option': 'NONE', 'dissolve_field': '#'})
    RightBuffer = Buffer(SiteLayer,"FORightBuffer",{'distance': FBuffer, 'line_side': 'RIGHT', 'line_end_type': 'FLAT', 'dissolve_option': 'NONE', 'dissolve_field': '#'})

    arcpy.AddMessage("    Intersect: Sites Layer + Fixed Obj Layer")
    LeftBI = Intersect(LeftBuffer + ';' + CMFDataLayer,"FOLeftIntersect" ,{'join_attributes': "ALL", 'cluster_tolerance': '', 'output_type': "LINE"})
    RightBI = Intersect(RightBuffer + ';' + CMFDataLayer,"FORightIntersect",{'join_attributes': "ALL", 'cluster_tolerance': '', 'output_type': "LINE"})

    arcpy.AddMessage("    Search Cursor: Sites Layer, Update Cursor: Fixed Obj Layer")
    # Saves a list of fixed objects in NumFO array, updates road FID in Fixed obj
    # layer
    def GetValFloat(Row, Field, Default):
         try:
             return float(Row.getValue(Field))
         except:
             arcpy.AddMessage("    Could not change " + Field + ' = ' + str(Row.getValue(Field)) + ' to float; Default value assumed: ' + str(Default))
    NumFO = []
    SitesWithData = 0
    SC1 = arcpy.UpdateCursor(SiteLayer)
    for SRow1 in SC1:
        SFID = SRow1.getValue(F_RouteFID['name'])
        Flag = True
        Left = []
        SC2 = arcpy.SearchCursor(LeftBI,'"' + F_RouteFID['name'] + '" = ' + str(SFID))
        for SRow2 in SC2:
            CMFFID = SRow2.getValue(F_CMFFID['name'])
            UC = arcpy.UpdateCursor(CMFDataLayer,'"' + F_CMFFID['name'] + '" = ' + str(CMFFID))
            URow = UC.next()
            DCT = int(GetValFloat(URow,DCField,1))        
            URow.setValue(F_RouteFID['name'],SFID)
            CMFLength = SRow2.getValue("Shape_Length")
            if DCT == 1:
                FO = int(GetValFloat(URow,FOField,0))
                Offset = int(GetValFloat(URow,OffsetField,15))
                if FO > int(CMFLength / 70) + 1: FO = int(CMFLength / 70) + 1        
            if DCT == 2:
                FO = 1
                Offset = CMFLength
            UC.updateRow(URow)
            Left.append([FO,Offset])
            if Flag:
                SitesWithData += 1
                Flag = False
        Right = []
        SC2 = arcpy.SearchCursor(RightBI,'"' + F_RouteFID['name'] + '" = ' + str(SFID))
        for SRow2 in SC2:
            CMFFID = SRow2.getValue(F_CMFFID['name'])
            UC = arcpy.UpdateCursor(CMFDataLayer,'"' + F_CMFFID['name'] + '" = ' + str(CMFFID))
            URow = UC.next()                
            DCT = int(GetValFloat(URow,DCField,1))        
            URow.setValue(F_RouteFID['name'],SFID)
            CMFLength = SRow2.getValue("Shape_Length")
            if DCT == 1:
                FO = int(GetValFloat(URow,FOField,0))
                Offset = int(GetValFloat(URow,OffsetField,15))
                if FO > int(CMFLength / 70) + 1: FO = int(CMFLength / 70) + 1        
            if DCT == 2:
                FO = 1
                Offset = CMFLength
            UC.updateRow(URow)
            Right.append([FO,Offset])
            if Flag:
                SitesWithData += 1
                Flag = False
        #if not Flag:arcpy.AddMessage(str([SFID,Left,Right]))
        NumFO.append([Left,Right])
    arcpy.AddMessage("    Total Sites with Data: " + str(SitesWithData))

    arcpy.AddMessage("    Update Cursor: Sites Layer")
    i = 0
    UC = arcpy.UpdateCursor(SiteLayer)
    for URow in UC:
        FType = URow.getValue(F_FType['name'])
        SegLength = URow.getValue('Shape').length

        # Counting Objects
        LTotObj = 0
        for Obj in NumFO[i][0]: LTotObj += Obj[0]
        RTotObj = 0
        for Obj in NumFO[i][1]: RTotObj += Obj[0]

        # Equivalent offset
        LSoM = 0 # Summation of Multiplications of # of Obj and Offsets for Left Side
        for Obj in NumFO[i][0]: LSoM += Obj[0] * Obj[1]  # # of Obj * Offset of Obj
        if LTotObj == 0:  # Left Equivalent Offset
            LEOffset = 0
        else:
            LEOffset = LSoM / LTotObj

        RSoM = 0 # Summation of Multiplications of # of Obj and Offsets for Right Side
        for Obj in NumFO[i][1]: RSoM += Obj[0] * Obj[1]  # # of Obj * Offset of Obj
        if RTotObj == 0:  # Right Equivalent Offset
            REOffset = 0
        else:
            REOffset = RSoM / RTotObj

        # Adjustment for maximum total number of objects
        MaxObj = int(SegLength / 70) + 1
        if LTotObj > MaxObj: LTotObj = MaxObj
        if RTotObj > MaxObj: RTotObj = MaxObj

        # Aggregating Both Sides:
        if SegLength == 0:
            Density = 0
        else:
            Density = (LTotObj + RTotObj) / (SegLength / 5280)
    
        if (LTotObj + RTotObj) == 0:
            EOffset = 0
        else:
            EOffset = (LEOffset * LTotObj + REOffset * RTotObj) / (LTotObj + RTotObj)
        #arcpy.AddMessage(str([FType,Density,LEOffset,REOffset,EOffset]))
        
        CMFFO = CMFFixedObjects(FType,Density,EOffset)
        URow.setValue(F_FODensity['name'],Density)
        if EOffset == 0: EOffset = 15
        URow.setValue(F_FOOffset['name'],EOffset)
        URow.setValue(F_CMFFO['name'],CMFFO)
        UC.updateRow(URow)
        i += 1

    for Field in [F_RouteFID]:
        arcpy.DeleteField_management(SiteLayer,Field['name'])

    arcpy.CopyFeatures_management(SiteLayer, Output)
    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")
def ImportLighting(SiteInput, CMFDataInput, LBuffer, Output):
    arcpy.AddMessage(" ")
    arcpy.AddMessage("    Lighting")

    OutDic = OutputParser(Output, 'shp')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("    Copy Features: Site Layer")
    SiteLayer = CopyFeatures(SiteInput,'SiteInput')
    TotalSites = arcpy.GetCount_management(SiteLayer)
    arcpy.AddMessage("     - Total Items Found: " + str(TotalSites))

    arcpy.AddMessage("    Copy Features: Lighting Data Layer")
    CMFDataLayer = CopyFeatures(CMFDataInput,'LightingInput')
    TotalCMF = arcpy.GetCount_management(CMFDataLayer)
    arcpy.AddMessage("     - Total Items Found: " + str(TotalCMF))

    arcpy.AddMessage("    Adding Fields")

    FieldList1 = [F_RouteFID, F_Mileage, F_CMFLight, F_LIGHTING]
    FieldList2 = [F_RouteFID, F_CMFFID]

    for Field in FieldList1:
        AddField(SiteLayer,Field,'append')
    arcpy.AddMessage("    Calculating Fields")
    UC = arcpy.UpdateCursor(SiteLayer)
    for URow in UC:
        FID = GetFID(URow)
        URow.setValue(F_RouteFID['name'],FID)
        UC.updateRow(URow)
    FIDMileage = {SRow.getValue(F_RouteFID['name']):[] for SRow in arcpy.SearchCursor(SiteLayer)}

    arcpy.AddMessage("    Locate Features Along Routes: SiteLayer + Lighting Data Layer")
    LFAR = LocateFeaturesAlongRoutes(CMFDataLayer,SiteLayer,  F_RouteFID['name'], str(LBuffer) + " Feet", "LLFAR", F_RouteFID['name'] + " POINT " + F_Mileage['name'])

    arcpy.AddMessage("    Finding Duplicates")
    for SRow in arcpy.SearchCursor(LFAR):
        FIDMileage[SRow.getValue(F_RouteFID['name'])].append(SRow.getValue(F_Mileage['name']) * 5280)

    for Field in FieldList2:
        AddField(CMFDataLayer,Field)


    UC = arcpy.UpdateCursor(CMFDataLayer)
    for URow in UC:
        FID = GetFID(URow)
        URow.setValue(F_CMFFID['name'],FID)
        UC.updateRow(URow)


    arcpy.AddMessage("    Buffer: SiteLayer")
    SBuffer = Buffer(SiteLayer,"LBuffer",{'distance': str(LBuffer) + " Feet", 'line_side': 'FULL', 'line_end_type': 'FLAT', 'dissolve_option': 'NONE', 'dissolve_field': '#'})

    arcpy.AddMessage("    Intersect: Buffer + CMF Layer")
    BI = Intersect(SBuffer + ';' + CMFDataLayer,"LIntersect",{'join_attributes': "ALL", 'cluster_tolerance': '', 'output_type': "POINT"})




    #arcpy.AddMessage(" Route Event Layer: SiteLayer + Lighting Data Layer")
    #REL = MakeRouteEventLayer(SiteLayer, F_RouteFID['name'], LFAR,
    #F_RouteFID['name'] + " POINT " + F_Mileage['name'], "LMREL")
    arcpy.AddMessage("    Reading Info")
    AllL = []
    SitesWithData = 0
    SC1 = arcpy.UpdateCursor(SiteLayer)
    for SRow1 in SC1:
        SFID = SRow1.getValue(F_RouteFID['name'])
        SC2 = arcpy.SearchCursor(BI,'"' + F_RouteFID['name'] + '" = ' + str(SFID))
        T = []
        Flag = True
        for SRow2 in SC2:
            CMFFID = SRow2.getValue(F_CMFFID['name'])
            UC = arcpy.UpdateCursor(CMFDataLayer,'"' + F_CMFFID['name'] + '" = ' + str(CMFFID))
            URow = UC.next()
            URow.setValue(F_RouteFID['name'],SFID)
            #L = int(GetVal(URow,LField,0))
            L = 1
            UC.updateRow(URow)
            if L == 1:
                T.append(L)
                if Flag:
                    SitesWithData += 1
                    Flag = False
        #arcpy.AddMessage(str(T))
        AllL.append(T)
    arcpy.AddMessage("    Total Sites with Data: " + str(SitesWithData))

    #arcpy.AddMessage(" Calculating CMF")
    #i = 0
    #UC = arcpy.UpdateCursor(SiteLayer)
    #for URow in UC:
    #    FType = URow.getValue(F_FType['name'])
    #    SLen = URow.getValue("Shape").length
    #    CMFL = 1
    #    L = len(AllL[i])
    #    #arcpy.AddMessage(str(L))
    #    if L > 0:
    #        Factor = L*200/SLen #Assuming each light pole is effective for 200ft
    #        length of roadway
    #        if Factor > 1: Factor = 1
    #        CMFL = 1 - (Factor * (1-CMFLighting('',FType,1)))
    #    URow.setValue(F_CMFLight['name'],CMFL)
    #    UC.updateRow(URow)
    #    i += 1
    def FindFactor(SegLen, MList, Cov):
        def MergeIntervals(Int1,Int2):
            if Int1[1] > Int2[0]:
                return [Int1[0],Int2[1]]
            else:
                return ''
        def NewIntervals(OldInts):
            if len(OldInts) > 1:
                NewInts = []
            else:
                return OldInts
            for i in range(0,len(OldInts) - 1):
                Res = MergeIntervals(OldInts[i], OldInts[i + 1])
                if Res <> '':
                    if len(NewInts) > 0:
                        if Res[1] > NewInts[len(NewInts) - 1][1]:
                            NewInts.append(Res)
                    else:
                        NewInts.append(Res)
                else:
                    if len(NewInts) > 0:
                        if OldInts[i][1] > NewInts[len(NewInts) - 1][1]:
                            NewInts.append(OldInts[i])
                    else:
                        NewInts.append(OldInts[i])
                    if i == len(OldInts) - 2:
                        if len(NewInts) > 0:
                            if OldInts[i + 1][1] > NewInts[len(NewInts) - 1][1]:
                                NewInts.append(OldInts[i + 1])
                        else:
                            NewInts.append(OldInts[i + 1])
            return NewInts

        MList.sort()
        Ints = []
        for M in MList:
            Ints.append([M - Cov / 2.0, M + Cov / 2.0])
        L1 = len(Ints)
        NI = NewIntervals(Ints)
        while len(NI) <> L1:
            L1 = len(NI)
            NI = NewIntervals(NI)
        L = []
        for Int in NI:
            L.append(Int[1] - Int[0])
        TotL = sum(L)
        Factor = TotL / SegLen
        if Factor > 1: Factor = 1
        return Factor

    arcpy.AddMessage("    Calculating CMF")
    i = 0
    UC = arcpy.UpdateCursor(SiteLayer)
    for URow in UC:
        FType = URow.getValue(F_FType['name'])
        RID = URow.getValue(F_RouteFID['name'])
        SLen = URow.getValue("Shape").length
        CMFL = 1
        Factor = 0
        L = len(FIDMileage[RID])
        if L > 0: 
        
            Factor = FindFactor(SLen,FIDMileage[RID],200) #Assuming each light pole is effective for 200ft length of roadway
            CMFL = 1 - (Factor * (1 - CMFLighting('',FType,1)))
        URow.setValue(F_LIGHTING['name'],Factor)
        URow.setValue(F_CMFLight['name'],CMFL)
        UC.updateRow(URow)
        i += 1
    del UC

    arcpy.CopyFeatures_management(SiteLayer, Output)
    for Field in [F_RouteFID['name'], F_Mileage['name'], 'MEAS', 'RID']:
        arcpy.DeleteField_management(Output,Field)
    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")
def ImportMedianWidth(SiteInput, CMFDataInput, MWField, Output):
    arcpy.AddMessage(" ")
    arcpy.AddMessage("    Median Width")

    OutDic = OutputParser(Output, 'shp')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("    Copy Features: Site Layer")
    SiteLayer = CopyFeatures(SiteInput,'SiteInput')
    TotalSites = arcpy.GetCount_management(SiteLayer)
    arcpy.AddMessage("     - Total number of Items Found: " + str(TotalSites))

    arcpy.AddMessage("    Copy Features: Median Width Layer")
    CMFDataLayer = CopyFeatures(CMFDataInput,'MWInput')
    TotalSites = arcpy.GetCount_management(CMFDataLayer)
    arcpy.AddMessage("     - Total number of Items Found: " + str(TotalSites))

    arcpy.AddMessage("    Adding Fields")

    FieldList1 = [F_FType, F_RouteFID, F_CMFMW, F_Median_Wid]
    FieldList2 = [F_RouteFID, F_SegLength, F_CMFFID]

    for Field in FieldList1:
        AddField(SiteLayer,Field,'append')

    for Field in FieldList2:
        AddField(CMFDataLayer,Field)

    arcpy.AddMessage("    Calculating Fields")
    UC = arcpy.UpdateCursor(SiteLayer)
    for URow in UC:
        FID = GetFID(URow)
        URow.setValue(F_RouteFID['name'],FID)
        UC.updateRow(URow)

    UC = arcpy.UpdateCursor(CMFDataLayer)

    for URow in UC:
        FID = GetFID(URow)
        URow.setValue(F_CMFFID['name'],FID)
        UC.updateRow(URow)

    arcpy.AddMessage("    Performing Buffer")
    FBuffer = 250
    SBuffer = Buffer(SiteLayer,"MWBuffer",{'distance': FBuffer, 'line_side': 'FULL', 'line_end_type': 'FLAT', 'dissolve_option': 'NONE', 'dissolve_field': '#'})

    arcpy.AddMessage("    Performing Intersect")
    BI = Intersect(SBuffer + ';' + CMFDataLayer,"MWIntersect",{'join_attributes': "ALL", 'cluster_tolerance': '', 'output_type': "POINT"})

    arcpy.AddMessage("    Reading Info")
    AllMW = []
    SitesWithData = 0
    SC1 = arcpy.UpdateCursor(SiteLayer)
    for SRow1 in SC1:
        SFID = SRow1.getValue(F_RouteFID['name'])
        SC2 = arcpy.SearchCursor(BI,'"' + F_RouteFID['name'] + '" = ' + str(SFID))
        T = []
        Flag = True
        for SRow2 in SC2:
            CMFFID = SRow2.getValue(F_CMFFID['name'])
            UC = arcpy.UpdateCursor(CMFDataLayer,'"' + F_CMFFID['name'] + '" = ' + str(CMFFID))
            URow = UC.next()
                
            URow.setValue(F_RouteFID['name'],SFID)

            MW = float(GetVal(URow,MWField,15))
            UC.updateRow(URow)
            T.append(MW)
            if Flag:
                SitesWithData += 1
                Flag = False
        AllMW.append(T)
    arcpy.AddMessage("    Total Sites with Data: " + str(SitesWithData))

    arcpy.AddMessage("    Calculating CMF")
    i = 0
    UC = arcpy.UpdateCursor(SiteLayer)
    for URow in UC:
        FType = URow.getValue(F_FType['name'])
        CMFMW = 0
        for MW in AllMW[i]:
            CMFMW += CMFMedianWidth(FType,MW)
        if CMFMW == 0:
            CMFMW = 1
        else:
            CMFMW = CMFMW / len(AllMW[i])
        URow.setValue(F_CMFMW['name'],CMFMW)
        URow.setValue(F_Median_Wid['name'],float(sum(AllMW[i]))/max(len(AllMW[i]),1))
        UC.updateRow(URow)
        i += 1

    arcpy.CopyFeatures_management(SiteLayer, Output)
    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")
def ImportOnStreetParking(SiteInput, CMFDataInput, ParkTypeField, AreaTypeField, Output):
    arcpy.AddMessage(" ")
    arcpy.AddMessage("    On Street Parking Import")

    OutDic = OutputParser(Output, 'shp')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("    Copy Features: Site Layer")
    SiteLayer = CopyFeatures(SiteInput,'OSPSite')
    TotalSites = arcpy.GetCount_management(SiteLayer)
    arcpy.AddMessage("     - Total number of Sites Found: " + str(TotalSites))

    arcpy.AddMessage("    Copy Features: CMF Data Layer")
    CMFDataLayer = CopyFeatures(CMFDataInput,'OSPData')
    TotalCMF = arcpy.GetCount_management(CMFDataLayer)
    arcpy.AddMessage("     - Total number of CMF Items Found: " + str(TotalCMF))

    arcpy.AddMessage("    Add Fields: Site Layer")
    FieldList1 = [F_RouteFID, F_CMFOSP, F_OSPType, F_OSPProp]
    for Field in FieldList1:
        AddField(SiteLayer,Field,'append')
    UC = arcpy.UpdateCursor(SiteLayer)
    for URow in UC:
        FID = GetFID(URow)
        URow.setValue(F_RouteFID['name'],FID)
        UC.updateRow(URow)

    arcpy.AddMessage("    Add Fields: On Street Parking Layer")
    FieldList2 = [F_RouteFID, F_SegLength, F_CMFFID, F_CMFLength]
    for Field in FieldList2:
        AddField(CMFDataLayer,Field)
    UC = arcpy.UpdateCursor(CMFDataLayer)
    for URow in UC:
        FID = GetFID(URow)
        URow.setValue(F_CMFFID['name'],FID)
        UC.updateRow(URow)

    arcpy.AddMessage("    Buffer: Sites Layer")
    FBuffer = 250
    SBuffer = Buffer(SiteLayer,"OSPBuffer",{'distance': FBuffer, 'line_side': 'FULL', 'line_end_type': 'FLAT', 'dissolve_option': 'NONE', 'dissolve_field': '#'})

    arcpy.AddMessage("    Intersect: Buffer + On Street Parking Layer")
    BI = Intersect(SBuffer + ';' + CMFDataLayer,"OSPIntersect",{'join_attributes': "ALL", 'cluster_tolerance': '', 'output_type': "LINE"})

    arcpy.AddMessage("    Update Cursor: Sites Layer")
    def GetOSP(Row, Field,DefaultVal):
        try:
            return int(Row.getValue(Field))
        except:
            return DefaultVal
    
    OSPPropor = []
    SitesWithData = 0
    SC1 = arcpy.UpdateCursor(SiteLayer)
    for SRow1 in SC1:
        SFID = SRow1.getValue(F_RouteFID['name'])
        FType = SRow1.getValue(F_FType['name'])
        if not FType: FType = ' '
        CMFOSP = 1
        SC2 = arcpy.SearchCursor(BI,'"' + F_RouteFID['name'] + '" = ' + str(SFID))
        T = [[0,0,0,0,0],[0,0,0,0,0]]
        Flag = True
        for SRow2 in SC2:
            CMFFID = SRow2.getValue(F_CMFFID['name'])
            UC = arcpy.UpdateCursor(CMFDataLayer,'"' + F_CMFFID['name'] + '" = ' + str(CMFFID))
            URow = UC.next()
                
            URow.setValue(F_RouteFID['name'],SFID)

            CMFLength = SRow2.getValue("Shape_Length")
            URow.setValue(F_CMFLength['name'],CMFLength)
            URow.setValue(F_SegLength['name'],SRow1.getValue("Shape").length)

            AreaT = GetOSP(URow,AreaTypeField,5)
            ParkT = GetOSP(URow,ParkTypeField,2)
            Propor = float(URow.getValue(F_CMFLength['name'])) / float(URow.getValue(F_SegLength['name'])) / 2
        
            UC.updateRow(URow)
            T[ParkT - 1][AreaT - 1] = T[ParkT - 1][AreaT - 1] + Propor
            if Flag:
                SitesWithData += 1
                Flag = False
        OSPP = 0
        OSPT = 0
        MaxCMF = 1
        if FType in ['U2U','U4D','U4U','U3T','U5T']:
            for ParkT in [1,2]:
                for AreaT in [1,2,3,4,5]:
                    t =  CMFOnStreetParking(FType,ParkT,AreaT,T[ParkT - 1][AreaT - 1])
                    if t>MaxCMF:
                        MaxCMF = t
                        OSPP = T[ParkT - 1][AreaT - 1]
                        OSPT = 1*(ParkT==2 and AreaT in [1,5]) + 2*(ParkT==2 and AreaT in [2,3,4]) + 3*(ParkT==2 and AreaT in [1,5]) + 4*(ParkT==2 and AreaT in [2,3,4])
                    CMFOSP = CMFOSP * t
        SRow1.setValue(F_CMFOSP['name'],CMFOSP)
        SRow1.setValue(F_OSPProp['name'],OSPP)
        SRow1.setValue(F_OSPType['name'],OSPT)
        SC1.updateRow(SRow1)
        if CMFOSP <> 1:
            arcpy.AddMessage('    FID: ' + str(SFID) + ', Type: ' + FType + ', OSP: ' + str(T) + ', CMF: ' + str(CMFOSP))

    arcpy.AddMessage("    Total Sites with Data: " + str(SitesWithData))
    arcpy.CopyFeatures_management(SiteLayer, Output)
    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")
def ImportRHR(SiteInput, CMFDataInput, RHRField, Output):
    arcpy.AddMessage(" ")
    arcpy.AddMessage("    RHR Import")

    OutDic = OutputParser(Output, 'shp')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("    Copy Features: Site Layer")
    SiteLayer = CopyFeatures(SiteInput,'OSPSite')
    TotalSites = arcpy.GetCount_management(SiteLayer)
    arcpy.AddMessage("     - Total number of Sites Found: " + str(TotalSites))

    arcpy.AddMessage("    Copy Features: CMF Data Layer")
    CMFDataLayer = CopyFeatures(CMFDataInput,'OSPData')
    TotalCMF = arcpy.GetCount_management(CMFDataLayer)
    arcpy.AddMessage("     - Total number of CMF Items Found: " + str(TotalCMF))

    arcpy.AddMessage("    Add Fields: Site Layer")
    FieldList1 = [F_RouteFID, F_RHR, F_CMFRHR]
    for Field in FieldList1:
        AddField(SiteLayer,Field,'append')
    UC = arcpy.UpdateCursor(SiteLayer)
    for URow in UC:
        FID = GetFID(URow)
        URow.setValue(F_RouteFID['name'],FID)
        UC.updateRow(URow)

    arcpy.AddMessage("    Add Fields: RHR Layer")
    FieldList2 = [F_RouteFID, F_SegLength, F_CMFFID]
    for Field in FieldList2:
        AddField(CMFDataLayer,Field)
    UC = arcpy.UpdateCursor(CMFDataLayer)
    for URow in UC:
        FID = GetFID(URow)
        URow.setValue(F_CMFFID['name'],FID)
        UC.updateRow(URow)

    arcpy.AddMessage("    Buffer: Sites Layer")
    FBuffer = 250
    SBuffer = Buffer(SiteLayer,"OSPBuffer",{'distance': FBuffer, 'line_side': 'FULL', 'line_end_type': 'ROUND', 'dissolve_option': 'NONE', 'dissolve_field': '#'})

    arcpy.AddMessage("    Intersect: Buffer + On Street Parking Layer")
    BI = Intersect(SBuffer + ';' + CMFDataLayer,"OSPIntersect",{'join_attributes': "ALL", 'cluster_tolerance': '', 'output_type': "POINT"})

    arcpy.AddMessage("    Update Cursor: Sites Layer")
    def GetOSP(Row, Field,DefaultVal):
        try:
            return int(Row.getValue(Field))
        except:
            return DefaultVal
    
    OSPPropor = []
    SitesWithData = 0
    SC1 = arcpy.UpdateCursor(SiteLayer)
    for SRow1 in SC1:
        SFID = SRow1.getValue(F_RouteFID['name'])
        FType = SRow1.getValue(F_FType['name'])
        if not FType: FType = ' '

        SC2 = arcpy.SearchCursor(BI,'"' + F_RouteFID['name'] + '" = ' + str(SFID))

        Flag = True
        RHR = []
        for SRow2 in SC2:
            CMFFID = SRow2.getValue(F_CMFFID['name'])
            UC = arcpy.UpdateCursor(CMFDataLayer,'"' + F_CMFFID['name'] + '" = ' + str(CMFFID))
            URow = UC.next()
                
            URow.setValue(F_RouteFID['name'],SFID)
            URow.setValue(F_SegLength['name'],SRow1.getValue("Shape").length)

            RHR.append(GetOSP(URow,RHRField,1))
        
            UC.updateRow(URow)

        t = float(sum(RHR))/max(len(RHR),1)
        if t == 0: t=1
        SRow1.setValue(F_RHR['name'],t)
        SRow1.setValue(F_CMFRHR['name'],CMFRHR(FType,t))
        
        SC1.updateRow(SRow1)
        if len(RHR) > 1:
            arcpy.AddMessage('    FID: ' + str(SFID) + ', Type: ' + FType + ', RHR: ' + str(RHR) + ', Average: ' + str(t))

    arcpy.AddMessage("    Total Sites with Data: " + str(SitesWithData))
    arcpy.CopyFeatures_management(SiteLayer, Output)
    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")
def ImportShoulderWidth(SiteInput, CMFDataInput, ShWField, ShTField, Output):
    arcpy.AddMessage(" ")
    arcpy.AddMessage("    Shoulder Width Import")

    OutDic = OutputParser(Output, 'shp')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("    Copy Features: Site Layer")
    SiteLayer = CopyFeatures(SiteInput,'OSPSite')
    TotalSites = arcpy.GetCount_management(SiteLayer)
    arcpy.AddMessage("     - Total number of Sites Found: " + str(TotalSites))

    arcpy.AddMessage("    Copy Features: CMF Data Layer")
    CMFDataLayer = CopyFeatures(CMFDataInput,'OSPData')
    TotalCMF = arcpy.GetCount_management(CMFDataLayer)
    arcpy.AddMessage("     - Total number of CMF Items Found: " + str(TotalCMF))

    arcpy.AddMessage("    Add Fields: Site Layer")
    FieldList1 = [F_RouteFID, F_Shuold_Wid, F_Shuold_Typ, F_CMFSW]
    for Field in FieldList1:
        AddField(SiteLayer,Field,'append')
    UC = arcpy.UpdateCursor(SiteLayer)
    for URow in UC:
        FID = GetFID(URow)
        URow.setValue(F_RouteFID['name'],FID)
        UC.updateRow(URow)

    arcpy.AddMessage("    Add Fields: ShW Layer")
    FieldList2 = [F_RouteFID, F_SegLength, F_CMFFID, F_CMFSW]
    for Field in FieldList2:
        AddField(CMFDataLayer,Field)
    UC = arcpy.UpdateCursor(CMFDataLayer)
    for URow in UC:
        FID = GetFID(URow)
        URow.setValue(F_CMFFID['name'],FID)
        UC.updateRow(URow)

    arcpy.AddMessage("    Buffer: Sites Layer")
    FBuffer = 250
    SBuffer = Buffer(SiteLayer,"OSPBuffer",{'distance': FBuffer, 'line_side': 'FULL', 'line_end_type': 'ROUND', 'dissolve_option': 'NONE', 'dissolve_field': '#'})

    arcpy.AddMessage("    Intersect: Buffer + On Street Parking Layer")
    BI = Intersect(SBuffer + ';' + CMFDataLayer,"OSPIntersect",{'join_attributes': "ALL", 'cluster_tolerance': '', 'output_type': "POINT"})

    arcpy.AddMessage("    Update Cursor: Sites Layer")
    def GetOSP(Row, Field,DefaultVal):
        try:
            return int(Row.getValue(Field))
        except:
            return DefaultVal
    
    OSPPropor = []
    SitesWithData = 0
    SC1 = arcpy.UpdateCursor(SiteLayer)
    for SRow1 in SC1:
        SFID = SRow1.getValue(F_RouteFID['name'])
        FType = SRow1.getValue(F_FType['name'])
        if not FType: FType = ' '

        SC2 = arcpy.SearchCursor(BI,'"' + F_RouteFID['name'] + '" = ' + str(SFID))

        Flag = True
        RHR = []
        ShT = []
        for SRow2 in SC2:
            CMFFID = SRow2.getValue(F_CMFFID['name'])
            UC = arcpy.UpdateCursor(CMFDataLayer,'"' + F_CMFFID['name'] + '" = ' + str(CMFFID))
            URow = UC.next()
                
            URow.setValue(F_RouteFID['name'],SFID)
            URow.setValue(F_SegLength['name'],SRow1.getValue("Shape").length)

            RHR.append(URow.getValue(ShWField))
            a = URow.getValue(ShTField)
            b= 1
            if a == 'Paved': b = 1
            if a == 'Gravel': b = 2
            if a == 'Composite': b = 3
            if a == 'Turf': b = 4
            ShT.append(b)
        
            UC.updateRow(URow)

        t1 = float(sum(RHR))/max(len(RHR),1)
        try:
            t2 = min(ShT)
        except:
            t2 = 0
        SRow1.setValue(F_Shuold_Wid['name'],t1)
        SRow1.setValue(F_Shuold_Typ['name'],t2)
        SRow1.setValue(F_CMFSW['name'],CMFShoulderWidthType(FType,t1,t2,SRow1.getValue(F_AADT['name'])))
        SC1.updateRow(SRow1)
        if len(RHR) > 1:
            arcpy.AddMessage('    FID: ' + str(SFID) + ', Type: ' + FType + ', ShW: ' + str(RHR) + ', Average: ' + str(t1))

    arcpy.AddMessage("    Total Sites with Data: " + str(SitesWithData))
    arcpy.CopyFeatures_management(SiteLayer, Output)
    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")
def ImportLaneWidth(SiteInput, CMFDataInput, LnWField, Output):
    arcpy.AddMessage(" ")
    arcpy.AddMessage("    Shoulder Width Import")

    OutDic = OutputParser(Output, 'shp')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("    Copy Features: Site Layer")
    SiteLayer = CopyFeatures(SiteInput,'OSPSite')
    TotalSites = arcpy.GetCount_management(SiteLayer)
    arcpy.AddMessage("     - Total number of Sites Found: " + str(TotalSites))

    arcpy.AddMessage("    Copy Features: CMF Data Layer")
    CMFDataLayer = CopyFeatures(CMFDataInput,'OSPData')
    TotalCMF = arcpy.GetCount_management(CMFDataLayer)
    arcpy.AddMessage("     - Total number of CMF Items Found: " + str(TotalCMF))

    arcpy.AddMessage("    Add Fields: Site Layer")
    FieldList1 = [F_RouteFID, F_Lane_Width, F_CMFLW]
    for Field in FieldList1:
        AddField(SiteLayer,Field,'append')
    UC = arcpy.UpdateCursor(SiteLayer)
    for URow in UC:
        FID = GetFID(URow)
        URow.setValue(F_RouteFID['name'],FID)
        UC.updateRow(URow)

    arcpy.AddMessage("    Add Fields: LnW Layer")
    FieldList2 = [F_RouteFID, F_SegLength, F_CMFFID]
    for Field in FieldList2:
        AddField(CMFDataLayer,Field)
    UC = arcpy.UpdateCursor(CMFDataLayer)
    for URow in UC:
        FID = GetFID(URow)
        URow.setValue(F_CMFFID['name'],FID)
        UC.updateRow(URow)

    arcpy.AddMessage("    Buffer: Sites Layer")
    FBuffer = 250
    SBuffer = Buffer(SiteLayer,"OSPBuffer",{'distance': FBuffer, 'line_side': 'FULL', 'line_end_type': 'ROUND', 'dissolve_option': 'NONE', 'dissolve_field': '#'})

    arcpy.AddMessage("    Intersect: Buffer + On Street Parking Layer")
    BI = Intersect(SBuffer + ';' + CMFDataLayer,"OSPIntersect",{'join_attributes': "ALL", 'cluster_tolerance': '', 'output_type': "POINT"})

    arcpy.AddMessage("    Update Cursor: Sites Layer")
    def GetOSP(Row, Field,DefaultVal):
        try:
            return float(Row.getValue(Field))
        except:
            return DefaultVal
    
    OSPPropor = []
    SitesWithData = 0
    SC1 = arcpy.UpdateCursor(SiteLayer)
    for SRow1 in SC1:
        SFID = SRow1.getValue(F_RouteFID['name'])
        FType = SRow1.getValue(F_FType['name'])
        if not FType: FType = ' '

        SC2 = arcpy.SearchCursor(BI,'"' + F_RouteFID['name'] + '" = ' + str(SFID))

        Flag = True
        RHR = []
        ShT = []
        for SRow2 in SC2:
            CMFFID = SRow2.getValue(F_CMFFID['name'])
            UC = arcpy.UpdateCursor(CMFDataLayer,'"' + F_CMFFID['name'] + '" = ' + str(CMFFID))
            URow = UC.next()
                
            URow.setValue(F_RouteFID['name'],SFID)
            URow.setValue(F_SegLength['name'],SRow1.getValue("Shape").length)

            RHR.append(GetOSP(URow,LnWField,12))
    
            UC.updateRow(URow)

        t1 = float(sum(RHR))/max(len(RHR),1)
        SRow1.setValue(F_Lane_Width['name'],t1)
        SRow1.setValue(F_CMFLW['name'],CMFLaneWidth(FType,t1,SRow1.getValue(F_AADT['name'])))
        SC1.updateRow(SRow1)
        if len(RHR) > 1:
            arcpy.AddMessage('    FID: ' + str(SFID) + ', Type: ' + FType + ', LnW: ' + str(RHR) + ', Average: ' + str(t1))

    arcpy.AddMessage("    Total Sites with Data: " + str(SitesWithData))
    arcpy.CopyFeatures_management(SiteLayer, Output)
    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")
def ImportLaneChange(SiteInput,WeavingInput,AllSegInput, Output):
    arcpy.AddMessage(" ")
    arcpy.AddMessage("    Lane Change Import")

    OutDic = OutputParser(Output, 'shp')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("    Copy Features: Site Layer")
    SiteLayer = CopyFeatures(SiteInput,'LCSite')
    TotalSites = arcpy.GetCount_management(SiteLayer)
    arcpy.AddMessage("     - Total number of Sites Found: " + str(TotalSites))

    arcpy.AddMessage("    Copy Features: CMF Data Layer")
    CMFDataLayer = CopyFeatures(WeavingInput,'LCData')
    TotalCMF = arcpy.GetCount_management(CMFDataLayer)
    arcpy.AddMessage("     - Total number of CMF Items Found: " + str(TotalCMF))

    arcpy.AddMessage("    Add Fields: Site Layer")
    FieldList1 = [F_RouteFID, F_CMFLChgFI,F_CMFLChgPDO]
    for Field in FieldList1:
        AddField(SiteLayer,Field,'append')
    UC = arcpy.UpdateCursor(SiteLayer)
    for URow in UC:
        FID = GetFID(URow)
        URow.setValue(F_RouteFID['name'],FID)
        UC.updateRow(URow)

    SiteDict = {Row.getValue(F_RouteFID['name']):{'LsWevInc':0,'LsWevDec':0,'LWevInc':1,'LWevDec':1,'Ls':Row.getValue('Shape').length/5280,
                                                  'XbEnt':10,'XbExt':10,'XeEnt':10,'XeExt':10,
                                                  'AADTbEnt':1000,'AADTbExt':1000,'AADTeEnt':1000,'AADTeExt':1000, 'Oneway':Row.getValue(F_Oneway['name'])} 
                for Row in arcpy.SearchCursor(SiteLayer)}

    arcpy.AddMessage("    Add Fields: Weaving Layer")
    FieldList2 = [F_RouteFID, F_SegLength, F_CMFFID]
    for Field in FieldList2:
        AddField(CMFDataLayer,Field)
    UC = arcpy.UpdateCursor(CMFDataLayer)
    for URow in UC:
        FID = GetFID(URow)
        URow.setValue(F_CMFFID['name'],FID)
        UC.updateRow(URow)

    CMFDict = {Row.getValue(F_CMFFID['name']):{'L':Row.getValue('Shape').length/5280} 
                for Row in arcpy.SearchCursor(CMFDataLayer)}

    arcpy.AddMessage("    Buffer: Sites Layer")
    FBuffer = 25
    SBuffer = Buffer(SiteLayer,"LCBuffer",{'distance': FBuffer, 'line_side': 'FULL', 'line_end_type': 'FLAT', 'dissolve_option': 'NONE', 'dissolve_field': '#'})

    arcpy.AddMessage("    Intersect: Buffer + Weaving Layer")
    BI = Intersect(SBuffer + ';' + CMFDataLayer,"LCIntersect",{'join_attributes': "ALL", 'cluster_tolerance': '', 'output_type': "POINT"})
    IntDict = {Row.getValue(F_RouteFID['name']):Row.getValue(F_CMFFID['name']) for Row in arcpy.SearchCursor(BI)}
    for fid in IntDict.keys():
        if SiteDict[fid]['Oneway'] == 0:
            SiteDict[fid]['LWevInc'] = CMFDict[IntDict[fid]]['L']
        if SiteDict[fid]['Oneway'] == 1:
            SiteDict[fid]['LWevDec'] = CMFDict[IntDict[fid]]['L']

    arcpy.AddMessage("    Split Line: Weaving Layer + Intersect")
    CMFSplit = SplitLineAtPoint(CMFDataLayer,BI,'SPLWev','20 Feet')
    arcpy.CalculateField_management(CMFSplit,F_SegLength['name'],'!Shape!.length','PYTHON_9.3')

    arcpy.AddMessage("    Spatial Join: Buffer + Split Layer")
    SPJ = SpatialJoin(SBuffer, CMFSplit, 'LCSPJ',{'join_operation':"JOIN_ONE_TO_MANY",'join_type':"KEEP_COMMON",'field_mapping':'','match_option':'CONTAINS','search_radius':'','distance_field_name':''})
    
    SPJDict = {Row.getValue(F_RouteFID['name']):Row.getValue(F_SegLength['name'])/5280 for Row in arcpy.SearchCursor(SPJ)}
    for fid in SPJDict.keys():
        if SiteDict[fid]['Oneway'] == 0:
            SiteDict[fid]['LsWevInc'] = SPJDict[fid]
        if SiteDict[fid]['Oneway'] == 1:
            SiteDict[fid]['LsWevDec'] = SPJDict[fid]

    arcpy.AddMessage("    Update Cursor: Sites Layer")
    SC = arcpy.UpdateCursor(SiteLayer)
    for SRow in SC:
        SFID = SRow.getValue(F_RouteFID['name'])
        FType = SRow.getValue(F_FType['name'])
        if not FType: FType = ' '

        Flag = True
        CMFLC = CMFLaneChange(FType,SiteDict[SFID])
        SRow.setValue(F_CMFLChgFI['name'],CMFLC['FI'])
        SRow.setValue(F_CMFLChgPDO['name'],CMFLC['PDO'])
        SC.updateRow(SRow)

    arcpy.CopyFeatures_management(SiteLayer, Output)
    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")
def ImportClearZone(SiteInput,CZInput,OBInput,Output):
    arcpy.AddMessage(" ")
    arcpy.AddMessage("    Clear Zone Import")

    OutDic = OutputParser(Output, 'shp')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("    Copy Features: Site Layer")
    SiteLayer = CopyFeatures(SiteInput,'CZSite')
    TotalSites = arcpy.GetCount_management(SiteLayer)
    arcpy.AddMessage("     - Total number of Sites Found: " + str(TotalSites))

    arcpy.AddMessage("    Copy Features: ClearZone Data Layer")
    CMFDataLayer = CopyFeatures(CZInput,'CZData')
    TotalCMF = arcpy.GetCount_management(CMFDataLayer)
    arcpy.AddMessage("     - Total number of CMF Items Found: " + str(TotalCMF))

    arcpy.AddMessage("    Copy Features: Outside Barrier Data Layer")
    OBDataLayer = CopyFeatures(OBInput,'OBData')
    TotalCMF = arcpy.GetCount_management(OBDataLayer)
    arcpy.AddMessage("     - Total number of CMF Items Found: " + str(TotalCMF))

    arcpy.AddMessage("    Add Fields: Site Layer")
    FieldList1 = [F_RouteFID,F_CZWidth,F_CMFCZFI,F_CMFOBFI,F_CMFOBPDO]
    for Field in FieldList1:
        AddField(SiteLayer,Field,'append')
    UC = arcpy.UpdateCursor(SiteLayer)
    for URow in UC:
        FID = GetFID(URow)
        URow.setValue(F_RouteFID['name'],FID)
        UC.updateRow(URow)

    SDict = {Row.getValue(F_RouteFID['name']):{'CMFFID':-1,'CZWidth':30,
                                               'SHW_LO':Row.getValue(F_Sh_Wid_LO['name']),'SHW_RO':Row.getValue(F_Sh_Wid_RO['name'])
                                               ,'SW_L':Row.getValue(F_L_Sur_W['name']),'SW_R':Row.getValue(F_R_Sur_W['name']),
                                               'Oneway':Row.getValue(F_Oneway['name'])} for Row in arcpy.SearchCursor(SiteLayer)}
    
    arcpy.AddMessage("    Buffer: Sites Layer")
    FBuffer = 300
    SBuffer = Buffer(SiteLayer,"LCBuffer",{'distance': FBuffer, 'line_side': 'FULL', 'line_end_type': 'FLAT', 'dissolve_option': 'NONE', 'dissolve_field': '#'})

    arcpy.AddMessage("    Intersect: Buffer + Weaving Layer")
    BI = Intersect(SBuffer + ';' + CMFDataLayer,"LCIntersect",{'join_attributes': "ALL", 'cluster_tolerance': '', 'output_type': "POINT"})

    arcpy.AddMessage("    Split Line: CMF Layer + Intersect")
    CMFSplit = SplitLineAtPoint(CMFDataLayer,BI,'SPLWev','5 Feet')

    arcpy.AddMessage("    Add Fields: CMF Layer")
    FieldList2 = [F_CMFFID]
    for Field in FieldList2:
        AddField(CMFSplit,Field)
    UC = arcpy.UpdateCursor(CMFSplit)
    i = 0
    for URow in UC:
        i = i + 1
        URow.setValue(F_CMFFID['name'],i)
        UC.updateRow(URow)
    CMFDict = {Row.getValue(F_CMFFID['name']):{'Dist':[],'SFID':-1} for Row in arcpy.SearchCursor(CMFSplit)}

    arcpy.AddMessage("    Spatial Join: Buffer + Split Layer")
    SPJ1 = SpatialJoin(SBuffer , CMFSplit , 'LCSPJB',{'join_operation':"JOIN_ONE_TO_MANY",'join_type':"KEEP_COMMON",'field_mapping':'','match_option':'CONTAINS','search_radius':'','distance_field_name':''})
    SPJ2 = SpatialJoin(CMFSplit, SiteLayer, 'LCSPJC',{'join_operation':"JOIN_ONE_TO_ONE" ,'join_type':"KEEP_COMMON",'field_mapping':'','match_option':'CLOSEST','search_radius':'','distance_field_name':''})

    for SRow in arcpy.SearchCursor(SPJ2):
        fid = SRow.getValue(F_CMFFID['name'])
        CMFDict[fid]['SFID'] = SRow.getValue(F_RouteFID['name'])  
        #arcpy.AddMessage(str([CMFDict[fid]['SFID'],fid]))
    for SRow in arcpy.SearchCursor(SPJ1):
        SFID   = SRow.getValue(F_RouteFID['name'])
        CMFFID = SRow.getValue(F_CMFFID  ['name'])
        #arcpy.AddMessage(str([SFID,CMFFID]))
        if SFID == CMFDict[CMFFID]['SFID']:
            SDict[SFID]['CMFFID'] = SRow.getValue(F_CMFFID['name'])  
            #arcpy.AddMessage(str([SDict[fid]['CMFFID']]))
    
    V2P = VerticesToPoints(CMFSplit,'CLV2P','ALL')

    arcpy.AddMessage("    Near Analysis: Split Layer")
    arcpy.Near_analysis(V2P,SiteLayer,str(FBuffer)+' Feet')

    for SRow in arcpy.SearchCursor(V2P):
        fid = SRow.getValue(F_CMFFID['name'])
        CMFDict[fid]['Dist'].append(SRow.getValue('NEAR_DIST'))  

    for fid in SDict.keys():
        cmffid = SDict[fid]['CMFFID']
        if cmffid in CMFDict.keys():
            L = CMFDict[cmffid]['Dist']
            MD = sum(L)/len(L)
            MSW = (SDict[fid]['SW_L']+SDict[fid]['SW_R'])/2
            MOS = (SDict[fid]['SHW_LO']+SDict[fid]['SHW_RO'])/2
            SDict[fid]['CZWidth'] = MD - MSW/2 - MOS
            if SDict[fid]['CZWidth']>30:SDict[fid]['CZWidth']=30
            arcpy.AddMessage(str([MD - MSW/2 - MOS]))

    arcpy.AddMessage("    Update Cursor: Sites Layer")
    SC = arcpy.UpdateCursor(SiteLayer)
    for SRow in SC:
        SFID = SRow.getValue(F_RouteFID['name'])
        FType = SRow.getValue(F_FType['name'])
        if not FType: FType = ' '

        Flag = True
        CMFList = CMFCZandOB(FType,0,SDict[SFID]['CZWidth'],30,(SDict[SFID]['SHW_LO']+SDict[SFID]['SHW_RO'])/2)
        SRow.setValue(F_CZWidth ['name'],SDict[SFID]['CZWidth'])
        SRow.setValue(F_CMFCZFI ['name'],CMFList[0])
        SRow.setValue(F_CMFOBFI ['name'],CMFList[1]['FI'])
        SRow.setValue(F_CMFOBPDO['name'],CMFList[1]['PDO'])
        SC.updateRow(SRow)

    arcpy.CopyFeatures_management(SiteLayer, Output)
    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")

## Population Dataset
def ImportRIMSAttributes(SiteInput,DataInput,AADTField,Output):
    SearchRadius = 20
    arcpy.AddMessage(" ")
    arcpy.AddMessage("    Import Attributes")

    OutDic = OutputParser(Output, 'shp')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("    Copy Features: Sites Layer")
    SiteLayer = CopyFeatures(SiteInput,'AttSite')
    TotalSites = arcpy.GetCount_management(SiteLayer)
    arcpy.AddMessage("     - Total number of Items Found: " + str(TotalSites))

    arcpy.AddMessage("    Copy Features: Data Layer")
    DataLayer = CopyFeatures(DataInput,'AttData')
    TotalCMF = arcpy.GetCount_management(DataLayer)
    arcpy.AddMessage("     - Total number of Items Found: " + str(TotalCMF))

    arcpy.AddMessage("    Check Fields: Data Layer")
    FieldList1 = [F_TargetFID]
    for Field in FieldList1:
        arcpy.DeleteField_management(DataLayer,Field['name'])

    arcpy.AddMessage("    Check Fields: Sites Layer")
    FieldList2 = [F_Func_Class, F_Route_Type, F_TotalLanes, F_Median_ID, F_SurWid_Tot, F_Median_Wid, F_AADT, F_Z_Mean, F_Grade, F_Lane_Width, F_Sh_Wid_LI, F_Sh_Wid_LO, F_Sh_Wid_RI, F_Sh_Wid_RO]
    for Field in FieldList2:
        arcpy.DeleteField_management(SiteLayer,Field['name'])
    for Field in FieldList1:
        AddField(SiteLayer, Field)
    UC = arcpy.UpdateCursor(SiteLayer)
    for URow in UC:
        FID = GetFID(URow)
        URow.setValue(F_TargetFID['name'],FID)
        UC.updateRow(URow)
    F2LDic = {SRow.getValue(F_TargetFID['name']):{'Lengths':[],'FuncClass':[], 'RouteType': [], 'TotLanes':[],'MedianID':[],'SurWid':[],'MedianWid':[],'AADT':[],'Grade':[],'Z_Mean':[],'Lane_Wid':[],'Sh_Wid_LO':[],'Sh_Wid_LI':[],'Sh_Wid_RO':[],'Sh_Wid_RI':[]} for SRow in arcpy.SearchCursor(SiteLayer)}

    arcpy.AddMessage("    Vertices to Points: Site Layer")
    V2P = VerticesToPoints(SiteLayer,'RAV2P')
    arcpy.AddMessage(arcpy.GetCount_management(V2P))

    arcpy.AddMessage("    Split Line at Points: Data Layer")
    SLP = SplitLineAtPoint(DataLayer, V2P, 'RASLP', SearchRadius)
    AddField(SLP,F_Length)
    CalField(SLP,F_Length,"!Shape!.length")
    arcpy.AddMessage(arcpy.GetCount_management(SLP))

    arcpy.AddMessage("    Buffer: Sites Layer")
    Buf = Buffer(SiteLayer, 'RABuffer', Dic = {'distance': SearchRadius, 'line_side': 'FULL', 'line_end_type': 'FLAT', 'dissolve_option': 'NONE', 'dissolve_field': '#'})
    arcpy.AddMessage(arcpy.GetCount_management(Buf))
    arcpy.DeleteField_management(Buf,'Length')

    arcpy.AddMessage("    Spatial Join: Buffer + Split Layer")
    SPJ = SpatialJoin(Buf, SLP, 'RASPJ',{'join_operation':"JOIN_ONE_TO_MANY",'join_type':"KEEP_ALL",'field_mapping':'','match_option':'CONTAINS','search_radius':'','distance_field_name':''})
    arcpy.AddMessage(arcpy.GetCount_management(SPJ))
    
    arcpy.AddMessage("    Search Cursor: SPJ Layer")
    for SRow in arcpy.SearchCursor(SPJ):
        SFID = SRow.getValue(F_TargetFID['name'])
        try:
            F2LDic[SFID]['Lengths'  ].append(float(SRow.getValue(F_Length['name'])))
            F2LDic[SFID]['FuncClass'].append(int  (SRow.getValue(F_Func_Class['name'])))
            F2LDic[SFID]['RouteType'].append(int  (SRow.getValue(F_Route_Type['name'])))
            F2LDic[SFID]['TotLanes' ].append(int  (SRow.getValue(F_TotalLanes['name'])))
            F2LDic[SFID]['MedianID' ].append(int  (SRow.getValue(F_Median_ID['name'])))
            F2LDic[SFID]['SurWid'   ].append(float(SRow.getValue(F_SurWid_Tot['name'])))
            F2LDic[SFID]['MedianWid'].append(float(SRow.getValue(F_Median_Wid['name'])))
            F2LDic[SFID]['AADT'     ].append(float(SRow.getValue(AADTField)))
            F2LDic[SFID]['Grade'    ].append(float(SRow.getValue(F_Grade['name'])))
            F2LDic[SFID]['Z_Mean'   ].append(float(SRow.getValue(F_Z_Mean['name'])))
            F2LDic[SFID]['Lane_Wid' ].append(float(SRow.getValue(F_Lane_Width['name'])))
            F2LDic[SFID]['Sh_Wid_LI'].append(float(SRow.getValue(F_Sh_Wid_LI['name'])))
            F2LDic[SFID]['Sh_Wid_LO'].append(float(SRow.getValue(F_Sh_Wid_LO['name'])))
            F2LDic[SFID]['Sh_Wid_RI'].append(float(SRow.getValue(F_Sh_Wid_RI['name'])))
            F2LDic[SFID]['Sh_Wid_RO'].append(float(SRow.getValue(F_Sh_Wid_RO['name'])))
        except:
            DoNothing = 1
            #arcpy.AddWarning(str(SFID)+': Cannot Read Attributes')


    arcpy.AddMessage("    Add Fields: Sites Layer")
    for Field in FieldList2:
        AddField(SiteLayer, Field)

    arcpy.AddMessage("    Update Cursor: Sites Layer")
    def MaxValue(Value,Weight):
        n = len(Value)
        Dic = {n:0 for n in Value}
        for i in range(0,n):
            Dic[Value[i]] += Weight[i]
        return [k for k,v in Dic.items() if v == max(Dic.values())][0]

    UC = arcpy.UpdateCursor(SiteLayer)
    for URow in UC:
        SFID = URow.getValue(F_TargetFID['name'])

        Lengths   = F2LDic[SFID]['Lengths'  ]
        FuncClass = F2LDic[SFID]['FuncClass']
        RouteType = F2LDic[SFID]['RouteType']
        TotLanes  = F2LDic[SFID]['TotLanes' ]
        MedianID  = F2LDic[SFID]['MedianID' ]
        SurWid    = F2LDic[SFID]['SurWid'   ]
        MedianWid = F2LDic[SFID]['MedianWid']
        AADT      = F2LDic[SFID]['AADT'     ]
        Grade     = F2LDic[SFID]['Grade'    ]
        Z_Mean    = F2LDic[SFID]['Z_Mean'   ]
        Lane_Wid  = F2LDic[SFID]['Lane_Wid' ]
        Sh_Wid_LI = F2LDic[SFID]['Sh_Wid_LI']
        Sh_Wid_LO = F2LDic[SFID]['Sh_Wid_LO']
        Sh_Wid_RI = F2LDic[SFID]['Sh_Wid_RI']
        Sh_Wid_RO = F2LDic[SFID]['Sh_Wid_RO']
        #arcpy.AddMessage(str([SFID,Lengths,TotLanes]))
        if len(Lengths) > 0:

            #if len(Lengths) > 1:
                #arcpy.AddMessage(' - FID: ' + str(SFID) + ', Seg(%): ' +
                #str([int(round(l/URow.getValue('Shape').length*100)) for l in
                #Lengths]))
            # Total Lanes <- Max length - Warning if differ
            if TotLanes.count(TotLanes[0]) == len(TotLanes):
                URow.setValue(F_TotalLanes['name'], TotLanes[0])
            else:
                SelTL = MaxValue(TotLanes,Lengths)
                arcpy.AddMessage('    - FID: ' + str(SFID) + ', Seg(%): ' + str([int(round(l / URow.getValue('Shape').length * 100)) for l in Lengths]))
                arcpy.AddWarning('      - Total Lanes: ' + str(TotLanes) + ', Sel: ' + str(SelTL))
                URow.setValue(F_TotalLanes['name'], SelTL)
        
            # Median ID <- Max Length - Message if differ
            if MedianID.count(MedianID[0]) == len(MedianID):
                URow.setValue(F_Median_ID['name'], MedianID[0])
            else:
                Value = []
                for ID in MedianID:
                    if ID in [1,2,4,5,6]:
                        Value.append(-1)
                    else:
                        Value.append(ID)
                SelID = MaxValue(Value,Lengths)
                if SelID == -1:
                    Value = []
                    Weight = []
                    for i in range(0,len(MedianID)):
                        if MedianID[i] in [1,2,4,5,6]:
                            Value.append(MedianID[i])
                            Weight.append(Lengths[i])
                    SelID = MaxValue(Value,Weight)
                arcpy.AddMessage('    - FID: ' + str(SFID) + ', Seg(%): ' + str([int(round(l / URow.getValue('Shape').length * 100)) for l in Lengths]))
                arcpy.AddMessage('      - Median ID: ' + str(MedianID) + ', Sel: ' + str(SelID))
                URow.setValue(F_Median_ID['name'], SelID)
            # Func Class <- Max Length
            URow.setValue(F_Func_Class['name'], MaxValue(FuncClass,Lengths))
            URow.setValue(F_Route_Type['name'], min(RouteType))
        
            # Surface Wid & Median Wid <- Max value
            URow.setValue(F_SurWid_Tot['name'], max(SurWid))
            URow.setValue(F_Median_Wid['name'], max(MedianWid))
        
            # Surface Wid & Median Wid <- Min value
            URow.setValue(F_Lane_Width['name'], MaxValue(Lane_Wid,Lengths))
            URow.setValue(F_Sh_Wid_LO['name'], MaxValue(Sh_Wid_LO,Lengths))
            URow.setValue(F_Sh_Wid_LI['name'], MaxValue(Sh_Wid_LI,Lengths))
            URow.setValue(F_Sh_Wid_RO['name'], MaxValue(Sh_Wid_RO,Lengths))
            URow.setValue(F_Sh_Wid_RI['name'], MaxValue(Sh_Wid_RI,Lengths))

            # AADT <- Waighted Average
            aadt = 0
            for i in range(0,len(Lengths)):
                aadt += Lengths[i] * AADT[i]
            aadt = round(aadt / sum(Lengths))
            URow.setValue(F_AADT['name'], aadt)

            # Grade <- Waighted Average
            grade = 0
            for i in range(0,len(Lengths)):
                grade += Lengths[i] * Grade[i]
            grade = (grade / sum(Lengths))
            URow.setValue(F_Grade['name'], grade)        

            # Z_Mean <- Waighted Average
            zmean = 0
            for i in range(0,len(Lengths)):
                zmean += Lengths[i] * Z_Mean[i]
            zmean = (zmean / sum(Lengths))
            URow.setValue(F_Z_Mean['name'], zmean)        
            
            UC.updateRow(URow)
        #else:
            #arcpy.AddWarning('    - No Matchs found for Site FID: ' + str(SFID))

    for Field in FieldList1:
        arcpy.DeleteField_management(SiteLayer,Field['name'])

    arcpy.CopyFeatures_management(SiteLayer, Output)
    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")
def ImportRIMSAttributesF2L(SiteInput,DataInput,AADTField,Output):
    arcpy.AddMessage(" ")
    arcpy.AddMessage("    Import Attributes")

    OutDic = OutputParser(Output, 'shp')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("    Copy Features: Sites Layer")
    SiteLayer = CopyFeatures(SiteInput,'AttSite')
    TotalSites = arcpy.GetCount_management(SiteLayer)
    arcpy.AddMessage("     - Total number of Items Found: " + str(TotalSites))

    arcpy.AddMessage("    Copy Features: Data Layer")
    DataLayer = CopyFeatures(DataInput,'AttData')
    TotalCMF = arcpy.GetCount_management(DataLayer)
    arcpy.AddMessage("     - Total number of Items Found: " + str(TotalCMF))

    arcpy.AddMessage("    Project: Data Layer")
    DataLayer = Project(DataLayer)

    arcpy.AddMessage("    Check Fields: Data Layer")
    FieldList1 = [F_TargetFID]
    for Field in FieldList1:
        arcpy.DeleteField_management(DataLayer,Field['name'])

    arcpy.AddMessage("    Check Fields: Sites Layer")
    FieldList2 = [F_Func_Class, F_Route_Type, F_TotalLanes, F_Median_ID, F_SurWid_Tot, F_Median_Wid, F_AADT, F_Z_Mean, F_Grade]
    for Field in FieldList2:
        arcpy.DeleteField_management(SiteLayer,Field['name'])
    for Field in FieldList1:
        AddField(SiteLayer, Field)
    UC = arcpy.UpdateCursor(SiteLayer)
    for URow in UC:
        FID = GetFID(URow)
        URow.setValue(F_TargetFID['name'],FID)
        UC.updateRow(URow)
    F2LDic = {SRow.getValue(F_TargetFID['name']):{'Lengths':[],'FuncClass':[], 'RouteType': [], 'TotLanes':[],'MedianID':[],'SurWid':[],'MedianWid':[],'AADT':[],'Grade':[],'Z_Mean':[]} for SRow in arcpy.SearchCursor(SiteLayer)}

    arcpy.AddMessage("    Feature to Line: Site Layer + Data Data")
    F2L = FeatureToLine(SiteLayer + ';' + DataLayer, "AttF2L", '')

    arcpy.AddMessage("    Search Cursor: F2L Layer")
    for SRow in arcpy.SearchCursor(F2L):
        SFID = SRow.getValue(F_TargetFID['name'])
        try:
            F2LDic[SFID]['Lengths'  ].append(float(SRow.getValue('Shape').length))
            F2LDic[SFID]['FuncClass'].append(int  (SRow.getValue(F_Func_Class['name'])))
            F2LDic[SFID]['RouteType'].append(int  (SRow.getValue(F_Route_Type['name'])))
            F2LDic[SFID]['TotLanes' ].append(int  (SRow.getValue(F_TotalLanes['name'])))
            F2LDic[SFID]['MedianID' ].append(int  (SRow.getValue(F_Median_ID['name'])))
            F2LDic[SFID]['SurWid'   ].append(float(SRow.getValue(F_SurWid_Tot['name'])))
            F2LDic[SFID]['MedianWid'].append(float(SRow.getValue(F_Median_Wid['name'])))
            F2LDic[SFID]['AADT'     ].append(float(SRow.getValue(AADTField)))
            F2LDic[SFID]['Grade'    ].append(float(SRow.getValue(F_Grade['name'])))
            F2LDic[SFID]['Z_Mean'   ].append(float(SRow.getValue(F_Z_Mean['name'])))
        except:
            DoNothing = 1
            #arcpy.AddWarning(str(SFID)+': Cannot Read Attributes')


    arcpy.AddMessage("    Add Fields: Sites Layer")
    for Field in FieldList2:
        AddField(SiteLayer, Field)

    arcpy.AddMessage("    Update Cursor: Sites Layer")
    def MaxValue(Value,Weight):
        n = len(Value)
        Dic = {n:0 for n in Value}
        for i in range(0,n):
            Dic[Value[i]] += Weight[i]
        return [k for k,v in Dic.items() if v == max(Dic.values())][0]

    UC = arcpy.UpdateCursor(SiteLayer)
    for URow in UC:
        SFID = URow.getValue(F_TargetFID['name'])

        Lengths   = F2LDic[SFID]['Lengths'  ]
        FuncClass = F2LDic[SFID]['FuncClass']
        RouteType = F2LDic[SFID]['RouteType']
        TotLanes  = F2LDic[SFID]['TotLanes' ]
        MedianID  = F2LDic[SFID]['MedianID' ]
        SurWid    = F2LDic[SFID]['SurWid'   ]
        MedianWid = F2LDic[SFID]['MedianWid']
        AADT      = F2LDic[SFID]['AADT'     ]
        Grade     = F2LDic[SFID]['Grade'    ]
        Z_Mean    = F2LDic[SFID]['Z_Mean'   ]
        if len(Lengths) > 0:

            #if len(Lengths) > 1:
                #arcpy.AddMessage(' - FID: ' + str(SFID) + ', Seg(%): ' +
                #str([int(round(l/URow.getValue('Shape').length*100)) for l in
                #Lengths]))
            # Total Lanes <- Max length - Warning if differ
            if TotLanes.count(TotLanes[0]) == len(TotLanes):
                URow.setValue(F_TotalLanes['name'], TotLanes[0])
            else:
                SelTL = MaxValue(TotLanes,Lengths)
                arcpy.AddMessage('    - FID: ' + str(SFID) + ', Seg(%): ' + str([int(round(l / URow.getValue('Shape').length * 100)) for l in Lengths]))
                arcpy.AddWarning('      - Total Lanes: ' + str(TotLanes) + ', Sel: ' + str(SelTL))
                URow.setValue(F_TotalLanes['name'], SelTL)
        
            # Median ID <- Max Length - Message if differ
            if MedianID.count(MedianID[0]) == len(MedianID):
                URow.setValue(F_Median_ID['name'], MedianID[0])
            else:
                Value = []
                for ID in MedianID:
                    if ID in [1,2,4,5,6]:
                        Value.append(-1)
                    else:
                        Value.append(ID)
                SelID = MaxValue(Value,Lengths)
                if SelID == -1:
                    Value = []
                    Weight = []
                    for i in range(0,len(MedianID)):
                        if MedianID[i] in [1,2,4,5,6]:
                            Value.append(MedianID[i])
                            Weight.append(Lengths[i])
                    SelID = MaxValue(Value,Weight)
                arcpy.AddMessage('    - FID: ' + str(SFID) + ', Seg(%): ' + str([int(round(l / URow.getValue('Shape').length * 100)) for l in Lengths]))
                arcpy.AddMessage('      - Median ID: ' + str(MedianID) + ', Sel: ' + str(SelID))
                URow.setValue(F_Median_ID['name'], SelID)
            # Func Class <- Max Length
            URow.setValue(F_Func_Class['name'], MaxValue(FuncClass,Lengths))
            URow.setValue(F_Route_Type['name'], min(RouteType))
        
            # Surface Wid & Median Wid <- Max value
            URow.setValue(F_SurWid_Tot['name'], max(SurWid))
            URow.setValue(F_Median_Wid['name'], max(MedianWid))
        
            # AADT <- Waighted Average
            aadt = 0
            for i in range(0,len(Lengths)):
                aadt += Lengths[i] * AADT[i]
            aadt = round(aadt / sum(Lengths))
            URow.setValue(F_AADT['name'], aadt)

            # Grade <- Waighted Average
            grade = 0
            for i in range(0,len(Lengths)):
                grade += Lengths[i] * Grade[i]
            grade = (grade / sum(Lengths))
            URow.setValue(F_Grade['name'], grade)        

            # Z_Mean <- Waighted Average
            zmean = 0
            for i in range(0,len(Lengths)):
                zmean += Lengths[i] * Z_Mean[i]
            zmean = (zmean / sum(Lengths))
            URow.setValue(F_Z_Mean['name'], zmean)        
            
            UC.updateRow(URow)
        #else:
            #arcpy.AddWarning('    - No Matchs found for Site FID: ' + str(SFID))

    for Field in FieldList1:
        arcpy.DeleteField_management(SiteLayer,Field['name'])

    arcpy.CopyFeatures_management(SiteLayer, Output)
    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")
def ImportAADT(SiteInput, ReadField, WriteField, DataInput, GrowthFactor, Output):
    arcpy.AddMessage(" ")
    arcpy.AddMessage("    Import Attributes")
    Threshold = 50  #Percent of difference in AADT to pop a message
    MinAADT = 4000  #Min AADT to pop a message

    OutDic = OutputParser(Output, 'shp')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("    Copy Features: Roads Layer")
    SiteLayer = CopyFeatures(SiteInput,'AADTInput')
    TotalSites = arcpy.GetCount_management(SiteLayer)
    arcpy.AddMessage("     - Total number of Items Found: " + str(TotalSites))

    arcpy.AddMessage("    Get Count: AADT Table")
    DataLayer = DataInput
    TotalCMF = arcpy.GetCount_management(DataLayer)
    arcpy.AddMessage("     - Total number of Items Found: " + str(TotalCMF))

    arcpy.AddMessage("    Search Cursor: AADT Table")
    FutDic = {SRow.getValue('maplrs'):[] for SRow in arcpy.SearchCursor(DataLayer)}
    SC = arcpy.SearchCursor(DataLayer)
    for SRow in SC:
        LA = [GetFloatVal(SRow,'BMP'),GetFloatVal(SRow,'EMP'),GetIntVal(SRow,'AADT')]
        LRSA = GetVal(SRow,'maplrs')
        FutDic[LRSA].append(LA)

    def AADTConvert(Current,Future,GFactor):
        C_BMP  = 0
        C_EMP  = 1
        C_AADT = 2
        Res = []
        for i in range(0,len(Current)):
            Curbmp = Current[i][C_BMP]
            Curemp = Current[i][C_EMP]
            bmp_ind = -1
            emp_ind = -1
            if Curbmp > Curemp:
                t = Curbmp
                Curbmp = Curemp
                Curemp = t
            AADT1 = 0
            AADT2 = 0
            for j in range(0,len(Future)):
                Futbmp = Future[j][C_BMP]
                Futemp = Future[j][C_EMP]
                if Futbmp > Futemp:
                    t = Futbmp
                    Futbmp = Futemp
                    Futemp = t
                if Curbmp >= Futbmp and Curbmp < Futemp:
                    bmp_ind = j
                    AADT1 = (Futemp-Curbmp) * Future[j][C_AADT] 
                    if Curemp < Futemp: AADT1 = (Curemp-Curbmp) * Future[j][C_AADT] 
                if Curemp > Futbmp and Curemp <= Futemp:
                    emp_ind = j
                    AADT2 = (Curemp - Futbmp) * Future[j][C_AADT] 
                    if Curbmp > Futbmp: AADT2 = (Curemp - Curbmp) * Future[j][C_AADT] 

            if AADT1 > 0 and AADT2 == 0: 
                AADT2 = Current[i][C_AADT] * GFactor * (Curemp-Future[bmp_ind][C_EMP])
            if AADT1 == 0 and AADT2 > 0: 
                AADT1 = Current[i][C_AADT] * GFactor * (Future[emp_ind][C_BMP]-Curbmp)
            
            AADT = Current[i][C_AADT] * GFactor
            if Curemp<>Curbmp: AADT = (AADT1+AADT2)/(Curemp-Curbmp)
            if bmp_ind == emp_ind: AADT = AADT / 2.0
            if AADT < Current[i][C_AADT]: AADT = Current[i][C_AADT] * GFactor
            Res.append([Curbmp,Curemp,AADT])
        return Res

    arcpy.AddMessage("    Update Cursor: Roads Layer")
    UC = arcpy.UpdateCursor(SiteLayer)
    for URow in UC:
        FID = GetFID(URow)
        LRS  = GetVal(URow,'Route_LRS')
        LS = [GetFloatVal(URow,'bmp',-1),GetFloatVal(URow,'emp',-1),GetIntVal(URow,ReadField)]
        Flag = False
        LA = []
        if LRS in FutDic.keys(): LA = FutDic[LRS]
        Res = AADTConvert([LS],LA,1.0)
        if (Res[0][2] < LS[2] * (1-Threshold/100.0) or Res[0][2] > LS[2] * (1+Threshold/100.0)) and (Res[0][2]>MinAADT or LS[2]>MinAADT):
            Flag = True
        if Flag:
            arcpy.AddMessage('     FID: %6.0f' %FID + ', Cur: ' + str(LS) + ', Res: ' + str(int(Res[0][2])) + ', Fut: ' + str(LA))
        URow.setValue(WriteField,Res[0][2])
        UC.updateRow(URow)

    arcpy.CopyFeatures_management(SiteLayer, Output)
    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")
def ResegmentAADT(SiteInput, TransferFields, DataInput, Output):
    #Resegmenting Sites with RIMS Data
    import json
    
    arcpy.AddMessage(" ")
    arcpy.AddMessage("  Import and Resegment Roads Layer")

    Threshold = 50  #Percent of difference in AADT to pop a message
    MinAADT = 4000  #Min AADT to pop a message

    OutDic = OutputParser(Output, 'shp')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("    Copy Features: Roads Layer")
    SiteLayer = CopyFeatures(SiteInput,'AADTInput')
    TotalSites = arcpy.GetCount_management(SiteLayer)
    arcpy.AddMessage("     - Total number of Items Found: " + str(TotalSites))

    arcpy.AddMessage("    Get Count: AADT Table")
    DataLayer = DataInput
    TotalCMF = arcpy.GetCount_management(DataLayer)
    arcpy.AddMessage("     - Total number of Items Found: " + str(TotalCMF))

    arcpy.AddMessage("    Search Cursor: Sites Layer")
    AllFieldList = arcpy.ListFields(SiteLayer)
    ImportFieldList = []
    for Field in AllFieldList:
        if Field.name in TransferFields:
            ImportFieldList.append(Field)
    CurDic = {SRow.getValue('Route_LRS'):{'MP':[],'Path':[],'Fields':[]} for SRow in arcpy.SearchCursor(SiteLayer)}
    SC = arcpy.SearchCursor(SiteLayer)
    for SRow in SC:
        LRSS = GetVal(SRow,'Route_LRS')
        CurDic[LRSS]['MP'].append([GetFloatVal(SRow,'bmp'),GetFloatVal(SRow,'emp'),GetIntVal(SRow,'AADT')])
        CurDic[LRSS]['Path'].append(json.loads(SRow.getValue('shape').JSON)['paths'][0])
        FL = []
        for Field in ImportFieldList:
            FL.append(SRow.getValue(Field.name))
        CurDic[LRSS]['Fields'].append(FL)


    arcpy.AddMessage("    Search Cursor: AADT Table")
    FutDic = {SRow.getValue('maplrs'):{'MP':[]} for SRow in arcpy.SearchCursor(DataLayer)}
    SC = arcpy.SearchCursor(DataLayer)
    for SRow in SC:
        LRSA = GetVal(SRow,'maplrs')
        FutDic[LRSA]['MP'].append([GetFloatVal(SRow,'BMP'),GetFloatVal(SRow,'EMP')])


    arcpy.AddMessage("   Creating Resegmented Road Layer")
    RSRoadLayer = CreateFeatureclass('RSRoad',{'geometry_type':'POLYLINE','has_m':'ENABLED','has_z':'ENABLED'})
    
    for field in [F_Route_LRS,F_BegMp,F_EndMp]:
        AddField(RSRoadLayer,field)
    for rec in ImportFieldList:
        AddField(RSRoadLayer,Field2Dic(rec))

    arcpy.AddMessage("    - Defining Projection")
    arcpy.DefineProjection_management(RSRoadLayer,CoordSystemSC)

    arcpy.AddMessage("    - Insert Cursor")
    IC = arcpy.InsertCursor(RSRoadLayer) 
    Total = 0
    for lrs in CurDic.keys():
        Flag = False
        if lrs in FutDic.keys():
                Flag = True
                Res = Resegment2(FutDic[lrs],CurDic[lrs])
        if not Flag:
            for mp in CurDic[lrs]['MP']:
                j = CurDic[lrs]['MP'].index(mp)
                IRow = IC.newRow()
                IRow.setValue(F_Route_LRS['name'],lrs)
                IRow.setValue(F_BegMp['name'],mp[0])
                IRow.setValue(F_EndMp['name'],mp[1])
                IRow.shape = arcpy.Polyline(arcpy.Array([arcpy.Point(p[0],p[1]) for p in CurDic[lrs]['Path'][j]]))
                i = 0
                for rec in ImportFieldList:
                    IRow.setValue(rec.name,CurDic[lrs]['Fields'][j][i])
                    i += 1
                IC.insertRow(IRow)             
        else:
            for mp in Res['MP']:
                j = Res['MP'].index(mp)
                IRow = IC.newRow()
                IRow.setValue(F_Route_LRS['name'],lrs)
                IRow.setValue(F_BegMp['name'],mp[0])
                IRow.setValue(F_EndMp['name'],mp[1])
                IRow.shape = arcpy.Polyline(arcpy.Array([arcpy.Point(p[0],p[1]) for p in Res['Path'][j]]))
                if len(Res['Fields'][j])>0:
                    for rec in ImportFieldList:
                        i = ImportFieldList.index(rec)
                        IRow.setValue(rec.name,Res['Fields'][j][i])
                IC.insertRow(IRow)             

    arcpy.AddMessage("    - Sort")
    RSSortRoad = Sort(RSRoadLayer, 'RSSortRoad', "Route_LRS ASCENDING;BegMp ASCENDING")

    Output = arcpy.CopyFeatures_management(RSSortRoad,Output)

    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")
def RoadwayType(RoadsLayer,Output):
    arcpy.AddMessage(" ")
    arcpy.AddMessage("   Add Roadway Type/Buffer")

    OutDic = OutputParser(Output, 'shp')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("   Copy Features: Roads Layer")
    temp = CopyFeatures(RoadsLayer,'Temp_RoadsType')
    temp = MakeFeatureLayer(temp, "Temp_RoadsLayer")

    arcpy.AddMessage("   Add Fields: Roads Layer")
    CrashTypeDic = [F_RBuffer, F_FType]
    for Field in CrashTypeDic:
        AddField(temp,Field)

    arcpy.AddMessage("   Calculate Fields: Roads Layer")
    CodeBlock = """def fval(Rural, Urban, TotLanes, MedianType, RoadType,EXR,ENR):
        S1 = 'U'
        if Rural == 1:
            S1 = 'R'

        S2 = str(int(TotLanes))
        if TotLanes in [3,5,7] and MedianType in [3] and Rural == 1:
            S2 = str(int(TotLanes-1))
        if TotLanes in [2,4,6] and MedianType in [3] and Urban == 1:
            S2 = str(int(TotLanes+1))
        if TotLanes in [3,5,7,9] and RoadType == 1:
            S2 = str(int(TotLanes-1))

        S3 = 'U'
        if MedianType in [1,2,3,4,5,6]:
            S3 = 'D'
        if Urban == 1 and MedianType in [3]:
            S3 = 'T'
        if RoadType == 1:
            S3 = 'F'
        if RoadType == 9:
            S3 = 'L'
        if MedianType in [8]:
            S3 = 'O'
        if RoadType in[5,6]:
            if EXR == 1 and ENR == 0:
                S3 = 'EXR'
            if ENR == 1 and EXR == 0:
                S3 = 'ENR'
            if ENR == 1 and EXR == 1:
                S3 = 'IR'
            if ENR == 0 and EXR == 0:
                S3 = 'OR'
        return S1+S2+S3 """
    CalField(temp,F_FType,"fval(!" + F_RURAL['name'] + "!, !" + F_URBAN['name'] + "!, !" + F_TotalLanes['name'] + "!, !" + F_Median_ID['name'] + "!, !" + F_Route_Type['name'] + "!, !EX_RAMP!, !EN_RAMP!)",CodeBlock)


    CodeBlock = """def fval(Median,Surf,Totallanes,ShWLI,ShWLO,ShWRI,ShWRO,DirePoly,Oneway):
        Offcenter = 12
        Expansion = 1.20
        Minbuffer = (12/2+6)*Expansion+Offcenter
        if ShWLI<6: ShWLI=6
        if ShWLO<6: ShWLO=6
        if ShWRI<6: ShWRI=6
        if ShWRO<6: ShWRO=6
        if Surf<Totallanes*12:Surf=Totallanes*12    
        if DirePoly == 0:
            out =  (0.5 * (Surf + Median) + max(ShWLO,ShWRO)) * Expansion + Offcenter
        if DirePoly == 1:    
            out =  0.25 * Surf + max(ShWRO,ShWRI) * Expansion + Offcenter
            if Oneway == 1:
                out =  0.25 * Surf + max(ShWLO,ShWLI) * Expansion + Offcenter
        if out<Minbuffer:out = Minbuffer
        return out"""
    CalField(temp,F_RBuffer,"fval(!" + F_Median_Wid['name'] + "!, !" + F_SurWid_Tot['name'] + "!, !" + F_TotalLanes['name'] + "!, !" + F_Sh_Wid_LI['name'] + "!, !" + F_Sh_Wid_LO['name'] + "!, !" + F_Sh_Wid_RI['name'] + "!, !" + F_Sh_Wid_RO['name'] + "!, !" + F_DirePoly['name'] + "!, !" + F_Oneway['name'] + "!)",CodeBlock)


    arcpy.CopyFeatures_management(temp, Output)

    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")
def DecodeHighways(SiteInput,Output):
    arcpy.AddMessage(" ")
    arcpy.AddMessage("    Decode Fields")

    OutDic = OutputParser(Output, 'shp')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("    Copy Features: Roads Layer")
    SiteLayer = CopyFeatures(SiteInput,'AADTInput')
    TotalSites = arcpy.GetCount_management(SiteLayer)
    arcpy.AddMessage("     - Total number of Items Found: " + str(TotalSites))
    
    TempF = F_OC_FIDs; TF = F_Route_Type
    AddField(SiteLayer,TempF)
    CalField(SiteLayer,TempF,'!'+TF['name']+'!')
    arcpy.DeleteField_management(SiteLayer,TF['name'])
    CB = '''def fval(x):
        y=15
        if x in ['I-','1',1]:y=1
        if x in ['US','2',2]:y=2
        if x in ['SC','4',4]:y=4
        if x in ['R-','5',5]:y=5
        if x in ['RS','6',6]:y=6
        if x in ['S-','S','','7',7]:y=7
        if x in ['D-','99',99,14]:y=14
        return(y)'''
    AddField(SiteLayer,TF)
    CalField(SiteLayer,TF,'fval(!'+TempF['name']+'!)',CB)
    arcpy.DeleteField_management(SiteLayer,TempF['name'])

    TempF = F_OC_FIDs; TF = F_Route_Numb
    AddField(SiteLayer,TempF)
    CalField(SiteLayer,TempF,'!'+TF['name']+'!')
    arcpy.DeleteField_management(SiteLayer,TF['name'])
    AddField(SiteLayer,TF)
    CalField(SiteLayer,TF,'(!'+TempF['name']+'!)')
    arcpy.DeleteField_management(SiteLayer,TempF['name'])
        
    RF = 'ROUTE_DIR'; WF = F_Route_Dire
    AddField(SiteLayer,WF)
    CalField(SiteLayer,WF,'!'+RF+'!')
    arcpy.DeleteField_management(SiteLayer,RF)

    RF = 'BEG_MILEPO'; WF = F_BegMp
    AddField(SiteLayer,WF)
    CalField(SiteLayer,WF,'!'+RF+'!')
    arcpy.DeleteField_management(SiteLayer,RF)

    RF = 'END_MILEPO'; WF = F_EndMp
    AddField(SiteLayer,WF)
    CalField(SiteLayer,WF,'!'+RF+'!')
    arcpy.DeleteField_management(SiteLayer,RF)

    SiteLayer = arcpy.Sort_management(SiteLayer, 'HDSort', F_Route_Type['name'] + ' ASCENDING;' + F_Route_Numb['name'] + ' ASCENDING;' + F_Route_Dire['name'] + ' ASCENDING;' + F_BegMp['name'] +' ASCENDING;' + F_EndMp['name'] +' ASCENDING', spatial_sort_method="UR")

    arcpy.CopyFeatures_management(SiteLayer, Output)
    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")
def CopyOppDirection(SiteInput,RType,Output):

    arcpy.AddMessage(" ")
    arcpy.AddMessage("    Copy Opposite Direction")
    RType = int(RType)
    OutDic = OutputParser(Output, 'shp')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("    Copy Features: Roads Layer")
    SiteLayer = CopyFeatures(SiteInput,'AADTInput')
    TotalSites = arcpy.GetCount_management(SiteLayer)
    arcpy.AddMessage("     - Total number of Items Found: " + str(TotalSites))
    SiteLayer = MakeFeatureLayer(SiteLayer,'COLayer')

    arcpy.AddMessage("    Calculate Dissolve ID")
    arcpy.SelectLayerByAttribute_management(SiteLayer,"NEW_SELECTION",""""ROUTE_TYPE" = """ + str(RType) + """ AND "DIREPOLY" = 1""")
    AddField(SiteLayer,F_TargetFID)
    if RType==1:
        arcpy.CalculateField_management(SiteLayer,F_TargetFID['name'],'[ROUTE_NUMB]','VB')
    if RType in [2,4]:
        arcpy.CalculateField_management(SiteLayer,F_TargetFID['name'],"[COUNTY] & [ROUTE_NUMB]",'VB')

    arcpy.AddMessage("    Copy Opposite Direction")
    arcpy.SelectLayerByAttribute_management(SiteLayer,"NEW_SELECTION",""""ROUTE_TYPE" = """ + str(RType) + """ AND "DIREPOLY" = 1 AND "ONEWAY" = 1 """)
    ONE1 = CopyFeatures(SiteLayer,'ONE1')
    TotalSites = arcpy.GetCount_management(ONE1)
    arcpy.AddMessage("     - Total number of Oneway == 1 Found: " + str(TotalSites))

    arcpy.AddMessage("    Dissolve: Oneway = 1")
    ONE1Diss = Dissolve(ONE1,'ONE1Diss',F_TargetFID['name'])
    One1L = {r.getValue(F_TargetFID['name']):r.getValue('Shape_Length') for r in arcpy.SearchCursor(ONE1Diss)}
    One1D = {r.getValue(F_TargetFID['name']):r.getValue('Shape') for r in arcpy.SearchCursor(ONE1Diss)}

    arcpy.SelectLayerByAttribute_management(SiteLayer,"NEW_SELECTION",""""ROUTE_TYPE" =""" + str(RType) + """ AND "DIREPOLY" = 1 AND "ONEWAY" = 0 """)
    ONE0 = CopyFeatures(SiteLayer,'ONE0')
    TotalSites = arcpy.GetCount_management(ONE0)
    arcpy.AddMessage("     - Total number of Oneway == 0 Found: " + str(TotalSites))

    arcpy.AddMessage("    Dissolve: Oneway = 0")
    ONE0Diss = Dissolve(ONE0,'ONE0Diss',F_TargetFID['name'])
    One0L = {r.getValue(F_TargetFID['name']):r.getValue('Shape_Length') for r in arcpy.SearchCursor(ONE0Diss)}
    Mult = {RTN:One1L[RTN]/One0L[RTN] for RTN in One0L.keys()}

    arcpy.AddMessage("    Search Cursor: Read Data")
    LDic = {R.getValue(F_TargetFID['name']):[] for R in arcpy.SearchCursor(ONE0)}
    SC = arcpy.SearchCursor(ONE0)
    for r in SC:
        RTN = r.getValue(F_TargetFID['name'])
        LDic[RTN].append({'Polyline':r.getValue('Shape'),'County':r.getValue('COUNTY'),'RTN':r.getValue('ROUTE_NUMB'),'DissID':r.getValue('DissolveID'),
                          'MP':[r.getValue('bmp'),r.getValue('emp')],
                          'AADT':[r.getValue('AADT10'),r.getValue('AADT11'),r.getValue('AADT12'),r.getValue('AADT13'),r.getValue('AADT14')],
                          'Lanes':[r.getValue('L_Lanes'),r.getValue('R_Lanes'),r.getValue('TotalLanes'),r.getValue('Lane_Width')],
                          'Func_Class':r.getValue('Func_Class'),
                          'Median':[r.getValue('Median_ID'),r.getValue('Rt_Divided'),r.getValue('Median_Wid')],
                          'Surface':[r.getValue('L_Sur_W'),r.getValue('R_Sur_W'),r.getValue('SurWid_Tot')],
                          'Shoulder':[r.getValue('Sh_Wid_LI'),r.getValue('Sh_Wid_LO'),r.getValue('Sh_Wid_RI'),r.getValue('Sh_Wid_RO')],
                          'ShoulderTrt':[r.getValue('L_SH_TRT'),r.getValue('RT_SH_TRT'),r.getValue('SH_TRT_1'),r.getValue('SH_TRT_2')],
                          'SideWTrt':[r.getValue('SW_TRT_1'),r.getValue('SW_TRT_2')],
                          'Curb':[r.getValue('L_OUTS_CRB'),r.getValue('R_INS_CRB'),r.getValue('R_OUT_CRB')],
                          'Unknowns':[r.getValue('SUB_PSUR_L'),r.getValue('SUBPHSUR_L'),r.getValue('SUB_PVSU_R')],
                          'Z_Mean':[r.getValue('Z_Mean'),r.getValue('AVG_SLOPE')]})

    arcpy.AddMessage("    Insert Cursor: Write Fields")
    temp = SpatialJoin(ONE1Diss,ONE1,'SPJ1')
    arcpy.DeleteRows_management(temp)
    arcpy.DeleteField_management(temp,"Join_Count;TARGET_FID")
    i = 0
    UC = arcpy.InsertCursor(temp)
    for RTN in LDic.keys():
        l0 = 0
        for Res in LDic[RTN]:
            l1 = l0 + Res['Polyline'].length * Mult[RTN]
            pl = One1D[RTN].segmentAlongLine(l0,l1)
            l0 = l1
            r = UC.newRow()
            r.setValue('ROUTEFID',i)
            r.setValue('DissolveID',Res['DissID'])
            i = i + 1
            r.Shape = pl
            r.setValue('LENGTH',pl.length)
            r.setValue('LEN_MILE',pl.length/5280)
            r.setValue('ROUTE_TYPE',RType)
            r.setValue('EN_RAMP',0)
            r.setValue('EX_RAMP',0)
            r.setValue('DIREPOLY',1)
            r.setValue('ROUTE_NUMB',Res['RTN'])
            r.setValue('ONEWAY',1)
            r.setValue('COUNTY',Res['County'])
            r.setValue('EMP',Res['MP'][1])
            r.setValue('BMP',Res['MP'][0])
            r.setValue('EMP',Res['MP'][1])
            r.setValue('AADT10',Res['AADT'][0])
            r.setValue('AADT11',Res['AADT'][1])
            r.setValue('AADT12',Res['AADT'][2])
            r.setValue('AADT13',Res['AADT'][3])
            r.setValue('AADT14',Res['AADT'][4])
            r.setValue('L_Lanes',Res['Lanes'][0])
            r.setValue('R_Lanes',Res['Lanes'][1])
            r.setValue('TotalLanes' ,Res['Lanes'][2])
            r.setValue('Lane_Width',Res['Lanes'][3])
            r.setValue('Func_Class',Res['Func_Class'])
            r.setValue('Median_ID' ,Res['Median'][0])
            r.setValue('Rt_Divided',Res['Median'][1])
            r.setValue('Median_Wid',Res['Median'][2])
            r.setValue('L_Sur_W'   ,Res['Surface'][0])
            r.setValue('R_Sur_W'   ,Res['Surface'][1])
            r.setValue('SurWid_Tot',Res['Surface'][2])
            r.setValue('Sh_Wid_LI',Res['Shoulder'][0])
            r.setValue('Sh_Wid_LO',Res['Shoulder'][1])
            r.setValue('Sh_Wid_RI',Res['Shoulder'][2])
            r.setValue('Sh_Wid_RO',Res['Shoulder'][3])
            r.setValue('Z_Mean',Res['Z_Mean'][0])
            r.setValue('AVG_SLOPE',Res['Z_Mean'][1])
            r.setValue('L_SH_TRT',Res['ShoulderTrt'][0])
            r.setValue('RT_SH_TRT',Res['ShoulderTrt'][1])
            r.setValue('SH_TRT_1',Res['ShoulderTrt'][2])
            r.setValue('SH_TRT_2',Res['ShoulderTrt'][3])
            r.setValue('SW_TRT_1',Res['SideWTrt'][0])
            r.setValue('SW_TRT_2',Res['SideWTrt'][1])
            r.setValue('L_OUTS_CRB',Res['Curb'][0])
            r.setValue('R_INS_CRB',Res['Curb'][1])
            r.setValue('R_OUT_CRB',Res['Curb'][2])
            r.setValue('SUB_PSUR_L',Res['Unknowns'][0])
            r.setValue('SUBPHSUR_L',Res['Unknowns'][1])
            r.setValue('SUB_PVSU_R',Res['Unknowns'][2])
            UC.insertRow(r)

    
    arcpy.AddMessage("   Update Cursor & Spatil Join: Route LRS")
    SPJ = SpatialJoin(temp,ONE1,'SPJS')
    SPJDic = {r.getValue('ROUTEFID'):{'LRS':r.getValue('ROUTE_LRS_1'),'DIRE':r.getValue('ROUTE_DIRE_1')} for r in arcpy.SearchCursor(SPJ)}
    UC = arcpy.UpdateCursor(temp)
    for r in UC:
        FID = r.getValue('ROUTEFID')
        r.setValue('ROUTE_LRS',SPJDic[FID]['LRS'])
        r.setValue('ROUTE_DIRE',SPJDic[FID]['DIRE'])
        UC.updateRow(r)

    arcpy.AddMessage("   Merge: Replace the Opposite Direction")
    arcpy.SelectLayerByAttribute_management(SiteLayer,"NEW_SELECTION",""""ROUTE_TYPE" = """ + str(RType) + """ AND "DIREPOLY" = 1 AND "ONEWAY" = 1 """)
    arcpy.SelectLayerByAttribute_management(SiteLayer,"SWITCH_SELECTION")
    Mtemp = Merge([SiteLayer,temp],'Merge')
    
    arcpy.AddMessage("   Sort")
    Mtemp = MakeFeatureLayer(Mtemp,'MtempLayer')
    arcpy.SelectLayerByAttribute_management(Mtemp,"NEW_SELECTION",""""ROUTE_TYPE" = 1""")
    Stemp1 = Sort(Mtemp,'Sa','ROUTE_TYPE;ROUTE_NUMB;ROUTE_DIRE;BMP;COUNTY')
    arcpy.SelectLayerByAttribute_management(Mtemp,"NEW_SELECTION",""""ROUTE_TYPE" IN (2,4)""")
    Stemp2 = Sort(Mtemp,'Sb','ROUTE_TYPE;ROUTE_NUMB;COUNTY;ROUTE_DIRE;BMP')
    arcpy.SelectLayerByAttribute_management(Mtemp,"NEW_SELECTION",""""ROUTE_TYPE" IN (5,6,7,9,14)""")
    Stemp3 = Sort(Mtemp,'Sc','ROUTE_TYPE;COUNTY;ROUTE_NUMB;ROUTE_DIRE;BMP')
    
    Ftemp = Merge([Stemp1,Stemp2,Stemp3],'FMerge')
    arcpy.DeleteField_management(Ftemp,'Target_FID;Target_FID_1;Shape_Length_1')
    arcpy.CopyFeatures_management(Ftemp, Output)
    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")
def CreateNetwork_old(RIMSInput,HighwaysInput,DEM,Output):
    arcpy.AddMessage(" ")
    arcpy.AddMessage("  Create Network")
    import json
    OutDic = OutputParser(Output, 'mdb')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("  Copy Features: RIMS Layer")
    SiteLayer = CopyFeatures(RIMSInput,'CNRInput')
    TotalSites = arcpy.GetCount_management(SiteLayer)
    arcpy.AddMessage("   - Total number of Items Found: " + str(TotalSites))
    SiteLayer = MakeFeatureLayer(SiteLayer,'COLayer')

    arcpy.AddMessage("  Copy Features: Highways Layer")
    HighLayer = CopyFeatures(HighwaysInput,'CNHInput')
    TotalSites = arcpy.GetCount_management(HighLayer)
    arcpy.AddMessage("   - Total number of Items Found: " + str(TotalSites))
    HighLayer = MakeFeatureLayer(HighLayer,'CHLayer')

    arcpy.SelectLayerByAttribute_management(SiteLayer,'NEW_SELECTION',"ROUTE_TYPE in (1,2,4,7)")
    RCT1R = CopyFeatures(SiteLayer,'RCT1R')

    arcpy.SelectLayerByAttribute_management(HighLayer,'NEW_SELECTION',""""ROUTE_TYPE" in (1,2,4,7)""")
    RCT1H = CopyFeatures(HighLayer,'RCT1H')

    arcpy.AddMessage("   - Add Fields")

    AddField(RCT1R,F_Name)
    CalField(RCT1R,F_Name,"!Route_LRS!")
    Oneway0 = {Row.getValue(F_Name['name']):0 for Row in arcpy.SearchCursor(RCT1R)}
    Oneway0 = Oneway0.keys()

    AddField(RCT1H,F_Name)
    CalField(RCT1H,F_Name,"!ROUTE_LRS!")
 
    arcpy.AddMessage("   - Search Cursor")
    MPDict = {Row.getValue(F_Name['name']):{'SegL':[],'Route':[]} for Row in arcpy.SearchCursor(RCT1R)}
    for Row in arcpy.SearchCursor(RCT1R):
        MPDict[Row.getValue(F_Name['name'])]['SegL'].append(Row.getValue('Shape'))

    def EqualPnts(P1,P2):
        if P1.X == P2.X and P1.Y == P2.Y:
            return True
        else:
            return False
    def ComparePointDict(P1,P2):
        if P1['X']==P2['X'] and P1['Y']==P2['Y']:
            return True
        else:
            return False

    arcpy.env.MTolerance  = 0.0001
    arcpy.env.MResolution = 0.0000001
    arcpy.env.ZTolerance  = "0.1 Feet"
    arcpy.env.ZResolution = "0.1 Feet"
    RCT1N = CreateFeatureclass('RCT1N',{'geometry_type':'POLYLINE','has_m':'ENABLED','has_z':'ENABLED'})
    arcpy.DefineProjection_management(RCT1N,CoordSystemSC)
    for field in [F_Name, F_County, F_Route_Type,F_Route_Numb,F_Route_Aux,F_Route_Dire,F_BegMp,F_EndMp, F_Oneway,F_DirePoly,F_DissolveID]:
        AddField(RCT1N,field)
    IC = arcpy.InsertCursor(RCT1N)
    for rn in MPDict.keys():
        #arcpy.AddMessage(str(rn))
        PartL = []
        PointL = []
        for seg in MPDict[rn]['SegL']:
            for prt in json.loads(seg.JSON)['paths']:
                PartL.append(prt)
        for prt in PartL:
            for pnt in prt:
                b = False
                if prt.index(pnt) == 0: b = True
                PointL.append({'X':pnt[0],'Y':pnt[1],'M':pnt[2],'PrtNum':PartL.index(prt),'BegPnt':b})
        for pnt in PointL:
            if pnt['BegPnt']:
                for prt in PartL:
                    if ComparePointDict({'X':prt[-1][0],'Y':prt[-1][1]},pnt) and PartL.index(prt)<>pnt['PrtNum']:
                        pnt['BegPnt'] = False

        BegPntD = {pnt['M']:pnt for pnt in PointL if pnt['BegPnt']}
        if len(BegPntD.keys())==0:
            m = min([pnt['M'] for pnt in PointL])
            for pnt in PointL:
                if pnt['M']==m:
                    pnt['BegPnt'] = True
                    BegPntD = {pnt['M']:pnt for pnt in PointL if pnt['BegPnt']}
        MKeys = BegPntD.keys()
        MKeys.sort()
        Route = []
        Parts = []
        for m in MKeys:
            RoutePart = [BegPntD[m]]
            for pnt in PartL[BegPntD[m]['PrtNum']][1:]:
                RoutePart.append({'X':pnt[0],'Y':pnt[1],'M':pnt[2],'PrtNum':BegPntD[m]['PrtNum'],'BegPnt':False})
            #arcpy.AddMessage(str([RoutePart[-1]]))
            Parts.append(PartL[BegPntD[m]['PrtNum']])
            NextPart = [prt for prt in PartL if ComparePointDict(RoutePart[-1],{'X':prt[0][0],'Y':prt[0][1]}) and not prt in Parts]
            while len(NextPart)>0:
                Parts.append(NextPart[0])
                for pnt in NextPart[0][1:]:
                    #arcpy.AddMessage(str(len(RoutePart)))
                    RoutePart.append({'X':pnt[0],'Y':pnt[1],'M':pnt[2],'PrtNum':PartL.index(NextPart[0]),'BegPnt':False})
                #arcpy.AddMessage(str([RoutePart[-1]]))
                NextPart = [prt for prt in PartL if ComparePointDict(RoutePart[-1],{'X':prt[0][0],'Y':prt[0][1]}) and not prt in Parts]
            Route.append(RoutePart)
        #MPDict[rn]['Route'] = Route
        IRow = IC.newRow() 
        IRow.setValue(F_Name['name'],rn)
        IRow.setValue(F_Oneway['name'],0)
        Arr = arcpy.Array()
        for prt in Route:
            a = arcpy.Array()
            i = 0
            for pnt in prt:
                i += 1
                p = arcpy.Point(pnt['X'],pnt['Y'],0,pnt['M'],i)
                a.add(p)
            Arr.add(a)
        pl = arcpy.Polyline(Arr,CoordSystemSC,True,True)
        IRow.shape = pl
        IC.insertRow(IRow)           
        #arcpy.AddMessage(str([len(MPDict[rn]['SegL']),len(Route)]))  
    del IC

    arcpy.AddMessage("   - Import Z Values")
    RCT1Z = arcpy.InterpolateShape_3d(DEM, RCT1N, 'RCT1Z', sample_distance="1000", z_factor="1", method="BILINEAR", vertices_only="VERTICES_ONLY", pyramid_level_resolution="0")
    SC = arcpy.SearchCursor(RCT1Z)
    for SRow in SC:
        rn = SRow.getValue(F_Name['name'])
        ZRoute = []
        Pl = SRow.getValue('Shape')
        for prt in Pl:
            ZPart = []
            for pnt in prt:
                ZPart.append(pnt.Z)
            ZRoute.append(ZPart)
        MPDict[rn].update({'z' : ZRoute})
    #arcpy.Delete_management(RCT1Z)
    UC = arcpy.UpdateCursor(RCT1N)
    for URow in UC:
        rn = URow.getValue(F_Name['name'])
        Pl = URow.getValue('Shape')
        n = len(Pl)
        RouteArr = arcpy.Array()
        for i in range(0,n):
            PartArr = arcpy.Array()
            m = len(Pl[i])
            for j in range(0,m):
                pnt = arcpy.Point()
                pnt.X = Pl[i][j].X
                pnt.Y = Pl[i][j].Y
                pnt.Z = MPDict[rn]['z'][i][j]
                pnt.M = Pl[i][j].M
                PartArr.add(pnt)
            RouteArr.add(PartArr)
        Pl = arcpy.Polyline(RouteArr,CoordSystemSC,True,True)
        #arcpy.AddMessage(str(MPDict[rn]['z'][0]))
        #arcpy.AddMessage(str(Pl[0][0]))
        URow.shape = arcpy.Polyline(RouteArr,CoordSystemSC,True,True)
        UC.updateRow(URow)

    CalField(RCT1N,F_County    ,'!'+F_Name['name']+'![0:2]')
    CalField(RCT1N,F_Route_Type,'!'+F_Name['name']+'![2:4]')
    CalField(RCT1N,F_Route_Numb,'!'+F_Name['name']+'![4:9]')
    CalField(RCT1N,F_Route_Aux ,'!'+F_Name['name']+'![9:11]')
    CalField(RCT1N,F_Route_Dire,'!'+F_Name['name']+'![-1]')
    CalField(RCT1N,F_BegMp,'!Shape!.firstPoint.M')
    CalField(RCT1N,F_EndMp,'!Shape!.lastPoint.M')
    CalField(RCT1N,F_DirePoly,1)
    RCT1S = Sort(RCT1N,'RCT1S',F_Route_Type['name']+';'+F_County['name']+';'+F_Route_Numb['name']+';'+F_Route_Dire['name'])
    arcpy.Delete_management(RCT1N)
def CreateNetwork(RIMSInput,HighwaysInput,CountyInput,DEM,Output):

    arcpy.AddMessage(" ")
    arcpy.AddMessage("  Create Network")
    import json
    OutDic = OutputParser(Output, 'mdb')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("  Copy Features: Highways Layer")
    SiteLayer = CopyFeatures(HighwaysInput,'CNHInput')
    TotalSites = arcpy.GetCount_management(SiteLayer)
    arcpy.AddMessage("   - Total number of Items Found: " + str(TotalSites))
    SiteLayer = MakeFeatureLayer(SiteLayer,'CNHLayer')

    arcpy.AddMessage("  Add Fields")
    AddField(SiteLayer,F_RouteLRSID)
    AddField(SiteLayer,F_Name)
    AddField(SiteLayer,F_RouteFID)
    CalField(SiteLayer,F_RouteFID,'!OBJECTID!')
    CalField(SiteLayer,F_RouteLRSID,'!ROUTE_NUMB!')

    arcpy.SelectLayerByAttribute_management(SiteLayer,'NEW_SELECTION',""""COUNTY_ID"<1 OR "COUNTY_ID">46""")
    SiteLayerNC = CopyFeatures(SiteLayer,'NC')
    
    arcpy.SelectLayerByAttribute_management(SiteLayer,'CLEAR_SELECTION')
    arcpy.DeleteField_management(SiteLayerNC,'COUNTY_ID')

    arcpy.AddMessage("  Spatial Join: Site Layer + County")
    SPJ = SpatialJoin(SiteLayerNC,CountyInput,'SPJCnty',{'join_operation':"JOIN_ONE_TO_ONE",'join_type':"KEEP_ALL",'field_mapping':'','match_option':'INTERSECT','search_radius':0,'distance_field_name':''})
    SPJDict = {SRow.getValue(F_RouteFID['name']):SRow.getValue('COUNTY_ID') for SRow in arcpy.SearchCursor(SPJ)}
    arcpy.Delete_management(SPJ)
    arcpy.Delete_management(SiteLayerNC)

    UC = arcpy.UpdateCursor(SiteLayer)
    for URow in UC:
        if URow.getValue('COUNTY_ID') not in range(1,47):
            URow.setValue('COUNTY_ID',SPJDict[URow.getValue(F_RouteFID['name'])])
            UC.updateRow(URow)
    del UC

    def FindDirection(FP,LP):
        x = LP.X - FP.X
        y = LP.Y - LP.Y
        if x > 0:
            if y>=x:return('N')
            if y<x and y>-x: return('E')
            if y<=-x:return('S')
        if x==0:
            if y>=x: return('N')
            if y<x:return('S')
        if x < 0:
            if y>=-x:return('N')
            if y<-x and y>x: return('W')
            if y<=x:return('S')
    RouteTypeDict = {'I-':1,'US':2,'SC':4,'R-':5,'RS':6,'S':7,'S-':7,'L-':9,'UD':9,'D-':14,'':14}
    AuxDict = {'SUM': 1,
'ALT': 2,
'MLC': 3,
'BUC': 4,
'SPR': 5,
'CON': 6,
'BUS': 7,
'BYP': 8,
'PRO': 9,
'1O1': 10,
'1O2': 11,
'1O3': 12,
'1E1': 14,
'1E2': 15,
'1E3': 16,
'2O1': 18,
'2O2': 19,
'2O3': 20,
'2E1': 22,
'2E2': 23,
'2E3': 24,
'3O1': 26,
'3O2': 27,
'3O3': 28,
'3E1': 30,
'3E2': 31,
'3E3': 32,
'4O1': 34,
'4O2': 35,
'4O3': 36,
'4E1': 38,
'4E2': 39,
'4E3': 40,
'OD1': 41,
'OD2': 42,
'OD3': 43,
'OD4': 44,
'CE4': 45,
'BU1': 48,
'BU2': 49,
'CO1': 50,
'CO2': 52,
'DC1': 53,
'DC2': 54,
'DC3': 55,
'DC4': 56,
'DC5': 57,
'DC6': 58,
'DC7': 59,
'DC8': 60,
'DC9': 61,
'DS1': 62,
'DS2': 63,
'DS3': 64,
'DS4': 65,
'DS5': 66,
'DS6': 67,
'DS7': 68,
'DS8': 69,
'DS9': 70,
'DR1': 71,
'DR2': 72,
'DR3': 73,
'DR4': 74,
'DR5': 75,
'DR6': 76,
'DR7': 77,
'DR8': 78,
'DR9': 79,
'RMP': 80,
'SVC': 81,
'OTH': 82,
'OD5': 83,
'OD6': 84,
'OD7': 85,
'SD4': 90,
'SD1': 91,
'SD2': 92,
'SD3': 93,
'CE1': 94,
'CE2': 95,
'CE3': 96,
'CH1': 97,
'CH2': 98,
'CH3': 99}
    arcpy.AddMessage("  Update Cursor")
    CDict     = {i:0 for i in range(1,47)}
    RNumbDict = {i:{} for i in range(1,47)}
    for SRow in arcpy.SearchCursor(SiteLayer):
        County = SRow.getValue('COUNTY_ID')
        RName  = SRow.getValue('STREET_NAM')
        if not RName in RNumbDict[County].keys():
            RNumbDict[County].update({RName:SRow.getValue('ROUTE_NUMB')})

    UC = arcpy.UpdateCursor(SiteLayer)
    for URow in UC:
        Cnty = URow.getValue('COUNTY_ID')

        rt = URow.getValue('ROUTE_TYPE')
        if rt in RouteTypeDict.keys():
            rt = RouteTypeDict[rt]
        else:
            rt = 14
        URow.setValue('ROUTE_TYPE',rt)
        
        rn = URow.getValue('ROUTE_NUMB')
        if rn == 0:
            sn = URow.getValue('STREET_NAM')
            if sn == '':
                CDict[Cnty] += 1
                while CDict[Cnty] in RNumbDict[Cnty].values():
                    CDict[Cnty] += 1
                rn = CDict[Cnty]
            else:
                CDict[Cnty] += 1
                while CDict[Cnty] in RNumbDict[Cnty].values():
                    CDict[Cnty] += 1
                RNumbDict[Cnty][sn] = CDict[Cnty]
                rn = CDict[Cnty]
        URow.setValue(F_RouteLRSID['name'],rn)

        dir = URow.getValue('ROUTE_DIR')
        if not dir in ['N','E','W','S']:
            dir = FindDirection(URow.getValue('Shape').firstPoint,URow.getValue('Shape').lastPoint)
            URow.setValue('ROUTE_DIR',dir)
        
        aux = URow.getValue('ROUTE_AUX')
        if aux in AuxDict.keys():
            aux = AuxDict[aux]
        else:
            aux = 0
        URow.setValue('ROUTE_AUX',aux)

        oneway = URow.getValue('ONEWAY')
        if oneway == 0:
            dir = 'T'
        n = '{:02.0f}{:02.0f}{:05.0f}{:02.0f}{}'.format(Cnty,rt,rn,aux,dir)
        #arcpy.AddMessage(n)
        URow.setValue(F_Name['name'],n)

        UC.updateRow(URow)
    del UC
    
    arcpy.AddMessage("  Search Cursor")
    MPDict = {Row.getValue(F_Name['name']):{'SegL':[],'Oneway':[],'BMP':[],'Len':0,'Z':[],'RouteID':'','RouteName':'','LRS':''} for Row in arcpy.SearchCursor(SiteLayer)}
    for Row in arcpy.SearchCursor(SiteLayer):
        rn = Row.getValue(F_Name['name'])
        MPDict[rn]['SegL'     ].append(json.loads(Row.getValue('Shape').JSON)['paths'])
        MPDict[rn]['Oneway'   ].append(Row.getValue('ONEWAY'))
        MPDict[rn]['BMP'      ].append(Row.getValue('BEG_MILEPO'))
        MPDict[rn]['RouteID'  ] = Row.getValue('ROUTE_ID')
        MPDict[rn]['RouteName'] = Row.getValue('STREET_NAM')
        MPDict[rn]['LRS'      ] = Row.getValue('ROUTE_LRS')
    SiteLayer = CopyFeatures(SiteLayer,'SCC')
    arcpy.AddMessage("  Interpolate Shape 3D")
    RCT1Z = arcpy.InterpolateShape_3d(DEM, SiteLayer, 'RCT1Z', sample_distance="800", z_factor="1", method="BILINEAR", vertices_only="VERTICES_ONLY", pyramid_level_resolution="0")
    SC = arcpy.SearchCursor(RCT1Z)
    for SRow in SC:
        rn = SRow.getValue(F_Name['name'])
        #arcpy.AddMessage(rn)
        ZRoute = []
        Pl = SRow.getValue('Shape')
        for prt in Pl:
            ZPart = []
            for pnt in prt:
                ZPart.append(pnt.Z)
            ZRoute.append(ZPart)
        #arcpy.AddMessage(rn)
        MPDict[rn]['Z'].append(ZRoute)
    arcpy.Delete_management(RCT1Z)

    arcpy.AddMessage("  Insert Cursor")
    def EqualPnts(P1,P2):
        if P1.X == P2.X and P1.Y == P2.Y:
            return True
        else:
            return False
    def ComparePointDict(P1,P2):
        if P1['X']==P2['X'] and P1['Y']==P2['Y']:
            return True
        else:
            return False
    def OppositeDirection(rn):
        Opp = {'N':'S','S':'N','W':'E','E':'W','T':'T'}
        return(rn[:-1]+Opp[rn[-1]])
    arcpy.env.MTolerance  = 0.0001
    arcpy.env.MResolution = 0.0000001
    arcpy.env.ZTolerance  = "0.1 Feet"
    arcpy.env.ZResolution = "0.1 Feet"
    RCT1N = CreateFeatureclass('RCT1N',{'geometry_type':'POLYLINE','has_m':'ENABLED','has_z':'ENABLED'})
    arcpy.DefineProjection_management(RCT1N,CoordSystemSC)
    #To do list:
    # loops have problem, creates additional part
    # partially divided routes should have the same milepost with main route
    
    for field in [F_Name, F_County, F_Route_Type,F_Route_Numb,F_Route_Aux,F_Route_Dire,F_Route_LRS,F_BegMp,F_EndMp, F_Oneway,F_DirePoly,F_DissolveID]:
        AddField(RCT1N,field)
    IC = arcpy.InsertCursor(RCT1N)
    for rn in MPDict.keys():
        #arcpy.AddMessage(str(rn))
        # 1st phase: Dissolving the segments and creating a list of all parts (PartL) along with each parts BMP (PartM)
        # plus importing z values to each point => pnt = [X,Y,Z]
        # assumption is parts in segments are consecutive so the milepost of the next part can be obtained by 
        # adding the length of the part to bmp 
        PartL = []
        PartM = []
        i = -1
        for seg in MPDict[rn]['SegL']:
            i += 1
            L = 0
            j = -1
            for prt in seg:
                j += 1
                PartL.append(prt)
                PartM.append(L+MPDict[rn]['BMP'][MPDict[rn]['SegL'].index(seg)])
                a = arcpy.Array()
                k = -1
                for pnt in prt:
                    k += 1
                    pnt.append(MPDict[rn]['Z'][i][j][k])
                    a.add(arcpy.Point(pnt[0],pnt[1]))
                L += arcpy.Polyline(a).length/5280
        # Phase 2: Dissolving parts to points and adding M values to each point
        # begpnts are defined as the starting point of each route or its seperate part
        # in first section, it is assumed that all the beg points of parts are begpnts
        PointL = []
        for prt in PartL:
            L = PartM[PartL.index(prt)]
            for pnt in prt:
                b = False
                if prt.index(pnt) == 0: b = True
                PointL.append({'X':pnt[0],'Y':pnt[1],'Z':pnt[2],'M':L,'PrtNum':PartL.index(prt),'BegPnt':b})
                a = arcpy.Array(arcpy.Point(pnt[0],pnt[1]))
                if prt.index(pnt)+1<len(prt):
                    a.add(arcpy.Point(prt[prt.index(pnt)+1][0],prt[prt.index(pnt)+1][1]))
                    L += arcpy.Polyline(a).length/5280
        # in second section, begpnts which are found as the ending point of another part are omitted
        # exception is if the point is the ending point of it's own part (#Loops)
        for pnt in PointL:
            if pnt['BegPnt']:
                for prt in PartL:
                    if ComparePointDict({'X':prt[-1][0],'Y':prt[-1][1]},pnt) and PartL.index(prt)<>pnt['PrtNum']:
                        pnt['BegPnt'] = False
        # if all begpnts are omitted the one with min m value is restored
        BegPntD = {pnt['M']:pnt for pnt in PointL if pnt['BegPnt']}
        if len(BegPntD.keys())==0:
            m = min([pnt['M'] for pnt in PointL])
            for pnt in PointL:
                if pnt['M']==m:
                    pnt['BegPnt'] = True
                    BegPntD = {pnt['M']:pnt for pnt in PointL if pnt['BegPnt']}
        # Third phase: creating final routes
        MKeys = BegPntD.keys()
        MKeys.sort()
        Route = []
        Parts = []
        # replacing the pnt dicts with pnt lists in PartL
        PartNumbers = range(0,len(PartL))
        PartL = []
        for i in PartNumbers:
            PartL.append([pnt for pnt in PointL if pnt['PrtNum']==i])
        # Creating routes
        for m in MKeys:
            RoutePart = [BegPntD[m]]
            for pnt in PartL[BegPntD[m]['PrtNum']][1:]:
                RoutePart.append(pnt)
            a = arcpy.Array(arcpy.Point(pnt['X'],pnt['Y']))
            LastM = pnt['M']
            #arcpy.AddMessage(str([RoutePart[-1]]))
            Parts.append(PartL[BegPntD[m]['PrtNum']])
            NextPart = [prt for prt in PartL if ComparePointDict(RoutePart[-1],prt[0]) and not prt in Parts]
            while len(NextPart)>0:
                Parts.append(NextPart[0])
                for pnt in NextPart[0][1:]:
                    a.add(arcpy.Point(pnt['X'],pnt['Y']))
                    L = arcpy.Polyline(a).length/5280
                    pnt['M'] = LastM + L
                    a = arcpy.Array(arcpy.Point(pnt['X'],pnt['Y']))
                    LastM = pnt['M']
                    #arcpy.AddMessage(str(len(RoutePart)))
                    RoutePart.append(pnt)
                #arcpy.AddMessage(str([RoutePart[-1]]))
                NextPart = [prt for prt in PartL if ComparePointDict(RoutePart[-1],prt[0]) and not prt in Parts]
            Route.append(RoutePart)
        #MPDict[rn]['Route'] = Route
        IRow = IC.newRow() 
        IRow.setValue(F_Name['name'],rn)
        IRow.setValue(F_Oneway['name'],MPDict[rn]['Oneway'][0])
        IRow.setValue(F_DirePoly['name'],0)
        if OppositeDirection(rn) in MPDict.keys():
            IRow.setValue(F_DirePoly['name'],1)
        Arr = arcpy.Array()
        for prt in Route:
            a = arcpy.Array()
            i = 0
            for pnt in prt:
                i += 1
                p = arcpy.Point(pnt['X'],pnt['Y'],pnt['Z'],pnt['M'],i)
                a.add(p)
            Arr.add(a)
        pl = arcpy.Polyline(Arr,CoordSystemSC,True,True)
        MPDict[rn]['Len'] = pl.length
        IRow.shape = pl

        IC.insertRow(IRow)           
    del IC

    arcpy.AddMessage("  Sort")
    CalField(RCT1N,F_County    ,'!'+F_Name['name']+'![0:2]')
    CalField(RCT1N,F_Route_Type,'!'+F_Name['name']+'![2:4]')
    CalField(RCT1N,F_Route_Numb,'!'+F_Name['name']+'![4:9]')
    CalField(RCT1N,F_Route_Aux ,'!'+F_Name['name']+'![9:11]')
    CalField(RCT1N,F_Route_Dire,'!'+F_Name['name']+'![-1]')
    CalField(RCT1N,F_BegMp,'!Shape!.firstPoint.M')
    CalField(RCT1N,F_EndMp,'!Shape!.lastPoint.M')
    RCT1S = Sort(RCT1N,'RCT1S',F_Route_Type['name']+';'+F_County['name']+';'+F_Route_Numb['name']+';'+F_Route_Aux['name']+';'+F_Route_Dire['name'])

    arcpy.AddMessage("  Update Cursor")    
    DissDict = {}
    i = 0
    UC = arcpy.UpdateCursor(RCT1S)
    for URow in UC:
        rn = URow.getValue(F_Name['name'])
        if OppositeDirection(rn) in MPDict.keys():
            if OppositeDirection(rn) in DissDict.keys():
                URow.setValue(F_DissolveID['name'],DissDict[OppositeDirection(rn)])
            else:
                i += 1
                DissDict.update({rn:i})
                URow.setValue(F_DissolveID['name'],i)
        else:
            i += 1
            URow.setValue(F_DissolveID['name'],i)
        UC.updateRow(URow)
    arcpy.Delete_management(RCT1N)
def GDBImportAttTables(RIMSInput,RoutesInput,Output):
    arcpy.AddMessage("    ")
    arcpy.AddMessage("    Create Network Geodatabase")

    OutDic = OutputParser(Output, 'mdb')
    
    arcpy.AddMessage("  Copy Features: RIMS Layer")
    RIMS = CopyRows(RIMSInput,'CNRInput')

    #arcpy.AddMessage("  Search Cursor: Routes")
    #RtDict = {r.getValue('Name'):{'Cn':r.getValue('County'),'Rt':r.getValue('Route_Type'),'Rn':r.getValue('Route_Numb'),
    #                              'Ra':r.getValue('Route_Aux'),'Rd':r.getValue('Route_Dire'),'On':r.getValue('Oneway'),
    #                              'LRS':r.getValue('Route_LRS'),'SN':r.getValue('StreetName')} for r in arcpy.SearchCursor(RoutesInput)}

    GDB = arcpy.CreatePersonalGDB_management(OutDic['folder'], OutDic['file'])
    arcpy.AddMessage("    Import Route Features")
    Routes = arcpy.FeatureClassToFeatureClass_conversion(RoutesInput, GDB, "Routes")
    
    arcpy.AddMessage("    Rearrange Fields")
    #ClearFields(Routes,['Name'])
    FL = [F_County,F_Route_Type,F_Route_Numb,F_Route_Aux,F_Route_Dire,F_BegMp,F_EndMp, F_Oneway,F_Route_LRS,F_StreetName]
    for field in FL:
        arcpy.AlterField_management(Routes, field['name'], field['name'], field['alias'], '', field['length'], field['nullable'], 'FALSE')

        #AddField(Routes,field)
    #UC = arcpy.UpdateCursor(Routes)
    #for URow in UC:
    #    n = URow.getValue('Name')
    #    URow.setValue(F_County    ['name'],RtDict[n]['Cn'])
    #    URow.setValue(F_Route_Type['name'],RtDict[n]['Rt'])
    #    URow.setValue(F_Route_Numb['name'],RtDict[n]['Cn'])
    #    URow.setValue(F_Route_Aux['name'],RtDict[n]['Cn'])
    #    URow.setValue(F_Route_Dire['name'],RtDict[n]['Cn'])
    #    URow.setValue(F_Oneway['name'],RtDict[n]['Cn'])
    #    URow.setValue(F_Route_LRS['name'],RtDict[n]['Cn'])
    #    URow.setValue(F_StreetName['name'],RtDict[n]['SN'])
    #    UC.updateRow(URow)
    #CalField(Routes,F_BegMp,'!Shape!.firstPoint.M')
    #CalField(Routes,F_EndMp,'!Shape!.lastPoint.M')

    Prop = "Route_LRS LINE bmp emp"
    AttDict  = {'MedType':{'OldFL':"Median_ID"                                   ,'NewFL':[F_Median_ID]                                     ,'Table':'','Alias':'Median Type'},
                'MedWid' :{'OldFL':"Median_Wid"                                  ,'NewFL':[F_Median_Wid]                                    ,'Table':'','Alias':'Median Width'},
                'Lanes'  :{'OldFL':"Left_Lanes;Rt_Lanes;TotalLanes"              ,'NewFL':[F_LeftLanes,F_RightLanes,F_TotalLanes]           ,'Table':'','Alias':'Number of Lanes'},
                'LaneWid':{'OldFL':"Lane_Width"                                  ,'NewFL':[F_Lane_Width]                                    ,'Table':'','Alias':'Lane Width'},
                'SurWid' :{'OldFL':"Sub_Sur_W;Sub_Surf_w;SurWid_Tot"             ,'NewFL':[F_L_Sur_W,F_R_Sur_W,F_SurWid_Tot]                ,'Table':'','Alias':'Surface Width'},
                'ShWid'  :{'OldFL':"Sh_Widt_li;Sh_Widt_lo;Rt_Sh_Widt;Sh_Wid_ro"  ,'NewFL':[F_Sh_Wid_LI,F_Sh_Wid_LO,F_Sh_Wid_RI,F_Sh_Wid_RO] ,'Table':'','Alias':'Shoulder Width'},
                'ShTrt'  :{'OldFL':"L_Sh_Trt;Sh_Trt_1;Rt_Sh_Trt;Sh_Trt_2"        ,'NewFL':[F_Sh_Trt_LI,F_Sh_Trt_LO,F_Sh_Trt_RI,F_Sh_Trt_RO] ,'Table':'','Alias':'Shoulder Treatment'},
                'Curb'   :{'OldFL':"L_insi_crb;L_Outs_Crb;Rt_ins_Crb;Rt_Out_Crb" ,'NewFL':[F_CurbPr_LI,F_CurbPr_LO,F_CurbPr_RI,F_CurbPr_RO] ,'Table':'','Alias':'Curb Presence'},
                'SwTrt'  :{'OldFL':"L_Sw_Trt;Sw_Trt_1;Rt_Sw_Trt;Sw_Trt_2"        ,'NewFL':[F_Sw_Trt_LI,F_Sw_Trt_LO,F_Sw_Trt_RI,F_Sw_Trt_RO] ,'Table':'','Alias':'Sidewalk Treatment'},
                'Other'  :{'OldFL':"Sub_Psur_l;SubPhsur_l;Sub_Pvsu_R"            ,'NewFL':[]                                                ,'Table':'','Alias':'Other'}}
    for att in AttDict.keys():
        arcpy.AddMessage('  '+att+':')
        #arcpy.AddMessage('   - Dissolve')
        AttDict[att]['Table'] = arcpy.DissolveRouteEvents_lr(RIMS,Prop,AttDict[att]['OldFL'],att,Prop,"DISSOLVE", "INDEX")
        #arcpy.AddMessage('   - Convert Fields')
        AddField(AttDict[att]['Table'],F_Name)
        CalField(AttDict[att]['Table'],F_Name,"'{:2.2f}{}{:2.2f}'.format(!bmp!,' - ',!emp!)")
        for field in AttDict[att]['NewFL']:
            oldf = AttDict[att]['OldFL'].split(';')[AttDict[att]['NewFL'].index(field)]
            #arcpy.AddMessage(str([AttDict[att]['Table'],field['name']]))
            try:
                if oldf<>field['name']:
                    AddField(AttDict[att]['Table'],field)
                    CalField(AttDict[att]['Table'],field,'!'+oldf+'!')
                    arcpy.DeleteField_management(AttDict[att]['Table'],oldf)
            except:
                arcpy.AlterField_management(AttDict[att]['Table'], oldf, field['name'], field['alias'], '', field['length'], field['nullable'], 'FALSE')
                arcpy.AddMessage(oldf)
        #arcpy.AddMessage('   - Sort')
        AttDict[att]['Table'] = Sort(AttDict[att]['Table'],str(AttDict[att]['Table'])+'S','Route_LRS;bmp')
        #arcpy.AddMessage('   - Add to GDB')
        AttTab = arcpy.TableToTable_conversion(AttDict[att]['Table'],GDB,att)
        #Routes = GDB + '\\'+'Routes'
        RLU = arcpy.CreateRelationshipClass_management(Routes, AttTab, OutDic['folder']+OutDic['file']+"\\Route-" + att, "SIMPLE", AttDict[att]['Alias'], "", "NONE", "ONE_TO_MANY", "NONE", "Route_LRS", "Route_LRS")    

    Domains = {
        'Route_Type':{1:'Interstate',
2:'US Route',
4:'SC Route',
5:'Ramp',
6:'Ramp Spur',
7:'Secondary road',
9:'Local road',
10:'State Park',
11:'State Institution',
12:'National Park',
13:'Forest Service road',
14:'Spur'},
        'Route_Aux':{1:'Summary',
2:'Alternate',
3:'Main Line Couplet',
4:'Business Couplet',
5:'Spur',
6:'Connection',
7:'Business',
8:'Bypass',
9:'Proposed Road',
10:'Quad 1 On-Ramp 1',
11:'Quad 1 On-Ramp 2',
12:'Quad 1 On-Ramp 3',
14:'Quad 1 Exit-Ramp 1',
15:'Quad 1 Exit-Ramp 2',
16:'Quad 1 Exit-Ramp 3',
18:'Quad 2 On-Ramp 1',
19:'Quad 2 On-Ramp 2',
20:'Quad 2 On-Ramp 3',
22:'Quad 2 Exit-Ramp 1',
23:'Quad 2 Exit-Ramp 2',
24:'Quad 2 Exit-Ramp 3',
26:'Quad 3 On-Ramp 1',
27:'Quad 3 On-Ramp 2',
28:'Quad 3 On-Ramp 3',
30:'Quad 3 Exit-Ramp 1',
31:'Quad 3 Exit-Ramp 2',
32:'Quad 3 Exit-Ramp 3',
34:'Quad 4 On-Ramp 1',
35:'Quad 4 On-Ramp 2',
36:'Quad 4 On-Ramp 3',
38:'Quad 4 Exit-Ramp 1',
39:'Quad 4 Exit-Ramp 2',
40:'Quad 4 Exit-Ramp 3',
41:'Other Drive 1',
42:'Other Drive 2',
43:'Other Drive 3',
44:'Other Drive 4',
45:'Cemetery Drive 4',
48:'Business1',
49:'Business2',
50:'Connector 1',
52:'Connector 2',
53:'CONNECTION DRIVE 1',
54:'CONNECTION DRIVE 2',
55:'CONNECTION DRIVE 3',
56:'CONNECTION DRIVE 4',
57:'CONNECTION DRIVE 5',
58:'CONNECTION DRIVE 6',
59:'CONNECTION DRIVE 7',
60:'CONNECTION DRIVE 8',
61:'CONNECTION DRIVE 9',
62:'SPUR DRIVE 1',
63:'SPUR DRIVE 2',
64:'SPUR DRIVE 3',
65:'SPUR DRIVE 4',
66:'SPUR DRIVE 5',
67:'SPUR DRIVE 6',
68:'SPUR DRIVE 7',
69:'SPUR DRIVE 8',
70:'SPUR DRIVE 9',
71:'MAINLINE DRIVE 1',
72:'MAINLINE DRIVE 2',
73:'MAINLINE DRIVE 3',
74:'MAINLINE DRIVE 4',
75:'MAINLINE DRIVE 5',
76:'MAINLINE DRIVE 6',
77:'MAINLINE DRIVE 7',
78:'MAINLINE DRIVE 8',
79:'MAINLINE DRIVE 9',
80:'BRIDGE RAMP',
81:'SERVICE',
82:'Other',
83:'Other Drive 5',
84:'Other Drive 6',
85:'Other Drive 7',
90:'School Drive 4',
91:'School Drive 1',
92:'School Drive 2',
93:'School Drive 3',
94:'Cemetery Drive 1',
95:'Cemetery Drive 2',
96:'Cemetery Drive 3',
97:'Church Drive 1',
98:'Church Drive 2',
99:'Church Drive 3'},
        'Route_Dire':{'N':'North',
'S':'South',
'E':'East',
'W':'West'},
        'Median_ID':{0:'Non-divided',
1:'Divided - Earth median',
2:'Divided - Concrete median',
3:'Multi-lane - bituminous Median',
4:'Divided - Raised Concrete & Surfaced Median',
5:'Divided - Physical Barrier',
6:'Divided - Cable Stay Guardrail',
8:'One-way street'},
        'County':{1:'Abbeville',
2:'Aiken',
3:'Allendale',
4:'Anderson',
5:'Bamberg',
6:'Barnwell',
7:'Beaufort',
8:'Berkeley',
9:'Calhoun',
10:'Charleston',
11:'Cherokee',
12:'Chester',
13:'Chesterfield',
14:'Clarendon',
15:'Colleton',
16:'Darlington',
17:'Dillon',
18:'Dorchester',
19:'Edgefield',
20:'Fairfield',
21:'Florence',
22:'Georgetown',
23:'Greenville',
24:'Greenwood',
25:'Hampton',
26:'Horry',
27:'Jasper',
28:'Kershaw',
29:'Lancaster',
30:'Laurens',
31:'Lee',
32:'Lexington',
33:'Mccormick',
34:'Marion',
35:'Marlboro',
36:'Newberry',
37:'Oconee',
38:'Orangeburg',
39:'Pickens',
40:'Richland',
41:'Saluda',
42:'Spartanburg',
43:'Sumter',
44:'Union',
45:'Williamsburg',
46:'York'},
        'CurbPr_LI':{0:'No',1:'Yes'},
        'Sh_Trt_LI':{-1:'Unknown',
0:'None',
1:'Bituminous Treatment',
2:'Bituminous Valley Gutter',
3:'Bituminous Treatment & Earth'}}
    Assignments = [ {'Domain':F_County,'Assign':[{'Table':Routes,'Fields':[F_County]}]},
                    {'Domain':F_Route_Type,'Assign':[{'Table':Routes,'Fields':[F_Route_Type]}]},
                    {'Domain':F_Route_Aux ,'Assign':[{'Table':Routes,'Fields':[F_Route_Aux ]}]},
                    {'Domain':F_Route_Dire,'Assign':[{'Table':Routes,'Fields':[F_Route_Dire]}]},
                    {'Domain':F_Median_ID,'Assign':[{'Table':OutDic['folder']+'\\'+OutDic['file'] + '\\'+'MedType','Fields':[F_Median_ID]}]},
                    {'Domain':F_CurbPr_LI,'Assign':[{'Table':OutDic['folder']+'\\'+OutDic['file'] + '\\'+'Curb','Fields':[F_CurbPr_LI,F_CurbPr_LO,F_CurbPr_RI,F_CurbPr_RO]}]},
                    {'Domain':F_Sh_Trt_LI,'Assign':[{'Table':OutDic['folder']+'\\'+OutDic['file'] + '\\'+'ShTrt','Fields':[F_Sh_Trt_LI,F_Sh_Trt_LO,F_Sh_Trt_RI,F_Sh_Trt_RO]},{'Table':OutDic['folder']+'\\'+OutDic['file'] + '\\'+'SwTrt','Fields':[F_Sw_Trt_LI,F_Sw_Trt_LO,F_Sw_Trt_RI,F_Sw_Trt_RO]}]}]
    for rec in Assignments:
        try:
            arcpy.AddMessage("     - " + rec['Domain']['name'])
            arcpy.CreateDomain_management(OutDic['folder']+'\\'+OutDic['file'], rec['Domain']['name'], rec['Domain']['alias'], rec['Domain']['type'], "CODED")
            for code in Domains[rec['Domain']['name']].keys():
                #arcpy.AddMessage(str(code)+':'+Domains[rec['Domain']['name']][code])
                arcpy.AddCodedValueToDomain_management(OutDic['folder']+'\\'+OutDic['file'], rec['Domain']['name'], code, Domains[rec['Domain']['name']][code])
            for assign in rec['Assign']:
                for field in assign['Fields']:
                    #arcpy.AddMessage(str(assign['Table'])+','+field['name']+','+rec['Domain']['name'])
                    arcpy.AssignDomainToField_management(assign['Table'], field['name'], rec['Domain']['name'])
        except Exception, e:
            import sys
            tb = sys.exc_info()[2]
            arcpy.AddMessage(field['name'])
            arcpy.AddWarning("Line %i" % tb.tb_lineno)
            arcpy.AddWarning(e.message)
    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")

 # Urban County Pop Density
def ImportPopDensity(TargetInput,BGInput,PopDField,Output):
    arcpy.AddMessage(" ")
    arcpy.AddMessage("    Population Density")

    OutDic = OutputParser(Output, 'shp')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("    Copy Features: Target Layer")
    TargetLayer = CopyFeatures(TargetInput,'PopTarget')
    TotalTargets = arcpy.GetCount_management(TargetLayer)
    arcpy.AddMessage("     - Total number of Items Found: " + str(TotalTargets))

    arcpy.AddMessage("    Copy Features: Population Layer")
    UDataLayer = CopyFeatures(BGInput,'PopPDInput')
    TotalU = arcpy.GetCount_management(UDataLayer)
    arcpy.AddMessage("     - Total number of Items Found: " + str(TotalU))

    arcpy.AddMessage("    Add Fields: Sites Layer & Population Layer")
    FieldList1 = [F_TargetFID]
    FieldList2 = [F_JoinFID]
    FieldList3 = [F_Pop_dens_p]

    for Field in FieldList3:
        arcpy.DeleteField_management(TargetLayer,Field['name'])

    for Field in [PopDField]:
        arcpy.DeleteField_management(TargetLayer,Field)

    for Field in FieldList1:
        AddField(TargetLayer,Field)

    UC = arcpy.UpdateCursor(TargetLayer)
    for URow in UC:
        FID = GetFID(URow)
        URow.setValue(F_TargetFID['name'],FID)
        UC.updateRow(URow)

    for Field in FieldList2:
        AddField(UDataLayer,Field)

    UC = arcpy.UpdateCursor(UDataLayer)
    for URow in UC:
        FID = GetFID(URow)
        URow.setValue(F_JoinFID['name'],FID)
        UC.updateRow(URow)

    arcpy.AddMessage("    Spatial Join: Sites Layer + Population Layer")
    USPJ = SpatialJoin(TargetLayer, UDataLayer, 'PopUSPJ', {'join_operation': "JOIN_ONE_TO_MANY", 'join_type': "KEEP_ALL", 'field_mapping': '', 'match_option': 'INTERSECT', 'search_radius': '', 'distance_field_name': ''})

    if arcpy.Describe(TargetLayer).shapetype=='Polyline':
        for Field in [F_Length['name']]:
            arcpy.DeleteField_management(TargetLayer,Field)

        for Field in [F_Length]:
            AddField(TargetLayer,Field)
        CalField(TargetLayer,F_Length,"!Shape!.length")
        arcpy.AddMessage("    Intersect: Sites Layer + Population Layer")
        UINT = Intersect([TargetLayer, UDataLayer], 'UrbUInt', {'join_attributes': "ALL", 'cluster_tolerance': "-1 Unknown", 'output_type': "INPUT"})
        FDic = {SRow.getValue(F_TargetFID['name']):[] for SRow in arcpy.SearchCursor(TargetLayer)}
        RDic = {SRow.getValue(F_TargetFID['name']):[] for SRow in arcpy.SearchCursor(TargetLayer)}
        for SRow in arcpy.SearchCursor(UINT):
            FDic[SRow.getValue(F_TargetFID['name'])].append(SRow.getValue(F_JoinFID['name']))
            RDic[SRow.getValue(F_TargetFID['name'])].append(SRow.getValue('Shape').length/SRow.getValue('Length'))

    arcpy.AddMessage("    Update Cursor: Sites Layer")
    if arcpy.Describe(TargetLayer).shapetype=='Polyline':
        UFIDList  = {SRow.getValue(F_TargetFID['name']):0 for SRow in arcpy.SearchCursor(TargetLayer)}
        for SRow in arcpy.SearchCursor(USPJ):
            tfid = SRow.getValue(F_TargetFID['name'])
            jfid = SRow.getValue(F_JoinFID['name'])
            #arcpy.AddMessage(str([tfid,SRow.getValue(PopDField),FDic[tfid],RDic[tfid]]))
            if jfid in FDic[tfid]:
                UFIDList[tfid] += SRow.getValue(PopDField) * RDic[tfid][FDic[tfid].index(jfid)]
    else:
        UFIDList  = {SRow.getValue(F_TargetFID['name']):SRow.getValue(PopDField) for SRow in arcpy.SearchCursor(USPJ)}

    for Field in FieldList3:
        AddField(TargetLayer,Field)

    UC = arcpy.UpdateCursor(TargetLayer)
    for URow in UC:
        TFID = URow.getValue(F_TargetFID['name'])
        URow.setValue(F_Pop_dens_p['name'],UFIDList[TFID])
        UC.updateRow(URow)

    for Field in FieldList1:
        arcpy.DeleteField_management(TargetLayer,Field['name'])

    arcpy.CopyFeatures_management(TargetLayer, Output)
    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")
def ImportUrbanCounty(TargetInput,UrbanInput,CountyInput,CountyField,AreaField1,AreaField2,Output):
    arcpy.AddMessage(" ")
    arcpy.AddMessage("    Urban Rural; County Area")

    OutDic = OutputParser(Output, 'shp')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("    Copy Features: Target Layer")
    TargetLayer = CopyFeatures(TargetInput,'UrbTarget')
    TotalTargets = arcpy.GetCount_management(TargetLayer)
    arcpy.AddMessage("     - Total number of Items Found: " + str(TotalTargets))

    arcpy.AddMessage("    Copy Features: Urban Layer")
    UDataLayer = CopyFeatures(UrbanInput,'UrbUrbanInput')
    TotalU = arcpy.GetCount_management(UDataLayer)
    arcpy.AddMessage("     - Total number of Items Found: " + str(TotalU))

    arcpy.AddMessage("    Copy Features: County Layer")
    CDataLayer = CopyFeatures(CountyInput,'UrbCountyInput')
    TotalC = arcpy.GetCount_management(CDataLayer)
    arcpy.AddMessage("     - Total number of Items Found: " + str(TotalC))

    arcpy.AddMessage("    Add Fields: Sites Layer & Urban Layer & County Layer")
    FieldList1 = [F_TargetFID]
    FieldList2 = [F_JoinFID]
    FieldList3 = [F_URBAN, F_RURAL, F_County, F_Area1, F_Area2]

    for Field in FieldList3:
        arcpy.DeleteField_management(TargetLayer,Field['name'])

    for Field in [CountyField, AreaField1, AreaField2]:
        arcpy.DeleteField_management(TargetLayer,Field)

    for Field in FieldList1:
        AddField(TargetLayer,Field)

    UC = arcpy.UpdateCursor(TargetLayer)
    for URow in UC:
        FID = GetFID(URow)
        URow.setValue(F_TargetFID['name'],FID)
        UC.updateRow(URow)

    for Field in FieldList2:
        AddField(UDataLayer,Field)

    UC = arcpy.UpdateCursor(UDataLayer)
    for URow in UC:
        FID = GetFID(URow)
        URow.setValue(F_JoinFID['name'],FID)
        UC.updateRow(URow)

    for Field in FieldList2:
        AddField(CDataLayer,Field)

    UC = arcpy.UpdateCursor(CDataLayer)
    for URow in UC:
        FID = GetFID(URow)
        URow.setValue(F_JoinFID['name'],FID)
        UC.updateRow(URow)

    #arcpy.AddMessage(" Calculating Fields")

    arcpy.AddMessage("    Spatial Join: Sites Layer + Urban Layer")
    USPJ = SpatialJoin(TargetLayer, UDataLayer, 'UrbUSPJ', {'join_operation': "JOIN_ONE_TO_ONE", 'join_type': "KEEP_COMMON", 'field_mapping': '', 'match_option': 'INTERSECT', 'search_radius': '', 'distance_field_name': ''})

    if arcpy.Describe(TargetLayer).shapetype=='Polyline':
        for Field in [F_Length['name']]:
            arcpy.DeleteField_management(TargetLayer,Field)

        for Field in [F_Length]:
            AddField(TargetLayer,Field)
        CalField(TargetLayer,F_Length,"!Shape!.length")
        arcpy.AddMessage("    Intersect: Sites Layer + Urban Layer")
        UINT = Intersect([TargetLayer, UDataLayer], 'UrbUInt', {'join_attributes': "ALL", 'cluster_tolerance': "-1 Unknown", 'output_type': "INPUT"})
        IDic      = {SRow.getValue(F_TargetFID['name']):SRow.getValue('Shape').length/SRow.getValue('Length') for SRow in arcpy.SearchCursor(UINT)}

    arcpy.AddMessage("    Spatial Join: Sites Layer + County Layer")
    if arcpy.Describe(TargetLayer).shapetype<>'Polyline':
        CSPJ = SpatialJoin(TargetLayer, CDataLayer, 'UrbCSPJ', {'join_operation': "JOIN_ONE_TO_ONE", 'join_type': "KEEP_COMMON", 'field_mapping': '', 'match_option': 'INTERSECT', 'search_radius': '', 'distance_field_name': ''})

    if arcpy.Describe(TargetLayer).shapetype=='Polyline':
        CSPJ = SpatialJoin(TargetLayer, CDataLayer, 'UrbCSPJ', {'join_operation': "JOIN_ONE_TO_MANY", 'join_type': "KEEP_COMMON", 'field_mapping': '', 'match_option': 'INTERSECT', 'search_radius': '', 'distance_field_name': ''})
        CDic      = {SRow.getValue(F_TargetFID['name']):[0,0,0] for SRow in arcpy.SearchCursor(CSPJ)}
        #for SRow in arcpy.SearchCursor(CSPJ):
        #    CDic[SRow.getValue(F_TargetFID['name'])].update({SRow.getValue(CountyField):0})
        arcpy.AddMessage("    Intersect: Sites Layer + County Layer")
        CINT = Intersect([TargetLayer, CDataLayer], 'UrbCInt', {'join_attributes': "ALL", 'cluster_tolerance': "-1 Unknown", 'output_type': "INPUT"})
        for SRow in arcpy.SearchCursor(CINT):
            TFID = SRow.getValue(F_TargetFID['name'])
            if SRow.getValue('Shape').length/SRow.getValue('Length')>0.5:
                CDic[TFID]=[SRow.getValue(CountyField),SRow.getValue(AreaField1),SRow.getValue(AreaField2)]

    #CountyDic = {SRow.getValue(CountyField):] for SRow in arcpy.SearchCursor(CDataLayer)}

    arcpy.AddMessage("    Update Cursor: Sites Layer")
    UFIDList  = [SRow.getValue(F_TargetFID['name']) for SRow in arcpy.SearchCursor(USPJ)]
    if arcpy.Describe(TargetLayer).shapetype=='Polyline':
        for fid in IDic.keys():
           if IDic[fid]<.5 and fid in UFIDList:
               UFIDList.pop(UFIDList.index(fid))
    if arcpy.Describe(TargetLayer).shapetype<>'Polyline':
        CFIDList  = [SRow.getValue(F_TargetFID['name']) for SRow in arcpy.SearchCursor(CSPJ)]
        CntyList  = [SRow.getValue(CountyField)         for SRow in arcpy.SearchCursor(CSPJ)]
        Area1List = [SRow.getValue(AreaField1)          for SRow in arcpy.SearchCursor(CSPJ)]
        Area2List = [SRow.getValue(AreaField2)          for SRow in arcpy.SearchCursor(CSPJ)]
    if arcpy.Describe(TargetLayer).shapetype=='Polyline':
        CFIDList  = [k for k in CDic.keys()]
        CntyList  = [CDic[k][0] for k in CDic.keys()]
        Area1List = [CDic[k][1] for k in CDic.keys()]
        Area2List = [CDic[k][2] for k in CDic.keys()]

    for Field in FieldList3:
        AddField(TargetLayer,Field)

    UC = arcpy.UpdateCursor(TargetLayer)
    for URow in UC:
        TFID = URow.getValue(F_TargetFID['name'])

        if TFID in UFIDList:
            URow.setValue(F_URBAN['name'],1)
            URow.setValue(F_RURAL['name'],0)
        else:
            URow.setValue(F_URBAN['name'],0)
            URow.setValue(F_RURAL['name'],1)

        if TFID in CFIDList:
            URow.setValue(F_County['name'],CntyList[CFIDList.index(TFID)])
            URow.setValue(F_Area1['name'],Area1List[CFIDList.index(TFID)])
            URow.setValue(F_Area2['name'],Area2List[CFIDList.index(TFID)])
        else:
            arcpy.AddWarning('     - No County Matches for FID ' + str(TFID)) 

        UC.updateRow(URow)

    for Field in FieldList1:
        arcpy.DeleteField_management(TargetLayer,Field['name'])

    arcpy.CopyFeatures_management(TargetLayer, Output)
    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")
def ImportFitted(TargetInput,FittedInput,Output):
    arcpy.AddMessage(" ")
    arcpy.AddMessage("    Fitted Crashes Import")

    OutDic = OutputParser(Output, 'shp')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("    Copy Features: Target Layer")
    TargetLayer = CopyFeatures(TargetInput,'FitTarget')
    TotalTargets = arcpy.GetCount_management(TargetLayer)
    arcpy.AddMessage("     - Total number of Items Found: " + str(TotalTargets))

    arcpy.AddMessage("    Count Features: Fitted Table")
    FitLayer = arcpy.ExcelToTable_conversion(FittedInput,'FitData')
    TotalU = arcpy.GetCount_management(FitLayer)
    arcpy.AddMessage("     - Total number of Items Found: " + str(TotalU))

    arcpy.AddMessage("    Add Fields: Sites Layer & Fit Layer")

    for Field in [F_Fitted, F_FitDif]:
        AddField(TargetLayer,Field)

    InputDic  = {SRow.getValue('FID'):[SRow.getValue('Fitted'),SRow.getValue('Diff')] for SRow in arcpy.SearchCursor(FitLayer)}

    arcpy.AddMessage("    Update Cursor: Sites Layer")
    UC = arcpy.UpdateCursor(TargetLayer)
    for URow in UC:
        FID = URow.getValue('OBJECTID')-1
        Fit = 0; Dif = 0
        if FID in InputDic.keys():
            Fit = InputDic[FID][0]
            Dif = InputDic[FID][1]
        try:
            URow.setValue(F_Fitted['name'],Fit)
            URow.setValue(F_FitDif['name'],Dif)
        except:
            arcpy.AddMessage(str([Fit,Dif]))
        UC.updateRow(URow)

    #arcpy.SelectLayerByAttribute_management(TargetLayer,'''"Fitted" <> 0''')
    arcpy.CopyFeatures_management(TargetLayer, Output)
    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")
def JoinFitted(TargetInput,JoinInputs,Output):
    arcpy.AddMessage(" ")
    arcpy.AddMessage("    Join Fitted Crashes")

    OutDic = OutputParser(Output, 'shp')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("    Copy Features: Target Layer")
    TargetLayer = CopyFeatures(TargetInput,'JFTarget')
    TotalTargets = arcpy.GetCount_management(TargetLayer)
    arcpy.AddMessage("     - Total number of Items Found: " + str(TotalTargets))

    arcpy.AddMessage("    Add Fields: Target Layer")
    for Field in [F_TargetFID]:
        AddField(TargetLayer,Field)
    CalField(TargetLayer,F_TargetFID,'!OBJECTID!')
    FitDic = {SRow.getValue(F_TargetFID['name']):{'Int':[],'IntW':[],'Seg':[],'SegW':[]} for SRow in arcpy.SearchCursor(TargetLayer)}

    for JoinInput in JoinInputs.split(';'):
        arcpy.AddMessage("    Count Features: " + JoinInput + " Layer")
        JoinLayer = CopyFeatures(JoinInput,'JFJoin')
        TotalU = arcpy.GetCount_management(JoinLayer)
        arcpy.AddMessage("     - Total number of Items Found: " + str(TotalU))

        arcpy.AddMessage("    Intersect: Target Layer + " + JoinInput + " Layer")
        UINT = Intersect([TargetLayer, JoinLayer], 'FJInt', {'join_attributes': "ALL", 'cluster_tolerance': "-1 Unknown", 'output_type': "INPUT"})
        if arcpy.Describe(JoinLayer).shapetype=='Point':
            for SRow in arcpy.SearchCursor(UINT):
                Diff = SRow.getValue(F_FitDif['name'])
                if Diff == 0:W = 0
                if Diff <> 0:W = SRow.getValue(F_AADT_Major['name']) + SRow.getValue(F_AADT_Minor['name'])
                FitDic[SRow.getValue(F_TargetFID['name'])]['Int' ].append(Diff)
                FitDic[SRow.getValue(F_TargetFID['name'])]['IntW'].append(W)
        if arcpy.Describe(JoinLayer).shapetype=='Polyline':
            for SRow in arcpy.SearchCursor(UINT):
                Diff = SRow.getValue(F_FitDif['name'])
                if Diff == 0:W = 0
                if Diff <> 0:W = SRow.getValue('Shape').length * SRow.getValue(F_AADT['name'])
                FitDic[SRow.getValue(F_TargetFID['name'])]['Seg' ].append(Diff)
                FitDic[SRow.getValue(F_TargetFID['name'])]['SegW'].append(W)

    for Field in [F_FitDif]:
        AddField(TargetLayer,Field)

    def WeightedAve(Vs1,Ws1,Vs2,Ws2):
        A1 = 0
        for i in range(0,len(Vs1)):
            A1 += Vs1[i]*Ws1[i]
        if sum(Ws1)<>0: A1 = float(A1)/sum(Ws1)
        A2 = 0
        for i in range(0,len(Vs2)):
            A2 += Vs2[i]*Ws2[i]
        if sum(Ws2)<>0: A2 = float(A2)/sum(Ws2)
        A = 0
        if A1<>0 and A2==0: A = A1
        if A1==0 and A2<>0: A = A2
        if A1<>0 and A2<>0: A = float(A1+A2)/2
        return A

    UC = arcpy.UpdateCursor(TargetLayer)
    for URow in UC:
        TFID = URow.getValue(F_TargetFID['name'])

        if TFID in FitDic.keys():
            URow.setValue(F_FitDif['name'],WeightedAve(FitDic[TFID]['Int'],FitDic[TFID]['IntW'],FitDic[TFID]['Seg'],FitDic[TFID]['SegW']))
        UC.updateRow(URow)

    for Field in [F_TargetFID]:
        arcpy.DeleteField_management(TargetLayer,Field['name'])

    arcpy.CopyFeatures_management(TargetLayer, Output)
    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")
def ImportAreaFromHotspot(TargetInputs,JoinInput,AreaField,ReadArea,OutputFolder):
    arcpy.AddMessage(" ")
    arcpy.AddMessage("    Import Area From Hotspot")

    AreaF  = {'name': AreaField,'alias': AreaField}; AreaF.update(FT_Short2)

    arcpy.AddMessage("    Copy Features: Join Layer")
    JoinLayer = CopyFeatures(JoinInput,'JFTargetLLL')
    TotalTargets = arcpy.GetCount_management(JoinLayer)
    arcpy.AddMessage("     - Total number of Items Found: " + str(TotalTargets))

    arcpy.AddMessage("    Add Fields: Join Layer")
    for Field in [F_JoinFID]:
        AddField(JoinLayer,Field)
    CalField(JoinLayer,F_JoinFID,'!OBJECTID!')
    AreaDic = {SRow.getValue(F_JoinFID['name']):SRow.getValue(ReadArea) for SRow in arcpy.SearchCursor(JoinLayer)}

    for TargetInput in TargetInputs.split(';'):
        arcpy.AddMessage("    Copy Features: " + TargetInput + " Layer")
        TargetLayer = CopyFeatures(TargetInput,'JFTarget')
        TotalU = arcpy.GetCount_management(TargetLayer)
        arcpy.AddMessage("     - Total number of Items Found: " + str(TotalU))

        arcpy.AddMessage("    Add Fields: " + TargetLayer + " Layer")
        for Field in [AreaF,F_TargetFID]:
            AddField(TargetLayer,Field)
        CalField(TargetLayer,F_TargetFID,'!OBJECTID!')
        
        TargetDic = {SRow.getValue(F_TargetFID['name']):0 for SRow in arcpy.SearchCursor(TargetLayer)}

        arcpy.AddMessage("    Spatial Join: " + TargetLayer + " + Join Layer")
        USPJ = SpatialJoin(TargetLayer, JoinLayer, 'UrbUSPJ', {'join_operation': "JOIN_ONE_TO_ONE", 'join_type': "KEEP_COMMON", 'field_mapping': '', 'match_option': 'INTERSECT', 'search_radius': '', 'distance_field_name': ''})

        for SRow in arcpy.SearchCursor(USPJ):
            TFID = SRow.getValue(F_TargetFID['name'])
            JFID = SRow.getValue(F_JoinFID['name'])
            TargetDic[TFID] = AreaDic[JFID]

        UC = arcpy.UpdateCursor(TargetLayer)
        for URow in UC:
            TFID = URow.getValue(F_TargetFID['name'])
            if TFID in TargetDic.keys():
                URow.setValue(AreaF['name'],TargetDic[TFID])
            UC.updateRow(URow)

        for Field in [F_TargetFID]:
            arcpy.DeleteField_management(TargetLayer,Field['name'])

        Output = OutputFolder + '\\' + TargetInput + '.shp'
        CopyFeatures(TargetLayer,Output)

    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")

#  Intersections
### Tool Scripts
def CreateIntersectionPointsSC(Input, Radius, Tollerance, DegreeTollerance, Output):
    import json 

    arcpy.AddMessage(" ")
    arcpy.AddMessage("   Create Intersections From Roads")

    OutDic = OutputParser(Output, 'shp')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("   Copy Features: Roads Layer")
    RoadsLayer = CopyFeatures(Input, "IfRInput")
    TotalRoads = int(str(arcpy.GetCount_management(RoadsLayer)))
    arcpy.AddMessage("    - Total: " + str(TotalRoads))
    
    arcpy.AddMessage("   Projec: Roads Layer")
    RoadsLayer = MakeFeatureLayer(RoadsLayer, "R_L")
    RoadsLayer = Project(RoadsLayer)

    RoadsLayer = MakeFeatureLayer(RoadsLayer,'IRLayer')
    arcpy.SelectLayerByAttribute_management(RoadsLayer,"NEW_SELECTION",'"Route_Type"<>14')
    
    arcpy.AddMessage("   Feature to Line: Roads Layer")
    RoadsLayer = FeatureToLine(RoadsLayer, "RoadLayer_F2L",str(Tollerance) + " Feet")
    After = int(str(arcpy.GetCount_management(RoadsLayer)))
    arcpy.AddMessage("    - Total: " + str(After))

    arcpy.AddMessage("   Add Field: Roads Layer")
    AddField(RoadsLayer,F_RouteFID)
    arcpy.CalculateField_management(RoadsLayer,F_RouteFID['name'],"!OBJECTID!","PYTHON_9.3")
    RoadDic = {SRow.getValue(F_RouteFID['name']):SRow.getValue('Shape') for SRow in arcpy.SearchCursor(RoadsLayer)}

    arcpy.AddMessage("   Intersect: Roads Layer")
    ptemp = Intersect(RoadsLayer, "I_Int",{'join_attributes':"ONLY_FID",'cluster_tolerance':str(Tollerance)+" Feet",'output_type':"POINT"})
    arcpy.AddMessage("    - Total Items: " + str(int(str(arcpy.GetCount_management(ptemp)))) + " Points")

    arcpy.AddMessage("   Delete Identical: Intersect Layer")
    arcpy.DeleteIdentical_management(ptemp,'Shape',str(Tollerance)+" Feet")
    arcpy.AddMessage("    - Total Items: " + str(int(str(arcpy.GetCount_management(ptemp)))) + " Points")

    arcpy.AddMessage("   Add Field: Intersect Layer")
    AddField(ptemp,F_TargetFID)
    arcpy.CalculateField_management(ptemp,F_TargetFID['name'],"!OBJECTID!","PYTHON_9.3")
    IntDic = {SRow.getValue(F_TargetFID['name']):{'X':SRow.getValue('Shape').centroid.X,
                                                  'Y':SRow.getValue('Shape').centroid.Y,
                                                  'Leg':0,'Deg':0,'Diff':0,'Flag':False,'Routes':{}} for SRow in arcpy.SearchCursor(ptemp)}

    arcpy.AddMessage("   Spatial Join: Intersect Layer & Roads Layer")
    USPJ = SpatialJoin(ptemp, RoadsLayer, 'PointSPJ', {'join_operation': "JOIN_ONE_TO_MANY", 'join_type': "KEEP_COMMON", 'field_mapping': '', 'match_option': 'INTERSECT', 'search_radius': str(Radius)+" Feet", 'distance_field_name': ''})
    
    arcpy.AddMessage("   Search Cursor: Spatial Join Layer")
    def FindAngle(O,P):
            import math
            if P[0] == O[0]:
                 if P[1] == O[1]:
                     #arcpy.AddWarning(str(O) + str(P))
                     return 0 #1
                 else:
                     if P[1] > O[1]:
                         return 90  #2
                     if P[1] < O[1]:
                         return 270 #3
            else:
                if P[1] == O[1]:
                    if P[0] > O[0]:
                        return 0 #4
                    else:
                        return 180 #5
                else:
                    if   (P[0] - O[0]) > 0 and (P[1] - O[1]) > 0:
                        return math.degrees(math.atan((P[1] - O[1]) / (P[0] - O[0]))) #6
                    elif (P[0] - O[0]) > 0 and (P[1] - O[1]) < 0:
                        return 360 - math.degrees(math.atan(-(P[1] - O[1]) / (P[0] - O[0]))) #7
                    elif (P[0] - O[0]) < 0 and (P[1] - O[1]) > 0:
                        return 180 - math.degrees(math.atan(-(P[1] - O[1]) / (P[0] - O[0]))) #8
                    elif (P[0] - O[0]) < 0 and (P[1] - O[1]) < 0:
                        return 180 + math.degrees(math.atan((P[1] - O[1]) / (P[0] - O[0])))
    def FindClosestPoint(PolylineList,IntPoint):
            n = len(PolylineList)
            Dist0 = ((PolylineList[0    ][0] - IntPoint[0]) ** 2 + (PolylineList[0    ][1] - IntPoint[1]) ** 2) ** 0.5
            Distn = ((PolylineList[n - 1][0] - IntPoint[0]) ** 2 + (PolylineList[n - 1][1] - IntPoint[1]) ** 2) ** 0.5
            if Dist0 <= Distn:
                return [PolylineList[0  ],PolylineList[1  ]]
            else:
                return [PolylineList[n-1],PolylineList[n-2]]
    def PopCloseDeg(DegList,Eps):
            Flag = False
            for i in range(0,len(DegList) - 1):
                A = DegList[i]
                for j in range(i + 1,len(DegList)):
                    B = DegList[j] 
                    if (A - B) ** 2 < Eps ** 2:
                        DegList.pop(j) 
                        Flag = True
                        break
                if Flag:
                    break
            return {'List':DegList,'Flag':Flag}
    SC = arcpy.SearchCursor(USPJ)
    for SRow in SC:
        TFID = SRow.getValue(F_TargetFID['name'])
        RFID = SRow.getValue(F_RouteFID['name'])
        PI = [IntDic[TFID]['X'],IntDic[TFID]['Y']]
        PR = FindClosestPoint(json.loads(RoadDic[RFID].JSON)['paths'][0],PI)
        Deg = FindAngle(PR[0],PR[1])
        if RoadDic[RFID].length > float(Radius):
            IntDic[TFID]['Routes'].update({RFID:
            {'Length':RoadDic[RFID].length,'Deg':Deg,'Number':SRow.getValue('Route_Numb'),'RCT':SRow.getValue('Route_Type'),'DRP':SRow.getValue('DirePoly')}})

    arcpy.AddMessage("   Clean up the Points ...")
    OverlayedPoly = 0
    for TFID in IntDic.keys():
        Flag = True
        Deg = [IntDic[TFID]['Routes'][RFID]['Deg'] for RFID in IntDic[TFID]['Routes'].keys()]
        while Flag:
            Dic = PopCloseDeg(Deg,float(DegreeTollerance))
            Deg = Dic['List']
            Flag = Dic['Flag']
            if Flag: OverlayedPoly = OverlayedPoly+1
    arcpy.AddMessage("     - Overlayed Polylines: " + str(OverlayedPoly))
    
    InterstateCrossRoads = 0
    for TFID in IntDic.keys():
        legs = len(IntDic[TFID]['Routes'].keys())
        if legs>3:
            for RFID in IntDic[TFID]['Routes'].keys():
             if IntDic[TFID]['Routes'][RFID]['DRP'] ==1:
                 IntDic[TFID]['Routes'].pop(RFID)
                 InterstateCrossRoads = InterstateCrossRoads+1
    arcpy.AddMessage("     - Interstate Cross Roads: " + str(InterstateCrossRoads))

    AuxRamps = 0
    for TFID in IntDic.keys():
        legs = len(IntDic[TFID]['Routes'].keys())
        RCT = [IntDic[TFID]['Routes'][RFID]['RCT'] for RFID in IntDic[TFID]['Routes'].keys()]
        RCT = list(set(RCT))
        RCT.sort()
        DRP = [IntDic[TFID]['Routes'][RFID]['DRP'] for RFID in IntDic[TFID]['Routes'].keys()]
        DRP = list(set(DRP))
        DRP.sort()
        if legs==3 and 5 in RCT and not 1 in RCT and not 1 in DRP:
            for RFID in IntDic[TFID]['Routes'].keys():
             if IntDic[TFID]['Routes'][RFID]['RCT'] ==5:
                 IntDic[TFID]['Routes'].pop(RFID)
                 AuxRamps = AuxRamps+1
    arcpy.AddMessage("     - Auxiliary Ramps: " + str(AuxRamps))

    TwoLegs = 0
    Confused4Leg = 0
    RmapOnRamp = 0
    for TFID in IntDic.keys():
        Flag = False
        Deg = [IntDic[TFID]['Routes'][RFID]['Deg'] for RFID in IntDic[TFID]['Routes'].keys()]
        Legs   = len(Deg)
        
        Deg = [int(d) for d in Deg]
        Deg.sort()
        
        Diff = [0]
        if  len(IntDic[TFID]['Routes'].keys()) > 1: Diff = [int(abs(360-Deg[len(Deg)-1]+Deg[0]))]
        for i in range(1,len(Deg)):
            Diff.append(int(abs(Deg[i]-Deg[i-1])))
        Diff.sort()
        
        RCT = [IntDic[TFID]['Routes'][RFID]['RCT'] for RFID in IntDic[TFID]['Routes'].keys()]
        RCT = list(set(RCT))
        RCT.sort()

        if Legs == 4 and True in [d>160 for d in Diff]: 
            Confused4Leg = Confused4Leg+1
            Legs = 3
        if Legs<3:
            TwoLegs = TwoLegs+1 
            Flag = True
        if RCT in [[5],[5,6],[6]]: 
            RmapOnRamp = RmapOnRamp+1
            Flag = True
        IntDic[TFID]['Deg' ] = Deg
        IntDic[TFID]['Leg' ] = Legs
        IntDic[TFID]['Diff'] = Diff
        IntDic[TFID]['Flag'] = Flag
        #arcpy.AddMessage(str([TFID,Deg,Legs,Flag]))
    arcpy.AddMessage("     - Two Legs: " + str(TwoLegs))
    arcpy.AddMessage("     - Ramp on Ramp: " + str(RmapOnRamp))
    arcpy.AddMessage("     - K 4 legs => 3 legs: " + str(Confused4Leg))

    arcpy.AddMessage("   Create Layer: Intersection Layer")
    All_Intersections = CreateFeatureclass('CI_Int',{'geometry_type':"POINT",'has_m':'ENABLED','has_z':'ENABLED'})

    FieldDic = [F_X, F_Y, F_LEGS, F_Degrees, F_Diff]
    for rec in FieldDic:
        AddField(All_Intersections,rec)

    arcpy.AddMessage("   Project: Intersection Layer")
    arcpy.DefineProjection_management(All_Intersections,CoordSystemSC)

    arcpy.AddMessage("   Insert Cursor: Intersection Layer")
    Pt = arcpy.Point()
    IC = arcpy.InsertCursor(All_Intersections) 
    ii = 0
    for TFID in IntDic.keys():
        if not IntDic[TFID]['Flag']:
            IRow = IC.newRow() 
            Pt.X = IntDic[TFID]['X']
            Pt.Y = IntDic[TFID]['Y']
            IRow.setValue(F_X['name'],Pt.X)
            IRow.setValue(F_Y['name'],Pt.Y)
            IRow.setValue(F_LEGS   ['name'],    IntDic[TFID]['Leg' ])
            IRow.setValue(F_Degrees['name'],str(IntDic[TFID]['Deg' ]))
            IRow.setValue(F_Diff   ['name'],str(IntDic[TFID]['Diff']))
        
            IRow.shape = Pt
            IC.insertRow(IRow)      
            ii += 1         

    arcpy.AddMessage("    - Total " + str(ii) + " Intersections Inserted")
    Output = arcpy.CopyFeatures_management(All_Intersections,Output)

    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")
def CreateIntersectionPointsNC(Input,ClassField,OnewayField,RtNumField,Output):
    import json 
    BufferSize = 100

    arcpy.AddMessage(" ")
    arcpy.AddMessage("   Create Intersections From Roads")

    OutDic = OutputParser(Output, 'shp')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("   Copy Features: Roads Layer")
    RoadsLayer = CopyFeatures(Input, "IfRInput")
    TotalRoads = int(str(arcpy.GetCount_management(RoadsLayer)))
    arcpy.AddMessage("    - Total: " + str(TotalRoads))
    
    #arcpy.AddMessage("   Clearing Fields")
    #RoadsLayer = ClearFields(RoadsLayer)

    arcpy.AddMessage("   Adding Route FID")
    AddField(RoadsLayer,F_RouteFID)
    arcpy.CalculateField_management(RoadsLayer,F_RouteFID['name'],"!OBJECTID!","PYTHON_9.3")

    arcpy.AddMessage("   Adding Projection")
    RoadsLayer = MakeFeatureLayer(RoadsLayer, "R_L")
    RoadsLayer = Project(RoadsLayer,CoordSystemNC)

    arcpy.AddMessage("   Feature to Line: Roads Layer")
    RoadsLayer = FeatureToLine(RoadsLayer, "RoadLayer_F2L")
    After = int(str(arcpy.GetCount_management(RoadsLayer)))
    arcpy.AddMessage("    - Total: " + str(After))

    arcpy.AddMessage("   Writing Coordinates")
    FieldList = [F_X0 ,F_Y0, F_X1, F_Y1, F_X2, F_Y2, F_X3, F_Y3]
    for Field in FieldList:
        AddField(RoadsLayer,Field)
    #Cor = []
    UC = arcpy.UpdateCursor(RoadsLayer)

    for URow in UC:
        PL = json.loads(URow.getValue('Shape').JSON)['paths'][0]

        #F_0 = [PL[0][0], PL[0][1]]
        #F_1 = [PL[1][0], PL[1][1]]

        n = len(PL)
        #F_2 = [PL[n-2][0], PL[n-2][1]]
        #F_3 = [PL[n-1][0], PL[n-1][1]]
        #Cor.append([F_0,F_1,F_2,F_3])
        URow.setValue(F_X0['name'],PL[0][0])
        URow.setValue(F_Y0['name'],PL[0][1])

        URow.setValue(F_X1['name'],PL[1][0])
        URow.setValue(F_Y1['name'],PL[1][1])

        n = len(PL)
        URow.setValue(F_X2['name'],PL[n-2][0])
        URow.setValue(F_Y2['name'],PL[n-2][1])

        URow.setValue(F_X3['name'],PL[n-1][0])
        URow.setValue(F_Y3['name'],PL[n-1][1])
        UC.updateRow(URow)

    arcpy.AddMessage("   Performing Intersect Tool")
    ptemp = Intersect(RoadsLayer, "I_Int",{'join_attributes':"All",'cluster_tolerance':"",'output_type':"POINT"})
    arcpy.AddMessage("    - Total Items: " + str(int(str(arcpy.GetCount_management(ptemp)))) + " Points")

    arcpy.AddXY_management(ptemp)
    def ReadIntersectionsNC(inLayer,ClassField,OnewayField,RtNumField):
        import json 

        SC = arcpy.SearchCursor(inLayer)
        def FindClosestPoint(PolylineList,IntPoint):
            n = len(PolylineList)
            Dist0 = ((PolylineList[0][0] - IntPoint[0]) ** 2 + (PolylineList[0][1] - IntPoint[1]) ** 2) ** 0.5
            if Dist0 < 1:
                return PolylineList[1]
            else:
                Distn = ((PolylineList[n - 1][0] - IntPoint[0]) ** 2 + (PolylineList[n - 1][1] - IntPoint[1]) ** 2) ** 0.5
                if Distn < 1:
                    return PolylineList[n - 2]
                else:
                    arcpy.AddWarning('Dist0: ' + str(Dist0) + ', Distn: ' + str(Distn))
                    return [0,0]    

        X_Old = 0; Y_Old = 0
        X = []; Y = []; Routes = []
        FirstRow = True
        for SRow in SC:
            if not(X_Old == SRow.getValue("POINT_X") and Y_Old == SRow.getValue("POINT_Y")):
                X_Old = SRow.getValue("POINT_X")
                Y_Old = SRow.getValue("POINT_Y")
                X.append(X_Old)
                Y.append(Y_Old)
                if not FirstRow:
                    R = {'FID': FID, 'PX': PX, 'PY': PY, 'Class':Class,'Oneway':Oneway,'RtNum':RtNum}
                    Routes.append(R)
                FID = []
                PX = []
                PY = []
                Class = [];Oneway = [];RtNum = []
                
            FID.append(SRow.getValue(F_RouteFID['name']))
            PL = [[SRow.getValue(F_X0['name']),SRow.getValue(F_Y0['name'])],[SRow.getValue(F_X1['name']),SRow.getValue(F_Y1['name'])],[SRow.getValue(F_X2['name']),SRow.getValue(F_Y2['name'])],[SRow.getValue(F_X3['name']),SRow.getValue(F_Y3['name'])]]
            P = FindClosestPoint(PL,[X_Old,Y_Old])
            PX.append(P[0])
            PY.append(P[1])
            Class.append(SRow.getValue(ClassField))
            Oneway.append(SRow.getValue(OnewayField))
            RtNum.append(SRow.getValue(RtNumField))
            FirstRow = False
        
        R = {'FID': FID, 'PX': PX, 'PY': PY, 'Class':Class,'Oneway':Oneway,'RtNum':RtNum}
        Routes.append(R)
        Intersections = {'X': X, 'Y': Y, 'Routes': Routes}
        return Intersections #Intersections From RIMS - Points

    arcpy.AddMessage("   Generating Intersections Layer ...")
    Intersections = ReadIntersectionsNC(ptemp,ClassField,OnewayField,RtNumField)
    arcpy.AddMessage("    - Total " + str(len(Intersections['X'])) + " Intersections Found")


    def FindAngle(O,P):
        import math
        if P[0] == O[0]:
             if P[1] == O[1]:
                 #arcpy.AddWarning(str(O) + str(P))
                 return 0 #1
             else:
                 if P[1] > O[1]:
                     return 90  #2
                 if P[1] < O[1]:
                     return 270 #3
        else:
            if P[1] == O[1]:
                if P[0] > O[0]:
                    return 0 #4
                else:
                    return 180 #5
            else:
                if   (P[0] - O[0]) > 0 and (P[1] - O[1]) > 0:
                    return math.degrees(math.atan((P[1] - O[1]) / (P[0] - O[0]))) #6
                elif (P[0] - O[0]) > 0 and (P[1] - O[1]) < 0:
                    return 360 - math.degrees(math.atan(-(P[1] - O[1]) / (P[0] - O[0]))) #7
                elif (P[0] - O[0]) < 0 and (P[1] - O[1]) > 0:
                    return 180 - math.degrees(math.atan(-(P[1] - O[1]) / (P[0] - O[0]))) #8
                elif (P[0] - O[0]) < 0 and (P[1] - O[1]) < 0:
                    return 180 + math.degrees(math.atan((P[1] - O[1]) / (P[0] - O[0])))
    def PopCloseDeg(DegList):
        Flag = False
        for i in range(0,len(DegList) - 1):
            A = DegList[i]
            for j in range(i + 1,len(DegList)):
                B = DegList[j] 
                if (A - B) ** 2 < 4:
                    DegList.pop(j) 
                    Flag = True
                    break
            if Flag:
                break
        return {'List':DegList,'Flag':Flag}
    def CountLegs(I,i):
        Deg = []
        for j in range(0,len(I['Routes'][i]['PX'])):
            Deg.append(FindAngle([I['X'][i],I['Y'][i]] , [I['Routes'][i]['PX'][j],I['Routes'][i]['PY'][j]]))
        #arcpy.AddMessage(str(Deg))
        Flag = True
        while Flag:
            Dic = PopCloseDeg(Deg)
            Deg = Dic['List']
            Flag = Dic['Flag']
    
        return Deg 

    arcpy.AddMessage("   Calculating the Attributes")
    Intersections.update({'Legs' : []})
    Intersections.update({'Degs' : []})
    Intersections.update({'Diffs': []})
    for i in range(0,len(Intersections['X'])):
        Deg = CountLegs(Intersections,i)
        Deg = [int(d) for d in Deg]
        Deg.sort()
        Diff = [int(abs(360-Deg[len(Deg)-1]+Deg[0]))]
        for i in range(1,len(Deg)):
            Diff.append(int(abs(Deg[i]-Deg[i-1])))
        Diff.sort()
        Intersections['Degs' ].append(Deg)
        Intersections['Diffs'].append(Diff)
        Intersections['Legs' ].append(len(Deg))
    
    arcpy.AddMessage("   Creating Layer and Adding Fields")
    All_Intersections = CreateFeatureclass('CI_Int',{'geometry_type':"POINT",'has_m':'ENABLED','has_z':'ENABLED'})

    FieldDic = [F_X, F_Y, F_LEGS, F_Degrees, F_Diff, F_RefFID]
    for rec in FieldDic:
        AddField(All_Intersections,rec)

    arcpy.AddMessage("   Defining Projection")
    arcpy.DefineProjection_management(All_Intersections,CoordSystemNC)

    arcpy.AddMessage("   Insert Cursur: Intersection Layer")
    Pt = arcpy.Point()
    IC = arcpy.InsertCursor(All_Intersections) 

    for i in range(0,len(Intersections['X'])):
        Flag = False
        Class  = Intersections['Routes'][i]['Class']
        Oneway = Intersections['Routes'][i]['Oneway']
        Legs   = Intersections['Legs'][i]
        Degs   = Intersections['Degs'][i]
        Diffs  = Intersections['Diffs'][i]
        if 'I' in Class:
            Flag = True
        if Legs == 3 and Class == ['RMP','RMP','RMP']:
            Flag = True
        if Legs == 3 and Oneway == [1,1,1] and 'RMP' in Class: #Exit
            Flag = True
        if Legs == 4 and True in [d>160 for d in Diffs]:
            Legs = 3
            Intersections['Legs'][i] = 3
        if Legs == 3: #Forks
            j = 0
            for d in Diffs:
                if d >= 140:
                    j += 1
            if j == 2:
                Flag = True
        #Rtn = []    #route number
        #RtI = []    #route number identifier
        #RtC = []    #count route numbers
        #for n in Intersections['Routes'][i]['RtNum']:
        #    c = 0
        #    for m in Intersections['Routes'][i]['RtNum']:
        #        if n==m:
        #            c += 1
        #    Rtn.append(int(str(n)[4:]))
        #    RtI.append(int(str(n)[2]))
        #    RtC.append(c)
        
        #Pop = 0
        #for ii in range(0,len(RtC)):
        #    if RtC[ii]>1:
        #        for j in range(0,len(RtC)):
        #            if ii<>j and Rtn[ii]==Rtn[j] and RtI[ii]<>RtI[j]:
        #                Pop += 1
        #Legs -= Pop
        #Intersections['Legs'][i] -= Pop

        if Legs > 2 and not Flag:
            IRow = IC.newRow() 
            Pt.X = Intersections['X'][i]
            Pt.Y = Intersections['Y'][i]
        
            IRow.setValue(F_LEGS['name'],Legs)
            IRow.setValue(F_Degrees['name'],str(Degs))
            IRow.setValue(F_Diff['name'],str(Diffs))
            IRow.setValue(F_X['name'],Pt.X)
            IRow.setValue(F_Y['name'],Pt.Y)
            IRow.setValue(F_RefFID['name'],i)
        
            IRow.shape = Pt
            IC.insertRow(IRow)             
    arcpy.AddMessage("    - Total " + str(int(str(arcpy.GetCount_management(All_Intersections)))))


    arcpy.AddMessage("   Spatial Join: Intersection Layer")
    SPJ = SpatialJoin(All_Intersections, All_Intersections, "IntLayer_SPJ1", {'join_operation': "JOIN_ONE_TO_MANY", 'join_type': "KEEP_ALL",'field_mapping': "",'match_option': "WITHIN_A_DISTANCE",'search_radius': str(BufferSize) + " Feet",'distance_field_name':''})
    After = int(str(arcpy.GetCount_management(SPJ)))
    arcpy.AddMessage("    - Total: " + str(After))

    arcpy.AddMessage("   Finding in Range Intersections")
    IRDic = {SRow.getValue('OBJECTID'):{'RefIDs':[], 'FIDs':[]} for SRow in arcpy.SearchCursor(All_Intersections)}
    RefDic = {SRow.getValue('OBJECTID'):SRow.getValue(F_RefFID['name']) for SRow in arcpy.SearchCursor(All_Intersections)}

    RMList = []
    for SRow in arcpy.SearchCursor(SPJ):
        t = SRow.getValue("TARGET_FID")
        j = SRow.getValue("JOIN_FID")
        if t != j and not (j in RMList):
            IRDic[t]['FIDs'].append(j)
            IRDic[t]['RefIDs'].append(RefDic[j])
            RMList.append(j)
            if not t in IRDic[t]['FIDs']:
                IRDic[t]['FIDs'].append(t)
                IRDic[t]['RefIDs'].append(RefDic[t])
                RMList.append(t)
    
    for k in IRDic.keys():
        if IRDic[k]['FIDs'] == []:
            del IRDic[k]

    UC = arcpy.UpdateCursor(All_Intersections)
    for URow in UC:
        if URow.getValue('OBJECTID') in RMList:
            UC.deleteRow(URow)
    del UC
    TotalInt = MaximumValue(All_Intersections,F_RefFID['name'])
    IC = arcpy.InsertCursor(All_Intersections)
    for k in IRDic.keys():
        Pt.X = 0
        Pt.Y = 0
        LegList = []
        for i in IRDic[k]['RefIDs']:
            Pt.X += Intersections['X'][i]
            Pt.Y += Intersections['Y'][i]
            LegList.append(Intersections['Legs'][i])
        Pt.X = Pt.X / len(IRDic[k]['RefIDs'])
        Pt.Y = Pt.Y / len(IRDic[k]['RefIDs'])
        
        IRow = IC.newRow()
        #arcpy.AddMessage(LegList)
        Legs = 4 
        if 3 in LegList:
            Legs = 3
        TotalInt += 1
        IRow.setValue(F_LEGS['name'],Legs)
        IRow.setValue(F_Degrees['name'],0)
        IRow.setValue(F_Diff['name'],0)
        IRow.setValue(F_X['name'],Pt.X)
        IRow.setValue(F_Y['name'],Pt.Y)
        IRow.setValue(F_RefFID['name'],TotalInt)
      
        IRow.shape = Pt
        IC.insertRow(IRow)    
    arcpy.AddMessage("    - Total " + str(int(str(arcpy.GetCount_management(All_Intersections)))))

    arcpy.AddMessage("   Spatial Join: Intersection Layer")
    SPJ = SpatialJoin(All_Intersections, All_Intersections, "IntLayer_SPJ2", {'join_operation': "JOIN_ONE_TO_MANY", 'join_type': "KEEP_ALL",'field_mapping': "",'match_option': "WITHIN_A_DISTANCE",'search_radius': str(BufferSize) + " Feet",'distance_field_name':''})
    After = int(str(arcpy.GetCount_management(SPJ)))
    arcpy.AddMessage("    - Total: " + str(After))

    arcpy.AddMessage("   Finding in Range Intersections")
    IRDic = {SRow.getValue('OBJECTID'):{'X':[],'Y': [],'LEGS':[], 'FIDs':[]} for SRow in arcpy.SearchCursor(All_Intersections)}
    RefDic = {SRow.getValue('OBJECTID'):SRow.getValue(F_RefFID['name']) for SRow in arcpy.SearchCursor(All_Intersections)}

    RMList = []
    for SRow in arcpy.SearchCursor(SPJ):
        t = SRow.getValue("TARGET_FID")
        j = SRow.getValue("JOIN_FID")
        if t != j and not (j in RMList):
            IRDic[t]['FIDs'].append(j)
            IRDic[t]['X'   ].append(SRow.getValue(F_X   ['name']))
            IRDic[t]['Y'   ].append(SRow.getValue(F_Y   ['name']))
            IRDic[t]['LEGS'].append(SRow.getValue(F_LEGS['name']))
            RMList.append(j)
            if not t in IRDic[t]['FIDs']:
                IRDic[t]['FIDs'].append(t)
                IRDic[t]['X'   ].append(SRow.getValue(F_X   ['name']))
                IRDic[t]['Y'   ].append(SRow.getValue(F_Y   ['name']))
                IRDic[t]['LEGS'].append(SRow.getValue(F_LEGS['name']))
                RMList.append(t)
    
    for k in IRDic.keys():
        if IRDic[k]['FIDs'] == []:
            del IRDic[k]

    UC = arcpy.UpdateCursor(All_Intersections)
    for URow in UC:
        if URow.getValue('OBJECTID') in RMList:
            UC.deleteRow(URow)
    del UC

    IC = arcpy.InsertCursor(All_Intersections)
    TotalInt = MaximumValue(All_Intersections,F_RefFID['name'])
    for k in IRDic.keys():
        Pt.X = 0
        Pt.Y = 0
        LegList = []
        for x in IRDic[k]['X']:
            Pt.X += x
        for y in IRDic[k]['Y']:
            Pt.Y += y
        for l in IRDic[k]['LEGS']:
            LegList.append(l)
        Pt.X = Pt.X / len(IRDic[k]['X'])
        Pt.Y = Pt.Y / len(IRDic[k]['Y'])
        
        IRow = IC.newRow()
        #arcpy.AddMessage(LegList)
        Legs = 4 
        if 3 in LegList:
            Legs = 3
        TotalInt += 1
        IRow.setValue(F_LEGS['name'],Legs)
        IRow.setValue(F_Degrees['name'],0)
        IRow.setValue(F_Diff['name'],0)
        IRow.setValue(F_X['name'],Pt.X)
        IRow.setValue(F_Y['name'],Pt.Y)
        IRow.setValue(F_RefFID['name'],TotalInt)
      
        IRow.shape = Pt
        IC.insertRow(IRow)    
    arcpy.AddMessage("    - Total " + str(int(str(arcpy.GetCount_management(All_Intersections)))))
    Output = arcpy.CopyFeatures_management(All_Intersections,Output)

    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")
def AddSignal(IntInput,SignalInput,SearchRadius,Output):
    arcpy.AddMessage(" ")
    arcpy.AddMessage("   Import Signal Data")

    OutDic = OutputParser(Output, 'shp')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("   Copy Features: Ints Layer")
    RoadsLayer = CopyFeatures(IntInput, "SGInt")
    TotalRoads = int(str(arcpy.GetCount_management(RoadsLayer)))
    arcpy.AddMessage("    - Total: " + str(TotalRoads))
    
    arcpy.AddMessage("   Copy Features: Signal Layer")
    SignalLayer = CopyFeatures(SignalInput, "SGSignal")
    TotalRoads = int(str(arcpy.GetCount_management(SignalLayer)))
    arcpy.AddMessage("    - Total: " + str(TotalRoads))
    
    arcpy.AddMessage("   Adding Fields")
    AddField(RoadsLayer , F_TargetFID)
    AddField(RoadsLayer , F_SG)
    CalField(RoadsLayer , F_TargetFID,'!OBJECTID!')
    AddField(SignalLayer, F_JoinFID)
    CalField(SignalLayer, F_JoinFID,'!OBJECTID!')

    arcpy.AddMessage("   Spatial Join: Signalized + Ints Layer")
    SPJ = SpatialJoin(SignalLayer, RoadsLayer, "Int_Spat", {'join_operation':"JOIN_ONE_TO_ONE",'join_type':"KEEP_ALL", 'field_mapping':'', 'match_option':"CLOSEST",'search_radius':str(SearchRadius)+" Feet",'distance_field_name':''})
    AddDic = [{'X':SRow.getValue('Shape').centroid.X,'Y':SRow.getValue('Shape').centroid.Y} for SRow in arcpy.SearchCursor(SPJ) if SRow.getValue('Join_Count') == 0]
    IDic   = {SRow.getValue(F_TargetFID['name']):1 for SRow in arcpy.SearchCursor(SPJ) if SRow.getValue('Join_Count') > 0}

    arcpy.AddMessage("   Insert Cursor: Ints Layer")
    IC = arcpy.InsertCursor(RoadsLayer)
    j = 0
    Pt = arcpy.Point()
    for OID in AddDic:
        IRow = IC.newRow()
        IRow.setValue(F_SG['name'],1)
        Pt.X = OID['X']
        Pt.Y = OID['Y']
        IRow.shape = Pt
        IRow.setValue(F_LEGS['name'],4)
        IRow.setValue(F_X['name'],Pt.X)
        IRow.setValue(F_Y['name'],Pt.Y)
        IC.insertRow(IRow)
        j += 1
    arcpy.AddMessage("    - Total Signals Added: " + str(j))
    
    arcpy.AddMessage("   Update Cursor: Ints Layer")
    SC = arcpy.UpdateCursor(RoadsLayer)
    j = 0
    for SRow in SC:
        f = SRow.getValue('OBJECTID')
        if f in IDic.keys():
            SRow.setValue(F_SG['name'],1)
            j += 1
        else:
            SRow.setValue(F_SG['name'],0)
        SC.updateRow(SRow)
    arcpy.AddMessage("    - Total Signals Found: " + str(j))


    arcpy.DeleteField_management(RoadsLayer,F_TargetFID['name'])
          
    arcpy.CopyFeatures_management(RoadsLayer,Output)
    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")
def AddInterchange(Input,BridgeInput,AADTMajorLimit,AADTMinorLimit,Output):
    arcpy.AddMessage(" ")
    arcpy.AddMessage("   Add Intersection Type and Buffer")

    OutDic = OutputParser(Output, 'shp')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("   Copy Features: Ints Layer")
    RoadsLayer = CopyFeatures(Input, "CCRoad")
    TotalRoads = int(str(arcpy.GetCount_management(RoadsLayer)))
    arcpy.AddMessage("    - Total: " + str(TotalRoads))
    
    arcpy.AddMessage("   Adding Fields")
    AddField(RoadsLayer,F_FType)
    AddField(RoadsLayer,F_IC)

    arcpy.AddMessage("   Calculate Field: Interchange")
    CB = '''def FindIC(Legs, Signal, RCTMajor, RCTMinor, AADTMajor, AADTMinor, AADTMajorLIM, AADTMinorLIM):
        IC = 0
        if 1 in [RCTMajor,RCTMinor] and not 5 in [RCTMajor,RCTMinor]: IC = 1
        if AADTMajor > AADTMajorLIM and AADTMinor > AADTMinorLIM and Signal == 0 and Legs > 3: IC = 1 

        return IC'''
    CalField(RoadsLayer,F_IC,"FindIC(!LEGS!,!SG!,!RCT_Major!,!RCT_Minor!,!AADT_Major!,!AADT_Minor!,"+str(AADTMajorLimit)+","+str(AADTMinorLimit)+")",CB)

    arcpy.CopyFeatures_management(RoadsLayer,Output)
    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")
def AddIntType(Input,Output):
    arcpy.AddMessage(" ")
    arcpy.AddMessage("   Add Intersection Type and Buffer")

    OutDic = OutputParser(Output, 'shp')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("   Copy Features: Ints Layer")
    RoadsLayer = CopyFeatures(Input, "CCRoad")
    TotalRoads = int(str(arcpy.GetCount_management(RoadsLayer)))
    arcpy.AddMessage("    - Total: " + str(TotalRoads))
    
    arcpy.AddMessage("   Adding Fields")
    AddField(RoadsLayer,F_FType)
    #AddField(RoadsLayer,F_IC)

    #arcpy.AddMessage("   Calculate Field: Interchange")
    #CB = '''def FindIC(Legs, Signal, RCTMajor, RCTMinor, AADTMajor, AADTMinor, AADTMajorLIM, AADTMinorLIM):
    #    IC = 0
    #    if 1 in [RCTMajor,RCTMinor] and not 5 in [RCTMajor,RCTMinor]: IC = 1
    #    if AADTMajor > AADTMajorLIM and AADTMinor > AADTMinorLIM and Signal == 0 and Legs > 3: IC = 1 

    #    return IC'''
    #CalField(RoadsLayer,F_IC,"FindIC(!LEGS!,!SG!,!RCT_Major!,!RCT_Minor!,!AADT_Major!,!AADT_Minor!,"+str(AADTMajorLimit)+","+str(AADTMinorLimit)+")",CB)


    arcpy.AddMessage("   Calculate Field: Facility Type")
    CB = '''def FindIntType(Urban, Rural, LaneMajor, Legs, Signal,Type_Minor,Type_Major):
        S1 = ''
        if Rural == 1: S1 = 'R'
        if Urban == 1: S1 = 'U'
        
        S2_1 = ''
        if Rural == 1 and LaneMajor == 4: S2_1 = 'M'
        if Rural == 1 and LaneMajor >  4: S2_1 = 'H'
        if Urban == 1 and LaneMajor >= 6: S2_1 = 'H'
        S2_2 = str(Legs)
        S2 = S2_1 + S2_2

        S3 = 'ST'
        if Signal == 1: S3 = 'SG'

        if Legs == 3 and Type_Minor in ['U1EXR','R1EXR'] and Type_Major[-1] in ['D','F']:
            S2 = ''
            S3 = 'DIV'
        if Legs == 3 and Type_Minor in ['U1ENR','R1ENR','R1IR','R1OR','U1IR','U1OR'] and Type_Major[-1] in ['D','F']:
            S2 = ''
            S3 = 'MER'
        if Legs > 3 and Type_Minor in ['U1EXR','R1EXR','U1ENR','R1ENR','R1IR','R1OR','U1IR','U1OR']:
            S3 = S3+'R'

        return S1 + S2 + S3'''
    CalField(RoadsLayer,F_FType,"FindIntType(!URBAN!,!RURAL!,!Lane_Major!,!LEGS!,!SG!,!Type_Minor!,!Type_Major!)",CB)

    arcpy.CopyFeatures_management(RoadsLayer,Output)
    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")
def ImportIntersectionsAttributesSC(TargetInt,RoadsLayer,AADTField,SearchRadius,Output):

    arcpy.AddMessage(" ")
    arcpy.AddMessage("    Import Intersections Attributes")

    OutDic = OutputParser(Output, 'shp')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("    Copy Features: Target Intersections Layer")
    IntLayer = CopyFeatures(TargetInt,'IAttInput')
    TotalSites = arcpy.GetCount_management(IntLayer)
    arcpy.AddMessage("     - Total number of Items Found: " + str(TotalSites))

    arcpy.DeleteField_management(IntLayer,'FType')

    arcpy.AddMessage("    Add Fields: Target Intersections Layer")
    FieldList = [F_TargetFID, F_ABuffer, F_BBuffer, F_AADT_Major, F_AADT_Minor, F_RCT_Major, F_RCT_Minor, F_Lane_Major, F_Lane_Minor, F_MedT_Major, F_MedT_Minor, F_Type_Major, F_Type_Minor, F_TWid_Major, F_TWid_Minor]
    for Field in FieldList:
        arcpy.DeleteField_management(IntLayer,Field['name'])
        AddField(IntLayer,Field)
    UC = arcpy.UpdateCursor(IntLayer)
    for URow in UC:
        FID = GetFID(URow)
        URow.setValue(F_TargetFID['name'],FID)
        UC.updateRow(URow)

    arcpy.AddMessage("   Spatial Join: Intersections + Roads")
    SPJ = SpatialJoin(IntLayer, RoadsLayer, "IAttSPJ", {'join_operation':"JOIN_ONE_TO_MANY",'join_type':"KEEP_ALL", 'field_mapping':'', 'match_option':"INTERSECT",'search_radius':SearchRadius,'distance_field_name':''})
    
    arcpy.AddMessage("   Search Cursor: Spatial Join")
    IntDic = {SRow.getValue(F_TargetFID['name']):[] for SRow in arcpy.SearchCursor(SPJ)}
    for SRow in arcpy.SearchCursor(SPJ):
        IntDic[SRow.getValue(F_TargetFID['name'])].append(
        [GetIntVal(SRow,AADTField), GetFloatVal(SRow,F_SurWid_Tot['name'],30), GetFloatVal(SRow,F_Median_Wid['name'],10), GetIntVal(SRow,F_Route_Type['name'],0),
         GetIntVal(SRow,F_TotalLanes['name']), GetIntVal(SRow,F_Median_ID['name']), GetVal(SRow,F_FType['name'])])

    arcpy.AddMessage("   Update Cursor: Target Intersections Layer")
    UC = arcpy.UpdateCursor(IntLayer)
    for URow in UC:
        FID       = URow.getValue(F_TargetFID['name'])
        AADT      = [Route[0] for Route in IntDic[FID]]
        SurfWid   = [Route[1] for Route in IntDic[FID]]
        MedianWid = [Route[2] for Route in IntDic[FID]]
        RCT       = [Route[3] for Route in IntDic[FID]]
        Lanes     = [Route[4] for Route in IntDic[FID]]
        MedID     = [Route[5] for Route in IntDic[FID]]
        FType     = [Route[6] for Route in IntDic[FID]]

        MajorIndex = AADT.index(max(AADT))
        MinorIndex = AADT.index(min(AADT))
        if max(AADT)==0 or max(AADT) == min(AADT):
            MajorIndex = RCT.index(min(RCT))
            MinorIndex = RCT.index(max(RCT))

        if MajorIndex == MinorIndex and len(AADT)>MajorIndex+1:
            MinorIndex = MajorIndex + 1
        if MajorIndex == MinorIndex and len(AADT)-1<MajorIndex+1:
            MinorIndex = MajorIndex - 1

        if RCT[MajorIndex]==9 and RCT[MinorIndex]==7:
            MajorIndex = RCT.index(min(RCT))
            MinorIndex = RCT.index(max(RCT))
            #arcpy.AddWarning(str([MajorIndex,MinorIndex,AADT,RCT]))

        URow.setValue(F_AADT_Major['name'],AADT[MajorIndex])
        URow.setValue(F_AADT_Minor['name'],AADT[MinorIndex])
        
        URow.setValue(F_RCT_Major['name'],RCT[MajorIndex])
        URow.setValue(F_RCT_Minor['name'],RCT[MinorIndex])

        URow.setValue(F_Lane_Major['name'],Lanes[MajorIndex])
        URow.setValue(F_Lane_Minor['name'],Lanes[MinorIndex])

        URow.setValue(F_MedT_Major['name'],MedID[MajorIndex])
        URow.setValue(F_MedT_Minor['name'],MedID[MinorIndex])

        URow.setValue(F_Type_Major['name'],FType[MajorIndex])
        URow.setValue(F_Type_Minor['name'],FType[MinorIndex])

        MajorWidth = (0.75 * SurfWid[MajorIndex] + MedianWid[MajorIndex])
        MinorWidth = (0.75 * SurfWid[MinorIndex] + MedianWid[MinorIndex])
        ABuffer = 1.2 * (MajorWidth ** 2 + MinorWidth ** 2) ** 0.5
        BBuffer = 250

        URow.setValue(F_TWid_Major['name'],MajorWidth)
        URow.setValue(F_TWid_Minor['name'],MinorWidth)

        URow.setValue(F_ABuffer['name'],ABuffer)
        URow.setValue(F_BBuffer['name'],BBuffer)
        UC.updateRow(URow)

    Output = arcpy.CopyFeatures_management(IntLayer,Output)
    FieldList = [F_TargetFID]
    for Field in FieldList:
        arcpy.DeleteField_management(Output,Field['name'])
    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")
def ImportIntersectionsAttributesNC(TargetInt,RoadsLayer,SurWidField,MedianWidField,AADTField,TotLanesField,SearchRadius,Output):

    arcpy.AddMessage(" ")
    arcpy.AddMessage("    Import Intersections Attributes")

    OutDic = OutputParser(Output, 'shp')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("    Copy Features: Target Intersections Layer")
    IntLayer = CopyFeatures(TargetInt,'IAttInput')
    TotalSites = arcpy.GetCount_management(IntLayer)
    arcpy.AddMessage("     - Total number of Items Found: " + str(TotalSites))

    arcpy.AddMessage("    Add Fields: Target Intersections Layer")
    FieldList = [F_TargetFID, F_ABuffer, F_BBuffer, F_AADT_Major, F_AADT_Minor,F_TotalLanes]
    for Field in FieldList:
        arcpy.DeleteField_management(IntLayer,Field['name'])
        AddField(IntLayer,Field)
    UC = arcpy.UpdateCursor(IntLayer)
    for URow in UC:
        FID = GetFID(URow)
        URow.setValue(F_TargetFID['name'],FID)
        UC.updateRow(URow)

    arcpy.AddMessage("   Spatial Join: Intersections + Roads")
    SPJ = SpatialJoin(IntLayer, RoadsLayer, "IAttSPJ", {'join_operation':"JOIN_ONE_TO_MANY",'join_type':"KEEP_ALL", 'field_mapping':'', 'match_option':"INTERSECT",'search_radius':SearchRadius,'distance_field_name':''})
    
    arcpy.AddMessage("   Search Cursor: Spatial Join")
    IntDic = {SRow.getValue(F_TargetFID['name']):[] for SRow in arcpy.SearchCursor(SPJ)}
    for SRow in arcpy.SearchCursor(SPJ):
        IntDic[SRow.getValue(F_TargetFID['name'])].append({'AADT':GetVal(SRow,AADTField,0,True),'SurWid':GetVal(SRow,SurWidField,30,True),'MedianWid':GetVal(SRow,MedianWidField,10,True),'TotalLanes':GetVal(SRow,TotLanesField,2,True)})

    arcpy.AddMessage("   Update Cursor: Target Intersections Layer")
    UC = arcpy.UpdateCursor(IntLayer)
    for URow in UC:
        FID  = URow.getValue(F_TargetFID['name'])
        AADT      = [Route['AADT'] for Route in IntDic[FID]]
        SurfWid   = [Route['SurWid'] for Route in IntDic[FID]]
        MedianWid = [Route['MedianWid'] for Route in IntDic[FID]]
        TotLanes  = [Route['TotalLanes'] for Route in IntDic[FID]]

        URow.setValue(F_AADT_Major['name'],max(AADT))
        URow.setValue(F_AADT_Minor['name'],min(AADT))
        URow.setValue(F_TotalLanes['name'],max(TotLanes))

        MajorWidth = (0.75 * max(SurfWid) + max(MedianWid))
        MinorWidth = (0.75 * sum(SurfWid)/len(SurfWid) + sum(MedianWid)/len(MedianWid))
        ABuffer = 1.2 * (MajorWidth ** 2 + MinorWidth ** 2) ** 0.5
        if ABuffer < 15: ABuffer = 15
        #BBuffer = ABuffer * 2.5
        BBuffer = 250

        URow.setValue(F_ABuffer['name'],ABuffer)
        URow.setValue(F_BBuffer['name'],BBuffer)
        UC.updateRow(URow)

    Output = arcpy.CopyFeatures_management(IntLayer,Output)
    FieldList = [F_TargetFID]
    for Field in FieldList:
        arcpy.DeleteField_management(Output,Field['name'])
    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")
def AddCCMF(Input,Output):
    arcpy.AddMessage(" ")
    arcpy.AddMessage("   Add Combined CMF")

    OutDic = OutputParser(Output, 'shp')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("   Copy Features: Roads Layer")
    RoadsLayer = CopyFeatures(Input, "CCRoad")
    TotalRoads = int(str(arcpy.GetCount_management(RoadsLayer)))
    arcpy.AddMessage("    - Total: " + str(TotalRoads))
    
    arcpy.AddMessage("   Adding CCMF Field")
    AddField(RoadsLayer,F_CCMF)

    arcpy.AddMessage("   Calculating CCMF Field")
    CB = '''def CCMF(CMFLight,CMFSkew,CMFLTL,CMFRTL,CMFLTP,CMFNoRTR,CMFAlco,CMFSchool,CMFBus):
        if CMFLight==0 :CMFLight=1
        if CMFSkew==0  :CMFSkew=1
        if CMFLTL==0   :CMFLTL=1
        if CMFRTL==0   :CMFRTL=1
        if CMFLTP==0   :CMFLTP=1
        if CMFNoRTR==0 :CMFNoRTR=1
        if CMFBus==0   :CMFBus=1
        if CMFSchool==0:CMFSchool=1
        if CMFAlco==0  :CMFAlco=1
        return(CMFSkew*CMFLight*CMFLTL*CMFNoRTR*CMFRTL*CMFLTP*CMFBus*CMFSchool*CMFAlco)'''
    CalField(RoadsLayer,F_CCMF,"CCMF(!CMFLight!,!CMFSkew!,!CMFLTL!,!CMFRTL!,!CMFLTP!,!CMFNoRTR!,!CMFAlco!,!CMFSchool!,!CMFBus!)",CB)

    arcpy.CopyFeatures_management(RoadsLayer,Output)
    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")

# NC Codes
#General Functions
def ExtractXY(BM,EM,CM,P):
        import math 
        #BM: begining milepoint
        #EM: ending milepoint
        #CM: desired milepoint (crash milepoint)
        #P: list of polyline vertices [[xi,yi]]
        Pt = arcpy.Point()
        Pt.X = -1
        Pt.Y = -1
        n = len(P)
        L = []
        for i in range(0,n-1):
            L.append(math.sqrt((P[i+1][1]-P[i][1])**2+(P[i+1][0]-P[i][0])**2))
        TotL = sum(L)
        DL = float((CM-BM))/(EM-BM)*TotL
        CUL = 0
        for i in range(0,len(L)):
            CUL += L[i]
            if CUL >= DL:
                Y1 = P[i][1]; Y2 = P[i+1][1]
                X1 = P[i][0]; X2 = P[i+1][0]
                dX = X2-X1  ; dY=Y2-Y1
                l = DL - (CUL - L[i])
                if dX==0 and dY==0:
                    Pt.X = X1 
                    Pt.Y = Y1 
                if dX==0 and dY>0:
                    Pt.X = X1 
                    Pt.Y = Y1 + l
                if dX==0 and dY<0:
                    Pt.X = X1 
                    Pt.Y = Y1 - l
                if dX>0 and dY>=0:
                    th = math.atan(dY/dX)
                    Pt.X = X1 + l*math.cos(th)
                    Pt.Y = Y1 + l*math.sin(th)
                if dX>0 and dY<0:
                    th = math.atan(-dY/dX)
                    Pt.X = X1 + l*math.cos(th)
                    Pt.Y = Y1 - l*math.sin(th)
                if dX<0 and dY>=0:
                    th = math.atan(-dY/dX)
                    Pt.X = X1 - l*math.cos(th)
                    Pt.Y = Y1 + l*math.sin(th)
                if dX<0 and dY<0:
                    th = math.atan(dY/dX)
                    Pt.X = X1 - l*math.cos(th)
                    Pt.Y = Y1 - l*math.sin(th)
                break
        if Pt.X == -1:arcpy.AddMessage([BM,EM,CM,P])
        return Pt
def CheckDirection(Road):
        P = []
        Br = MilepostBreaks(Road)
        for br in Br:
            if br[1] > br[0]+1:
                for i in range(br[0],br[1]):
                    if i == br[0]:
                        if ComparePoints(Road['Path'][i][0],Road['Path'][i+1][0]) or ComparePoints(Road['Path'][i][0],Road['Path'][i+1][-1]):
                            P.append(ChangeDirection(Road['Path'][i]))
                        elif ComparePoints(Road['Path'][i][-1],Road['Path'][i+1][0]) or ComparePoints(Road['Path'][i][0],Road['Path'][i+1][-1]):
                            P.append(Road['Path'][i])
                        else:
                            arcpy.AddMessage( "    Polylines are not continuous")
                    elif i==br[1]-1:
                        if ComparePoints(Road['Path'][i][-1],Road['Path'][i-1][0]) or ComparePoints(Road['Path'][i][-1],Road['Path'][i-1][-1]):
                            P.append(ChangeDirection(Road['Path'][i]))
                        elif ComparePoints(Road['Path'][i][0],Road['Path'][i-1][0]) or ComparePoints(Road['Path'][i][0],Road['Path'][i-1][-1]):
                            P.append(Road['Path'][i])
                        else:
                            arcpy.AddMessage( "    Polylines are not continuous")
                    else:
                        if (ComparePoints(Road['Path'][i][0],Road['Path'][i+1][0]) or ComparePoints(Road['Path'][i][0],Road['Path'][i+1][-1])) and (ComparePoints(Road['Path'][i][-1],Road['Path'][i-1][0]) or ComparePoints(Road['Path'][i][-1],Road['Path'][i-1][-1])):
                            P.append(ChangeDirection(Road['Path'][i]))
                        elif (ComparePoints(Road['Path'][i][0],Road['Path'][i-1][0]) or ComparePoints(Road['Path'][i][0],Road['Path'][i-1][-1])) and (ComparePoints(Road['Path'][i][-1],Road['Path'][i+1][0]) or ComparePoints(Road['Path'][i][-1],Road['Path'][i+1][-1])):
                            P.append(Road['Path'][i])
                        else:
                            arcpy.AddMessage( "    Polylines are not continuous")

            else:
                P.append(Road['Path'][br[0]])
        return P
def ComparePoints(P1,P2):
        import math
        d = math.sqrt((P1[0]-P2[0])**2+(P1[1]-P2[1])**2)
        if d<.01: 
            return True
        else:
            return False
def ChangeDirection(P):
        n = len(P)
        OP = []
        for i in range(0,n):
            OP.append(P[n-i-1])
        return OP
def Field2Dic(Field):
        Dic = {}
        Dic.update({'name':Field.name})
        Dic.update({'type':Field.type})
        Dic.update({'precision':Field.precision})
        Dic.update({'scale':Field.scale})
        Dic.update({'length':Field.length})
        Dic.update({'alias':Field.aliasName})
        Dic.update({'nullable':Field.isNullable})
        Dic.update({'required':Field.required})
        return Dic
def Resegment(Att,Road):
    OutField = []
    OutPath = []
    MRoad = MergeSegments(Road)
    MMP = MergeMileposts(Att['MP'],Road['MP'])
    NullField = []
    #arcpy.AddMessage(str([MMP,Att['MP']]))
    for mp in MMP:
        Flag = False
        for amp in Att['MP']:
            if mp[0]>=float(amp[0]) and mp[1]<= float(amp[1]):
                i = Att['MP'].index(amp)
                OutField.append(Att['Fields'][i])
                #arcpy.AddMessage(str(Att['Fields'][i]))
                Flag = True
                break
        if not Flag: OutField.append(NullField)
        for rmp in Road['MP']:
            if rmp[0]<=mp[0] and rmp[1]>=mp[1]:
                i = Road['MP'].index(rmp)
                OutPath.append(DivideSegment(rmp,Road['Path'][i],mp))
                break
    return {'MP':MMP,'Fields':OutField,'Path':OutPath}
def DivideSegment(RoadMP,RoadPath,DesiredMP):
    import math
    P = []
    n = len(RoadPath)
    L = []
    for i in range(0,n-1):
        L.append(math.sqrt((RoadPath[i+1][1]-RoadPath[i][1])**2+(RoadPath[i+1][0]-RoadPath[i][0])**2))
    TotL = sum(L)
    DL0 = (DesiredMP[0]-RoadMP[0])/(RoadMP[1]-RoadMP[0])*TotL
    DL1 = (DesiredMP[1]-RoadMP[0])/(RoadMP[1]-RoadMP[0])*TotL

    P0 = ExtractXY(RoadMP[0],RoadMP[1],DesiredMP[0],RoadPath)
    P1 = ExtractXY(RoadMP[0],RoadMP[1],DesiredMP[1],RoadPath)

    CUL = 0
    P.append([P0.X,P0.Y])
    for i in range(0,len(L)):
        CUL += L[i]
        if CUL > DL0 and CUL < DL1:
            P.append(RoadPath[i+1])
    P.append([P1.X,P1.Y])
    return P
def RemoveDuplicate(ListIn):
    ListOut = []
    i = 0
    for l in ListIn:
        i += 1
        if not(l in ListOut) and not(l[0] in [k[0] for k in ListOut]) and not(l[1] in [k[1] for k in ListOut]):
            ListOut.append(l)
    return(ListOut)
def MergeMileposts(MPAttIn,MPRoad):
    MPAtt = RemoveDuplicate(MPAttIn)
    #MPRoad = RemoveDuplicate(MPRoadIn)
    OutMP = []
    Br = MilepostBreaks({'MP':MPRoad})
    for br in Br:
        i = 0
        MPR = []
        for j in range(br[0],br[1]):
            MPR.append(MPRoad[j])
        SMP = MPR[i][0]
        EMP = SMP
        for mp in MPAtt:
            if float(mp[1])>SMP and float(mp[0])<MPR[i][1]:
                EMP = min(mp[1],MPR[i][1])
                OutMP.append([SMP,EMP])
                i += (EMP>=MPR[i][1])*(i<len(MPR)-1)
                SMP = EMP
                while mp[1]>EMP and i<(len(MPR)-1):
                    EMP = min(mp[1],MPR[i][1])
                    OutMP.append([SMP,EMP])
                    i += (EMP>=MPR[i][1])
                    SMP = EMP
                if i>(len(MPR)-1): i = len(MPR)-1
        if EMP<MPR[i][1]:
            for j in range(i,len(MPR)):
                EMP = MPR[j][1]
                OutMP.append([SMP,EMP])
                SMP = EMP
    Flag = False
    for mp in OutMP:
        if mp[0]==mp[1]:Flag =True
    if Flag:arcpy.AddMessage([MPAtt,MPRoad,OutMP])
    return OutMP
def MilepostBreaks(Road):
    n = len(Road['MP'])
    Br = []
    Old = 0
    for i in range(1,len(Road['MP'])):
        if Road['MP'][i][0] <> Road['MP'][i-1][1]:
            Br.append([Old,i])
            Old = i
    Br.append([Old,len(Road['MP'])])
    return(Br)
def MergeSegments(Road):
    OutP = []
    OutM = []
    RoadP = CheckDirection(Road)
    Br = MilepostBreaks(Road)
    for br in Br:
        P = []
        P.extend(RoadP[br[0]])
        for i in range(br[0]+1,br[1]):
            P.extend(RoadP[i][1:])
        OutP.append(P)
        OutM.append([Road['MP'][br[0]][0],Road['MP'][br[1]-1][1]])
    return {'MP':OutM,'Path':OutP}
#Tool Scripts
def NCCrashGeoCode(CrashInput,CIDField,CRtField,CCnField,CMpField,RoadInput,RRtField,RCnField,RBMpField,REMpField,Output):
    import json
    arcpy.AddMessage(" ")
    arcpy.AddMessage("  GeoCode Crashes")

    OutDic = OutputParser(Output, 'shp')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("    Count: Crash Layer")
    CrashLayer = CrashInput
    TotalCrashes = arcpy.GetCount_management(CrashLayer)
    arcpy.AddMessage("     - Total Number of Crashes Found: " + str(TotalCrashes))

    arcpy.AddMessage("    Count: Road Layer")
    RoadLayer  = RoadInput
    TotalRoads = arcpy.GetCount_management(RoadLayer)
    arcpy.AddMessage("     - Total number of Road Segments Found: " + str(TotalRoads))

    #arcpy.AddMessage("    Sort: Crash Layer")
    #SortString = CRtField + " ASCENDING;" + CCnField + " ASCENDING;" + CMpField + " ASCENDING;"
    #CrashSorted = Sort(CrashLayer,'GCCrashS',SortString)

    #arcpy.AddMessage("    Sort: Roads Layer")
    #SortString = RRtField + " ASCENDING;" + RCnField + " ASCENDING;" + RBMpField + " ASCENDING;"
    #RoadSorted = Sort(RoadLayer,'GCRoadS',SortString)

    arcpy.AddMessage("    Reading Crash Info")
    CrashDic = {SRow.getValue(CIDField):{} for SRow in arcpy.SearchCursor(CrashLayer)}
    arcpy.AddMessage("     - Crash ID Field Completed")
    for SRow in arcpy.SearchCursor(CrashLayer):
        OID = SRow.getValue(CIDField)
        CrashDic[OID].update({'Rt':SRow.getValue(CRtField)})
        CrashDic[OID].update({'Cn':SRow.getValue(CCnField)})
        CrashDic[OID].update({'Mp':SRow.getValue(CMpField)})
    arcpy.AddMessage("     - Route Number & County & Milepost Completed")

    arcpy.AddMessage("    Reading Roads Info")
    RoadDic = {int(SRow.getValue(RRtField)):{} for SRow in arcpy.SearchCursor(RoadLayer)}
    arcpy.AddMessage("     - Route Number Completed")
    for SRow in arcpy.SearchCursor(RoadLayer):
        Rt = int(SRow.getValue(RRtField))
        RoadDic[Rt].update({int(SRow.getValue(RCnField)):{'MP':[],'Path':[]}})
    arcpy.AddMessage("     - County Completed")
    for SRow in arcpy.SearchCursor(RoadLayer):
        Rt = int(SRow.getValue(RRtField))
        Cn = int(SRow.getValue(RCnField))
        RoadDic[Rt][Cn]['MP'  ].append([SRow.getValue(RBMpField),SRow.getValue(REMpField)])
        RoadDic[Rt][Cn]['Path'].append(json.loads(SRow.getValue('shape').JSON)['paths'][0])
    arcpy.AddMessage("     - Milepost & Path Completed")

    arcpy.AddMessage("   Creating Geocoded Crash Layer")
    GCrashLayer = CreateFeatureclass('CGGCrash',{'geometry_type':"POINT",'has_m':'ENABLED','has_z':'ENABLED'})

    arcpy.AddMessage("    - Adding Fields")
    FieldDic = [F_X, F_Y,F_CT_ANO,F_County,F_RouteNBR,F_Milepost]
    for rec in FieldDic:
        AddField(GCrashLayer,rec)

    arcpy.AddMessage("    - Defining Projection")
    arcpy.DefineProjection_management(GCrashLayer,CoordSystemNC)


    arcpy.AddMessage("    - Insert Cursor")
    IC = arcpy.InsertCursor(GCrashLayer) 
    Total = 0
    for CID in CrashDic.keys():
        CRt = int(CrashDic[CID]['Rt'])
        CCn = int(CrashDic[CID]['Cn'])
        CMp = CrashDic[CID]['Mp']
        Pt = arcpy.Point()
        Flag = False
        Pt.X = 0
        Pt.Y = 0
        if CRt in RoadDic.keys():
            if CCn in RoadDic[CRt].keys():
                P = CheckDirection(RoadDic[CRt][CCn])
                Flag = True
                for MPL in RoadDic[CRt][CCn]['MP']:
                    if CMp >= MPL[0] and CMp <= MPL[1]:
                        i = RoadDic[CRt][CCn]['MP'].index(MPL)
                        Pt = ExtractXY(MPL[0],MPL[1],CMp,P[i])
                        Total += 1
                        break
                    if Pt.X == 0 and CMp > MPL[1] and CMp - MPL[1] < 0.1:
                        i = RoadDic[CRt][CCn]['MP'].index(MPL)
                        Pt = ExtractXY(MPL[0],MPL[1],MPL[1],P[i])
                if Pt.X == 0 or Pt.X == -1:
                    arcpy.AddMessage("      Milepost Not Found: RTN = " + str(CRt) + ", Cnty = " + str(CCn) + ",Crash Mp = "+ str(CMp) + ', Max Road Mp = ' + str(MPL[1]))
        if not Flag:
            arcpy.AddMessage("      Route Not Found: RTN = " + str(CRt) + ", Cnty = " + str(CCn) + ", Crash Mp = " + str(CMp))
        else:
            IRow = IC.newRow()
            IRow.setValue(F_CT_ANO['name'],CID)
            IRow.setValue(F_County['name'],CCn)
            IRow.setValue(F_RouteNBR['name'],CRt)
            IRow.setValue(F_Milepost['name'],CMp)
            IRow.setValue(F_X['name'],Pt.X)
            IRow.setValue(F_Y['name'],Pt.Y)
            IRow.shape = Pt
            IC.insertRow(IRow)             
    TotalCrashes = int(str(TotalCrashes))
    arcpy.AddMessage("    Total " + str(TotalCrashes-Total) + " of " + str(TotalCrashes) + " crashes were not geocoded (" + str(round(float(TotalCrashes-Total)/TotalCrashes*10000)/100) + "%).")
    Output = arcpy.CopyFeatures_management(GCrashLayer,Output)

    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")
def Resegmenting_Old(RoadInput,RRtField,RCnField,RBMpField,REMpField,AttributeInput,ACRNField,ABMpField,AEMpField,ImportList,Output):
    import json
    arcpy.AddMessage(" ")
    arcpy.AddMessage("  Import and Resegment Roads Layer")

    OutDic = OutputParser(Output, 'shp')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("    Count: Roads Layer")
    RoadLayer  = RoadInput
    TotalRoads = int(str(arcpy.GetCount_management(RoadLayer)))
    arcpy.AddMessage("     - Total number of Road Segments Found: " + str(TotalRoads))

    arcpy.AddMessage("    Count: Attribute Table")
    AttributeLayer  = AttributeInput
    TotalAttributes = int(str(arcpy.GetCount_management(AttributeLayer)))
    arcpy.AddMessage("     - Total number of Table Rows Found: " + str(TotalAttributes))

    arcpy.AddMessage("    Reading Roads Info")
    RoadDic = {int(SRow.getValue(RRtField)):{} for SRow in arcpy.SearchCursor(RoadLayer)}
    arcpy.AddMessage("     - Route Number Completed")
    for SRow in arcpy.SearchCursor(RoadLayer):
        Rt = int(SRow.getValue(RRtField))
        RoadDic[Rt].update({int(SRow.getValue(RCnField)):{'MP':[],'Path':[]}})
    arcpy.AddMessage("     - County Completed")
    for SRow in arcpy.SearchCursor(RoadLayer):
        Rt = int(SRow.getValue(RRtField))
        Cn = int(SRow.getValue(RCnField))
        RoadDic[Rt][Cn]['MP'  ].append([SRow.getValue(RBMpField),SRow.getValue(REMpField)])
        RoadDic[Rt][Cn]['Path'].append(json.loads(SRow.getValue('shape').JSON)['paths'][0])
    arcpy.AddMessage("     - Milepost & Path Completed")

    arcpy.AddMessage("    Reading Attributes Info")
    AttDic = {}
    for SRow in arcpy.SearchCursor(AttributeLayer):
        CRt = str(SRow.getValue(ACRNField))
        Rt = int(CRt[2:])
        AttDic.update({Rt:{}})
    arcpy.AddMessage("     - Route Number Completed")
    for SRow in arcpy.SearchCursor(AttributeLayer):
        CRt = str(SRow.getValue(ACRNField))
        Rt = int(CRt[2:])
        Cn = int(CRt[0:2])
        AttDic[Rt].update({Cn:{'MP':[],'Fields':[]}})
    arcpy.AddMessage("     - County Completed")
    AllFieldList = arcpy.ListFields(AttributeLayer)
    ImportFieldList = []
    for Field in AllFieldList:
        if Field.name in ImportList:
            ImportFieldList.append(Field)
    for SRow in arcpy.SearchCursor(AttributeLayer):
        CRt = str(SRow.getValue(ACRNField))
        Rt = int(CRt[2:])
        Cn = int(CRt[0:2])
        AttDic[Rt][Cn]['MP'].append([SRow.getValue(ABMpField),SRow.getValue(AEMpField)])
        FL = []
        for Field in ImportFieldList:
            FL.append(SRow.getValue(Field.name))
        AttDic[Rt][Cn]['Fields'].append(FL)
    arcpy.AddMessage("     - Milepost & Import Fields Completed")

    arcpy.AddMessage("   Creating Resegmented Road Layer")
    RSRoadLayer = CreateFeatureclass('RSRoad',{'geometry_type':"POLYLINE"})

    arcpy.AddMessage("    - Adding Fields")
    FieldDic = [F_County,F_RouteNBR,F_BegMp,F_EndMp]
    for rec in FieldDic:
        AddField(RSRoadLayer,rec)
    for rec in ImportFieldList:
        AddField(RSRoadLayer,Field2Dic(rec))

    arcpy.AddMessage("    - Defining Projection")
    arcpy.DefineProjection_management(RSRoadLayer,CoordSystemNC)

    arcpy.AddMessage("    - Insert Cursor")
    IC = arcpy.InsertCursor(RSRoadLayer) 
    Total = 0
    for Rt in RoadDic.keys():
        for Cn in RoadDic[Rt].keys():
            Flag = False
            if Rt in AttDic.keys():
                if Cn in AttDic[Rt].keys():
                    Flag = True
                    Res = Resegment(AttDic[Rt][Cn],RoadDic[Rt][Cn])
            if not Flag:
                Res = MergeSegments(RoadDic[Rt][Cn])
                for mp in Res['MP']:
                    j = Res['MP'].index(mp)
                    IRow = IC.newRow()
                    IRow.setValue(F_County['name'],Cn)
                    IRow.setValue(F_RouteNBR['name'],Rt)
                    IRow.setValue(F_BegMp['name'],mp[0])
                    IRow.setValue(F_EndMp['name'],mp[1])
                    #if mp[0]==mp[1]:arcpy.AddMessage(RoadDic[Rt][Cn])
                    IRow.shape = arcpy.Polyline(arcpy.Array([arcpy.Point(p[0],p[1]) for p in Res['Path'][j]]))
                    IC.insertRow(IRow)             
            else:
                for mp in Res['MP']:
                    j = Res['MP'].index(mp)
                    IRow = IC.newRow()
                    IRow.setValue(F_County['name'],Cn)
                    IRow.setValue(F_RouteNBR['name'],Rt)
                    IRow.setValue(F_BegMp['name'],mp[0])
                    IRow.setValue(F_EndMp['name'],mp[1])
                    IRow.shape = arcpy.Polyline(arcpy.Array([arcpy.Point(p[0],p[1]) for p in Res['Path'][j]]))
                    if len(Res['Fields'][j])>0:
                        for rec in ImportFieldList:
                            i = ImportFieldList.index(rec)
                            IRow.setValue(rec.name,Res['Fields'][j][i])
                    IC.insertRow(IRow)             
    #TotalAttributes = int(str(TotalAttributes))
    #arcpy.AddMessage("    Total " + str(TotalAttributes-Total) + " of " + str(TotalAttributes) + " attributes were not geocoded (" + str(round(float(TotalAttributes-Total)/TotalAttributes*10000)/100) + "%).")

    arcpy.AddMessage("    - Sort")
    RSSortRoad = Sort(RSRoadLayer, 'RSSortRoad', "RouteNBR ASCENDING;County ASCENDING;BegMp ASCENDING")
    Output = arcpy.CopyFeatures_management(RSSortRoad,Output)

    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")
def Resegmenting(RoadInput,RRtField,RCnField,RBMpField,REMpField,AttributeInput,ACRNField,ABMpField,AEMpField,ImportList,Output):
    import json
    import math 
    arcpy.AddMessage(" ")
    arcpy.AddMessage("  Import and Resegment Roads Layer")

    OutDic = OutputParser(Output, 'shp')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("    Count: Roads Layer")
    RoadLayer  = RoadInput
    TotalRoads = int(str(arcpy.GetCount_management(RoadLayer)))
    arcpy.AddMessage("     - Total number of Road Segments Found: " + str(TotalRoads))

    arcpy.AddMessage("    Count: Attribute Table")
    AttributeLayer  = AttributeInput
    TotalAttributes = int(str(arcpy.GetCount_management(AttributeLayer)))
    arcpy.AddMessage("     - Total number of Table Rows Found: " + str(TotalAttributes))

    arcpy.AddMessage("    Reading Roads Info")
    RoadDic = {int(SRow.getValue(RRtField)):{} for SRow in arcpy.SearchCursor(RoadLayer)}
    arcpy.AddMessage("     - Route Number Completed")
    for SRow in arcpy.SearchCursor(RoadLayer):
        Rt = int(SRow.getValue(RRtField))
        RoadDic[Rt].update({int(SRow.getValue(RCnField)):{'MP':[],'Path':[]}})
    arcpy.AddMessage("     - County Completed")
    for SRow in arcpy.SearchCursor(RoadLayer):
        Rt = int(SRow.getValue(RRtField))
        Cn = int(SRow.getValue(RCnField))
        RoadDic[Rt][Cn]['MP'  ].append([SRow.getValue(RBMpField),SRow.getValue(REMpField)])
        RoadDic[Rt][Cn]['Path'].append(json.loads(SRow.getValue('shape').JSON)['paths'][0])
    arcpy.AddMessage("     - Milepost & Path Completed")

    arcpy.AddMessage("    Reading Attributes Info")
    AttDic = {}
    for SRow in arcpy.SearchCursor(AttributeLayer):
        CRt = str(SRow.getValue(ACRNField))
        Rt = int(float(CRt[2:]))
        AttDic.update({Rt:{}})
    arcpy.AddMessage("     - Route Number Completed")
    for SRow in arcpy.SearchCursor(AttributeLayer):
        CRt = str(SRow.getValue(ACRNField))
        Rt = int(float(CRt[2:]))
        Cn = int(float(CRt[0:2]))
        AttDic[Rt].update({Cn:{'MP':[],'Fields':[]}})
    arcpy.AddMessage("     - County Completed")
    AllFieldList = arcpy.ListFields(AttributeLayer)
    ImportFieldList = []
    for Field in AllFieldList:
        if Field.name in ImportList:
            ImportFieldList.append(Field)
    for SRow in arcpy.SearchCursor(AttributeLayer):
        CRt = str(SRow.getValue(ACRNField))
        Rt = int(float(CRt[2:]))
        Cn = int(float(CRt[0:2]))
        #arcpy.AddMessage([Rt,Cn,SRow.getValue(ABMpField),SRow.getValue(AEMpField)])
        AttDic[Rt][Cn]['MP'].append([SRow.getValue(ABMpField),SRow.getValue(AEMpField)])
        FL = []
        for Field in ImportFieldList:
            FL.append(SRow.getValue(Field.name))
        AttDic[Rt][Cn]['Fields'].append(FL)
    arcpy.AddMessage("     - Milepost & Import Fields Completed")

    arcpy.AddMessage("   Creating Resegmented Road Layer")
    RSRoadLayer = CreateFeatureclass('RSRoad',{'geometry_type':"POLYLINE",'has_m':'ENABLED','has_z':'ENABLED'})

    arcpy.AddMessage("    - Adding Fields")
    FieldDic = [F_County,F_RouteNBR,F_BegMp,F_EndMp]
    for rec in FieldDic:
        AddField(RSRoadLayer,rec)
    for rec in ImportFieldList:
        AddField(RSRoadLayer,Field2Dic(rec))

    arcpy.AddMessage("    - Defining Projection")
    arcpy.DefineProjection_management(RSRoadLayer,CoordSystemNC)

    arcpy.AddMessage("    - Insert Cursor")
    IC = arcpy.InsertCursor(RSRoadLayer) 
    Total = 0
    for Rt in RoadDic.keys():
        for Cn in RoadDic[Rt].keys():
            Flag = False
            if Rt in AttDic.keys():
                if Cn in AttDic[Rt].keys():
                    Flag = True
                    Res = Resegment(AttDic[Rt][Cn],RoadDic[Rt][Cn])
            if not Flag:
                #Res = MergeSegments(RoadDic[Rt][Cn])
                for mp in RoadDic[Rt][Cn]['MP']:
                    j = RoadDic[Rt][Cn]['MP'].index(mp)
                    IRow = IC.newRow()
                    IRow.setValue(F_County['name'],Cn)
                    IRow.setValue(F_RouteNBR['name'],Rt)
                    IRow.setValue(F_BegMp['name'],mp[0])
                    IRow.setValue(F_EndMp['name'],mp[1])
                    #if mp[0]==mp[1]:arcpy.AddMessage(RoadDic[Rt][Cn])
                    for rec in ImportFieldList:
                        i = ImportFieldList.index(rec)
                        try:
                            IRow.setValue(rec.name,-1)
                        except:
                            DoNothing = True
                    IRow.shape = arcpy.Polyline(arcpy.Array([arcpy.Point(p[0],p[1]) for p in RoadDic[Rt][Cn]['Path'][j]]))
                    IC.insertRow(IRow)             
            else:
                for mp in Res['MP']:
                    j = Res['MP'].index(mp)
                    #arcpy.AddMessage([Cn,Rt,mp[0],mp[1]])
                    IRow = IC.newRow()
                    IRow.setValue(F_County['name'],Cn)
                    IRow.setValue(F_RouteNBR['name'],Rt)
                    IRow.setValue(F_BegMp['name'],mp[0])
                    IRow.setValue(F_EndMp['name'],mp[1])
                    IRow.shape = arcpy.Polyline(arcpy.Array([arcpy.Point(p[0],p[1]) for p in Res['Path'][j]]))
                    for rec in ImportFieldList:
                        i = ImportFieldList.index(rec)
                        try:
                            IRow.setValue(rec.name,Res['Fields'][j][i])
                        except:
                            IRow.setValue(rec.name,-1)

                    IC.insertRow(IRow)             
    #TotalAttributes = int(str(TotalAttributes))
    #arcpy.AddMessage("    Total " + str(TotalAttributes-Total) + " of " + str(TotalAttributes) + " attributes were not geocoded (" + str(round(float(TotalAttributes-Total)/TotalAttributes*10000)/100) + "%).")

    arcpy.AddMessage("    - Sort")
    RSSortRoad = Sort(RSRoadLayer, 'RSSortRoad', "RouteNBR ASCENDING;County ASCENDING;BegMp ASCENDING")
    Output = arcpy.CopyFeatures_management(RSSortRoad,Output)

    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")
def NCRoadwayTypeBuffer(RoadsLayer,FMedianType,FTotalLanes,FSurfaceWidth,FMedianWidth,Output):
    arcpy.AddMessage(" ")
    arcpy.AddMessage("   Add Roadway Type & Buffer")

    OutDic = OutputParser(Output, 'shp')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("   Copy Features: Roads Layer")
    temp = CopyFeatures(RoadsLayer,'Temp_RoadsType')


    arcpy.AddMessage("   Add Fields: Roads Layer")
    CrashTypeDic = [F_RBuffer, F_FType]
    for Field in CrashTypeDic:
        AddField(temp,Field)


    arcpy.AddMessage("   Calculate Fields: Roads Layer")
    #CodeBlock = """def fval(c):
    #    if ((c>=1 and c<=5) or c==9):
    #       return 1
    #    else:
    #       return 0"""
    #CalField(temp,F_RURAL,"fval(!" + FR_Func_Class + "!)",CodeBlock)

    #CodeBlock = """def fval(c):
    #    if ((c>=11 and c<=15) or c==18):
    #       return 1
    #    else:
    #       return 0"""
    #CalField(temp,F_URBAN,"fval(!" + FR_Func_Class + "!)",CodeBlock)
    CodeBlock = """def fval(Rural, Urban, TotLanes, MedianType):
        if   Rural == 1 and TotLanes == 2 and MedianType in [0, 3]:
           return "R2U"
        elif Rural == 1 and TotLanes == 4 and MedianType == 0:
           return "R4U"
        elif Rural == 1 and TotLanes == 4 and MedianType in [1, 2, 4, 5, 6, 9, 10, 11]:
           return "R4D"

        elif Urban == 1 and TotLanes == 2 and MedianType == 0:
           return "U2U"
        elif Urban == 1 and TotLanes == 2 and MedianType == 3:
           return "U3T"
        elif Urban == 1 and TotLanes == 4 and MedianType == 0:
           return "U4U"
        elif Urban == 1 and TotLanes == 4 and MedianType in [1, 2, 4, 5, 6, 9, 10, 11]:
           return "U4D"
        elif Urban == 1 and TotLanes == 4 and MedianType == 3:
           return "U5T"   """
    CalField(temp,F_FType,"fval(!" + F_RURAL['name'] + "!, !" + F_URBAN['name'] + "!, !" + FTotalLanes + "!, !" + FMedianType + "!)",CodeBlock)

    CodeBlock = """def fval(Type, Median, Surf):
        if Type in ['R2U','U2U']:   # Polyline in the center of the Road
            return 0.5 * (Surf + Median) + 30
        else:                       # Polyline in the center of one direction
            return 0.75 * Surf + Median + 30"""
    CalField(temp,F_RBuffer,"fval(!" + F_FType['name'] + "!, !" + FMedianWidth + "!, !" + FSurfaceWidth + "!)",CodeBlock)

    Output = arcpy.CopyFeatures_management(temp, Output)

    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")
def ImpotCrashAttributesNC(CrashInput,LocInput,Output):
    arcpy.AddMessage("    ")
    arcpy.AddMessage("    Import Crash Attributes NC")

    OutDic = OutputParser(Output, 'shp')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("    Sort: Crash Layer")
    CrashLayer = Sort(CrashInput,'CAtt_Sort_Crash','ANO')
    C = arcpy.GetCount_management(CrashLayer)
    arcpy.AddMessage("     - Total Items Found: " + str(C))

    arcpy.AddMessage("    Assuming Location File is Sorted, Counting")
    LocFile = LocInput
    U = arcpy.GetCount_management(LocFile)
    arcpy.AddMessage("     - Total Items Found: " + str(U))

    arcpy.AddMessage("    Add Field: Crash Layer")
    CrashTypeDicR = ['numvehs', 'loc_type', 'rodwycls', 'severity', 'acctype', 'acc_date']
    CrashTypeDicW = [F_CT_UNT , F_CT_JCT  , F_CT_RCT  , F_CT_INJ  , F_CT_PRC , F_CT_DAT  ]
    for Field in CrashTypeDicW:
        arcpy.DeleteField_management(CrashLayer,Field['name'])
    for Field in CrashTypeDicW:
        AddField(CrashLayer,Field)

    arcpy.AddMessage("    Update Cursor: Crash Layer")
    UC = arcpy.UpdateCursor(CrashLayer)
    SC = arcpy.SearchCursor(LocFile)

    arcpy.SetProgressor("step","Import Crash Attributes - Location File",0,100,1)
    arcpy.SetProgressorLabel("Update Crash Layer:")
    arcpy.SetProgressorPosition(0)
    PP = 0
    def GetANO(Row, IntErr=-1, RowErr=99999999):
        if Row:
            try:
                ANO = Row.getValue('caseno')
            except:
                ANO = Row.getValue('ANO')

            try:
                ANO = int(ANO)
            except:
                ANO = IntErr
        else:
            ANO = RowErr
        return ANO
    def ConvertType(Value, Type):
        if   Type in ['TEXT']:
            try:
                fval = str(Value)
            except:
                fval = 'NotConv'
        elif Type in ['SHORT', 'LONG']:
            try:
                fval = int(Value)
            except:
                fval = -1
        elif Type in ['DOUBLE']:
            try:
                fval = float(Value)
            except:
                fval = -1.0
        return fval
    SRow = SC.next()
    ANOU = GetANO(SRow)
    for URow in UC:
        FID = GetFID(URow)
        ANOC = GetANO(URow)
        while ANOU < ANOC:
            SRow = SC.next()
            ANOU = GetANO(SRow,-2)
        if ANOC == ANOU:
            VList = []
            for Field in CrashTypeDicR:
                VList.append(SRow.getValue(Field))
        
            i = 0
            for Field in CrashTypeDicW:
                URow.setValue(Field['name'],ConvertType(VList[i],Field['type']))
                i += 1

            k = -1
            while ANOC == ANOU:
                SRow = SC.next()
                ANOU = GetANO(SRow,-2)
                k += 1

            UC.updateRow(URow)
            if k > 1:
               arcpy.AddWarning('     - ANO = ' + str(ANOC) + ', ' + str(k) + 'Records found in Location File')
        elif ANOU > ANOC:
            arcpy.AddWarning("     - ANO: " + str(ANOC) + " Not Found in Location File")
        NewPP = (100 * FID) / int(str(C))
        if NewPP > PP:
            arcpy.SetProgressorPosition(NewPP)
            PP = NewPP

    Output = arcpy.CopyFeatures_management(CrashLayer,Output)
    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")
def CrashSplitterNC(CrashInput,IntersectionsLayer,RoadsLayer,Output):
    arcpy.AddMessage("   ")
    arcpy.AddMessage("   Crash Split")

    OutDic = OutputParser(Output, 'shp')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("   Copy: Crash Layer")
    CrashLayer = CopyFeatures(CrashInput,'CSplit_Temp')

    arcpy.AddMessage("   Get Count: Crash Layer")
    TotalCrashes = int(str(arcpy.GetCount_management(CrashLayer)))
    arcpy.AddMessage("    - " + str(TotalCrashes))

    arcpy.AddMessage("   Projec: Crash Layer")
    CrashLayer = Project(CrashLayer,CoordSystemNC)

    arcpy.AddMessage("   Adding XY: Crash Layer")
    arcpy.DeleteField_management(CrashLayer,'POINT_X')
    arcpy.DeleteField_management(CrashLayer,'POINT_Y')
    arcpy.AddXY_management(CrashLayer)

    arcpy.AddMessage("   Add Field: Crash Layer")
    CrashFieldDic = [F_TargetFID, F_RCrash, F_ICrash, F_RFType, F_RFID, F_CI_X, F_CI_Y, F_Dist2CF]
    for Field in CrashFieldDic:
        AddField(CrashLayer,Field)

    def ReadCrash(Row,Field,Default=-1):
        try:
            return int(Row.getValue(Field))
        except:
            return Default
    def CalRatio(Dist,ABuffer,BBuffer,AADTMajor,AADTMinor,JCT):
            Ratio = 0
            if Dist <= ABuffer:
                Ratio = 500000 + AADTMajor + AADTMinor
            elif Dist > ABuffer and Dist <= BBuffer:
                if (JCT in [7,8,9,11]):
                    Ratio = AADTMajor + AADTMinor
            return Ratio

    UC = arcpy.UpdateCursor(CrashLayer)
    FID = 0
    for URow in UC:
        URow.setValue(F_TargetFID['name'],FID)
        FID += 1
        UC.updateRow(URow)

    arcpy.AddMessage("   Read Crash Data")
    CrashDic = {SRow.getValue(F_TargetFID['name']):{'JCT':ReadCrash(SRow,F_CT_JCT['name']),'C_X': SRow.getValue("POINT_X"),'C_Y': SRow.getValue("POINT_Y"),'IList':[],'RList':[]} for SRow in arcpy.SearchCursor(CrashLayer)}

    arcpy.AddMessage("   Spatial Join: Crash Layer + Intersections Layer")
    IMaxBuffer = MaximumValue(IntersectionsLayer,F_BBuffer['name'])
    SPJI = SpatialJoin(CrashLayer, IntersectionsLayer,"SPJI" , {'join_operation': "JOIN_ONE_TO_MANY", 'join_type': "KEEP_COMMON",'field_mapping': "",'match_option': "WITHIN_A_DISTANCE",'search_radius': str(IMaxBuffer) + " Feet",'distance_field_name': ""})

    arcpy.AddMessage("   Append Intersection Data")
    for SRow in arcpy.SearchCursor(SPJI):
        X = SRow.getValue(F_X['name'])
        Y = SRow.getValue(F_Y['name'])
        FID   = SRow.getValue(F_TargetFID['name'])
        Dist  = ((CrashDic[FID]['C_X'] - X) ** 2 + (CrashDic[FID]['C_Y'] - Y) ** 2) ** 0.5
        Ratio = CalRatio(Dist,SRow.getValue(F_ABuffer['name']),SRow.getValue(F_BBuffer['name']),SRow.getValue(F_AADT_Major['name']),SRow.getValue(F_AADT_Minor['name']),CrashDic[FID]['JCT'])
        if Ratio > 0:
            CrashDic[FID]['IList'].append({'Dist': Dist, 'Type': SRow.getValue(F_FType['name']),'X':X,'Y':Y,'Ratio': Ratio})

    arcpy.AddMessage("   Spatial Join: Crash Layer + Roads Layer")
    RMaxBuffer = MaximumValue(RoadsLayer ,F_RBuffer['name'])
    SPJR = SpatialJoin(CrashLayer, RoadsLayer,"SPJR" , {'join_operation': "JOIN_ONE_TO_ONE" , 'join_type': "KEEP_COMMON",'field_mapping': "",'match_option': "CLOSEST"          ,'search_radius': str(RMaxBuffer) + " Feet" ,'distance_field_name': "distance"})

    arcpy.AddMessage("   Append Roadway Data")
    for SRow in arcpy.SearchCursor(SPJR):
        Dist = SRow.getValue("distance")
        FID  = SRow.getValue(F_TargetFID['name'])
        if Dist <= SRow.getValue(F_RBuffer['name']):
            #arcpy.AddMessage([SRow.getValue(F_FType['name']),SRow.getValue(F_RouteFID['name']),Dist])
            CrashDic[FID]['RList'].append({'Dist': Dist, 'Type': SRow.getValue(F_FType['name']),'RFID':SRow.getValue(F_RouteFID['name'])})

    arcpy.AddMessage("   Update Cursor: Crash Layer")
    
    UC = arcpy.UpdateCursor(CrashLayer)
    arcpy.SetProgressor("step"," ",0,TotalCrashes,1)
    arcpy.SetProgressorLabel("Update Crash Layer:")
    arcpy.SetProgressorPosition(0)
    for URow in UC:
        FID = ReadCrash(URow,F_TargetFID['name'])
        MaxRatio = 0
        MaxIndex = 0
        for i in range(0,len(CrashDic[FID]['IList'])):
            Ratio = CrashDic[FID]['IList'][i]['Ratio']
            if Ratio > MaxRatio:
                MaxRatio = Ratio
                MaxIndex = i
        if MaxRatio > 0:
            if len(CrashDic[FID]['RList']) > 0:
                URow.setValue(F_ICrash ['name'], 1)
                URow.setValue(F_CI_X   ['name'], CrashDic[FID]['IList'][MaxIndex]['X'])
                URow.setValue(F_CI_Y   ['name'], CrashDic[FID]['IList'][MaxIndex]['Y'])
                URow.setValue(F_Dist2CF['name'], CrashDic[FID]['IList'][MaxIndex]['Dist'])
                URow.setValue(F_RFType ['name'], CrashDic[FID]['IList'][MaxIndex]['Type'])
                #arcpy.AddMessage("   FID = " + str(FID) + ', Intersection at ' + str(int(CrashDic[FID]['IList'][MaxIndex]['Dist'])) + ' Feet')
        else:
            if len(CrashDic[FID]['RList']) > 0:
                URow.setValue(F_RCrash ['name'], 1)
                URow.setValue(F_RFType ['name'], CrashDic[FID]['RList'][0]['Type'])
                URow.setValue(F_RFID   ['name'], CrashDic[FID]['RList'][0]['RFID'])
                URow.setValue(F_Dist2CF['name'], CrashDic[FID]['RList'][0]['Dist'])
                #arcpy.AddMessage("   FID = " + str(FID) + ", Roadway at " + str(int(CrashDic[FID]['RList'][0]['Dist'])) + ' Feet')
        UC.updateRow(URow)
        arcpy.SetProgressorPosition(FID)

    arcpy.AddMessage("   Copy: Output")
    arcpy.DeleteField_management(CrashLayer, F_TargetFID['name'])
    arcpy.CopyFeatures_management(CrashLayer, Output)

    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")
def ObservedCrashNC(SitesInput, CrashLayer, Output):
    arcpy.AddMessage("    ")
    arcpy.AddMessage("    Add Observed Crashes")

    OutDic = OutputParser(Output, 'shp')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("    Copy Features: Sites Layer")
    SitesLayer = CopyFeatures(SitesInput,'OCSites')
    TotalSites = int(str(arcpy.GetCount_management(SitesLayer)))
    arcpy.AddMessage("     - Total number of Items Found: " + str(TotalSites))

    arcpy.AddMessage("    Adding Fields")
    CrashFieldDic = [F_TargetFID, F_OC_FIDs, F_TOT_OC, F_FI_OC, F_MV_OC, F_MVFI_OC, F_MVPDO_OC, F_SV_OC, F_SVFI_OC, F_SVPDO_OC, F_Ped_OC]
    for Field in CrashFieldDic:
        arcpy.DeleteField_management(SitesLayer,Field['name'])
    for Field in CrashFieldDic:
        AddField(SitesLayer,Field)
    CalField(SitesLayer,F_TargetFID,'!OBJECTID! - 1')

    arcpy.AddMessage("    Reading Sites Information")
    IntDic = {SRow.getValue(F_TargetFID['name']):{'Type':GetVal(SRow, F_FType['name'], ' '),'MBuffer': max([GetVal(SRow, F_RBuffer['name'], 0), GetVal(SRow, F_ABuffer['name'], 0), GetVal(SRow, F_BBuffer['name'], 0)]),'CList':[]} for SRow in arcpy.SearchCursor(SitesLayer)}

    arcpy.AddMessage("    Spatial Join: CrashLayer + SitesLayer")
    RMaxBuffer = MaximumValue(SitesLayer        ,F_RBuffer['name'])
    IMaxBuffer = MaximumValue(SitesLayer        ,F_BBuffer['name'])
    MaxBuffer  = max([RMaxBuffer, IMaxBuffer])
    SPJ = SpatialJoin(CrashLayer, SitesLayer, "SPJ" , {'join_operation': "JOIN_ONE_TO_ONE", 'join_type': "KEEP_COMMON",'field_mapping': "",'match_option': "CLOSEST",'search_radius': str(MaxBuffer) + " feet",'distance_field_name':'Dist'})
    TotalMatches = int(str(arcpy.GetCount_management(SPJ)))
    arcpy.AddMessage("     - Total number of Items Found: " + str(TotalMatches))

    arcpy.AddMessage("    Appending Crash Information")
    for SRow in arcpy.SearchCursor(SPJ):
        FID     = SRow.getValue(F_TargetFID['name'])
        FType   = SRow.getValue('Shape')
        if ((GetVal(SRow, F_ICrash['name'], 0) == 1 and FType.type == 'point') or (GetVal(SRow, F_RCrash['name'], 0) == 1 and FType.type == 'polyline')) and SRow.getValue('Dist') <= IntDic[FID]['MBuffer']:
            IntDic[FID]['CList'].append({'INJ':GetVal(SRow,F_CT_INJ['name']), 'UNT':GetVal(SRow,F_CT_UNT['name']),'FID':GetVal(SRow,"FID")})

    arcpy.AddMessage("    Update Cursor: Sites Layer")
    def AddCrash(TargetRow,CrashDic):

        INJ = CrashDic['INJ']
        UNT = CrashDic['UNT']
        FID = CrashDic['FID']

        b = TargetRow.getValue(F_OC_FIDs['name'])
        if not b:
            b = ''
        if b == '':
            s = str(FID)
        else:
            if len(b + ',' + str(FID)) < F_OC_FIDs['length']:
                s = b + ',' + str(FID)
            else:
                s = b
        TargetRow.setValue(F_OC_FIDs['name'], s)
    
        b = TargetRow.getValue(F_TOT_OC['name'])
        if not b:
            b = 0
        TargetRow.setValue(F_TOT_OC['name'], b + 1)
        if (INJ in [1,2,3,4]):
            b = TargetRow.getValue(F_FI_OC['name'])
            if not b:
                b = 0
            TargetRow.setValue(F_FI_OC['name'], b + 1)

        if UNT > 1:
            b = TargetRow.getValue(F_MV_OC['name'])
            if not b:
                b = 0
            TargetRow.setValue(F_MV_OC['name'], b + 1)
            if (INJ in [1,2,3,4]):
                b = TargetRow.getValue(F_MVFI_OC['name'])
                if not b:
                    b = 0
                TargetRow.setValue(F_MVFI_OC['name'], b + 1)
            else:
                b = TargetRow.getValue(F_MVPDO_OC['name'])
                if not b:
                    b = 0
                TargetRow.setValue(F_MVPDO_OC['name'], b + 1)
        if UNT <= 1:
            b = TargetRow.getValue(F_SV_OC['name'])
            if not b:
                b = 0
            TargetRow.setValue(F_SV_OC['name'], b + 1)
            if (INJ in [1,2,3,4]):
                b = TargetRow.getValue(F_SVFI_OC['name'])
                if not b:
                    b = 0
                TargetRow.setValue(F_SVFI_OC['name'], b + 1)
            else:
                b = TargetRow.getValue(F_SVPDO_OC['name'])
                if not b:
                    b = 0
                TargetRow.setValue(F_SVPDO_OC['name'], b + 1)
       
        return TargetRow
    Tot_OC = 0
    UC = arcpy.UpdateCursor(SitesLayer)
    for URow in UC:
        RFID    = URow.getValue(F_TargetFID['name'])
        CrashesFound = 0
        for Crash in IntDic[RFID]['CList']:
            URow = AddCrash(URow,Crash)
            CrashesFound += 1
            UC.updateRow(URow)
        #if CrashesFound >= 1:
        #    arcpy.AddMessage("     %5.0f" % RFID + " out of %5.0f" % TotalSites + ", Crashes Found: " + str(CrashesFound))
        Tot_OC += CrashesFound

    arcpy.AddMessage("     - Total Observed Crashes Matched: " + str(Tot_OC))
    arcpy.CopyFeatures_management(SitesLayer, Output)

    for Field in [F_TargetFID, F_OC_FIDs]:
        arcpy.DeleteField_management(Output,Field['name'])

    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")
def EstimateAADT(SitesInput,JoinField1,ProjectAADTYear, AADTTable,JoinField2,BaseAADTYear,GrowthFactor,Output):
    arcpy.AddMessage("    ")
    arcpy.AddMessage("    Estimate AADT")

    OutDic = OutputParser(Output, 'shp')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    if ProjectAADTYear>=BaseAADTYear:
        GF = (1.0+float(GrowthFactor))**(float(ProjectAADTYear)-float(BaseAADTYear))
    if ProjectAADTYear<BaseAADTYear:
        GF = (1.0-float(GrowthFactor))**(-float(ProjectAADTYear)+float(BaseAADTYear))

    arcpy.AddMessage("    Copy Features: Sites Layer")
    SitesLayer = CopyFeatures(SitesInput,'EASites')
    TotalSites = int(str(arcpy.GetCount_management(SitesLayer)))
    arcpy.AddMessage("     - Total number of Items Found: " + str(TotalSites))

    arcpy.AddMessage("    Count Features: AADT Table")
    TotalSites = int(str(arcpy.GetCount_management(AADTTable)))
    arcpy.AddMessage("     - Total number of Items Found: " + str(TotalSites))

    arcpy.AddMessage("    Search Cursor: AADT Table")
    BaseDic = {SRow.getValue(JoinField2):{'AADT_Major':SRow.getValue('AADT_Major'),'AADT_Minor':SRow.getValue('AADT_Minor')} for SRow in arcpy.SearchCursor(AADTTable)}

    arcpy.AddMessage("    Update Cursor: Sites Layer")
    UC = arcpy.UpdateCursor(SitesLayer)
    UpdateNum = 0
    for URow in UC:
        ID = URow.getValue(JoinField1)
        Flag = False
        if ID in BaseDic.keys():
            if not URow.getValue('AADT_Major') > 0:
                URow.setValue('AADT_Major',BaseDic[ID]['AADT_Major']*GF)
                Flag = True
            if not URow.getValue('AADT_Minor') > 0:
                URow.setValue('AADT_Minor',BaseDic[ID]['AADT_Minor']*GF)
                Flag = True
        if Flag:
            UpdateNum += 1
            UC.updateRow(URow)
    
    arcpy.AddMessage("     - Total Updated Rows: " + str(UpdateNum))
    arcpy.CopyFeatures_management(SitesLayer, Output)
    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")

# Spatial Statistics:
def Distance(x1,x2,y1,y2):
    
    return ((x1-x2)**2+(y1-y2)**2)**0.5
def wijGetis1992(Dic,d,i,j):
    Dis = Distance(Dic[i]['X'],Dic[j]['X'],Dic[i]['Y'],Dic[j]['Y'])
    #arcpy.AddMessage([Dic[i]['X'],Dic[j]['X'],Dic[i]['Y'],Dic[j]['Y'],Dis,d])
    if Dis <= d and i<>j:
        return 1
    else:
        return 0
def WeightFactorMatrix(Dic,d,Method):
    if Method == 'Getis1992':
        W = {i:{j:wijGetis1992(Dic,d,i,j) for j in Dic.keys()} for i in Dic.keys()}
    return W
def giGetis1992(Dic,W,i):
    N = 0
    for j in Dic.keys():
        N = N + W[i][j]*Dic[j]['V']
    D = sum([Dic[k]['V'] for k in Dic.keys() if k <> i])
    #arcpy.AddMessage(str([N,D,N/D]))
    return(N/D)
def Zstat(Dic,d,Method):
    GZDic = {i:{'G':0,'Z':0} for i in Dic.keys()}
    if Method == 'Getis1992':
        W = WeightFactorMatrix(Dic,d,Method)
        n = len(Dic)
        for i in Dic.keys():
            Gi    = giGetis1992(Dic,W,i)
            Wi    = sum([wi for wi in W[i].values()])
            SumV2 = sum([Dic[j]['V']    for j in Dic.keys() if j<>i])**2
            Sum2V = sum([Dic[j]['V']**2 for j in Dic.keys() if j<>i])
            EGi   = Wi/(n-1)
            EGi2  = 1/SumV2*(Wi*Sum2V/(n-1)+(Wi**2-Wi)/(n-1)/(n-2)*(SumV2-Sum2V))
            VarG  = EGi2 - EGi**2
            if VarG<=0:
                Zi = 0
            else:
                Zi    = (Gi -EGi)/VarG**0.5
            arcpy.AddMessage(str([Wi,Gi,VarG,Zi]))
            GZDic[i]['G'] = Gi
            GZDic[i]['Z'] = Zi
    return GZDic
def SpatialCorrelation(inLayer,XField,d,Method,Output):
    arcpy.AddMessage("    ")
    arcpy.AddMessage("    Spatial Correlation")

    Method = str(Method)
    d = float(d)
    OutDic = OutputParser(Output, 'shp')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    arcpy.AddMessage("    Copy Features: Sites Layer")
    SitesLayer = CopyFeatures(inLayer,'SCLayer')
    TotalSites = int(str(arcpy.GetCount_management(SitesLayer)))
    arcpy.AddMessage("     - Total number of Items Found: " + str(TotalSites))

    arcpy.AddMessage("    Adding Fields")
    FieldDic = [F_TargetFID,F_GStat,F_ZScore]
    for Field in FieldDic:
        AddField(SitesLayer,Field)
    CalField(SitesLayer,F_TargetFID,'!OBJECTID! - 1')

    arcpy.AddMessage("    Search Cursor: Sites Layer")
    SDic = {SRow.getValue(F_TargetFID['name']):{'X':SRow.getValue('Shape').centroid.X, 'Y':SRow.getValue('Shape').centroid.Y, 'V':SRow.getValue(XField)} for SRow in arcpy.SearchCursor(SitesLayer)}
    
    arcpy.AddMessage("    Calculate Z Scores")
    GZDic = Zstat(SDic,d,Method)

    arcpy.AddMessage("    Update Cursor:Sites Layer")
    UC = arcpy.UpdateCursor(SitesLayer)
    for URow in UC:
        FID = URow.getValue(F_TargetFID['name'])
        URow.setValue(F_ZScore['name'],GZDic[FID]['Z'])
        URow.setValue(F_GStat ['name'],GZDic[FID]['G'])
        UC.updateRow(URow)

    FieldDic = [F_TargetFID]
    for Field in FieldDic:
        arcpy.DeleteField_management(SitesLayer,Field['name'])

    arcpy.CopyFeatures_management(SitesLayer, Output)
    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")
def CFTest(BGInput,IntInput,SegInput,Output):

    OutDic = OutputParser(Output, 'xls')
    Output = OutDic['folder'] + '\\' + OutDic['file']

    def CFSD(OC,PC):
        import numpy
        return((numpy.var(OC)/len(OC)/numpy.mean(PC)**2)**0.5) 
    def ExportasCSV(Dic,Method,File):
        import csv
        fd = 'C:\\Users\\Mahdi\\Dropbox\\R Scripts\\Inputs\\'
        fn = str(File) + '_' + str(Method) + '.csv'
        fo = open(fd+fn,'wb')
        fw = csv.writer(fo)
        fw.writerow(["FID","FType","TOT_OC","TOT_PC","Bin"])
        for fid in Dic.keys():
            fw.writerow([fid,Dic[fid]['Type'],Dic[fid]["OC"],Dic[fid]["PC"],Dic[fid]['Bin']])
        fo.close()
    SPMethods = {1:{'Method':"FIXED_DISTANCE_BAND",'Distance':20000},
                 2:{'Method':"FIXED_DISTANCE_BAND",'Distance':30000},
                 3:{'Method':"FIXED_DISTANCE_BAND",'Distance':40000},
                 4:{'Method':"FIXED_DISTANCE_BAND",'Distance':50000},
                 5:{'Method':"FIXED_DISTANCE_BAND",'Distance':60000},
                 6:{'Method':"FIXED_DISTANCE_BAND",'Distance':70000},
                 7:{'Method':"FIXED_DISTANCE_BAND",'Distance':80000},
                 8:{'Method':"FIXED_DISTANCE_BAND",'Distance':90000},
                 9:{'Method':"FIXED_DISTANCE_BAND",'Distance':100000},
                10:{'Method':"FIXED_DISTANCE_BAND",'Distance':110000},
                11:{'Method':"FIXED_DISTANCE_BAND",'Distance':120000},
                12:{'Method':"FIXED_DISTANCE_BAND",'Distance':130000},
                13:{'Method':"FIXED_DISTANCE_BAND",'Distance':140000},
                14:{'Method':"FIXED_DISTANCE_BAND",'Distance':150000},
                15:{'Method':"FIXED_DISTANCE_BAND",'Distance':160000}}
    AllResults = []
    for i in SPMethods.keys():
        arcpy.AddMessage("    Hotspot Analysis: Method: " + SPMethods[i]['Method'] + ', Distance: ' + str(SPMethods[i]['Distance']))
        HS = arcpy.HotSpots_stats(BGInput, "FitDif", "HS", SPMethods[i]['Method'], "EUCLIDEAN_DISTANCE", "NONE", str(SPMethods[i]['Distance']), "", "", "APPLY_FDR")
        arcpy.AddMessage("    Search Cursor")
        Bin = {SRow.getValue("OBJECTID"):SRow.getValue("Gi_Bin") for SRow in arcpy.SearchCursor(HS)}
        for IntLayer in IntInput.split(";"):
            arcpy.AddMessage("    Spatial Join: " + str(IntLayer))
            SPJ = SpatialJoin(IntLayer,HS,'SPJ'+IntLayer+str(i),{'join_operation': "JOIN_ONE_TO_ONE", 'join_type': "KEEP_ALL",'field_mapping': "",'match_option': "INTERSECT",'search_radius': "",'distance_field_name':''})
            arcpy.AddMessage("    Search Cursor")
            FID1 = {SRow.getValue("TARGET_FID"):{'Bin':SRow.getValue("Gi_Bin"),'OC':SRow.getValue("TOT_OC"),'PC':SRow.getValue("TOT_PC"),'Type':SRow.getValue("FType")} for SRow in arcpy.SearchCursor(SPJ)}
            ExportasCSV(FID1,i,IntLayer)
            for Type in ITypes:
                OCH = [fid1['OC'] for fid1 in FID1.values() if fid1['Bin'] in [2,3   ] and fid1['Type'] == Type]
                OCN = [fid1['OC'] for fid1 in FID1.values() if fid1['Bin'] in [-1,0,1] and fid1['Type'] == Type]
                OCL = [fid1['OC'] for fid1 in FID1.values() if fid1['Bin'] in [-2,-3 ] and fid1['Type'] == Type]
                PCH = [fid1['PC'] for fid1 in FID1.values() if fid1['Bin'] in [2,3   ] and fid1['Type'] == Type]
                PCN = [fid1['PC'] for fid1 in FID1.values() if fid1['Bin'] in [-1,0,1] and fid1['Type'] == Type]
                PCL = [fid1['PC'] for fid1 in FID1.values() if fid1['Bin'] in [-2,-3 ] and fid1['Type'] == Type]
                
                arcpy.AddMessage("    " + str(Type) + ":")
                if sum(OCH)>0 and sum(PCH)>0 and len(OCH)>3:
                    CFH = float(sum(OCH))/float(sum(PCH))
                    Results = {'Type':'','SampleSize':0,'SPMethod':'','Distance':0,'Area':'','CF':0,'SD':0}
                    Results['Type'] = (Type)
                    Results['SampleSize'] = (len(OCH))
                    Results['SPMethod'] = (SPMethods[i]['Method'])
                    Results['Distance'] = (SPMethods[i]['Distance'])
                    Results['Area'] = ('Hotspot' )
                    Results['CF'] = (CFH)
                    Results['SD'] = (CFSD(OCH,PCH))
                    AllResults.append(Results)
                    arcpy.AddMessage("     - " + str(['Hotspot',len(OCH),CFH]))
                
                if sum(OCN)>0 and sum(PCN)>0 and len(OCN)>3:
                    CFN = float(sum(OCN))/float(sum(PCN))
                    Results = {'Type':'','SampleSize':0,'SPMethod':'','Distance':0,'Area':'','CF':0,'SD':0}
                    Results['Type'] = (Type)
                    Results['SampleSize'] = (len(OCN))
                    Results['SPMethod'] = (SPMethods[i]['Method'])
                    Results['Distance'] = (SPMethods[i]['Distance'])
                    Results['Area'] = ('Neutral')
                    Results['CF'] = (CFN)
                    Results['SD'] = (CFSD(OCN,PCN))
                    AllResults.append(Results)
                    arcpy.AddMessage("     - " + str(['Neutral',len(OCN),CFN]))

                if sum(OCL)>0 and sum(PCL)>0 and len(OCL)>3:
                    CFL = float(sum(OCL))/float(sum(PCL))
                    Results = {'Type':'','SampleSize':0,'SPMethod':'','Distance':0,'Area':'','CF':0,'SD':0}
                    Results['Type'] = (Type)
                    Results['SampleSize'] = (len(OCL))
                    Results['SPMethod'] = (SPMethods[i]['Method'])
                    Results['Distance'] = (SPMethods[i]['Distance'])
                    Results['Area'] = ('Coldspot')
                    Results['CF'] = (CFL)
                    Results['SD'] = (CFSD(OCL,PCL))
                    AllResults.append(Results)
                    arcpy.AddMessage("     - " + str(['Coldspot',len(OCL),CFL]))
        for SegLayer in SegInput.split(";"):
            arcpy.AddMessage("    Spatial Join: " + str(SegLayer))
            SPJ = SpatialJoin(SegLayer,HS,'SPJ'+SegLayer+str(i),{'join_operation': "JOIN_ONE_TO_ONE", 'join_type': "KEEP_ALL",'field_mapping': "",'match_option': "INTERSECT",'search_radius': "",'distance_field_name':''})
            arcpy.AddMessage("    Search Cursor")
            FID1 = {SRow.getValue("TARGET_FID"):{'Bin':SRow.getValue("Gi_Bin"),'OC':SRow.getValue("TOT_OC"),'PC':SRow.getValue("TOT_PC"),'Type':SRow.getValue("FType")} for SRow in arcpy.SearchCursor(SPJ)}
            ExportasCSV(FID1,i,SegLayer)
            for Type in RTypes:
                OCH = [fid1['OC'] for fid1 in FID1.values() if fid1['Bin'] in [2,3   ] and fid1['Type'] == Type]
                OCN = [fid1['OC'] for fid1 in FID1.values() if fid1['Bin'] in [-1,0,1] and fid1['Type'] == Type]
                OCL = [fid1['OC'] for fid1 in FID1.values() if fid1['Bin'] in [-2,-3 ] and fid1['Type'] == Type]
                PCH = [fid1['PC'] for fid1 in FID1.values() if fid1['Bin'] in [2,3   ] and fid1['Type'] == Type]
                PCN = [fid1['PC'] for fid1 in FID1.values() if fid1['Bin'] in [-1,0,1] and fid1['Type'] == Type]
                PCL = [fid1['PC'] for fid1 in FID1.values() if fid1['Bin'] in [-2,-3 ] and fid1['Type'] == Type]

                arcpy.AddMessage("    " + str(Type) + ":")
                if sum(OCH)>0 and sum(PCH)>0 and len(OCH)>3:
                    CFH = float(sum(OCH))/float(sum(PCH))
                    Results = {'Type':'','SampleSize':0,'SPMethod':'','Distance':0,'Area':'','CF':0,'SD':0}
                    Results['Type'] = (Type)
                    Results['SampleSize'] = (len(OCH))
                    Results['SPMethod'] = (SPMethods[i]['Method'])
                    Results['Distance'] = (SPMethods[i]['Distance'])
                    Results['Area'] = ('Hotspot' )
                    Results['CF'] = (CFH)
                    Results['SD'] = (CFSD(OCH,PCH))
                    AllResults.append(Results)
                    arcpy.AddMessage("     - " + str(['Hotspot',len(OCH),CFH]))
                
                if sum(OCN)>0 and sum(PCN)>0 and len(OCN)>3:
                    CFN = float(sum(OCN))/float(sum(PCN))
                    Results = {'Type':'','SampleSize':0,'SPMethod':'','Distance':0,'Area':'','CF':0,'SD':0}
                    Results['Type'] = (Type)
                    Results['SampleSize'] = (len(OCN))
                    Results['SPMethod'] = (SPMethods[i]['Method'])
                    Results['Distance'] = (SPMethods[i]['Distance'])
                    Results['Area'] = ('Neutral')
                    Results['CF'] = (CFN)
                    Results['SD'] = (CFSD(OCN,PCN))
                    AllResults.append(Results)
                    arcpy.AddMessage("     - " + str(['Neutral',len(OCN),CFN]))

                if sum(OCL)>0 and sum(PCL)>0 and len(OCL)>3:
                    CFL = float(sum(OCL))/float(sum(PCL))
                    Results = {'Type':'','SampleSize':0,'SPMethod':'','Distance':0,'Area':'','CF':0,'SD':0}
                    Results['Type'] = (Type)
                    Results['SampleSize'] = (len(OCL))
                    Results['SPMethod'] = (SPMethods[i]['Method'])
                    Results['Distance'] = (SPMethods[i]['Distance'])
                    Results['Area'] = ('Coldspot')
                    Results['CF'] = (CFL)
                    Results['SD'] = (CFSD(OCL,PCL))
                    AllResults.append(Results)
                    arcpy.AddMessage("     - " + str(['Coldspot',len(OCL),CFL]))

    tempTable = CreateFeatureclass('Temp_Table',{'geometry_type':"POINT"})
    StatDic = [F_FType, F_TOT_OC,F_TOT_PC,F_CCMF,F_IRouteFIDs,F_Length,F_Dist2CF,F_CI_X,F_OC_FIDs]
    arcpy.AddMessage("    Create Output")
    for Field in StatDic:
        AddField(tempTable,Field)
    arcpy.AddMessage("    Insert Cursor")
    IC = arcpy.InsertCursor(tempTable)
    for Result in AllResults:
        NewRow = IC.newRow()
        NewRow.setValue(F_FType  ['name'],Result['Type'])
        NewRow.setValue(F_Length ['name'],Result['SampleSize'])
        NewRow.setValue(F_OC_FIDs['name'],Result['SPMethod'])
        NewRow.setValue(F_Dist2CF['name'],Result['Distance'])
        NewRow.setValue(F_IRouteFIDs['name'],Result['Area'])
        NewRow.setValue(F_CCMF['name'],Result['CF'])
        NewRow.setValue(F_CI_X['name'],Result['SD'])
        IC.insertRow(NewRow)
    arcpy.TableToExcel_conversion(tempTable, Output)

    arcpy.AddMessage("   --> Done.")
    arcpy.AddMessage(" ")

# Functions
def RouteNameFeature(L,R):
    import pandas
    print('Define Dict')
    RDict = {r.getValue('Name'):{'FeatureL':[],'NameL':[],'Name':'','Feature':''} for r in arcpy.SearchCursor(L)}
    print('Search Cursor')
    for r in arcpy.SearchCursor(L):
            n = r.getValue('Name')
            #F = r.getValue('FEATURE_TY')
            N = r.getValue('STREET_NAM')
            #if not F in [' ','']:
            #    RDict[n]['FeatureL'].append(F)
            if not N in [' ','']:
                RDict[n]['NameL'].append(N)    
    print('Find Names')
    for n in RDict.keys():
        #s = pandas.Series(RDict[n]['FeatureL'])
        #d = dict(s.value_counts())
        #if len(d)>0:
        #    m = max(d.values())
        #    x = [x for x in d if d[x] == m][0]
        #    RDict[n]['Feature'] = x
        s = pandas.Series(RDict[n]['NameL'])
        d = dict(s.value_counts())
        if len(d)>0:
            m = max(d.values())
            x = [x for x in d if d[x] == m][0]
            RDict[n]['Name'] = x
    print('Update Cursor')
    UC = arcpy.UpdateCursor(R)
    for r in UC:
        n = r.getValue('Name')
        r.setValue('StreetName',RDict[n]['Name'])
        UC.updateRow(r)
def PedApprDirection(Loc,Unit):
    print('Pedestrian Approach Direction')
    print(' - Search Cursor(Unit): Finding UTC=41 ANOs')
    anoL = []
    for r in arcpy.SearchCursor(Unit):
        if r.getValue('UTC')==41:
            anoL.append(r.getValue('ANO'))
    
    print(' - Search Cursor(Unit): Reading DOT for Selected ANOs')
    Dir = {ano:{'VehDir':'','PedDir':'','PedAppr':''} for ano in anoL}
    for r in arcpy.SearchCursor(Unit):
        ano = r.getValue('ANO') 
        if ano in anoL:
            utc = r.getValue('UTC')
            if utc in [1,12,13,14,15,16,17,61,62,98,99]:
                Dir[ano]['VehDir'] = r.getValue('DOT')
            if utc in [41]:
                Dir[ano]['PedDir'] = r.getValue('DOT')

    print(' - Delete/Add Field (PedAppr) to Loc')
    arcpy.DeleteField_management(Loc,'PedAppr')
    arcpy.AddField_management(Loc,'PedAppr','SHORT')

    print(' - Update Cursor(Loc): Calculating Ped Appr Direction')
    DirDict = {'NN':'S','SS':'S','WW':'S','EE':'S',
               'NS':'O','SN':'O','WE':'O','EW':'O',
               'NW':'R','SE':'R','WN':'R','ES':'R',
               'NE':'L','SW':'L','WS':'L','EN':'L'}
    DirCode = {'S':1,'O':2,'R':3,'L':4}
    UC = arcpy.UpdateCursor(Loc)
    for URow in UC:
        ano = URow.getValue('ANO') 
        if ano in anoL:
            if Dir[ano]['VehDir']+Dir[ano]['PedDir'] in DirDict.keys():
                URow.setValue('PedAppr',DirCode[DirDict[Dir[ano]['VehDir']+Dir[ano]['PedDir']]])
                UC.updateRow(URow)
    del UC
    print(' - Code Dictionary:' + str(DirCode))
    print(' - Done')
def CreateLocalLRS(L):
    def FindDirection(FP,LP):
        x = LP.X - FP.X
        y = LP.Y - LP.Y
        if x > 0:
            if y>=x:return('N')
            if y<x and y>-x: return('E')
            if y<=-x:return('S')
        if x==0:
            if y>=x: return('N')
            if y<x:return('S')
        if x < 0:
            if y>=-x:return('N')
            if y<-x and y>x: return('W')
            if y<=x:return('S')
    arcpy.AddMessage("  Update Cursor")
    CDict     = {i:0 for i in range(1,47)}
    RNumbDict = {i:[] for i in range(1,47)}
    for SRow in arcpy.SearchCursor(L):
        County = SRow.getValue('COUNTY')
        RNumbDict[County].append(SRow.getValue('ROUTE_NUMB'))
    UC = arcpy.UpdateCursor(L)
    for URow in UC:
        Cnty = URow.getValue('COUNTY')

        rt = 9
        
        rn = URow.getValue('ROUTE_NUMB')
        if rn == 0 or rn is None:
                CDict[Cnty] += 1
                while CDict[Cnty] in RNumbDict[Cnty]:
                    CDict[Cnty] += 1
                rn = CDict[Cnty]
                URow.setValue('ROUTE_NUMB',rn)

        s = URow.getValue('Shape')
        dir = FindDirection(s.firstPoint,s.lastPoint)
        URow.setValue('ROUTE_DIRE',dir)
        
        aux = 0

        oneway = 0
        if oneway == 0:
            dir = 'T'
        #print(str([Cnty,rt,rn,aux,dir]))
        n = '{:02.0f}{:02.0f}{:05.0f}{:02.0f}{}'.format(Cnty,rt,rn,aux,dir)
        URow.setValue('Name',n)

        UC.updateRow(URow)
    del UC
def BatchCrashFromWindow():
    arcpy.ImportToolbox( os.path.abspath("C:\Users\mrajabi\Dropbox\Python Scripts\T2.tbx"))
    Years = range(2007,2016)
    Loc = ['SC_Crash_'+str(y)+'_Loc.txt' for y in Years]
    Unit = ['SC_Crash_'+str(y)+'_Unit.txt' for y in Years]
    Occ = ['SC_Crash_'+str(y)+'_Occ.txt' for y in Years]
    StateBoundary = 'SC_State'
    Jur = 'Jurisdiction'
    for i in range(0,len(Years)):
        arcpy.AddMessage(Years[i])
        arcpy.AddMessage(Loc[i])
        arcpy.AddMessage(Unit[i])
        arcpy.AddMessage(Occ[i])

        arcpy.Delete_management('Geo'+str(Years[i]))
        arcpy.Delete_management('Out'+str(Years[i]))
        Geo = arcpy.CrashGeocode(Loc[i],"LAT","LON","ANO",Years[i],StateBoundary,'Geo'+str(Years[i]),'Out'+str(Years[i]))

        arcpy.Delete_management('Att'+str(Years[i]))
        Att = arcpy.ImpotCrashAttributes('Geo'+str(Years[i]),Loc[i],'Att'+str(Years[i]))
        arcpy.Delete_management('OutAtt'+str(Years[i]))
        OutAtt = arcpy.ImpotCrashAttributes('Out'+str(Years[i]),Loc[i],'OutAtt'+str(Years[i]))

        arcpy.AddField('Att'+str(Years[i]),F_CT_Symbol)
        arcpy.CalField('Att'+str(Years[i]),F_CT_Symbol,'fval(!UNT!,!FAT!,!INJ!)',"""def fval(unt,fat,inj):
        s1 = 'MV'
        if unt<2:
            s1 = 'SV'
        s2 = 'PDO'
        if inj>0:
            s2 = 'Inj'
        if fat>0:
            s2 = 'Fat'
        code = {'MVFat':1,'MVInj':2,'MVPDO':3,'SVFat':4,'SVInj':5,'SVPDO':6}
        return(code[s1+s2])""")
        AddField('Att'+str(Years[i]),F_Route_LRS)
        CalField('Att'+str(Years[i]),F_Route_LRS,'fval( !CTY!, !RCT!, !RTN!, !RAI!, !DLR!, !TWAY!)',"""def fval(cnty,rt,rn,aux,dir,oneway):
            rtdict = {1:1,2:2,3:4,4:7,5:9}
            if rt in rtdict.keys():
                rt = rtdict[rt]
            if not dir in ['E','W','N','S']:
                dir = 'T'
            if oneway in [2,3]:
                dir = 'T'
            if not rn>0:
                rn=0
            return('{:02.0f}{:02.0f}{:05.0f}{:02.0f}{}'.format(cnty,rt,rn,aux,dir))""")
        AddField('OutAtt'+str(Years[i]),F_Route_LRS)
        CalField('OutAtt'+str(Years[i]),F_Route_LRS,'fval( !CTY!, !RCT!, !RTN!, !RAI!, !DLR!, !TWAY!)',"""def fval(cnty,rt,rn,aux,dir,oneway):
            rtdict = {1:1,2:2,3:4,4:7,5:9}
            if rt in rtdict.keys():
                rt = rtdict[rt]
            if not dir in ['E','W','N','S']:
                dir = 'T'
            if oneway in [2,3]:
                dir = 'T'
            if not rn>0:
                rn=0
            return('{:02.0f}{:02.0f}{:05.0f}{:02.0f}{}'.format(cnty,rt,rn,aux,dir))""")

        arcpy.Delete_management('Sec'+str(Years[i]))
        Sec = SecondaryCrashes('Att'+str(Years[i]),2,2500,'Sec'+str(Years[i]))
        SecL = MakeFeatureLayer('Sec'+str(Years[i]),'SecL'+str(Years[i]))
        arcpy.SelectLayerByAttribute_management(SecL,'NEW_SELECTION',"PrmSec IS NOT NULL AND PrmSec <> 'Primary'")
        Sec = CopyFeatures(SecL,'SelSecL')
        ClearFields(Sec,[F_CT_ANO['name'],F_CT_Label['name'],F_CT_PrmSec['name'],F_CT_Tempor['name'],F_CT_Spatio['name']])
        CalField(Sec,F_CT_Label,"'{:3.0f}{}{:4.0f}{}'.format(!"+F_CT_Tempor['name']+"!,' Min, ',!"+F_CT_Spatio['name']+"!,' Feet')")
        AddField(Sec,F_CT_PrmANO)
        CalField(Sec,F_CT_PrmANO,'!'+F_CT_PrmSec['name']+'!')
        arcpy.DeleteField_management(Sec,F_CT_PrmSec['name'])

        arcpy.Delete_management('Unit'+str(Years[i]))
        UTb = ImpotUnitAttributes(Unit[i],Years[i],'Unit'+str(Years[i]))

        arcpy.Delete_management('Occ'+str(Years[i]))
        OTb = ImpotOccAttributes(Occ[i],Years[i],'Occ'+str(Years[i]))

        GDB = CreateGeodatabase('Att'+str(Years[i]),'Unit'+str(Years[i]),'Occ'+str(Years[i]),'OutAtt'+str(Years[i]),Years[i],OutputPath+'\\SC_Crash_'+str(Years[i])+'.mdb')
        
        arcpy.AddMessage('    Add Secondary Table')
        Sec = arcpy.TableToTable_conversion(Sec,OutputPath+'\\SC_Crash_'+str(Years[i])+'.mdb','Sec'+str(Years[i]))
        arcpy.AddMessage('    Add Jurisdiction Feature Class')
        JurTab = arcpy.FeatureClassToFeatureClass_conversion(Jur,OutputPath+'\\SC_Crash_'+str(Years[i])+'.mdb','Jur')
        
        L   = OutputPath+'\\SC_Crash_'+str(Years[i])+'.mdb\\'+'Loc'+str(Years[i])
        Sec = OutputPath+'\\SC_Crash_'+str(Years[i])+'.mdb\\'+'Sec'+str(Years[i])
        Out = OutputPath+'\\SC_Crash_'+str(Years[i])+'.mdb\\'+'Out'+str(Years[i])
        UTb = OutputPath+'\\SC_Crash_'+str(Years[i])+'.mdb\\'+'Unit'+str(Years[i])
        JUR = OutputPath+'\\SC_Crash_'+str(Years[i])+'.mdb\\'+'Jur'

        arcpy.AddMessage('    Create Relationships')
        arcpy.CreateRelationshipClass_management(L, Sec, OutputPath+'\\SC_Crash_'+str(Years[i])+'.mdb'+"\\PriCrash-SecTable", "SIMPLE", "Secondary Table", "Primary Crash"  , "NONE", "ONE_TO_MANY", "NONE", "ANO", F_CT_PrmANO['name'])    
        arcpy.CreateRelationshipClass_management(Sec, L, OutputPath+'\\SC_Crash_'+str(Years[i])+'.mdb'+"\\SecTable-SecCrash", "SIMPLE", "Secondary Crash", "Secondary Table", "NONE", "ONE_TO_ONE" , "NONE", "ANO", "ANO")    
        arcpy.CreateRelationshipClass_management(L, JUR, OutputPath+'\\SC_Crash_'+str(Years[i])+'.mdb'+"\\Loc-Jur"          , "SIMPLE", "Jur Table"      , "Loc Table"      , "NONE", "ONE_TO_MANY", "NONE", "JUR", "JUR")    
        
        arcpy.AddMessage('    Add Representation')
        try:
            arcpy.AddRepresentation_cartography(L,"CrashType","NU_Sev","Override","STORE_CHANGE_AS_OVERRIDE","C:\\Users\\mrajabi\\Dropbox\\GDB Crash layer.lyr","ASSIGN")
        except:
            DoNothing = True        
        try:
            arcpy.CalculateField_management(L,'NU_Sev','!'+F_CT_Symbol['name']+'!',"PYTHON_9.3")
        except:
            DoNothing = True
        try:
            arcpy.AddMessage('    Compact the Database')
            arcpy.Compact_management(OutputPath+'\\SC_Crash_'+str(Years[i])+'.mdb')
            #arcpy.CompressFileGeodatabaseData_management (OutputPath+'\\SC_Crash_'+str(Years[i])+'.mdb', "Lossless compression")
        except:
            DoNothing = True
def FindCrashLRS(R,C):
    import copy
    def CrashLRS(cd,MBS):

            rtdict = {1:1,2:2,3:4,4:7,5:9}
            if not cd[MBS]['typ'] in rtdict.keys(): rt = 5
            rt = rtdict[cd[MBS]['typ']]

            rn = copy.deepcopy(cd[MBS]['num'])
            if not rn>0:
                rn=0

            radict = {0:0,2:2,5:5,6:6,7:7,9:81}
            if not cd[MBS]['aux'] in radict: ra = 0
            ra = radict[cd[MBS]['aux']]
            
            dir = copy.deepcopy(cd[MBS]['dir'])
            if not dir in ['E','W','N','S']:
                dir = 'T'
            
            return('{:02.0f}{:02.0f}{:05.0f}{:02.0f}{}'.format(cd['County'],rt,rn,ra,dir))
    def ExplodeLRS(lrs):
        cnty = int(lrs[0:2])
        rt   = int(lrs[2:4])
        rn   = int(lrs[4:9])
        ra   = int(lrs[9:11])
        dir  =    (lrs[-1])
        return({'County':cnty,'typ':rt,'num':rn,'aux':ra,'dir':dir})
    def FindMLRS(cd,LRSD,RD,oldMLRS='',oldBLRS='',oldSLRS='',oldCMP=-1,oldBMP=-1,oldSMP=-1):
        if cd['P']<>'':
            if cd['Main']['num']>0:
                MLRS = CrashLRS(cd['County'],cd['Main']['typ'],cd['Main']['num'],cd['Main']['aux'],cd['Main']['dir'],cd['TWAY'])
                if MLRS in LRSD.keys():
                    q = LRSD[MLRS].queryPointAndDistance(cd['P'])
                    SnapP = q[0]
                    CMP = q[1]/5280
                    MLO = q[2]
                    MLODir = q[3]
    def StreetNameLRS(cd,MBS,RD,LRSD,MLRS=''):
        LRS = []
        if cd[MBS]['nam'] <> '' and cd[MBS]['nam'] in RD.keys():
            for lrs in RD[cd[MBS]['nam']]:
                exlrs = ExplodeLRS(lrs)
                if exlrs['County']==cd['County'] and exlrs['typ']==cd[MBS]['typ']:
                   LRS.append(lrs)
        if len(LRS)>1:
            if MBS == 'M':
                    if cd['P'] <> '':
                        dist = []
                        for lrs in LRS:
                            dist.append(LRSD[lrs].distanceTo(cd['P']))
                        md = min(dist)
                        LRS = LRS[dist.index(md)]
            if MBS in ['B','S']:
                nL = []
                for lrs in LRS:
                    if MLRS in LRSD.keys():
                        if LRSD[lrs].touches(LRSD[MLRS]):
                            nL.append(lrs)
                if len(nL)==1:
                    LRS = nL[0]
                if len(nL)>1:
                    dist = []
                    for lrs in nL:
                        dist.append(LRSD[lrs].distanceTo(cd['P']))
                    md = min(dist)
                    LRS = nL[dist.index(md)]
                if len(nL)==0:
                    dist = []
                    for lrs in LRS:
                        dist.append(LRSD[lrs].distanceTo(cd['P']))
                    md = min(dist)
                    LRS = LRS[dist.index(md)]
        else:
            if len(LRS)==0:LRS=''
            if len(LRS)==1:LRS=LRS[0]
        return(LRS)
    # Reading crash data
    CD = {r.getValue('ANO'):{'County':r.getValue(F_CT_CTY['name']),'P':r.getValue('Shape'),'RouteL':[],
                             'M':{'typ':r.getValue(F_CT_RCT['name']),'num':r.getValue(F_CT_RTN['name']),'aux':r.getValue(F_CT_RAI['name']),'dir':r.getValue(F_CT_DLR['name']),'nam':r.getValue(F_CT_ALS ['name']),'LRS':''},
                             'B':{'typ':r.getValue(F_CT_BIR['name']),'num':r.getValue(F_CT_BRN['name']),'aux':r.getValue(F_CT_BRA['name']),'dir':''                          ,'nam':r.getValue(F_CT_ALSB['name']),'LRS':''},
                             'S':{'typ':r.getValue(F_CT_SIC['name']),'num':r.getValue(F_CT_SRN['name']),'aux':r.getValue(F_CT_SRA['name']),'dir':''                          ,'nam':r.getValue(F_CT_ALSS['name']),'LRS':''}}
          for r in arcpy.SearchCursor(C)}
    # format crash data: County, route type, route aux
    for ano in CD:
        if not CD[ano]['County'] in range(1,47):
            print('No County')
            exit()
        for MBS in ['M','B','S']:
            if not CD[ano][MBS]['typ'] in [1,2,3,4,5]:
                CD[ano][MBS]['typ'] = 5
        for MBS in ['M','B','S']:
            if not CD[ano][MBS]['aux'] in [0,2,5,6,7,9]:
                CD[ano][MBS]['aux'] = 0

    # reading roadway data: street names and lrs
    RD = {}
    for r in arcpy.SearchCursor(R):
        N1 = r.getValue('StreetN1')
        N2 = r.getValue('StreetN2')
        RD.update({N1:[],N2:[]})
    for r in arcpy.SearchCursor(R):
        N1 = r.getValue('StreetN1')
        N2 = r.getValue('StreetN2')
        if N1<>'':RD[N1].append(r.getValue('Name'))
        if N2<>'':RD[N2].append(r.getValue('Name'))
    
    LRSD = {r.getValue('Name'):r.getValue('Shape') for r in arcpy.SearchCursor(R)}
    
    #Spatial Join    
    arcpy.Delete_management('SPJRC')
    SPJ = arcpy.SpatialJoin_analysis(C,R,'SPJRC',"JOIN_ONE_TO_MANY","KEEP_COMMON",'',"WITHIN_A_DISTANCE",'250 Feet')
    for r in arcpy.SearchCursor(SPJ):
        ano = r.getValue('ANO')
        CD[ano]['RouteL'].append(r.getValue('Name'))

    Dirs = ['N','S','W','E','T']
    for field in [F_CT_MLRS,F_CT_BLRS,F_CT_SLRS]:
        AddField(C,field)
    UC = arcpy.UpdateCursor(C)
    i = 0
    for URow in UC:
        i += 1
        ano = URow.getValue('ANO')
        # First guess MLRS
        MLRS = CrashLRS(CD[ano],'M')
        if not MLRS in LRSD.keys():
            CD[ano]['M']['dir'] = 'T'
            MLRS = CrashLRS(CD[ano],'M')
        if not MLRS in LRSD.keys():
            MLRS = StreetNameLRS(CD[ano],'M',RD,LRSD)
        # First guess BLRS and SLRS        
        BLRS = []
        SLRS  = []
        for dir in Dirs:
            CD[ano]['B']['dir'] = dir
            CD[ano]['S' ]['dir'] = dir
            lrs = CrashLRS(CD[ano],'B')
            if lrs in LRSD.keys():
                BLRS.append(lrs)
            lrs = CrashLRS(CD[ano],'S')
            if lrs in LRSD.keys():
                SLRS.append(lrs)
        if len(BLRS)==0:
            BLRS = StreetNameLRS(CD[ano],'B',RD,LRSD)
        if len(SLRS)==0:
            SLRS = StreetNameLRS(CD[ano],'S',RD,LRSD)
        
        URow.setValue('MLRS',str(MLRS))    
        URow.setValue('BLRS',str(BLRS))    
        URow.setValue('SLRS',str(SLRS))    
        print(i,ano, str(MLRS),str(BLRS),str(SLRS)  ) 
            
        UC.updateRow(URow)
