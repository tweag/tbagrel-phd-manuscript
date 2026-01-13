OTT_OPTS = -tex_show_meta true -tex_wrap false -picky_multiple_parses false -tex_suppress_ntr Q
PDF_ARXIV_DEPENDENCIES = *.sty *.tikzstyles *.bst graphics/* schemas/* *.cls *.ist tulloria.pdf tulul.pdf *.ist fonts/iosevka* fonts/kennerley*
PDF_OTHER_DEPENDENCIES = *.bib *.py pygmentize_local shell.nix nix/*

CHAPTERS_MNG := $(wildcard chapters/*.mng)
CHAPTERS_TEX := $(CHAPTERS_MNG:.mng=.tex)

all: tbagrel_phd_manuscript.pdf tbagrel_phd_presentation.pdf tbagrel_phd_summary_fr.pdf

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

tbagrel_phd_manuscript.tar.gz: tbagrel_phd_manuscript.tex $(CHAPTERS_TEX) destination_calculus_ott.tex tbagrel_phd_manuscript.bbl tbagrel_phd_manuscript.ind tbagrel_phd_manuscript.idx tbagrel_phd_manuscript.glo _minted-tbagrel_phd_manuscript $(PDF_ARXIV_DEPENDENCIES)
	tar -cvzf $@ $^

arxiv-nix:
	nix-shell --pure --run "make arxiv"

clean:
	rm -f destination_calculus_rules_mod.ott
	rm -f ./{*.aux,*.bbl,*.ptb,*.toc,*.out,*.run.xml,*.log,*.bcf,*.bcf-SAVE-ERROR,*.fdb_latexmk,*.fls,*.blg,*.toc,*.ind,*.idx,*.gls,*.glo,*.flg,*.ilg,*.lof,*.lop,*.tex}
	rm -f chapters/{*.aux,*.bbl,*.ptb,*.toc,*.out,*.run.xml,*.log,*.bcf,*.bcf-SAVE-ERROR,*.fdb_latexmk,*.fls,*.blg,*.toc,*.ind,*.idx,*.gls,*.glo,*.flg,*.ilg,*.lof,*.lop,*.tex}
	rm -f tbagrel_phd_manuscript.pdf
	rm -f tbagrel_phd_presentation.pdf
	rm -f tbagrel_phd_summary_fr.pdf
	rm -f tbagrel_phd_manuscript.tar.gz
	rm -rf _minted-tbagrel_phd_manuscript
	rm -rf _minted-tbagrel_phd_presentation
	rm -rf _minted-tbagrel_phd_summary_fr

destination_calculus_rules_mod.ott: patch_rules.py destination_calculus_rules.ott
	python patch_rules.py destination_calculus_rules.ott destination_calculus_rules_mod.ott

destination_calculus_ott.tex: destination_calculus_grammar.ott destination_calculus_rules_mod.ott lin_calculus_rules.ott
	ott $(OTT_OPTS) -o $@ $^

%.tex: %.mng destination_calculus_grammar.ott destination_calculus_rules_mod.ott lin_calculus_rules.ott
	ott $(OTT_OPTS) -tex_filter $< $@ destination_calculus_grammar.ott destination_calculus_rules_mod.ott lin_calculus_rules.ott

tbagrel_phd_manuscript.pdf tbagrel_phd_manuscript.bbl: tbagrel_phd_manuscript.tex destination_calculus_ott.tex $(CHAPTERS_TEX) $(PDF_ARXIV_DEPENDENCIES) $(PDF_OTHER_DEPENDENCIES)
	latexmk tbagrel_phd_manuscript.tex

tbagrel_phd_presentation.pdf: tbagrel_phd_presentation.tex destination_calculus_ott.tex $(PDF_ARXIV_DEPENDENCIES) $(PDF_OTHER_DEPENDENCIES)
	latexmk tbagrel_phd_presentation.tex

tbagrel_phd_summary_fr.pdf: tbagrel_phd_summary_fr.tex destination_calculus_ott.tex $(PDF_ARXIV_DEPENDENCIES) $(PDF_OTHER_DEPENDENCIES)
	latexmk tbagrel_phd_summary_fr.tex

nix::
	nix-shell --pure --run "make tbagrel_phd_manuscript.pdf"

continuous::
	ls tbagrel_phd_manuscript.mng $(CHAPTERS_MNG) *.ott $(PDF_ARXIV_DEPENDENCIES) $(PDF_OTHER_DEPENDENCIES) Makefile | entr -s 'make tbagrel_phd_manuscript.pdf'

continuous-nix:: nix
	nix-shell --pure --run "make continuous"

nix-presentation::
	nix-shell --pure --run "make tbagrel_phd_presentation.pdf"

continuous-presentation::
	ls tbagrel_phd_presentation.mng *.ott $(PDF_ARXIV_DEPENDENCIES) $(PDF_OTHER_DEPENDENCIES) Makefile | entr -s 'make tbagrel_phd_presentation.pdf'
continuous-nix-presentation:: nix-presentation
	nix-shell --pure --run "make continuous-presentation"

nix-summary::
	nix-shell --pure --run "make tbagrel_phd_summary_fr.pdf"
continuous-summary::
	ls tbagrel_phd_summary_fr.mng *.ott $(PDF_ARXIV_DEPENDENCIES) $(PDF_OTHER_DEPENDENCIES) Makefile | entr -s 'make tbagrel_phd_summary_fr.pdf'
continuous-nix-summary:: nix-summary
	nix-shell --pure --run "make continuous-summary"

# .SECONDARY:
# Uncommenting the line above prevents deletion of temporary files, which can be helpful for debugging build problems
