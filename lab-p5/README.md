# Lab P5: Looping Patterns and Hurricane API

This lab will introduce you to some fundamental looping patterns
that will be helpful in solving p5. 
It is designed to help you get comfortable
with using functions in `project.py` for p5. 
You will also learn basic methods to manipulate strings
that will be helpful in solving p5.

## Corrections and clarifications

None yet. 

**Find any issues?** Report to us: 

- Dyah Adila <adila@wisc.edu>
- Parker Lougheed <plougheed@wisc.edu>

## Project API

The `project.py` file helps give you access
to the dataset you'll use this week, `hurricanes.csv`.
Start by looking at the hurricane dataset
[here](https://github.com/msyamkumar/cs220-f21-projects/blob/main/lab-p5/hurricanes.csv).
This data is a summary of statistics pulled from the 
[List of United States hurricanes](https://en.wikipedia.org/wiki/List_of_United_States_hurricanes) 
on Wikipedia.

Look through the dataset for a recent hurricane, such as hurricane Delta (at index 66),
and briefly familiarize yourself with some of the numbers.
The data shows name, the date of formation, the date of dissipation, 
max wind speed (in MPH), damage (in US dollars), and deaths. 
Note that the death stats are usually direct deaths, 
meaning they don't count deaths that occur after the storm due to, say
infrastructure damage to hospitals.

Often, we'll organize data by assigning numbers (called indexes)
to different parts of the data (e.g., rows or columns in a table). In
Computer Science, indexing typically starts with the number 0 (zero);
i.e., when you have a sequence of things, you'll start counting them
from 0 (zero) instead of 1 (one).
Thus, you should **ignore the numbers shown by GitHub to the left of the rows**.
From the perspective of `project.py`, the indexes of Baker, Camille, and Eloise
are 0, 1, and 2 respectively (and so on).

Download
[hurricanes.csv](https://github.com/msyamkumar/cs220-f21-projects/blob/main/lab-p5/hurricanes.csv)
and
[project.py](https://github.com/msyamkumar/cs220-f21-projects/blob/main/lab-p5/project.py)
to a `lab5` directory that you create, 
and start a new notebook in that directory for some scratch work.

Run the following in cells to explore the API:

```python
import project
dir(project)
```

Spend a little time reading about each of the six functions that don't
begin with two underscores. 
For example, run this to learn about `count`:

```python
help(project.count)
```

or alternatively, you could run the following to just see the function's documentation:

```python
print(project.count.__doc__)
```

You may also open up the `project.py` file directly
to learn about the functions provided.
E.g., you might see this:

```python
def count():
    """This function will return the number of records in the dataset"""
    return len(__hurricane__)
```

You don't need to understand the code in the functions, 
but the strings in triple quotes (called *docstrings*) 
explain what each function does.
As it turns out, all `project.count.__doc__` is doing
is providing you the the docstring for the `count` function.

Try learning the project API, by running the following
(in each case, make sure you have the `hurricanes.csv` file open in GitHub
and find where the data returned by the function call is coming from):

1. `project.get_name(0)`
2. `project.get_name(1)`
3. `project.get_mph(0)`
4. `project.get_deaths(0)`
5. `project.get_damage(0)`
6. `project.get_damage(1)`

For 5 and 6, note that the damage amount ends with "M" and "B" respectively.
In this dataset, "K" represents one thousand, 
"M" represents one million, and "B" represents one billion.
In the project, you'll need to convert these strings to the appropriate ints
(e.g., `"1.5K"` will become `1500`).

7. `project.get_name(project.count())`

Oops, 7 failed!
Can you change the code so that you get
the name of the last hurricane (in this case, "OMar")?

## Loop Warmups

You're going to need to write lots of loops for this project. 
We'll walk you through some examples here that will help you later.

### 1. Using `for` and `range`

Run this snippet and observe the output:

```python
i = 0
while i <= 5:
    print(i)
    i += 1
```

Your job is to replace the `???` parts below to create a loop
that does the same thing:

```python
for ??? in range(???):
    ???
```

Make sure the last number printed is exactly the same
with both code snippets!

### 2. When to use `range`

Consider these two loops:

Loop A:

```python
s = "bahahaha"
for x in s:
    pass # TODO
```

Loop B:

```python
s = "bahahaha"
for i in range(len(s)):
    pass # TODO
```

Now imagine two different problems.

1. You need to print every letter in `s` on its own line
2. You need to print the index of every "h" in `s` on its own line

Which loop is the easier starting point for each problem?
Give it a try, and discuss with your partner or classmates.

### 3. Looping over indexes and values

You want a loop that prints the index of every row index in `hurricanes.csv`
(from 0 to 140, inclusive):

```python
for idx in range(???):
    print(idx)
```

Your job is to replace the `???` parts below with
a call to one of the functions in the `project` module.

Your next task is to complete the following loop so it
prints the name of every hurricane in the dataset:

```python
for idx in range(???):
    name = ???
    print(name)
```

Both places where `???` occurs should be replaced with
calls to functions in `project`.

### 4. Filtering data

Your job is to replace the `???` parts below
so that the name of every hurricane with a speed under 80 mph is printed.

```python
for i in range(???):
    if ???:
        print(project.get_name(i))
```

### 5. Finding a maximum or minimum

Replace `???` so that the code does what the comments say it should do:

```python
def f(n):
    return 3 + n % 7

# we want to find the integer n in the range of 0 to 10 (including 10)
# such that f(n) is largest.
best_n = 0
for n in range(11):
    if ???:
        best_n = n

print(best_n)
```

Now, can you modify the function so that it finds the integer n such 
that f(n) is the *smallest*?

### Working with strings

We have seen how several of the functions in `project.py` work. 
We have not yet looked at the functions `get_formed()` and `get_dissipated()`.
Let us do that now. Run each of the following in its own cell:

1. `project.get_formed(0)`
2. `project.get_dissipated(0)`

The dates are represented in the standard mm/dd/yyyy notation. 
This date is represented as a string. 
Note that the dates have been formatted so that two digits are used
to represent the month/date even when the month/date can be
represented using only one digit. 
So, `'9/1/1950'` is represented as `'09/01/1950'`.
This is to make it easier to extract data from the string.
Run the following code:

```python
print(project.get_formed(0)[:2])
```

The above code displays the month in which the hurricane at index 0 was formed. 
Can you guess what the following code does?

```python
print(project.get_formed(0)[-4:])
```

### Creating some helper functions

We will now create three functions that will be useful
for dealing with dates in p5.
Copy/paste the following code into your notebook and finish the TODOs:

```python
def get_month(date):
    """Returns the month when the date is the in the 'mm/dd/yyyy' format"""
    return int(date[:2])


def get_day(date):
    """Returns the day when the date is the in the 'mm/dd/yyyy' format"""
    pass  # TODO: Use string slicing to return the day


def get_year(date):
    """Returns the year when the date is the in the 'mm/dd/yyyy' format"""
    pass  # TODO: Use string slicing to return the year
```

When you are done with the functions, think of some test cases
(e.g., `get_year("10/06/2021")`) to make sure they are correct.
You may copy these functions to your project notebook if you like.

### Working with Python's module for manipulating dates and times

We will now introduce you to Python's [`datetime` module]((https://docs.python.org/3/library/datetime.html))
that allows easy manipulation and operations of dates for use in p5.
Paste the following function within your notebook, and call it:

```python
import datetime

def get_number_of_days(start_date, end_date):
    """Gets the number of days between the start_date (in 'mm/dd/yyyy' format) and end_date (in 'mm/dd/yyyy' format)"""
    day1 = datetime.datetime.strptime(start_date, '%m/%d/%Y') # The second argument is a format string to tell the function how to process the date string
    day2 = datetime.datetime.strptime(end_date, '%m/%d/%Y')
    delta = day2 - day1
    return delta.days
```

The above code allows you to find the number of days between two dates. 
It might be trivial to find the day difference between 08/01/2021 and 08/12/2021. 
But, how about 04/20/2021 and 08/12/2021? With th function above, you can call:

```python
get_number_of_days('04/20/2021', '08/12/2021')
```

The function `get_number_of_days` uses the `datetime` module 
to calculate this for us with just 2 steps:

1. Convert the date strings into the datetime format
   that the module can process and manipulate
   (`datetime.datetime.strptime`).

2. Directly subtract them
   in the datetime format (`day2 - day1`), 
   and return the number of days (`delta.days`).

The `datetime` module can do a lot more
manipulation and computations with date formats. 
However, for this lab and project, 
you just need to know the ones we have discussed above.

---

You are now ready to take on [p5](https://github.com/msyamkumar/cs220-f21-projects/tree/main/p5)!
Remember to only work with at most one partner on p5 from this point on. 
Have fun!
