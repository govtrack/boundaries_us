# Definition file for United States - Block Groups, 2012, from the
# United States Census Bureau's TIGER shapefiles.
#
# Download using "./fetch.sh" to grab the state files. Then run:
#
#     python manage.py loadshapefiles --only 2012-blockgroups
#

import sys
sys.path.append("data/shapefiles")

import census_helpers

def get_feature_name(feature):
   #print { k: feature.get(k) for k in feature.feature.fields }
   return feature.get("GEOID")

def get_feature_id(feature):
   return feature.get("GEOID")

census_helpers.register_boundary(
	"blockgroups",
	"Block Groups",
	"bg",
	get_feature_name,
	get_feature_id)

