# Definition file for United States - County Subdivisions, 2012, from the
# United States Census Bureau's TIGER shapefiles.
#
# Download
#
#     ftp://ftp2.census.gov/geo/tiger/TIGER2012/COUSUB/tl_2012_us_cousub.zip
#
# into this directory. Then run:
#
#     python manage.py loadshapefiles --only 2012-countysubs
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

census_helpers.register_boundary("countysubs", "County Subdivisions", "cousub",
	get_feature_name("name"),
	get_feature_name("id"))

