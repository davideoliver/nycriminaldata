from dataclasses import dataclass

@dataclass
class ComplaintData:
    CMPLNT_NUM: str
    CMPLNT_FR_DT: str
    CMPLNT_FR_TM: str
    CMPLNT_TO_DT: str
    CMPLNT_TO_TM: str
    ADDR_PCT_CD: int
    RPT_DT: str
    KY_CD: int
    OFNS_DESC: str
    PD_CD: int
    PD_DESC: int
    CRM_ATPT_CPTD_CD: str
    LAW_CAT_CD: str
    BORO_NM: str
    LOC_OF_OCCUR_DESC: str
    PREM_TYP_DESC: str
    JURIS_DESC: str
    JURISDICTION_CODE: int
    PARKS_NM: int
    HADEVELOPT: int
    HOUSING_PSA: int
    X_COORD_CD: int
    Y_COORD_CD: int
    SUSP_AGE_GROUP: str
    SUSP_RACE: str
    SUSP_SEX: str   # char em C++ vira str com tamanho 1 em Python
    TRANSIT_DISTRICT: int
    Latitude: float
    Longitude: float
    Lat_Lon: str
    PATROL_BORO: str
    STATION_NAME: str
    VIC_AGE_GROUP: str
    VIC_RACE: str
    VIC_SEX: str    # char em C++ vira str com tamanho 1 em Python