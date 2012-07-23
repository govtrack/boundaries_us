# Projects Michican shapefiles into WGS84. Michigan uses a projection
# that is not supported by the GDAL tools, although it is supported
# by proj4. Use proj4 to project to WGS84 and use ogr2ogr to re-package
# it as a shapefile.
#
# Extract the Michigan shapefiles to this directory. Make sure any
# output from a previous run of this command is deleted or ogr2ogr
# will fail.
#
# Run this script: ./reproject_michigan.py
#
# This produces output.xml and output_new/*, and ZIPs up the new
# shapefile files as MI.zip. You can delete the other output files.
# You'll then need to add an appropriately named .prj file to the
# ZIP file. You can copy the one from AL.zip, for instance.

import lxml.etree, subprocess, tempfile

# Output shapefile to XML so we can read it easily.
subprocess.check_call(["ogr2ogr", "-f", "GML", "output.xml", "US_Cong_Districts_2010.shp"])

dom = lxml.etree.parse('output.xml')
for c in dom.xpath('//gml:coordinates', namespaces={'gml':"http://www.opengis.net/gml"}):
	f = tempfile.TemporaryFile()
	coords = "\n".join([r.replace(",", " ") for r in c.text.split(" ")])
	reproj = subprocess.Popen(["invproj", "-f", "%.12f", "+proj=omerc", "+lat_0=45.30916666666666", "+lonc=-86", "+alpha=337.255555555556", "+k=0.9996", "+x_0=2546731.496", "+y_0=-4354009.816", "+ellps=GRS80", "+datum=NAD83", "+units=m", "+no_uoff"], stdin=subprocess.PIPE, stdout=f)
	reproj.stdin.write(coords)
	reproj.stdin.close()
	reproj.wait()
	f.seek(0)
	c.text = " ".join([r.replace("\t", ",") for r in f.read().split("\n")])

with open('output.xml', 'w') as f:
    f.write(lxml.etree.tostring(dom))

subprocess.check_call(["ogr2ogr", "-f", "ESRI Shapefile", "output_new", "output.xml"])

subprocess.check_call(["zip", "-j", "MI.zip", "output_new/US_Cong_Districts_2010.dbf", "output_new/US_Cong_Districts_2010.shp", "output_new/US_Cong_Districts_2010.shx"])
