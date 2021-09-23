# Project 3: Renewable energy consumption by the US Electric Power Sector

### Corrections/Clarifications

1. **(9/23/2021 - 10:45am)** Q18 reworded for clarity.

**Find any issues?** Report to us: 

- Yelun Bao <ybao35@wisc.edu>
- Hardik Chauhan <hchauhan2@wisc.edu>

## Learning Objectives

In this project, you will walk through how to

* Import a module and use its functions
* Practice writing functions
* Practice doing some basic statistical analysis on the dataset

**Please go through [lab-p3](https://github.com/msyamkumar/cs220-f21-projects/tree/main/lab-p3) 
before working on this project.** The lab 
introduces some useful techniques necessary 
for this project.

## Description

In this project, you'll analyze data about five different renewable energy
sources consumed by the US commercial power industry between 2015 and 2020. 
In other words, this is the amount of renewable energy that was used to generate
electricity that was sold to consumers.
The dataset we will analyze is truncated and modified from 
[here](https://www.eia.gov/totalenergy/data/browser/xls.php?tbl=T10.02C&freq=m) 
published by [U.S. Energy Information Administration](https://www.eia.gov/totalenergy/data/monthly/index.php).

You'll get practice calling 
functions from the `project` module, which we've provided, 
and practice writing your own functions.

Start by downloading `project.py`, `test.py` and `energy.csv`.
Double check that these files don't get renamed by your browser (by
running `ls` in the terminal from your `p3` project directory).
You'll do all your work in a new `main.ipynb` notebook that you'll
create also in `p3` project directory and hand in when you're done 
(please do not write your functions in a separate .py file). 
You'll test as usual by running `python test.py` (or similar, 
depending on your laptop setup).  Before handing in, 
please put the project, submitter, and partner info in a
comment in the first cell, in the same format you used for `p2`
(please continue doing so for all projects this semester).

The first cell should contain and only contain information like this:
```python
# project: p3
# submitter: NETID1
# partner: NETID2
# hours: ????
```

We won't explain how to use the `project` module here (the code is in the
`project.py` file).  Refer to [lab-p3](https://github.com/msyamkumar/cs220-f21-projects/tree/main/lab-p3) 
to understand the functions in `project.py` and use those. 
Feel free to take a look at the `project.py` code if you are 
curious about how it works.

This project consists of writing code to answer 20 questions.  If
you're answering a particular question in a cell in your notebook, you
need to put a comment in the cell so we know what you're answering.
For example, if you're answering question 13, the first line of your
cell should contain `#q13` (or `#Q13`).

## Dataset

The data looks like this:

index|energy type|2015|2016|2017|2018|2019|2020
------|------|------|------|------|------|------|------| 
1|Conventional Hydroelectric Power|2307.717|2458.721|2752.024|2650.608|2552.636|2581.291
3|Solar Energy|227.901|327.712|485.742|575.854|634.613|802.317
4|Wind Energy|1775.705|2093.728|2340.784|2479.897|2632.354|2998.142
5|Wood Energy|243.857|224.407|229.324|221.063|200.524|185.145
7|Biomass Energy|524.879|505.069|509.541|496.085|448.137|423.513

This table lists 5 different renewable energy sources, and the amount
of energy from each of these sources that was consumed by the US commercial power industry
in each of the years between 2015 and 2020. The units used here are 
trillions of Btu (British thermal units).

The dataset is in the `energy.csv` file which you downloaded. 
We'll learn about CSV files later in the semester.  
For now, you should know this about them:
* it's easy to create them by exporting from Excel
* it's easy to use them in Python programs
* we'll give you a `project.py` module to help you extract data from CSV files until we teach you to do it directly yourself

## Requirements

You **may not** hardcode indices in your code. For example, if we ask
how much Wood Energy was consumed in 2020, you could obtain the answer
with this code: `get_consumption(get_idx("Wood Energy"), 2020)`.  If you don't
use `get_idx` and instead use `get_consumption(5, 2020)`, we'll **manually deduct**
points from your `test.py` score during code review.

For some of the questions, we'll ask you to write (then use) a
function to compute the answer.  If you compute the answer **without**
creating the function we ask you to write, we'll **manually deduct** points from
your `test.py` score when recording your final grade, even if the way
you did it produced the correct answer.

## Incremental Coding and Testing
You should always strive to do incremental coding. Incremental coding enables you to avoid
challenging bugs. What exactly is incremental coding? Always write a few lines of code and then test
those lines of code, before proceeding to write further code. We also recommend you to do incremental
testing: solve a question and run auto-grader script `test.py`, to verify that you get a PASS for that 
particular question, before proceeding to the next.

## Questions and Functions

### #Q1: What is the index of Biomass Energy?


### #Q2: How much of the energy indexed 7 was consumed by the US electric power sector in 2017?

Answer in units of trillions of Btu. Your answer should just be a number 
(without any units at the end).

It is OK to hardcode `7` for Q2 in this case since we asked directly about
index 7 (instead of about "Biomass Energy"). Please **do not** hardcode the 
indices for Q3 onwards.

---

### #Q3: How much Solar Energy was consumed by the US electric power sector in 2019? 

Hint: instead of repeatedly calling `project.get_idx("Solar Energy")` (or
similar) for each question, you may wish to make these calls once at
the beginning of your notebook and save the results in variables,
something like this:

```python
hydroelectric_idx = project.get_idx("Conventional Hydroelectric Power")
solar_idx = project.get_idx("Solar Energy")
...
```

---

### Function 1: `year_max(year)`

This function will compute the maximum amount of energy consumed by
the US electric power sector from a single renewable energy source 
in the given year.

```python
def year_max(year):
    # grab the consumption of each energy source in the given year
    hydroelectric_consumption = project.get_consumption(project.get_idx("Conventional Hydroelectric Power"), year)
    solar_consumption = project.get_consumption(project.get_idx("Solar Energy"), year)
    wind_consumption = project.get_consumption(project.get_idx("Wind Energy"), year)
    wood_consumption = project.get_consumption(project.get_idx("Wood Energy"), year)    
    biomass_consumption = project.get_consumption(project.get_idx("Biomass Energy"), year)

    # use builtin max function to get the maximum of the five values
    return max(hydroelectric_consumption, solar_consumption, wind_consumption, wood_consumption, biomass_consumption)
```

### #Q4: What was the maximum energy consumed by the US electric power sector from a single renewable energy source in 2015?

Use `year_max` to answer this.

### #Q5: What was the maximum energy consumed by the US electric power sector from a single renewable energy source in 2017?

---

### Function 2: `energy_min(source)`

We'll help you start this one, but you need to fill in the rest
yourself.

```python
def energy_min(source):
    source_idx = project.get_idx(source)    
    y15 = project.get_consumption(source_idx, 2015)
    y16 = project.get_consumption(source_idx, 2016)
    # grab the consumptions from other years

    # use the min function (similar to the max function)
    # to get the minimum across the six years
    # and return that value
```

This function should compute the minimum energy consumed by 
the US electric power sector from the given renewable energy source
in any of the six years.

### #Q6: What was the minimum amount of Wood Energy consumed by the US electric power sector in a single year?

Use your `energy_min` function.

### #Q7: What was the minimum amount of Conventional Hydroelectric Power consumed by the US electric power sector in a single year?

---

### Function 3: `energy_avg(energy_source)`

This function should compute the average energy consumed 
by the US electric power sector from the given energy source 
across the six years in the datatset.

Hint: start by copy/pasting `energy_min` and renaming your copy to
`energy_avg`.  Instead of computing the minimum of `y15`, `y16`, etc.,
compute the average of these by adding, then dividing by six.

### #Q8: How much Solar Energy was consumed by the US electric power sector on average between 2015 and 2020?

Use your `energy_avg` function.

### #Q9: How much Wind Energy was consumed by the US electric power sector on average between 2015 and 2020?


### #Q10: How much Biomass Energy was consumed by the US electric power sector in 2018 above its average over the 6 years?

You should answer by giving a percent between 0 and 100, with no
percent sign.

---

### Function 4: `year_sum(year)`

This function should compute the total renewable energy 
consumption of the US electric power sector (over the five 
sources) in a given year.

You can start from the following code:

```python
def year_sum(year=2016):
     pass # TODO: replace this line with your code
```

**Note**: Python requires all functions to have at least one line of code.
When you don't have some code yet, it's common for that line to be `pass`,
which does nothing. After writing the rest of the function,
you may safely delete the `pass` from the function.
Note the default arguments above.


### #Q11: How much renewable energy was consumed by the US electric power sector in 2016?

Use the default argument (your call to `year_sum` should not pass any argument).
**If you do not use default arguments, you will lose points.**

### #Q12: How much renewable energy was consumed by the US electric power sector in 2020?
---

### Function 5: `change_per_year(energy, start_year, end_year)`

It is clear from looking at the dataset that the consumption of
some renewable energy sources (like Solar Energy) by the US electric 
power sector is trending upwards, while some (like Wood Energy) 
are trending downwards.
It would be interesting to find the *average* increase/decrease
in energy consumption per year, for these energy sources.

This function should return the average increase in consumption (could be
negative if there's a decrease) over the period from `start_year` to
`end_year` for the given `energy` source (example `energy` source: "Solar Energy").

You can start with the following code snippet:

```python
def change_per_year(energy, start_year=2015, end_year=2020):
     pass # TODO: replace this line with your code
```

We're not asking you to assume exponential growth or do anything complicated
here; you just need to compute the difference in consumption between the
last year and the first year, then divide by the number of elapsed
years. 


### #Q13: How much has the consumption of Solar Energy by the US electric power sector increased per year (on average) from 2015 to 2020? 

Use the default arguments (your call to `change_per_year` should only
pass one argument explicitly). **If you do not use the default arguments 
and instead pass more than one argument explicitly, you will lose points.**

### #Q14: How much has the consumption of Wind Energy by the US electric power sector increased per year (on average) from 2016 to 2020?

Use the same function `change_per_year` to answer this.
**As with Q13, if you explicitly pass more arguments than necessary, 
you will lose points.**

---

### Function 6: `find_threshold_year(energy, threshold)`

We saw from calling `change_per_year` that the consumption of some 
renewble energy sources by the US electric power sector is increasing rapidly. 
However, the consumption of some other renewable energy sources is 
also shrinking. It will be interesting to estimate when the 
consumption of these energy sources will shrink to 0.

Write a function named `find_threshold_year` to estimate the year 
when the consumption of a given energy source by the US electric power sector 
crosses a given threshold. Find the average change in consumption
over the six years (using `change_per_year`), and assuming that 
the energy consumption keeps decreasing at the same rate, 
compute the year when this energy will become lower than the 
threshold.

**Note**: You may find that the year when the consumption crosses
the threshold is not a whole number. For instance, you may find 
that the consumption of Biomass Energy by the US electric power sector 
goes below a threshold of 100 (trillion Btu) in 2038.42. 
Of course, a fractional number doesn't make much sense in this 
context, so we have to round up the number to 2039.

In order to round up the numbers, you may use the function 
`math.ceil` from the `math` module. You can refer to the 
[official documentation](https://docs.python.org/3/library/math.html).
You can also take a look at [this example](https://www.geeksforgeeks.org/python-math-ceil-function/). 
Before using the function, remember to import `math` module.

**It is a good practice to include all import statements at the beginning of your program. Go back to
the input cell where you imported project and add the below import statement.**

```python
import math
``` 

If you find it challenging to write this function, you can start 
with the following code snippet:

```python
def find_threshold_year(energy, threshold=0):
    pass
     # TODO: compute the average change in consumption from 2015 to 2020
     # TODO: assume that the energy consumption keeps decreasing at same rate
     # TODO: compute the required decrease in energy consumption from 2020 to cross threshold
     # TODO: estimate the number of years it will take from 2020 to cross threshold
     # TODO: use math.ceil() to round it up.
``` 

If you find any of this confusing, feel free to reach out to TAs and Peer Mentors!

### #Q15: In which year is the consumption of Wood Energy by the US electric power sector estimated to reach zero?


### #Q16: In which year is the consumption of Biomass Energy by the US electric power sector estimated to reach zero?


### #Q17: In which year is the consumption of Biomass Energy by the US electric power sector estimated to be less than the consumption of Wood Energy in 2020?

Do **not** hardcode the consumption of Wood Energy to answer this.

---

### Function 7: `find_overtake_year(energy1,energy2)`

We previously saw that the consumption of some energy sources 
by the US electric power sector is growing.
But we also saw that some energy sources are growing faster
than others. Similarly, the consumption of some energy sources are 
shrinking much faster than others. Just like we estimated when some 
energy sources will shrink to zero, it wil be interesting to 
estimate when some energy sources will overtake others in their 
consumption.

Write a function named `find_overtake_year` to estimate the year
when the consumption of energy source `energy1` by the US power 
sector will exceed the consumption of energy source `energy2`. 
To do this, find the average change in consumption over the 
six years for both energy sources, and assume that this does 
not change for either energy source. 
Extrapolate from this data to estimate when 
`energy1` will overtake `energy2`.

Hint 1: You will need to use math.ceil() once again to get you answer rounded up.

Hint 2: Focus on the difference in energy consumption between the two 
energy sources, and just like `find_threshold_year`, 
estimate when this crosses the threshold 0.

You can start with the following code snippet:

```python
def find_overtake_year(energy1, energy2):
    pass
    # TODO: compute the average change in consumption for both energy sources from 2015 to 2020.
    # TODO: assume both energy consumptions keep changing at the same rate.
    # TODO: compute the intial gap between consumption of energy1 and energy2 in 2020.    
    # TODO: estimate the number of years it will take from 2020 for this gap to decrease to 0.
    # TODO: use math.ceil() to round it up.
``` 

### #Q18: In which year will the consumption of Wood Energy by the US electric power sector overtake Biomass Energy?


### #Q19: In which year will the consumption of Solar Energy by the US electric power sector overtake Conventional Hydroelectric Power?

---

We see that Solar Energy is poised to beat Conventional Hydroelectric Power eventually. 
It will also be interesting to see how quickly Solar Energy consumption by the 
US electric power sector is growing *right now* in comparison with other renewable
energy sources. One way to do this is to look at the Unit Market Share of 
Solar Energy, and see how it is increasing each year.

You can find the definition of unit market share [here](https://en.wikipedia.org/wiki/Market_share#Construction).

### #Q20: What is the increase in the unit market share for Solar Energy from 2019 to 2020? 

Hint: You may find one of the earlier functions you wrote useful for computing the market share.
Look for it!

---

#### READ ME: Please remember to `Kernel->Restart and Run All` to check for errors, save your notebook, then run the test.py script one more time before submitting the project. To keep your code concise, please remove your own testing code that does not influence the correctness of answers. Finally, if you are unable to solve a question and have partial code that is causing an error when running test.py, please comment out the lines in the cell for that question before submitting your file. Failing to do so will cause the auto-grader to fail when you submit your file and give you 0 points even if you have some questions correctly answered.

Cheers!
