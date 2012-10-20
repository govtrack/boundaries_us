=============
boundaries_us
=============


A full Django deployment for represent-boundaries (https://github.com/tauberer/represent-boundaries) and represent-maps (https://github.com/tauberer/represent-maps) with definitions for U.S.-specific data files.

This project has a complicated history. The Chicago Tribune created django-boundaryservice (http://github.com/newsapps/django-boundaryservice), a framework for creating an API around shapefiles. The OpenNorth guys tweaked it in a separate fork (https://github.com/rhymeswithcycle/represent-boundaries). Then I forked the fork to tweak the data import process (pull request pending). I also created a separate new project represent-maps (https://github.com/tauberer/represent-maps) for creating map tiles for use with Google Maps API and OpenLayers/OpenStreetMap. This project wraps it all up with actual data and deployment details.

Inside you'll find some ready-to-go data:

* A ready-to-go definition file for loading the 2010 Census's congressional districts data (which are about to go out of date).

* The 2012 redistricting shapefiles collected by the Statistical Reform in Redistricting (SRR) Project (http://www.srrproject.org/resources/redistricting-shapefiles/) and the Brennan Center for Justice at NYU, which in turn were originally created by the 50 states. The ZIP files are included in the repository because they had to be renamed to be consistent and some had to be modified to fix the names of files within the ZIP files.

* A definition file for SRR's 2012 redistricting files which figures out how to handle the slightly different naming conventions used in the shapefiles from each state.

The redistricting layer is currently running here: http://gis.govtrack.us/map/demo/2010-cd/

Installation
------------

Clone this repository.

Install Django and PostgreSQL, and the other dependencies of GeoDjango (https://docs.djangoproject.com/en/dev/ref/contrib/gis/install/). On Ubuntu::

  sudo apt-get install binutils gdal-bin libproj-dev postgresql-9.1-postgis \
     postgresql-server-dev-9.1 python-psycopg2 python-django

Install the dependencies of represent-boundaries, which are listed in externals/represent-boundaries/README.rst::

  sudo pip install django-appconf django-jsonfield django-tastypie south
  
And likewise for represent-maps, as listed in externals/represent-maps/README.rst::

  sudo apt-get install python-cairo

Follow GeoDjango's instructions to create a PostGIS spatial database template.
On Debian/Ubuntu, the script is in this git repo::

  sudo -u postgres misc/create_template_postgis-debian.sh 

Create the database and the database user::

  sudo -u postgres createdb -T template_postgis boundaries_us
  sudo -u postgres createuser -P boundaries_us

Create a settings_local.py file from the template settings_local.template.py. You'll need to fill in SECRET_KEY. Here's a quick way to generate a new key::

  python -c 'import random; print "".join([random.choice("abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)") for i in range(50)])'

Set up the Django database tables::

  python manage.py syncdb
  python manage.py migrate
  
Verify that everything worked so far::

  python manage.py runserver
  
And then open http://127.0.0.1:8000/boundary-sets in your web browser. You should see some sane JSON output. Of course there's no actual GIS data loaded yet.

Loading Data
------------

Load 2010 congressional district boundaries::

  cd data/shapefiles/tiger-2010-cd
  wget ftp://ftp.census.gov/geo/tiger/TIGER2011/CD/tl_2011_us_cd112.zip
  cd ../../..
  python manage.py loadshapefiles --only 2010-cd

This could take about 10 minutes.
  
(You may get an error "django.db.utils.DatabaseError: invalid byte sequence for encoding "UTF8": 0x00". Postgres 9.1 Django 1.3 do not agree. You can avoid this by editing /etc/postgresql/9.1/main/postgresql.conf and setting standard_conforming_strings = off, and then restart postgresql. See https://code.djangoproject.com/ticket/16778.)

Now run the server again to test (this time we'll need static files, and DEBUG is required to serve them)::

  python manage.py collectstatic
  DEBUG=1 python manage.py runserver

This dataset is loaded as '2010-cd'. Here are some API examples::

  http://127.0.0.1:8000/boundary-sets/2010-cd
  
Create a map layer with automatically assigned colors to each district::
	
  python manage.py create-layer -c 2010-cd
  
You can then see the map test page here, which you can adapt to your own needs::

   http://127.0.0.1:8000/map/demo/2010-cd

Caching Maps
------------

You are responsible for caching the map tiles generated for maps. It's best to cache at the level of the HTTP server for this so that cached responses never hit Django.

Not Using Maps?
---------------

You should comment out the maps.urls entry in urls.py. The map tile generating view is computationally expensive, so you shouldn't expose it if you aren't going to implement caching.

Nginx Configuration
---------------

I'm using the following nginx configuration to serve this site at gis.govtrack.us. It enables caching and gzip compression in useful ways::
	
	fastcgi_cache_path  /tmp/nginx-cache/gis.govtrack.us  levels=1:2 keys_zone=gis.govtrack.us:100m inactive=72h max_size=1g;
	
	server {
		listen   [::]:80;
		
		server_name gis.govtrack.us;
	
		root /home/govtrack/boundaries_us/static;
	
		location /media/ {
			alias /home/govtrack/boundaries_us/media/;
			expires 3d;
			}
		location /static/ {
			alias /home/govtrack/boundaries_us/static_collected/;
			expires 3d;
			}
	
		location / {
			include fastcgi_params;
			fastcgi_split_path_info ^()(.*)$;
			fastcgi_pass localhost:3008;
			fastcgi_read_timeout 20s;
			fastcgi_cache gis.govtrack.us;
			fastcgi_cache_key "$scheme$request_method$host$request_uri";
			fastcgi_cache_valid 200 3d;
			fastcgi_cache_valid 301 1d;
			fastcgi_cache_valid any 1m;
			fastcgi_cache_use_stale  error timeout invalid_header updating
							  http_500 http_503;
			fastcgi_no_cache $arg_nocache;
		}
	
		gzip             on;
		gzip_min_length  1000;
		gzip_types       text/plain application/xml application/json;
		gzip_disable     "MSIE [1-6]\.";
	}

