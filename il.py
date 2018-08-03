#HSMPY2
import math
from datetime import datetime
import pandas as pd
import arcpy
import os
import common
import sys, csv, json, subprocess
import numpy as np

class domains(object):
    ACC_CNTL = {'name':'ACC_CNTL'   ,'alias':'Access Control'               ,'type':'SHORT','codes':{0:'Uncontrolled',
                1:'Partial control',
                2:'Full control'}}
    BLT = {'name':'BLT'   ,'alias':'Built By'               ,'type':'TEXT','codes':{
        0:'Unknown',
        1:'State',
        2:'City, town or village by agreement with State',
        3:'State and county',
        4:'County',
        5:'Township or road district',
        6:'City, town or village',
        7:'Park district or State Division of Parks and Memorials',
        8:'Other governmental unit',
        9:'Private',
        'X':'Proposed or designated roads',
        'A':'Joint-county and city'}}
    COUNTY = {'name':'COUNTY'   ,'alias':'County'               ,'type':'SHORT','codes':{
        1:'Adams',
        2:'Alexander',
        3:'Bond',
        4:'Boone',
        5:'Brown',
        6:'Bureau',
        7:'Calhoun',
        8:'Carroll',
        9:'Cass',
        10:'Champaign',
        11:'Christian',
        12:'Clark',
        13:'Clay',
        14:'Clinton',
        15:'Coles',
        16:'Cook',
        17:'Crawford',
        18:'Cumberland',
        19:'DeKalb',
        20:'DeWitt',
        21:'Douglas',
        22:'DuPage',
        23:'Edgar',
        24:'Edwards',
        25:'Effingham',
        26:'Fayette',
        27:'Ford',
        28:'Franklin',
        29:'Fulton',
        30:'Gallatin',
        31:'Greene',
        32:'Grundy',
        33:'Hamilton',
        34:'Hancock',
        35:'Hardin',
        36:'Henderson',
        37:'Henry',
        38:'Iroquois',
        39:'Jackson',
        40:'Jasper',
        41:'Jefferson',
        42:'Jersey',
        43:'JoDaviess',
        44:'Johnson',
        45:'Kane',
        46:'Kankakee',
        47:'Kendall',
        48:'Knox',
        49:'Lake',
        50:'LaSalle',
        51:'Lawrence',
        52:'Lee',
        53:'Livingston',
        54:'Logan',
        55:'McDonough',
        56:'McHenry',
        57:'McLean',
        58:'Macon',
        59:'Macoupin',
        60:'Madison',
        61:'Marion',
        62:'Marshall',
        63:'Mason',
        64:'Massac',
        65:'Menard',
        66:'Mercer',
        67:'Monroe',
        68:'Montgomery',
        69:'Morgan',
        70:'Moultrie',
        71:'Ogle',
        72:'Peoria',
        73:'Perry',
        74:'Piatt',
        75:'Pike',
        76:'Pope',
        77:'Pulaski',
        78:'Putnam',
        79:'Randolph',
        80:'Richland',
        81:'Rock Island',
        82:'St. Clair',
        83:'Saline',
        84:'Sangamon',
        85:'Schuyler',
        86:'Scott',
        87:'Shelby',
        88:'Stark',
        89:'Stephenson',
        90:'Tazewell',
        91:'Union',
        92:'Vermilion',
        93:'Wabash',
        94:'Warren',
        95:'Washington',
        96:'Wayne',
        97:'White',
        98:'Whiteside',
        99:'Will',
        100:'Williamson',
        101:'Winnebago',
        102:'Woodford'}}
    CRS = 'Condition Rating Survey'
def IsNan(value):
            try:
                if math.isnan(value):
                    return(True)
            except:
                pass
            try:
                if value == 'nan':
                    return(True)
            except:
                pass
            try:
                if value == None:
                    return(True)
            except:
                pass
            return(False)
def ConvertHSIP(value,Type):
        def TryDateFormat(value,Format):
            try:
                value = str(value)
                return(datetime.strptime(value,Format))
            except:
                return(False)
        if Type == 'currency':
            if IsNan(value):
                return(0)
            try:
                value = str(value)
                #value = value.split('.')[0]
                return(float(value.replace('$','').replace(' ','').replace(',','').replace('-','0')))
            except:
                #print(Type,value)
                return(0)
        if Type == 'date':
            if IsNan(value):
                return(None)
            value = str(value)
            value = value.lstrip()
            value = value.split(',')[0]
            Res = False
            for Format in ['%m/%d/%Y','%m/%d/%Y %H:%M','%Y','%Y-%m-%d %H:%M:%S']:
                Res = TryDateFormat(value,Format)
                if not not Res:
                    return(Res)
            #print(Type,value)
            return(None)
        if Type == 'bool':
            if IsNan(value):
                return(None)
            value = str(value)
            value = value.rstrip()
            value = value.lstrip()
            value = str(value).lower()
            if value in ['false','no','n','0.0']:
                return(False)
            if value in ['true','yes','1.0']:
                return(True)
            #print(Type,value)
            return(None)
        if Type == 'float':
            if IsNan(value):
                return(0)
            try:
                return(float(value))
            except:
                #print(Type,value)
                return(0)
        if Type == 'int':
            if IsNan(value):
                return(0)
            try:
                return(int(value))
            except:
                #print(Type,value)
                return(0)
        if Type == 'district':
            if IsNan(value):
                return(None)
            try:
                return(int(value[-1]))
            except:
                #print(Type,value)
                return(None)
        return(value)
def ReadHSIPData(ExcelFile,Years):
    df = pd.read_excel(ExcelFile)

    FDict = {c:{'type':'String'} for c in list(df.columns)}

    FDict['District'].update({'type':'district'})
    FDict['County'  ].update({'type':'county'})

    for field in ['Cost Est','Is Intersection','Is Segment','Is Local Project','Systematic Improvements']:
        FDict[field].update({'type':'bool'})

    for field in ['Length','Mile Station From','Mile Station To','Length NA','Total Length of Rtes.',
                  'Latitude','Longitude','Benefit Cost Ratio']:
        FDict[field].update({'type':'float'})

    for field in ['Lanes','SpeedLimit','AADTIntersection','AADTSegment','Fiscal Year','HSIP ID']:
        FDict[field].update({'type':'int'})
    
    for field in ['Estimated Project Cost','Requested HSIP Funding Amount','ApprovedAmt','FundBseAmt','FundHrrrAmt',
                  'FundHsipAmt','FundLocalAmt','Total Award Amount','HSIP AWARD AMOUNT']:
        FDict[field].update({'type':'currency'})

    for field in ['Targeted Letting Date','Letting Date','Award Date','Central HSIP Approval Date','Created','Date Submitted',
                  'Modified','Completion Date']:
        FDict[field].update({'type':'date'})

    NDF = pd.DataFrame()
    for c in list(df.columns):
        NDF[c] = [ConvertHSIP(i,FDict[c]['type']) for i in list(df[c])]
    HSIP_DF = NDF
    HSIP_DF = HSIP_DF.drop_duplicates(keep='first')
    droplist = []
    for i,r in HSIP_DF.iterrows():
        if not r['HSIP ID']>200000000:
            droplist.append(i)
    HSIP_DF = HSIP_DF.drop(droplist)
    HSIP_DF = HSIP_DF.sort_values(by = ['HSIP ID','Central HSIP Approval Date'])
    HSIP_DF = HSIP_DF.drop_duplicates(subset = ['HSIP ID'], keep='first')
    BeforePeriod = []
    AfterPeriod  = []
    ConstPeriod  = []
    for i,hsip in HSIP_DF.iterrows():
        if hsip['Letting Date'].year>2003 and hsip['Letting Date'].year<2017 and hsip['Completion Date'].year>2003 and hsip['Completion Date'].year<2017:
            BeforePeriod.append(';'.join([str(y) for y in Years if y<hsip['Letting Date'].year]))
            AfterPeriod.append (';'.join([str(y) for y in Years if y>hsip['Completion Date'].year]))
            ConstPeriod.append (';'.join([str(y) for y in Years if y>=hsip['Letting Date'].year and y<=hsip['Completion Date'].year]))
        else:
            BeforePeriod.append('')
            AfterPeriod.append('')
            ConstPeriod.append('')
    HSIP_DF['BeforePeriod'] = BeforePeriod
    HSIP_DF['AfterPeriod'] = AfterPeriod
    HSIP_DF['ConstPeriod'] = ConstPeriod
    HSIP_DF.index = HSIP_DF['HSIP ID']
    return(HSIP_DF)
def ReadHSIPData_csv(CSVFile):
    df = pd.read_csv(CSVFile)

    FDict = {c:{'type':'String'} for c in list(df.columns)}

    FDict['District'].update({'type':'district'})
    FDict['County'  ].update({'type':'county'})

    for field in ['CostEst','IntersectionIncl','SegmentIncl','IsLocalProject','SystematicImprovements']:
        if field in FDict.keys():
            FDict[field].update({'type':'bool'})

    for field in ['Length','Mile Station From','Mile Station To','Length NA','Total Length of Rtes.',
                  'Latitude','Longitude','BenefitCostRatio']:
        if field in FDict.keys():
            FDict[field].update({'type':'float'})

    for field in ['Lanes','SpeedLimit','AADTIntersection','AADTSegment','FiscalYear','HSIPID']:
        if field in FDict.keys():
            FDict[field].update({'type':'int'})
    
    for field in ['EstimatedProjectCost','RequestedHSIPFundingAmount','ApprovedAmt','FundBseAmt','FundHrrrAmt',
                  'FundHsipAmt','FundLocalAmt','TotalAwardAmount','HSIPAWARDAMOUNT']:
        if field in FDict.keys():
            FDict[field].update({'type':'currency'})

    for field in ['TargetedLettingDate','LettingDate','AwardDate','CentralHSIPApprovalDate','Created','DateSubmitted',
                  'Modified','CompletionDate']:
        if field in FDict.keys():
            FDict[field].update({'type':'date'})
    String = ['AllSelectedImprovements','']
    NDF = pd.DataFrame()
    for c in list(df.columns):
        NDF[c] = [ConvertHSIP(i,FDict[c]['type']) for i in list(df[c])]
    return(NDF)


def FindPG_Old():
    IRIS = r'C:\Users\mr068144\Downloads\IRIS\HWY2015_CH2M_Editions.mdb\HWY2015_CH2M_20180213'
    arcpy.AddField_management(IRIS,'PGMahdi','TEXT')
    for year in [2015]:
        #IRIS = os.path.join(IRISPath,'HWY'+str(year)+'.shp')
        PGDict = {}
        uc = arcpy.UpdateCursor(IRIS)
        for r in uc:
            OID = r.getValue('OBJECTID')
            JUR_TYPE   = r.getValue('JUR_TYPE')
            FUNC_CLASS     = r.getValue('FUNC_CLASS')
            URBAN      = r.getValue('URBAN')
            KEY_RT_TYP = r.getValue('KEY_RT_TYP')
            LANES        = r.getValue('LANES')
            LNS        = r.getValue('LNS')
            KEY_RT_APP = r.getValue('KEY_RT_APP')
            OP_1_2_WAY = r.getValue('OP_1_2_WAY')
            MED_TYP    = r.getValue('MED_TYP')
            MARKED_RT  = r.getValue('MARKED_RT')
            MARKED_RT2  = r.getValue('MARKED_RT2')
            MARKED_RT3  = r.getValue('MARKED_RT3')
            MARKED_RT4  = r.getValue('MARKED_RT4')
            FC         = FUNC_CLASS
            if JUR_TYPE in ['1','7']:
                PG = []
                if FUNC_CLASS != '1' and LANES == 2 and URBAN == '0000' and JUR_TYPE == '1' and KEY_RT_APP != '7' and KEY_RT_APP != '4':
                    PG.append(1)
                if FUNC_CLASS >= '3' and LANES > 2 and URBAN == '0000' and JUR_TYPE == '1' and MED_TYP == 0 and KEY_RT_APP != '7' and KEY_RT_APP != '4':
                    PG.append(2)
                if FUNC_CLASS >= '3' and LANES > 2 and URBAN == '0000' and JUR_TYPE == '1' and MED_TYP != 0 and KEY_RT_APP != '7' and KEY_RT_APP != '4':
                    PG.append(3)
                if FUNC_CLASS <= '2' and (LANES == 3 or LANES == 4) and URBAN == '0000' and JUR_TYPE == '1' and KEY_RT_APP != '4' and KEY_RT_APP != '7':
                    PG.append(4)
                if FUNC_CLASS <= '2' and URBAN == '0000' and LANES >= 6 and JUR_TYPE == '1' and KEY_RT_APP != '4' and KEY_RT_APP != '7':
                    PG.append(5)
                if (FUNC_CLASS <= '4' or FUNC_CLASS == '7') and LANES <= 2 and URBAN != '0000' and OP_1_2_WAY == '2' and JUR_TYPE == '1' and KEY_RT_APP != '4' and KEY_RT_APP != '7':
                    PG.append(6)
                if (FUNC_CLASS <= '4' or FUNC_CLASS == '7') and URBAN != '0000' and OP_1_2_WAY == '1' and JUR_TYPE == '1' and KEY_RT_APP != '4' and KEY_RT_APP != '7':
                    PG.append(7)
                if (FUNC_CLASS == '3' or FUNC_CLASS == '4' or FUNC_CLASS == '7') and LANES > 2 and MED_TYP == 0 and URBAN != '0000' and OP_1_2_WAY == '2' and JUR_TYPE == '1' and KEY_RT_APP != '4' and KEY_RT_APP != '7':
                    PG.append(8)
                if (FUNC_CLASS == '3' or FUNC_CLASS == '4' or FUNC_CLASS == '7') and LANES > 2 and MED_TYP != 0 and URBAN != '0000' and OP_1_2_WAY == '2' and JUR_TYPE == '1' and KEY_RT_APP != '4' and KEY_RT_APP != '7':
                    PG.append(9)
                if FUNC_CLASS <= '2' and URBAN != '0000' and (LANES == 3 or LANES == 4) and OP_1_2_WAY == '2' and JUR_TYPE == '1' and KEY_RT_APP != '4' and KEY_RT_APP != '7':
                    PG.append(10)
                if FUNC_CLASS <= '2' and URBAN != '0000' and (LANES == 5 or LANES == 6) and OP_1_2_WAY == '2' and JUR_TYPE == '1' and KEY_RT_APP != '4' and KEY_RT_APP != '7':
                    PG.append(11)
                if FC <= '20' and LNS >= 7 and URBAN != '0000' and JUR_TYPE == '1' and OP_1_2_WAY == '2' and KEY_RT_APP != '4' and KEY_RT_APP != '7':
                    PG.append(12)
                if JUR_TYPE == '7' and KEY_RT_APP != '4' and KEY_RT_APP != '7':
                    PG.append(13)
                if (JUR_TYPE == '1' or JUR_TYPE == '7') and (KEY_RT_APP == '4' or KEY_RT_APP == '7'):
                    PG.append(14)
                if PG==[]:
                    PG.append(15)
                PG = ['S' + str(i) for i in PG]
            else:
                PG = []
                if LANES == 2 and URBAN == '0000' and KEY_RT_APP != '4' and KEY_RT_APP != '7' and OP_1_2_WAY == '2' and MARKED_RT =='' and MARKED_RT2 == '' and MARKED_RT3 == '' and MARKED_RT4 == '':
                    PG.append(1)
                if URBAN != '0000' and KEY_RT_APP != '4' and KEY_RT_APP != '7' and OP_1_2_WAY == '1':
                    PG.append(2)
                if LANES <= 2 and URBAN != '0000' and KEY_RT_APP != '4' and KEY_RT_APP != '7' and OP_1_2_WAY == '2' and MARKED_RT =='' and MARKED_RT2 == '' and MARKED_RT3 == '' and MARKED_RT4 == '':
                    PG.append(3)
                if LANES > 2 and MED_TYP == 0 and URBAN != '0000' and OP_1_2_WAY == '2' and KEY_RT_APP != '4' and KEY_RT_APP != '7':
                    PG.append(4)
                if LANES > 2 and MED_TYP != 0 and URBAN != '0000' and OP_1_2_WAY == '2' and KEY_RT_APP != '4' and KEY_RT_APP != '7':
                    PG.append(5)
                if PG == []:
                    PG.append(6)
                PG = ['L' + str(i) for i in PG]
            PGDict.update({OID:PG})
            r.setValue('PGMahdi',PGConv[PG[0]])
            uc.updateRow(r)
    del uc,r
def FindPG(JUR_TYPE,URBAN,KEY_RT_APP,FCNAME,LNS,MED_TYP,OP_1_2_WAY):
    JUR_TYPE = int(JUR_TYPE)
    URBAN = str(URBAN)
    KEY_RT_APP = int(KEY_RT_APP)
    FCNAME = str(FCNAME)
    LNS = int(LNS)
    MED_TYP = int(MED_TYP)
    OP_1_2_WAY = int(OP_1_2_WAY)
    
    if JUR_TYPE in [1]:
        s1 = 'State'
    elif JUR_TYPE in [7]:
        s1 = 'Private'
    else:
        s1 = 'Local'
        
    if URBAN == '0000':
        s2 = 'Rural'
    else:
        s2 = 'Urban'
        
    if FCNAME in ['Interstate','Freeway and Expressway','Freeway and Expressway (Urban)']:
        s3 = 'Freeway'
    else:
        s3 = 'non-Freeway'
    
    if MED_TYP in [0]:
        s4 = 'undivided'
    else:
        s4 = 'divided'
    
    if KEY_RT_APP in [4,7]:
        s5 = 'RampCD'
    else:
        s5 = 'nonRampCD'
    
    if OP_1_2_WAY == 1:
        s6 = 'oneway'
    else:
        s6 = 'twoway'
    
    PG = 0
    if s1 == 'State':
        if s5 == 'nonRampCD':
            if s2 == 'Rural':
                if s3 == 'non-Freeway':
                    if LNS == 2:
                        PG = 'S1'
                    if LNS>2:
                        if s4 == 'undivided':
                            PG = 'S2'
                        else:
                            PG = 'S3'
                else: #Freeway
                    if LNS in [3,4]:
                        PG = 'S4'
                    if LNS>5:
                        PG = 'S5'
            else: #Urban
                if s6=='oneway':
                    PG = 'S7'
                else: #Twoway
                    if s3 == 'non-Freeway':
                        if LNS==2:
                            PG = 'S6'
                        if LNS>2:
                            if s4 == 'undivided':
                                PG = 'S8'
                            else:
                                PG = 'S9'
                    else: #Freeway
                        if LNS in [3,4]:
                            PG = 'S10'
                        if LNS in [5,6]:
                            PG = 'S11'
                        if LNS>=7:
                            PG = 'S12'
        else: #RampCD
            PG = 'S14'
    if s1 == 'Private':
        if s5 == 'nonRampCD':
            PG = 'S13'
        else: #RampCD
            PG = 'S14'
    if s1 in ['State','Private'] and PG == 0:
        PG = 'S15'
    if s1 == 'Local':
        if s5 == 'nonRampCD':
            if s2 == 'Rural':
                if LNS == 2 and s6 == 'twoway':
                    PG = 'L1'
            else: #Urban
                if s6 == 'oneway':
                    PG = 'L2'
                else: #twoway
                    if LNS <= 2:
                        PG = 'L3'
                    else:
                        if s4 == 'undivided':
                            PG = 'L4'
                        else:
                            PG = 'L5'
        if PG == 0:
            PG = 'L6'
    return(PG)
def AddBaseData(FCList,Years,IRIS_route,IRIS_table,Intersections,OutputDir,Distance="0.5 Miles"):
    def SelectionType(NewSelection):
        if NewSelection:
            return("NEW_SELECTION")
        else:
            return("ADD_TO_SELECTION")
    for year in Years:
        #RteFN = os.path.basename(IRIS_route[year]).split('.')[0]
        #IntFN = os.path.basename(Intersections[year]).split('.')[0]
        #TabFN = os.path.basename(IRIS_table[year]).split('.')[0]
        RteFN = 'HWY' + str(year) + '_route'
        IntFN = 'HWY' + str(year) + '_inter'
        TabFN = 'HWY' + str(year) + '_table'
        IRISRoute = common.CreateOutLayer('IRISRoute')
        IRISInter = common.CreateOutLayer('IRISInter')
        arcpy.MakeFeatureLayer_management(IRIS_route[year],IRISRoute)
        arcpy.MakeFeatureLayer_management(Intersections[year],IRISInter)
        Flag = True
        for FC in FCList:
            if int(str(arcpy.GetCount_management(FC)))>0:
                arcpy.SelectLayerByLocation_management(in_layer=IRISRoute, 
                                               overlap_type="WITHIN_A_DISTANCE", 
                                               select_features=FC, 
                                               search_distance=Distance, 
                                               selection_type=SelectionType(Flag), 
                                               invert_spatial_relationship="NOT_INVERT")
                arcpy.SelectLayerByLocation_management(in_layer=IRISInter, 
                                               overlap_type="WITHIN_A_DISTANCE", 
                                               select_features=FC, 
                                               search_distance=Distance, 
                                               selection_type=SelectionType(Flag), 
                                               invert_spatial_relationship="NOT_INVERT")
                Flag = False
        if not Flag:
            arcpy.Delete_management(os.path.join(OutputDir,RteFN))
            arcpy.FeatureClassToFeatureClass_conversion (IRISRoute, OutputDir, RteFN)
            arcpy.Delete_management(os.path.join(OutputDir,IntFN))
            arcpy.FeatureClassToFeatureClass_conversion (IRISInter, OutputDir, IntFN)
            INV = [r.getValue('INVENTORY') for r in arcpy.SearchCursor(os.path.join(OutputDir,RteFN))]
            arcpy.Delete_management(os.path.join(OutputDir,TabFN))
            #arcpy.TableToTable_conversion(in_rows=IRIS_table[year], 
            #                                out_path=OutputDir, 
            #                                out_name=TabFN,
            #                                where_clause = '"INVENTORY" IN (' + ','.join(["'" + str(inv) + "'" for inv in INV]) + ')')
            arcpy.TableToTable_conversion(in_rows=IRIS_table[year], 
                                            out_path=OutputDir, 
                                            out_name=TabFN,
                                            where_clause = '[INVENTORY] IN (' + ','.join(["'" + str(inv) + "'" for inv in INV]) + ')')
        print('Year: {},Routes: {}, Int: {}, RETable: {}'.format(year,
                                                                 int(str(arcpy.GetCount_management(os.path.join(OutputDir,RteFN)))),
                                                                 int(str(arcpy.GetCount_management(os.path.join(OutputDir,IntFN)))),
                                                                 int(str(arcpy.GetCount_management(os.path.join(OutputDir,TabFN))))
                                                                 ))
def CON_AddBaseData(WDir,HSMPY_PATH,FCList,Years,IRIS_route,IRIS_table,Intersections,OutputDir,Distance,Title):
    sys.path.append(HSMPY_PATH)

    pyFN = os.path.join(WDir , 'HSIP_' + str(Title) + '_AddBaseData.py')
    OutFile = open(pyFN, 'w')
    pyfile = """from time import gmtime, strftime
print(strftime("%Y-%m-%d %H:%M:%S"))
print("Add Base Data: " + "{}")
import os, sys
import atexit
#atexit.register(raw_input, 'Press Enter to continue...')
HSMPY_PATH = r'{}'
FCList = {}
Years = {}
IRIS_route = {}
IRIS_table = {}
Intersections = {}
OutputDir = r"{}"
Distance = "{}"
sys.path.append(HSMPY_PATH) 
import hsmpy
import arcpy
hsmpy.il.AddBaseData(FCList,Years,IRIS_route,IRIS_table,Intersections,OutputDir,Distance)
print(strftime("%Y-%m-%d %H:%M:%S"))
""".format(Title,HSMPY_PATH,FCList,Years,IRIS_route,IRIS_table,Intersections,OutputDir,Distance)
    OutFile.write(pyfile)
    OutFile.close()
    SW_MINIMIZE = 6
    SW_HIDE = 0
    info = subprocess.STARTUPINFO()
    info.dwFlags = subprocess.STARTF_USESHOWWINDOW
    info.wShowWindow = SW_MINIMIZE
    SubProcess = subprocess.Popen(
                [sys.executable, pyFN],
                shell=False,creationflags = subprocess.CREATE_NEW_CONSOLE)
    return(SubProcess)
def CON_CreateMDBforHSIP(WDir,HSMPY_PATH,Title,HSIP_Seg,HSIP_Int):
    sys.path.append(HSMPY_PATH)
    pyFN = os.path.join(WDir , 'HSIP_' + str(Title) + '_CreateMDB.py')
    OutFile = open(pyFN, 'w')
    pyfile = """from time import gmtime, strftime
print(strftime("%Y-%m-%d %H:%M:%S"))
Title = "{}"
print("Create MDB: " + Title)
import os, sys
import atexit
#atexit.register(raw_input, 'Press Enter to continue...')
WDir = r'{}'
HSMPY_PATH = r'{}'
HSIP_Seg = r'{}'
HSIP_Int = r'{}'
sys.path.append(HSMPY_PATH) 
import hsmpy
import arcpy

IntLayer = hsmpy.common.CreateOutLayer('IntLayer')
SegLayer = hsmpy.common.CreateOutLayer('SegLayer')
arcpy.MakeFeatureLayer_management(HSIP_Seg,SegLayer)
arcpy.MakeFeatureLayer_management(HSIP_Int,IntLayer)
arcpy.env.outputMFlag = "Enabled"
arcpy.env.outputZFlag = "Enabled"
p = str(Title)
FN = 'HSIP_' + p + '_GIS.mdb'
MDB = os.path.join(WDir,FN)
try: os.remove(MDB)
except: pass
try: arcpy.CreatePersonalGDB_management(out_folder_path=WDir,out_name=FN)
except: pass   
arcpy.SelectLayerByAttribute_management(IntLayer,'NEW_SELECTION','"HSIP_ID" = ' +  p )
arcpy.SelectLayerByAttribute_management(SegLayer,'NEW_SELECTION','"HSIP_ID" = ' +  p )
   
SegFC = MDB + '\\Seg_' + p
IntFC = MDB + '\\Int_' + p
arcpy.Delete_management(SegFC)
arcpy.Delete_management(IntFC)
arcpy.FeatureClassToFeatureClass_conversion (SegLayer, MDB, os.path.basename(SegFC))
arcpy.FeatureClassToFeatureClass_conversion (IntLayer, MDB, os.path.basename(IntFC))
print('Total Segments: ' + arcpy.GetCount_management(SegFC)[0])
print('Total Int: ' + arcpy.GetCount_management(IntFC)[0]) 
print(strftime("%Y-%m-%d %H:%M:%S"))
""".format(Title,WDir,HSMPY_PATH,HSIP_Seg,HSIP_Int)
    OutFile.write(pyfile)
    OutFile.close()
    SubProcess = subprocess.Popen(
                [sys.executable, pyFN],
                shell=False,creationflags = subprocess.CREATE_NEW_CONSOLE)
    return(SubProcess)
def CON_Seg_PC_HSIP(WDir,HSMPY_PATH,MDB,Years,SPFPath,Title):
    sys.path.append(HSMPY_PATH)
    pyFN = os.path.join(WDir , 'HSIP_' + str(Title) + '_SegPC.py')
    OutFile = open(pyFN, 'w')
    pyfile = """from time import gmtime, strftime
print(strftime("%Y-%m-%d %H:%M:%S"))
Title = "{}"
print("Add Predicted Crashes: " + Title)
import os, sys
import pandas as pd
import atexit
#atexit.register(raw_input, 'Press Enter to continue...')
HSMPY_PATH = r'{}'
MDB = r'{}'
Years = {}
SPFPath = r'{}'
sys.path.append(HSMPY_PATH) 
import hsmpy
import numpy as np
import arcpy
SPF_DF = pd.read_excel(SPFPath,sheetname='Summary')
SPF_DF['PGNumber'] = [int(s.split('PeerGroup ')[1][:2]) for s in SPF_DF.PG]
for year in Years:
    p = str(Title)
    SegFC = MDB + '\\Seg_' + p + '_' + str(year)
    IntFC = MDB + '\\Int_' + p + '_' + str(year) + '_points'
    NumSeg = 0
    NumInt = 0
    try: NumSeg = int(str(arcpy.GetCount_management(SegFC)))
    except: pass
    try: NumInt = int(str(arcpy.GetCount_management(IntFC)))
    except: pass
    if NumSeg > 0:
        try: hsmpy.il.AddRoadway_PC(SegFC,SPF_DF)
        except: pass
        try:
    	    print('Seg: ' + str(year) + ', K: ' + str(np.mean([r.getValue('K_EC') for r in arcpy.SearchCursor(SegFC)])) +
        	      ', A: ' + str(np.mean([r.getValue('A_EC') for r in arcpy.SearchCursor(SegFC)])) +
            	  ', B: ' + str(np.mean([r.getValue('B_EC') for r in arcpy.SearchCursor(SegFC)]))
    	    )
        except: pass
    if NumInt > 0:
        try: hsmpy.il.AddInt_PC(IntFC,SPF_DF)
        except: pass
        try:
    	    print('Int: ' + str(year) + ', K: ' + str(np.mean([r.getValue('K_EC') for r in arcpy.SearchCursor(IntFC)])) +
        	      ', A: ' + str(np.mean([r.getValue('A_EC') for r in arcpy.SearchCursor(IntFC)])) +
        	    ', B: ' + str(np.mean([r.getValue('B_EC') for r in arcpy.SearchCursor(IntFC)]))
    	    )
        except: pass
print(strftime("%Y-%m-%d %H:%M:%S"))
""".format(Title,HSMPY_PATH,MDB,Years,SPFPath)
    OutFile.write(pyfile)
    OutFile.close()
    SubProcess = subprocess.Popen(
                [sys.executable, pyFN],
                shell=False,creationflags = subprocess.CREATE_NEW_CONSOLE)
    return(SubProcess)

def AddRoadway_PC(FC,SPF_DF):
    arcpy.AddField_management(FC,'K_PC','Double')
    arcpy.AddField_management(FC,'A_PC','Double')
    arcpy.AddField_management(FC,'B_PC','Double')
    arcpy.AddField_management(FC,'K_k','Double')
    arcpy.AddField_management(FC,'A_k','Double')
    arcpy.AddField_management(FC,'B_k','Double')
    arcpy.AddField_management(FC,'K_EC','Double')
    arcpy.AddField_management(FC,'A_EC','Double')
    arcpy.AddField_management(FC,'B_EC','Double')
    uc = arcpy.UpdateCursor(FC)
    for r in uc:
        PG = r.getValue('PG')
        pg_j = {'S':'State','L':"Local"}[PG[:1]]
        pg_n = int(PG[1:])
        aadt = r.getValue('AADT')
        l = r.getValue('Shape').length/5280
        for sev in ['K','A','B']:
            pc = PredictedCrash(SPF_DF,Severity = sev,Type='Roadway',Jur=pg_j,PG = pg_n,L = l,AADT = aadt)
            oc = r.getValue(sev+'_OC')
            r.setValue(sev+'_PC',pc['Pred'])
            r.setValue(sev+'_k',pc['k'])
            r.setValue(sev+'_EC',ExpectedCrash(pc['Pred'],pc['k'],oc))
        uc.updateRow(r)
def AddInt_PC(FC,SPF_DF):
    arcpy.AddField_management(FC,'K_PC','Double')
    arcpy.AddField_management(FC,'A_PC','Double')
    arcpy.AddField_management(FC,'B_PC','Double')
    arcpy.AddField_management(FC,'K_k','Double')
    arcpy.AddField_management(FC,'A_k','Double')
    arcpy.AddField_management(FC,'B_k','Double')
    arcpy.AddField_management(FC,'K_EC','Double')
    arcpy.AddField_management(FC,'A_EC','Double')
    arcpy.AddField_management(FC,'B_EC','Double')
    uc = arcpy.UpdateCursor(FC)
    for r in uc:
        PG = r.getValue('PeerGroup_CH2M_TJM')
        pg_j = {'S':'State','L':"Local"}[PG[:1]]
        pg_n = int(PG[-2:])
        aadt_major = r.getValue('AADT_Major')
        aadt_minor = r.getValue('AADT_Minor')
        for sev in ['K','A','B']:
            pc = PredictedCrash(SPF_DF,Severity = sev,Type='Intersection',Jur=pg_j,PG = pg_n,AADT_Major = aadt_major,AADT_Minor = aadt_minor)
            r.setValue(sev+'_PC',pc['Pred'])
            r.setValue(sev+'_k',pc['k'])
            oc = r.getValue(sev+'_OC')
            r.setValue(sev+'_EC',ExpectedCrash(pc['Pred'],pc['k'],oc))
        uc.updateRow(r)
def PredictedCrash(SPF_DF,Severity = 'K',Type='Roadway',Jur='State',PG = 1,L = 0,AADT = 0,AADT_Major = 0,AADT_Minor = 0):
    df = SPF_DF[(SPF_DF.Type==Type) & (SPF_DF.State==Jur) & (SPF_DF.Severity == Severity) & (SPF_DF.PGNumber == PG)]
    #if len(df) != 1:
    #    print(Severity,Type,Jur,PG)
    Npred = 0
    k = 0
    if len(df)==1 and (AADT>0 or (AADT_Major>0 and AADT_Minor>0)):
        if Jur == 'State':
            if Type == 'Roadway':
                Npred = L * math.exp(df.a.item()) * AADT ** df.b.item()
                k = df.k.item() / L
            else:
                Npred = math.exp(df.a.item()) * AADT_Major ** df.b.item() * AADT_Minor ** df.c.item()
                k = df.k.item()
        else:
            if Type == 'Roadway':
                Npred = L * math.exp(df.a.item()) * AADT ** df.b.item() /(1 + math.exp(df.c.item() + AADT * df.d.item()))
                k = df.k.item() / L
            else:
                Npred = math.exp(df.a.item()) * AADT_Major ** df.b.item() * AADT_Minor ** df.c.item() / (1 + math.exp(df.d.item() + AADT_Major * df.e.item() + AADT_Minor * df.f.item()))
                k = df.k.item()
    return({'Pred': Npred,'k':k})
def ExpectedCrash(PC,k,OC):
    w = 1.0/(1+k*PC)
    EC = PC*w + OC*(1-w)
    return(EC)

def HSIP_SummarySheet(HSIP_DF,p,MDB,ExcelOut,Years,Fields):
    CrashCost = {'K':6245736 ,'A':336521 ,'B':123079 ,'C':69953 ,'PDO':11529 }
    CurYear = 2018
    Interest = 0.02
    TrafficGrowth = 0.01
    if not(len(HSIP_DF[HSIP_DF['HSIP ID'] ==  int(p)]['BeforePeriod'].item())>0 and len(HSIP_DF[HSIP_DF['HSIP ID'] ==  int(p)]['AfterPeriod'].item())>0):
        print('{}: Before-After Periods are not defined'.format(p))
    p = str(p)
    #FN = 'HSIP_' + p + '_GIS.mdb'
    #MDB = os.path.join(AnalysisDir,FN)
    SegFC = MDB + '\\Seg_' + p
    IntFC = MDB + '\\Int_' + p
    FN = ExcelOut
    try: os.remove(FN)
    except: pass
    writer = pd.ExcelWriter(FN, engine = 'openpyxl')
    
    BeforePeriod = [int(y) for y in HSIP_DF[HSIP_DF['HSIP ID'] ==  int(p)]['BeforePeriod'].item().split(';')]
    ConstPeriod  = [int(y) for y in HSIP_DF[HSIP_DF['HSIP ID'] ==  int(p)]['ConstPeriod' ].item().split(';')]
    AfterPeriod  = [int(y) for y in HSIP_DF[HSIP_DF['HSIP ID'] ==  int(p)]['AfterPeriod' ].item().split(';')]
    
    Project_df = HSIP_DF[HSIP_DF['HSIP ID'] ==  int(p)]
    Project_df = Project_df.transpose()
    Project_df = Project_df.sort_index()
    Project_df.to_excel(writer, sheet_name = 'ProjectDesc')
    
    NumSeg = 0
    NumInt = 0
    try: NumSeg = int(str(arcpy.GetCount_management(SegFC)))
    except: pass
    try: NumInt = int(str(arcpy.GetCount_management(IntFC)))
    except: pass
    if NumSeg==0 and NumInt == 0:
        print('{}: No Geocoded Location data'.format(p))
        
    PC_df = pd.DataFrame(columns = ['K_PC','A_PC','B_PC','K_EC','A_EC','B_EC'])
    i = 0
    for year in Years:
        PC_df.loc[i] = [0 for j in range(len(PC_df.columns))]
        i += 1
    PC_df.index = Years
    PC_df['Period'] = AssignPeriod(Years,{'BeforePeriod':BeforePeriod,'AfterPeriod':AfterPeriod,'CosntPeriod':ConstPeriod})
    
    SegAtt_df = pd.DataFrame()
    if NumSeg > 0:
        rdfCol = ['Year','SiteID','INVENTORY','BEG_STA','END_STA']
        rdfCol.extend(Fields)
        for year in Years:
            RoadwayData = SegFC + '_' + str(year)
            try:
                rdf = common.AttributeTabletoDF(RoadwayData)
                rdf['Year'] = year
                SegAtt_df = pd.concat([SegAtt_df,rdf[rdfCol]])
                for c in ['K_PC','A_PC','B_PC','K_EC','A_EC','B_EC']:
                    if c in rdf.columns:
                        PC_df.set_value(year,c,PC_df.loc[year][c]+sum(list(rdf[c])))
            except:
                pass
        if len(SegAtt_df)>0:
            SegAtt_df['Period'] = AssignPeriod(list(SegAtt_df['Year']),{'BeforePeriod':BeforePeriod,'AfterPeriod':AfterPeriod,'CosntPeriod':ConstPeriod})
            SegAtt_df.to_excel(writer, sheet_name = 'Segment Attributes')

    IntPoint_df = pd.DataFrame()
    IntApprc_df = pd.DataFrame()
    if NumInt > 0:
        rdfCol = ['Year','SiteID','INVENTORY','MP']
        rdfCol.extend(Fields)
        rdfCol.append('ApprType')
        for year in Years:
            Intpoints = IntFC + '_' + str(year) + '_points'
            Inttables = IntFC + '_' + str(year) + '_tables'
            try:
                rdf1 = common.AttributeTabletoDF(Intpoints)
                rdf2 = common.AttributeTabletoDF(Inttables)
                rdf1['Year'] = year
                rdf2['Year'] = year
                IntPoint_df = pd.concat([IntPoint_df,rdf1[['Year','SiteID','TRAF_CONT','AADT_Major','AADT_Minor','PeerGroup_CH2M_TJM']]])
                IntApprc_df = pd.concat([IntApprc_df,rdf2[rdfCol]])
                for c in ['K_PC','A_PC','B_PC','K_EC','A_EC','B_EC']:
                    if c in rdf1.columns:
                        PC_df.set_value(year,c,PC_df.loc[year][c]+sum(list(rdf1[c])))
            except:
                pass
            
        if len(IntPoint_df)>0:
            IntPoint_df['Period'] = AssignPeriod(list(IntPoint_df['Year'])  ,{'BeforePeriod':BeforePeriod,'AfterPeriod':AfterPeriod,'CosntPeriod':ConstPeriod})
            IntPoint_df.to_excel(writer, sheet_name = 'IntPointAttr')
        if len(IntApprc_df)>0:
            IntApprc_df['Period'] = AssignPeriod(list(IntApprc_df['Year']),{'BeforePeriod':BeforePeriod,'AfterPeriod':AfterPeriod,'CosntPeriod':ConstPeriod})
            IntApprc_df.to_excel(writer, sheet_name = 'IntApproachAttr')
            
    if len(IntPoint_df) == 0 and len(SegAtt_df) == 0:
        print('{}: No Segment or Intersection attributes found'.format(p))
        
    df3 = DF_RawCrash(MDB,p,Years,BeforePeriod,AfterPeriod,ConstPeriod)        
    if len(df3) == 0:
        print('{}: No crash data'.format(p))
        return
    df3.to_excel(writer, sheet_name = 'RawCrash')
    #df4 = pd.DataFrame()
    #for year in BeforePeriod:
    #    SegCrashes = SegFC + '_' + str(year) + '_Crash'
    #    cdf = common.AttributeTabletoDF(SegCrashes)
    #    cdf['Year'] = year
    #    df4 = pd.concat([df4,cdf])
    #df4 = CrashTypeDF(df4)
    #df4.to_excel(writer, sheet_name = 'SegBeforeCrashType')
    
    #df5 = pd.DataFrame()
    #for year in AfterPeriod:
    #    SegCrashes = SegFC + '_' + str(year) + '_Crash'
    #    cdf = common.AttributeTabletoDF(SegCrashes)
    #    cdf['Year'] = year
    #    df5 = pd.concat([df5,cdf])
    #df5 = CrashTypeDF(df5)
    #df5.to_excel(writer, sheet_name = 'SegAfterCrashType')
    #PlotCrashType(df4,df5)
    
    df6 = CrashSevDF(df3,Years)
    df6['Period'] = AssignPeriod(list(df6.index),{'BeforePeriod':BeforePeriod,'AfterPeriod':AfterPeriod,'CosntPeriod':ConstPeriod})
    #df6.to_excel(writer, sheet_name = 'SegCrashSevAll')

    df7 = CrashSevDF(df3,BeforePeriod)
    df7.to_excel(writer, sheet_name = 'CrashSevBefore')
    
    df8 = CrashSevDF(df3,AfterPeriod)
    df8.to_excel(writer, sheet_name = 'CrashSevAfter')
    
    constcost = HSIP_DF[HSIP_DF['HSIP ID']==int(p)]['Total Award Amount'].item()
    ServiceYears = 15

    df9 = DF_BCDetail(Years,df6,PC_df,constcost,BeforePeriod,AfterPeriod,ConstPeriod,ServiceYears,Interest,TrafficGrowth,CrashCost)
    df9.to_excel(writer, sheet_name = 'BCDetails')

    df10 = DF_BCSummary(BeforePeriod,AfterPeriod,df9)
    df10.to_excel(writer, sheet_name = 'BCSummary')
    print(df10.loc[2])
    #print('{}: Finished: BC_OC: {:0.2f}, BC_EC: {:0.2f}'.format(p,EUAB_OC/EUAC,EUAB_EC/EUAC))
    writer.save()

    writer.close()
def DF_BCSummary(BeforePeriod,AfterPeriod,df9):
    df10 = pd.DataFrame(columns=['Period','BeginYear','EndYear',
                                 'K_OC','A_OC','B_OC','K_EC','A_EC','B_EC',
                                 'EUAC','EUAB_OC','EUAB_EC','BC_OC','BC_EC'])
    EUAC    = list(df9.loc[AfterPeriod]['EUAC'])[0]
    EUAB_OC = list(df9.loc[AfterPeriod]['EUAB_OC'])[0]
    EUAB_EC = list(df9.loc[AfterPeriod]['EUAB_EC'])[0]
    BC_EC = 0
    BC_OC = 0
    if EUAC!=0:
        BC_EC = EUAB_EC/EUAC
        BC_OC = EUAB_OC/EUAC

    df10.loc[1] = ['Before' , 
                   BeforePeriod[0],
                   BeforePeriod[-1],
                   np.mean([list(df9.loc[BeforePeriod]['K_OC'])]),
                   np.mean([list(df9.loc[BeforePeriod]['A_OC'])]),
                   np.mean([list(df9.loc[BeforePeriod]['B_OC'])]),
                   np.mean([list(df9.loc[BeforePeriod]['K_EC'])]),
                   np.mean([list(df9.loc[BeforePeriod]['A_EC'])]),
                   np.mean([list(df9.loc[BeforePeriod]['B_EC'])]),
                   0,0,0,0,0
                  ]
    df10.loc[2] = ['After' , 
                   AfterPeriod[0],
                   AfterPeriod[-1],
                   np.mean([list(df9.loc[AfterPeriod]['K_OC'])]),
                   np.mean([list(df9.loc[AfterPeriod]['A_OC'])]),
                   np.mean([list(df9.loc[AfterPeriod]['B_OC'])]),
                   np.mean([list(df9.loc[AfterPeriod]['K_EC'])]),
                   np.mean([list(df9.loc[AfterPeriod]['A_EC'])]),
                   np.mean([list(df9.loc[AfterPeriod]['B_EC'])]),
                   EUAC,EUAB_OC,EUAB_EC,BC_OC,BC_EC
                  ]
    return(df10)
def DF_BCDetail(Years,df6,PC_df,constcost,BeforePeriod,AfterPeriod,ConstPeriod,ServiceYears,Interest,TrafficGrowth,CrashCost):
    df9 = pd.DataFrame(columns=['Period',
                                'K_OC','A_OC','B_OC','C_OC','PDO_OC',
                                'K_PC','A_PC','B_PC','K_EC','A_EC','B_EC',
                                'ConstCost',
                                'CrashCost_OC',
                                'CrashCost_EC'
                               ])
    df9['Period'] = list(df6.loc[Years]['Period'])
    df9['K_OC']   = list(df6.loc[Years]['K_Crashes'])
    df9['A_OC']   = list(df6.loc[Years]['A_Crashes'])
    df9['B_OC']   = list(df6.loc[Years]['B_Crashes'])
    df9['C_OC']   = list(df6.loc[Years]['C_Crashes'])
    df9['PDO_OC'] = list(df6.loc[Years]['PDO'])
    for c in ['K_PC','A_PC','B_PC','K_EC','A_EC','B_EC']:
        df9[c]   = list(PC_df.loc[Years][c])
    constcost1 = [0 for y in BeforePeriod]
    constcost2 = [constcost/len(ConstPeriod) for y in ConstPeriod]
    constcost3 = [0 for y in AfterPeriod]
    ccl = constcost1
    ccl.extend(constcost2)
    ccl.extend(constcost3)
    df9['ConstCost'] = ccl
    #df9['ConstCostPV'] = [TodayDollar(ccl[i],y,CurYear,Interest) for i,y in enumerate(Years)]
    df9['CrashCost_OC'] =   [sum([df9.loc[i][c+'_OC'].item()*CrashCost[c] for c in ['K','A','B','C','PDO']]) for i,y in enumerate(Years)]
    #df9['CrashCost_OCPV'] = [TodayDollar(df9.loc[i]['CrashCost_OC'].item(),y,CurYear,Interest) for i,y in enumerate(Years)]
    df9['CrashCost_EC'] =   [sum([df9.loc[i][c+'_EC'].item()*CrashCost[c] for c in ['K','A','B']]) for i,y in enumerate(Years)]
    #df9['CrashCost_ECPV'] = [TodayDollar(df9.loc[i]['CrashCost_EC'].item(),y,CurYear,Interest) for i,y in enumerate(Years)]
    df9.index = Years
    
    ServicePeriod = range(AfterPeriod[-1]+1,ConstPeriod[-1]+ServiceYears+1)
    for i in ServicePeriod:
        df9.loc[i] = ['Service',
                  np.mean([list(df9.loc[AfterPeriod]['K_OC'])]),
                  np.mean([list(df9.loc[AfterPeriod]['A_OC'])]),
                  np.mean([list(df9.loc[AfterPeriod]['B_OC'])]),
                  np.mean([list(df9.loc[AfterPeriod]['C_OC'])]),
                  np.mean([list(df9.loc[AfterPeriod]['PDO_OC'])]),
                  np.mean([list(df9.loc[AfterPeriod]['K_PC'])]),
                  np.mean([list(df9.loc[AfterPeriod]['A_PC'])]),
                  np.mean([list(df9.loc[AfterPeriod]['B_PC'])]),
                  np.mean([list(df9.loc[AfterPeriod]['K_EC'])]),
                  np.mean([list(df9.loc[AfterPeriod]['A_EC'])]),
                  np.mean([list(df9.loc[AfterPeriod]['B_EC'])]),
                  0,
                  np.mean([list(df9.loc[AfterPeriod]['CrashCost_OC'])]),
                  #TodayDollar(np.mean([list(df9.loc[AfterPeriod]['CrashCost_OC'])]),i,CurYear,Interest),
                  np.mean([list(df9.loc[AfterPeriod]['CrashCost_EC'])])
                  #TodayDollar(np.mean([list(df9.loc[AfterPeriod]['CrashCost_EC'])]),i,CurYear,Interest)
                     ]
    EUAC    = constcost * AP(Interest,ServiceYears)
    CrashBenefit_OC = np.mean([list(df9.loc[BeforePeriod]['CrashCost_OC'])]) - np.mean([list(df9.loc[AfterPeriod]['CrashCost_OC'])])
    CrashBenefit_EC = np.mean([list(df9.loc[BeforePeriod]['CrashCost_EC'])]) - np.mean([list(df9.loc[AfterPeriod]['CrashCost_EC'])])
    EUAB_OC = CrashBenefit_OC * FA(TrafficGrowth,ServiceYears) /ServiceYears
    EUAB_EC = CrashBenefit_EC * FA(TrafficGrowth,ServiceYears) /ServiceYears
    #if EUAB_OC<0: EUAB_OC = 0
    #if EUAB_EC<0: EUAB_EC = 0
    df9.set_value(range(ConstPeriod[-1]+1,ConstPeriod[-1]+ServiceYears+1),'EUAC',EUAC)
    df9.set_value(range(ConstPeriod[-1]+1,ConstPeriod[-1]+ServiceYears+1),'EUAB_OC',EUAB_OC)
    df9.set_value(range(ConstPeriod[-1]+1,ConstPeriod[-1]+ServiceYears+1),'EUAB_EC',EUAB_EC)
    return(df9)
def RemoveTotals(df):
    df = df[[c for c in df.columns if c!='Total']]
    df = df.loc[[i for i in df.index if i!='Total']]
    return(df)
def PlotCrashType(DFBefore,DFAfter):
    ymin = 0
    ymax = 12
    fig, ax = plt.subplots(figsize=(6,3))  
    axes = plt.gca()
    axes.set_ylim([ymin,ymax])    
    DFBefore = RemoveTotals(DFBefore)
    DFAfter = RemoveTotals(DFAfter)
    df = DFBefore
    sev = df.index
    margin_bottom = np.zeros(len(df.columns))
    
    #cmap = mcolors.LinearSegmentedColormap('redgreen',  [(0,'#FF0000'),(1,'#74C476')], 100)
    #colors = [cmap(i) for i in np.linspace(0, 1, 5)]
    colors = ["red", "brown","coral","yellow","green"]

    for num, s in enumerate(sev):
        values = list(df.loc[s])

        df.loc[s].plot.bar(ax=ax, stacked=True, 
                                    bottom = margin_bottom, label=s,color = colors[num])
        margin_bottom += values
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    ax.grid()
    plt.title('Before Period')
    plt.show()
    fig, ax = plt.subplots(figsize=(6,3))  
    axes = plt.gca()
    axes.set_ylim([ymin,ymax])    
    df = DFAfter
    sev = df.index
    margin_bottom = np.zeros(len(df.columns))

    for num, s in enumerate(sev):
        values = list(df.loc[s])

        df.loc[s].plot.bar(ax=ax, stacked=True, 
                                    bottom = margin_bottom, label=s,color = colors[num])
        margin_bottom += values
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    ax.grid()
    plt.title('After Period')
    
    plt.savefig('plt.png',transparent=True)
    plt.show()
def CreateEmptyCSDF(Years):
    CSDF = pd.DataFrame(columns = ['K_Crashes','A_Crashes','B_Crashes','C_Crashes','Fatalities','A_Injuries','B_Injuries','C_Injuries','PDO','Wet_Weather','Not_Lighted'])
    i = 0
    for year in Years:
        CSDF.loc[i] = [0 for j in range(len(CSDF.columns))]
        i += 1
    CSDF.index = Years
    return(CSDF)
def AddCrashSevValues(DF,year,SiteCrash):
    DF.loc[year]['K_Crashes']   += len([1 for i,r in SiteCrash.iterrows() if r['Crash_injury_severity']=='Fatal Crash'    and r['Crash_Year']==year-2000])
    DF.loc[year]['A_Crashes']   += len([1 for i,r in SiteCrash.iterrows() if r['Crash_injury_severity']=='A Injury Crash' and r['Crash_Year']==year-2000])
    DF.loc[year]['B_Crashes']   += len([1 for i,r in SiteCrash.iterrows() if r['Crash_injury_severity']=='B Injury Crash' and r['Crash_Year']==year-2000])
    DF.loc[year]['C_Crashes']   += len([1 for i,r in SiteCrash.iterrows() if r['Crash_injury_severity']=='C Injury Crash' and r['Crash_Year']==year-2000])
    DF.loc[year]['PDO']         += sum([1 for i,r in SiteCrash.iterrows() if r['Crash_injury_severity']=='No Injuries'    and r['Crash_Year']==year-2000])
    DF.loc[year]['Wet_Weather'] += sum([1 for i,r in SiteCrash.iterrows() if r['Weather']=='Rain' and r['Crash_Year']==year-2000])
    DF.loc[year]['Not_Lighted'] += sum([1 for i,r in SiteCrash.iterrows() if r['Light_condition']=='Darkness' and r['Crash_Year']==year-2000])
    DF.loc[year]['Fatalities']  += sum([r['Total_killed'] for i,r in SiteCrash.iterrows() if r['Crash_Year']==year-2000])
    DF.loc[year]['A_Injuries']  += sum([r['A_injuries'] for i,r in SiteCrash.iterrows() if r['Crash_Year']==year-2000])
    DF.loc[year]['B_Injuries']  += sum([r['B_injuries'] for i,r in SiteCrash.iterrows() if r['Crash_Year']==year-2000])
    DF.loc[year]['C_Injuries']  += sum([r['C_injuries'] for i,r in SiteCrash.iterrows() if r['Crash_Year']==year-2000])
    return(DF)
def CrashSevDF(Data,Years):
    DFSev = CreateEmptyCSDF(Years)
    for year in Years:
        DFSev = AddCrashSevValues(DFSev,year,Data)
    DFSev['Total'] = [sum([r[c].item() for c in ['K_Crashes','A_Crashes','B_Crashes','C_Crashes','PDO']]) for i,r in DFSev.iterrows()]
    DFSev.loc['Total'] = [sum(DFSev[c]) for c in DFSev.columns]
    return(DFSev)
def AssignPeriod(L,Assignmnts):
    out = []
    for l in L:
        a = ''
        for i in Assignmnts.keys():
            if l in Assignmnts[i]:
                a = i
                break
        out.append(a)
    return(out)
def TodayDollar(Value,Year,CurYear,interest):
    n = CurYear - Year
    r = (1+interest)**n
    return(Value*r)
def CrashTypeDF(Data):
    ctL = []
    for i,r in Data.iterrows():
        ct = r['Type_of_crash']
        ct_adj = ct.lower()
        ct_adj = ct_adj.replace('-', ' ')
        ctL.append(ct_adj)
    Data['Type_of_crash'] = ctL
    Rows = ['Fatal Crash','A Injury','B Injury','C Injury','PDO']
    Columns = ['animal', 'fixed object', 'head on', 'overturned', 'other object','other non collision',
           'rear end','angle','turning','sideswipe opposite direction', 'sideswipe same direction',
           'parked motor vehicle', 'pedestrian',]
    Summary = Data['Type_of_crash'].value_counts()
    CTDF = pd.DataFrame(columns = Columns)
    for ct in Columns:
        CTDF[ct] = [
           sum([1 for i,r in Data.iterrows() if r['Type_of_crash'] == ct and r['Crash_injury_severity']=='Fatal Crash']), 
           sum([1 for i,r in Data.iterrows() if r['Type_of_crash'] == ct and r['Crash_injury_severity']=='A Injury Crash']), 
           sum([1 for i,r in Data.iterrows() if r['Type_of_crash'] == ct and r['Crash_injury_severity']=='B Injury Crash']), 
           sum([1 for i,r in Data.iterrows() if r['Type_of_crash'] == ct and r['Crash_injury_severity']=='C Injury Crash']), 
           sum([1 for i,r in Data.iterrows() if r['Type_of_crash'] == ct and r['Crash_injury_severity']=='No Injuries']), 
        ]
    CTDF.index = Rows
    CTDF['Total'] = [sum([r[c].item() for c in CTDF.columns]) for i,r in CTDF.iterrows()]
    CTDF.loc['Total'] = [sum(CTDF[c]) for c in CTDF.columns]
    return(CTDF)
def AP(i,n):
        r = (1+i)**n
        return(i*r/(r-1))
def FA(i,n):
        r = (1+i)**n
        return((r-1)/i)
def BCRatio(TotalCost,ServiceYears,Interest,TrafficGrowth,AverageCrashValue,CMF):

    TotalCost = 6243402
    ServiceYears = 15
    Interest = 0.04
    TrafficGrowth = 0.02
    AverageCrashBenefit = AverageCrashValue * (1-CMF)  # Average crash cost per year for before period x CMF
    TotalCost = float(TotalCost)
    EUAC = TotalCost * AP(Interest,ServiceYears)
    EUAB = AverageCrashBenefit * FA(TrafficGrowth,ServiceYears) /ServiceYears
    BC = EUAB/EUAC
    print(EUAB,EUAC)
    return(BC)
def DF_RawCrash(MDB,p,Years,BeforePeriod,AfterPeriod,ConstPeriod):
    #p = int(os.path.basename(MDB).split('_')[1])
    SegFC = MDB + '\\Seg_' + p
    IntFC = MDB + '\\Int_' + p
    NumSeg = 0
    NumInt = 0
    try: NumSeg = int(str(arcpy.GetCount_management(SegFC)))
    except: pass
    try: NumInt = int(str(arcpy.GetCount_management(IntFC)))
    except: pass

    if NumSeg > 0:
        df3 = pd.DataFrame()
        for year in Years:
            SegCrashes = SegFC + '_' + str(year) + '_Crash'
            try:
                cdf = common.AttributeTabletoDF(SegCrashes)
                cdf['Year'] = year
                df3 = pd.concat([df3,cdf])
            except:
                pass
    if NumInt > 0:
        df3 = pd.DataFrame()
        for year in Years:
            IntCrashes = IntFC + '_' + str(year) + '_points_Crash'
            try:
                cdf = common.AttributeTabletoDF(IntCrashes)
                cdf['Year'] = year
                df3 = pd.concat([df3,cdf])
            except:
                pass
    if 'Year' in df3.columns:
        df3['Period'] = AssignPeriod(list(df3['Year']),{'BeforePeriod':BeforePeriod,'AfterPeriod':AfterPeriod,'CosntPeriod':ConstPeriod})
    return(df3)
def CON_ExcelSheetSummary(WDir,HSMPY_PATH,MDB,Years,ExcelOut,HSIP_Path,Title,Fields):
    sys.path.append(HSMPY_PATH)
    pyFN = os.path.join(WDir , 'HSIP_' + str(Title) + '_ExcelSum.py')
    OutFile = open(pyFN, 'w')
    pyfile = """from time import gmtime, strftime
print(strftime("%Y-%m-%d %H:%M:%S"))
Title = "{}"
print("Create Summary Sheet: " + Title)
import os, sys
import pandas as pd
import atexit
#atexit.register(raw_input, 'Press Enter to continue...')
HSMPY_PATH = r'{}'
MDB = r'{}'
Years = {}
ExcelOut = r'{}'
HSIP_Path = r'{}'
Fields = {}
sys.path.append(HSMPY_PATH) 
import hsmpy
import numpy as np
import arcpy
HSIP_DF = hsmpy.il.ReadHSIPData(HSIP_Path,Years)
hsmpy.il.HSIP_SummarySheet(HSIP_DF,Title,MDB,ExcelOut,Years,Fields)
print(strftime("%Y-%m-%d %H:%M:%S"))
""".format(Title,HSMPY_PATH,MDB,Years,ExcelOut,HSIP_Path,Fields)
    OutFile.write(pyfile)
    OutFile.close()
    SubProcess = subprocess.Popen(
                [sys.executable, pyFN])
                #shell=False,creationflags = subprocess.CREATE_NEW_CONSOLE)
    return(SubProcess)
def HIP_FindMissingData(gdb,Years):
    Mis_Base = []
    Mis_Att = []
    Mis_Crash = []
    Results = {'Seg_Input':0,'Int_Input':0}
    for year in Years:
        Results.update({'BaseRoute_' + str(year):0,
                        'BaseInt_'   + str(year):0,
                        'BaseTable_' + str(year):0,
                        'SegAtt_'    + str(year):None,
                        'SegCrash_'  + str(year):None,
                        'IntPoints_' + str(year):None,
                        'IntTables_' + str(year):None,
                        'IntCrash_'  + str(year):None})
    hsip_id = int(os.path.basename(gdb).split('_')[1])
    FCs = [gdb + '\\' + fc for fc in common.ListFCinGDBorMDB(gdb)]
    SegFC = gdb + '\\Seg_' + str(hsip_id)
    IntFC = gdb + '\\Int_' + str(hsip_id)
    if SegFC in FCs:
        Results.update({'Seg_Input':int(str(arcpy.GetCount_management(SegFC)))})
    if IntFC in FCs:
        Results.update({'Int_Input':int(str(arcpy.GetCount_management(IntFC)))})
    if Results['SegInput'] + Results['IntInput']==0:
        return({'Mis_Loc':True,'Mis_Base':Mis_Base,'Mis_Att':Mis_Att,'Mis_Crash':Mis_Crash})
    for year in Years:
        BaseRoute = gdb + '\\' + 'HWY' + str(year) + '_route'
        BaseTab   = gdb + '\\' + 'HWY' + str(year) + '_inter'
        BaseInt   = gdb + '\\' + 'HWY' + str(year) + '_table'
        if BaseRoute in FCs:
            Results.update({'BaseRoute_' + str(year):int(str(arcpy.GetCount_management(BaseRoute)))})
        if BaseInt in FCs:
            Results.update({'BaseInt_' + str(year):int(str(arcpy.GetCount_management(BaseInt)))})
        if BaseTab in FCs:
            Results.update({'BaseTable_' + str(year):int(str(arcpy.GetCount_management(BaseTab)))})

        SegAtt    = gdb + '\\' + 'Seg_' + str(hsip_id) + '_' + str(year)
        SegCrash  = SegAtt + '_Crash'
        IntPoints = gdb + '\\' + 'Int_' + str(hsip_id) + '_' + str(year) + '_points'
        IntTables = gdb + '\\' + 'Int_' + str(hsip_id) + '_' + str(year) + '_tables'
        IntCrash  = IntPoints + '_Crash'
        if SegAtt in FCs:
            Results.update({'SegAtt_'    + str(year):int(str(arcpy.GetCount_management(SegAtt)))})
        if SegCrash in FCs:
            Results.update({'SegCrash_' + str(year):int(str(arcpy.GetCount_management(SegCrash)))})
        if IntPoints in FCs:
            Results.update({'IntPoints_' + str(year):int(str(arcpy.GetCount_management(IntPoints)))})
        if IntTables in FCs:
            Results.update({'IntTables_'  + str(year):int(str(arcpy.GetCount_management(IntTables)))})
        if IntCrash in FCs:
            Results.update({'IntCrash_'  + str(year):int(str(arcpy.GetCount_management(IntCrash)))})
    for year in Years:
        AttFlag = False
        CrashFlag = False
        if Results['BaseRoute_' + str(year)] ==0 or Results['BaseInt_' + str(year)] ==0 or Results['BaseTable_' + str(year)] ==0:
            Mis_Base.append(str(year))
        if Results['Seg_Input'] > 0:
            if Results['SegAtt_' + str(year)] is None:
                AttFlag = True
            if Results['SegCrash_' + str(year)] is None:
                CrashFlag = True
        if Results['Int_Input'] > 0:
            if Results['IntPoints_' + str(year)] is None or Results['IntTables_' + str(year)] is None:
                AttFlag = True
            if Results['IntCrash_' + str(year)] is None:
                CrashFlag = True
        if AttFlag:
            Mis_Att.append(str(year))
        if CrashFlag:
            Mis_Crash.append(str(year))
    return({'Mis_Loc':False,'Mis_Base':Mis_Base,'Mis_Att':Mis_Att,'Mis_Crash':Mis_Crash})


