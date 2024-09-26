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
          mathpartir
          microtype
          minted
          mmap
          ms
          mweights
          natbib
          ncctools
          newtx
          newunicodechar
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
          totpages
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
          ;
      })

      ];
    LANG="C.UTF-8";
    NIX_PATH = "nixpkgs=${pkgs.path}";
    FONTCONFIG_FILE = pkgs.makeFontsConf { fontDirectories =
    # Fonts for Xetex
    [ pkgs.libertine
      pkgs.inconsolata
    ]; };
  }
