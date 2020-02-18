# Introduction

One day you will die.
It's worth keeping in mind.
This project will generate an A4-sized sheet of paper with a grid containing one square for every week of your expected life (which defaults to 78 years).
If you provide your birthdate, it will `x` out the ones that have passed and are therefore only part of your fading memory.

![Picture of a skull](skull.jpg)

# Usage

The script generates a LaTeX file:

    ./momento.py > page.tex

You can tell it how many years to generate (default: 78) and have it `x` off the weeks you've lived if you provide a birthdate:

    ./momento.py -y 84 -b 1980-07-04 > page.tex

Compile with `pdflatex`:

    pdflatex page.tex

This will produce a file, `page.pdf`, which you can print out and hang somewhere prominent.
