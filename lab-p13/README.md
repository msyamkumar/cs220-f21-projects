# Lab 13: Fit Lines

# WARNING: Unless you took a time portal to become my student in the past, this is not the correct repository :) Please go to the correct github repository for the current semester. If you are a Fall'21 semester student though, you are in the right place.

In this lab, you'll learn three things:

1. how to draw a fit line
2. what numpy is, and its relationship to pandas
3. how to compute a fit line

<h2> Corrections/Clarifications
    **(12/8/2021 - 12:30pm)**: typos fixed in SQL practice section
</h2> 

* **(12/07/2021 - 11:25am)**: Fixing typo in SQL question --- 7 popular pizza toppings (instead of majors) 

## Drawing a Fit

Scatter plots are a good way to visualize correlations.  We'll
often want to overlay the scattered points with a line to represent
the approximate relationship.  This can help us see the pattern
in underlying the noise.

Let's construct a DataFrame with two related columns: tree age and
tree height.  We'll randomly generate data.  Let's imagine that
`height ≈ age * 2.3` (or `height = age * 2.3 + NOISE`) and randomly
generate some data.  Complete and run the following code to generate 100
random trees. Make sure to paste the import statements in a separate cell at the top
of the notebook.

```python
import random
from pandas import DataFrame
```

```python
ages = []
heights = []
for i in range(????):
    age = random.uniform(1, 10)
    noise = random.uniform(-1.5, 1.5)
    height = age * 2.3 + noise
    ages.append(age)
    heights.append(????)

trees = DataFrame({"age":ages, ????:heights})
trees.head()
```


The above code has some randomness, so you'll get different numbers
each time you run it, but it should look something like this:

<img src="images/tree-df.png">

Complete the following to plot a scatter of the data:

```python
import matplotlib
```

```python
# ensures that font.size setting remains permanent
%matplotlib inline 
```

```python
# tree scatter
matplotlib.rcParams["font.size"] = ???? # TODO: the default font size is 10, set it to a higher value, say 13

ax = trees.plot.????(x="age", y="height", c=????, xlim=0, ylim=0)
ax.set_xlabel(????)
ax.????("Height (feet)")
```

Fill in the `????` parts to get a plot that looks something this:

<img src="images/scatter.png">

If we want to draw a fit line, we need to add some fitted height
values to match the age values we already have in the trees DataFrame.
Let's use a slope of 2.

```python
trees["height-fitted"] = trees["age"] * 2
trees.head()
```

It should look something like this:

<img src="images/tree-df-2.png">

Notice there's some difference between `height` and `height-fitted`.
The former are the actual values; the latter is what height would be
if height were always twice age, with no noise.  Let's plot the fit
line on top of our scatter:

```python
ax = trees.plot.????(x="age", y="height", c=????, xlim=0, ylim=0)
ax.set_xlabel(????)
ax.????("Height (feet)")

trees.plot.line(ax=ax, x="age", y="height-fitted", color="red")
```

Note that the above cell is the same as the earlier example, with the
addition of just the `trees.plot.line` line at the end, so you could
copy code from earlier example, rather than fill in all the `????` parts.  Your plot should
look like this:

<img src="images/scatter-2.png">

So drawing a fit line is easy.  Of course, we just made up the slope.
We need to do some *linear algebra* to compute the slope and intercept
in a meaningful way.  We'll use the `numpy` module for this.

## Numpy

Numpy is the most popular way to represent matrices in Python and do
linear algebra. Let's import numpy (make sure to add it with the other imports):

```python
import numpy as np
```

The main data structure in numpy is the array; it is used to represent
vectors and matrices.  Try creating one:

```python
np.array([1, 2, 3, 4, 5, 6, 7, 8])
```

To create a matrix, you can start with a vector, then impose some
structure on it with a call to `.reshape(ROWS, COLS)`.

Create a matrix with 2 rows and 4 columns:

```python
matrix = np.array([1, 2, 3, 4, 5, 6, 7, 8]).reshape(2, 4)
matrix
```
The output of the above code looks like this:

```
array([[1, 2, 3, 4],
       [5, 6, 7, 8]])
```

Now create a matrix with 4 rows and 2 columns:

```python
matrix = np.array([1, 2, 3, 4, 5, 6, 7, 8]).reshape(4, 2)
matrix
```

The output of the above code looks like this:

```
array([[1, 2],
       [3, 4],
       [5, 6],
       [7, 8]])
```

As you can see, a numpy array looks like a list of lists; indeed, you
can access it as such (the following gets 7):

```python
matrix[3][0]
```

Complete the following to get `6` from `matrix`:

```python
matrix[????][????]
```


Pandas is closely integrated with numpy, so it is easy to convert a
Pandas DataFrame to a numpy array, using the `.values` attribute.  Try
it:

```python
trees.values
```

You should see something like this:

```
array([[ 4.74371708, 12.00074986,  9.48743415],
       [ 9.29054235, 20.08030328, 18.58108469],
       [ 6.01233576, 13.31622645, 12.02467151],
       [ 3.97135042,  8.41919774,  7.94270085],
       [ 4.13624753,  8.87260787,  8.27249507],
       [ 4.02866154,  8.24494275,  8.05732308],
       [ 1.92147542,  5.71251348,  3.84295085],
       [ 7.36679907, 18.38501823, 14.73359814],
       [ 4.74236776,  9.74468899,  9.48473553],
       ...
       [ 2.6725559 ,  6.03215439,  5.3451118 ]])
```

## Computing a Fit

We'll use something called the *Least Squares Method* to find a fit
line for our trees data (https://en.wikipedia.org/wiki/Least_squares).
For CS 220, you only need to understand it at an intuitive level.
Imagine we attached a movable line to every point in our data, as in
the following:

<img src="images/springs.png">

The line will naturally settle so as to minimize the total tension in
all the strings.  Imagine that the tension in a spring is the square
of the distance the spring is stretched (e.g., stretching a spring
twice as far increases the tension in that spring by 4 times).

Rather than getting into the math of computing how the line will settle,
we'll use the `np.linalg.lstsq(...)` function in numpy.

To setup the problem, imagine that we want to find some coefficients
to get an approximate formula that relates some of the columns in a
DataFrame.  For a simple `y = m * x + n` line, the relationship on the
DataFrame might look like this:

<img src="images/columns.png">

Note that the coefficients (even the one for the line's intercept)
need to be multiplied by a column (that's just what the `lstsq`
function expects), so we have a dummy column containing just ones for
`n`.  As you can see, we're trying to relate the `y` column Series (an
output) to a `DataFrame` of values (the inputs) from which we want to
estimate `y`.

Let's add the dummy column to our `trees` DataFrame and pull out the
inputs and output:

```python
output = trees["height"]
trees["one"] = 1
inputs = trees[["age", "one"]]
inputs.head()
```

If we have a DataFrame `df`, then `df[list_of_columns]` will create a
DataFrame that has a subset of the original columns (as specified in
the list), so `inputs` will look something like this (`age` is the
`x` in this case and `height` is the `y`):

<img src="images/inputs.png">

Ok, now we're ready to crunch some numbers:

```python
result = np.linalg.lstsq(inputs, output, rcond=None)
result
```

Notice we're passing our `inputs` DataFrame and `output` Series; numpy
can work with these Pandas types.  The `rcond=None` is an unimportant
detail (you should always pass that).  `result` will look something
like this:

```
(array([2.27595611, 0.10250293]),
 array([80.70169711]),
 2,
 array([64.20719236,  3.56646379]))
```

Notice it's a tuple with four values, as described here:
https://docs.scipy.org/doc/numpy/reference/generated/numpy.linalg.lstsq.html.
According to the documentation, the tuple is like this:
`(coefficients, residuals, rank, singular_values)`.  Here, we only
care about the coefficients, so let's pull those out:

```python
slope = result[0][0]
intercept = result[0][1]
slope, intercept
```

Let's use this slope and intercept to fill in the `height-fitted` column correctly now:

```python
trees["height-fitted"] = trees["age"] * slope + intercept
trees.head()
```

Let's conclude by re-plotting the scatter data and fit line:

```python
ax = trees.plot.scatter(x="age", y="height", c="black", xlim=0, ylim=0)
ax.set_xlabel("Age (years)")
ax.set_ylabel("Height (feet)")

trees.plot.line(ax=ax, x="age", y="height-fitted", color="red")
```

<img src="images/final.png">

## SQL practice

Download [`survey.db`](https://github.com/msyamkumar/cs220-f21-projects/tree/master/lab-p13/survey.db).
The following code enables us to establish connection to `survey.db` database. Paste the code into a new cell:

```python
import sqlite3
import pandas as pd
```

```python
conn = sqlite3.connect('survey.db')
# remember to do conn.close() at the end of your notebook!
```

Now, let's take a look at the details of the database. Paste the following code to your notebook:

```python
pd.read_sql("SELECT * FROM sqlite_master", conn)
```

What name do you see for the database table? Complete the following code to explore the first seven lines of the database table. 

```python
pd.read_sql(
"""
SELECT *
FROM ???
LIMIT ???
""", conn)
```

### How many students are in each lecture?
Recall that, you can create groups based on unique values in a column, using `group by` SQL clause. `Group by` enables you to apply aggregation operations for every group. The `as` keyword enables you to rename the newly computed column, either using aggregation or by using computation. Complete the following query to answer this question:

```python
pd.read_sql(
"""
select ???, ???(*) as student_count
from fall_2021
group by ???
""", conn)
```

### How many students are in each lecture - visualize using barplot?
X-axis should be `lecture` and Y-axis should be `student_count`. Capture the DataFrame from the above SQL query into a variable called `student_count_df` and complete the following code:

```python
count_series = student_count_df["student_count"]
ax = count_series.plot.???()
ax.set_ylabel("Count of students")
None # helps you supress the output from the above function call
```
What went wrong? Can you identify where the x-axis labels are coming from? 
Let's fix that by using `set_index` function on the pandas DataFrame.

```python
student_count_df = student_count_df.set_index("lecture")
count_series = student_count_df["student_count"]
ax = count_series.plot.???()
ax.set_ylabel("Count of students")
None # helps you supress the output from the above function call
```
The x-axis label is kind of redundant. Let's remove that. To the same cell where you typed the above code, type and run:

```python
ax.set_xlabel("Count of students")
```
What happened? Did you run into `KeyError: "None of ['lecture'] are in the columns"`. You cannot invoke set_index on the same DataFrame twice! If you really have to re-run that cell, you must do `Kernel Restart & Run All`. Once you do that, your x-axis label should disappear.

### What are the top 5 popular majors?
Recall that `order by` SQL clause enables you to perform sorting. The default ordering is ascending (`ASC`). You can specify descending ordering by mentioning `DESC` after the column name (based on whose ordering you want to sort your rows). Complete the following code:

```python
pd.read_sql("""
select major, ???(*) as major_count
from fall_2021
group by ???
order by ???
LIMIT ???
""", conn)
```

### What are the top 7 popular pizza toppings?
Recall that `order by` SQL clause enables you to perform sorting. The default ordering is ascending (`ASC`). You can specify descending ordering by mentioning `DESC` after the column name (based on whose ordering you want to sort your rows). The `as` keyword enables you to rename the newly computed column, either using aggregation or by using computation. Complete the following code:

```python
pd.read_sql("""
select ???, ???(*) as topping_count
from fall_2021
group by ???
order by ??? ???
LIMIT ???
""", conn)
```
### How many Engineering majors like pepperoni piazza topping?
In a `where` clause, you can use `and` to combine multiple conditions. Complete the following code:

```python
pd.read_sql(
"""
SELECT ???(*)
FROM fall_2021
WHERE ??? = "Engineering" and ??? = "pepperoni"
""", conn)
```

### What is the minimum age for each lecture?
The lecture and minimum age should be displayed in ascending order of minimum age. If the minimum ages are tied, then the lectures should be ordered in alphabetical order (ascending). You can achieve this, by specifying two column information for `order by` clause. Complete the following code:

```python
pd.read_sql("""
select ???, ???(age) as min_age
from fall_2021
group by ???
order by min_age ASC, lecture ASC
""", conn)
```

### What year where students born in?
Recall that, in SQL `select` clause, you can specify computation. For example, complete the following code to compute `year_of_birth` from `age` and `curr_year` column values.

```python
pd.read_sql("""
select *, ??? - ??? as year_of_birth
from fall_2021
""", conn)
```

## Project

In p13, you will need to construct several scatter plots using pandas, compute an appropriate fit using numpy, and draw a fit line on the same plot as the scatter plot.

**Good luck**


