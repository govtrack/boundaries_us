# Definition file for redistricting shapefile from the Statistical Reform in
# Redistricting Project (srrproject.org) and the Brennan Center for Justice
# at NYU. http://www.srrproject.org/resources/redistricting-shapefiles/
#
# Unfortunately, in some ZIP files from SRR the .dbf filename has a different case
# than the .shp filename, resulting in the shapefile loader not seeing the
# .dbf file, which has all of the metadata. Each ZIP file has to be individually
# checked & fixed so that the case is consistent.
#
# Also, we assume that the ZIP files are named with the state's two-letter
# USPS abbreviation, which is different from the file names used by SRR.
#
# Finally, to load:
#
# python manage.py loadshapefiles -c -r --only 2012-cd
#
# Last I checked the SRR website (2012-07-08), only Rhode Island was missing data.
# Michigan uses a projection that doesn't seem to load right, so we're skipping
# those files for now too.


from datetime import date
import os.path
import random

import boundaries

def get_feature_name(mode):
    def g(feature):
        state = os.path.basename(feature.layer.source.zipfile).replace(".zip", "")

        if state in ('CO', 'IL', 'IN', 'NE', 'NM', 'NV', 'OK', 'OR', 'PA', 'WA', 'WI'):
            dfield = "District_N"
        elif state in ("ME","NC","TX"):
            dfield = "District"
        elif state in ("HI",):
            dfield = "USDist"
        elif state in ("LA",):
            dfield = "DISTRICT_I"
        elif state in ("NH",):
            dfield = "CONG2012"
        elif state in ("AL",):
            dfield = "NAME"
        else:
            dfield = "DISTRICT"
            
        if dfield not in feature.feature.fields or feature.get(dfield) == "":
            # We're about to crash with django.contrib.gis.gdal.error.OGRIndexError: 'invalid OFT field name given: "DISTRICT"'
            from pprint import pprint
            print feature.layer.source.zipfile
            print feature.layer.source.name
            pprint(dict((f, feature.get(f)) for f in feature.feature.fields))
            return False
       
        if mode == "is_valid": return True

        if state == "AL":
            cd = int(feature.get(dfield).replace("District ", ""))
        else:
            cd = int(feature.get(dfield))
            
        if state == "MD":
            cd -= 2400 # hmm
        
        if mode == "name":
            #print "%s-%d" % (state, cd)
            return "%s-%d" % (state, cd)
        else:
            return "%s-%02d" % (state.lower(), cd)
    return g

boundaries.register('2012-cd',
    name='United States Congressional Districts (2012)',
    singular='United States Congressional District (2012)',
    domain='United States',
    last_updated=date(2012, 7, 8),
    is_valid_func=get_feature_name("is_valid"),
    name_func=get_feature_name("name"),
    id_func=get_feature_name("id"),
    slug_func=get_feature_name("slug"),
    authority='SRR Project/Brennan Center',
    source_url='http://www.srrproject.org/resources/redistricting-shapefiles/',
    #data_url='',
    encoding='iso-8859-1',
)

