#!/usr/bin/env python3
"""

Usage: ./momento.py [-b] [-a] [-y] [-t]
where


Author: Matt Post
"""


import sys
from datetime import datetime
from typing import List

template_header = r"""\documentclass{article}

\usepackage[legalpaper, total={8in, 16in}]{geometry}
\usepackage{adjustbox}
\usepackage{graphicx}
\usepackage{pdfpages}
\usepackage{booktabs}
\usepackage{colortbl}

\begin{document}

\begin{table}[p]
  \begin{adjustbox}{max width=\textwidth}
  \begin{tabular}{|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|}
"""

template_row = r"""
    \cline{11-52}
    \multicolumn{10}{c|}{} & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & \\
    \hline
    & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & \\
    \hline
    & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & \\
    \hline
"""

template_footer = r"""
  \end{tabular}
  \end{adjustbox}
\end{table}

\end{document}
"""

default_color = "white"


def build_cells(color=default_color, num=52, label="", lastlabel="") -> List[str]:
    cells = []
    for weekno in range(1, num + 1):
        label = lastlabel if weekno == num else label
        cells.append(fr"\cellcolor{{{color}}}{label}")
    return cells

def main(args):
    current_week = datetime.utcnow().strftime("%U")

    table = ""
    color = "white"
    print(template_header, file=args.outfile)
    print(fr"  \cline{{{args.birth_week+1}-52}}", file=args.outfile)
    print(fr"\multicolumn{{{args.birth_week}}}{{c|}}{{}} & ", file=args.outfile)
    print(" & ".join(build_cells(color=color, num=52-args.birth_week)), file=args.outfile)
    print(r"\\")
    print(r"\hline")

    for year in range(2, args.years):
        if year % 10 == 0:
            color = "gray!25"
            lastlabel = str(year)
        else:
            color = "white"
            lastlabel = ""

        if year <= args.age:
            label = "x"
        else:
            label = ""

        print(" & ".join(build_cells(color=color, label=label, lastlabel=lastlabel)), r"\\", file=args.outfile)
        print(r"  \hline", file=args.outfile)

    print(template_footer, file=args.outfile)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--birth-week", "-b" , type=int, default=1,
                        help="Week number of birthday (1--52)")
    parser.add_argument("--age", "-a", type=int, default=0,
                        help="Your current age")
    parser.add_argument("--years", "-y", type=int, default=78,
                        help="Years you expect to live")
    parser.add_argument("--title", "-t", type=str, default="momento mori",
                        help="The document title")
    parser.add_argument("--outfile", "-o", type=argparse.FileType("w"), default=sys.stdout,
                        help="File to write to")
    args = parser.parse_args()

    main(args)
