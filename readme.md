# SBF Fragen Tester
Parses questions from the german sporting boat license as html and addes them sqlite db.
It can also serve a tiny frontend which shows a random question and lets the user choose an answer.

## Status
Basic functionality works but its quite a in between project.


## Usage

parser.py [-h] [-p] [-s] [file_name]

Process HTML files or serve the application.

positional arguments:
  file_name    Name of the HTML file to parse (optional)

options:
  -h, --help   show this help message and exit
  -p, --parse  Parse an HTML file
  -s, --serve  Serve the application

## Sources
Based on Fragen from "Stand: 01. August 2023"

I took the questions from:
https://www.elwis.de/DE/Sportschifffahrt/Sportbootfuehrerscheine/Fragenkatalog-See/Fragenkatalog-See-neu-node.html

