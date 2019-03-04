Tilings
=======

Code associated to Rob Nicolaides's 2015 summer scholarship at the
University of Sheffield, supervised by James Cranch.


Prerequisites
-------------

In order to build the code, the following tools are needed needed:

 * python3

   This has been tested with python version 3.5.3.

 * make

   GNU make is the build tool.

 * avconv / libav-tools

   In order to make the videos, the avconv utility (from Debian's
   libav-tools) is required.

 * LaTeX + epspdf

   A latex distribution is required, with the utility epspdf (to
   convert postscript files to PDFs). Several LaTeX packages are
   needed, including xebaposter.


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

   The test suite (best run by running `nosetests3` in src/, or using
   `make test`).