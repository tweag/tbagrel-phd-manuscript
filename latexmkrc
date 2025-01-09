$pdf_mode = "1";
$pdflatex = "lualatex -shell-escape -halt-on-error -interaction=nonstopmode -file-line-error";
$clean_ext = "bbl synctex.gz synctex.gz(busy)";

# hardcoded file names because we need two different styles for index/glossary
$makeindex = 'makeindex -s tulind.ist -o tbagrel_phd_manuscript.ind tbagrel_phd_manuscript.idx && makeindex -s tulglo.ist -o tbagrel_phd_manuscript.gls tbagrel_phd_manuscript.glo';

# When a file required for the compilation of the main latex file
# (such as an image for `\includegraphics`) latexmk will call `make`
# in order to have it built.
#
# This option is not suitable for Arxiv submission, so it's better to
# explicitly build the dependencies in the Makefile.
#
# $use_make_for_missing_files = "1";
