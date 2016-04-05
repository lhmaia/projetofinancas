FILE = pre_proposta

LATEX_EXECUTABLE = latex

all: ${FILE}.tex
	${LATEX_EXECUTABLE} ${FILE}.tex
	${LATEX_EXECUTABLE} ${FILE}.tex
	dvipdf ${FILE}.dvi
clean:
	rm -f *.log *.aux *.bbl *.blg

