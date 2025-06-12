with { pkgs = import ./nix {}; };

pkgs.mkShell
  { buildInputs = with pkgs; [
      bashInteractive
      python310Packages.pygments
      which
      gnumake
      # coq
      # coqPackages.coqide
      # haskellPackages.lhs2tex
      biber
      ott
      pdftk
      entr
      (texlive.combine {
        inherit (texlive)
          acmart
          amscls
          amsfonts
          amsmath
          bbold
          biblatex
          biblatex-software
          bibtex
          booktabs
          bussproofs
          caption
          cleveref
          cm-super
          cmap
          comment
          doclicense
          draftwatermark
          enumitem
          environ
          etoolbox
          fancyhdr
          float
          fontaxes
          geometry
          graphics
          graphics-def
          halloweenmath
          hyperref
          hyperxmp
          ifmtarg
          iftex
          inconsolata
          kastrup
          l3kernel
          l3packages
          latexmk
          lazylist
          libertine
          lm
          lm-math
          logreq
          lualatex-math
          mathpartir
          mathspec
          microtype
          minted
          mmap
          ms
          mweights
          natbib
          ncctools
          newtx
          newunicodechar
          nowidow
          oberdiek
          placeins
          pict2e
          polytable
          preprint
          refcount
          scheme-basic
          scheme-small
          setspace
          stmaryrd
          supertabular
          textcase
          tikz-cd
          todonotes
          tools
          lastpage
          trimspaces
          txfonts
          ulem
          unicode-math
          upquote
          url
          xargs
          xcolor
          xifthen
          xkeyval
          xpatch
          xstring

          bclogo
          # for bclogo
          mdframed
          zref
          needspace
          chngcntr
          csquotes
          pdfx
          luatex85
          xmpincl
          ;
      })

      ];
    LANG="C.UTF-8";
    NIX_PATH = "nixpkgs=${pkgs.path}";
  }
