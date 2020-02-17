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

\usepackage[letterpaper, total={6.5in, 10in}]{geometry}
\usepackage{adjustbox}
\usepackage{graphicx}
\usepackage{pdfpages}
\usepackage{booktabs}
\usepackage{colortbl}

\pagestyle{empty}

\begin{document}

\begin{table}[p]
  \begin{adjustbox}{max width=\textwidth}
  \begin{tabular}{|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c}
"""
#   \multicolumn{53}{c}{\LARGE MOMENTO MORI\newline} \\

template_footer = r"""
  \end{tabular}
  \end{adjustbox}
\end{table}

\end{document}
"""

default_color = "white"


def build_cells(color=default_color, num=52, label_until=52) -> List[str]:
    cells = []
    for weekno in range(1, num + 1):
        label = "x" if weekno <= label_until else ""
        cells.append(fr"\cellcolor{{{color}}}{label}")
    return cells

def main(args):
    current_week = int(datetime.utcnow().strftime("%U"))

    table = ""
    color = "white"
    print(template_header, file=args.outfile)
    print(fr"  \cline{{{args.birth_week+1}-52}}", file=args.outfile)
    print(fr"\multicolumn{{{args.birth_week}}}{{c|}}{{}} & ", file=args.outfile)
    print(" & ".join(build_cells(color=color, num=52-args.birth_week, label_until=52)), r" \\", file=args.outfile)
    print(fr"  \cline{{1-52}}", file=args.outfile)

    for year in range(2, args.years):
        if year % 10 == 0:
            color = "gray!25"
            finalcol = rf" & {year} \\"
        else:
            color = "white"
            finalcol = r" \\"

        if year <= args.age:
            label = "x"
        else:
            label = ""

        if year > args.age + 1:
            label_until = 0
        elif year == args.age + 1:
            label_until = current_week
        else:
            label_until = 52

        print(" & ".join(build_cells(color=color, label_until=label_until)), finalcol, file=args.outfile)
        print(fr"  \cline{{1-52}}", file=args.outfile)

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
