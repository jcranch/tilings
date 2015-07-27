all: build-posters

demos/cubic2.eps: demo_static.py
	python demo_static.py

demos/%.pdf: demos/%.eps
	epspdf $< $@

build-posters: demos/cubic2.pdf demos/hexagonal.pdf
	$(MAKE) -C posters
