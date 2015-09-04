Tilings
=======

Code associated to Rob Nicolaides's 2015 summer scholarship at the
University of Sheffield, supervised by James Cranch.


Files and directories
---------------------

Here are some hints about the way the project is laid out, that might
be useful for someone starting off.

 * autotilings/

   Some complicated stored tiling objects. They can be automatically
   generated (using `tiling4_make_polytopes.py`) but it takes a long
   time.

 * demos/

   Some files automatically generated (by `make build-demos`). These
   include videos which are slow to build.

 * posters/

   Some illustrations of the code and its applications (built by `make
   build-posters`).

 * posters/diagrams/

   Static illustrations for posters.

 * tests/

   The test suite (best run by running `nosetests` in the base
   directory).