all: build-posters build-animation

clean:
	rm -f demos/*.eps demos/*.pdf demos/*.png
	rm -rf demos/*_png
	rm -f posters/*.aux posters/*.log posters/*.pdf

tidy:
	rm -f demos/*.eps
	rm -rf demos/*_png
	rm -f posters/*.aux posters/*.log


demos/%.eps: demo_static.py
	python demo_static.py

demos/%.pdf: demos/%.eps
	epspdf $< $@

build-demos: demos/cubic2.pdf demos/hexagonal.pdf

build-posters: build-demos
	$(MAKE) -C posters


VIDEOS = demos/pentatope_translate_z.mp4 demos/hypercube_translate_z.mp4 \
         demos/cell16_translate_z.mp4 demos/cell24_translate_z.mp4 \
         demos/cell120_translate_z.mp4 demos/cell600_translate_z.mp4 \
         demos/pentatope_rotate_wx.mp4 demos/hypercube_rotate_wx.mp4 \
         demos/cell16_rotate_wx.mp4 demos/cell24_rotate_wx.mp4 \
         demos/cell120_rotate_wx.mp4 demos/cell600_rotate_wx.mp4 \

build-animation: $(VIDEOS)

demos/%.mp4: demos/%_png/img000001.png
	avconv -y -framerate 25 -i demos/$*_png/img%06d.png -c:v libx264 -r 30 -pix_fmt yuv420p $@

demos/%_png/img000001.png: demo_animation.py
	python demo_animation.py $*


build-polytopes:
	python tiling4_make_polytopes.py cell24 cell120 cell600

