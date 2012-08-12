# Definition file for United States Census Tracts, 2010 Census.
#
# Download
#
#     http://www2.census.gov/geo/tiger/TIGER2010DP1/Tract_2010Census_DP1.zip
#     (from http://www.census.gov/geo/www/tiger/tgrshp2010/2010DP1.html)
#
# into this directory. Then run:
#
#     python manage.py loadshapefiles --only 2010-tract
#

from datetime import date

import boundaries

def get_feature_name(feature):
	#from pprint import pprint
	#pprint(dict((f, feature.get(f)) for f in feature.feature.fields))
	return feature.get("NAMELSAD10")
def get_feature_slug(feature):
	return feature.get("NAMELSAD10").replace("Census Tract ", "")
def get_feature_id(feature):
	return feature.get("GEOID10")
def get_innerpt(feature):
	return "POINT(%f %f)" % (float(feature.get("INTPTLON10")), float(feature.get("INTPTLAT10")))

boundaries.register('2010-tract',
    name='United States Census Tracts (2010)',
	singular='United States Census Tract (2010)',
    domain='United States',
    last_updated=date(2012, 8, 11),
    name_func=get_feature_name,
    id_func=get_feature_id,
    slug_func=get_feature_id,
    label_point_func=get_innerpt,
    authority='United States Census',
    source_url='http://www.census.gov/geo/www/tiger/tgrshp2010/2010DP1.html',
    #licence_url='',
    data_url='http://www2.census.gov/geo/tiger/TIGER2010DP1/Tract_2010Census_DP1.zip',
    #notes='',
    encoding='iso-8859-1',
)

