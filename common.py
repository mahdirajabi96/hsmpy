import arcpy
import sys
import math
import urllib
import zipfile
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import args
from ftplib import FTP
from urlparse import urlparse
import subprocess
import time
import shutil
from time import gmtime, strftime

NAD1983IL = arcpy.SpatialReference(102672)
NAD1983SC = arcpy.SpatialReference(102733)
NAD1983NC = arcpy.SpatialReference(2264)
WGS1984   = arcpy.SpatialReference(4326)
# Find the route between two points, local HSIP projects
FRTypes= ['U4F', 'U6F', 'R4F']
RTypes = ['R2U', 'R4U', 'R4D', 'U2U', 'U3T', 'U4D', 'U4U', 'U5T']
ITypes = ['R3ST' ,'R4ST' , 'R4SG', 'RM3ST', 'RM4ST', 'RM4SG', 'U3ST', 'U4ST', 'U3SG', 'U4SG']
FTypes = RTypes + ITypes + FRTypes

def Downloadfile(URL,OutputDir,extension,filterForSC=False):
    name = os.path.join(OutputDir, URL.split('/')[-1])
    urlp = urlparse(URL)
    print('Downloading: '+URL)
    try:
        if urlp.scheme == 'ftp':
            ftp = FTP(urlp.hostname)
            ftp.login()
            ftp.retrbinary('RETR '+urlp.path, open(name, 'wb').write)
        if urlp.scheme == 'http':
            urllib.urlretrieve(URL, name)
    except IOError, e:
        print "Can't retrieve %r to %r: %s" % (URL, OutputDir, e)
        return
    try:
        z = zipfile.ZipFile(name)
    except zipfile.error, e:
        print "Bad zipfile (from %r): %s" % (URL, e)
        return
    shapefile = []
    #print('Extracting:')
    for n in z.namelist():
        #print(n)
        if n.split('.')[-1] == extension:
            shapefile.append(n)
    z.extractall(OutputDir)
    output = [os.path.join(OutputDir,shp) for shp in shapefile]
    if filterForSC:
        print('Filtering for STATEFP = 45')
        filter_output = os.path.splitext(output)[0] + '_Filtered' + os.path.splitext(output)[1]
        arcpy.Delete_management(filter_output)
        arcpy.Select_analysis(in_features=output,
                              out_feature_class=filter_output,
                              where_clause=""""STATEFP"='45'""")
        output = filter_output
        #sum = PrintSummary(output)
    #else:
        #sum = PrintSummary(output)
    print('\n'.join(output))
    return(output)
def GetFID(Row):
    FID = ''
    try:
        FID = Row.getValue('FID')
    except:
        try:
            FID = Row.getValue('OBJECTID')
        except:
            print("FID or OBJECTID not Found")
    return FID
def GetVal(Row, Field, Default=0, AddWarning=False):
    try:
        Val = Row.getValue(Field)
        #return(Val)
        if not Val is None:
            return Val
        else:
        #    if AddWarning: print('Failed to read: ' + Field + ', Default value Assigned')
            return Default
    except:
        if AddWarning: print('Failed to read: ' + Field + ', Default value Assigned')
        return Default
def GetIntVal(Row, Field, Default=0, AddWarning=False):
        try:
            Val = int(Row.getValue(Field))
            if not Val is None:
                return Val
            else:
                if AddWarning: print('Failed to read: ' + Field + ', Default value Assigned')
                return Default
        except:
            if AddWarning: print('Failed to read: ' + Field + ', Default value Assigned')
            return Default
def GetFloatVal(Row, Field, Default=0.0, AddWarning=False):
        try:
            Val = float(Row.getValue(Field))
            if not Val is None:
                return Val
            else:
                if AddWarning: print('Failed to read: ' + Field + ', Default value Assigned')
                return Default
        except:
            if AddWarning: print('Failed to read: ' + Field + ', Default value Assigned')
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
def GetANO(Row, IntErr=-1, RowErr=99999999):
        if Row:
            ANO = Row.getValue('ANO')
            try:
                ANO = int(ANO)
            except:
                ANO = IntErr
        else:
            ANO = RowErr
        if int(str(ANO)[0:4]) in [2001,2005,2006]:
            ANO = int(str(ANO)[2:])
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
def GetDistance(P1,P2):
        X1 = P1.firstPoint.X
        X2 = P2.firstPoint.X
        Y1 = P1.firstPoint.Y
        Y2 = P2.firstPoint.Y
        return(((X1-X2)**2+(Y1-Y2)**2)**0.5)
def NaturalLog(A):
        
        if A > 0:
            return math.log1p(A - 1)
        else:
            return 0
def PrintSummary(Input,extension='shp'):
    desc = arcpy.Describe(Input)
    ext = extension
    out = {'ShapeType':'','Rows':'','Columns':''}
    if ext == 'shp':
        print('Type: ' + desc.shapeType)
        FieldObjList = arcpy.ListFields(Input)
        FieldNameList = [Field.name for Field in arcpy.ListFields(Input)]
        FieldNameList.sort()
        TotalSites = int(str(arcpy.GetCount_management(Input)))
        print("Columns: " + str(len(FieldNameList)) + " x Rows: " + str(TotalSites))
        print(FieldNameList)
        out = {'ShapeType':desc.shapeType,'Rows':TotalSites,'Columns':FieldNameList}
    if ext == 'rrd':
        print('Type: ' + desc.format)
        out['Type']=desc.format
    return(out)
def FieldSummary(Layer,FieldName):
    s1 = pd.Series([row.getValue(FieldName) for row in arcpy.SearchCursor(Layer)])
    plt.bar(np.arange(len(s1.value_counts())),list(s1.value_counts()),align	= 'center')
    plt.xticks(np.arange(len(s1.value_counts())),list(s1.value_counts().index), rotation='vertical')
    plt.xlabel(FieldName)
    plt.title(os.path.basename(Layer))
    plt.show()
    return(s1.value_counts())
def Distance(x1,x2,y1,y2):
    return ((x1-x2)**2+(y1-y2)**2)**0.5
def CreateOutPath(MainFile,appendix,Extension = 'shp'):
    if Extension <> '':
        out = os.path.splitext(MainFile)[0] + '_' + appendix + '.' + Extension
    else:
        out = os.path.splitext(MainFile)[0] + '_' + appendix
    try:
        arcpy.Delete_management(out)
    except:
        pass
    return(out)
def CreateOutLayer(Name):
    out = Name
    try:
        arcpy.Delete_management(out)
    except:
        pass
    return(out)
def IRIS_HSM_ShType(SHD_TYP):
    #Converts IRIS shoulder type for hsmpy
    IRIS = {0: 'Not applicable',1: 'Earth',2: 'Sod',3: 'Aggregate',4: 'treated',5: 'Bituminous',6: 'Concrete-untied',7: 'Concrete-tied',8: 'V Gutter',9: 'Curb and Gutter'}
    HSMPY = {'Paved':1,'Gravel':2,'Composite':3,'Turf':4}
    Conv = {'Not applicable':'Turf',
        'Earth':'Turf',
        'Sod':'Turf',
        'Aggregate':'Gravel',
        'treated':'Paved',
        'Bituminous':'Paved',
        'Concrete-untied':'Paved',
        'Concrete-tied':'Paved',
        'V Gutter':'Paved',
        'Curb and Gutter':'Paved'}
    return(HSMPY[Conv[IRIS[SHD_TYP]]])
def AddField(FC,Fields):
    for field in Fields:
        try:
            res = arcpy.AddField_management(FC,field['name'],field['type'],field['precision'],field['scale'],field['length'],field['alias'],field['nullable'],field['required'])
        except:
            try:
                print(res.res.getMessages())
            except:
                pass
            pass
def AddPointFromAddress(Input,AddressField):
    import requests
    APIKey = 'AIzaSyCs80htAI4UAHHuF5m9IclsbMqg1FKxoEQ'
    UC = arcpy.UpdateCursor(Input)
    for r in UC:
        Address = r.getValue(AddressField)
        response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=' 
                                + Address.replace(' ','+') +
                               '&key=' + APIKey)
        resp_json_payload = response.json()
        if resp_json_payload['status'] == 'OK':
            
            pnt = arcpy.Point(resp_json_payload['results'][0]['geometry']['location']['lng'],
                          resp_json_payload['results'][0]['geometry']['location']['lat'])
            pntg = arcpy.PointGeometry(pnt,WGS1984).projectAs(NAD1983IL)
            r.setValue(arcpy.Describe(Input).shapeFieldName,pntg)
            UC.updateRow(r)
        else:
            print(resp_json_payload['status'])
        print(','.join([Address,
                        str(resp_json_payload['results'][0]['geometry']['location']['lng']),
                        str(resp_json_payload['results'][0]['geometry']['location']['lat']),
                        str(pntg.firstPoint.X),
                        str(pntg.firstPoint.Y),
                        resp_json_payload['status']]))
    del UC
    del r
def AddSegFromAddresses(AddressList,SegInput,RouteID,Output):
    import requests
    APIKey = 'AIzaSyCs80htAI4UAHHuF5m9IclsbMqg1FKxoEQ'

    PntLayer = CreateOutPath(Output,'pnts','')
    arcpy.CreateFeatureclass_management(
        out_path = os.path.dirname(Output),
        out_name = os.path.basename(PntLayer),
        geometry_type='POINT',
        spatial_reference=NAD1983IL)
    arcpy.AddField_management(PntLayer,'SegID','SHORT')
    arcpy.AddField_management(PntLayer,'Address','TEXT')
    IC = arcpy.InsertCursor(PntLayer)
    i = 0
    for add in AddressList:
        r = IC.newRow()
        r.setValue('SegID',i)
        r.setValue('Address',add[0])
        IC.insertRow(r)
        r = IC.newRow()
        r.setValue('SegID',i)
        r.setValue('Address',add[1])
        IC.insertRow(r)
        i += 1
    del IC
    AddPointFromAddress(PntLayer,'Address')
    
    Buffer = "200 Feet"
    SPJ = CreateOutPath(MainFile=Output,appendix='SPJ',Extension='')
    arcpy.SpatialJoin_analysis(
        target_features = SegInput, 
        join_features = PntLayer, 
        out_feature_class = SPJ, 
        join_operation = "JOIN_ONE_TO_ONE", 
        join_type = "KEEP_COMMON", 
        match_option = "INTERSECT", 
        search_radius = Buffer, 
    )

    UnSplt = CreateOutPath(MainFile=Output,appendix='Unsplt',Extension='')
    arcpy.UnsplitLine_management(
        in_features=SPJ, 
        out_feature_class=UnSplt, 
        dissolve_field="", 
        statistics_fields="")

    SPJ2 = CreateOutPath(MainFile=Output,appendix='SPJ2',Extension='')
    arcpy.SpatialJoin_analysis(
        target_features = UnSplt, 
        join_features = PntLayer, 
        out_feature_class = SPJ2, 
        join_operation = "JOIN_ONE_TO_ONE", 
        join_type = "KEEP_COMMON", 
        match_option = "INTERSECT", 
        search_radius = Buffer, 
    )

    Final_Layer = CreateOutLayer('FinalLayer')
    arcpy.MakeFeatureLayer_management(in_features=SPJ2,out_layer=Final_Layer)
    arcpy.SelectLayerByAttribute_management(in_layer_or_view = Final_Layer,
                                            selection_type = 'NEW_SELECTION',
                                            where_clause = "Join_Count = 2")
    
    EventTable = CreateOutPath(MainFile=Output,appendix='EventTable',Extension='')
    arcpy.LocateFeaturesAlongRoutes_lr(
        in_features                = PntLayer, 
        in_routes                = SPJ, 
        route_id_field            = RouteID, 
        radius_or_tolerance        = Buffer, 
        out_table                = EventTable, 
        out_event_properties    = " ".join([RouteID, "POINT", "MP"]),
        route_locations            = "FIRST", 
        distance_field            = "DISTANCE", 
        in_fields                = "FIELDS", 
        m_direction_offsetting    = "M_DIRECTON"
        )

    SegTable = CreateOutPath(MainFile=Output,appendix='SegTable',Extension='')
    arcpy.CreateTable_management(out_path=os.path.dirname(SegTable),out_name=os.path.basename(SegTable))
    arcpy.AddField_management(SegTable,RouteID,'TEXT')
    arcpy.AddField_management(SegTable,'BEG_STA','DOUBLE')
    arcpy.AddField_management(SegTable,'END_STA','DOUBLE')
    arcpy.AddField_management(SegTable,'Address1','TEXT')
    arcpy.AddField_management(SegTable,'Address2','TEXT')
    #SegIDDict = {r.getValue('SegID'):{'INV':'','BMP':0,'EMP':0,'Add1':'','Add2':''}}
    SegIDDict = {}
    for r in arcpy.SearchCursor(EventTable):
        k = r.getValue('SegID')
        if k in SegIDDict.keys():
            mp = r.getValue('MP')
            add = r.getValue('Address')
            if SegIDDict[k]['BMP']<=mp:
                SegIDDict[k]['EMP'] = mp
                SegIDDict[k]['Add2'] = add
            else:
                SegIDDict[k]['EMP'] = SegIDDict[k]['BMP']
                SegIDDict[k]['BMP'] = mp
                SegIDDict[k]['Add2'] = SegIDDict[k]['Add1']
                SegIDDict[k]['Add1'] = add
        else:
            SegIDDict.update({r.getValue('SegID'):{'INV':r.getValue(RouteID),
                                                   'BMP':r.getValue('MP'),
                                                   'EMP':-1,
                                                   'Add1':r.getValue('Address'),
                                                   'Add2':''}})
            print('End point was not found')
    IC = arcpy.InsertCursor(SegTable)
    for k in SegIDDict.keys():
        r = IC.newRow()
        r.setValue(RouteID,SegIDDict[k]['INV'])
        r.setValue('BEG_STA',SegIDDict[k]['BMP'])
        r.setValue('END_STA',SegIDDict[k]['EMP'])
        r.setValue('Address1',SegIDDict[k]['Add1'])
        r.setValue('Address2',SegIDDict[k]['Add2'])
        IC.insertRow(r)
    del IC

    Overlay_Event_Layer = CreateOutLayer('OverlayEventLayer')
    arcpy.MakeRouteEventLayer_lr(in_routes = SegInput, 
                                 route_id_field = RouteID, 
                                 in_table = SegTable, 
                                 in_event_properties = ' '.join([RouteID,'LINE','BEG_STA','END_STA']), 
                                 out_layer = Overlay_Event_Layer, 
                                 offset_field = "", 
                                 add_error_field = "ERROR_FIELD") 
    
    Sort = CreateOutPath(MainFile=Output,appendix='sort',Extension='')
    arcpy.Sort_management(in_dataset = Overlay_Event_Layer,
                          out_dataset = Sort,
                          sort_field = ';'.join([RouteID,'BEG_STA','END_STA']))
    Final_Layer = CreateOutLayer('FinalLayer')
    
    arcpy.MakeFeatureLayer_management(in_features=Sort,out_layer=Final_Layer)
    arcpy.SelectLayerByAttribute_management(in_layer_or_view = Final_Layer,
                                            selection_type = 'NEW_SELECTION',
                                            where_clause = "Shape_Length > 0")
    arcpy.Delete_management(Output)
    arcpy.CopyFeatures_management(in_features=Final_Layer,out_feature_class=Output)

    arcpy.Delete_management(PntLayer)
    arcpy.Delete_management(SPJ)
    arcpy.Delete_management(SPJ2)
    arcpy.Delete_management(EventTable)
    arcpy.Delete_management(SegTable)
    arcpy.Delete_management(Overlay_Event_Layer)
    arcpy.Delete_management(Sort)
    arcpy.Delete_management(Final_Layer)
    arcpy.Delete_management(UnSplt)
def AttributeTabletoDF(FC):
    f = os.path.basename(FC)
    ExOut = CreateOutPath(os.path.join(os.getcwd(),f +'_' + strftime("%Y%m%d%H%M%S")) + str(np.random.normal()),'Out','xls')

    arcpy.TableToExcel_conversion(FC,ExOut)
    DF = pd.read_excel(ExOut)
    arcpy.Delete_management(ExOut)
    return(DF)
def FieldSummary_temporal(InputDict,Field):
    HSMPY_PATH = r'C:\Users\MR068144\Downloads\Python Scripts'
    
    sys.path.append(HSMPY_PATH)
    
    SubProcess = []
    PyList = []
    keylist = InputDict.keys()
    keylist.sort()
    for key in keylist:
        Output = os.path.join(os.path.dirname(InputDict[keylist[0]]) , 'FST_' + str(key) + '.csv')
        pyFN = os.path.join(os.path.dirname(InputDict[keylist[0]]) , 'FST_' + str(key) + '.py')
        OutFile = open(pyFN, 'w')
        pyfile = """try:
    from time import gmtime, strftime
    print(strftime("%Y-%m-%d %H:%M:%S"))
    import os, sys
    import pandas as pd
    import arcpy
    sys.path.append(r'{}') #1
    import hsmpy
    Input = r"{}"
    Field = "{}"
    key = "{}"
    Output = r"{}"
    print(Input)
    print(Field)
    s = pd.Series([r.getValue(Field) for r in arcpy.SearchCursor(Input)])
    df1 = pd.DataFrame(s.value_counts())
    df1.columns = [key]
    df1['key'] = df1.index
    df1.to_csv(Output)
    print(strftime("%Y-%m-%d %H:%M:%S"))
except Exception as e:
    print e
    raw_input('Press Enter to continue...')
""".format(HSMPY_PATH,InputDict[key],Field,key,Output)
        OutFile.write(pyfile)
        OutFile.close()
        PyList.append(pyFN)
    for py in PyList:
        SubProcess.append(subprocess.Popen(
                [sys.executable, py],
                shell=False,creationflags = subprocess.CREATE_NEW_CONSOLE))  
    w = [p.wait() for p in SubProcess]
    df = pd.DataFrame()
    for key in keylist:
        Output = os.path.join(os.path.dirname(InputDict[keylist[0]]) , 'FST_' + str(key) + '.csv')
        df1 = pd.read_csv(Output)
        df1 = pd.DataFrame(index = df1['key'].values,data=df1[str(key)].values,columns=[key])
        df = pd.concat([df, df1], axis=1)

    for key in keylist:
        Output = os.path.join(os.path.dirname(InputDict[keylist[0]]) , 'FST_' + str(key) + '.csv')
        pyFN = os.path.join(os.path.dirname(InputDict[keylist[0]]) , 'FST_' + str(key) + '.py')
        try:os.remove(Output)
        except:pass
        try:os.remove(pyFN)
        except:pass
    df = df.sort_index()
    #df.plot(title=Field,grid=True,rot=90)
    return(df)
def ListFCinGDBorMDB(DB):
    #print('List of datasets in the {}:\n'.format(DB))
    return([datasets for root, dirs, datasets in arcpy.da.Walk(DB)][0])
def ConvertMDBtoGDB(mdb,gdb):
    tables = []
    featurs = []
    FCs = ListFCinGDBorMDB(mdb)
    #print(FCs)
    for fc in FCs:
        ft = arcpy.Describe(mdb+'\\'+fc).dataElementType
        #print(ft)
        if ft=='DEFeatureClass':
            featurs.append(mdb + '\\' + fc)
        if ft=='DETable':
            tables.append(mdb + '\\' + fc)
    if os.path.exists(gdb):
        try:
            shutil.rmtree(gdb)
        except Exception, e:
            print(e)
            pass
    arcpy.CreateFileGDB_management(os.path.dirname(gdb),os.path.basename(mdb).split('.')[0])
    if len(featurs)>0:
        arcpy.FeatureClassToGeodatabase_conversion(featurs,gdb)
    if len(tables)>0:
        arcpy.TableToGeodatabase_conversion (tables, gdb)
    outL = featurs
    outL.extend(tables)
    return(outL)
def CON_ConvertMDBtoGDB(WDir,HSMPY_PATH,mdb,gdb):
    sys.path.append(HSMPY_PATH)
    Title = os.path.basename(mdb).split('.')[0]
    pyFN = os.path.join(WDir , 'MDB2GDB_' + Title + '.py')
    OutFile = open(pyFN, 'w')
    pyfile = """from time import gmtime, strftime
print(strftime("%Y-%m-%d %H:%M:%S"))
print("MDB to GDB")
import os, sys
import atexit
#atexit.register(raw_input, 'Press Enter to continue...')
HSMPY_PATH = r'{}'
mdb = r'{}'
gdb = r'{}'
sys.path.append(HSMPY_PATH) 
import hsmpy
import arcpy
print(gdb)
Out = hsmpy.common.ConvertMDBtoGDB(mdb,gdb)
print(Out)
print(strftime("%Y-%m-%d %H:%M:%S"))
""".format(HSMPY_PATH,mdb,gdb)
    OutFile.write(pyfile)
    OutFile.close()
    SW_MINIMIZE = 6
    SW_HIDE = 0
    info = subprocess.STARTUPINFO()
    info.dwFlags = subprocess.STARTF_USESHOWWINDOW
    info.wShowWindow = SW_MINIMIZE
    SP = subprocess.Popen(
                [sys.executable, pyFN])
    return(SP)
def WaitIfNecessary(Processes,MaxOpenProcesses,Frequency = 2):
    Poll = [p['Process'].poll() for p in Processes if p['Process'].poll() is None]
    while len(Poll)>=MaxOpenProcesses:
        time.sleep(Frequency)
        Poll = [p['Process'].poll() for p in Processes if p['Process'].poll() is None]
    for p in Processes:
        status = p['Process'].poll()
        p['LastStatus'] = status
        if status is not None and not p['Printed']:
            print('Title: {}: {}'.format(p['Title'],status))
            p['Printed'] = True
    return(Processes)
