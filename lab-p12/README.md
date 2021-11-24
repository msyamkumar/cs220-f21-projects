# Lab 12: Lint, Time, Cashing and Creating DataFrames

In this lab, you'll learn these things:

1. How to use a linter to make your code better.
2. How to measure the runtime of your code.
3. How to cache data onto your computer. 
4. How to construct DataFrames in different ways.
5. How to write one long line of Python code on multiple lines.

<h2> Corrections/Clarifications
</h2>

None yet.

**Find any issues?** Report to us:

- Brian Huang <thuang273@wisc.edu>
- Yelun Bao <ybao35@wisc.edu>
- Soumya Suvra Ghosal <sghosal2@wisc.edu>

## Lint

"Lint" refers to bad code that is not necessarily buggy (though "bad"
coding style often leads to bugs).  A linter helps warn you about
common issues. If you are interested in finding out about the origins
of this term, check out the [Wikipedia page](https://en.wikipedia.org/wiki/Lint_(software)).

For project p12, we're adding a linter as part of `test.py`.
It will notify you of code that is bad style, deducting 1% per issue
(for a max of a 10% penalty).  You can also run the linter yourself,
apart from the tests.  Let's do that now.

You should first install the `pylint` module. You can do that with the command
```
pip install pylint
```

from your Terminal/PowerShell window.

**Reminder:** Based on your Python setup, you might need to use `pip3` instead of `pip`.

After downloading the module `pylint`, you need to download the file
[`lint.py`](https://github.com/msyamkumar/cs220-f21-projects/tree/master/lab-p12/lint.py)
from this repository.

In a new notebook (e.g., named `lint_nb.ipynb`), paste the following code:

```python
def abs(list):
    # Objective: return a new list, which contains absolute values of 
    #            items from the original list
    list = list[:] # copy it
    for i in range(len(list)):
        if list[i] < 0:
            list[i] = -list[i]
    return list

abs([-1, -3, 5, -4, 8])
```

Now open your terminal (Windows: PowerShell, Mac: Terminal), navigate to the directory you are currently working on (the folder which contains the `lint_nb.ipynb` and `lint.py`), and run the linter: `python lint.py -v lint_nb.ipynb` (change the name
if necessary).  Consider why the linter is complaining, then write a
better version of the function to make the linter happy. Recall that any word with green syntax highlighting in jupyter notebook is a Python keyword. You should not be using such words as variable names or function names.

You can find extensive documentation for the file `lint.py`
[here](https://github.com/msyamkumar/cs220-f21-projects/tree/main/linter). If you find the linter confusing, 
please read the full documentation there!

## Timing

Import the `time` module; this module contains a function also called
`time`.

```python
import time
```

Call the time function:

```python
time.time()
```

You should get something like `1617759420.5367446`.  Call it again.
You'll get a slightly different number the second time (e.g.,
`1617759437.1342952`).

The function is returning the number of seconds that have passed since
January 1st, 1970.  That's not that useful by itself, but people often
call `time.time()` twice, then subtract to find out how much time has
passed.  This is one common way to learn how efficient your code is.
You'll generally do something like this:

```python
t1 = time.time()
# some code we want to measure
t2 = time.time()
t2 - t1
```

The result on the last line will be the number of seconds it takes to
execute the code between the two `time.time()` calls.

### Measuring Addition

Let's experiment with measuring the time it takes to add the numbers
0, 1, 2, 3, 4, 5, 6, 7, 8, and 9.  We'll multiply seconds by 1000 to
get milliseconds:

```python
t1 = time.time()

sum = 0
limit = 10 # try changing this
for i in range(limit):
    sum += i

t2 = time.time()

print("SUM:", sum)
milliseconds = (t2 - t1) * 1000
print("ms:", milliseconds)
```

What if we wanted to add numbers 1 through 100?  Try changing the
value for the `limit` variable above, and observe whether the code
runs for more milliseconds.

Keep increasing the limit by factors of 10 until it takes
about 1 second to run.  How many numbers can you add in
one second on your computer?


### Measuring Web Requests and File Usage

import `requests` module in the same cell that you used to import `time` module:

```python
import requests
```

Copy the following code snippet and paste it three times, in three
separate cells:

```python
t1 = time.time()

# code to measure

t2 = time.time()

milliseconds = (t2-t1) * 1000
print("ms:", milliseconds)
```

In each cell, replace `# code to measure` with one of the following
(in this order):

```python
r = requests.get("https://raw.githubusercontent.com/msyamkumar/cs220-f21-projects/main/lab-p12/hello.txt")
r.raise_for_status()
data = r.text
```

```python
f = open("hello.txt", "w", encoding="utf-8")
f.write(data)
f.close()
```

```python
f = open("hello.txt", encoding="utf-8")
data = f.read()
f.close()
```

How long did the code that does a GET request using the `requests`
module take compared to the cells accessing a file on your own
computer?  It's quite likely that fetching data from the Internet took
10x longer.

### Relevance to p12

Because fetching data from the Internet is so slow, your web browser
tries to avoid downloading things more than necessary.  So, the first
time you visit a page, the web browser will download the content, and
also save it on your computer.  If you need to view the same page
again soon, your browser may use the file on your computer instead of
re-fetching the original.  This technique is called **caching**.

## Implementing Caching

We will now implement a `download` function with caching. Make sure to move import `os` to the cell with import statements.
```python
import os

def download(filename, url):
    # We do not download again if the file already exists
    if os.path.exists(filename):
        return (str(filename) + " already exists!")

    # TODO: Write the code to download the file from URL
    # and save it in `filename`
    # Make sure to call the function that checks for 200 status_code

    return (str(filename) + " created!")
```

Now call `download("hello.html", "https://raw.githubusercontent.com/msyamkumar/cs220-f21-projects/main/lab-p12/hello.html")`.
You should be able to see `hello.html` in your Explorer/Finder.


### Relevance to p12

You will have to use this `download` function to download files during p12. This will ensure
that you do not download the files each time you 'Restart & Run All'.

## Creating DataFrames

Do your pandas setup:

```python
import pandas as pd
from pandas import DataFrame, Series
```

There are many ways to create pandas DataFrames.  Here are four ways
involving data structures, you are familiar with (basically every
combination of nesting):

1. `list` of `lists`
2. `dict` of `lists`
3. `list` of `dicts`
4. `dict` of `dicts`

We used to load CSV tables to lists of lists (option 1).  In that case, the list
of lists served as a list of rows.  It works the same for a DataFrame.
Try it!

```python
# option 1
DataFrame([[1, 2], [3, 4]])
```

In options 2 and 3, we have a mix of lists and dicts.  The important
thing to remember is this: **when the outer data structure is a list, inner
data structures represent rows (similar to CSVs); when the outer data structure 
is a dict, inner data structures represent columns.** Depending on whether the inner
data structures represent rows or not, you will get row index and column name information accordingly.

This means both of these give us the same:

```python
# option 2
DataFrame({"x" : [1, 3],
           "y" : [2, 4]})
```

and

```python
# option 3
DataFrame([{"x" : 1, "y" : 2},
           {"x" : 3, "y" : 4}])
```

Then, we have a dict of dicts.  In this case, keys of the
outer dict will be the column names of the DataFrame, and the keys of the
inner dicts will be the row index of the DataFrame.  Try it!

```python
# option 4
DataFrame({"x" : {"A" : 1, "B" : 3},
           "y" : {"A" : 2, "B" : 4}})
```

Finally, here is how you can configure row indices and column names:

```python
# revised option 1
DataFrame([[1, 2], [3, 4]], columns = ["x", "y"], index = ["A", "B"])
```

*Try changing values and visualizing the changes to the DataFrames.*

## Boolean Indexing

Download [`cs220_survey_data.csv`](https://github.com/msyamkumar/cs220-f21-projects/tree/master/lab-p12/cs220_survey_data.csv).
The following code enables us to read the contents of `cs220_survey_data.csv` into a DataFrame. Paste the code into a new cell:

```python
survey_data = pd.read_csv("cs220_survey_data.csv")
```

Let's go through examples to recall the concept of Boolean indexing

## Wrapping Lines in Python

Sometimes in Python you may need to write a very long line of code.  
For the sake of readability, it may be better to take one line of code and write on more than one line.

Copy and run this example:
```python
lyrics = "On, Wisconsin! On, Wisconsin! Plunge right through that line!"
lyric_list = lyrics.split(" ")
lyric_list

# use a comprehension to make a list of all words that:
#   start with a lowercase letter, 
#   the last char is not '!' or ','
#   have a length > 2

[word for word in lyric_list if word[0] == word[0].lower()  \
 and word[-1] not in ["!", ","] and len(word) > 2]
```

Notice that the `\` character at the end of a line allows you to wrap a line of code onto the next line.
Experiment with moving the `\` character.  Remove it, place it somewhere else, then try to extend the code to 3 lines.

You will be writing long lines of code in p12, and this will help make your code easier to read.


**Note:** Run `lint.py` once again, and clear the all warnings from the linter. This will be good practice for p12.

### Project hints

* In p12, you will need to use the `download` function as described already. Make sure that your function does **not** download files that have already been downloaded.
* Using Pandas for this project, you can solve most of the questions in this project very efficiently (i.e. with a couple of lines of code). 
* You should use Boolean indexing of appropriate DataFrame to answer questions in this project. You will lose points during code review if you use conditional statements or loops.
* You might want to review the code from Pandas lectures or rewatch the lectures on Pandas (specifically boolean indexing).
* Note: sometimes you will be using lists and other data structures to manipulate the Series / DataFrame to answer questions. You may use for loops when the question description or code specifies you to use for loops. Both of these scenarios would be considered acceptable.

**Good luck!**
