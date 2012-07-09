import os
os.environ["DJANGO_SETTINGS_MODULE"] = 'settings'

from datetime import date

from django.contrib.gis.geos import MultiPolygon

from boundaries.models import *
from boundaries.management.commands.loadshapefiles import Command as LoadShapefiles

SLUGS = ("cd-changes", "cd-unified")

BoundarySet.objects.filter(slug__in=SLUGS).delete()

bset_changes = BoundarySet.objects.create(
	slug=SLUGS[0],
	name="Changed Congressional Districts, 2010 to 2012",
	singular="Changed Congressional District",
	authority="SRR Project/Brennan Center and United States Census",
	domain="United States",
	last_updated=date(2012, 7, 8),
	source_url='',
	notes='',
	licence_url='',
	)

bset_unified = BoundarySet.objects.create(
	slug=SLUGS[1],
	name="Congressional Districts with Changes, 2010 to 2012",
	singular="Congressional District or Changed Region",
	authority="SRR Project/Brennan Center and United States Census",
	domain="United States",
	last_updated=date(2012, 7, 8),
	source_url='',
	notes='',
	licence_url='',
	)

bset_2010 = BoundarySet.objects.get(slug="2010-cd")
bset_2012 = BoundarySet.objects.get(slug="2012-cd")

def fixup_intersection(geometry):
	if geometry.geom_type != "MultiPolygon":
		if geometry.geom_type != "GeometryCollection": geometry = [geometry]
		geometry = MultiPolygon([p if p.geom_type == 'Polygon' else Polygon([p]) for p in geometry if p.geom_type in ('Polygon', 'LinearRing')])
	return geometry

for _bdry2012 in bset_2012.boundaries.values('slug'):
	bdry2012 = bset_2012.boundaries.get(slug=_bdry2012["slug"])
	print bdry2012.name
	
	state = bdry2012.name[0:2]
	
	# For each district in 2012, find all intersecting 2010 districts
	# (including itself). For each intersection with a different numbered
	# district, create a new Boundary in the changed boundaries set and
	# also in the unified districts set. If it's the same numbered district,
	# only include it in the unified set.
	for bdry2010 in bset_2010.boundaries\
		.filter(shape__intersects=bdry2012.shape)\
		.filter(name__startswith=state):
			
		# The new boundary overlaps with a boundary for a different
		# district in 2010.
		
		geometry = bdry2012.shape.intersection(bdry2010.shape)
		if geometry.empty: continue
		geometry = fixup_intersection(geometry)
		if geometry.area < .0000000001: continue
		
		print "", bdry2010.name, geometry.area

		feature_slug = bdry2010.slug + "__" + bdry2012.slug
		
		if bdry2010.name == bdry2012.name:
			feature_name = bdry2012.name
		else:
			feature_name = state + " " + (bdry2010.name + u"\u2192" + bdry2012.name).replace(state + "-", "")
		
		# see loadshapefiles...
		simple_geometry = geometry.simplify(app_settings.SIMPLE_SHAPE_TOLERANCE, preserve_topology=True)
		simple_geometry = fixup_intersection(simple_geometry)
			
		for bset in (bset_changes, bset_unified):
			if bdry2010.name == bdry2012.name and bset == bset_changes: continue
			Boundary.objects.create(
				set=bset,
				set_name=bset.singular,
				external_id=feature_slug,
				name=feature_name,
				slug=feature_slug,
				metadata={ "from_id": bdry2010.external_id, "to_id": bdry2012.external_id, "from_slug": bdry2010.slug, "to_slug": bdry2012.slug, "from_name": bdry2010.name, "to_name": bdry2012.name },
				shape=geometry.wkt,
				simple_shape=simple_geometry.wkt,
				centroid=geometry.centroid,
				extent=geometry.extent,
				color=[255,0,0],
				)

LoadShapefiles.assign_colors(bset_unified)

