all: build-posters build-animation


clean-general:
	rm -f *.pyc tests/*.pyc

clean-posters: clean-general
	rm -rf posters/*.aux posters/*.log posters/*.pdf posters/mathsimages posters/codeimages

clean-animation: clean-general
	rm -f demos/*.eps demos/*.pdf demos/*.png
	rm -f demos/*.mp4
	rm -rf demos/*_png

clean: clean-posters clean-animation


tidy:
	rm -f demos/*.eps
	rm -rf demos/*_png
	rm -f posters/*.aux posters/*.log


demos/%.eps: demo_static.py
	python demo_static.py

demos/%.pdf: demos/%.eps
	epspdf $< $@


MATHSPOSTER_EXTRAS = posters/mathsimages/platonic_solids.png \
                     posters/mathsimages/dual_platonic_solids.png \
                     posters/mathsimages/regular_polygons.png \
                     posters/mathsimages/cube_slice_1.png \
                     posters/mathsimages/cube_slice_2.png \
                     posters/mathsimages/cell600_cell120.png \
                     posters/mathsimages/hypercube_crosssections.png \
                     posters/mathsimages/tessellations_2d.png \
                     posters/mathsimages/cell24.png \
                     posters/diagrams/sheffield-logo.pdf

CODEPOSTER_EXTRAS = posters/codeimages/unit_ball.pdf \
                    posters/listings/norm1.pdf \
                    posters/listings/triangles.pdf \
                    posters/diagrams/fundamental.pdf \
                    posters/diagrams/sheffield-logo.pdf

posters/%.pdf: posters/%.tex
	cd posters && pdflatex -halt-on-error $*.tex
	cd posters && pdflatex -halt-on-error $*.tex

posters/mathsimages/%: mathsposter_images.py
	python3 mathsposter_images.py $*

posters/codeimages/%: codeposter_images.py
	python3 codeposter_images.py $*

posters/codeimages/%.pdf: posters/codeimages/%.eps
	epspdf $< $@

posters/diagrams/%.pdf: posters/diagrams/%.eps
	epspdf $< $@

posters/listings/%.pdf: posters/listings/%.tex posters/listings/%.py posters/listings/common.tex
	cd posters/listings && pdflatex -halt-on-error $*.tex
	cd posters/listings && pdflatex -halt-on-error $*.tex

posters/mathsposter.pdf: $(MATHSPOSTER_EXTRAS)

posters/codeposter.pdf: $(CODEPOSTER_EXTRAS)

build-posters: posters/mathsposter.pdf posters/codeposter.pdf


VIDEOS = demos/pentatope_translate_z.mp4 demos/hypercube_translate_z.mp4 \
         demos/cell16_translate_z.mp4 demos/cell24_translate_z.mp4 \
         demos/cell120_translate_z.mp4 demos/cell600_translate_z.mp4 \
         demos/pentatope_rotate_wx.mp4 demos/hypercube_rotate_wx.mp4 \
         demos/cell16_rotate_wx.mp4 demos/cell24_rotate_wx.mp4 \
         demos/cell120_rotate_wx.mp4 demos/cell600_rotate_wx.mp4 \
         demos/pentatope_full_uniform_rotate.mp4 \
         demos/hypercube_full_uniform_rotate.mp4 \
         demos/cell16_full_uniform_rotate.mp4 \
         demos/cell24_full_uniform_rotate.mp4 \
         demos/cell120_full_uniform_rotate.mp4 \
         demos/cell600_full_uniform_rotate.mp4 \
         demos/tetrahedron_rotate_z.mp4 \
         demos/cube_rotate_z.mp4 demos/octahedron_rotate_z.mp4 \
         demos/icosahedron_rotate_z.mp4 demos/dodecahedron_rotate_z.mp4

build-animation: $(VIDEOS)

demos/%.mp4: demos/%_png/img000001.png
	avconv -y -framerate 15 -i demos/$*_png/img%06d.png -c:v libx264 -r 30 -pix_fmt yuv420p $@

demos/%_png/img000001.png: demo_animation.py
	python3 demo_animation.py $*


POLYTOPES = autotilings/cell24.data \
            autotilings/cell120.data \
            autotilings/cell600.data

build-polytopes: $(POLYTOPES)

autotilings/%.data:
	python3 tiling4_make_polytopes.py $*
