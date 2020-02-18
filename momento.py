#!/usr/bin/env python3

"""
Generates a PDF with all the weeks of an average human lifespan in the US.
If a birthday is provided (in ISO-8601 format), the calendar will be customized to it, including clipping the first row to your actual birth week, and marking off the weeks you have already lived.

Usage:

    ./momento.py [-b YYYY-MM-DD] [-y YY] > momento.tex
    pdflatex momento

which produces a printable A4-size PDF in `momento.pdf`.

Command-line arguments:

- `-b` is your birthdate in ISO-8601 format
- `-y` is an expected lifespan (default: 78)

Author: Matt Post
"""

import sys

from datetime import datetime
from typing import List

template_header = r"""\documentclass{article}

\usepackage[a4paper, total={6.5in, 9in}]{geometry}
\usepackage{adjustbox}
\usepackage{graphicx}
\usepackage{pdfpages}
\usepackage{booktabs}
\usepackage{colortbl}

\pagestyle{empty}

\begin{document}

\noindent MOMENTO MORI

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

    if args.birthday is not None:
        birthday = datetime.strptime(args.birthday, "%Y-%m-%d")
        birth_week = int(birthday.strftime("%U"))
        age = get_age(birthday, today)
        header_label_until = 52
    else:
        birth_week = 0
        age = 0
        header_label_until = 0

    ## Print the header
    table = ""
    color = "white"
    print(template_header, file=args.outfile)
    print(fr"  \cline{{{birth_week+1}-52}}", file=args.outfile)

    if birth_week > 0:
        print(fr"  \multicolumn{{{birth_week}}}{{c|}}{{}} & ", file=args.outfile)
    print(" & ".join(build_cells(color=color, num=52-birth_week, label_until=header_label_until)), r" \\", file=args.outfile)
    print(fr"  \cline{{1-52}}", file=args.outfile)

    ## Print the years
    for year in range(2, args.years + 1):
        if year % 10 == 0:
            color = DECADE_COLOR
            if args.birthday:
                finalcol = rf" & {birthday.year + year} \\"
            else:
                finalcol = rf" & {year} \\"
        else:
            color = "white"
            finalcol = r" \\"

        if args.birthday is None or year > age + 1:
            label_until = 0
        elif year == age + 1:
            label_until = current_week
        else:
            label_until = 52

        print("  ", " & ".join(build_cells(color=color, label_until=label_until)), finalcol, file=args.outfile)
        print(fr"  \cline{{1-52}}", file=args.outfile)

    print(template_footer, file=args.outfile)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--birthday", "-b" , type=str, default=None,
                        help="Birthday in ISO-8601 format (YYYY-MM-DD)")
    parser.add_argument("--years", "-y", type=int, default=78,
                        help="Years you expect to live")
    parser.add_argument("--outfile", "-o", type=argparse.FileType("w"), default=sys.stdout,
                        help="File to write to")
    args = parser.parse_args()

    main(args)
