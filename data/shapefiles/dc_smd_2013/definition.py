# Definition file for DC Wards, Advisory Neighborhood Commissions, and
# Single Member Districts, which are neighborhood districts in
# the District of Columbia.
#
# To load:
#
# ./manage.py loadshapefiles -r --only dc-smd-2013
# ./manage.py loadshapefiles -r --only dc-anc-2013 --merge union
# ./manage.py loadshapefiles -r --only dc-ward-2013 --merge union
# PYTHONPATH=data/shapefiles/ ./manage.py create-layer dc-smd-2013 dc-smd-2013 dc_smd_2013.definition.anc_colorer
# PYTHONPATH=data/shapefiles/ ./manage.py create-layer dc-smd-2013 dc-smd-2013-outlines dc_smd_2013.definition.smd_colorer
# PYTHONPATH=data/shapefiles/ ./manage.py create-layer dc-anc-2013 dc-anc-2013 dc_anc_2013.definition.anc_colorer
# PYTHONPATH=data/shapefiles/ ./manage.py create-layer dc-anc-2013 dc-anc-2013-outlines dc_smd_2013.definition.anc_colorer_outlines
# PYTHONPATH=data/shapefiles/ ./manage.py create-layer dc-ward-2013 dc-ward-2013 dc_ward_2013.definition.ward_colorer
# PYTHONPATH=data/shapefiles/ ./manage.py create-layer dc-ward-2013 dc-ward-2013 dc_smd_2013.definition.ward_colorer_outlines


from datetime import date
import boundaries

def get_smd_name(mode):
	def g(feature):
		#from pprint import pprint
		#pprint(dict((f, feature.get(f)) for f in feature.feature.fields))
		if mode == "name": return feature.get("NAME")
		if mode == "id": return feature.get("SMD_ID")
		if mode == "slug": return feature.get("SMD_ID")
		return True
	return g

def get_anc_name(mode):
	def g(feature):
		if mode == "name": return "ANC " + feature.get("SMD_ID")[0:2]
		if mode == "id": return feature.get("SMD_ID")[0:2]
		if mode == "slug": return feature.get("SMD_ID")[0:2]
		return True
	return g

def get_ward_name(mode):
	def g(feature):
		if mode == "name": return "Ward " + feature.get("SMD_ID")[0]
		if mode == "id": return feature.get("SMD_ID")[0]
		if mode == "slug": return feature.get("SMD_ID")[0]
		return True
	return g

boundaries.register('dc-smd-2013',
    name='DC Single Member Districts (2013)',
    singular='DC Single Member District (2013)',
    domain='District of Columbia, United States',
    last_updated=date(2012, 10, 19),
    is_valid_func=get_smd_name("is_valid"),
    name_func=get_smd_name("name"),
    id_func=get_smd_name("id"),
    slug_func=get_smd_name("slug"),
    authority='DC OCTO/DC GIS/DC OP',
    source_url='http://data.dc.gov/Metadata.aspx?id=3090',
    #data_url='',
    #encoding='iso-8859-1',
)

boundaries.register('dc-anc-2013',
    name='DC Advisory Neighborhood Commissions (2013)',
    singular='DC Advisory Neighborhood Commission (2013)',
    domain='District of Columbia, United States',
    last_updated=date(2012, 10, 19),
    is_valid_func=get_anc_name("is_valid"),
    name_func=get_anc_name("name"),
    id_func=get_anc_name("id"),
    slug_func=get_anc_name("slug"),
    authority='DC OCTO/DC GIS/DC OP',
    source_url='http://data.dc.gov/Metadata.aspx?id=3090',
    #data_url='',
    #encoding='iso-8859-1',
)

boundaries.register('dc-ward-2013',
    name='DC Wards (2013)',
    singular='DC Ward (2013)',
    domain='District of Columbia, United States',
    last_updated=date(2012, 10, 19),
    is_valid_func=get_ward_name("is_valid"),
    name_func=get_ward_name("name"),
    id_func=get_ward_name("id"),
    slug_func=get_ward_name("slug"),
    authority='DC OCTO/DC GIS/DC OP',
    source_url='http://data.dc.gov/Metadata.aspx?id=3090',
    #data_url='',
    #encoding='iso-8859-1',
)

def avg(t1, f1, t2, f2):
	return (int((t1[0]*f1+t2[0]*f2)/(f1+f2)), int((t1[1]*f1+t2[1]*f2)/(f1+f2)), int((t1[2]*f1+t2[2]*f2)/(f1+f2)), 150)

ward_color_set = [ (27, 158, 119), (217, 95, 2), (166, 118, 29), (117, 112, 179), (231, 41, 138), (102, 166, 30), (230, 171, 2), (166, 118, 29) ]
def ward_colorer(bdry, layer):
	return { "color": ward_color_set[int(bdry.slug)-1], "border": { "width": 3 } }
def ward_colorer_outlines(bdry, layer):
	return { "color": None, "border": { "width": 8 }, "label": None }

anc_color_set = [ (228, 26, 28), (55, 126, 184), (77, 175, 74), (152, 78, 163), (255, 127, 0), (255, 127, 0), (166, 86, 40) ]
def anc_colorer(bdry, layer):
	ward = int(bdry.slug[0])
	anc = bdry.slug[1]
	ward_color = ward_color_set[ward-1]
	anc_color = anc_color_set[ord(anc)-ord('a')]
	return { "color": avg(ward_color, 1.0, anc_color, 0.22), "border": { "width": 2 } }
def anc_colorer_outlines(bdry, layer):
	return { "color": None, "border": { "width": 4 }, "label": None }
	
def smd_colorer(bdry, layer):
	return { "border": { "width": 1, "color": (0,0,0,.2) }, "label": None } 
	
