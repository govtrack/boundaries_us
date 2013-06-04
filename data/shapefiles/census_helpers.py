# Common routines for generating a boundaryset for U.S. Census TIGER shapefiles.

from datetime import date

import boundaries

state_fips_codes = {
    1: "AL", 2: "AK", 4: "AZ", 5: "AR", 6: "CA", 8: "CO", 9: "CT",
    10: "DE", 11: "DC", 12: "FL", 13: "GA", 15: "HI", 16: "ID", 17: "IL",
    18: "IN", 19: "IA", 20: "KS", 21: "KY", 22: "LA", 23: "ME", 24: "MD",
    25: "MA", 26: "MI", 27: "MN", 28: "MS", 29: "MO", 30: "MT", 31: "NE",
    32: "NV", 33: "NH", 34: "NJ", 35: "NM", 36: "NY", 37: "NC", 38: "ND",
    39: "OH", 40: "OK", 41: "OR", 42: "PA", 44: "RI", 45: "SC", 46: "SD",
    47: "TN", 48: "TX", 49: "UT", 50: "VT", 51: "VA", 53: "WA", 54: "WV",
    55: "WI", 56: "WY", 60: "AS", 66: "GU", 69: "MP", 72: "PR", 78: "VI"
    }

def get_innerpt(feature):
	return "POINT(%f %f)" % (float(feature.get("INTPTLON")), float(feature.get("INTPTLAT")))

def register_boundary(layer_name, nice_name, tiger_name, name_func, id_func):
	boundaries.register('2012-%s' % layer_name,
		name='United States - %s (2012)' % nice_name,
		singular='United States - %s (2012)' % nice_name,
		domain='United States',
		last_updated=date(2012, 8, 17),
		name_func=name_func,
		id_func=id_func,
		slug_func=id_func,
		label_point_func=get_innerpt,
		authority='United States Census',
		source_url='http://www.census.gov/geo/maps-data/data/tiger-line.html',
		#licence_url='',
		data_url='http://www2.census.gov/geo/tiger/TIGER2012/%s/tl_2012_us_%s.zip' % (tiger_name.upper(), tiger_name.lower()),
		#notes='',
		encoding='iso-8859-1',
	)

