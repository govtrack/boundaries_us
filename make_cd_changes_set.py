import os
os.environ["DJANGO_SETTINGS_MODULE"] = 'settings'

from datetime import date

from django.contrib.gis.geos import MultiPolygon, Polygon

from boundaries.models import *
from boundaries.management.commands.loadshapefiles import Command as LoadShapefiles

bset_2010 = BoundarySet.objects.get(slug="2010-cd")
bset_2012 = BoundarySet.objects.get(slug="2012-cd")


# At-large districts were omitted from the redistricting source data.
for _b in bset_2010.boundaries.filter(slug__endswith="-00").values_list("slug", flat=True):
	if not bset_2012.boundaries.filter(slug=_b).exists():
		b = bset_2010.boundaries.get(slug=_b)
		b.id = None # prepare to duplicate
		b.set = bset_2012
		b.save()

SLUGS = ("cd-changes", "cd-unified")

BoundarySet.objects.filter(slug__in=SLUGS).delete()

bset_changes = BoundarySet.objects.create(
	slug=SLUGS[0],
	name="Changed Congressional Districts, 2010 to 2012",
	singular="Changed Congressional District",
	authority="SRR Project/Brennan Center, the 50 states, and the United States Census",
	domain="United States",
	last_updated=date(2012, 7, 8),
	source_url='',
	notes='No redistricting data is available yet from Rhode Island. Michigan is missing because their GIS files have something odd about them that I haven\'t figured out yet.',
	licence_url='',
	)

bset_unified = BoundarySet.objects.create(
	slug=SLUGS[1],
	name="Congressional Districts with Changes, 2010 to 2012",
	singular="Congressional District or Changed Region",
	authority="SRR Project/Brennan Center, the 50 states, and the United States Census",
	domain="United States",
	last_updated=date(2012, 7, 8),
	source_url='',
	notes='No redistricting data is available yet from Rhode Island. Michigan is missing because their GIS files have something odd about them that I haven\'t figured out yet.',
	licence_url='',
	)

def fixup_intersection(geometry):
	# Interesection and simplify can give us back any sort of geometry,
	# but our shape columns must be MultiPolygons. Additionally,
	# intersection is also known to return invalid geometries. That's
	# unfortunate. We can test if it's valid, but there's no guaranteed
	# way to fix it.
	
	if geometry.geom_type == "GeometryCollection":
		polygons = []
		for p in geometry:
			mp = fixup_intersection(p)
			if mp: polygons.extend(mp)
	elif geometry.geom_type == "MultiPolygon":
		polygons = geometry
	elif geometry.geom_type == "Polygon":
		polygons = [geometry]
	elif geometry.geom_type == "LinearRing":
		polygons = [Polygon([geometry])]
	else:
		# Other geomtries (point, line) are useless to us.
		return None
		
	valid_polygons = []
	for p in polygons:
		# Check if the resulting polygon is valid.
		
		# In order to prevent GEOS_NOTICEs which clutter output, do our own
		# check for whether the polygon's outer ring has at least three distinct
		# coordinates. If not, we can skip now because it is obviously not
		# correctable.
		if len(set(p[0])) < 3: continue
		
		if not p.valid:
			# Use buffer() as a trick to fix polygon.
			# http://workshops.opengeo.org/postgis-intro/validity.html
			try:
				p = p.buffer(0.0) # raises an error sometimes
				if not p.valid: raise Exception()
			except:
				print "Could not fix invalid polygon."
				continue
			print "Fixed invalid polygon! Yay!", p.area
			
		# If it's really small, we don't really care about this component anyway.
		# We shouldn't trust the area computation on an invalid shape, so we can't
		# do this earlier. It's possible buffer() gives back valid zero-area shapes
		# even if the input was supposed to be something real, so we might be
		# unwittingly eliminating wants-to-be-good polygons here.
		if p.area < .00000000001: continue
			
		valid_polygons.append(p)
		
	if len(valid_polygons) == 0: return None
		
	return MultiPolygon(valid_polygons)

for _bdry2012 in bset_2012.boundaries.order_by("slug").values_list('slug', flat=True):
	bdry2012 = bset_2012.boundaries.get(slug=_bdry2012)
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
		# district in 2010. Compute the intersection.
		
		geometry = bdry2012.shape.intersection(bdry2010.shape)
		geometry = fixup_intersection(geometry)
		if not geometry or geometry.empty: continue
		if geometry.area < .0000000001: continue
		
		# If it's not empty or really tiny....
		
		print "", bdry2010.name, geometry.area

		feature_slug = bdry2010.slug + "__" + bdry2012.slug
		
		if bdry2010.name == bdry2012.name:
			feature_name = bdry2012.name
		else:
			feature_name = state + " " + (bdry2010.name + u"\u2192" + bdry2012.name).replace(state + "-", "")
		
		# see loadshapefiles...
		simple_geometry = geometry.simplify(app_settings.SIMPLE_SHAPE_TOLERANCE, preserve_topology=True)
		simple_geometry = fixup_intersection(simple_geometry)
		if not simple_geometry or simple_geometry.empty: simple_geometry = geometry # revert to what we know is OK
			
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

#LoadShapefiles.assign_colors(bset_unified)

# Assign colors to the unified map based on the colors assigned
# to the corresponding 2010 boundaries.
#bset_unified = BoundarySet.objects.get(slug="cd-unified")
for _b in bset_unified.boundaries.values_list("slug", flat=True):
	n0, n1 = _b.split("__") if "__" in _b else (_b, _b) # at-large are set without __
	
	b0 = bset_2010.boundaries.get(slug=n0)
	b1 = bset_unified.boundaries.get(slug=_b)
	b1.color = b0.color
	
	if n0 != n1:
		# If the district changed, assign a special color value
		# that includes the from and to colors. For new districts,
		# use white as the 2nd color.
		try:
			b2 = bset_2010.boundaries.get(slug=n1)
			b1.color = { "mode": "stripes-small", "color1": b0.color, "color2": b2.color } 
		except Boundary.DoesNotExist:
			b1.color = { "mode": "stripes-small", "color1": b0.color, "color2": (255,255,255) }
	
	b1.save()


