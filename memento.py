#!/usr/bin/env python3

"""
Generates a PDF with all the weeks of an average human lifespan in the US.
If a birthday is provided (in ISO-8601 format), the calendar will be customized to it, including clipping the first row to your actual birth week, and marking off the weeks you have already lived.

Usage:

    ./memento.py [-b YYYY-MM-DD] [-y YY] > memento.tex
    pdflatex memento

which produces a printable A4-size PDF in `memento.pdf`.

Command-line arguments:

- `-t` sets the title displayed in the upper left
- `-b` is your birthdate in ISO-8601 format
- `-y` is an expected lifespan (default: 78)
- `--background FILE` use the specified background image and rasterize to the grid
- `--opacity FLOAT` is the opacity to use for the background image
- `--watermark FILE` uses a watermark image behind the table instead

Author: Matt Post
"""

import sys

from datetime import datetime
from PIL import Image
from typing import List

template_header = r"""\documentclass{{article}}

\usepackage[a4paper, total={{6.5in, 9in}}]{{geometry}}
\usepackage{{adjustbox}}
\usepackage{{graphicx}}
\usepackage{{pdfpages}}
\usepackage{{booktabs}}
\usepackage{{colortbl}}
\usepackage[pages=all]{{background}}

\pagestyle{{empty}}
\setlength\minrowclearance{{6pt}}
\setlength{{\arrayrulewidth}}{{1.2pt}}

{WATERMARK}

\begin{{document}}

% \noindent {TITLE}

\begin{{table}}[ht!]
  \begin{{adjustbox}}{{max width=\textwidth}}
  \begin{{tabular}}{{|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c}}
"""
#   \multicolumn{53}{c}{\LARGE MEMENTO MORI\newline} \\

template_footer = r"""
  \end{tabular}
  \end{adjustbox}
\end{table}

\end{document}
"""

DEFAULT_COLOR = "white!10"
DECADE_COLOR = "gray!10"

def build_cells(colors=None,
                title="",
                row=1,
                startcol=1,
                endcol=52,
                label_until=52) -> List[str]:
    cells = []
    if startcol != 1:
        cells.append(fr"\multicolumn{{{startcol-1}}}{{r|}}{{{title}}}")
    for weekno in range(startcol, endcol + 1):
        label = r"\textbf{X}" if weekno <= label_until else r"\phantom{\textbf{X}}"
        try:
            color = colors[weekno-1][row-1] if colors else ""
        except:
            # might be beyond length of image
            color = ""
        cells.append(f"{color}{label}")

    if endcol != 52:
        cells.append(fr"\multicolumn{{{52-endcol}}}{{|l}}{{}}")

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

    # Figure out background or watermark
    colors = None
    if args.background:
        img = Image.open(args.background)
        width, height = img.size

        # Resize image
        if width != 52:
            height = int(img.size[1] / (img.width / 52))
            print(f"Resizing image from ({width},{img.size[1]}) to (52,{height})", file=sys.stderr)
            width = 52
            img = img.resize((width, height))

        # Center the image vertically, padding it with the color in the upper right of the original image (assumed to be the background color)
        if height < args.years:
            new_image = Image.new("RGB", (width, args.years), img.getpixel((51, 0)))
            new_image.paste(img, (0, (args.years - height) // 2))
            img = new_image
            height = args.years

        colors = [["" for y in range(height)] for x in range(width)]

        for x in range(width):
            for y in range(height):
                r, g, b = list(map(lambda x: ((255 - ((255 - x) * args.opacity)) / 255), img.getpixel((x, y))))[0:3]
                colors[x][y] = fr"\cellcolor[rgb]{{{r:.2f},{g:.2f},{b:.2f}}}"

    color = DEFAULT_COLOR
    WATERMARK = ""
    if args.watermark:
        WATERMARK = rf"""\backgroundsetup{{
scale=0.85,
color=black,
opacity=0.05,
angle=0,
contents={{%
  \includegraphics[width=\paperwidth,height=\paperheight]{{{args.watermark}}}
  }}%
}}"""

    ## Print the header
    # startcol = birth_week
    startcol = max(len(args.title) // 2, birth_week)
    print(template_header.format(WATERMARK=WATERMARK, TITLE=args.title), file=args.outfile)
    print(fr"  \cline{{{startcol}-52}}", file=args.outfile)

    print(" & ".join(build_cells(row=1, title=args.title, startcol=startcol, label_until=header_label_until, colors=colors)), r" \\", file=args.outfile)
    print(fr"  \cline{{1-52}}", file=args.outfile)

    ## Print the years
    for year in range(2, args.years + 1):
        if year % 10 == 0:
            if args.birthday:
                finalcol = rf" & {birthday.year + year} \\"
            else:
                finalcol = rf" & {year} \\"
        else:
            finalcol = r" \\"

        if args.birthday is None or year > age + 1:
            label_until = 0
        elif year == age + 1:
            label_until = current_week
        else:
            label_until = 52

        # adjustments for last row
        weeks_to_print = 52
        if birth_week != 0 and year == args.years:
            weeks_to_print = birth_week

        print("  ", " & ".join(build_cells(row=year, endcol=weeks_to_print, label_until=label_until, colors=colors)), finalcol, file=args.outfile)
        print(fr"  \cline{{1-{weeks_to_print}}}", file=args.outfile)

    # close the table
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
    parser.add_argument("--title", "-t", type=str, default="MEMENTO MORI",
                        help="Page title")
    parser.add_argument("--watermark", type=str,
                        help="File containing watermark image to superimpose")
    parser.add_argument("--background", "-bg", type=str,
                        help="File containing background image (52 pixels wide) to incorporate into the table")
    parser.add_argument("--opacity", type=float, default=1.0,
                        help="Opacity of background image")
    args = parser.parse_args()

    if args.background and args.watermark:
        print("I can only take exactly one of --watermark and --background|-bg", file=sys.stderr)
        sys.exit(1)

    main(args)
