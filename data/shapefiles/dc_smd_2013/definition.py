# Definition file for DC Single Member Districts, which form the Advisory
# Neighborhood Commissions, which are neighborhood districts in
# the District of Columbia.
#
# To load:
#
# python manage.py loadshapefiles -r --only dc-smd-2013
# python manage.py create-layer -c dc-smd-2013

import boundaries

def get_feature_name(mode):
	def g(feature):
		#from pprint import pprint
		#pprint(dict((f, feature.get(f)) for f in feature.feature.fields))
		if mode == "name": return feature.get("NAME")
		if mode == "id": return feature.get("SMD_ID")
		if mode == "slug": return feature.get("SMD_ID")
		return True
	return g

boundaries.register('dc-smd-2013',
    name='DC Single Member Districts (2013)',
    singular='DC Single Member District (2013)',
    domain='District of Columbia, United States',
    last_updated=date(2012, 10, 19),
    is_valid_func=get_feature_name("is_valid"),
    name_func=get_feature_name("name"),
    id_func=get_feature_name("id"),
    slug_func=get_feature_name("slug"),
    authority='DC OCTO/DC GIS/DC OP',
    source_url='http://data.dc.gov/Metadata.aspx?id=3090',
    #data_url='',
    #encoding='iso-8859-1',
)

