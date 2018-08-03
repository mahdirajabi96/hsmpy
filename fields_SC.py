class type(object):
    Text1    = {'type': 'TEXT'  ,'precision': 0 ,'scale': 0 ,'length': 5  ,'nullable': 'NULLABLE' ,'required': 'NON_REQUIRED'}
    Text2    = {'type': 'TEXT'  ,'precision': 0 ,'scale': 0 ,'length': 15 ,'nullable': 'NULLABLE' ,'required': 'NON_REQUIRED'}
    Text3    = {'type': 'TEXT'  ,'precision': 0 ,'scale': 0 ,'length': 400,'nullable': 'NULLABLE' ,'required': 'NON_REQUIRED'}
    Text4    = {'type': 'TEXT'  ,'precision': 0 ,'scale': 0 ,'length': 100,'nullable': 'NULLABLE' ,'required': 'NON_REQUIRED'}
    Text6    = {'type': 'TEXT'  ,'precision': 0 ,'scale': 0 ,'length': 6  ,'nullable': 'NULLABLE' ,'required': 'NON_REQUIRED'}
    Short1   = {'type': 'SHORT' ,'precision': 1 ,'scale': 0 ,'length': 0  ,'nullable': 'NULLABLE' ,'required': 'NON_REQUIRED'}
    Short2   = {'type': 'SHORT' ,'precision': 2 ,'scale': 0 ,'length': 0  ,'nullable': 'NULLABLE' ,'required': 'NON_REQUIRED'}
    Short3   = {'type': 'SHORT' ,'precision': 4 ,'scale': 0 ,'length': 0  ,'nullable': 'NULLABLE' ,'required': 'NON_REQUIRED'}
    Long1    = {'type': 'LONG'  ,'precision': 6 ,'scale': 0 ,'length': 0  ,'nullable': 'NULLABLE' ,'required': 'NON_REQUIRED'}
    Long2    = {'type': 'LONG'  ,'precision':10 ,'scale': 0 ,'length': 0  ,'nullable': 'NULLABLE' ,'required': 'NON_REQUIRED'}
    Double1  = {'type': 'DOUBLE','precision':15 ,'scale': 6 ,'length': 0  ,'nullable': 'NULLABLE' ,'required': 'NON_REQUIRED'}
    Double2  = {'type': 'DOUBLE','precision':9  ,'scale': 6 ,'length': 0  ,'nullable': 'NULLABLE' ,'required': 'NON_REQUIRED'}
    Double3  = {'type': 'DOUBLE','precision':4  ,'scale': 3 ,'length': 0  ,'nullable': 'NULLABLE' ,'required': 'NON_REQUIRED'}
class domains(object):
	Route_Type = {'name':'Route_type'   ,'alias':'Route Type'               ,'type':'SHORT','codes':{1:'Interstate',
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
14:'Spur'}}
	Route_Aux  = {'name':'Route_Aux'    ,'alias':'Route Aux'                ,'type':'SHORT','codes':{1:'Summary',
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
99:'Church Drive 3'}}
	Route_Dire = {'name':'Route_Dire'   ,'alias':'Route Direction'          ,'type':'TEXT' ,'codes':{'N':'North',
'S':'South',
'E':'East',
'W':'West'}}
	Median_ID  = {'name':'Median_ID'    ,'alias':'Median Type'              ,'type':'SHORT','codes':{0:'Non-divided',
1:'Divided - Earth median',
2:'Divided - Concrete median',
3:'Multi-lane - bituminous Median',
4:'Divided - Raised Concrete & Surfaced Median',
5:'Divided - Physical Barrier',
6:'Divided - Cable Stay Guardrail',
8:'One-way street'}}
	CurbPr     = {'name':'CurbPr'       ,'alias':'Curb Presence'            ,'type':'SHORT','codes':{0:'No',1:'Yes'}}
	Treat      = {'name':'Treat'        ,'alias':'Treatment'                ,'type':'SHORT','codes':{-1:'Unknown',
0:'None',
1:'Bituminous Treatment',
2:'Bituminous Valley Gutter',
3:'Bituminous Treatment & Earth'}}
	GMET       = {'name':'GMET'         ,'alias':'Geocode Method'           ,'type':'SHORT','codes':{0:'Not Geocoded',
		5:'Milepost',
		6:'State Coordinate',
		7:'DD',
		8:'DMS',
		9:'Milepost and DMS'}}
	GCXY       = {'name':'GCXY'         ,'alias':'Geocode XY Comment'       ,'type':'SHORT','codes':{0:'Out of State',
		1:'Main Route Not Found',
		2:'Far From Main Route',
		9:'On Main Route'}}
	GCMP       = {'name':'GCMP'         ,'alias':'Geocode MP Comment'       ,'type':'SHORT','codes':{1:'Main Route Not Found',
	   2:'Base Route Not Found',
	   3:'Base Intersection Not Found',
	   4:'False BDO',
	   5:'Only Base Intersection',
	   9:'Between BI and SI'}}
	RCT        = {'name':'RCT'          ,'alias':'Route Category'           ,'type':'SHORT','codes':{1:"Interstate",
		2: "US Route",
		3: "SC Route",
		4: "Secondary Route",
		5: "Local Route"}}
	RAI        = {'name':'RAI'          ,'alias':'Route Auxiliary'          ,'type':'SHORT','codes':{0:'Main Line',
	2:	'Alternate Route',
	5:	'Spur',
	6:	'Connection',
	7:	'Business',
	9:	'Other'}}
	ART        = {'name':'ART'          ,'alias':'Ramp Type'                ,'type':'SHORT','codes':{0:'Exit',
																				   1:	'Entrance',
																				   -1:'Blank'}}
	BDI        = {'name':'BDI'          ,'alias':'Base Distant Indicator'   ,'type':'TEXT' ,'codes':{'M':'Mile','F':'Feet'}}
	DAY_       = {'name':'DAY_'         ,'alias':'Day of Week'              ,'type':'SHORT','codes':{1:'Sunday',
		2:'Monday',
		3:'Tuesday',
		4:'Wednesday',
		5:'Thursday',
		6:'Friday',
		7:'Saturday'}}
	ALC        = {'name':'ALC'          ,'alias':'Light Condition'          ,'type':'SHORT','codes':{1:'DAYLIGHT (Full daylight)',
	2:'DAWN (Early morning light)',
	3:'DUSK (Early evening light)',
	4:'DARK (Lighting unspecified)',
	5:'DARK (Street lamp lit)',
	6:'DARK (Street lamp not lit)',
	7:'DARK (No lights)'}}
	WCC        = {'name':'WCC'          ,'alias':'Weather Condition'        ,'type':'SHORT','codes':{1:'CLEAR (NO ADVERSE CONDITIONS)',
2:'RAIN',
3:'CLOUDY',
4:'SLEET/HAIL',
5:'SNO ',
6:'FOG, SMOG, SMOKE',
7:'BLOWING SAND, OIL, DIRT, OR SNOW',
8:'SEVERE CROSSWINDS',
9:'UNKNOWN'}}
	RSC        = {'name':'RSC'          ,'alias':'Route Surface Condition'  ,'type':'SHORT','codes':{1:'DRY',
2:'WET',
3:'SNOW',
4:'SLUSH',
5:'ICE',
6:'CONTAMINATE',
7:'WATER (STANDING, ETC.)',
8:'OTHER',
9:'UNKNOWN'}}
	AHC        = {'name':'AHC'          ,'alias':'Highway Character'        ,'type':'SHORT','codes':{1:'STRAIGHT-LEVEL',
2:'STRAIGHT-ON GRADE',
3:'STRAIGHT-HILLCREST',
4:'CURVE-LEVEL',
5:'CURVE- ON GRADE',
6:'CURVE-HILLCREST'}}
	TWAY       = {'name':'TWAY'         ,'alias':'Traffic way'              ,'type':'SHORT','codes':{1:'TWO-WAY, NOT DIVIDED',
2:'TWO-WAY, DIVIDED, UNPROTECTED MEDIAN',
3:'TWO-WAY, DIVIDED, BARRIER',
4:'ONE-WAY',
8:'OTHER'}}
	TCT        = {'name':'TCT'          ,'alias':'Traffic Control'          ,'type':'SHORT','codes':{1:'STOP AND GO LIGHT',
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
99:'UNKNOWN'}}
	JCT        = {'name':'JCT'          ,'alias':'Junction Type'            ,'type':'SHORT','codes':{1:'CROSSOVER',
2:'DRIVEWAY',
3:'FIVE OR MORE POINTS',
4:'FOUR WAY INTERSECTION',
5:'RAILWAY GRADE CROSSING',
7:'SHARED USE PATH OR TRAILS',
8:'T-INTERSECTION',
9:'TRAFFIC CIRCLE',
12:'Y INTERSECTION',
13:'NON JUNCTION',
99:'UNKNOWN'}}
	CTY        = {'name':'CTY'          ,'alias':'County'                   ,'type':'SHORT','codes':{1:'Abbeville',
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
46:'York'}}
	Event      = {'name':'Event'        ,'alias':'Events'                   ,'type':'SHORT','codes':{1:'CARGO/EQUIPMENT LOSS OR SHIFT',
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
69:'UNKNOWN'}}
	HEL        = {'name':'HEL'          ,'alias':'FHE Location'             ,'type':'SHORT','codes':{1:'GORE',
2:'ISLAND',
3:'MEDIAN',
4:'ROADSIDE',
5:'ROADWAY',
6:'SHOULDER',
7:'SIDEWALK',
8:'OUTSIDE TRAFFICWAY',
9:'UNKNOWN'}}
	Factor     = {'name':'Factor'       ,'alias':'Contributing Factor'      ,'type':'SHORT','codes':{1:'DISREGARDED SIGN,SIGNALS, ETC.',
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
89:'UNKNOWN'}}
	MAC        = {'name':'MAC'          ,'alias':'Manner of Collision'      ,'type':'SHORT','codes':{0:'NOT COLLISION WITH MOTOR VEHICLE IN TRANSPORT',
10:'REAR END',
20:'HEAD-ON',
30:'REAR-TO-REAR',
41:'ANGLE',
42:'ANGLE',
43:'ANGLE',
50:'SIDESWIPE, SAME DIRECTION',
60:'SIDESWIPE, OPPOSITE DIRECTION',
70:'BACKED INTO',
99:'UNKNOWN'}}
	JUR        = {'name':'JUR'          ,'alias':'Jurisdiction'             ,'type':'TEXT' ,'codes':{'HP01':'S.C. HIGHWAY PATROL DISTRICT 1',
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
'4609':'RIVERHILLS PLANTATION SECURITY'}}
	YesNo      = {'name':'YesNo'        ,'alias':'Yes or No'                ,'type':'TEXT' ,'codes':{1:'Yes',2:'No'}}
	WZT        = {'name':'WZT'          ,'alias':'Workzone Type'            ,'type':'SHORT','codes':{1:'Shoulder/Median Work',
			2:	'Lane Shift/Crossover',
			3:	'Intermittent/Moving Work',
			4:	'Lane Closure',
			8:	'Other',
			9:	'Unknown'}}
	WZL        = {'name':'WZL'          ,'alias':'Workzone Location'        ,'type':'SHORT','codes':{1:'BEFORE FIRST SIGN',
			2:	'ADVANCED WARNING',
			3:	'TRANSITION AREA',
			4:	'ACTIVITY AREA',
			5:	'TERMINATION AREA'}}
	UTC        = {'name':'UTC'          ,'alias':'Unit Type'                ,'type':'SHORT','codes':{1:"AUTOMOBILE",
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
			99:	"UNKNOWN (HIT AND RUN ONLY)"}}
	Race       = {'name':'Race'         ,'alias':'Race'                     ,'type':'TEXT' ,'codes':{'A':'Asian',
'B':'African American',
'I':'American Indian',
'H':'Hispanic',
'W':'White',
'O':'Other',
'U':'Unknown'}}
	VUC        = {'name':'VUC'          ,'alias':'Vehicle Use Code'         ,'type':'SHORT','codes':{1:'PERSONAL',
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
41:'PEDESTRIAN'}}
	Action     = {'name':'Action'       ,'alias':'Action'                   ,'type':'SHORT','codes':{1:'BACKING',
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
99:'UNKNOWN'}}
	DTG        = {'name':'DTG'          ,'alias':'Drug Test Given'          ,'type':'SHORT','codes':{1:'Given Known Results',
			2:	'Given - Unusable',
			3:	'Given-Pending',
			4:	'None',
			5:	'Refused'}}
	DTT        = {'name':'DTT'          ,'alias':'Drug Test Type'           ,'type':'SHORT','codes':{1:'Breath',
			2:	'Blood',
			3:	'Urine',
			4:	'Serum',
			8:	'Other'}}
	DTR        = {'name':'DTR'          ,'alias':'Drug Test Results'        ,'type':'SHORT','codes':{1:'Amphetamines',
			2:	'Cocaine',
			3:	'Marijuana',
			4:	'Opiates',
			7:	'PCP',
			8:	'Other'}}
	UOR        = {'name':'UOR'          ,'alias':'Underride Override'       ,'type':'SHORT','codes':{1:'UNDER-COMPARTMENT INTRUSION',
			2:	'UNDER-NO INTRUSION',
			3:	'UNDER-UNKNOWN',
			4:	'OVER-MOTOR VEHICLE IN TRANSPORT',
			5:	'OVER-OTHER MOTOR VEHICLE',
			6:	'NONE',
			9:	'UNKNOWN'}}
	Sex        = {'name':'Sex'          ,'alias':'Sex'                      ,'type':'TEXT' ,'codes':{'M':'Male','F':'Female','U':'Unknown'}}
	Location   = {'name':'Location'     ,'alias':'Location'                 ,'type':'SHORT','codes':{1:'NOT TRAPPED',
			2:	'EXTRICATED (MECHANICAL MEANS)',
			3:	'FREED (NON-MECHANICAL)',
			4:	'NOT APPLICABLE',
			9:	'UNKNOWN'}}
	EJE        = {'name':'EJE'          ,'alias':'Ejection'                 ,'type':'SHORT','codes':{1:'NOT EJECTED',
			2:	'PARTIALLY EJECTE',
			3:	'TOTALLY EJECTEN',
			7:	'NOT APPLICABLE',
			9:	'UNKNOWN'}}
	AIR        = {'name':'AIR'          ,'alias':'Airbag Deployed'          ,'type':'SHORT','codes':{1:'DEPLOYED FRONT',
			2:	'DEPLOYED SIDE',
			3:	'DEPLOYED BOTH (Front and Side)',
			4:	'NOT DEPLOYED',
			7:	'NOT APPLICABLE',
			9:	'DEPLOYMENT UNKNOWN'}}
	SWT        = {'name':'SWT'          ,'alias':'Airbag Switch'            ,'type':'SHORT','codes':{1:'SWITCH IN ON POSITION',
			2:	'SWITCH IN OFF POSITION',
			3:	'NO SWITCH',
			9:	'UNKNOWN'}}
	SEV        = {'name':'SEV'          ,'alias':'Severity'                 ,'type':'SHORT','codes':{0:'No Injury',
1:'Poss Inj',
2:'Non Incapacitating Inj',
3:'Incapacitating Inj',
4:'Fatal'}}
	REU        = {'name':'REU'          ,'alias':'Restraint'                ,'type':'SHORT','codes':{0:'NONE USED',
11:'SHOULDER BELT',
12:'LAP BELT ONLY',
13:'SHOULDER AND LAP BELT',
21:'CHILD SAFETY SEAT',
88:'OTHER',
99:'UNKNOWN',
31:'HELMET',
41:'PROTECTIVE PADS',
51:'REFLECTIVE CLOTHING',
61:'LIGHTING'}}
	OSL        = {'name':'OSL'          ,'alias':'Seat Location'            ,'type':'SHORT','codes':{1:'Driver Seat',
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
			99:	'Unknown'}}
	EDAM       = {'name':'EDAM'         ,'alias':'Estimated Damage'         ,'type':'SHORT','codes':{0:'NONE/MINOR',
2:	'FUNCTIONAL DAMAGE',
3:	'DISABLING DAMAGE',
4:	'SEVERE/TOTALED',
5:	'NOT APPLICABLE',
9:	'UNKNOWN'}}
	MDA        = {'name':'MDA'          ,'alias':'Most Deformed Area'       ,'type':'SHORT','codes':{21:'Pedestrian',
			81:'None',
			92:'Rollover',
			93:'Total',
			94:'Under Carriage',
			98:'Other',
			99:'Unknown'}}
	VAT        = {'name':'VAT'          ,'alias':'Vehicle Attachment'       ,'type':'TEXT' ,'codes':{'1':	'NONE',
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
			'F':	'OTHER'}}
	VEW        = {'name':'VEW'          ,'alias':'Vehicle Weight Code'      ,'type':'SHORT','codes':{1:	'Less than 10000 pounds',
			2:	'10001-26000',
			3:	'More than 26000',
			99:	'Unknown'}}
class gen(object):
    URBAN      = {'name': 'URBAN'      ,'alias': 'Urban'                  ,'domain':None                }; URBAN.update       (type.Short1)
    RURAL      = {'name': 'RURAL'      ,'alias': 'Rural'                  ,'domain':None                }; RURAL.update       (type.Short1)
    Area       = {'name': 'Area'       ,'alias': 'Area ID'                ,'domain':None                }; Area.update        (type.Short2)
    Area1      = {'name': 'Area1'      ,'alias': 'Area ID 1'              ,'domain':None                }; Area1.update       (type.Short2)
    Area2      = {'name': 'Area2'      ,'alias': 'Area ID 2'              ,'domain':None                }; Area2.update       (type.Short2)
    Pop_dens_p = {'name': 'Pop_dens_p' ,'alias': 'Population Density'     ,'domain':None                }; Pop_dens_p.update  (type.Double2)
class route(object):
    Name       = {'name': 'Name'       ,'alias': 'Name'                   ,'domain':None                }; Name.update        (type.Text4)
    County     = {'name': 'COUNTY_ID'     ,'alias': 'County ID'              ,'domain':domains.CTY         }; County.update      (type.Short2)
    Route_Type = {'name': 'ROUTE_TYPE' ,'alias': 'Route Type'             ,'domain':domains.Route_Type  }; Route_Type.update  (type.Short2)
    Route_Numb = {'name': 'ROUTE_NUMB' ,'alias': 'Route Number'           ,'domain':None                }; Route_Numb.update  (type.Long2)
    Route_Dire = {'name': 'ROUTE_DIR' ,'alias': 'Route Direction'        ,'domain':domains.Route_Dire  }; Route_Dire.update  (type.Text1)
    Route_Aux  = {'name': 'ROUTE_AUX'  ,'alias': 'Route Auxiliary'        ,'domain':domains.Route_Aux   }; Route_Aux.update   (type.Short2)
    Route_LRS  = {'name': 'Route_LRS'  ,'alias': 'Route LRS'              ,'domain':None                }; Route_LRS.update   (type.Text2)
    Milepost   = {'name': 'Milepost'   ,'alias': 'Milepost'               ,'domain':None                }; Milepost.update    (type.Double2)
    BegMp      = {'name': 'BEG_MILEPO'      ,'alias': 'Begin Milepost'         ,'domain':None                }; BegMp.update       (type.Double2)
    EndMp      = {'name': 'END_MILEPO'      ,'alias': 'End Milepost'           ,'domain':None                }; EndMp.update       (type.Double2)
    Oneway     = {'name': 'ONEWAY'     ,'alias': 'Oneway'                 ,'domain':None                }; Oneway.update      (type.Short1)
    DirePoly   = {'name': 'DirePoly'   ,'alias': 'Directional Polylines'  ,'domain':None                }; DirePoly.update    (type.Short1)
    Length     = {'name': 'Length'     ,'alias': 'Length'                 ,'domain':None                }; Length.update      (type.Double2)
    Mileage    = {'name': 'Mileage'    ,'alias': 'Mileage'                ,'domain':None                }; Mileage.update     (type.Double2)
    StreetName = {'name': 'STREET_NAM' ,'alias': 'Street Name'            ,'domain':None                }; StreetName.update  (type.Text4)
    FType      = {'name': 'FType'      ,'alias': 'Facility Type'          ,'domain':None                }; FType.update       (type.Text2)

    Route_TypO = {'name': 'Route_TypO' ,'alias': 'Route Type Overpass'     ,'domain':domains.Route_Type  }; Route_TypO.update  (type.Short2)
    Route_NumO = {'name': 'Route_NumO' ,'alias': 'Route Number Overpass'   ,'domain':None                }; Route_NumO.update  (type.Long2)
    Route_DirO = {'name': 'Route_DirO' ,'alias': 'Route Direction Overpass','domain':domains.Route_Dire  }; Route_DirO.update  (type.Text1)
    Route_AuxO = {'name': 'Route_AuxO' ,'alias': 'Route Auxiliary Overpass','domain':domains.Route_Aux   }; Route_AuxO.update  (type.Short2)
    Route_LRSO = {'name': 'Route_LRSO' ,'alias': 'Route LRS Overpass'      ,'domain':None                }; Route_LRSO.update  (type.Text2)
    MilepostO  = {'name': 'MilepostO'  ,'alias': 'Milepost Overpass'       ,'domain':None                }; MilepostO.update   (type.Double2)

    Route_TypU = {'name': 'Route_TypU' ,'alias': 'Route Type Underpass'    ,'domain':domains.Route_Type  }; Route_TypU.update  (type.Short2)
    Route_NumU = {'name': 'Route_NumU' ,'alias': 'Route Number Underpass'  ,'domain':None                }; Route_NumU.update  (type.Long2)
    Route_DirU = {'name': 'Route_DirU' ,'alias': 'Route Direction Underpas','domain':domains.Route_Dire  }; Route_DirU.update  (type.Text1)
    Route_AuxU = {'name': 'Route_AuxU' ,'alias': 'Route Auxiliary Underpas','domain':domains.Route_Aux   }; Route_AuxU.update  (type.Short2)
    Route_LRSU = {'name': 'Route_LRSU' ,'alias': 'Route LRS Underpass'     ,'domain':None                }; Route_LRSU.update  (type.Text2)
    MilepostU  = {'name': 'MilepostU'  ,'alias': 'Milepost Underpass'      ,'domain':None                }; MilepostU.update   (type.Double2)
    BLength    = {'name': 'BLength'    ,'alias': 'Bridge Length'           ,'domain':None                }; BLength.update     (type.Double2)
    BridgeID   = {'name': 'BridgeID'   ,'alias': 'Bridge ID'               ,'domain':None                }; BridgeID.update    (type.Long2)

    Func_Class = {'name': 'Func_Class' ,'alias': 'Functional Class'       ,'domain':None                }; Func_Class.update  (type.Short2)
    AADT       = {'name': 'AADT'       ,'alias': 'AADT'                   ,'domain':None                }; AADT.update        (type.Long2)
    SegLength  = {'name': 'SegLength'  ,'alias': 'Segment Length in Feet' ,'domain':None                }; SegLength.update   (type.Double1)
    RouteFID   = {'name': 'RouteFID'   ,'alias': 'Route FID'              ,'domain':None                }; RouteFID.update    (type.Long2)
    DissolveID = {'name': 'DissolveID' ,'alias': 'Dissolve ID'            ,'domain':None                }; DissolveID.update  (type.Long2)
    TargetFID  = {'name': 'TargetFID'  ,'alias': 'TargetFID'              ,'domain':None                }; TargetFID.update   (type.Long2)
    JoinFID    = {'name': 'JoinFID'    ,'alias': 'JoinFID'                ,'domain':None                }; JoinFID.update     (type.Long2)
    RefFID     = {'name': 'RefFID'     ,'alias': 'RefrenceFID'            ,'domain':None                }; RefFID.update      (type.Long2)
    SimSites   = {'name': 'SimSites'   ,'alias': 'Similar Sites'          ,'domain':None                }; SimSites.update    (type.Long2)
    Selected   = {'name': 'Selected'   ,'alias': 'Selected'               ,'domain':None                }; Selected.update    (type.Short1)

    Median_ID  = {'name': 'Median_ID'  ,'alias': 'Median ID'              ,'domain':domains.Median_ID   }; Median_ID.update   (type.Short2)
    Median_Wid = {'name': 'Median_Wid' ,'alias': 'Median Width'           ,'domain':None                }; Median_Wid.update  (type.Double3)
    Lane_Width = {'name': 'Lane_Width' ,'alias': 'Lane Width'             ,'domain':None                }; Lane_Width.update  (type.Double3)
    #TOTALLANES = {'name': 'TOTALLANES' ,'alias': 'Total Lanes'            ,'domain':None                }; TOTALLANES.update  (type.Short1)
    TotalLanes = {'name': 'TotalLanes' ,'alias': 'Total Lanes'            ,'domain':None                }; TotalLanes.update  (type.Short1)
    LeftLanes  = {'name': 'LeftLanes'  ,'alias': 'Left Lanes'             ,'domain':None                }; LeftLanes.update   (type.Short1)
    RightLanes = {'name': 'RightLanes' ,'alias': 'Right Lanes'            ,'domain':None                }; RightLanes.update  (type.Short1)
    L_Sur_W    = {'name': 'L_Sur_W'    ,'alias': 'Left Surface Width'     ,'domain':None                }; L_Sur_W.update     (type.Double3)
    R_Sur_W    = {'name': 'R_Sur_W'    ,'alias': 'Right Surface Width'    ,'domain':None                }; R_Sur_W.update     (type.Double3)
    SurWid_Tot = {'name': 'SurWid_Tot' ,'alias': 'Surface Width'          ,'domain':None                }; SurWid_Tot.update  (type.Double3)
    Shuold_Wid = {'name': 'Shuold_Wid' ,'alias': 'Shoulder Width'         ,'domain':None                }; Shuold_Wid.update  (type.Double3)
    Sh_Wid_LI  = {'name': 'Sh_Wid_LI'  ,'alias': 'Shoulder Wid Left In'   ,'domain':None                }; Sh_Wid_LI.update   (type.Double3)
    Sh_Wid_LO  = {'name': 'Sh_Wid_LO'  ,'alias': 'Shoulder Wid Left Out'  ,'domain':None                }; Sh_Wid_LO.update   (type.Double3)
    Sh_Wid_RI  = {'name': 'Sh_Wid_RI'  ,'alias': 'Shoulder Wid Right In'  ,'domain':None                }; Sh_Wid_RI.update   (type.Double3)
    Sh_Wid_RO  = {'name': 'Sh_Wid_RO'  ,'alias': 'Shoulder Wid Right Out' ,'domain':None                }; Sh_Wid_RO.update   (type.Double3)
    Shuold_Typ = {'name': 'Shuold_Typ' ,'alias': 'Shoulder Type'          ,'domain':None                }; Shuold_Typ.update  (type.Short3)
    Sh_Trt_LI  = {'name': 'Sh_Trt_LI'  ,'alias': 'Shoulder Treatment LI'  ,'domain':domains.Treat   }; Sh_Trt_LI.update   (type.Short2)
    Sh_Trt_LO  = {'name': 'Sh_Trt_LO'  ,'alias': 'Shoulder Treatment LO'  ,'domain':domains.Treat   }; Sh_Trt_LO.update   (type.Short2)
    Sh_Trt_RI  = {'name': 'Sh_Trt_RI'  ,'alias': 'Shoulder Treatment RI'  ,'domain':domains.Treat   }; Sh_Trt_RI.update   (type.Short2)
    Sh_Trt_RO  = {'name': 'Sh_Trt_RO'  ,'alias': 'Shoulder Treatment RO'  ,'domain':domains.Treat   }; Sh_Trt_RO.update   (type.Short2)
    CurbPr_LI  = {'name': 'CurbPr_LI'  ,'alias': 'Curb Presence LI'       ,'domain':domains.CurbPr  }; CurbPr_LI.update   (type.Short1)
    CurbPr_LO  = {'name': 'CurbPr_LO'  ,'alias': 'Curb Presence LO'       ,'domain':domains.CurbPr  }; CurbPr_LO.update   (type.Short1)
    CurbPr_RI  = {'name': 'CurbPr_RI'  ,'alias': 'Curb Presence RI'       ,'domain':domains.CurbPr  }; CurbPr_RI.update   (type.Short1)
    CurbPr_RO  = {'name': 'CurbPr_RO'  ,'alias': 'Curb Presence RO'       ,'domain':domains.CurbPr  }; CurbPr_RO.update   (type.Short1)
    Sw_Trt_L   = {'name': 'Sw_Trt_L'   ,'alias': 'Sidewalk Treatment L'   ,'domain':domains.Treat   }; Sw_Trt_L.update   (type.Short2)
    Sw_Trt_R   = {'name': 'Sw_Trt_R'   ,'alias': 'Sidewalk Treatment R'   ,'domain':domains.Treat   }; Sw_Trt_R.update   (type.Short2)

    dMjC       = {'name': 'dMjC'       ,'alias': 'Num Driveway Major Comm','domain':None                }; dMjC.update        (type.Short3)
    dMnC       = {'name': 'dMnC'       ,'alias': 'Num Driveway Minor Comm','domain':None                }; dMnC.update        (type.Short3)
    dMjI       = {'name': 'dMjI'       ,'alias': 'Num Driveway Major Indu','domain':None                }; dMjI.update        (type.Short3)
    dMnI       = {'name': 'dMnI'       ,'alias': 'Num Driveway Minor Indu','domain':None                }; dMnI.update        (type.Short3)
    dMjR       = {'name': 'dMjR'       ,'alias': 'Num Driveway Major Resi','domain':None                }; dMjR.update        (type.Short3)
    dMnR       = {'name': 'dMnR'       ,'alias': 'Num Driveway Minor Resi','domain':None                }; dMnR.update        (type.Short3)
    dO         = {'name': 'dO'         ,'alias': 'Num Driveway Other'     ,'domain':None                }; dO.update          (type.Short3)
    OSPProp    = {'name': 'OSPProp'    ,'alias': 'On Street Parking Prop' ,'domain':None                }; OSPProp.update     (type.Short3)
    OSPType    = {'name': 'OSPType'    ,'alias': 'On Street Parking Type' ,'domain':None                }; OSPType.update     (type.Short3)
    FODensity  = {'name': 'FODensity'  ,'alias': 'Fixed Objects Density'  ,'domain':None                }; FODensity.update   (type.Double3)
    FOOffset   = {'name': 'FOOffset'   ,'alias': 'Fixed Objects Offset'   ,'domain':None                }; FOOffset.update    (type.Double3)
    RHR        = {'name': 'RHR'        ,'alias': 'Roadway Hazard Rating'  ,'domain':None                }; RHR.update         (type.Double3)
    TWLTL      = {'name': 'TWLTL'      ,'alias': 'Two Way Left Turn Lane' ,'domain':None                }; TWLTL.update       (type.Short3)
    HorCur     = {'name': 'HorCur'     ,'alias': 'Horizontal Curvature'   ,'domain':None                }; HorCur.update      (type.Double3)
    HorRd      = {'name': 'HorRd'      ,'alias': 'Horizontal Radius'      ,'domain':None                }; HorRd.update       (type.Double3)
    HorLn      = {'name': 'HorLn'      ,'alias': 'Horizontal Length'      ,'domain':None                }; HorLn.update       (type.Double3)
    Z_Mean     = {'name': 'Z_Mean'     ,'alias': 'Z Mean'                 ,'domain':None                }; Z_Mean.update      (type.Double3)
    Grade      = {'name': 'Grade'      ,'alias': 'Average Grade'          ,'domain':None                }; Grade.update       (type.Double3)
    DrwDens    = {'name': 'DrwDens'    ,'alias': 'Driveway Density'       ,'domain':None                }; DrwDens.update     (type.Double3)
    CZWidth    = {'name': 'CZWidth'    ,'alias': 'Clear Zone Width'       ,'domain':None                }; CZWidth.update     (type.Double3)
    PHighVol   = {'name': 'PHighVol'   ,'alias': 'Prop. High Volume'      ,'domain':None                }; PHighVol.update    (type.Double3)
class intr(object):
    AADT_Major = {'name': 'AADT_Major' ,'alias': 'AADT Major'             ,'domain':None                }; AADT_Major.update  (type.Long2)
    AADT_Minor = {'name': 'AADT_Minor' ,'alias': 'AADT Minor'             ,'domain':None                }; AADT_Minor.update  (type.Long2)
    X          = {'name': 'X'          ,'alias': 'X'                      ,'domain':None                }; X.update           (type.Double1)
    Y          = {'name': 'Y'          ,'alias': 'Y'                      ,'domain':None                }; Y.update           (type.Double1)
    X0         = {'name': 'X0'         ,'alias': 'X0'                     ,'domain':None                }; X0.update          (type.Double1)
    Y0         = {'name': 'Y0'         ,'alias': 'Y0'                     ,'domain':None                }; Y0.update          (type.Double1)
    X1         = {'name': 'X1'         ,'alias': 'X1'                     ,'domain':None                }; X1.update          (type.Double1)
    Y1         = {'name': 'Y1'         ,'alias': 'Y1'                     ,'domain':None                }; Y1.update          (type.Double1)
    X2         = {'name': 'X2'         ,'alias': 'X2'                     ,'domain':None                }; X2.update          (type.Double1)
    Y2         = {'name': 'Y2'         ,'alias': 'Y2'                     ,'domain':None                }; Y2.update          (type.Double1)
    X3         = {'name': 'X3'         ,'alias': 'X3'                     ,'domain':None                }; X3.update          (type.Double1)
    Y3         = {'name': 'Y3'         ,'alias': 'Y3'                     ,'domain':None                }; Y3.update          (type.Double1)
    IRouteFIDs = {'name': 'RouteFIDs'  ,'alias': 'Intersect. Routes FIDs' ,'domain':None                }; IRouteFIDs.update  (type.Text3)
    LEGS       = {'name': 'LEGS'       ,'alias': 'Number of Legs'         ,'domain':None                }; LEGS.update        (type.Short1)
    Degrees    = {'name': 'Degrees'    ,'alias': 'Degrees'                ,'domain':None                }; Degrees.update     (type.Text3)
    Diff       = {'name': 'Diff'       ,'alias': 'Diff in Degrees'        ,'domain':None                }; Diff.update        (type.Text3)
    SG         = {'name': 'SG'         ,'alias': 'Signal Control'         ,'domain':None                }; SG.update          (type.Short1)
    IC         = {'name': 'IC'         ,'alias': 'Interchange'            ,'domain':None                }; IC.update          (type.Short1)
    RMajor  = {'name': 'RMajor'  ,'alias': 'Route Type Major Appr'  ,'domain':None                }; RMajor.update   (type.Short2)
    RMinor  = {'name': 'RMinor'  ,'alias': 'Route Type Minor Appr'  ,'domain':None                }; RMinor.update   (type.Short2)
    Lane_Major = {'name': 'Lane_Major' ,'alias': 'Total Lanes Major Appr' ,'domain':None                }; Lane_Major.update  (type.Short2)
    Lane_Minor = {'name': 'Lane_Minor' ,'alias': 'Total Lanes Minor Appr' ,'domain':None                }; Lane_Minor.update  (type.Short2)
    MedT_Major = {'name': 'MedT_Major' ,'alias': 'Median Type Major Appr' ,'domain':None                }; MedT_Major.update  (type.Short2)
    MedT_Minor = {'name': 'MedT_Minor' ,'alias': 'Median Type Minor Appr' ,'domain':None                }; MedT_Minor.update  (type.Short2)
    Type_Major = {'name': 'Type_Major' ,'alias': 'Facility Type Major App','domain':None                }; Type_Major.update  (type.Text2)
    Type_Minor = {'name': 'Type_Minor' ,'alias': 'Facility Type Minor App','domain':None                }; Type_Minor.update  (type.Text2)
    TWid_Major = {'name': 'TWid_Major' ,'alias': 'Total Width Major Appr' ,'domain':None                }; TWid_Major.update  (type.Double3)
    TWid_Minor = {'name': 'TWid_Minor' ,'alias': 'Total Width Minor Appr' ,'domain':None                }; TWid_Minor.update  (type.Double3)

    LIGHTING   = {'name': 'LIGHTING'   ,'alias': 'Lighting'               ,'domain':None                }; LIGHTING.update    (type.Short1)
    LTL        = {'name': 'LTL'        ,'alias': 'Left Turn Lane'         ,'domain':None                }; LTL.update         (type.Short1)
    RTL        = {'name': 'RTL'        ,'alias': 'Right Turn Lane'        ,'domain':None                }; RTL.update         (type.Short1)
    SKEW1      = {'name': 'SKEW1'      ,'alias': 'Skew Angle 1'           ,'domain':None                }; SKEW1.update       (type.Short2)
    SKEW2      = {'name': 'SKEW2'      ,'alias': 'Skew Angle 2'           ,'domain':None                }; SKEW2.update       (type.Short2)
    LTP1       = {'name': 'LTP1'       ,'alias': 'LT Phasing App. 1'      ,'domain':None                }; LTP1.update        (type.Short1)
    LTP2       = {'name': 'LTP2'       ,'alias': 'LT Phasing App. 2'      ,'domain':None                }; LTP2.update        (type.Short1)
    LTP3       = {'name': 'LTP3'       ,'alias': 'LT Phasing App. 3'      ,'domain':None                }; LTP3.update        (type.Short1)
    LTP4       = {'name': 'LTP4'       ,'alias': 'LT Phasing App. 4'      ,'domain':None                }; LTP4.update        (type.Short1)
    No_RTOR    = {'name': 'No_RTOR'    ,'alias': 'No RT on Red'           ,'domain':None                }; No_RTOR.update     (type.Short1)
    BUS_STOPS  = {'name': 'BUS_STOPS'  ,'alias': 'Bus Stops'              ,'domain':None                }; BUS_STOPS.update   (type.Short1)
    SCHOOLS    = {'name': 'SCHOOLS'    ,'alias': 'Presence of School'     ,'domain':None                }; SCHOOLS.update     (type.Short1)
    ALCO_SALES = {'name': 'ALCO_SALES' ,'alias': 'Alco Sales'             ,'domain':None                }; ALCO_SALES.update  (type.Short1)
    LANESX     = {'name': 'LANESX'     ,'alias': 'Lanes Crossed'          ,'domain':None                }; LANESX.update      (type.Short1)
    PED_VOL    = {'name': 'PED_VOL'    ,'alias': 'Ped Volume'             ,'domain':None                }; PED_VOL.update     (type.Short1)
class cmf(object):
    CMFFID     = {'name': 'CMFFID'     ,'alias': 'CMF FID'                ,'domain':None                }; CMFFID.update      (type.Long2)
    CMFLength  = {'name': 'CMFLength'  ,'alias': 'CMF Length'             ,'domain':None                }; CMFLength.update   (type.Double1)
    CMFOSP     = {'name': 'CMFOSTPark' ,'alias': 'CMF On Street Parking'  ,'domain':None                }; CMFOSP.update      (type.Double3)
    CMFMW      = {'name': 'CMFMW'      ,'alias': 'CMF Median Width'       ,'domain':None                }; CMFMW.update       (type.Double3)
    CMFLW      = {'name': 'CMFLW'      ,'alias': 'CMF Lane Width'         ,'domain':None                }; CMFLW.update       (type.Double3)
    CMFSW      = {'name': 'CMFSW'      ,'alias': 'CMF Shoulder Width Type','domain':None                }; CMFSW.update       (type.Double3)
    CMFMWBMFI  = {'name': 'CMFMWBMFI'  ,'alias': 'CMF Median Wid Bar MFI' ,'domain':None                }; CMFMWBMFI.update   (type.Double3)
    CMFMWBMPD  = {'name': 'CMFMWBMPD'  ,'alias': 'CMF Median Wid Bar MPDO','domain':None                }; CMFMWBMPD.update   (type.Double3)
    CMFMWBSFI  = {'name': 'CMFMWBSFI'  ,'alias': 'CMF Median Wid Bar SFI' ,'domain':None                }; CMFMWBSFI.update   (type.Double3)
    CMFMWBSPD  = {'name': 'CMFMWBSPD'  ,'alias': 'CMF Median Wid Bar SPDO','domain':None                }; CMFMWBSPD.update   (type.Double3)
    CMFInSWFI  = {'name': 'CMFInSWFI'  ,'alias': 'CMF Inside Shou W FI'   ,'domain':None                }; CMFInSWFI.update   (type.Double3)
    CMFInSWPD  = {'name': 'CMFInSWPD'  ,'alias': 'CMF Inside Shou W PDO'  ,'domain':None                }; CMFInSWPD.update   (type.Double3)
    CMFOutSWFI = {'name': 'CMFOutSWFI' ,'alias': 'CMF Outside Sho W FI'   ,'domain':None                }; CMFOutSWFI.update  (type.Double3)
    CMFOutSWPD = {'name': 'CMFOutSWPD' ,'alias': 'CMF Outside Sho W PDO'  ,'domain':None                }; CMFOutSWPD.update  (type.Double3)
    CMFHorCur  = {'name': 'CMFHorCur'  ,'alias': 'CMF Horizontal Curv'    ,'domain':None                }; CMFHorCur.update   (type.Double3)
    CMFHCMVFI  = {'name': 'CMFHCMVFI'  ,'alias': 'CMF Horiz Curv MV FI'   ,'domain':None                }; CMFHCMVFI.update   (type.Double3)
    CMFHCMVPD  = {'name': 'CMFHCMVPD'  ,'alias': 'CMF Horiz Curv MV PDO'  ,'domain':None                }; CMFHCMVPD.update   (type.Double3)
    CMFHCSVFI  = {'name': 'CMFHCSVFI'  ,'alias': 'CMF Horiz Curv SV FI'   ,'domain':None                }; CMFHCSVFI.update   (type.Double3)
    CMFHCSVPD  = {'name': 'CMFHCSVPD'  ,'alias': 'CMF Horiz Curv SV PDO'  ,'domain':None                }; CMFHCSVPD.update   (type.Double3)
    CMFLChgFI  = {'name': 'CMFLChgFI'  ,'alias': 'CMF Lane Change FI'     ,'domain':None                }; CMFLChgFI.update   (type.Double3)
    CMFLChgPDO = {'name': 'CMFLChgPDO' ,'alias': 'CMF Lane Change PDO'    ,'domain':None                }; CMFLChgPDO.update  (type.Double3)
    CMFCZFI    = {'name': 'CMFCZFI'    ,'alias': 'CMF ClearZone FI'       ,'domain':None                }; CMFCZFI.update     (type.Double3)
    CMFOBFI    = {'name': 'CMFOBFI'    ,'alias': 'CMF Outside Barrier FI' ,'domain':None                }; CMFOBFI.update     (type.Double3)
    CMFOBPDO   = {'name': 'CMFOBPDO'   ,'alias': 'CMF Outside Barrier PDO','domain':None                }; CMFOBPDO.update    (type.Double3)
    CMFRSSVFI  = {'name': 'CMFRSSVFI'  ,'alias': 'CMF Rumble Strip SV FI ','domain':None                }; CMFRSSVFI.update   (type.Double3)
    CMFHVSVFI  = {'name': 'CMFHVSVFI'  ,'alias': 'CMF High Volume SV FI  ','domain':None                }; CMFHVSVFI.update   (type.Double3)
    CMFHVSVPDO = {'name': 'CMFHVSVPDO' ,'alias': 'CMF High Volume SV PDO ','domain':None                }; CMFHVSVPDO.update  (type.Double3)
    CMFHVMVFI  = {'name': 'CMFHVMVFI'  ,'alias': 'CMF High Volume MV FI  ','domain':None                }; CMFHVMVFI.update   (type.Double3)
    CMFHVMVPDO = {'name': 'CMFHVMVPDO' ,'alias': 'CMF High Volume MV PDO ','domain':None                }; CMFHVMVPDO.update  (type.Double3)
    CMFGrade   = {'name': 'CMFGrade'   ,'alias': 'CMF Grade'              ,'domain':None                }; CMFGrade.update    (type.Double3)
    CMFDrwDens = {'name': 'CMFDrwDens' ,'alias': 'CMF Driveway Density'   ,'domain':None                }; CMFDrwDens.update  (type.Double3)
    CMFRHR     = {'name': 'CMFRHR'     ,'alias': 'CMF RHR'                ,'domain':None                }; CMFRHR.update      (type.Double3)
    CMFLight   = {'name': 'CMFLight'   ,'alias': 'CMF Lighting'           ,'domain':None                }; CMFLight.update    (type.Double3)
    CMFFO      = {'name': 'CMFFO'      ,'alias': 'CMF Fixed Objects'      ,'domain':None                }; CMFFO.update       (type.Double3)
    CMFSkew    = {'name': 'CMFSkew'    ,'alias': 'CMF Skew'               ,'domain':None                }; CMFSkew.update     (type.Double3)
    CMFLTL     = {'name': 'CMFLTL'     ,'alias': 'CMF LT Lane'            ,'domain':None                }; CMFLTL.update      (type.Double3)
    CMFRTL     = {'name': 'CMFRTL'     ,'alias': 'CMF RT Lane'            ,'domain':None                }; CMFRTL.update      (type.Double3)
    CMFLTP     = {'name': 'CMFLTP'     ,'alias': 'CMF LT Phasing'         ,'domain':None                }; CMFLTP.update      (type.Double3)
    CMFNoRTR   = {'name': 'CMFNoRTR'   ,'alias': 'CMF No RT on Red'       ,'domain':None                }; CMFNoRTR.update    (type.Double3)
    CMFBus     = {'name': 'CMFBus'     ,'alias': 'CMF Bus Stops'          ,'domain':None                }; CMFBus.update      (type.Double3)
    CMFSchool  = {'name': 'CMFSchool'  ,'alias': 'CMF School'             ,'domain':None                }; CMFSchool.update   (type.Double3)
    CMFAlco    = {'name': 'CMFAlco'    ,'alias': 'CMF Alco Sales'         ,'domain':None                }; CMFAlco.update     (type.Double3)
    CCMF       = {'name': 'CCMF'       ,'alias': 'Combined CMF'           ,'domain':None                }; CCMF.update        (type.Double3)
class crash(object):
    # Observed Crash Related Fields
    CF        = {'name': 'CF'          ,'alias': 'Calibration Factor'     ,'domain':None                }; CF.update          (type.Double2)

    OC_FIDs   = {'name': 'OC_FIDs'     ,'alias': 'Obs. Crash FIDs'        ,'domain':None                }; OC_FIDs.update     (type.Text3)
    TOT_OC    = {'name': 'TOT_OC'      ,'alias': 'Tot. Obs. Crash'        ,'domain':None                }; TOT_OC.update      (type.Short3)
    Fitted    = {'name': 'Fitted'      ,'alias': 'Tot. Fit. Crash'        ,'domain':None                }; Fitted.update      (type.Double2)
    FitDif    = {'name': 'FitDif'      ,'alias': 'Tot. FitDif. Crash'     ,'domain':None                }; FitDif.update      (type.Double2)
    FI_OC     = {'name': 'FI_OC'       ,'alias': 'Fat. Inj. ObsCrash'     ,'domain':None                }; FI_OC.update       (type.Short3)
    MV_OC     = {'name': 'MV_OC'       ,'alias': 'Multi Veh ObsCrash'     ,'domain':None                }; MV_OC.update       (type.Short3)
    MVFI_OC   = {'name': 'MVFI_OC'     ,'alias': 'M.V. Fat. Inj. ObsCrash','domain':None                }; MVFI_OC.update     (type.Short3)
    MVPDO_OC  = {'name': 'MVPDO_OC'    ,'alias': 'M.V. PDO. ObsCrash'     ,'domain':None                }; MVPDO_OC.update    (type.Short3)
    SV_OC     = {'name': 'SV_OC'       ,'alias': 'Single Veh ObsCrash'    ,'domain':None                }; SV_OC.update       (type.Short3)
    SVFI_OC   = {'name': 'SVFI_OC'     ,'alias': 'S.V. Fat. Inj. ObsCrash','domain':None                }; SVFI_OC.update     (type.Short3)
    SVPDO_OC  = {'name': 'SVPDO_OC'    ,'alias': 'S.V. PDO. ObsCrash'     ,'domain':None                }; SVPDO_OC.update    (type.Short3)
    Ped_OC    = {'name': 'Ped_OC'      ,'alias': 'Ped Veh ObsCrash'       ,'domain':None                }; Ped_OC.update      (type.Short3)

    RDP_OC    = {'name': 'RDP_OC'      ,'alias': 'Road Depart ObsCrash'   ,'domain':None                }; RDP_OC.update      (type.Short3)

    # Predicted Crash Related Fields
    TOT_PC    = {'name': 'TOT_PC'      ,'alias': 'Tot. Pre. Crash'        ,'domain':None                }; TOT_PC.update      (type.Double2)
    TOTk_PC   = {'name': 'TOTk_PC'     ,'alias': 'Tot. Pre. Crash k'      ,'domain':None                }; TOTk_PC.update     (type.Double2)
    FI_PC     = {'name': 'FI_PC'       ,'alias': 'Fat. Inj. PreCrash'     ,'domain':None                }; FI_PC.update       (type.Double2)
    FIk_PC    = {'name': 'FIk_PC'      ,'alias': 'Fat. Inj. PreCrash k'   ,'domain':None                }; FIk_PC.update      (type.Double2)
    FIKAB_PC  = {'name': 'FIKAB_PC'    ,'alias': 'Fat. Inj. KAB PreCrash' ,'domain':None                }; FIKAB_PC.update    (type.Double2)
    FIKABk_PC = {'name': 'FIKABk_PC'   ,'alias': 'Fat. Inj. KAB PreCrashk','domain':None                }; FIKABk_PC.update   (type.Double2)
    MV_PC     = {'name': 'MV_PC'       ,'alias': 'Multi Veh PreCrash'     ,'domain':None                }; MV_PC.update       (type.Double2)
    MVk_PC    = {'name': 'MVk_PC'      ,'alias': 'Multi Veh PreCrash k'   ,'domain':None                }; MVk_PC.update      (type.Double2)
    MVFI_PC   = {'name': 'MVFI_PC'     ,'alias': 'M.V. Fat. Inj. PreCrash','domain':None                }; MVFI_PC.update     (type.Double2)
    MVFIk_PC  = {'name': 'MVFIk_PC'    ,'alias': 'M.V. Fat. Inj. PreCrshk','domain':None                }; MVFIk_PC.update    (type.Double2)
    MVPDO_PC  = {'name': 'MVPDO_PC'    ,'alias': 'M.V. PDO. PreCrash'     ,'domain':None                }; MVPDO_PC.update    (type.Double2)
    MVPDOk_PC = {'name': 'MVPDOk_PC'   ,'alias': 'M.V. PDO. PreCrash k'   ,'domain':None                }; MVPDOk_PC.update   (type.Double2)
    MVd_PC    = {'name': 'MVd_PC'      ,'alias': 'M.V. Drvway PreCrash'   ,'domain':None                }; MVd_PC.update      (type.Double2)
    MVdk_PC   = {'name': 'MVdk_PC'     ,'alias': 'M.V. Drvway PreCrash k' ,'domain':None                }; MVdk_PC.update     (type.Double2)
    MVFId_PC  = {'name': 'MVFId_PC'    ,'alias': 'M.V. Dr FI PreCrash'    ,'domain':None                }; MVFId_PC.update    (type.Double2)
    MVFIdk_PC = {'name': 'MVFIdk_PC'   ,'alias': 'M.V. Dr FI. PreCrshk'   ,'domain':None                }; MVFIdk_PC.update   (type.Double2)
    MVPDOd_PC = {'name': 'MVPDOd_PC'   ,'alias': 'M.V. Dr PDO. PreCrash'  ,'domain':None                }; MVPDOd_PC.update   (type.Double2)
    MVPDOdk_PC= {'name': 'MVPDOdk_PC'  ,'alias': 'M.V. Dr PDO. PreCrash k','domain':None                }; MVPDOdk_PC.update  (type.Double2)
    MVnd_PC   = {'name': 'MVd_PC'      ,'alias': 'M.V. NDrvway PreCrash'  ,'domain':None                }; MVnd_PC.update     (type.Double2)
    MVndk_PC  = {'name': 'MVdk_PC'     ,'alias': 'M.V. NDrvway PreCrash k','domain':None                }; MVndk_PC.update    (type.Double2)
    MVFInd_PC = {'name': 'MVFId_PC'    ,'alias': 'M.V. NDr FI PreCrash'   ,'domain':None                }; MVFInd_PC.update   (type.Double2)
    MVFIndk_PC= {'name': 'MVFIdk_PC'   ,'alias': 'M.V. NDr FI. PreCrshk'  ,'domain':None                }; MVFIndk_PC.update  (type.Double2)
    MVPDOnd_PC= {'name': 'MVPDOd_PC'   ,'alias': 'M.V. NDr PDO. PreCrash' ,'domain':None                }; MVPDOnd_PC.update  (type.Double2)
    MVPDOndk_PC= {'name': 'MVPDOdk_PC' ,'alias': 'M.V. NDr PDO. PreCrashk','domain':None                }; MVPDOndk_PC.update (type.Double2)
    SV_PC     = {'name': 'SV_PC'       ,'alias': 'Single Veh PreCrash'    ,'domain':None                }; SV_PC.update       (type.Double2)
    SVk_PC    = {'name': 'SVk_PC'      ,'alias': 'Single Veh PreCrash k'  ,'domain':None                }; SVk_PC.update      (type.Double2)
    SVFI_PC   = {'name': 'SVFI_PC'     ,'alias': 'S.V. Fat. Inj. PreCrash','domain':None                }; SVFI_PC.update     (type.Double2)
    SVFIk_PC  = {'name': 'SVFIk_PC'    ,'alias': 'S.V. Fat. Inj. PreCrshk','domain':None                }; SVFIk_PC.update    (type.Double2)
    SVPDO_PC  = {'name': 'SVPDO_PC'    ,'alias': 'S.V. PDO. PreCrash'     ,'domain':None                }; SVPDO_PC.update    (type.Double2)
    SVPDOk_PC = {'name': 'SVPDOk_PC'   ,'alias': 'S.V. PDO. PreCrashk '   ,'domain':None                }; SVPDOk_PC.update   (type.Double2)
    Ped_PC    = {'name': 'Ped_PC'      ,'alias': 'Ped Veh PreCrash'       ,'domain':None                }; Ped_PC.update      (type.Double2)
    Pedk_PC   = {'name': 'Pedk_PC'     ,'alias': 'Ped Veh PreCrash k'     ,'domain':None                }; Pedk_PC.update     (type.Double2)
    ## Split Crash Related Fields
    ABuffer   = {'name': 'ABuffer'     ,'alias': 'A Buffer'               ,'domain':None                }; ABuffer.update     (type.Double2)
    BBuffer   = {'name': 'BBuffer'     ,'alias': 'B Buffer'               ,'domain':None                }; BBuffer.update     (type.Double2)
    RBuffer   = {'name': 'RBuffer'     ,'alias': 'Road Buffer'            ,'domain':None                }; RBuffer.update     (type.Double2)
    Dist2CF   = {'name': 'Dist2CF'     ,'alias': 'Distant to Closest Faci','domain':None                }; Dist2CF.update     (type.Double2)
    ICrash    = {'name': 'ICrash'      ,'alias': 'Intersection Crash'     ,'domain':None                }; ICrash.update      (type.Short1)
    RCrash    = {'name': 'RCrash'      ,'alias': 'Road Crash'             ,'domain':None                }; RCrash.update      (type.Short1)
    OCrash    = {'name': 'OCrash'      ,'alias': 'Officer Crash'          ,'domain':None                }; OCrash.update      (type.Short1)
    RFID      = {'name': 'RFID'        ,'alias': 'Route FID'              ,'domain':None                }; RFID.update        (type.Long2)
    CI_X      = {'name': 'CI_X'        ,'alias': 'Close Intersectin X'    ,'domain':None                }; CI_X.update        (type.Double1)
    CI_Y      = {'name': 'CI_Y'        ,'alias': 'Close Intersectin Y'    ,'domain':None                }; CI_Y.update        (type.Double1)
    RFType    = {'name': 'RFType'      ,'alias': 'Related F Type'         ,'domain':None                }; RFType.update      (type.Text2)

    ## Crash Types
    Units  = {'name': 'Units'       ,'alias': 'Number of Units'        ,'domain':None                }; Units.update    (type.Text4)
    ColTyp = {'name': 'ColType'     ,'alias': 'Collision Type'         ,'domain':None                }; ColTyp.update   (type.Text4)
    Night  = {'name': 'Night'       ,'alias': 'Night Time Crash'       ,'domain':None                }; Night.update    (type.Text4)
    Fatal  = {'name': 'Fatal'       ,'alias': 'Description'            ,'domain':None                }; Fatal.update    (type.Long1)
    IncInj = {'name': 'IncInj'      ,'alias': 'Incap Injury'           ,'domain':None                }; IncInj.update   (type.Long1)
    NInInj = {'name': 'NInInj'      ,'alias': 'Not Inc Inj'            ,'domain':None                }; NInInj.update   (type.Long1)
    PosInj = {'name': 'PosInj'      ,'alias': 'Possible Inj'           ,'domain':None                }; PosInj.update   (type.Long1)
    TotFI  = {'name': 'TotFI'       ,'alias': 'Total Fatal'            ,'domain':None                }; TotFI.update    (type.Long1)
    PDO    = {'name': 'PDO'         ,'alias': 'Prop Dam Onl'           ,'domain':None                }; PDO.update      (type.Long1)
    Total  = {'name': 'Total'       ,'alias': 'Total'                  ,'domain':None                }; Total.update    (type.Long1)
    SOE1   = {'name': 'SOE1'        ,'alias': 'Seq of Events 1'        ,'domain':None                }; SOE1.update     (type.Short2)
    SOE2   = {'name': 'SOE2'        ,'alias': 'Seq of Events 2'        ,'domain':None                }; SOE2.update     (type.Short2)
    SOE3   = {'name': 'SOE3'        ,'alias': 'Seq of Events 3'        ,'domain':None                }; SOE3.update     (type.Short2)
    SOE4   = {'name': 'SOE4'        ,'alias': 'Seq of Events 4'        ,'domain':None                }; SOE4.update     (type.Short2)
    UNF    = {'name': 'UNF'         ,'alias': 'Number of units file'   ,'domain':None                }; UNF.update      (type.Short2)
    NV     = {'name': 'NV'          ,'alias': 'Number of vehicles'     ,'domain':None                }; NV.update       (type.Short2)
    Code   = {'name': 'Code'        ,'alias': 'Crash Code'             ,'domain':None                }; Code.update     (type.Short3)
    FO     = {'name': 'FO'          ,'alias': 'Fixed Object Crash'     ,'domain':None                }; FO.update       (type.Short1)
    PrmSec = {'name': 'PrmSec'      ,'alias': 'Primary or Secondary'   ,'domain':None                }; PrmSec.update   (type.Text4)  
    PrmANO = {'name': 'PrmANO'      ,'alias': 'Primary Crash ANO'      ,'domain':None                }; PrmANO.update   (type.Long2)  
    Tempor = {'name': 'Tempor'      ,'alias': 'Temporal Diff'          ,'domain':None                }; Tempor.update   (type.Double3)  
    Spatio = {'name': 'Spatio'      ,'alias': 'Spatio Diff'            ,'domain':None                }; Spatio.update   (type.Double3)  
    CNum      = {'name': 'CNum'        ,'alias': 'Cluster ID'             ,'domain':None                }; CNum.update        (type.Long2)  
    CSize     = {'name': 'CSize'       ,'alias': 'Cluster Size'           ,'domain':None                }; CSize.update       (type.Long2)  
    ZScore    = {'name': 'ZScore'      ,'alias': 'Z Score'                ,'domain':None                }; ZScore.update      (type.Double1)
    GStat     = {'name': 'GStat'       ,'alias': 'G Statistics'           ,'domain':None                }; GStat.update       (type.Double1)
class loc(object):
    Label  = {'name': 'Name'        ,'alias': 'Name'                   ,'domain':None                }; Label.update    (type.Text4)
    ANO    = {'name': 'ANO'         ,'alias': 'Accident Number'        ,'domain':None                }; ANO.update      (type.Long2)  
    CTY    = {'name': 'CTY'         ,'alias': 'County'                 ,'domain':domains.CTY      }; CTY.update      (type.Short2)
    RCT    = {'name': 'RCT'         ,'alias': 'Route Category'         ,'domain':domains.RCT         }; RCT.update      (type.Short2)
    RTN    = {'name': 'RTN'         ,'alias': 'Route Number'           ,'domain':None                }; RTN.update      (type.Long2)
    ALS    = {'name': 'ALS'         ,'alias': 'Route Name'             ,'domain':None                }; ALS.update      (type.Text4)
    RAI    = {'name': 'RAI'         ,'alias': 'Route Auxiliary'        ,'domain':domains.RAI         }; RAI.update      (type.Short2)
    LOA    = {'name': 'LOA'         ,'alias': 'Lane of Accident'       ,'domain':None                }; LOA.update      (type.Short2)
    ART    = {'name': 'ART'         ,'alias': 'Ramp Type'              ,'domain':domains.ART         }; ART.update      (type.Short2)
    DLR    = {'name': 'DLR'         ,'alias': 'Lane/Ramp Direction'    ,'domain':domains.Route_Dire         }; DLR.update      (type.Text1)

    BIR    = {'name': 'BIR'         ,'alias': 'Base Route Category'    ,'domain':domains.RCT         }; BIR.update      (type.Short2)
    BRN    = {'name': 'BRN'         ,'alias': 'Base Route Number'      ,'domain':None                }; BRN.update      (type.Long2)
    ALSB   = {'name': 'ALSB'        ,'alias': 'Base Route Name'        ,'domain':None                }; ALSB.update     (type.Text4)
    BRA    = {'name': 'BRA'         ,'alias': 'Base Route Auxiliary'   ,'domain':domains.RAI         }; BRA.update      (type.Short2)
    SIC    = {'name': 'SIC'         ,'alias': 'Second Route Category'  ,'domain':domains.RCT         }; SIC.update      (type.Short2)
    SRN    = {'name': 'SRN'         ,'alias': 'Second Route Number'    ,'domain':None                }; SRN.update      (type.Long2)
    ALSS   = {'name': 'ALSS'        ,'alias': 'Second Route Name'      ,'domain':None                }; ALSS.update     (type.Text4)
    SRA    = {'name': 'SRA'         ,'alias': 'Second Route Auxiliary' ,'domain':domains.RAI         }; SRA.update      (type.Short2)
    BDI    = {'name': 'BDI'         ,'alias': 'Base Distant Indicator' ,'domain':domains.BDI         }; BDI.update      (type.Text1)
    BDO    = {'name': 'BDO'         ,'alias': 'Base Distant Offset'    ,'domain':None                }; BDO.update      (type.Double1)
    ODR    = {'name': 'ODR'         ,'alias': 'Base Distant Direction' ,'domain':domains.Route_Dire         }; ODR.update      (type.Text1)

    DAY    = {'name': 'DAY_'        ,'alias': 'Day of Week'            ,'domain':domains.DAY_        }; DAY.update      (type.Short1)  
    DAT    = {'name': 'DAT'         ,'alias': 'Date'                   ,'domain':None                }; DAT.update      (type.Long2)  
    TIM    = {'name': 'TIM'         ,'alias': 'Time'                   ,'domain':None                }; TIM.update      (type.Short3)
    PNT    = {'name': 'PNT'         ,'alias': 'Police Notify Time'     ,'domain':None                }; PNT.update      (type.Short3)
    PAT    = {'name': 'PAT'         ,'alias': 'Police Arrive Time'     ,'domain':None                }; PAT.update      (type.Short3)

    ALC    = {'name': 'ALC'         ,'alias': 'Light Condition'        ,'domain':domains.ALC         }; ALC.update      (type.Short1)
    WCC    = {'name': 'WCC'         ,'alias': 'Weather Condition'      ,'domain':domains.WCC         }; WCC.update      (type.Short1)
    RSC    = {'name': 'RSC'         ,'alias': 'Road Surface Condition' ,'domain':domains.RSC         }; RSC.update      (type.Short1)
    AHC    = {'name': 'AHC'         ,'alias': 'Highway Character'      ,'domain':domains.AHC         }; AHC.update      (type.Short1)
    TWAY   = {'name': 'TWAY'        ,'alias': 'Traffic Way'            ,'domain':domains.TWAY        }; TWAY.update     (type.Short2)
    TCT    = {'name': 'TCT'         ,'alias': 'Traffic Control Type'   ,'domain':domains.TCT         }; TCT.update      (type.Short2)
    JCT    = {'name': 'JCT'         ,'alias': 'Junction Type'          ,'domain':domains.JCT         }; JCT.update      (type.Short2)

    UNT    = {'name': 'UNT'         ,'alias': 'Num of Units'           ,'domain':None                }; UNT.update      (type.Short2)
    FHE    = {'name': 'FHE'         ,'alias': 'First Harmful Event'    ,'domain':domains.Event         }; FHE.update      (type.Short2)
    HEL    = {'name': 'HEL'         ,'alias': 'FHE Loc'                ,'domain':domains.HEL         }; HEL.update      (type.Short2)
    XWK    = {'name': 'XWK'         ,'alias': 'FHE Crosswalk'          ,'domain':domains.YesNo         }; XWK.update      (type.Short1)
    PRC    = {'name': 'PRC'         ,'alias': 'Primary Contributing F' ,'domain':domains.Factor         }; PRC.update      (type.Short2)
    OCF1   = {'name': 'OCF1'        ,'alias': 'Other Contributing F 1' ,'domain':domains.Factor         }; OCF1.update     (type.Short2)
    OCF2   = {'name': 'OCF2'        ,'alias': 'Other Contributing F 2' ,'domain':domains.Factor         }; OCF2.update     (type.Short2)
    OCF3   = {'name': 'OCF3'        ,'alias': 'Other Contributing F 3' ,'domain':domains.Factor         }; OCF3.update     (type.Short2)
    OCF4   = {'name': 'OCF4'        ,'alias': 'Other Contributing F 4' ,'domain':domains.Factor         }; OCF4.update     (type.Short2)
    MAC    = {'name': 'MAC'         ,'alias': 'Manner of Collision'    ,'domain':domains.MAC         }; MAC.update      (type.Short2)

    FAT    = {'name': 'FAT'         ,'alias': 'Number of Fatalitiy'    ,'domain':None                }; FAT.update      (type.Short2)
    INJ    = {'name': 'INJ'         ,'alias': 'Number of Injury'       ,'domain':None                }; INJ.update      (type.Short2)

    JUR    = {'name': 'JUR'         ,'alias': 'Jurisdiction'           ,'domain':domains.JUR         }; JUR.update      (type.Text2)

    WZN    = {'name': 'WZN'         ,'alias': 'Work Zone'              ,'domain':domains.YesNo         }; WZN.update      (type.Short2)
    WZT    = {'name': 'WZT'         ,'alias': 'Work Zone Type'         ,'domain':domains.WZT         }; WZT.update      (type.Short2)
    WZL    = {'name': 'WZL'         ,'alias': 'Work Zone Location'     ,'domain':domains.WZL         }; WZL.update      (type.Short2)
    WPR    = {'name': 'WPR'         ,'alias': 'Workers Present'        ,'domain':domains.YesNo         }; WPR.update      (type.Short2)

    REPORT = {'name': 'REPORT'      ,'alias': 'Report'                 ,'domain':None                }; REPORT.update   (type.Text2)
    Symbol = {'name': 'Symbol'      ,'alias': 'Symbology Code'         ,'domain':None         }; Symbol.update   (type.Short1)

    MLRS   = {'name': 'MLRS'        ,'alias': 'Main Route LRS'         ,'domain':None                }; MLRS.update     (type.Text2)
    BLRS   = {'name': 'BLRS'        ,'alias': 'Base Route LRS'         ,'domain':None                }; BLRS.update     (type.Text2)
    SLRS   = {'name': 'SLRS'        ,'alias': 'Secondary Route LRS'    ,'domain':None                }; SLRS.update     (type.Text2)
    GMET   = {'name': 'GMET'        ,'alias': 'Geocode Method'         ,'domain':domains.GMET         }; GMET.update     (type.Short1)
    GCXY   = {'name': 'GCXY'        ,'alias': 'Geocode XY Comment'     ,'domain':domains.GCXY        }; GCXY.update     (type.Short1)
    GDXY   = {'name': 'GDXY'        ,'alias': 'Geocode XY Offset'      ,'domain':None                }; GDXY.update     (type.Double1)
    GCMP   = {'name': 'GCMP'        ,'alias': 'Geocode MP Comment'     ,'domain':domains.GCMP                }; GCMP.update     (type.Short1)
    GDMP   = {'name': 'GDMP'        ,'alias': 'Geocode MP Difference'  ,'domain':None                }; GDMP.update     (type.Double1)
    MEAS   = {'name': 'MEAS'        ,'alias': 'Milepost'               ,'domain':None                }; MEAS.update     (type.Double1)

    LAT    = {'name': 'LAT'         ,'alias': 'Latitude'               ,'domain':None                }; LAT.update      (type.Text2)
    LON    = {'name': 'LON'         ,'alias': 'Longitude'              ,'domain':None                }; LON.update      (type.Text2)
class unit(object):
    ID     = {'name': 'ID'          ,'alias': 'Identifier'             ,'domain':None                }; ID.update       (type.Long2)
    AUN    = {'name': 'AUN'         ,'alias': 'Unit Number'            ,'domain':None                }; AUN.update      (type.Short2)

    DOB    = {'name': 'DOB'         ,'alias': 'Dr-Ped Birth Date'      ,'domain':None                }; DOB.update      (type.Long2)  
    DSEX   = {'name': 'DSEX'        ,'alias': 'Dr-Ped Sex'             ,'domain':domains.Sex         }; DSEX.update     (type.Text1)
    DRAC   = {'name': 'DRAC'        ,'alias': 'Dr-Ped Race'            ,'domain':domains.Race         }; DRAC.update     (type.Text1)

    UTC    = {'name': 'UTC'         ,'alias': 'Unit Type'              ,'domain':domains.UTC         }; UTC.update      (type.Short2)
    VUC    = {'name': 'VUC'         ,'alias': 'Vehicle Use'            ,'domain':domains.VUC         }; VUC.update      (type.Short2)
    NOC    = {'name': 'NOC'         ,'alias': 'Number of Occupants'    ,'domain':None                }; NOC.update      (type.Short2)

    VMK    = {'name': 'VMK'         ,'alias': 'Vehicle Make'            ,'domain':None                }; VMK.update      (type.Text4)
    VYR    = {'name': 'VYR'         ,'alias': 'Vehicle Year'            ,'domain':None                }; VYR.update      (type.Long2)
    RPS    = {'name': 'RPS'         ,'alias': 'Veh. Reg. Plate State'   ,'domain':None                }; RPS.update      (type.Text6)
    VRY    = {'name': 'VRY'         ,'alias': 'Veh. Reg. Plate Year'    ,'domain':None                }; VRY.update      (type.Long2)
    RPN    = {'name': 'RPN'         ,'alias': 'Veh. Reg. Plate Number'  ,'domain':None                }; RPN.update      (type.Text2)
    VAT    = {'name': 'VAT'         ,'alias': 'Vehicle Attachment'      ,'domain':domains.VAT         }; VAT.update      (type.Text6)
    VEW    = {'name': 'VEW'         ,'alias': 'Vehicle Weight Code'     ,'domain':domains.VEW         }; VEW.update      (type.Short2)
    VIN    = {'name': 'VIN'         ,'alias': 'Vehicle VIN Number'      ,'domain':None                }; VIN.update      (type.Text4)

    DLN    = {'name': 'DLN'         ,'alias': 'Dr. Lic. Number'        ,'domain':None                }; DLN.update      (type.Text2)
    DLC    = {'name': 'DLC'         ,'alias': 'Dr. Lic. Class'         ,'domain':None                }; DLC.update      (type.Text2)
    DLS    = {'name': 'DLS'         ,'alias': 'Dr. Lic. State'         ,'domain':None                }; DLS.update      (type.Text6)

    VLC1   = {'name': 'VLC1'        ,'alias': 'Violation Code 1'       ,'domain':None                }; VLC1.update     (type.Short2)
    VLC2   = {'name': 'VLC2'        ,'alias': 'Violation Code 2'       ,'domain':None                }; VLC2.update     (type.Short2)
    VLC3   = {'name': 'VLC3'        ,'alias': 'Violation Code 3'       ,'domain':None                }; VLC3.update     (type.Short2)
    DTG    = {'name': 'DTG'         ,'alias': 'Drug Test Given'        ,'domain':domains.DTG         }; DTG.update      (type.Short2)
    DTT    = {'name': 'DTT'         ,'alias': 'Drug Test Type'         ,'domain':domains.DTT         }; DTT.update      (type.Short2)
    DTR    = {'name': 'DTR'         ,'alias': 'Drug Test Results'      ,'domain':domains.DTR         }; DTR.update      (type.Short2)
    UOR    = {'name': 'UOR'         ,'alias': 'Underride Override'     ,'domain':domains.UOR         }; UOR.update      (type.Short2)

    CTA    = {'name': 'CTA'         ,'alias': 'Contribute to Accident' ,'domain':domains.YesNo         }; CTA.update      (type.Short2)
    MAN    = {'name': 'MAN'         ,'alias': 'Manner of Collision'    ,'domain':domains.MAC         }; MAN.update      (type.Short2)
    MHE    = {'name': 'MHE'         ,'alias': 'Most Harmful Event'     ,'domain':domains.Event         }; MHE.update      (type.Short2)
    SOE    = {'name': 'SOE'         ,'alias': 'Seq of Events'          ,'domain':None                }; SOE.update      (type.Long2)
    SOE1   = {'name': 'SOE1'        ,'alias': 'Seq of Events 1'        ,'domain':domains.Event         }; SOE1.update     (type.Short2)
    SOE2   = {'name': 'SOE2'        ,'alias': 'Seq of Events 2'        ,'domain':domains.Event       }; SOE2.update     (type.Short2)
    SOE3   = {'name': 'SOE3'        ,'alias': 'Seq of Events 3'        ,'domain':domains.Event         }; SOE3.update     (type.Short2)
    SOE4   = {'name': 'SOE4'        ,'alias': 'Seq of Events 4'        ,'domain':domains.Event         }; SOE4.update     (type.Short2)
    API    = {'name': 'API'         ,'alias': 'Action Prior to Impact' ,'domain':domains.Action         }; API.update      (type.Short2)

    EDAM   = {'name': 'EDAM'        ,'alias': 'Extent of Damage'       ,'domain':domains.EDAM         }; EDAM.update     (type.Short2)
    EAD    = {'name': 'EAD'         ,'alias': 'Unit Dmage in Dollars'  ,'domain':None                }; EAD.update      (type.Long2)
    MDA    = {'name': 'MDA'         ,'alias': 'Most Deforemed Area'    ,'domain':None                }; MDA.update      (type.Short2)
    FDA    = {'name': 'FDA'         ,'alias': 'First Deformed Area'    ,'domain':None                }; FDA.update      (type.Short2)
    EDP    = {'name': 'EDP'         ,'alias': 'Property Damage 1'      ,'domain':None                }; EDP.update      (type.Long2)
    PD2    = {'name': 'PD2'         ,'alias': 'Property Damage 2'      ,'domain':None                }; PD2.update      (type.Long2)

    ECS    = {'name': 'ECS'         ,'alias': 'Est. Collison Speed'    ,'domain':None                }; ECS.update      (type.Short3)
    SPL    = {'name': 'SPL'         ,'alias': 'Speed Limit'            ,'domain':None                }; SPL.update      (type.Short3)
    DOT    = {'name': 'DOT'         ,'alias': 'Direction of Travel'    ,'domain':domains.Route_Dire         }; DOT.update      (type.Text1)
class occ(object):
    # Crash Occ File Fields
    OCCZIP = {'name': 'OCCZIP'      ,'alias': 'Occ. ZIP COde'          ,'domain':None                }; OCCZIP.update   (type.Long2)  
    DBIR   = {'name': 'DBIR'        ,'alias': 'Occ. Birth Date'        ,'domain':None                }; DBIR.update     (type.Long2)  
    OSEX   = {'name': 'OSEX'        ,'alias': 'Occ. Sex'               ,'domain':domains.Sex         }; OSEX.update     (type.Text1)
    ORAC   = {'name': 'ORAC'        ,'alias': 'Occ. Race'              ,'domain':domains.Race        }; ORAC.update     (type.Text1)
    AGE    = {'name': 'AGE'         ,'alias': 'Occ. Age'               ,'domain':None                }; AGE.update      (type.Short2)  

    SEV    = {'name': 'SEV'         ,'alias': 'Severity'               ,'domain':domains.SEV         }; SEV.update      (type.Short2)
    MHI    = {'name': 'MHI'         ,'alias': '2 3 Whld. Veh. Head Inj','domain':domains.YesNo         }; MHI.update      (type.Short2)
    OSL    = {'name': 'OSL'         ,'alias': 'Occ Seat Location'      ,'domain':domains.OSL         }; OSL.update      (type.Short2)
    REU    = {'name': 'REU'         ,'alias': 'Restraint Used'         ,'domain':domains.REU         }; REU.update      (type.Short2)
    LAI    = {'name': 'LAI'         ,'alias': 'Location After Impact'  ,'domain':domains.Location         }; LAI.update      (type.Short2)

    EJE    = {'name': 'EJE'         ,'alias': 'Ejection Status'        ,'domain':domains.EJE         }; EJE.update      (type.Short2)
    AIR    = {'name': 'AIR'         ,'alias': 'Airbag Deployed'        ,'domain':domains.AIR         }; AIR.update      (type.Short2)
    SWT    = {'name': 'SWT'         ,'alias': 'Airbag Switch on off'   ,'domain':domains.SWT         }; SWT.update      (type.Short2)
