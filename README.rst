=============
boundaries_us
=============

See the live demo of this project at http://gis.govtrack.us/map/demo/cd-2012/.

This project creates an API and map tile layers for geospatial data. It lets you easily go from shapefiles (of, say, political boundaries) to an API that can answer questions like what district is a coordinate in and which districts touch, and can create pretty Google Maps/OSM maps with those boundaries outlined.

This is a full Django deployment of two other projects --- represent-boundaries by OpenNorth (https://github.com/rhymeswithcycle/represent-boundaries) and represent-maps (https://github.com/tauberer/represent-maps), which I created --- plus examples of how to load in some U.S.-specific data files such as 2012 congressional districts. You might need a little familiarity with Django to get this to work.

Inside you'll find some ready-to-go data: 2012 U.S. congressional districts, U.S. state boundaries, and District of Columbia Ward/ANC/SMD boundaries. The purpose of this project is to show you how you can deploy a similar site for whatever data you have.


Installation
------------

You'll need Ubuntu 11.10 (or later) and Django 1.5::

  sudo pip install --upgrade "django>=1.5,<=1.6"

Start by cloning this repository. You'll need to clone it using the --recursive flag so that the dependencies get cloned as submodules::

  git clone --recursive https://github.com/tauberer/boundaries_us

Install PostgreSQL and the other dependencies of GeoDjango (https://docs.djangoproject.com/en/dev/ref/contrib/gis/install/). On Ubuntu::

  sudo apt-get install binutils gdal-bin libproj-dev postgresql-9.1-postgis \
     postgresql-server-dev-9.1 python-psycopg2

Install the dependencies of represent-boundaries, which at the time of writing are::

  sudo pip install django-appconf django-jsonfield south pil
  
And likewise for represent-maps, as listed in externals/represent-maps/README.rst::

  sudo apt-get install python-cairo
  (python-cairo is only readily available in Ubuntu)

Follow GeoDjango's instructions to create a PostGIS spatial database template.
On Debian/Ubuntu, the script is in this git repo::

  sudo -u postgres misc/create_template_postgis-debian.sh 

Create the database and the database user::

  sudo -u postgres createdb -T template_postgis boundaries_us
  sudo -u postgres createuser -P boundaries_us

Create a settings_local.py file from the template settings_local.template.py. You'll need to fill in SECRET_KEY. Here's a quick way to generate a new key::

  python -c 'import random; print "".join([random.choice("abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)") for i in range(50)])'

And tweak the other settings, such as the database credientials, if needed.
  
Set up the Django database tables::

  python manage.py syncdb
  
Verify that everything worked so far::

  python manage.py runserver
  
And then open http://127.0.0.1:8000/boundary-sets in your web browser. You should see some sane JSON output. Of course there's no actual GIS data loaded yet.

Loading Data
------------

Load 2012 congressional district boundaries::

  cd data/shapefiles/cd-2012-census-bas/
  ./fetch
  cd ../../..
  python manage.py loadshapefiles -c -r --only cd-2012

This will take a little bit of time.
  
(You may get an error "django.db.utils.DatabaseError: invalid byte sequence for encoding "UTF8": 0x00". Postgres 9.1 Django 1.3 do not agree. You can avoid this by editing /etc/postgresql/9.1/main/postgresql.conf and setting standard_conforming_strings = off, and then restart postgresql. See https://code.djangoproject.com/ticket/16778.)

Now run the server again to test (this time we'll need static files, and DEBUG is required to serve them)::

  python manage.py collectstatic
  DEBUG=1 python manage.py runserver

This dataset is loaded as 'cd-2012'. Here are some API examples::

  http://127.0.0.1:8000/boundary-sets/cd-2012
  
Create a map layer with automatically assigned colors to each district::
	
  python manage.py create-layer -c cd-2012
  
You can then see the map test page here, which you can adapt to your own needs::

   http://127.0.0.1:8000/map/demo/cd-2012

Caching Maps
------------

You are responsible for caching the map tiles generated for maps. It's best to cache at the level of the HTTP server for this so that cached responses never hit Django.

Not Using Maps?
---------------

You should comment out the maps.urls entry in urls.py. The map tile generating view is computationally expensive, so you shouldn't expose it if you aren't going to implement caching.

Nginx Configuration
---------------

I'm using the following nginx configuration to serve this site at gis.govtrack.us. It enables caching and gzip compression in useful ways::
	
	fastcgi_cache_path  /tmp/nginx-cache-gis.govtrack.us  levels=1:2 keys_zone=gis.govtrack.us:100m inactive=72h max_size=1g;
	
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
			fastcgi_cache_bypass $arg_nocache;
		}
	
		gzip             on;
		gzip_min_length  1000;
		gzip_types       text/plain application/xml application/json;
		gzip_disable     "MSIE [1-6]\.";
	}

