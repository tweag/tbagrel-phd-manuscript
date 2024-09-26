OTT_OPTS = -tex_show_meta true -tex_wrap false -picky_multiple_parses false -tex_suppress_ntr Q
PDF_ARXIV_DEPENDENCIES = *.cls *.sty *.tikzstyles *.bst graphics/* schemas/*
PDF_OTHER_DEPENDENCIES = *.bib *.py pygmentize_local

all: tbagrel_phd_manuscript.pdf

# Manual steps to submit to Arxiv:
# - the no-editing-mark trick isn't used on Arxiv submission. Make
#   sure that the editing marks are deactivated. Or that there is no
#   mark left in the pdf.
arxiv:
	$(MAKE) clean
	sed -i 's/\\usepackage{minted}/\\usepackage[finalizecache]{minted}/' tbagrel_phd_manuscript.mng
	$(MAKE) tbagrel_phd_manuscript.pdf
	sed -i 's/\\usepackage\[finalizecache\]{minted}/\\usepackage[frozencache]{minted}/' tbagrel_phd_manuscript.mng
	$(MAKE) tbagrel_phd_manuscript.tar.gz
	sed -i 's/\\usepackage\[frozencache\]{minted}/\\usepackage{minted}/' tbagrel_phd_manuscript.mng

tbagrel_phd_manuscript.tar.gz: tbagrel_phd_manuscript.tex destination_calculus_ott.tex tbagrel_phd_manuscript.bbl _minted-tbagrel_phd_manuscript $(PDF_ARXIV_DEPENDENCIES)
	tar -cvzf $@ $^

arxiv-nix:
	nix-shell --pure --run "make arxiv"

clean:
	rm -f *.aux *.bbl *.ptb *.toc *.out *.run.xml
	rm -f *.log *.bcf *.fdb_latexmk *.fls *.blg
	rm -f tbagrel_phd_manuscript.tex
	rm -f destination_calculus_ott.tex
	rm -f tbagrel_phd_manuscript.pdf
	rm -f tbagrel_phd_manuscript.tar.gz
	rm -rf _minted-tbagrel_phd_manuscript

destination_calculus_rules_mod.ott : destination_calculus_rules.ott
	python patch_rules.py destination_calculus_rules.ott destination_calculus_rules_mod.ott

destination_calculus_ott.tex: destination_calculus_grammar.ott destination_calculus_rules_mod.ott
	ott $(OTT_OPTS) -o $@ $^

tbagrel_phd_manuscript.tex: tbagrel_phd_manuscript.mng destination_calculus_grammar.ott destination_calculus_rules_mod.ott
	ott $(OTT_OPTS) -tex_filter $< $@ destination_calculus_grammar.ott destination_calculus_rules_mod.ott

tbagrel_phd_manuscript.pdf tbagrel_phd_manuscript.bbl: tbagrel_phd_manuscript.tex destination_calculus_ott.tex $(PDF_ARXIV_DEPENDENCIES) $(PDF_OTHER_DEPENDENCIES)
	latexmk tbagrel_phd_manuscript.tex

nix::
	nix-shell --pure --run make

continuous::
	ls tbagrel_phd_manuscript.mng *.ott $(PDF_ARXIV_DEPENDENCIES) $(PDF_OTHER_DEPENDENCIES) | entr make

continuous-nix:: nix
	nix-shell --pure --run "make continuous"

# .SECONDARY:
# Uncommenting the line above prevents deletion of temporary files, which can be helpful for debugging build problems
