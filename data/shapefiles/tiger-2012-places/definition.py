# Definition file for United States - Census Plates, 2012, from the
# United States Census Bureau's TIGER shapefiles.
#
# Download using "./fetch.sh" to grab the state files. Then run:
#
#     python manage.py loadshapefiles --only 2012-places
#

import sys
sys.path.append("data/shapefiles")

import census_helpers

def get_feature_name(feature):
   #print { k: feature.get(k) for k in feature.feature.fields }
   return feature.get("NAME")

def get_feature_id(feature):
   return feature.get("GEOID")

census_helpers.register_boundary("places", "Census Places", "place",
	get_feature_name,
	get_feature_id)

