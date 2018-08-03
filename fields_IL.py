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
	Route_Type = {'name':'Key_Rt_Typ'   ,'alias':'Route Type'               ,'type':'SHORT','codes':{
1:'FA Interstate (FAI)',
2:'FA Primary (FAP)',
3:'FA Secondary (FAS)',
4:'State Bond Issue (SBI)',
5:'County Highway (CH)',
6:'House/Senate Bill (H/SB)',
7:'Township Road (TR)',
8:'Other Road (OR)',
9:'FA Urban (FAU)',
0:'Municipal Street System (MUN)',
}}

class gen(object):
    URBAN      = {'name': 'URBAN'      ,'alias': 'Urban'                  ,'domain':None                }; URBAN.update       (type.Short1)
    RURAL      = {'name': 'RURAL'      ,'alias': 'Rural'                  ,'domain':None                }; RURAL.update       (type.Short1)
    Area       = {'name': 'Area'       ,'alias': 'Area ID'                ,'domain':None                }; Area.update        (type.Short2)
    Area1      = {'name': 'Area1'      ,'alias': 'Area ID 1'              ,'domain':None                }; Area1.update       (type.Short2)
    Area2      = {'name': 'Area2'      ,'alias': 'Area ID 2'              ,'domain':None                }; Area2.update       (type.Short2)
    Pop_dens_p = {'name': 'Pop_dens_p' ,'alias': 'Population Density'     ,'domain':None                }; Pop_dens_p.update  (type.Double2)
class route(object):
    Name       = {'name': 'Name'       ,'alias': 'Name'                   ,'domain':None                }; Name.update        (type.Text4)
    INVENTORY  = {'name': 'INVENTORY'  ,'alias': 'Iventory'               ,'domain':None                }; INVENTORY.update   (type.Text2)
    Route_Type = {'name': 'Key_Rt_Typ' ,'alias': 'Route Type'             ,'domain':domains.Route_Type  }; Route_Type.update  (type.Short2)
    Route_Numb = {'name': 'Key_Rt_NUM' ,'alias': 'Route Number'           ,'domain':None                }; Route_Numb.update  (type.Long2)
    Route_Suf  = {'name': 'Key_Rt_SUF' ,'alias': 'Route Suffix'           ,'domain':None                }; Route_Suf.update   (type.Short2)



