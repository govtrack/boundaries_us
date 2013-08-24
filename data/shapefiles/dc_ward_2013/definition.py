# Definition file for DC Wards.
#
# To load:
#
# ./manage.py loadshapefiles -r --only dc-ward-2013
# PYTHONPATH=data/shapefiles/ ./manage.py create-layer dc-ward-2013 dc-ward-2013 dc_ward_2013.definition.ward_colorer
# PYTHONPATH=data/shapefiles/ ./manage.py create-layer dc-ward-2013 dc-ward-2013 dc_ward_2013.definition.ward_colorer_outlines


from datetime import date
import boundaries

def get_ward_name(mode):
	def g(feature):
		print { k: feature.get(k) for k in feature.feature.fields }
		if mode == "name": return "Ward " + feature.get("WARD_ID")
		if mode == "id": return feature.get("WARD_ID")
		if mode == "slug": return feature.get("WARD_ID")
		return True
	return g

boundaries.register('dc-ward-2013',
    name='DC Wards (2013)',
    singular='DC Ward (2013)',
    domain='District of Columbia, United States',
    last_updated=date(2012, 2, 1),
    is_valid_func=get_ward_name("is_valid"),
    name_func=get_ward_name("name"),
    id_func=get_ward_name("id"),
    slug_func=get_ward_name("slug"),
    authority='DC OCTO/DC GIS',
    source_url='http://data.dc.gov/Metadata.aspx?id=2860',
    #data_url='',
    #encoding='iso-8859-1',
)

ward_color_set = [ (27, 158, 119), (217, 95, 2), (166, 118, 29), (117, 112, 179), (231, 41, 138), (102, 166, 30), (230, 171, 2), (166, 118, 29) ]
def ward_colorer(bdry, layer):
	return { "color": ward_color_set[int(bdry.slug)-1], "border": { "width": 4 } }
def ward_colorer_outlines(bdry, layer):
	return { "color": None, "border": { "width": 4 }, "label": None }
