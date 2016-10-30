#!/bin/bash

tikz=$1
ofile=$2

cat >tmp.tex <<EOF
\documentclass[border={2pt, 2pt, 0pt, 2pt}]{standalone}
\usepackage{graphics}
\usepackage{tikz}
\usetikzlibrary{arrows.meta, shadows, shapes, fit, positioning, calc, shadows}
\tikzset{help lines/.style={very thine, gray}}

\begin{document}
\input{$tikz}
\end{document}
EOF

pdflatex tmp.tex
convert tmp.pdf $ofile
rm tmp.pdf tmp.tex tmp.aux tmp.log

