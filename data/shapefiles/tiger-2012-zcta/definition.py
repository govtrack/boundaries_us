# Definition file for Census Zip Code Tabulation Areas, 2012, from the
# United States Census Bureau's TIGER shapefiles.
#
# ZCTAs aren't zip codes. They're way, way approximate and usually
# have little value for building applications.
#
# Download
#
#     ftp://ftp2.census.gov/geo/tiger/TIGER2012/ZCTA5/tl_2012_us_zcta510.zip
#
# into this directory. Then run:
#
#     python manage.py loadshapefiles --only 2012-zcta
#

import sys
sys.path.append("data/shapefiles")

import census_helpers

def get_feature_name(mode):
	def g(feature):
		print feature.feature.fields
		
		global census_helpers
		state = census_helpers.state_fips_codes[int(feature.get("STATEFP"))]
		if mode == "name":
			return state + " " + feature.get("NAME")
		else:
			return state.lower() + "-" + feature.get("COUNTYFP")
	return g

census_helpers.register_boundary("zctas", "ZCTAs", "zcta5",
	get_feature_name("name"),
	get_feature_name("id"))

