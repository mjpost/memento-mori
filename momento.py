#!/usr/bin/env python3
"""

Usage: ./momento.py [-b] [-y] [-t]
where


Author: Matt Post
"""


import sys
from datetime import datetime
from typing import List

template_header = r"""\documentclass{article}

\usepackage[letterpaper, total={6.5in, 9in}]{geometry}
\usepackage{adjustbox}
\usepackage{graphicx}
\usepackage{pdfpages}
\usepackage{booktabs}
\usepackage{colortbl}

\pagestyle{empty}

\begin{document}

MOMENTO MORI

\begin{table}[h!]
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

DEFAULT_COLOR = "white"
DECADE_COLOR = "gray!10"

def build_cells(color=DEFAULT_COLOR, num=52, label_until=52) -> List[str]:
    cells = []
    for weekno in range(1, num + 1):
        label = "x" if weekno <= label_until else ""
        cells.append(fr"\cellcolor{{{color}}}{label}")
    return cells


def get_age(birthday, today) -> int:
    return today.year - birthday.year - 1 + (today.month >= birthday.month and today.day >= birthday.day)


def main(args):
    today = datetime.utcnow()
    current_week = int(today.strftime("%U"))
    birthday = datetime.strptime(args.birthday, "%Y-%m-%d")
    birth_week = int(birthday.strftime("%U"))
    age = get_age(birthday, today)

    ## Print the header
    table = ""
    color = "white"
    print(template_header, file=args.outfile)
    print(fr"  \cline{{{birth_week+1}-52}}", file=args.outfile)
    print(fr"\multicolumn{{{birth_week}}}{{c|}}{{}} & ", file=args.outfile)
    print(" & ".join(build_cells(color=color, num=52-birth_week, label_until=52)), r" \\", file=args.outfile)
    print(fr"  \cline{{1-52}}", file=args.outfile)

    ## Print the years
    for year in range(2, args.years):
        if year % 10 == 0:
            color = DECADE_COLOR
            finalcol = rf" & {year} \\"
        else:
            color = "white"
            finalcol = r" \\"

        if year <= age:
            label = "x"
        else:
            label = ""

        if year > age + 1:
            label_until = 0
        elif year == age + 1:
            label_until = current_week
        else:
            label_until = 52

        print(" & ".join(build_cells(color=color, label_until=label_until)), finalcol, file=args.outfile)
        print(fr"  \cline{{1-52}}", file=args.outfile)

    print(template_footer, file=args.outfile)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--birthday", "-b" , type=str, default="2000-01-01",
                        help="Birthday in ISO-8601 format (YYYY-MM-DD)")
    parser.add_argument("--years", "-y", type=int, default=78,
                        help="Years you expect to live")
    parser.add_argument("--title", "-t", type=str, default="momento mori",
                        help="The document title")
    parser.add_argument("--outfile", "-o", type=argparse.FileType("w"), default=sys.stdout,
                        help="File to write to")
    args = parser.parse_args()

    main(args)
