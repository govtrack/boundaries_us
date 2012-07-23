#!/usr/bin/python
import os, sys
os.environ["DJANGO_SETTINGS_MODULE"] = 'settings'
sys.path.append('.')

from boundaries.models import *

bset_2010 = BoundarySet.objects.get(slug="2010-cd")
bset_2012 = BoundarySet.objects.get(slug="2012-cd")

# At-large districts are initially omitted from the redistricting source data
# because no shapefiles are included for those states/territories. Just copy
# them over from the 2010 census boundaries.
for _b in bset_2010.boundaries.filter(slug__endswith="-00").values_list("slug", flat=True):
	if not bset_2012.boundaries.filter(slug=_b).exists():
		b = bset_2010.boundaries.get(slug=_b)
		b.id = None # prepare to duplicate
		b.set = bset_2012
		b.set_name = bset_2012.name
		b.save()
