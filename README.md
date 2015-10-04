Tilings
=======

Code associated to Rob Nicolaides's 2015 summer scholarship at the
University of Sheffield, supervised by James Cranch.


Prerequisites
-------------

In order to build the code, the following is needed

 * python2

   This has been tested with python version 2.7.

 * make

   GNU make has been used to build the project.

 * avconv

   In order to make the videos, the avconv package is required.

 * LaTeX + epspdf + baposter

   A latex distribution is required, with the utility epspdf (to
   convert postscript files to PDFs), and the baposter class installed
   (this is not part of CTAN, so needs downloading separately).


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

 * posters/mathsimages
   posters/codeimages

   Dynamically-generated illustrations for posters.

 * posters/listings

   Code for inclusion in the code poster

 * tests/

   The test suite (best run by running `nosetests` in the base
   directory).