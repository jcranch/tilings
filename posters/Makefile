# Requires baposter
#
# See:
#   http://www.brian-amberg.de/uni/poster/
#   https://blogs.cs.st-andrews.ac.uk/jfdm/tag/tutorial/

all: example.pdf

%.pdf: %.tex
	pdflatex -halt-on-error $<
	pdflatex -halt-on-error $<

example.pdf: listing1.pdf sheffield-logo.pdf ../demos/cubic2.pdf

sheffield-logo.pdf: sheffield-logo.eps
	epspdf $<

