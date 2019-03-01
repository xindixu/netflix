#!/usr/bin/env python3

# -------
# imports
# -------
from Netflix import netflix_eval
from unittest import main, TestCase
from math import sqrt
from io import StringIO
from numpy import sqrt, square, mean, subtract

# -----------
# TestNetflix
# -----------


class TestNetflix (TestCase):

    # ----
    # eval
    # ----

    def test_eval_1(self):
        r = StringIO("10040:\n2417853\n1207062\n2487973\n")
        w = StringIO()
        netflix_eval(r, w)
        self.assertEqual(
            w.getvalue(), "10040:\n3.6\n3.5\n3.9\n0.89\n")

    # test if it works when there is only one customer
    def test_eval_2(self):
        r = StringIO("9999:\n1473765\n")
        w = StringIO()
        netflix_eval(r, w)
        pred = w.getvalue().split('\n')
        self.assertEqual(len(pred), 4)

    # test if rmse is less than 1
    def test_rmse(self):
        r = StringIO("1:\n30878\n2647871\n1283744\n")
        w = StringIO()
        netflix_eval(r, w)
        rmse = float(w.getvalue()[-5:])
        self.assertTrue(rmse < 1)


# ----
# main
# ----
if __name__ == '__main__':
    main()

""" #pragma: no cover
% coverage3 run --branch TestNetflix.py >  TestNetflix.out 2>&1



% coverage3 report -m                   >> TestNetflix.out



% cat TestNetflix.out
.
----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
Name             Stmts   Miss Branch BrPart  Cover   Missing
------------------------------------------------------------
Netflix.py          27      0      4      0   100%
TestNetflix.py      13      0      0      0   100%
------------------------------------------------------------
TOTAL               40      0      4      0   100%

"""
