flaskinit
=========
Bootstraps Flask projects

Install
-------
::

  $ pip install flaskinit

Usage
-----
Initialize a simple Flask project::

  $ flaskinit project

           flaskinit

     project package: project/__init__.py
       views package: project/views/__init__.py
           blueprint: project/views/root.py
        requirements: requirements.txt
   extensions module: project/extensions.py
       config module: project/config.py
          app module: project/app.py
         wsgi module: project/wsgi.py
    runserver module: runserver.py

Add blueprints::

  $ flaskinit project -b admin

           flaskinit

     project package: project/__init__.py
       views package: project/views/__init__.py
           blueprint: project/views/admin.py
           blueprint: project/views/root.py
        requirements: requirements.txt
   extensions module: project/extensions.py
       config module: project/config.py
          app module: project/app.py
         wsgi module: project/wsgi.py
    runserver module: runserver.py

Add extensions::

  $ flaskinit project -e sqlalchemy

           flaskinit

     project package: project/__init__.py
       views package: project/views/__init__.py
           blueprint: project/views/root.py
           extension: sqlalchemy
        requirements: requirements.txt
   extensions module: project/extensions.py
       config module: project/config.py
          app module: project/app.py
         wsgi module: project/wsgi.py
    runserver module: runserver.py

Available extensions:

* ``sqlalchemy`` - Flask-SQLAlchemy
* Fork and add more!

Requirements file and server script are included so you can get started quick::

  $ pip install -r requirements.txt
  $ python runserver.py

License
-------
http://marksteve.mit-license.org

