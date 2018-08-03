# Developed By Mahdi Rajabi mrajabi@clemson.edu
import os
import sys
import common
import fields
import fields_SC
import fields_IL
import datetime
import json
import arcpy
import args
import math
import pandas as pd
import numpy as np
from scipy import optimize
import re

def ExtractIntFromSeg(Segments,Intersections,Buffer,Output):
    #Output should be on a GDB not a shapefile
    SegFields = [f.name for f in arcpy.ListFields(Segments)]

    SelInt = common.CreateOutPath(MainFile=Output,appendix='SelInt',Extension='')
    arcpy.SpatialJoin_analysis(target_features = Intersections, 
                               join_features = Segments, 
                               out_feature_class = SelInt, 
                               join_operation = 'JOIN_ONE_TO_ONE', 
                               join_type = 'KEEP_COMMON', 
                               match_option = 'INTERSECT',
                               search_radius = Buffer)
    arcpy.DeleteField_management(SelInt,[f.name for f in arcpy.ListFields(SelInt) if not  f.required])

    SelIntBuf = common.CreateOutPath(MainFile=Output,appendix='SelIntBuf',Extension='')
    arcpy.Buffer_analysis(in_features = SelInt, 
                          out_feature_class = SelIntBuf, 
                          buffer_distance_or_field = str(Buffer) + ' Feet', 
                          line_side = 'FULL', 
                          line_end_type = 'FLAT')

    F2L = common.CreateOutPath(MainFile = Output,appendix='F2L',Extension='')
    arcpy.FeatureToLine_management (in_features = [Segments,SelIntBuf], 
                                    out_feature_class = F2L,attributes='ATTRIBUTES')
    
    F2LLayer = common.CreateOutLayer('F2LLayer')
    arcpy.MakeFeatureLayer_management(in_features = F2L,out_layer = F2LLayer)
    arcpy.SelectLayerByAttribute_management(in_layer_or_view = F2LLayer,
                                            selection_type = 'NEW_SELECTION',
                                            where_clause = "BUFF_DIST = 0")

    Seg1F = common.CreateOutPath(MainFile = Output,appendix='Seg1F',Extension='')
    arcpy.CopyFeatures_management(in_features=F2LLayer,out_feature_class=Seg1F)
    arcpy.DeleteField_management(Seg1F,[f.name for f in arcpy.ListFields(Seg1F) if not f.required and not f.name in SegFields])
    
    Selseg = common.CreateOutPath(MainFile=Output,appendix='SelSeg',Extension='')
    arcpy.SpatialJoin_analysis(target_features = Seg1F, 
                               join_features = SelIntBuf, 
                               out_feature_class = Selseg, 
                               join_operation = 'JOIN_ONE_TO_ONE', 
                               join_type = 'KEEP_ALL', 
                               match_option = 'WITHIN')
    
    SPJLayer = common.CreateOutLayer('SPJLayer')
    arcpy.MakeFeatureLayer_management(in_features = Selseg,out_layer = SPJLayer)
    arcpy.SelectLayerByAttribute_management(in_layer_or_view = SPJLayer,
                                            selection_type = 'NEW_SELECTION',
                                            where_clause = "Join_Count = 0 AND Shape_Length>528")

    arcpy.CopyFeatures_management(in_features=SPJLayer,out_feature_class=Output)
    arcpy.DeleteField_management(Output,[f.name for f in arcpy.ListFields(Output) if not f.required and not f.name in SegFields])

    arcpy.Delete_management(SelInt)    
    arcpy.Delete_management(SelIntBuf)    
    arcpy.Delete_management(F2L)    
    arcpy.Delete_management(F2LLayer)    
    arcpy.Delete_management(Seg1F)    
    arcpy.Delete_management(Selseg)    
    arcpy.Delete_management(SPJLayer)
def ImportRoadwayData(Input,Route,AttTable,Fields,Output,RouteID,BMP,EMP,XY_Tolerance):
    #Output should be on a GDB not a shapefile

    #Step 1: Create a route FC based on the input 
    Sites_Event_Table = common.CreateOutPath(MainFile=Output,appendix='EventTab',Extension='')
    arcpy.LocateFeaturesAlongRoutes_lr(in_features = Input, 
                                       in_routes = Route, 
                                       route_id_field = RouteID, 
                                       radius_or_tolerance = XY_Tolerance, 
                                       out_table = Sites_Event_Table, 
                                       out_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
                                       route_locations = "FIRST", 
                                       distance_field = "DISTANCE", 
                                       zero_length_events = "ZERO", 
                                       in_fields = "FIELDS", 
                                       m_direction_offsetting = "M_DIRECTON")
    Sites_Event_Layer = common.CreateOutLayer('EventLayer')
    arcpy.MakeRouteEventLayer_lr(in_routes = Route, 
                                 route_id_field = RouteID, 
                                 in_table = Sites_Event_Table, 
                                 in_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
                                 out_layer = Sites_Event_Layer, 
                                 add_error_field="NO_ERROR_FIELD")
    
    Sites_Routes = common.CreateOutPath(MainFile=Output,appendix='route',Extension='')
    arcpy.CopyFeatures_management(in_features = Sites_Event_Layer,
                                  out_feature_class = Sites_Routes)
    
    IRIS_Diss = common.CreateOutPath(MainFile=Output,appendix='diss',Extension='')
    arcpy.DissolveRouteEvents_lr(in_events = AttTable, 
                                 in_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
                                 dissolve_field = ';'.join(Fields), 
                                 out_table = IRIS_Diss, 
                                 out_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
                                 dissolve_type="DISSOLVE", 
                                 build_index="INDEX")    
    
    Overlay_Event_Table1 = common.CreateOutPath(MainFile=Output,appendix='OverlayTab1',Extension='')
    arcpy.OverlayRouteEvents_lr(in_table = IRIS_Diss, 
                                in_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
                                overlay_table = Sites_Event_Table, 
                                overlay_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
                                overlay_type = "INTERSECT", 
                                out_table = Overlay_Event_Table1, 
                                out_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
                                zero_length_events = "NO_ZERO", 
                                in_fields = "FIELDS", 
                                build_index="INDEX")    
    
    Overlay_Event_Layer = common.CreateOutLayer('OverlayEventLayer')
    arcpy.MakeRouteEventLayer_lr(in_routes = Route, 
                                 route_id_field = RouteID, 
                                 in_table = Overlay_Event_Table1, 
                                 in_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
                                 out_layer = Overlay_Event_Layer, 
                                 offset_field = "", 
                                 add_error_field = "ERROR_FIELD")     
    
    Sites_segs1 = common.CreateOutPath(MainFile=Output,appendix='seg1',Extension='')
    arcpy.CopyFeatures_management(in_features = Overlay_Event_Layer,
                                  out_feature_class = Sites_segs1)


    #Curves_Table = common.CreateOutPath(MainFile=Output,appendix='curves',Extension='')
    #ExtractCurves(inp=Sites_segs1,IDField=RouteID,RMax=5280,RMin=10,DegMin=2,desd=1000,LenMin=1000,out=Curves_Table)

    #Overlay_Event_Table2 = common.CreateOutPath(MainFile=Output,appendix='OverlayTab2',Extension='')
    #arcpy.OverlayRouteEvents_lr(in_table = Overlay_Event_Table1, 
    #                            in_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
    #                            overlay_table = Curves_Table, 
    #                            overlay_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
    #                            overlay_type = "UNION", 
    #                            out_table = Overlay_Event_Table2, 
    #                            out_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
    #                            zero_length_events = "NO_ZERO", 
    #                            in_fields = "FIELDS", 
    #                            build_index="INDEX") 

    #Overlay_Event_Layer2 = common.CreateOutLayer('OverlayEventLayer2')
    #arcpy.MakeRouteEventLayer_lr(in_routes = Route, 
    #                             route_id_field = RouteID, 
    #                             in_table = Overlay_Event_Table2, 
    #                             in_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
    #                             out_layer = Overlay_Event_Layer2, 
    #                             offset_field = "", 
    #                             add_error_field = "ERROR_FIELD") 
    
    Sort = common.CreateOutPath(MainFile=Output,appendix='sort',Extension='')
    arcpy.Sort_management(in_dataset = Sites_segs1,
                          out_dataset = Sort,
                          sort_field = ';'.join([RouteID,BMP,EMP]))
    Final_Layer = common.CreateOutLayer('FinalLayer')
    
    arcpy.MakeFeatureLayer_management(in_features=Sort,out_layer=Final_Layer)
    arcpy.SelectLayerByAttribute_management(in_layer_or_view = Final_Layer,
                                            selection_type = 'NEW_SELECTION',
                                            where_clause = "Shape_Length > 52")
    
    arcpy.Delete_management(Output)
    arcpy.MultipartToSinglepart_management(in_features=Final_Layer, 
                                           out_feature_class=Output)    
    arcpy.DeleteField_management(Output,'ORIG_FID')
    FL = [f.name for f in arcpy.ListFields(Output) if f.name != arcpy.Describe(Output).OIDFieldName]
    arcpy.DeleteIdentical_management(in_dataset = Output, 
                                     fields = ';'.join(FL), 
                                     xy_tolerance = "", 
                                     z_tolerance = "0")


    arcpy.Delete_management(Sites_Event_Table)
    arcpy.Delete_management(Sites_Event_Layer)
    arcpy.Delete_management(Sites_Routes)
    arcpy.Delete_management(IRIS_Diss)
    arcpy.Delete_management(Overlay_Event_Table1)
    arcpy.Delete_management(Overlay_Event_Layer)
    arcpy.Delete_management(Sites_segs1)
    #arcpy.Delete_management(Curves_Table)
    #arcpy.Delete_management(Overlay_Event_Table2)
    #arcpy.Delete_management(Overlay_Event_Layer2)
    arcpy.Delete_management(Sort)
    arcpy.Delete_management(Final_Layer)
def CreateRouteEventLayer(Sites_Routes,AttTable,RouteID,BMP,EMP,Fields,Output):
    IRIS_Diss = common.CreateOutPath(MainFile=Output,appendix='diss',Extension='')
    arcpy.DissolveRouteEvents_lr(in_events = AttTable, 
                                 in_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
                                 dissolve_field = ';'.join(Fields), 
                                 out_table = IRIS_Diss, 
                                 out_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
                                 dissolve_type="DISSOLVE", 
                                 build_index="INDEX")    
    
    Overlay_Event_Layer = common.CreateOutLayer('OverlayEventLayer')
    arcpy.MakeRouteEventLayer_lr(in_routes = Sites_Routes, 
                                 route_id_field = RouteID, 
                                 in_table = IRIS_Diss, 
                                 in_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
                                 out_layer = Overlay_Event_Layer, 
                                 offset_field = "", 
                                 add_error_field = "ERROR_FIELD") 

    Sort = common.CreateOutPath(MainFile=Output,appendix='sort',Extension='')
    arcpy.Sort_management(in_dataset = Overlay_Event_Layer,
                          out_dataset = Sort,
                          sort_field = ';'.join([RouteID,BMP,EMP]))
    Final_Layer = common.CreateOutLayer('FinalLayer')
    
    arcpy.MakeFeatureLayer_management(in_features=Sort,out_layer=Final_Layer)
    arcpy.SelectLayerByAttribute_management(in_layer_or_view = Final_Layer,
                                            selection_type = 'NEW_SELECTION',
                                            where_clause = "Shape_Length > 0")
    arcpy.Delete_management(Output)
    arcpy.CopyFeatures_management(in_features=Final_Layer,out_feature_class=Output)

    arcpy.Delete_management(IRIS_Diss)
    arcpy.Delete_management(Overlay_Event_Layer)
    arcpy.Delete_management(Sort)
    arcpy.Delete_management(Final_Layer)
def PrintSegSummary(Input,Title = ''):
    ts = int(str(arcpy.GetCount_management(Input)))
    ml = sum([r.getValue('Shape').length for r in arcpy.SearchCursor(Input)])/5280
    if 'AADT' in [f.name for f in arcpy.ListFields(Input)]:
        aa = sum([r.getValue('AADT') for r in arcpy.SearchCursor(Input)])/max(ts,1)
        print('{}: Total Segments: {}, Mileage: {:0.2f}, Average AADT {:0.2f}'.format(Title,ts,ml,aa)) 
    else:
        print('{}: Total Segments: {}, Mileage: {:0.2f}'.format(Title,ts,ml)) 
def PrintIntSummary(InputPoints,InputTable,Title = ''):
    ts = int(str(arcpy.GetCount_management(InputPoints)))
    tr = int(str(arcpy.GetCount_management(InputTable)))
    if 'AADT' in [f.name for f in arcpy.ListFields(InputTable)]:
        aa = sum([r.getValue('AADT') for r in arcpy.SearchCursor(InputTable)])/max(tr,1)
        print('{}: Total Points: {}, Total Legs: {}, Average AADT {:0.2f}'.format(Title,ts,tr,aa)) 
    else:
        print('{}: Total Points: {}, Total Legs: {}'.format(Title,ts,tr)) 
def ExtractCurves(inp,IDField,DegMin,RMax,RMin,LenMin,desd,out):
    def RemoveOverlap(Curves):
        import pandas as pd
        CDF = pd.DataFrame(columns=['BMP','EMP','Radius','Cen_X','Cen_Y'])
        CDF['BMP'] = [cur[0] for cur in Curves]
        CDF['EMP'] = [cur[1] for cur in Curves]
        CDF['Radius'] = [cur[2] for cur in Curves]
        CDF['Cen_X'] = [cur[3] for cur in Curves]
        CDF['Cen_Y'] = [cur[4] for cur in Curves]    
        for i in range(1,len(CDF)):
            if CDF.loc[i]['BMP']<CDF.loc[i-1]['EMP']:
                ave = (CDF.loc[i]['BMP']+CDF.loc[i-1]['EMP'])/2 
                CDF.loc[i]['BMP'] = ave
                CDF.loc[i-1]['EMP'] = ave
        return(CDF)
    def FindClusters(CD,DegMin):
        flag = False
        j = 0
        R = []
        T = []
        for i in range(len(CD['Radius'])):
            if abs(CD['Radius'][i]) > DegMin:
                T.append(int(math.copysign(1,CD['Radius'][i])))
                if not flag:
                    flag = True
                    j += 1
                else:
                    if CD['Radius'][i]*CD['Radius'][i-1]<=0:
                        j =+ 1
                        flag = True
            else:
                T.append(0)
                if flag:
                    j += 1
                    flag = False
            R.append(j)
        return({'CN':R,'CT':T})
    def FindRadius(Shape,DegMin,MinLen):
        import json
        import pandas as pd
        CD = HorCurvature(Shape)
        CL = FindClusters(CD,DegMin)
        l = json.loads(Shape.JSON)['paths'][0]
        DF = pd.DataFrame()
        DF['X'] = [i[0] for i in l]
        DF['Y'] = [i[1] for i in l]
        DF['Milepost'] = [i[3] for i in l]
        CD = HorCurvature(Shape)
        CL = FindClusters(CD,DegMin)
        DF['Heading Angle'] = CD['Radius']
        DF['Cluster Number'] = CL['CN']
        DF['Cluster Type'] = CL['CT']
        DF['Cluster Type'] = MergeCurves(DF,MinLen)
        Radius = []
        Cen_X = []
        Cen_Y = []
        Points = []
        kr = [-1]
        Curves = []
        for i in range(len(DF)):
            if not i in kr:
                if DF.loc[i]['Cluster Type'] == 0:
                    Cen_X.append(0)
                    Cen_Y.append(0)
                    Radius.append(0)
                    Points.append(str(i))
                else:
                    cl = [[DF.loc[i-1]['X'],DF.loc[i-1]['Y']]]
                    j = i
                    while DF.loc[j]['Cluster Type']==DF.loc[i]['Cluster Type']:
                        cl.append([DF.loc[j]['X'],DF.loc[j]['Y']])
                        j += 1
                    cl.append([DF.loc[j]['X'],DF.loc[j]['Y']])
                    CF = CircleFitting(cl)
                    Curves.append([
                        DF.loc[i-1]['Milepost'],
                        DF.loc[j]['Milepost'],
                        math.copysign(CF['Radius'],DF.loc[i]['Cluster Type']),
                        CF['Center'][0],
                        CF['Center'][1]
                    ])
                    kr = range(i,j)
                    for k in kr:
                            Radius.append(math.copysign(CF['Radius'],DF.loc[i]['Cluster Type']))
                            Cen_X.append(CF['Center'][0])
                            Cen_Y.append(CF['Center'][1])
                            Points.append(';'.join([str(t) for t in range(i-1,j+1)]))
                    
        DF['Radius'] = Radius
        DF['Center_X'] = Cen_X
        DF['Center_Y'] = Cen_Y
        DF['Points'] = Points
        CDF = RemoveOverlap(Curves)
        Res = RemoveSharpTurns(DF)
        DF['Cluster Type'] = Res[0]
        CDF = CDF.loc[[k for k in list(CDF.index) if not k in Res[1]]]
        return([DF,CDF])
    def MergeCurves(DF,MinLen):
        CT = [0]
        for i in range(1,len(DF)-1):
            if DF.loc[i]['Cluster Type'] == 0:
                if DF.loc[i-1]['Cluster Type'] == DF.loc[i+1]['Cluster Type']:
                    if (DF.loc[i+1]['Milepost']-DF.loc[i-1]['Milepost']) * 5280 <MinLen:
                        CT.append(DF.loc[i-1]['Cluster Type'])
                    else:
                        CT.append(DF.loc[i]['Cluster Type'])
                else:
                    CT.append(DF.loc[i]['Cluster Type'])
            else:
                CT.append(DF.loc[i]['Cluster Type'])
        CT.append(0)
        return(CT)
    def AddMidPoints(l,desd):
        pntl = [arcpy.Point(X = l[0][0],Y=l[0][1],Z=0,M=l[0][3])]
        for p in l[1:]:
            curpnt = arcpy.Point(X = p[0],Y=p[1],Z=0,M=p[3])
            curd = arcpy.PointGeometry(pntl[-1]).distanceTo(curpnt)
            if curd <= desd:
                pntl.append(curpnt)
            else:
                n = int(curd/desd)+1
                delta = curd/n
                pl = arcpy.Polyline(arcpy.Array([pntl[-1],curpnt]))
                for j in range(1,n):
                    if j*delta<curd:
                        midpg = pl.positionAlongLine(j*delta)
                        m = float((curpnt.M - pntl[-1].M))/n*j + pntl[-1].M
                        midp = arcpy.Point(midpg.firstPoint.X,midpg.firstPoint.Y,0,m)
                        pntl.append(midp)
                pntl.append(curpnt)
        return(pntl)
    def FindCurves(pl,DegMin,RMax,RMin,LenMin,desd):
        import json
        Curve = []
        pntl = json.loads(pl.JSON)['paths'][0]
        CD = HorCurvature(pl)
        flag = False
        for i in range(len(CD['Radius'])):
            if abs(CD['Radius'][i]) > DegMin:
                if not flag:
                    start = CD['Milepost'][i-1]
                    startSign =  math.copysign(1,CD['Radius'][i])
                    Dis = 0
                    flag = True
                    R = [pntl[i-1],pntl[i]]
                else:
                    if math.copysign(1,CD['Radius'][i])==startSign:
                        Dis = 0
                        endi = i
                        R.append(pntl[i])
                    else:
                        if Dis > 0:
                            end = CD['Milepost'][endi]
                            R = [r for r in R if r[3]<=end]
                            cirD = CircleFitting(R)
                            cirD['Radius'] = math.copysign(cirD['Radius'],CD['Radius'][endi-1])
                            if end<start:
                                print(start,end)
                            if abs(cirD['Radius'])<RMax and abs(cirD['Radius'])>RMin and (end-start)>LenMin:
                                Curve.append([start,end,cirD['Radius'],cirD['Center'][0],cirD['Center'][1]])
                            start = end
                            Dis = 0
                            flag = False
                            i=endi
                            R = []
                        else:
                            end = (CD['Milepost'][i-1] + CD['Milepost'][i])/2.0
                            R.append(pntl[i])
                            cirD = CircleFitting(R)
                            cirD['Radius'] = math.copysign(cirD['Radius'],CD['Radius'][i-1])
                            if end<start:
                                print(start,end)
                            if abs(cirD['Radius'])<RMax and abs(cirD['Radius'])>RMin and (end-start)>LenMin:
                                Curve.append([start,end,cirD['Radius'],cirD['Center'][0],cirD['Center'][1]])
                            start = end
                            Dis = 0
                            flag = True
                            R = [pntl[i-1],pntl[i]]
            else:
                if flag:
                    if Dis == 0:
                        endi = i
                    Dis += (CD['Milepost'][i] - CD['Milepost'][i-1])
                    if Dis>float(desd)/5280.0 or i==len(CD['Milepost'])-1:
                        end = CD['Milepost'][endi]
                        R.append(pntl[i])
                        R = [r for r in R if r[3]<=end]
                        if len(R)>=3:
                            cirD = CircleFitting(R)
                            cirD['Radius'] = math.copysign(cirD['Radius'],CD['Radius'][endi-1])
                            if end<start:
                                print(start,end)
                            if abs(cirD['Radius'])<RMax and abs(cirD['Radius'])>RMin and (end-start)>LenMin:
                                Curve.append([start,end,cirD['Radius'],cirD['Center'][0],cirD['Center'][1]])
                        flag = False
                        R = []
                        i=endi
                    else:
                        R.append(pntl[i])
        return(Curve)
    def CircleFitting(l):
        from scipy import optimize
        import numpy
        def calc_R(xc, yc):
            return numpy.sqrt((x-xc)**2 + (y-yc)**2)
        def f_2(c):
            Ri = calc_R(*c)
            return Ri - Ri.mean()
        x = numpy.array([i[0] for i in l])
        y = numpy.array([i[1] for i in l])
        x_m = sum(x)/max(len(x),1)
        y_m = sum(y)/max(len(y),1)
        center_estimate = x_m, y_m
        center_2, ier = optimize.leastsq(f_2, center_estimate)
        xc_2, yc_2 = center_2
        Ri_2       = calc_R(*center_2)
        R_2        = Ri_2.mean()
        residu_2   = sum((Ri_2 - R_2)**2)
        return({'Radius':R_2,'Center':[xc_2, yc_2]})
    def HorCurvature(Shape):
        import re
        import math
        import arcpy
        from math import acos
        from numpy.linalg import norm
        import numpy
        import json
        Inf = 52800 
        def findangle(p1, p2,p3):
            A = np.array(p1)
            B = np.array(p2)
            C = np.array(p3)
            v1 = B - A
            v2 = C - B
            def unit_vector(vector):
                return vector / np.linalg.norm(vector)
            v1_u = unit_vector(v1)
            v2_u = unit_vector(v2)
            return(np.degrees(np.arctan2(v2_u[1], v2_u[0])-np.arctan2(v1_u[1], v1_u[0])))
        def Radius(P1,P2,P3):
            Inf = 52800
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
                R = min(R,Inf)
                R = math.copysign(R,m2)
            elif y2==y3 and y1<>y2:
                m1 = -(x2-x1)/(y2-y1)
                xm1 = (x1+x2)/2
                ym1 = (y1+y2)/2
                xm2 = (x3+x2)/2
                ym2 = (y3+y2)/2
                xc = xm2
                yc = m1*(xc-xm1)+ym1
                R  = math.sqrt((xc-x1)**2+(yc-y1)**2)
                R = min(R,Inf)
                R = math.copysign(R,-m1)
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
                        R = min(R,Inf)
                        R = math.copysign(R,m2-m1)
            return(min(R,Inf))
        def Length(P1,P2):
            return(math.sqrt((P2[0]-P1[0])**2+(P2[1]-P1[1])**2))
        Vertices = json.loads(Shape.JSON)['paths'][0]
        R = [0]
        M = [Vertices[0][3]]
        L = Shape.length
        for i in range(2,len(Vertices)):
            l1 = Length(Vertices[i-2],Vertices[i-1])
            l2 = Length(Vertices[i-1],Vertices[i  ])
            #R.append(Radius(Vertices[i-2],Vertices[i-1],Vertices[i]))
            R.append(findangle(Vertices[i-2],Vertices[i-1],Vertices[i]))
            M.append(Vertices[i-1][3])
        R.append(0)
        M.append(Vertices[-1][3])
        return({'Radius':R,'Milepost':M})
    def progressBar(value, endvalue, bar_length=20):
        percent = float(value) / endvalue
        sys.stdout.write("\r{}%".format(int(round(percent * 100))))
        sys.stdout.flush()
    def RemoveSharpTurns(DF):
        j = -1
        pDict = {}
        rmcurve = []
        ct = []
        for i in range(0,len(DF)):
            Points = DF.loc[i]['Points'].split(';')
            if len(Points)>1 and not DF.loc[i]['Points'] in pDict.keys():
                j +=  1
                pDict.update({DF.loc[i]['Points']:0})
            if len(Points)>=3:
                Points = Points[1:-1]
                b = int(Points[0])
                e = int(Points[len(Points)-1])
                l = DF.loc[e]['Milepost'] - DF.loc[b]['Milepost']
                ha = list(DF.loc[[int(p) for p in Points]]['Heading Angle'])
                ha = abs(sum(ha)/len(ha))
                if l<0.03 and ha>=15:
                    rmcurve.append(j)
                    ct.append(2)
                else:
                    ct.append(DF.loc[i]['Cluster Type'])
            else:
                ct.append(DF.loc[i]['Cluster Type'])
        return([ct,rmcurve])
    #inp = sys.argv[1]
    #IDField = sys.argv[2]
    #desd = sys.argv[3]
    #DegMin = sys.argv[4]
    #RMax= sys.argv[5]
    #RMin= sys.argv[6]
    #LenMin= sys.argv[7]
    #out = sys.argv[3]
    #DegMin=2
    #RMax=5280*3
    #RMin=50
    #LenMin=100/5280
    #desd = 250

    arcpy.CreateTable_management(out_path=os.path.dirname(out),out_name=os.path.basename(out))
    arcpy.AddField_management(out,IDField,'TEXT')
    arcpy.AddField_management(out,'BEG_STA','DOUBLE')
    arcpy.AddField_management(out,'END_STA','DOUBLE')
    arcpy.AddField_management(out,'Radius','DOUBLE')
    arcpy.AddField_management(out,'CurveLen','DOUBLE')
    arcpy.AddField_management(out,'Center_X','DOUBLE')
    arcpy.AddField_management(out,'Center_Y','DOUBLE')
    arcpy.AddField_management(out,'CMF_CH10','DOUBLE')
    arcpy.AddField_management(out,'CMF_CH18','DOUBLE')
    OID = arcpy.Describe(inp).OIDFieldName
    INV = {r.getValue(OID):{'INV':r.getValue(IDField),'Shape':r.getValue('Shape')} for r in arcpy.SearchCursor(inp)}
    IC = arcpy.InsertCursor(out)
    arcpy.SetProgressor("step", "Finding Curves...",0, len(INV),1)
    k = INV.keys()
    k.sort()
    for inv in k:
        leng = 0
        try:
            l = json.loads(INV[inv]['Shape'].JSON)['paths'][0]
            leng = INV[inv]['Shape'].length/5280
        except:
            l = []
        #if not None in [p[3] for p in l]:
        if len(l)>2 and leng>=0.3:
            pntl = AddMidPoints(l,desd) 
            a = arcpy.Array(pntl)
            pl = arcpy.Polyline(a,arcpy.Describe(inp).spatialReference,True,True)
            #Curve = FindCurves(pl,DegMin,RMax,RMin,LenMin,desd)
            Curve = FindRadius(pl,DegMin,LenMin)[1]
            for i,cur in Curve.iterrows():
                R = abs(cur['Radius'])
                L = cur['EMP']-cur['BMP']
                if L<100.0/5280.0:
                    L = 100.0/5280.0
                if R<100:
                    R = 100
                CMF1 = (1.55*L+80.2/R)/(1.55*L)
                if CMF1<1:CMF1 =1
                CMF2 = 1 + 0.0626*(5730.0/R)**2
                if CMF2<1:CMF2 =1
                #if abs(cur['Radius'])<RMax and abs(cur['Radius'])<RMin:
                if min([CMF1,CMF2])>1.001 and L>0.2:
                
                    r = IC.newRow()
                    r.setValue(IDField,INV[inv]['INV'])
                    r.setValue('BEG_STA',cur['BMP'])
                    r.setValue('END_STA',cur['EMP'])
                    r.setValue('Radius',cur['Radius'])
                    r.setValue('CurveLen',cur['EMP']-cur['BMP'])
                    r.setValue('Center_X',cur['Cen_X'])
                    r.setValue('Center_Y',cur['Cen_Y'])
                    r.setValue('CMF_CH10',CMF1)
                    r.setValue('CMF_CH18',CMF2)
                    IC.insertRow(r)
        arcpy.SetProgressorPosition(INV.keys().index(inv))
        progressBar(INV.keys().index(inv),len(INV))
    del IC
def ImportIntAtt(Intersections,TrafficControl,Routes,RouteID,BMP,EMP,AttTable,Fields,Output,OutputTable):
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
    
    Buffer = "80 Feet"
    Tolerance = "10 Feet"
    Int = common.CreateOutPath(MainFile=Output,appendix='Int',Extension='')
    arcpy.Intersect_analysis(
        in_features = Routes,
        out_feature_class = Int, 
        join_attributes = "ALL", 
        cluster_tolerance = "-1 Unknown", 
        output_type = "POINT")

    SPJ = common.CreateOutPath(MainFile=Output,appendix='SPJ',Extension='')
    arcpy.SpatialJoin_analysis(
        target_features = Int, 
        join_features = Intersections, 
        out_feature_class = SPJ, 
        join_operation = "JOIN_ONE_TO_ONE", 
        join_type = "KEEP_COMMON", 
        match_option = "CLOSEST", 
        search_radius = Buffer, 
        distance_field_name = "")

    arcpy.DeleteIdentical_management(
        in_dataset = SPJ, 
        fields = arcpy.Describe(SPJ).ShapeFieldName, 
        xy_tolerance = "", 
        z_tolerance = "0")

    OrgFields = [f.name for f in arcpy.ListFields(Intersections)]
    arcpy.DeleteField_management(SPJ,[f.name for f in arcpy.ListFields(SPJ) if not f.required and not f.name in OrgFields])

    arcpy.SpatialJoin_analysis(
        target_features = SPJ, 
        join_features = TrafficControl, 
        out_feature_class = Output, 
        join_operation = "JOIN_ONE_TO_ONE", 
        join_type = "KEEP_COMMON", 
        match_option = "CLOSEST", 
        search_radius = Buffer, 
        distance_field_name = "")

    OrgFields.extend(['TRAF_CONT','LEG_COUNT','PeerGroup_CH2M_TJM'])
    arcpy.DeleteField_management(Output,[f.name for f in arcpy.ListFields(Output) if not f.required and not f.name in OrgFields])

    EventTable = common.CreateOutPath(MainFile=Output,appendix='EventTable',Extension='')
    arcpy.LocateFeaturesAlongRoutes_lr(
        in_features                = Output, 
        in_routes                = Routes, 
        route_id_field            = RouteID, 
        radius_or_tolerance        = Tolerance, 
        out_table                = EventTable, 
        out_event_properties    = " ".join([RouteID, "POINT", "MP"]),
        route_locations            = "ALL", 
        in_fields                = "FIELDS", 
        m_direction_offsetting    = "M_DIRECTON"
        )

    # Milepost Correction
    EMPDict = {r.getValue('INVENTORY'):r.getValue('Shape').lastPoint.M for r in arcpy.SearchCursor(Routes)}
    r = 0 
    uc = arcpy.UpdateCursor(EventTable)
    for r in uc:
        inv = r.getValue('INVENTORY')
        MP = r.getValue('MP')
        if MP<0:
            r.setValue('MP',0)
            uc.updateRow(r)
        if MP>EMPDict[inv]:
            r.setValue('MP',EMPDict[inv])
            uc.updateRow(r)
    del uc, r

    AllF = [f.name for f in arcpy.ListFields(AttTable)]
    MF = [f for f in Fields if not f in AllF]
    if not MF == []:
        print(str(MF) + ' not found in ' + AttTable)
    IRIS_Diss = common.CreateOutPath(MainFile=Output,appendix='diss',Extension='')
    arcpy.DissolveRouteEvents_lr(
        in_events = AttTable, 
        in_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
        dissolve_field = ';'.join(Fields), 
        out_table = IRIS_Diss, 
        out_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
        dissolve_type="DISSOLVE", 
        build_index="INDEX"
        )

    arcpy.OverlayRouteEvents_lr(
        in_table = EventTable , 
        in_event_properties = ' '.join([RouteID,'POINT','MP']), 
        overlay_table = IRIS_Diss, 
        overlay_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
        overlay_type = "INTERSECT", 
        out_table = OutputTable, 
        out_event_properties = ' '.join([RouteID,'POINT','MP']),  
        in_fields = "FIELDS", 
        build_index="INDEX"
        ) 
    
    common.AddField(Output, [
        fields_SC.intr.AADT_Major,
        fields_SC.intr.AADT_Minor,
        fields_SC.crash.ABuffer,
        fields_SC.crash.BBuffer
        ])

    arcpy.AddField_management(OutputTable,'ApprType','TEXT')
    #arcpy.AddField_management(OutputTable,'ApprDeg','Double')
    Approach = {r.getValue('SiteID'):[] for r in arcpy.SearchCursor(Output)}

    OID = arcpy.Describe(OutputTable).OIDFieldName
    for r in arcpy.SearchCursor(OutputTable):
        k = r.getValue('SiteID')
        if k in Approach.keys():
            Approach[k].append({
                'OID':r.getValue(OID),
                'INV':r.getValue('INVENTORY'),
                'AADT':common.GetIntVal(r,'AADT'),
                'Lanes':common.GetIntVal(r,'LNS',2),
                'Urban':r.getValue('URBAN'),
                'SurfWid':common.GetFloatVal(r,'SURF_WTH',24),
                'MedWid':common.GetFloatVal(r,'MED_WTH')
                })
    for k in Approach.keys():
        AADT = [i['AADT'] for i in Approach[k]]
        INV = [i['INV'] for i in Approach[k]]
        major_i = AADT.index(max(AADT))
        major_inv = INV[major_i]
        for i,appr in enumerate(Approach[k]):
            if appr['AADT'] == max(AADT) or appr['INV']==major_inv:
                Approach[k][i].update({'ApprType':'Major'})
            else:
                Approach[k][i].update({'ApprType':'Minor'})

    UC = arcpy.UpdateCursor(OutputTable)
    for r in UC:
        k = r.getValue('SiteID')
        o = r.getValue(OID)
        Type = ''
        for appr in Approach[k]:
            if appr['OID'] == o:
                Type = appr['ApprType']
        r.setValue('ApprType',Type)

        UC.updateRow(r)
                    
    UC = arcpy.UpdateCursor(Output)
    for r in UC:
        k = r.getValue('SiteID')
        try:r.setValue(fields_SC.intr.AADT_Major['name'],max([appr['AADT'] for appr in Approach[k] if appr['ApprType']=='Major']))
        except:r.setValue(fields_SC.intr.AADT_Major['name'],0)
        try:r.setValue(fields_SC.intr.AADT_Minor['name'],max([appr['AADT'] for appr in Approach[k] if appr['ApprType']=='Minor']))
        except:r.setValue(fields_SC.intr.AADT_Minor['name'],0)
        try:W_Major = max([appr['SurfWid'] + appr['MedWid'] for appr in Approach[k] if appr['ApprType']=='Major'])
        except:W_Major = 24
        try:W_Minor = max([appr['SurfWid'] + appr['MedWid'] for appr in Approach[k] if appr['ApprType']=='Minor'])
        except:W_Minor = 24
        ABuffer = max(1.2 * (W_Major**2+W_Minor**2) ** 0.5,50)
        r.setValue(fields_SC.crash.ABuffer['name'],ABuffer)
        r.setValue(fields_SC.crash.BBuffer['name'],max(ABuffer,250))
        AADT = [i['AADT'] for i in Approach[k]]
        major_i = AADT.index(max(AADT))
        LaneMajor = [i['Lanes'] for i in Approach[k]][0]
        UC.updateRow(r)

    arcpy.Delete_management(Int)
    arcpy.Delete_management(EventTable)
    arcpy.Delete_management(SPJ)
    arcpy.Delete_management(IRIS_Diss)
def CON_ExtractCurves(WDir,HSMPY_PATH,IRIS_Routes,IRIS_Table,Curve_Table,CurveLayer,Overlay_Table,OverlayLayer,Title):
    import sys, os, subprocess

    pyFN = os.path.join(WDir , 'CurveExtract_' + str(Title) + '.py')
    OutFile = open(pyFN, 'w')
    pyfile = """print("Curve Extract")
from time import gmtime, strftime
print(strftime("%Y-%m-%d %H:%M:%S"))
import os, sys
import atexit
#atexit.register(raw_input, 'Press Enter to continue...')
HSMPY_PATH = r'{}'
IRIS_Routes = r"{}"
IRIS_Table = r"{}"
Curve_Table = r"{}"
CurveLayer = r"{}"
Overlay_Table = r"{}"
OverlayLayer = r"{}"

sys.path.append(HSMPY_PATH)
import arcpy
import hsmpy

print(Curve_Table)
hsmpy.network.ExtractCurves(inp=IRIS_Routes,IDField='INVENTORY',DegMin=2,RMax=5280,RMin=10,LenMin=1000,desd=1000, out=Curve_Table)
print()

F = [f.name for f in arcpy.ListFields(Curve_Table) if not f.required and not f.name in ['INVENTORY','BEG_STA','END_STA']]
print(CurveLayer)
hsmpy.network.CreateRouteEventLayer(Sites_Routes=IRIS_Routes,AttTable=Curve_Table,BMP='BEG_STA',EMP='END_STA',RouteID='INVENTORY',Fields=F,Output=CurveLayer)

print(Overlay_Table)
arcpy.OverlayRouteEvents_lr(in_table = IRIS_Table, 
                                in_event_properties = ' '.join(['INVENTORY','LINE','BEG_STA','END_STA']), 
                                overlay_table = Curve_Table, 
                                overlay_event_properties = ' '.join(['INVENTORY','LINE','BEG_STA','END_STA']), 
                                overlay_type = "UNION", 
                                out_table = Overlay_Table, 
                                out_event_properties = ' '.join(['INVENTORY','LINE','BEG_STA','END_STA']), 
                                zero_length_events = "NO_ZERO", 
                                in_fields = "FIELDS", 
                                build_index="INDEX") 

print(OverlayLayer)
F = [f.name for f in arcpy.ListFields(Overlay_Table) if not f.required and not f.name in ['INVENTORY','BEG_STA','END_STA']]
hsmpy.network.CreateRouteEventLayer(Sites_Routes=IRIS_Routes,AttTable=Overlay_Table,BMP='BEG_STA',EMP='END_STA',RouteID='INVENTORY',Fields=F,Output=OverlayLayer)

print(strftime("%Y-%m-%d %H:%M:%S"))
""".format(HSMPY_PATH,
           IRIS_Routes,
           IRIS_Table,
           Curve_Table,
           CurveLayer,
           Overlay_Table,
           OverlayLayer)
    OutFile.write(pyfile)
    OutFile.close()
    SubProcess  = subprocess.Popen([sys.executable, pyFN],shell=False,creationflags = subprocess.CREATE_NEW_CONSOLE)
    return(SubProcess)
def CON_ImportRoadwayData(WDir,HSMPY_PATH,Input,Route,AttTable,Fields,Output,RouteID,BMP,EMP,XY_Tolerance):
    import sys, os, arcpy, csv, json, math, subprocess
    sys.path.append(HSMPY_PATH)

    SubProcess = []
    PyList = []
    pyFN = os.path.join(WDir , os.path.basename(Output) + '.py')
    OutFile = open(pyFN, 'w')
    pyfile = """from time import gmtime, strftime
print(strftime("%Y-%m-%d %H:%M:%S"))
import os, sys
import arcpy
import atexit
atexit.register(raw_input, 'Press Enter to continue...')
sys.path.append(r'{}') #1
import hsmpy
Input = r"{}"
Route = r"{}"
AttTable = r"{}"
Fields = {}
Output = r"{}"
RouteID = "{}"
BMP = "{}"
EMP = "{}"
XY_Tolerance = "{}"
print("Roadway Attributes")
print(Output)
hsmpy.network.ImportRoadwayData(Input,Route,AttTable,Fields,Output,
                                    RouteID,BMP,EMP,XY_Tolerance)
hsmpy.network.PrintSegSummary(Output)
print(strftime("%Y-%m-%d %H:%M:%S"))
""".format(HSMPY_PATH,Input,Route,AttTable,Fields,Output,RouteID,BMP,EMP,XY_Tolerance)
    OutFile.write(pyfile)
    OutFile.close()
    PyList.append(pyFN)
    for py in PyList:
        SubProcess.append(subprocess.Popen(
                [sys.executable, py],
                shell=False,creationflags = subprocess.CREATE_NEW_CONSOLE))  
    return(SubProcess[0])
def CON_ImportRoadwayData_Temporal(WDir,HSMPY_PATH,Input,Route,AttTable,Fields,Output,RouteID,BMP,EMP,XY_Tolerance,Title):
    import sys, os, arcpy, csv, json, math, subprocess
    sys.path.append(HSMPY_PATH)

    pyFN = os.path.join(WDir , 'HSIP_' + str(Title) + '_RoadwayAtt.py')
    OutFile = open(pyFN, 'w')
    pyfile = """from time import gmtime, strftime
print(strftime("%Y-%m-%d %H:%M:%S"))
import os, sys
import atexit
#atexit.register(raw_input, 'Press Enter to continue...')
HSMPY_PATH = r'{}'
Input = r"{}"
Route = {}
AttTable = {}
Fields = {}
Output = {}
RouteID = "{}"
BMP = "{}"
EMP = "{}"
XY_Tolerance = "{}"

sys.path.append(HSMPY_PATH) 
import hsmpy
import arcpy
print("Roadway Attributes")
for year in Output.keys():
    print(Output[year])
    hsmpy.network.ImportRoadwayData(Input,Route[year],AttTable[year],Fields,Output[year],
                                    RouteID,BMP,EMP,XY_Tolerance)
    hsmpy.network.PrintSegSummary(Output[year],year)
print(strftime("%Y-%m-%d %H:%M:%S"))
""".format(HSMPY_PATH,Input,Route,AttTable,Fields,Output,RouteID,BMP,EMP,XY_Tolerance)
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
def CON_ImportIntData_Temporal(WDir,HSMPY_PATH,Input,TrafficControl,Routes,RouteID,BMP,EMP,AttTable,Fields,Output,OutpuTable,Title):
    import sys, os, arcpy, csv, json, math, subprocess
    sys.path.append(HSMPY_PATH)

    pyFN = os.path.join(WDir , 'HSIP_' + str(Title) + '_IntAtt.py')
    OutFile = open(pyFN, 'w')
    pyfile = """from time import gmtime, strftime
print(strftime("%Y-%m-%d %H:%M:%S"))
import os, sys
import atexit
#atexit.register(raw_input, 'Press Enter to continue...')
HSMPY_PATH = r'{}'
Input = r"{}"
TrafficControl = {}
Routes = {}
RouteID = "{}"
BMP = "{}"
EMP = "{}"
AttTable = {}
Fields = {}
Output = {}
OutputTable = {}

print("Intersection Attributes")

sys.path.append(HSMPY_PATH) 
import hsmpy
import arcpy
for year in Output.keys():
    print(Output[year])
    hsmpy.network.ImportIntAtt(Input,TrafficControl[year],Routes[year],RouteID,BMP,EMP,AttTable[year],Fields,Output[year],OutputTable[year])
    hsmpy.network.PrintIntSummary(Output[year],OutputTable[year],year)
print(strftime("%Y-%m-%d %H:%M:%S"))
""".format(HSMPY_PATH,Input,TrafficControl,Routes,RouteID,BMP,EMP,AttTable,Fields,Output,OutpuTable)
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

