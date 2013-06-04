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

import sys
sys.path.append("data/shapefiles")

import census_helpers

def get_feature_name(mode):
	def g(feature):
		global state_fips_codes
		
		state = state_fips_codes[int(feature.get("STATEFP"))]
		if mode == "name":
			return state
		else:
			return state.lower()
	return g

census_helpers.register_boundary("states", "States", "state",
	get_feature_name("name"),
	get_feature_name("id"))

