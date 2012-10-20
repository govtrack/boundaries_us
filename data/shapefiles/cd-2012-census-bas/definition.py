# Definition file for United States congressional districts, 2012 (113th Congress),
# from the United States Census Bureau's Boundary and Annexation Survey
# made available in October 2012.
#
# Downloads are from
#
#     https://www.census.gov/rdo/data/113th_congressional_and_new_state_legislative_district_plans.html
#
# But it's complicated to pull all the right files, so there's a
# script for that:
#
#     ./fetch.sh
#
# Then run:
#
#     python manage.py loadshapefiles -c -r --only cd-2012-census-bas
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
		
		if feature.get("CDFP") == "ZZ":
			# "areas with no congressional district defined (usually large water bodies)"
			return False
		if mode == "valid":
			return True
		
		cd = int(feature.get("CDFP"))
		if cd in (98, 99): # Census's convention for non-state territories
			cd = 0 # Our convention for all at-large districts
			
		if mode == "name":
			return "%s-%d" % (state, cd)
		else:
			return "%s-%02d" % (state.lower(), cd)
	return g

boundaries.register('cd-2012',
    name='United States Congressional Districts (2012; Census BAS)',
	singular='United States Congressional District (2012)',
    domain='United States',
    last_updated=date(2012, 10, 19),
    is_valid_func=get_feature_name("valid"),
    name_func=get_feature_name("name"),
    id_func=get_feature_name("id"),
    slug_func=get_feature_name("slug"),
    authority='United States Census',
    source_url='https://www.census.gov/rdo/data/113th_congressional_and_new_state_legislative_district_plans.html',
    encoding='iso-8859-1',
)

