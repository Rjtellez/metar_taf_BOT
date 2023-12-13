from models.DSM import Get, Insert

# read = Get()
# metar = read.get_last('MMMZP')
# print(metar[0])

insert = Insert()
insert.insert_metar('MMMZP 301515Z 00000KT 7SM FEW030 19/12 A3010 RMK 8/100 INCIDENTE CESSNA 182 MAT 6378 EN PISTA NORTE')