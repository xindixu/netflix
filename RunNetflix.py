#!/usr/bin/env python3

# -------
# imports
# -------

from Netflix import netflix_eval
import sys

# ----
# main
# ----

if __name__ == "__main__":
    netflix_eval(sys.stdin, sys.stdout)


""" #pragma: no cover
% cat RunNetflix.in
10040:
2417853
1207062
2487973



% RunNetflix.py < RunNetflix.in > RunNetflix.out



% cat RunNetflix.out
10040:
2.4
2.4
2.4
0.90



% pydoc3 -w Netflix
# That creates the file Collatz.html
"""
