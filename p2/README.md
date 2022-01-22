# Project 2 (P2)

# WARNING: Unless you took a time portal to become my student in the past, this is not the correct repository :) Please go to the correct github repository for the current semester. If you are a Fall'21 semester student though, you are in the right place.

## Clarifications/Corrections

**Find any issues?** Report to us:

- ASHWIN MARAN <amaran@wisc.edu>
- ZACHARY BAKLUND <baklund@wisc.edu>

## Learning Objectives

This project will walk you through the concept and the application of:
- Arithmetic operators, including the *floor division* operator.
- The `type` function that returns the type of some expression.
- Logic operators such as `and` and `or`.
- Comparison operators.

## Overview

In this project, you'll learn about types, operators, and boolean
logic.  To start, create a `p2` directory, and download `main.ipynb`
and `test.py` to that directory (IMPORTANT: use the same process to
download that you used for [p1](https://github.com/msyamkumar/cs220-f21-projects/tree/main/p1#step-1-download-project-files), 
which involves left-clicking the files
and then right-clicking the "Raw" button).

You will work on `main.ipynb` and hand it in. You **should not change**
`test.py`, and you **should not hand it in**.

After you've downloaded both files to `p2`, open a terminal window and
use `cd` to navigate to that directory. You will likely need to
review the steps you used to cd to `p1` for the previous project, then
adapt those steps for `p2`. To make sure you're in the correct
directory in terminal, type `ls` and make sure you see `main.ipynb`
and `test.py` listed.

Now run the following command:

```
python test.py
```

You should see the following output:

```
Summary:
  Test 1: PASS
  Test 2: no outputs in an Out[N] cell
  Test 3: PASS
  Test 4: no outputs in an Out[N] cell
  Test 5: no outputs in an Out[N] cell
  Test 6: no outputs in an Out[N] cell
  Test 7: no outputs in an Out[N] cell
  Test 8: no outputs in an Out[N] cell
  Test 9: no outputs in an Out[N] cell
  Test 10: expected to find type int but found type str
  Test 11: expected ':-(:-):-):-)' but found ':-(:-(:-(:-)'
  Test 12: expected to find type int but found type str
  Test 13: expected 49 but found 343
  Test 14: no outputs in an Out[N] cell
  Test 15: expected True but found False
  Test 16: expected True but found False
  Test 17: expected True but found False
  Test 18: expected to find type bool but found type int
  Test 19: expected True but found False
  Test 20: no outputs in an Out[N] cell

TOTAL SCORE: 10.00%

```

This means if you turn in `main.ipynb` now, you'll get 10% for your score.
Pretty good for having done nothing yet, no?

You would get 10% because there are 20 problems, each worth 5%, and we
have done problems 1 and 3 for you.  You can see this because the
output above says "PASS" by them.  Your goal is to get more points by
getting test.py to print "PASS" by more problems.  In some cases, you
can see there is no answer in the original notebook (when it says `no
outputs in an Out[N] cell`), and in other cases you need to make a
change to correct a wrong answer (e.g., when it says `expected 49 
but found 343`).

Now let's open a second terminal window (we want one to run Jupyter
and one to run the tests).  In the second one, perform the same steps
to navigate to `p2` (again checking with `ls`).  Now run `jupyter
notebook` (or, if that doesn't work, try `python -m jupyter
notebook`, or perhaps `python3 -m jupyter notebook`).

Try solving the second question.  Then do a `Kernel` > `Restart & Run
All`.  If that looks good, save your work, switch to your other
terminal, and run the tests.  Make sure you're scoring 15% before
proceeding to the other questions. (if it appears the test did not 
change from when you ran your tests in the notebook make sure to SAVE)

#### Please remember to `Kernel->Restart and Run All` to check for errors, save your notebook, then run the `test.py` script one more time before submitting the project.

Finally, __if you are unable to solve a question and have partial code that is causing an error__
when running test.py, please __comment out the lines in the cell for that question.__
Failing to do so will cause the auto-grader to fail when you submit your file
and give you 0 points even if you have some questions correctly answered.

Have fun, and run `test.py` often to track your progress!
