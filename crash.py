# Developed By Mahdi Rajabi mrajabi@clemson.edu
import os
import sys
import common
import fields
import datetime
import copy
import arcpy
import subprocess 
import time

def parallel_geocode(LocFile,CrashYear,StateLayer,Routes,Tolerance,FinalOutput,subsetEntries,ScrathDir,PathtoHSMPY):
    ScratchLabel  = 'PGEO'
    TextFileLabel = 'LocText'
    GeoOutLabel   = 'Loc'
    i = 0
    while os.path.exists(ScrathDir + '\\' + ScratchLabel + '_' + str(i)):
        i += 1
    ScrathDir += '\\' + ScratchLabel + '_' + str(i)
    os.makedirs(ScrathDir)
    print('Create ' + ScratchLabel + '_' + str(i))
    #FinalGDB = 'Final.gdb'
    #FinalGDB = Outgdb
    #arcpy.CreateFileGDB_management(ScrathDir, FinalGDB)
    #for j in range(0,len(LocFile)):
    print(LocFile)
    ScratchGDB  = str(CrashYear) + '.gdb'
    arcpy.CreateFileGDB_management(ScrathDir, ScratchGDB)
    AllLoc = ScrathDir + '\\' + ScratchGDB + '\\' + TextFileLabel + '_' + str(CrashYear)
    arcpy.TableToTable_conversion(LocFile,
                                  ScrathDir + '\\' + ScratchGDB,
                                  TextFileLabel + '_' + str(CrashYear))
    numObservations = int(arcpy.GetCount_management(AllLoc).getOutput(0))
    numNewFeatureClasses = (numObservations // subsetEntries) + 1   
    OutList = []
    SubProcess =[]
    PyList = []
    for i in range(1, (numNewFeatureClasses + 1)):
        subsetFC = TextFileLabel + '_' + str(CrashYear) + '_' + str(i)
        print(' - ' + subsetFC)
        subsetGDB = str(CrashYear) + '_' + str(i) + '.gdb'
        arcpy.CreateFileGDB_management(ScrathDir, subsetGDB)
        startNdx = ((i-1) * subsetEntries) + 1
        endNdx = startNdx + subsetEntries - 1
        whereClause = '"OBJECTID" >= ' + str(startNdx) + ' AND "OBJECTID" <= ' + str(endNdx)
        arcpy.TableSelect_analysis(AllLoc,
                                    ScrathDir + '\\' + subsetGDB + '\\' + subsetFC,
                                    whereClause)
        OutFile = open(ScrathDir + '\\' + subsetFC+'.py', 'w')
        Input = ScrathDir + '\\' + subsetGDB + '\\' + subsetFC
        Output = ScrathDir + '\\' + subsetGDB + '\\' + GeoOutLabel + '_' + str(CrashYear) + '_' + str(i)
        OutList.append(Output)
        pyfile = """print("Import")
import os, sys
import arcpy
sys.path.append('{}')
import hsmpy
hsmpy.crash.geocode('{}',{},'{}','{}',{},'{}')
hsmpy.crash.locAttributes('{}','{}')
""".format(PathtoHSMPY,Input.replace('\\','\\\\'),CrashYear,StateLayer.replace('\\','\\\\'),
            Routes.replace('\\','\\\\'),Tolerance,Output.replace('\\','\\\\'),
            Input.replace('\\','\\\\'),Output.replace('\\','\\\\'))
        OutFile.write(pyfile)
        OutFile.close()
        PyList.append(ScrathDir + '\\' + subsetFC+'.py')

    for py in PyList:
        SubProcess.append(subprocess.Popen(
            [sys.executable, py],
            shell=False,creationflags = subprocess.CREATE_NEW_CONSOLE))
    print(' - Waiting for Subprocesses')
    w = [p.wait() for p in SubProcess]
    print(w)
    Merge = ScrathDir + '\\' + ScratchGDB + '\\' + GeoOutLabel + '_Merge_' + str(CrashYear)
    arcpy.Merge_management(OutList,Merge)
    arcpy.Sort_management(Merge,FinalOutput,'Name')
def geocode(LocFile,CrashYear,StateLayer,Routes,Tolerance,Output):
    print('Geocode Based on Milepost and Lat/Lon')

    def ANOtoName(Row, CrashYear,LastArtifANO):
        if Row:
            ANO = Row.getValue('ANO')
            try:
                ANO = int(ANO)
            except:
                ANO = 9999
        else:
            ANO = -1
        if ANO >= (CrashYear - 2000) * 10 ** 6 and ANO < (CrashYear - 2000) * 10 ** 6 + 999999 and ANO <> 9999:
            Name = str(ANO)
        else:
            Name = str(int(LastArtifANO) + 1)
        return ANO
    def Dec2String(L):
        L = abs(L)
        Deg = int(L)
        Min = int((L-Deg)*60)
        Sec = int((L-Deg-Min/60)*3600*10000)/10000
        return (long('{:02.0f}{:02.0f}{:04.0f}'.format(Deg,Min,Sec)))
    def Deg2Dec(S):
        Deg = 0
        Min = 0
        Sec = 0
        Comm = 'NA'
        if len(S)==8:
            Deg = S[0:2]
            Min = S[2:4]
            Sec = S[4:8]
        try:
            Deg = float(Deg)
            Min = float(Min)
            Sec = float(Sec)
            if Min>60 or Sec>6000:
                Comm = 'DD'
                Dec = Deg + float(S[2:8])/1000000.0
            else:
                Comm = 'DMS'
                Dec = Deg + Min/60 +  Sec/100/3600
        except:
            Dec = 0
        return({'Dec':Dec,'Comm':Comm})
    def DD2Dec(S):
        Deg = 0
        Min = 0
        Sec = 0
        if len(S)==8:
            Deg = S[0:2]
            Min = S[2:4]
            Sec = S[4:8]
        try:
            Deg = float(Deg)
            Min = float(Min)
            Sec = float(Sec)
            Dec = Deg + float(S[2:8])/1000000.0
        except:
            Dec = 0
        return(Dec)
    def LRSByNumber(cd,MBS,LRSD):

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
            
            LRS = '{:02.0f}{:02.0f}{:05.0f}{:02.0f}{}'.format(cd['County'],rt,rn,ra,dir)

            if not LRS in LRSD.keys():
                LRS = LRS[:-1]+'T'
                if not LRS in LRSD.keys():
                    LRS = ''
            
            return(LRS)
    def LRSByName  (cd,MBS,RD,LRSD,MLRS=''):
        LRS = []
        if cd[MBS]['nam'] <> '' and cd[MBS]['nam'] in RD.keys():
            for lrs in RD[cd[MBS]['nam']]:
                exlrs = ExplodeLRS(lrs)
                if exlrs['County']==cd['County'] and exlrs['typ']==cd[MBS]['typ']:
                   LRS.append(lrs)
        if len(LRS)>1:
            if MBS == 'M':
                if cd['P'] <> '':
                    LRS = ClosestLineToPoint(LRS,cd['P'],LRSD)
                else:
                    LRS = ''
            if MBS in ['B','S']:
                LRS = SelectLRS(LRS,cd,LRSD,MLRS)
        else:
            if len(LRS)==0:
                LRS=''
            else:
                LRS=LRS[0]
        return(LRS)
    def LRSBySPJ   (cd,LRSD):
        LRS = ''
        lrsL = [lrs for lrs in cd['RouteL']]
        if len(lrsL)==0:
            LRS = ''
        if len(lrsL)==1:
            LRS = lrsL[0]
        if len(lrsL)>1:
            dist = []
            for lrs in lrsL:
                dist.append(LRSD[lrs].distanceTo(cd['P']))
            LRS = lrsL[dist.index(min(dist))]
        return(LRS)
    def ExplodeLRS(lrs):
        cnty = int(lrs[0:2])
        rt   = int(lrs[2:4])
        rn   = int(lrs[4:9])
        ra   = int(lrs[9:11])
        dir  =    (lrs[-1])
        return({'County':cnty,'typ':rt,'num':rn,'aux':ra,'dir':dir})
    def FindLRS(cd,MBS,LRSD,RD):
        LRS = LRSByNumber(cd,MBS,LRSD)
        if LRS == '':
            LRS = LRSByName(cd,MBS,RD,LRSD)
            if LRS == '':
                LRS = LRSBySPJ(cd,MBS,LRSD)
        return(LRS)      
    def TouchTest(BSLRSList,MLRS,LRSD):
        OutList = []
        for lrs in BSLRSList:
            if LRSD[MLRS].distanceTo(LRSD[lrs])<250:
                OutList.append(lrs)
        return(OutList)
    def ClosestLineToPoint(BSLRSList,Pnt,LRSD):
        dist = []
        for lrs in BSLRSList:
            dist.append(LRSD[lrs].distanceTo(Pnt))
        return(BSLRSList[dist.index(min(dist))])
    def ClosestLinetoLine(BSLRSList,MLRS,LRSD):
        dist = []
        for lrs in BSLRSList:
            dist.append(LRSD[MLRS].distanceTo(LRSD[lrs]))
        return(BSLRSList[dist.index(min(dist))])
    def SelectLRS(LRSList,cd,LRSD,MLRS):
        if len(LRSList)==0:
            LRS = ''
        if len(LRSList)==1:
            LRS = LRSList[0]
        if len(LRSList)>=1:
            TL = TouchTest(LRSList,MLRS,LRSD)
            if len(TL)==0:
                LRS = ''
            if len(TL)==1:
                LRS = TL[0]
            if len(TL)>1:
                if cd['P']<>'':
                    LRS = ClosestLineToPoint(TL,cd['P'],LRSD)
                else:
                    LRS = ClosestLinetoLine(TL,MLRS,LRSD)
        return(LRS)        
    def ReadOffset(cd,BMp=-1,SMp=-1):
        Offset = 0
        if cd['OffInd'] == 'F':
            Offset = cd['Offset']
        if cd['OffInd'] == 'M':
            if int(cd['Offset']) == cd['Offset']:
                Offset = cd['Offset'] * 52.8
                if (BMp<>-1 and SMp <> -1) and ((BMp<SMp and BMp + Offset > SMp) or (BMp>SMp and BMp - Offset < SMp)):
                    Offset = cd['Offset'] * 5.28
            else:
                Offset = cd['Offset'] * 5280
                if (BMp<>-1 and SMp <> -1) and ((BMp<SMp and BMp + Offset > SMp) or (BMp>SMp and BMp - Offset < SMp)):
                    Offset = cd['Offset'] * 52.8
        return Offset
    def GeocodeM(cd,LRSD,RD,Tolerance):
        Status = {'MLRS':'','BLRS':'','SLRS':'',
                  'Geocode':'','Comment_M':'','Comment_XY':'',
                  'FinalPoint':-1,'Update':'',
                  'BIp':-1,'SIp':-1,'Cp_M':-1,'SnapP':-1,'CrossOffset':-1,'MpDiff':-1}
        Comm = cd['Comm']
        # Geocode Based on M (Main, Base and Second Routes + BDO + ODR)
        # Finding MLRS
        MLRS = LRSByNumber(cd,'M',LRSD)
        if MLRS == '':
            MLRS = LRSByName(cd,'M',RD,LRSD)
            if MLRS == '':
                if cd['P']<>'':
                    MLRS = LRSBySPJ(cd,LRSD)
        # Finding BLRS and SLRS
        BLRS = ''
        SLRS = ''
        BIp = -1
        SIp = -1
        Cp_M = -1
        if MLRS<>'':
            if cd['P'] <> '':
                q = LRSD[MLRS].queryPointAndDistance(cd['P'])
                CMp_XY   = LRSD[MLRS].measureOnLine(cd['P'])
                Cp_XY    = q[0]
                CrossOff = q[2]
                if not q[3]:
                    CrossOff = -q[2]
                if abs(CrossOff)>Tolerance:
                    if cd['Comm'] == 'DMS':
                        pnt = cd['P'].projectAs(common.WGS1984)
                        ddpnt = arcpy.Point(-DD2Dec(str(Dec2String(pnt.firstPoint.X))),DD2Dec(str(Dec2String(pnt.firstPoint.Y))))
                        pnt = arcpy.PointGeometry(ddpnt,common.WGS1984).projectAs(common.NAD1983SC)
                        q = LRSD[MLRS].queryPointAndDistance(pnt)
                        if q[2]<Tolerance:
                            cd['P'] = pnt
                            CMp_XY   = LRSD[MLRS].measureOnLine(cd['P'])
                            Cp_XY    = q[0]
                            CrossOff = q[2]
                            cd['Comm'] == 'DD'
                Status['SnapP'      ] = Cp_XY
                Status['CrossOffset'] = CrossOff
            BLRSList = []
            SLRSList = []
            for dir in ['T','N','S','W','E']:
                if (cd['B']['typ'] == 5 and dir == 'T') or cd['B']['typ'] <> 5:
                    cd['B']['dir'] = dir
                    LRS = LRSByNumber(cd,'B',LRSD)
                    if LRS <> '':
                        BLRSList.append(LRS)
                if (cd['S']['typ'] == 5 and dir == 'T') or cd['S']['typ'] <> 5:
                    cd['S']['dir'] = dir
                    LRS = LRSByNumber(cd,'S',LRSD)
                    if LRS <> '':
                        SLRSList.append(LRS)
            if len(BLRSList) == 0:
                LRS = LRSByName(cd,'B',RD,LRSD,MLRS)
                if LRS <> '':
                    BLRSList.append(LRS)
            if len(SLRSList) == 0:
                LRS = LRSByName(cd,'S',RD,LRSD,MLRS)
                if LRS <> '':
                    SLRSList.append(LRS)
            BLRS = SelectLRS(BLRSList,cd,LRSD,MLRS)
            SLRS = SelectLRS(SLRSList,cd,LRSD,MLRS)

            # Finding BIp (Base Intersection Point), BMp (Base Milepost)
            if BLRS<>'':
                BMp = -1
                if LRSD[MLRS].crosses(LRSD[BLRS]):
                    BIp = LRSD[MLRS].intersect(LRSD[BLRS],1)[0]
                    BMp = LRSD[MLRS].measureOnLine(BIp)

                # Finding Crash Point based on Offset (BDO) 
                if BMp <> -1:
                    # Finding the Direction: SLRS or ODR
                    BDO_Dir = 0
                    SMp = -1
                    if SLRS<>'':
                        if LRSD[MLRS].crosses(LRSD[SLRS]):
                            SIp = LRSD[MLRS].intersect(LRSD[SLRS],1)[0]
                            SMp = LRSD[MLRS].measureOnLine(SIp)
                            if SMp > BMp:
                                BDO_Dir = +1
                            else:
                                BDO_Dir = -1
                    if BDO_Dir == 0:
                        BDO_Dir = +1 #Find based on direction of route and BDO 
                    # Find Cp_M and CMp_M (Crash Milepost based on BDO)
                    BDO = ReadOffset(cd,BMp,SMp)
                    CMp_M = BMp + BDO*BDO_Dir
                    Cp_M  = LRSD[MLRS].positionAlongLine(CMp_M)
                    Dist = -1
                    if cd['P'] <> '':
                        Dist = common.GetDistance(Cp_M,Cp_XY)
                    Status['MpDiff'] = Dist
                    # Compare M geocode and XY geocode
                    if cd['P'] <> '':
                        if abs(CrossOff) > Tolerance:
                            if SMp <> -1:
                                if (BMp<=SMp and BMp + BDO <= SMp) or (BMp>=SMp and BMp - BDO >= SMp):
                                    Status['Geocode'] = 'M'
                                    Status['Comment_M' ] = 'BETWEEN BI AND SI'
                                    Status['Comment_XY'] = 'OFF MLRS'
                                    Status['FinalPoint'] = Cp_M
                                    Status['Update'] = 'FROM XY TO M'
                                else:
                                    Status['Geocode'] = ''
                                    Status['Comment_M' ] = 'FALSE BDO'
                                    Status['Comment_XY'] = 'OFF MLRS'
                                    Status['FinalPoint'] = cd['P']
                                    Status['Update'] = 'XY REMOVED'
                            else:
                                Status['Geocode'] = 'M'
                                Status['Comment_M' ] = 'ONLY BI'
                                Status['Comment_XY'] = 'OFF MLRS'
                                Status['FinalPoint'] = Cp_M
                                Status['Update'] = 'FROM XY TO M WITHOUT SI'
                        else:
                            if SMp <> -1:
                                if (BMp<=SMp and BMp + BDO <= SMp) or (BMp>=SMp and BMp - BDO >= SMp):
                                    Status['Geocode'] = 'M and XY'
                                    Status['Comment_M' ] = 'BETWEEN BI AND SI'
                                    Status['Comment_XY'] = 'ON MLRS'
                                    Status['FinalPoint'] = cd['P']
                                    Status['Update'] = ''
                                else:
                                    Status['Geocode'] = Comm
                                    Status['Comment_M' ] = 'FALSE BDO'
                                    Status['Comment_XY'] = 'ON MLRS'
                                    Status['FinalPoint'] = cd['P']
                                    Status['Update'] = ''
                            else:
                                Status['Geocode'] = Comm
                                Status['Comment_M' ] = 'ONLY BI'
                                Status['Comment_XY'] = 'ON MLRS'
                                Status['FinalPoint'] = cd['P']
                                Status['Update'] = ''
                    else:
                        if SMp <> -1:
                            if (BMp<=SMp and BMp + BDO <= SMp) or (BMp>=SMp and BMp - BDO >= SMp):
                                Status['Geocode'] = 'M'
                                Status['Comment_M' ] = 'BETWEEN BI AND SI'
                                Status['Comment_XY'] = 'OUT OF STATE'
                                Status['FinalPoint'] = Cp_M
                                Status['Update'] = 'OUT OF STATE TO M'
                            else:
                                Status['Geocode'] = ''
                                Status['Comment_M' ] = 'FALSE BDO'
                                Status['Comment_XY'] = 'OUT OF STATE'
                                Status['FinalPoint'] = Cp_M
                                Status['Update'] = ''
                        else:
                            Status['Geocode'] = 'M'
                            Status['Comment_M' ] = 'ONLY BI'
                            Status['Comment_XY'] = 'OUT OF STATE'
                            Status['FinalPoint'] = Cp_M
                            Status['Update'] = 'OUT OF STATE TO M WITHOUT SI'
                else:
                    if cd['P'] <> '':
                        if abs(CrossOff) > Tolerance:
                            Status['Geocode'] = ''
                            Status['Comment_M' ] = 'NO BI'
                            Status['Comment_XY'] = 'OFF MLRS'
                            Status['FinalPoint'] = cd['P']
                            Status['Update'] = 'XY REMOVED'
                        else:
                            Status['Geocode'] = Comm
                            Status['Comment_M' ] = 'NO BI'
                            Status['Comment_XY'] = 'ON MLRS'
                            Status['FinalPoint'] = cd['P']
                            Status['Update'] = ''
                    else:
                        Status['Geocode'] = ''
                        Status['Comment_M' ] = 'NO BI'
                        Status['Comment_XY'] = 'OUT OF STATE'
                        Status['FinalPoint'] = -1
                        Status['Update'] = ''
            else:
                if cd['P'] <> '':
                    if abs(CrossOff) > Tolerance:
                        Status['Geocode'] = ''
                        Status['Comment_M' ] = 'NO BLRS'
                        Status['Comment_XY'] = 'OFF MLRS'
                        Status['FinalPoint'] = cd['P']
                        Status['Update'] = 'XY REMOVED'
                    else:
                        Status['Geocode'] = Comm
                        Status['Comment_M' ] = 'NO BLRS'
                        Status['Comment_XY'] = 'ON MLRS'
                        Status['FinalPoint'] = cd['P']
                        Status['Update'] = ''
                else:
                    Status['Geocode'] = ''
                    Status['Comment_M' ] = 'NO BLRS'
                    Status['Comment_XY'] = 'OUT OF STATE'
                    Status['FinalPoint'] = -1
                    Status['Update'] = ''
        else:
            if cd['P'] <> '':
                Status['Geocode'] = ''
                Status['Comment_M' ] = 'NO MLRS'
                Status['Comment_XY'] = 'NO MLRS'
                Status['FinalPoint'] = cd['P']
                Status['Update'] = ''
            else:
                Status['Geocode'] = ''
                Status['Comment_M' ] = 'NO MLRS'
                Status['Comment_XY'] = 'OUT OF STATE'
                Status['FinalPoint'] = -1
                Status['Update'] = ''
        
        Status['MLRS'] = MLRS
        Status['BLRS'] = BLRS
        Status['SLRS'] = SLRS
        Status['BIp' ] = BIp
        Status['SIp' ] = SIp
        Status['Cp_M'] = Cp_M
        if Status['SnapP'] == -1 and Cp_M <> -1:
            Status['SnapP'] = Cp_M

        return(Status)
    def GeocodeXY(cd,State):
        # Geocode Based on XY (LAT/LON)
        try:
            inity = abs(long(cd['Lat']))
        except:
            inity = -1
        try:
            initx = abs(long(cd['Lon']))
        except:
            initx = -1

        # State Extents
        #NAD Y Min	74,263.2145
        #NAD Y Max	1,233,475.5534
        
        #NAD X Min	1,292,515.4781
        #NAD X Max	2,744,469.5352
        
        #WGS Y Min	32,020,134.0000
        #WGS Y Max	35,120,775.0000
        
        #WGS X Max	78,321,969.0000
        #WGS X Min	83,211,274.0000

        # Deg Min Sec, Psitive LON
        x_NAD = -1
        x_WGS = -1
        y_NAD = -1
        y_WGS = -1
        #Comm_X = 'NA'
        #Comm_Y = 'NA'
        #X_Swapped = False
        #Y_Swapped = False
        if inity>=State['NAD_Extent'].YMin and inity<=State['NAD_Extent'].YMax:
            y_NAD = inity
            #Comm_Y = 'SC'
        if initx>=State['NAD_Extent'].YMin and initx<=State['NAD_Extent'].YMax:
            y_NAD = initx
            #Comm_X = 'SC'
            #X_Swapped = True
        if inity>=State['NAD_Extent'].XMin and inity<=State['NAD_Extent'].XMax:
            x_NAD = inity
            #Comm_X = 'NAD'
            #Y_Swapped = True
        if initx>=State['NAD_Extent'].XMin and initx<=State['NAD_Extent'].XMax:
            x_NAD = initx
            #Comm_X = 'NAD'
        if inity>=Dec2String(State['WGS_Extent'].YMin) and inity<=Dec2String(State['WGS_Extent'].YMax):
            y_WGS = inity
            #Comm_Y = 'WGS'
        if initx>=Dec2String(State['WGS_Extent'].YMin) and initx<=Dec2String(State['WGS_Extent'].YMax):
            y_WGS = initx
            #Comm_Y = 'WGS'
            #X_Swapped = True
        if inity>=Dec2String(State['WGS_Extent'].XMax) and inity<=Dec2String(State['WGS_Extent'].XMin):
            x_WGS = inity
            #Comm_X = 'WGS'
            #Y_Swapped = True
        if initx>=Dec2String(State['WGS_Extent'].XMax) and initx<=Dec2String(State['WGS_Extent'].XMin):
            x_WGS = initx
            #Comm_X = 'WGS'

        pnt = ''
        if x_WGS<>-1 and y_WGS<>-1:
            X = Deg2Dec(str(x_WGS))
            Y = Deg2Dec(str(y_WGS))
            pnt = arcpy.PointGeometry(arcpy.Point(-X['Dec'],Y['Dec']),common.WGS1984).projectAs(common.NAD1983SC)
            Comm = X['Comm']
        elif x_NAD<>-1 and y_NAD<>-1:
            Comm = 'SC'
            pnt = arcpy.PointGeometry(arcpy.Point(x_NAD,y_NAD),common.NAD1983SC)
        #elif (x_WGS<>-1 or x_NAD<>-1) and (y_WGS==-1 or y_NAD==-1):
        #    Comm = 'NO Y,'
        #elif (y_WGS<>-1 or y_NAD<>-1) and (x_WGS==-1 or x_NAD==-1):
        #    Comm = 'NO X,'
        #else:
        #    Comm = 'NO XY,'
        
        #if X_Swapped and Y_Swapped:
        #    Comm += 'SWAPPED,'
        
        if pnt <> '':
            if not pnt.within(State['NAD_Shape']):
                pnt = ''
                Comm = 'OUT OF STATE'
        else:
            Comm = 'OUT OF STATE'

        return({'P':pnt,'Comm':Comm})
    def RemainingTime(ElapsedSec,Total,Index):
        S = 0
        AveSec = ElapsedSec/max(Index,1)
        RemainTime = AveSec * (Total-Index)
        RemainDays  = int(RemainTime/60/60/24) 
        RemainHours = int((RemainTime - RemainDays * 24)/60/60) 
        RemainMins  = int((RemainTime - RemainDays * 24*60    - RemainHours*60)/60) 
        RemainSecs  = int (RemainTime - RemainDays * 24*60*60 - RemainHours*60*60 - RemainMins*60) 
        if RemainDays>0:
            S = '{:1.0f} Day(s) Remain'.format(RemainDays)
        elif RemainDays==0 and RemainHours>0:
            S = '{:1.0f} Hour(s) Remain'.format(RemainHours)
        elif RemainHours==0 and RemainMins>0:
            S = '{:1.0f} Min(s) Remain'.format(RemainMins)
            if RemainMins<60:
                S = '<60 Min(s) Remain'
            if RemainMins<50:
                S = '<50 Min(s) Remain'
            if RemainMins<40:
                S = '<40 Min(s) Remain'
            if RemainMins<30:
                S = '<30 Min(s) Remain'
            if RemainMins<20:
                S = '<20 Min(s) Remain'
            if RemainMins<10:
                S = '<10 Min(s) Remain'
            if RemainMins<5:
                S = '<5 Min(s) Remain'
        elif RemainMins==0:
            S = '<5 Min(s) Remain'
        return S

    BIP = os.path.splitext(Output)[0] + '_BIp' + os.path.splitext(Output)[1]
    SIP = os.path.splitext(Output)[0] + '_SIp' + os.path.splitext(Output)[1]
    CPM = os.path.splitext(Output)[0] + '_CpM' + os.path.splitext(Output)[1]
    SNP = os.path.splitext(Output)[0] + '_Snp' + os.path.splitext(Output)[1]
    LFR = os.path.splitext(Output)[0] + '_LFR' + os.path.splitext(Output)[1]
    SPJ = os.path.splitext(Output)[0] + '_SpatialJoin' + os.path.splitext(Output)[1]
    NSR = os.path.splitext(Output)[0] + '_Notsorted' + os.path.splitext(Output)[1]
    #NPR = os.path.splitext(Output)[0] + '_NotProjected' + os.path.splitext(Output)[1]
    arcpy.Delete_management(BIP)
    arcpy.Delete_management(SIP)
    arcpy.Delete_management(CPM)
    arcpy.Delete_management(SPJ)
    arcpy.Delete_management(SNP)
    arcpy.Delete_management(LFR)
    arcpy.Delete_management(NSR)
    #arcpy.Delete_management(NPR)
    arcpy.Delete_management(Output)
    CrashYear = int(CrashYear)

    print('Search Cursor: ' + os.path.basename(StateLayer))
    SC = arcpy.SearchCursor(StateLayer)
    SRow = SC.next()
    shape = SRow.getValue('Shape')
    shapeWGS = shape.projectAs(common.WGS1984)
    shapeNAD = shape.projectAs(common.NAD1983SC)
    State = {'NAD_Shape':shapeNAD,'NAD_Extent':shapeNAD.extent,'WGS_Shape':shapeWGS,'WGS_Extent':shapeWGS.extent}
    del SRow, SC

    print("Create Feature Class: " + os.path.basename(NSR))
    arcpy.CreateFeatureclass_management(os.path.dirname(NSR),os.path.basename(NSR),
                                        "POINT",'','DISABLED','DISABLED',common.NAD1983SC)
    #print("Project: " + os.path.basename(NPR))
    #arcpy.Project_management(NPR,NSR,common.NAD1983SC)

    print("Add Fields: " + os.path.basename(NSR))
    FieldDic = [fields.loc.ANO,
                fields.loc.LON,fields.loc.LAT,
                fields.loc.GMET,fields.loc.GCXY,fields.loc.GDXY,fields.loc.GCMP,fields.loc.GDMP,
                fields.loc.CTY, 
                fields.loc.RCT, fields.loc.RTN ,fields.loc.ALS , fields.loc.RAI, fields.loc.DLR, fields.loc.MLRS, fields.loc.MEAS, 
                fields.loc.BIR, fields.loc.BRN, fields.loc.ALSB, fields.loc.BRA,                 fields.loc.BLRS,
                fields.loc.SIC, fields.loc.SRN, fields.loc.ALSS, fields.loc.SRA,                 fields.loc.SLRS,
                fields.loc.BDI, fields.loc.BDO, fields.loc.ODR]
    for field in FieldDic:
        print(" - " + field['name'])
        arcpy.AddField_management(NSR,field['name'],field['type'],field['precision'],field['scale'],field['length'],field['alias'],field['nullable'],field['required'])
    
    print("Count: " + os.path.basename(LocFile))
    C = int(str(arcpy.GetCount_management(LocFile)))
    print(" - Total Items Found: {:,}".format(C))

    print("Search Cursor: " + os.path.basename(LocFile))
    CD = {}
    for r in arcpy.SearchCursor(LocFile):
        ANO = common.GetANO(r)
        if ANO>=(CrashYear-2000)*10**6 and ANO<(CrashYear-2000)*10**6+999999 and ANO<>99999999:
            CD.update({ANO: {'RouteL':[],
                          'County'  :common.ConvertType(common.GetVal(r,fields.loc.CTY['name']),fields.loc.CTY['type']),
                          'Lat'     :common.ConvertType(common.GetVal(r,fields.loc.LAT['name']),fields.loc.LAT['type']),
                          'Lon'     :common.ConvertType(common.GetVal(r,fields.loc.LON['name']),fields.loc.LON['type']),
                          'Offset'  :common.ConvertType(common.GetVal(r,fields.loc.BDO['name']),fields.loc.BDO['type']),
                          'OffDir'  :common.ConvertType(common.GetVal(r,fields.loc.ODR['name']),fields.loc.ODR['type']),
                          'OffInd'  :common.ConvertType(common.GetVal(r,fields.loc.BDI['name'],''),fields.loc.BDI['type']),
                          'MEAS'    :-1,
                          'M':{'typ':common.ConvertType(common.GetVal(r,fields.loc.RCT['name'],5),fields.loc.RCT['type']),
                               'num':common.ConvertType(common.GetVal(r,fields.loc.RTN['name']),fields.loc.RTN['type']),
                               'aux':common.ConvertType(common.GetVal(r,fields.loc.RAI['name']),fields.loc.RAI['type']),
                               'dir':common.ConvertType(common.GetVal(r,fields.loc.DLR['name'],'T'),fields.loc.DLR['type']),
                               'nam':common.ConvertType(common.GetVal(r,fields.loc.ALS['name'],''),fields.loc.ALS['type'])},
                          'B':{'typ':common.ConvertType(common.GetVal(r,fields.loc.BIR['name'],5),fields.loc.BIR['type']),
                               'num':common.ConvertType(common.GetVal(r,fields.loc.BRN['name']),fields.loc.BRN['type']),
                               'aux':common.ConvertType(common.GetVal(r,fields.loc.BRA['name']),fields.loc.BRA['type']),
                               'dir':'',
                               'nam':common.ConvertType(common.GetVal(r,fields.loc.ALSB['name'],''),fields.loc.ALSB['type'])},
                          'S':{'typ':common.ConvertType(common.GetVal(r,fields.loc.SIC['name'],5),fields.loc.SIC['type']),
                               'num':common.ConvertType(common.GetVal(r,fields.loc.SRN['name']),fields.loc.SRN['type']),
                               'aux':common.ConvertType(common.GetVal(r,fields.loc.SRA['name']),fields.loc.SRA['type']),
                               'dir':'',
                               'nam':common.ConvertType(common.GetVal(r,fields.loc.ALSS['name'],''),fields.loc.ALSS['type'])}}})
    for ano in CD:
        if not CD[ano]['County'] in range(1,47):
            print('No County')
            CD[ano]['County'] = 0
        for MBS in ['M','B','S']:
            if not CD[ano][MBS]['typ'] in [1,2,3,4,5]:
                CD[ano][MBS]['typ'] = 5
        for MBS in ['M','B','S']:
            if not CD[ano][MBS]['aux'] in [0,2,5,6,7,9]:
                CD[ano][MBS]['aux'] = 0  

    print("Insert Cursor: " + os.path.basename(NSR))
    IC = arcpy.InsertCursor(NSR)
    NameSorted = CD.keys()
    NameSorted.sort()
    Comm_Stat = {}
    start = datetime.datetime.now()
    remain_old = ''
    for name in NameSorted:
        Status = GeocodeXY(CD[name],State)
        CD[name].update(Status)
        IRow = IC.newRow() 
        IRow.setValue(fields.loc.ANO  ['name'],name)
        
        IRow.setValue(fields.loc.LON['name'],CD[name]['Lon'])
        IRow.setValue(fields.loc.LAT['name'],CD[name]['Lat'])
        
        IRow.setValue(fields.loc.CTY['name'],CD[name]['County'])

        IRow.setValue(fields.loc.RCT['name'],CD[name]['M']['typ'])
        IRow.setValue(fields.loc.RTN['name'],CD[name]['M']['num'])
        IRow.setValue(fields.loc.ALS['name'],CD[name]['M']['nam'])
        IRow.setValue(fields.loc.RAI['name'],CD[name]['M']['aux'])
        IRow.setValue(fields.loc.DLR['name'],CD[name]['M']['dir'])

        IRow.setValue(fields.loc.BIR['name'],CD[name]['B']['typ'])
        IRow.setValue(fields.loc.BRN['name'],CD[name]['B']['num'])
        IRow.setValue(fields.loc.ALSB['name'],CD[name]['B']['nam'])
        IRow.setValue(fields.loc.BRA['name'],CD[name]['B']['aux'])
        
        IRow.setValue(fields.loc.SIC['name'],CD[name]['B']['typ'])
        IRow.setValue(fields.loc.SRN['name'],CD[name]['B']['num'])
        IRow.setValue(fields.loc.ALSS['name'],CD[name]['B']['nam'])
        IRow.setValue(fields.loc.SRA['name'],CD[name]['B']['aux'])
        
        IRow.setValue(fields.loc.BDI['name'],CD[name]['OffInd'])
        IRow.setValue(fields.loc.BDO['name'],CD[name]['Offset'])
        IRow.setValue(fields.loc.ODR['name'],CD[name]['OffDir'])

        if CD[name]['P']<>'':
            IRow.setValue('Shape',CD[name]['P'])
        IC.insertRow(IRow) 
        if CD[name]['Comm'] in Comm_Stat.keys():
            Comm_Stat[CD[name]['Comm']] += 1
        else:
            Comm_Stat.update({CD[name]['Comm']:1})
        elapsed = datetime.datetime.now() - start
        remain = RemainingTime(elapsed.total_seconds(),len(NameSorted),NameSorted.index(name))
        if remain<>remain_old:
            print(remain)
        remain_old = remain
        #print(' -  {}, ANO: {:<13}, GEOCODE: {:<20}'.format(remain,name,S)) 
    del IC
    for comm in Comm_Stat:
        if comm[-1]==',':
            print(' - {:>25}: {:,}'.format(comm+'IN STATE',Comm_Stat[comm]))
        else:
            print(' - {:>25}: {:,}'.format(comm,Comm_Stat[comm]))
    print(' - {:>25}: {:,}'.format('Total Crashes',len(CD)))
        
    print('Search Cursor: ' + os.path.basename(Routes))
    start = datetime.datetime.now()
    RD = {}
    for r in arcpy.SearchCursor(Routes):
        N1 = r.getValue('StreetN1')
        N2 = r.getValue('StreetN2')
        RD.update({N1:[],N2:[]})
    for r in arcpy.SearchCursor(Routes):
        N1 = r.getValue('StreetN1')
        N2 = r.getValue('StreetN2')
        if N1<>'':RD[N1].append(r.getValue('Name'))
        if N2<>'':RD[N2].append(r.getValue('Name'))
    LRSD = {r.getValue('Name'):r.getValue('Shape') for r in arcpy.SearchCursor(Routes)}
    stop = datetime.datetime.now()-start
    TotTime = stop.seconds + stop.microseconds/1000000
    print(' - {:>25}: {:,}'.format('Total Routes',len(LRSD)))
    print(' - {:>25}: {:,}'.format('Total Route Names',len(RD)))
    print(' - {:>25}: {:2.2f} seconds'.format('Total Time',TotTime))
    
    print('Spatial Join: ' + os.path.basename(NSR) + ' + '  + os.path.basename(Routes) )
    fm1  = arcpy.FieldMap()
    fm2  = arcpy.FieldMap()
    fms = arcpy.FieldMappings()
    fm1.addInputField(NSR,fields.loc.ANO['name'])
    fm2.addInputField(Routes,fields.route.Name['name'])
    fms.addFieldMap(fm1)
    fms.addFieldMap(fm2)
    arcpy.SpatialJoin_analysis(NSR,Routes,SPJ,"JOIN_ONE_TO_MANY","KEEP_COMMON",fms,"WITHIN_A_DISTANCE",str(Tolerance) + ' Feet')
    for r in arcpy.SearchCursor(SPJ):
        ano = common.GetANO(r)
        CD[ano]['RouteL'].append(r.getValue('Name'))
    arcpy.Delete_management(SPJ)

    print("Update Cursor: " + os.path.basename(NSR))
    GMETDict = {''            :0,                                                        'M':5,'SC':6,'DD':7,'DMS':8,'M and XY':9}
    GCXYDict = {'OUT OF STATE':0,'NO MLRS':1,'OFF MLRS':2,                                                            'ON MLRS':9}
    GCMPDict = {                 'NO MLRS':1, 'NO BLRS':2, 'NO BI':3,'FALSE BDO':4,'ONLY BI':5,             'BETWEEN BI AND SI':9}
    UC = arcpy.UpdateCursor(NSR)
    Comm_Stat = {}
    i = 0
    start = datetime.datetime.now()
    for URow in UC:
        name = common.GetANO(URow)
        #print(name)
        Status = GeocodeM(CD[name],LRSD,RD,Tolerance)
        CD[name].update(Status)
        URow.setValue(fields.loc.GMET['name'],GMETDict[CD[name]['Geocode']])
        URow.setValue(fields.loc.GCMP['name'],GCMPDict[CD[name]['Comment_M']])
        URow.setValue(fields.loc.GCXY['name'],GCXYDict[CD[name]['Comment_XY']])
        if CD[name]['CrossOffset']<>-1:
            URow.setValue(fields.loc.GDXY['name'],CD[name]['CrossOffset'])
        if CD[name]['MpDiff']<>-1:
            URow.setValue(fields.loc.GDMP['name'],CD[name]['MpDiff'])
        
        URow.setValue(fields.loc.MLRS['name'],CD[name]['MLRS'])
        URow.setValue(fields.loc.BLRS['name'],CD[name]['BLRS'])
        URow.setValue(fields.loc.SLRS['name'],CD[name]['SLRS'])

        if CD[name]['FinalPoint']<>-1:
            URow.setValue('Shape',CD[name]['FinalPoint'])
            i += 1
        UC.updateRow(URow) 

        if CD[name]['Update'] in Comm_Stat.keys():
            Comm_Stat[CD[name]['Update']] += 1
        else:
            Comm_Stat.update({CD[name]['Update']:1})

        elapsed = datetime.datetime.now() - start
        remain = RemainingTime(elapsed.total_seconds(),len(NameSorted),NameSorted.index(name))
        if remain<>remain_old:
            print(remain)
        remain_old = remain
        #print(' -  {}, ANO: {:<13}, GEOCODE: {:<10},{:<50},{:<40}'.format(remain,name,Status['Geocode'],Status['Comment_M'],Status['Comment_XY'])) 
    del UC

    for comm in Comm_Stat:
        print(' - {:>25}: {:,}'.format(comm,Comm_Stat[comm]))
    print(' - {:>25}: {:,}'.format('Total Updated',i))

    print("Insert Cursor: " + os.path.basename(SNP))
    arcpy.CreateFeatureclass_management(os.path.dirname(SNP),os.path.basename(SNP),
                                        "POINT",'','DISABLED','DISABLED',common.NAD1983SC)
    field = fields.loc.ANO
    arcpy.AddField_management(SNP,field['name'],field['type'],field['precision'],field['scale'],field['length'],field['alias'],field['nullable'],field['required'])
    field = fields.loc.MLRS
    arcpy.AddField_management(SNP,field['name'],field['type'],field['precision'],field['scale'],field['length'],field['alias'],field['nullable'],field['required'])
    IC = arcpy.InsertCursor(SNP)
    for name in NameSorted:
        if CD[name]['SnapP']<>-1:
            IRow = IC.newRow() 
            IRow.setValue(fields.loc.ANO['name'],name)
            IRow.setValue(fields.loc.MLRS['name'],CD[name]['MLRS'])
            IRow.setValue('Shape',CD[name]['SnapP'])
            IC.insertRow(IRow) 
    del IC

    print("Locate Features Along Routes: " + os.path.basename(SNP))
    arcpy.LocateFeaturesAlongRoutes_lr(in_features=SNP,
                                       in_routes=Routes,
                                       route_id_field=fields.route.Name['name'],
                                       radius_or_tolerance="500 Feet",
                                       out_table=LFR,
                                       out_event_properties="RID POINT MEAS",
                                       route_locations="ALL",
                                       distance_field="DISTANCE",
                                       zero_length_events="ZERO",
                                       in_fields="FIELDS",
                                       m_direction_offsetting="M_DIRECTON")
    for r in arcpy.SearchCursor(LFR):
        rid = r.getValue('RID')
        mlrs = r.getValue(fields.loc.MLRS['name'])
        if mlrs == rid:
            ano = common.GetANO(r)
            meas = r.getValue('MEAS')
            CD[ano]['MEAS'] = r.getValue('MEAS')
    arcpy.Delete_management(SNP)
    arcpy.Delete_management(LFR)

    print("Update Cursor: " + os.path.basename(NSR))
    field = fields.loc.Label
    arcpy.AddField_management(NSR,field['name'],field['type'],field['precision'],field['scale'],field['length'],field['alias'],field['nullable'],field['required'])
    UC = arcpy.UpdateCursor(NSR)
    for URow in UC:
        ano = common.GetANO(URow)
        S = ''
        if CD[ano]['MLRS']<>'':
            if CD[ano]['MEAS']<>-1:
                URow.setValue(fields.loc.MEAS['name'],CD[ano]['MEAS'])
                S = '{},{:07.3f}'.format(CD[ano]['MLRS'],CD[ano]['MEAS'])
            else:
                S = '{},{}'.format(CD[ano]['MLRS'],'No Mp')
        else:
            S = 'No MLRS'
        URow.setValue(fields.loc.Label['name'],S)
        UC.updateRow(URow) 

    print("Sort: " + os.path.basename(NSR))
    arcpy.Sort_management(NSR,Output,fields.loc.Label['name'])
    arcpy.Delete_management(NSR)

    #print("Insert Cursor: " + os.path.basename(CPM))
    #arcpy.CreateFeatureclass_management(os.path.dirname(CPM),os.path.basename(CPM),
    #                                    "POINT",'','DISABLED','DISABLED',common.NAD1983SC)
    #field = fields.loc.Label
    #arcpy.AddField_management(CPM,field['name'],field['type'],field['precision'],field['scale'],field['length'],field['alias'],field['nullable'],field['required'])
    #IC = arcpy.InsertCursor(CPM)
    #for name in NameSorted:
    #    if CD[name]['Cp_M']<>-1:
    #        IRow = IC.newRow() 
    #        IRow.setValue(fields.loc.Label['name'],name)
    #        IRow.setValue('Shape',CD[name]['Cp_M'])
    #        IC.insertRow(IRow) 
    #del IC

    #print("Insert Cursor: " + os.path.basename(BIP))
    #arcpy.CreateFeatureclass_management(os.path.dirname(BIP),os.path.basename(BIP),
    #                                    "POINT",'','DISABLED','DISABLED',common.NAD1983SC)
    #arcpy.AddField_management(BIP,field['name'],field['type'],field['precision'],field['scale'],field['length'],field['alias'],field['nullable'],field['required'])
    #IC = arcpy.InsertCursor(BIP)
    #for name in NameSorted:
    #    if CD[name]['BIp']<>-1:
    #        IRow = IC.newRow() 
    #        IRow.setValue(fields.loc.Label['name'],name)
    #        IRow.setValue('Shape',CD[name]['BIp'])
    #        IC.insertRow(IRow) 
    #del IC

    #print("Insert Cursor: " + os.path.basename(SIP))
    #arcpy.CreateFeatureclass_management(os.path.dirname(SIP),os.path.basename(SIP),
    #                                    "POINT",'','DISABLED','DISABLED',common.NAD1983SC)
    #arcpy.AddField_management(SIP,field['name'],field['type'],field['precision'],field['scale'],field['length'],field['alias'],field['nullable'],field['required'])
    #IC = arcpy.InsertCursor(SIP)
    #for name in NameSorted:
    #    if CD[name]['SIp']<>-1:
    #        IRow = IC.newRow() 
    #        IRow.setValue(fields.loc.Label['name'],name)
    #        IRow.setValue('Shape',CD[name]['SIp'])
    #        IC.insertRow(IRow) 
    #del IC

    print(" --> Done.")
def geocode_old(LocFile,LatField,LonField,ANOField,CrashYear,StateLayer,Instate,OutOfState):
    print("Geocode Crashes")
    # Stores the not projected in state crash features
    Instate_NotProj = os.path.splitext(Instate)[0] + '_NotProj' + os.path.splitext(Instate)[1]
    SPJ = os.path.splitext(Instate)[0] + '_SpatialJoin' + os.path.splitext(Instate)[1]
    arcpy.Delete_management(Instate_NotProj)
    arcpy.Delete_management(Instate)
    arcpy.Delete_management(OutOfState)
    arcpy.Delete_management(SPJ)

    CrashYear = int(CrashYear)

    print("Count: " + os.path.basename(LocFile))
    C = arcpy.GetCount_management(LocFile)
    print(" - Total Items Found: " + str(C))

    print("Search Cursor: " + os.path.basename(LocFile))
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
    CDic = {common.GetANO(SRow):{'Lat':Deg2Dec(str(SRow.getValue(LatField))),
                          'Lon':Deg2Dec(str(SRow.getValue(LonField)))} for SRow in arcpy.SearchCursor(LocFile)}
    Tot = len(CDic)
    print("Create Feature Class: " + os.path.basename(Instate_NotProj))
    arcpy.CreateFeatureclass_management(os.path.dirname(Instate_NotProj),os.path.basename(Instate_NotProj),
                                        "POINT",'','DISABLED','DISABLED',common.WGS1984)

    print("Add Fields: " + os.path.basename(Instate_NotProj))
    FieldDic = [fields.loc.Label,fields.loc.ANO]
    for field in FieldDic:
        print(" - " + field['name'])
        arcpy.AddField_management(Instate_NotProj,field['name'],field['type'],field['precision'],field['scale'],field['length'],field['alias'],field['nullable'],field['required'])

    print("Insert Cursor: " + os.path.basename(Instate_NotProj))
    Pt = arcpy.Point()
    IC = arcpy.InsertCursor(Instate_NotProj) 
    ANOList = CDic.keys()
    ANOList.sort()
    j = 0
    for ANO in ANOList:
        if ANO >= (CrashYear - 2000) * 10 ** 6 and ANO < (CrashYear - 2000) * 10 ** 6 + 999999 and ANO <> 99999999:
            j = j + 1
            IRow = IC.newRow() 
            Pt.X = CDic[ANO]['Lon']
            Pt.Y = CDic[ANO]['Lat']
            IRow.setValue(fields.loc.ANO['name'],ANO)
            IRow.shape = Pt
            IC.insertRow(IRow)      
    del IC

    print("Project: " + os.path.basename(Instate_NotProj))
    CrashLayer = arcpy.Project_management(Instate_NotProj,Instate,common.NAD1983SC)
    arcpy.Delete_management(Instate_NotProj)

    print("Spatial Join: " + os.path.basename(Instate) + ' + ' + os.path.basename(StateLayer))
    arcpy.SpatialJoin_analysis(Instate,StateLayer,SPJ,"JOIN_ONE_TO_ONE","KEEP_COMMON",'',"INTERSECT")
    InState = [SRow.getValue('ANO') for SRow in arcpy.SearchCursor(SPJ)]
    arcpy.Delete_management(SPJ)

    print("Update Cursor: " + os.path.basename(Instate))
    UC = arcpy.UpdateCursor(Instate) 
    for URow in UC:
        ANO = common.GetANO(URow) 
        if not ANO in InState:
            UC.deleteRow(URow)      
    del UC

    t = float(str(C))
    i = float(len(InState))
    ip = i/t
    ip = int(ip*10000)/100.0
    print(" - Total: %d, False ANOs: %d, In-state(percentage): %d, %r" %(t, (t-j), i, ip))
    
    print("Create Table: " + os.path.basename(OutOfState))
    arcpy.CreateTable_management(os.path.dirname(OutOfState),os.path.basename(OutOfState))

    print("Add Fields: " + os.path.basename(OutOfState))
    for field in FieldDic:
        print(" - " + field['name'])
        arcpy.AddField_management(OutOfState,field['name'],field['type'],field['precision'],field['scale'],field['length'],field['alias'],field['nullable'],field['required'])

    print("Insert Cursor: " + os.path.basename(OutOfState))
    IC = arcpy.InsertCursor(OutOfState) 
    ANOList = CDic.keys()
    ANOList.sort()
    j = 0
    for ANO in ANOList:
        if not ANO in InState:
            if ANO >= (CrashYear - 2000) * 10 ** 6 and ANO < (CrashYear - 2000) * 10 ** 6 + 999999 and ANO <> 99999999:
                j = j + 1
                IRow = IC.newRow() 
                IRow.setValue(fields.loc.ANO['name'],ANO)
                IC.insertRow(IRow)      
    del IC
    print(" - Out-state: %d" %(j))

    print('Caculate Field: Label') 
    arcpy.CalculateField_management(Instate,fields.loc.Label['name'],'!ANO!',"PYTHON_9.3")
    arcpy.CalculateField_management(OutOfState,fields.loc.Label['name'],'!ANO!',"PYTHON_9.3")
    print(" --> Done.")
def locAttributes(CrashInput,LocInput):
    print("Import Crash Attributes")
    print("Count: " + os.path.basename(CrashInput))
    C = arcpy.GetCount_management(CrashInput)
    print(" - Total Items Found: " + str(C))

    print("Count: " + os.path.basename(LocInput))
    U = arcpy.GetCount_management(LocInput)
    print(" - Total Items Found: " + str(U))

    print("Add Field: " + os.path.basename(CrashInput))
    CrashTypeDic = [fields.loc.CTY, 
                fields.loc.RCT, fields.loc.RTN ,fields.loc.ALS , fields.loc.RAI, fields.loc.DLR,  
                fields.loc.BIR, fields.loc.BRN, fields.loc.ALSB, fields.loc.BRA,                 
                fields.loc.SIC, fields.loc.SRN, fields.loc.ALSS, fields.loc.SRA,                 
                fields.loc.BDI, fields.loc.BDO, fields.loc.ODR,
        fields.loc.LOA, fields.loc.ART,
                    fields.loc.DAT, fields.loc.DAY, fields.loc.TIM , fields.loc.PNT, fields.loc.PAT, 
                    fields.loc.ALC, fields.loc.WCC, fields.loc.RSC , fields.loc.AHC,fields.loc.TWAY, fields.loc.TCT, fields.loc.JCT,
                    fields.loc.UNT, fields.loc.FHE, fields.loc.HEL , fields.loc.XWK, fields.loc.PRC, fields.loc.OCF1, fields.loc.OCF2, fields.loc.OCF3, fields.loc.OCF4, fields.loc.MAC,  
                    fields.loc.FAT, fields.loc.INJ,
                    fields.loc.JUR,
                    fields.loc.WZN, fields.loc.WZT, fields.loc.WZL, fields.loc.WPR,
                    fields.loc.REPORT,
                    fields.loc.Symbol]

    for field in CrashTypeDic:
        print(' - ' + field['name'])
        arcpy.DeleteField_management(CrashInput,field['name'])
        arcpy.AddField_management   (CrashInput,field['name'],field['type'],field['precision'],field['scale'],field['length'],field['alias'],field['nullable'],field['required'])

    print("Search Cursor: " + os.path.basename(LocInput))
    LocDic = {common.GetANO(SRow):{} for SRow in arcpy.SearchCursor(LocInput)}
    for SRow in arcpy.SearchCursor(LocInput):
        ANO = common.GetANO(SRow)
        for Field in CrashTypeDic:
            try:
                if Field['name']=='DAY_':
                    Val = SRow.getValue('DAY')
                else:
                    Val = SRow.getValue(Field['name'])
            except:
                Val = ''
            LocDic[ANO].update({Field['name']:Val})

    print("Update Cursor: " + os.path.basename(CrashInput))
    UC = arcpy.UpdateCursor(CrashInput)
    i = 0
    for URow in UC:
        ANO = common.GetANO(URow)
        if ANO in LocDic.keys():
            i += 1
            for Field in CrashTypeDic:
                URow.setValue(Field['name'],common.ConvertType(LocDic[ANO][Field['name']],Field['type']))
        UC.updateRow(URow)
    del UC
    arcpy.CalculateField_management(CrashInput,fields.loc.Symbol['name'],'fval(!UNT!,!FAT!,!INJ!)',"PYTHON_9.3","""def fval(unt,fat,inj):
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

    print(" - Total Crashes Updated: " + str(i))
    print(" --> Done.")
def unitAttributes(UnitInput,CrashYear,Output):
    print("Import Unit Crash Attributes")
    # Stores the not sorted unit table
    Output_NotSorted = os.path.splitext(Output)[0] + '_NotSorted' + os.path.splitext(Output)[1]
    arcpy.Delete_management(Output_NotSorted)
    arcpy.Delete_management(Output)

    CrashYear = int(CrashYear)

    print("Create Table: " + os.path.basename(Output_NotSorted))
    arcpy.CreateTable_management(os.path.dirname(Output_NotSorted),os.path.basename(Output_NotSorted))

    print("Add Field: " + os.path.basename(Output_NotSorted))
    UnitDic1 = [fields.unit.AUN,
                fields.unit.DOB, fields.unit.DSEX, fields.unit.DRAC, 
                fields.unit.VMK, fields.unit.VYR,  fields.unit.RPS, fields.unit.VRY, fields.unit.RPN, fields.unit.NOC, fields.unit.UTC, fields.unit.VUC, fields.unit.VAT, fields.unit.VEW, fields.unit.VIN,
                fields.unit.MAN, fields.unit.CTA,  fields.unit.MHE, fields.unit.SOE]
    UnitDic2 = [fields.unit.API,
                fields.unit.DLN, fields.unit.DLC, fields.unit.DLS,
                fields.unit.VLC1, fields.unit.VLC2, fields.unit.VLC3, fields.unit.DTG, fields.unit.DTT, fields.unit.DTR, fields.unit.UOR,
                fields.unit.EDAM, fields.unit.EAD, fields.unit.MDA, fields.unit.FDA, fields.unit.EDP, fields.unit.PD2,
                fields.unit.ECS, fields.unit.SPL, fields.unit.DOT]
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
    for field in [fields.loc.Label, fields.unit.ID, fields.loc.ANO]:
        print(' - ' + field['name'])
        arcpy.AddField_management(Output_NotSorted,field['name'],field['type'],field['precision'],field['scale'],field['length'],field['alias'],field['nullable'],field['required'])
    for field in UnitDic1:
        print(' - ' + field['name'])
        arcpy.AddField_management(Output_NotSorted,field['name'],field['type'],field['precision'],field['scale'],field['length'],field['alias'],field['nullable'],field['required'])
    for field in [fields.unit.SOE1,fields.unit.SOE2,fields.unit.SOE3,fields.unit.SOE4]:
        print(' - ' + field['name'])
        arcpy.AddField_management(Output_NotSorted,field['name'],field['type'],field['precision'],field['scale'],field['length'],field['alias'],field['nullable'],field['required'])
    for field in UnitDic2:
        print(' - ' + field['name'])
        arcpy.AddField_management(Output_NotSorted,field['name'],field['type'],field['precision'],field['scale'],field['length'],field['alias'],field['nullable'],field['required'])
    UnitDic = UnitDic1 + UnitDic2

    print("Search Cursor: " + os.path.basename(UnitInput))
    Dic = []
    for SRow in arcpy.SearchCursor(UnitInput):
        ANO = common.GetANO(SRow)
        if ANO>=(CrashYear-2000)*10**6 and ANO<(CrashYear-2000)*10**6+999999 and ANO<>99999999:
            s={'ANO':ANO}
            for Field in UnitDic:
                val = SRow.getValue(Field['name'])
                s.update({Field['name']:common.ConvertType(val,Field['type'])})
            Dic.append(s)

    print("Insert Cursor: " + os.path.basename(Output_NotSorted))
    IC = arcpy.InsertCursor(Output_NotSorted)
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
                IRow.setValue(fields.loc.Label['name'],str(Rec['AUN'])+": "+UTC[Rec['UTC']])
            else:
                IRow.setValue(fields.loc.Label['name'],str(Rec['AUN'])+": "+str(Rec['UTC']))

            for Field in UnitDic:
                IRow.setValue(Field['name'],Rec[Field['name']])
            SOEs = common.SOEExtract(Rec[fields.unit.SOE['name']])
            IRow.setValue(fields.unit.SOE1['name'],SOEs[0])
            IRow.setValue(fields.unit.SOE2['name'],SOEs[1])
            IRow.setValue(fields.unit.SOE3['name'],SOEs[2])
            IRow.setValue(fields.unit.SOE4['name'],SOEs[3])

            IC.insertRow(IRow)
    del IC

    print('Sort: ' + os.path.basename(Output_NotSorted))
    arcpy.Sort_management(Output_NotSorted,Output,'ANO;AUN')
    arcpy.Delete_management(Output_NotSorted)
    print(" --> Done.")
def occAttributes(OccInput,CrashYear,Output):
    print("Import Occ Crash Attributes")
    CrashYear = int(CrashYear)

    # Stores the not sorted Occ table
    Output_NotSorted = os.path.splitext(Output)[0] + '_NotSorted' + os.path.splitext(Output)[1]
    arcpy.Delete_management(Output_NotSorted)
    arcpy.Delete_management(Output)

    print("Create Table: " + os.path.basename(Output_NotSorted))
    arcpy.CreateTable_management(os.path.dirname(Output_NotSorted),os.path.basename(Output_NotSorted))

    print("Add Field: " + os.path.basename(Output_NotSorted))
    OccDic = [fields.unit.AUN,
              fields.occ.OCCZIP, fields.occ.OSEX, fields.occ.ORAC, fields.occ.AGE, fields.occ.DBIR,
              fields.occ.SEV, fields.occ.MHI,
              fields.occ.OSL, fields.occ.REU, fields.occ.LAI, fields.occ.EJE,fields.occ.AIR, fields.occ.SWT]
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
    for field in [fields.loc.Label, fields.unit.ID, fields.loc.ANO]:
        print(' - ' + field['name'])
        arcpy.AddField_management(Output_NotSorted,field['name'],field['type'],field['precision'],field['scale'],field['length'],field['alias'],field['nullable'],field['required'])
    for field in OccDic:
        print(' - ' + field['name'])
        arcpy.AddField_management(Output_NotSorted,field['name'],field['type'],field['precision'],field['scale'],field['length'],field['alias'],field['nullable'],field['required'])

    print("Search Cursor: " + os.path.basename(OccInput))
    Dic = []
    i = 0
    for SRow in arcpy.SearchCursor(OccInput):
        i = i + 1
        ANO = common.GetANO(SRow)
        if ANO>=(CrashYear-2000)*10**6 and ANO<(CrashYear-2000)*10**6+999999 and ANO<>99999999:
            s={'ANO':ANO}
            for Field in OccDic:
                val = SRow.getValue(Field['name'])
                s.update({Field['name']:common.ConvertType(val,Field['type'])})
            Dic.append(s)

    print("Insert Cursor: Occ Table")
    IC = arcpy.InsertCursor(Output_NotSorted)
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
                IRow.setValue(fields.loc.Label['name'],OSL[Rec['OSL']])
            else:
                IRow.setValue(fields.loc.Label['name'],str(Rec['OSL']))
            for Field in OccDic:
                IRow.setValue(Field['name'],Rec[Field['name']])
            IC.insertRow(IRow)
    del IC

    print('Sort: ' + os.path.basename(Output_NotSorted))
    arcpy.Sort_management(Output_NotSorted,Output,'ANO;AUN')
    arcpy.Delete_management(Output_NotSorted)
    print(" --> Done.")
def secondary(CrashInput,TimeInt,Distance,Output):
    print("Secondary Crashes")
    SPJ = os.path.splitext(Output)[0] + '_SpatialJoin' + os.path.splitext(Output)[1]
    arcpy.Delete_management(Output)
    arcpy.Delete_management(SPJ)

    print('Count: ' + os.path.basename(CrashInput))
    C = arcpy.GetCount_management(CrashInput)
    arcpy.AddMessage("     - Total Items Found: " + str(C))

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

    print("Search Cursor: " + os.path.basename(CrashInput))
    CDic = {SRow.getValue('ANO'):{'P'   :SRow.getValue('Shape'),
                                  'Time':SRow.getValue(fields.loc.TIM['name']),
                                  'Date':SRow.getValue(fields.loc.DAT['name']),
                                  'RCT' :SRow.getValue(fields.loc.RCT['name']),
                                  'RTN' :SRow.getValue(fields.loc.RTN['name']),
                                  'DIR' :SRow.getValue(fields.loc.DLR['name'])} for SRow in arcpy.SearchCursor(CrashInput)}

    print('Merge: ' + os.path.basename(CrashInput))
    fm  = arcpy.FieldMap()
    fms = arcpy.FieldMappings()
    fm.addInputField(CrashInput,'ANO')
    outF = fm.outputField
    outF.name  = fields.loc.ANO['name']
    outF.alias = fields.loc.ANO['alias']  
    outF.type  = fields.loc.ANO['type']
    fm.outputField = outF
    fms.addFieldMap(fm)
    arcpy.Merge_management(CrashInput,Output,fms)

    print("Spatial Join: " + os.path.basename(Output))
    arcpy.SpatialJoin_analysis(Output, Output, SPJ,"JOIN_ONE_TO_MANY","KEEP_ALL",'',"WITHIN_A_DISTANCE",str(Distance)+" Feet")
    SortedANO = sorted(CDic.keys())
    Pairs   = {ANO:[] for ANO in SortedANO}
    for SRow in arcpy.SearchCursor(SPJ):
        ANO1 = SRow.getValue("ANO")
        ANO2 = SRow.getValue("ANO_1")
        if ANO2>ANO1:
            Pairs[ANO1].append(ANO2)
    arcpy.Delete_management(SPJ)
    
    print("Finding Crash Pairs ...")
    
    FPair   = {ANO:-1 for ANO in SortedANO}
    Primary = []
    Secondary = []
    Prg = 0.1
    for ANO1 in SortedANO:
        if float(SortedANO.index(ANO1))/float(str(C)) >= Prg:
            print(" - " + str(int(Prg*100)) + "% Completed")
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
                            #print(str(ANO1)+', ' + str(ANO2)+','+str(abs(D1-D2).total_seconds()/3600))
                        if (D1-D2).total_seconds() > 0 and not (ANO2 in Secondary):
                            FPair[ANO1]=(ANO2)
                            Primary.append(ANO2)
                            Secondary.append(ANO1)
                                
    print("Add Field: " + os.path.basename(Output))
    for field in [fields.crash.PrmANO,fields.crash.Tempor,fields.crash.Spatio,fields.loc.Label]:
        print(' - ' + field['name'])
        arcpy.AddField_management(Output,field['name'],field['type'],field['precision'],field['scale'],field['length'],field['alias'],field['nullable'],field['required'])

    print("Update Cursor: " + os.path.basename(Output))
    i = 0
    UC = arcpy.UpdateCursor(Output)
    for URow in UC:
        ANO = URow.getValue("ANO")
        if ANO in Secondary:
            URow.setValue(fields.crash.PrmANO['name'],FPair[ANO])
            D1 = DateDecompose(CDic[ANO       ]['Date'],CDic[ANO       ]['Time'])
            D2 = DateDecompose(CDic[FPair[ANO]]['Date'],CDic[FPair[ANO]]['Time'])
            t = abs(D1-D2).total_seconds()/60
            d = common.GetDistance(CDic[ANO]['P'],CDic[FPair[ANO]]['P'])
            URow.setValue(fields.crash.Tempor['name'],t)
            URow.setValue(fields.crash.Spatio['name'],d)
            URow.setValue(fields.loc.Label   ['name'],'{:3.0f}{}{:4.0f}{}'.format(t,' Min, ',d,' Feet'))
            UC.updateRow(URow)
        else:
            UC.deleteRow(URow)

    print(" --> Done.")
def MDB(Loc,Unit,Occ,Jur,Year,Layer,Output):
    print("Create Geodatabase")

    arcpy.Delete_management(Output)

    Year = long(Year)
    print('Create: ' + os.path.basename(Output))
    arcpy.CreatePersonalGDB_management(os.path.dirname(Output),os.path.basename(Output))

    print("Import: " + os.path.basename(Loc))
    arcpy.FeatureClassToFeatureClass_conversion(Loc, Output, "Loc" + str(Year))
    LocTable = Output + '\\Loc' + str(Year)

    print("Import: " + os.path.basename(Unit))
    arcpy.TableToTable_conversion(Unit, Output, "Unit" + str(Year))
    UnitTable = Output + '\\Unit' + str(Year)
      
    print("Import: " + os.path.basename(Occ))
    OccTable = arcpy.TableToTable_conversion(Occ, Output, "Occ" + str(Year))
    OccTable = Output + '\\Occ' + str(Year)

    #print("Import Out Table")
    #arcpy.TableToTable_conversion(Out, Output, "Out" + str(Year))
    #OutTable = Output + '\\Out' + str(Year)

    #print("Import Sec Table")
    #arcpy.TableToTable_conversion(Sec, Output, "Sec" + str(Year))
    #SecTable = Output + '\\Sec' + str(Year)

    print("Import: " + os.path.basename(Jur))
    arcpy.FeatureClassToFeatureClass_conversion(Jur, Output, "Jur")
    JurTable = Output + '\\Jur'

    print("Create Relationships")
    arcpy.CreateRelationshipClass_management(LocTable , UnitTable, Output+"\\Loc-Unit"         , "SIMPLE", "Unit Table"     , "Loc Table"         , "FORWARD", "ONE_TO_MANY", "NONE", fields.loc.ANO['name'], fields.loc.ANO     ['name'])
    #arcpy.CreateRelationshipClass_management(OutTable , UnitTable, Output+"\\Out-Unit"         , "SIMPLE", "Unit Table"     , "Out of State Table", "FORWARD", "ONE_TO_MANY", "NONE", fields.loc.ANO['name'], fields.loc.ANO     ['name'])
    arcpy.CreateRelationshipClass_management(UnitTable, OccTable , Output+"\\Unit-Occ"         , "SIMPLE", "Occ Table"      , "Unit Table"        , "FORWARD", "ONE_TO_MANY", "NONE", fields.unit.ID['name'], fields.unit.ID     ['name'])
    #arcpy.CreateRelationshipClass_management(LocTable , SecTable , Output+"\\PriCrash-SecTable", "SIMPLE", "Secondary Table", "Primary Crash"     , "NONE"   , "ONE_TO_MANY", "NONE", fields.loc.ANO['name'], fields.crash.PrmANO['name'])    
    #arcpy.CreateRelationshipClass_management(SecTable , LocTable , Output+"\\SecTable-SecCrash", "SIMPLE", "Secondary Crash", "Secondary Table"   , "NONE"   , "ONE_TO_ONE" , "NONE", fields.loc.ANO['name'], fields.loc.ANO     ['name'])    
    arcpy.CreateRelationshipClass_management(LocTable , JurTable , Output+"\\Loc-Jur"          , "SIMPLE", "Jur Table"      , "Loc Table"         , "NONE"   , "ONE_TO_MANY", "NONE", fields.loc.JUR['name'], fields.loc.JUR     ['name'])    
            
    print("Assign Domains")
    Domains     = {
    'GMET':{0:'Not Geocoded',
        5:'Milepost',
        6:'State Coordinate',
        7:'DD',
        8:'DMS',
        9:'Milepost and DMS'},
    'GCXY':{0:'Out of State',
        1:'Main Route Not Found',
        2:'Far From Main Route',
        9:'On Main Route'},
    'GCMP':{1:'Main Route Not Found',
       2:'Base Route Not Found',
       3:'Base Intersection Not Found',
       4:'False BDO',
       5:'Only Base Intersection',
       9:'Between BI and SI'},
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
    Assignments = [ {'Domain':fields.loc.GMET,'Assign':[{'Table':LocTable,'Fields':[fields.loc.GMET]}]},
                    {'Domain':fields.loc.GCXY,'Assign':[{'Table':LocTable,'Fields':[fields.loc.GCXY]}]},
                    {'Domain':fields.loc.GCMP,'Assign':[{'Table':LocTable,'Fields':[fields.loc.GCMP]}]},
                    {'Domain':fields.loc.CTY,'Assign':[{'Table':LocTable,'Fields':[fields.loc.CTY]}]},
                    {'Domain':fields.loc.RCT,'Assign':[{'Table':LocTable,'Fields':[fields.loc.RCT,fields.loc.BIR,fields.loc.SIC]}]},
                    {'Domain':fields.loc.RAI,'Assign':[{'Table':LocTable,'Fields':[fields.loc.RAI]}]},
                    {'Domain':fields.loc.DLR,'Assign':[{'Table':LocTable,'Fields':[fields.loc.DLR,fields.loc.ODR]},{'Table':UnitTable,'Fields':[fields.unit.DOT]}]},
                    {'Domain':fields.loc.ART,'Assign':[{'Table':LocTable,'Fields':[fields.loc.ART,fields.loc.BRA,fields.loc.SRA]}]},
                    {'Domain':fields.loc.BDI,'Assign':[{'Table':LocTable,'Fields':[fields.loc.BDI]}]},
                    {'Domain':fields.loc.DAY,'Assign':[{'Table':LocTable,'Fields':[fields.loc.DAY]}]},
                    {'Domain':fields.loc.ALC,'Assign':[{'Table':LocTable,'Fields':[fields.loc.ALC]}]},
                    {'Domain':fields.loc.WCC,'Assign':[{'Table':LocTable,'Fields':[fields.loc.WCC]}]},
                    {'Domain':fields.loc.RSC,'Assign':[{'Table':LocTable,'Fields':[fields.loc.RSC]}]},
                    {'Domain':fields.loc.AHC,'Assign':[{'Table':LocTable,'Fields':[fields.loc.AHC]}]},
                    {'Domain':fields.loc.TWAY,'Assign':[{'Table':LocTable,'Fields':[fields.loc.TWAY]}]},
                    {'Domain':fields.loc.TCT,'Assign':[{'Table':LocTable,'Fields':[fields.loc.TCT]}]},
                    {'Domain':fields.loc.JCT,'Assign':[{'Table':LocTable,'Fields':[fields.loc.JCT]}]},
                    {'Domain':fields.loc.FHE,'Assign':[{'Table':LocTable,'Fields':[fields.loc.FHE]},{'Table':UnitTable,'Fields':[fields.unit.MHE,fields.unit.SOE1,fields.unit.SOE2,fields.unit.SOE3,fields.unit.SOE4]}]},
                    {'Domain':fields.loc.HEL,'Assign':[{'Table':LocTable,'Fields':[fields.loc.HEL]}]},
                    {'Domain':fields.loc.PRC,'Assign':[{'Table':LocTable,'Fields':[fields.loc.PRC,fields.loc.OCF1,fields.loc.OCF2,fields.loc.OCF3,fields.loc.OCF4]}]},
                    {'Domain':fields.loc.MAC,'Assign':[{'Table':LocTable,'Fields':[fields.loc.MAC]},{'Table':UnitTable,'Fields':[fields.unit.MAN]}]},
                    {'Domain':fields.loc.JUR,'Assign':[{'Table':LocTable,'Fields':[fields.loc.JUR]}]},
                    {'Domain':fields.loc.WZN,'Assign':[{'Table':LocTable,'Fields':[fields.loc.WZN,fields.loc.WPR]},{'Table':UnitTable,'Fields':[fields.unit.CTA]},{'Table':OccTable,'Fields':[fields.occ.MHI]}]},
                    {'Domain':fields.loc.WZT,'Assign':[{'Table':LocTable,'Fields':[fields.loc.WZT]}]},
                    {'Domain':fields.loc.WZL,'Assign':[{'Table':LocTable,'Fields':[fields.loc.WZL]}]},
                    {'Domain':fields.unit.UTC,'Assign':[{'Table':UnitTable,'Fields':[fields.unit.UTC]}]},
                    {'Domain':fields.unit.DSEX,'Assign':[{'Table':UnitTable,'Fields':[fields.unit.DSEX]},{'Table':OccTable,'Fields':[fields.occ.OSEX]}]},
                    {'Domain':fields.unit.DRAC,'Assign':[{'Table':UnitTable,'Fields':[fields.unit.DRAC]},{'Table':OccTable,'Fields':[fields.occ.ORAC]}]},
                    {'Domain':fields.unit.VUC,'Assign':[{'Table':UnitTable,'Fields':[fields.unit.VUC]}]},
                    {'Domain':fields.unit.API,'Assign':[{'Table':UnitTable,'Fields':[fields.unit.API]}]},
                    {'Domain':fields.unit.DTG,'Assign':[{'Table':UnitTable,'Fields':[fields.unit.DTG]}]},
                    {'Domain':fields.unit.DTT,'Assign':[{'Table':UnitTable,'Fields':[fields.unit.DTT]}]},
                    {'Domain':fields.unit.DTR,'Assign':[{'Table':UnitTable,'Fields':[fields.unit.DTR]}]},
                    {'Domain':fields.unit.UOR,'Assign':[{'Table':UnitTable,'Fields':[fields.unit.UOR]}]},
                    {'Domain':fields.unit.VAT,'Assign':[{'Table':UnitTable,'Fields':[fields.unit.VAT]}]},
                    {'Domain':fields.unit.VEW,'Assign':[{'Table':UnitTable,'Fields':[fields.unit.VEW]}]},
                    {'Domain':fields.unit.EDAM,'Assign':[{'Table':UnitTable,'Fields':[fields.unit.EDAM]}]},
                    {'Domain':fields.unit.MDA,'Assign':[{'Table':UnitTable,'Fields':[fields.unit.MDA,fields.unit.FDA]}]},
                    {'Domain':fields.occ.LAI,'Assign':[{'Table':OccTable,'Fields':[fields.occ.LAI]}]},
                    {'Domain':fields.occ.EJE,'Assign':[{'Table':OccTable,'Fields':[fields.occ.EJE]}]},
                    {'Domain':fields.occ.AIR,'Assign':[{'Table':OccTable,'Fields':[fields.occ.AIR]}]},
                    {'Domain':fields.occ.SWT,'Assign':[{'Table':OccTable,'Fields':[fields.occ.SWT]}]},
                    {'Domain':fields.occ.SEV,'Assign':[{'Table':OccTable,'Fields':[fields.occ.SEV]}]},
                    {'Domain':fields.occ.REU,'Assign':[{'Table':OccTable,'Fields':[fields.occ.REU]}]},
                    {'Domain':fields.occ.OSL,'Assign':[{'Table':OccTable,'Fields':[fields.occ.OSL]}]}
                    ]
    for rec in Assignments:
        try:
            print(" - " + rec['Domain']['name'])
            arcpy.CreateDomain_management(Output, rec['Domain']['name'], rec['Domain']['alias'], rec['Domain']['type'], "CODED")
            for code in Domains[rec['Domain']['name']].keys():
                arcpy.AddCodedValueToDomain_management(Output, rec['Domain']['name'], code, Domains[rec['Domain']['name']][code])
            for assign in rec['Assign']:
                for field in assign['Fields']:
                    arcpy.AssignDomainToField_management(assign['Table'], field['name'], rec['Domain']['name'])
        except Exception, e:
            tb = sys.exc_info()[2]
            print(field['name'])
            print("Line %i" % tb.tb_lineno)
            print(e.message)

    print('Add Representation')
    lyr = arcpy.mapping.Layer(Layer)
    lyr.replaceDataSource(LocTable,'NONE')
    try:
        arcpy.AddRepresentation_cartography(LocTable,"CrashType",fields.loc.Symbol['name'],"Override","STORE_CHANGE_AS_OVERRIDE",Layer,"ASSIGN")
    except Exception, e:
        print(e.message)
    #try:
    #    arcpy.CalculateField_management(L,'NU_Sev','!'+F_CT_Symbol['name']+'!',"PYTHON_9.3")
    #except Exception, e:
    #    print(e.message)
    #print('Comapct and Compress')
    #try:
    #    print('Compact the Database')
    #    arcpy.Compact_management(Output)
    #except Exception, e:
    #    print(e.message)
    #try:
    #    print('Compress the Database')
    #    arcpy.CompressFileGeodatabaseData_management (Output, "Lossless compression")
    #except Exception, e:
    #    print(e.message)
    print(" --> Done.")

def PedApprDirection(Loc,Unit):
    print('Pedestrian Approach Direction')
    print(' - Search Cursor({}): Finding UTC=41 ANOs'.format(Unit))
    anoL = []
    for r in arcpy.SearchCursor(Unit):
        if r.getValue('UTC')==41:
            anoL.append(r.getValue('ANO'))
    
    print(' - Search Cursor({}): Reading DOT for Selected ANOs'.format(Unit))
    Dir = {ano:{'VehDir':'','PedDir':'','PedAppr':''} for ano in anoL}
    for r in arcpy.SearchCursor(Unit):
        ano = r.getValue('ANO') 
        if ano in anoL:
            utc = r.getValue('UTC')
            if utc in [1,12,13,14,15,16,17,61,62,98,99]:
                Dir[ano]['VehDir'] = r.getValue('DOT')
            if utc in [41]:
                Dir[ano]['PedDir'] = r.getValue('DOT')

    print(' - Delete/Add Field (PedAppr) to {}'.format(Loc))
    arcpy.DeleteField_management(Loc,'PedAppr')
    arcpy.AddField_management(Loc,'PedAppr','SHORT')

    print(' - Update Cursor({}): Calculating Ped Appr Direction'.format(Loc))
    DirDict = {'NN':'S','SS':'S','WW':'S','EE':'S',
               'NS':'O','SN':'O','WE':'O','EW':'O',
               'NW':'R','SE':'R','WN':'L','ES':'L',
               'NE':'L','SW':'L','WS':'R','EN':'R'}
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
def AddObservedCrashes(Sites,Crashes,Buffer_Distance,OutputCrashes):
    arcpy.AddField_management(Sites,'RefFID','LONG')
    uc = arcpy.UpdateCursor(Sites)
    i = 1
    for r in uc:
        r.setValue('RefFID',i)
        uc.updateRow(r)
        i += 1
    del uc

    buf = common.CreateOutPath(MainFile= Sites,appendix='buf',Extension='')
    arcpy.Buffer_analysis (in_features = Sites,
                    out_feature_class = buf,
                    buffer_distance_or_field = Buffer_Distance, 
                    line_side = 'FULL', 
                    line_end_type = 'FLAT')
    arcpy.SpatialJoin_analysis (target_features = Crashes, 
                    join_features = buf, 
                    out_feature_class = OutputCrashes, 
                    join_operation = 'JOIN_ONE_TO_ONE', 
                    join_type = 'KEEP_COMMON', 
                    match_option = 'INTERSECT')
    arcpy.Delete_management(buf)
    OC = {r.getValue('RefFID'):{'TOT':0,'K':0,'A':0,'B':0,'C':0,'PDO':0} for r in arcpy.SearchCursor(Sites)}
    for r in arcpy.SearchCursor(OutputCrashes):
        fid = r.getValue('RefFID')
        OC[fid]['TOT'] += 1
        if r.getValue('Crash_injury_severity')=='Fatal Crash':
            OC[fid]['K'] += 1
        if r.getValue('Crash_injury_severity')=='A Injury Crash':
            OC[fid]['A'] += 1
        if r.getValue('Crash_injury_severity')=='B Injury Crash':
            OC[fid]['B'] += 1
        if r.getValue('Crash_injury_severity')=='C Injury Crash':
            OC[fid]['C'] += 1
        if r.getValue('Crash_injury_severity')=='No Injuries':
            OC[fid]['PDO'] += 1
        
    UC = arcpy.UpdateCursor(OutputCrashes)
    for r in UC:
        ct = r.getValue('Type_of_crash')
        ct_adj = ct.lower()
        ct_adj = ct_adj.replace('-', ' ')
        r.setValue('Type_of_crash',ct_adj)
        UC.updateRow(r)
    del UC    
        
    for fn in ['TOT_OC','K_OC','A_OC','B_OC','C_OC','PDO_OC']:
        if not fn in [f.name for f in arcpy.ListFields(Sites)]:
            arcpy.AddField_management(Sites,fn,'Double')

    uc = arcpy.UpdateCursor(Sites)
    i = 1
    for r in uc:
        fid = r.getValue('RefFID')
        r.setValue('TOT_OC',OC[fid]['TOT'])
        r.setValue('K_OC',OC[fid]['K'])
        r.setValue('A_OC',OC[fid]['A'])
        r.setValue('B_OC',OC[fid]['B'])
        r.setValue('C_OC',OC[fid]['C'])
        r.setValue('PDO_OC',OC[fid]['PDO'])
        uc.updateRow(r)
        i += 1
    del uc
    print('Total Observed Crashes: {}'.format(int(str(arcpy.GetCount_management(OutputCrashes)))))
def CON_AddObservedCrashes_Temporal(WDir,HSMPY_PATH,SitesList,Crashes,Title):
    import sys, os, arcpy, subprocess
    sys.path.append(HSMPY_PATH)

    pyFN = os.path.join(WDir , 'HSIP_' + str(Title) + '_ObsCrash.py')
    OutFile = open(pyFN, 'w')
    pyfile = """from time import gmtime, strftime
print(strftime("%Y-%m-%d %H:%M:%S"))
print("Observed Crashes")
import os, sys
import atexit
#atexit.register(raw_input, 'Press Enter to continue...')
HSMPY_PATH = r'{}'
SitesList = {}
Crashes = {}

sys.path.append(HSMPY_PATH) 
import hsmpy
import arcpy
for site in SitesList:
    print(site['Output'])
    hsmpy.crash.AddObservedCrashes(site['Input'],Crashes[site['year']],site['Buffer'],site['Output'])
print(strftime("%Y-%m-%d %H:%M:%S"))
""".format(HSMPY_PATH,SitesList,Crashes)
    OutFile.write(pyfile)
    OutFile.close()
    SubProcess = subprocess.Popen(
                [sys.executable, pyFN],
                shell=False,creationflags = subprocess.CREATE_NEW_CONSOLE)
    return(SubProcess)
    print(site['year'],int(str(arcpy.GetCount_management(SegFC))))