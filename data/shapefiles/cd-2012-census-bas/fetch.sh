#!/bin/sh

# Download the BAS 2012 files, one for each state identified by the
# state's FIPS code, and then extract from the zip file just the
# shapefile for congressional districts, as there are other boundaries
# in there too (like state districts). The shapefiles are left in
# this directory.

mkdir -p data
for fips in 01 02 04 05 06 08 09 10 11 12 13 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 44 45 46 47 48 49 50 51 53 54 55 56 60 66 69 72 78
do
	echo $fips;
	wget -q -nc -O data/$fips.zip ftp://ftp2.census.gov/geo/pvs/$fips/partnership_shapefiles_12v2_$fips.zip;
	unzip -q -u data/$fips.zip "*_cd_*";
done
