# Definition file for United States - States, 2012, from the
# United States Census Bureau's TIGER shapefiles.
#
# Download
#
#     http://www2.census.gov/geo/tiger/TIGER2012/STATE/tl_2012_us_state.zip
#
# into this directory. Then run:
#
#     python manage.py loadshapefiles --only 2012-states
#

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

def get_feature_name(mode):
	def g(feature):
		global state_fips_codes
		
		state = state_fips_codes[int(feature.get("STATEFP"))]
		if mode == "name":
			return state
		else:
			return state.lower()
	return g

def get_innerpt(feature):
	return "POINT(%f %f)" % (float(feature.get("INTPTLON")), float(feature.get("INTPTLAT")))

boundaries.register('2012-states',
    name='United States - States (2012)',
	singular='United States - State (2012)',
    domain='United States',
    last_updated=date(2012, 8, 17),
    name_func=get_feature_name("name"),
    id_func=get_feature_name("id"),
    slug_func=get_feature_name("slug"),
    label_point_func=get_innerpt,
    authority='United States Census',
    source_url='http://www.census.gov/geo/maps-data/data/tiger-line.html',
    #licence_url='',
    data_url='http://www2.census.gov/geo/tiger/TIGER2012/STATE/tl_2012_us_state.zip',
    #notes='',
    encoding='iso-8859-1',
)

