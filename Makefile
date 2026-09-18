.PHONY: paper check clean
paper:
	cd paper && pdflatex -interaction=nonstopmode -halt-on-error main.tex
	cd paper && pdflatex -interaction=nonstopmode -halt-on-error main.tex
check:
	python3 code/verify.py --output code/checks.json
	python3 code/verify_extensions.py --output code/extension_checks.json
clean:
	rm -f paper/main.aux paper/main.log paper/main.out
