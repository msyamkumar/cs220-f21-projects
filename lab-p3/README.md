# Lab 3: Learning an API

## Corrections

None yet.

**Find any issues?** Report to us: 

- Yelun Bao <ybao35@wisc.edu>
- Hardik Chauhan <hchauhan2@wisc.edu>

## Description

For many projects this semester, we'll provide you with a *module* (a
collection of functions) named `project`, in a file named
`project.py`. This module will provide functions that will help you
complete the project. Today, we'll introduce the `project.py` file for
[p3](https://github.com/msyamkumar/cs220-f21-projects/tree/main/p3).

When using an unfamiliar module, the first thing you should do is
study the module's *API*.  API stands for "Application Programming
Interface", and refers to a collection of related functions (e.g.,
those in a module).  Understanding the API will involve learning about
each function and the parameters it takes.  You might also need to
learn new *protocols* for using the function; protocols specify the
order in which you may call functions.

There are two ways you can learn about an API.  First, the person who
created the API may have provided written directions, called
*documentation*.  Second, there are ways you can write code to learn
about a collection of functions; this approach is called *inspection*.

Summary of new terms:
* module
* API
* protocol
* documentation
* inspection

## Note on Academic Misconduct

You may do these lab exercises with anybody you like.  But be careful!
It's very natural to start working on p3 immediately after completing
the lab.  If you start working with somebody on p3 (after the lab),
that person must be your project partner until the next project; you
are not allowed to start working on p3 with one person during lab,
then finish the project with a different partner.  Now may be a good
time to review [our course
policies](https://www.msyamkumar.com/cs220/f21/syllabus.html).

## Setup

Create a `lab3` directory and download `lab.csv` above.  Also download
these files from the lab page to the `lab3` directory:

* `energy.csv`
* `project.py`

Open a terminal and navigate to your `lab3` directory.  Run `ls` to
make sure your three files are available.

We'll be doing these exercises in interactive mode, so type `python`
(or `python3`, if that's what you need to do on your laptop), and hit
ENTER.

## Inspecting `__builtins__` and `math`

In interactive mode, try the following examples (only type things after the `>>>`).

```python
>>> abs(-4)
4
>>> x = abs(-3)
>>> x
3
```

These two calls invoke the `abs` function because we have parenthesis.
What if we don't use parenthesis?  Try the following and see what you
get:

```python
>>> abs
```

```python
>>> type(abs)
```

What if we want to read about what `abs` does?  Run this:

```python
>>> abs.__doc__
```

Or this (compare the result):

```python
>>> print(abs.__doc__)
```

We didn't need to import anything to use `abs` because it is part of a
special module that is always imported called `__builtins__`.  Try
running this to see:

```python
>>> type(__builtins__)
```

The `dir` function will show you everything that is inside a module,
so let's use it to learn about `__builtins__`.  Run this:

```python
>>> dir(__builtins__)
```

This displays the names of lots of functions we've seen, such as
`abs`, `print`, `int`, `input`, and others.  You'll see some things
that begin and end with `__` (two underscores).  Those are generally things to ignore.
Choose one function from the list that you're familiar with and one
that is unfamiliar to you, and then use `.__doc__` to read the
descriptions for both.  For example, you might learn about `max` like
this:

```python
>>> print(max.__doc__)
max(iterable, *[, default=obj, key=func]) -> value
max(arg1, arg2, *args, *[, key=func]) -> value

With a single iterable argument, return its biggest item. The
default keyword-only argument specifies an object to return if
the provided iterable is empty.
With two or more arguments, return the largest argument.
```

Wow, that mentions a lot of things we haven't learned about yet!  As a
new Python programmer reading documentation, you'll have to dig
through things you don't understand yet to find bits that are useful
for you.  For example, in this case, the last line tells you
everything you need to know: *"With two or more arguments, return the
largest argument."*

Let's give it a try:

```python
max(-1000, 99, 50, 60)
```

Let's see what's in the math module now:

```python
>>> import math
>>> dir(math)
```

Let's see what the `log` function does:

```python
>>> print(math.log.__doc__)
```

As a convention, documentation that displays parameters in brackets
(like `[base=math.e]`) mean that the parameter is optional.  Let's try
calling the `log` function different ways:

1. `math.log(10000, 10)` (positional arguments)
2. `math.log(math.e ** 3)` (positional argument and default argument)
3. `math.log(x=10000, base=10)` (keyword arguments)

Note that the last command fails with `TypeError: log() takes no
keyword arguments`.  Not every function you encounter will support
keyword arguments, unfortunately.

What happens if you run this?

```python
>>> log(10000, 10)
```

It doesn't work because we've imported math with `import math`.  Try
this style instead, then repeat that call:

```python
>>> from math import log
>>> log(10000, 10)
```

We'll still need to use `math.sqrt(4)` instead of `sqrt(4)`, though,
unless we specifically import `sqrt` like we did for `log`.  Or, we
can import everything in math at once:

```python
>>> from math import *
```

Try some other mathematical functions to verify you don't need to
start the calls with `math.`

## Inspecting `project`

Let's check out the `project.py` API you'll use for P3:

```python
>>> import project
>>> dir(project)
['__DictReader',
 '__builtins__',
 '__cached__',
 '__data',
 '__doc__',
 '__energy_to_idx',
 '__file__',
 '__loader__',
 '__name__',
 '__package__',
 '__spec__',
 'dump',
 'get_consumption',
 'get_idx',
 'init']
```

We see there are four functions here (ignoring the things beginning with two underscores):

* `dump`
* `get_consumption`
* `get_idx`
* `init`

What does `dump` do?

```python
>>> print(project.dump.__doc__)
```

Let's try calling it then:

```python
>>> project.dump()
```

You'll get an error:

```python
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "~\Documents\ms\cs220\lab-p3\project.py", line 36, in dump
    raise Exception("you did not call init first")
Exception: you did not call init first
```

Let's figure out what `init` is, then:

```python
>>> print(project.init.__doc__)
```

Looks like it wants us to do this:

```python
project.init("energy.csv")
```

After calling `init`, let's try calling `project.dump()` again.  It
should show this now:

```python
Biomass Energy [Index 7]
  2015: 524.879000 Trillion Btu
  2016: 505.069000 Trillion Btu
  2017: 509.541000 Trillion Btu
  2018: 496.085000 Trillion Btu
  2019: 448.137000 Trillion Btu
  2020: 423.513000 Trillion Btu

Conventional Hydroelectric Power [Index 1]
  2015: 2307.717000 Trillion Btu
  2016: 2458.721000 Trillion Btu
  2017: 2752.024000 Trillion Btu
  2018: 2650.608000 Trillion Btu
  2019: 2552.636000 Trillion Btu
  2020: 2581.291000 Trillion Btu

Solar Energy [Index 3]
  2015: 227.901000 Trillion Btu
  2016: 327.712000 Trillion Btu
  2017: 485.742000 Trillion Btu
  2018: 575.854000 Trillion Btu
  2019: 634.613000 Trillion Btu
  2020: 802.317000 Trillion Btu

Wind Energy [Index 4]
  2015: 1775.705000 Trillion Btu
  2016: 2093.728000 Trillion Btu
  2017: 2340.784000 Trillion Btu
  2018: 2479.897000 Trillion Btu
  2019: 2632.354000 Trillion Btu
  2020: 2998.142000 Trillion Btu

Wood Energy [Index 5]
  2015: 243.857000 Trillion Btu
  2016: 224.407000 Trillion Btu
  2017: 229.324000 Trillion Btu
  2018: 221.063000 Trillion Btu
  2019: 200.524000 Trillion Btu
  2020: 185.145000 Trillion Btu
```

This is the annual consumption data of some renewable energy sources
by the US electric power sector from 2015 to 2020.

Why do we need to call `init` before `dump` and other functions?
Because `init` loads data from a CSV file (CSV files are like simple
spreadsheets), and you might want to also use other CSV files.  For
example, try this to see a smaller dataset about other renewble energy
sources in
`lab.csv`:

```python
>>> project.init("lab.csv")
WARNING!  Opening a path other than energy.csv.  That's fine for testing your code yourself, but energy.csv will be the only file around when we test your code for grading.
>>> project.dump()
Geothermal Energy [Index 2]
  2015: 148.336000 Trillion Btu
  2016: 146.104000 Trillion Btu
  2017: 146.733000 Trillion Btu
  2018: 145.060000 Trillion Btu
  2019: 133.851000 Trillion Btu
  2020: 146.765000 Trillion Btu

Waste Energy [Index 6]
  2015: 281.022000 Trillion Btu
  2016: 280.662000 Trillion Btu
  2017: 280.217000 Trillion Btu
  2018: 275.021000 Trillion Btu
  2019: 247.613000 Trillion Btu
  2020: 238.367000 Trillion Btu
```

What about `get_idx` and `get_consumption`?  Print the documentation
for those too, as you have for other functions (i.e., using
`.__doc__`).

As you may have noticed, each type of energy has an index and a name.
`get_consumption` looks up consumption in a specific year, given an index.
`get_idx` looks up an index given a name.  Try a few uses:

* `project.get_idx("Geothermal Energy")` (looks up index of Geothermal Energy, which should be 2)
* `project.get_consumption(6, 2020)` (looks up consumption of the energy source with index 6 in 2020, which should be 238.367)
* `project.get_consumption(project.get_idx("Geothermal Energy"), 2017)` (looks up consumption of Geothermal Energy in 2017; Geothermal Energy has ID 2)
* `project.get_consumption(project.get_idx("Waste Energy"))` (looks up consumption of Waste Energy in 2020, the default year argument)

Try switching back to the `energy.csv` dataset (with
`project.init("energy.csv")`) and see if you can lookup consumption Solar Energy in 2019.

You should also experiment with the three ways to initialize parameters:

* `project.get_consumption(3, 2020)` (positional argument for year)
* `project.get_consumption(3, year=2020)` (keyword argument for year)
* `project.get_consumption(3)` (default argument for year)

Finally, you should try some commands that will fail and note the
kinds of errors produced:

* `project.get_idx("coal")`
* `project.get_idx("wood energy")`
* `project.get_consumption(0, 2018)`
* `project.get_consumption(8, 2019)`
* `project.get_consumption(1, 2019, year=2019)`
* `project.init("BAD.csv")`
* `project.init(220)`
* `project.init()`
* `project.dump(True)`

## Project 3

Great, now you're ready to start [p3](https://github.com/msyamkumar/cs220-f21-projects/tree/main/p3)!  All the things you've been
doing here in interactive mode will work in your notebook as well.
Remember to only work with at most one partner on p3 from this point
on.  Have fun!

## Reference
The datasets `lab.csv` and `energy.csv` are truncated and modified from [here](https://www.eia.gov/totalenergy/data/browser/xls.php?tbl=T10.02C&freq=m) published by [U.S. Energy Information Administration](https://www.eia.gov/totalenergy/data/monthly/index.php).
