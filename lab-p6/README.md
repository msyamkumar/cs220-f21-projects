# Lab P6

In this lab, you will practice accessing CSVs, sorting, and using sets.

To start, familiarize yourself with the dataset for p6 here:
[airbnb.csv](https://github.com/msyamkumar/cs220-f21-projects/blob/main/lab-p6/airbnb.csv).
Download the `airbnb.csv` to a new `lab6` directory, and start a new
notebook in that directory for this lab.

## Corrections and clarifications

None yet.

**Find any issues?** Report to us:

- Brian Huang ([thuang273@wisc.edu](mailto:thuang273@wisc.edu))
- Parker Lougheed ([plougheed@wisc.edu](mailto:plougheed@wisc.edu))


## CSVs

### Loading from CSVs

[Chapter 14](https://automatetheboringstuff.com/chapter14/) 
of Automate the Boring Stuff introduces CSV files
and provides a code snippet we can reuse.
Copy the following into a cell in your notebook and run it:

```python
import csv

# Modified from https://automatetheboringstuff.com/chapter14/
def process_csv(filename):
    example_file = open(filename, encoding="utf-8")
    example_reader = csv.reader(example_file)
    example_data = list(example_reader)
    example_file.close()
    return example_data

# Use process_csv to pull out the header and data rows
csv_rows = process_csv("airbnb.csv")
csv_header = csv_rows[0] # A list of the column headers
csv_data = csv_rows[1:] # The entire CSV data set besides the headers
```

We recommend you also copy the above code into your p6 notebook
when you start the project.

### About the dataset

The `airbnb.csv` file has data about nearly 50,000 listings on Airbnb
from New York City, NY from the year 2019. Each row in the file 
contains data about a single listing. The columns contain the 
following data about each listing (along with the correct data type to represent it):

* `room_id` - The ID of the room listing (`str`)
* `name` - The name of the room listing (`str`)
* `host_id` - The ID of the host for the room listing (`str`)
* `host_name` - The name of the host for the room listing (`str`)
* `neighborhood_group` - The group of neighborhoods the room is in (`str`)
* `neighborhood` - The neighborhood the room is in (`str`)
* `latitude` - The latitude where the room is located (`float`)
* `longitude` - The longitude where the room is located (`float`)
* `room_type` - The type of room (`str`)
* `price` - The price per night for the room in US dollars (`int`)
* `minimum_nights` - The minimum amount of nights the room can be booked for (`int`)
* `number_of_reviews` - The total number of reviews the room has received (`int`)
* `last_review` - The date of the most recent review in the form `yyyy-mm-dd` (`str`)
* `reviews_per_month` - How many reviews per month the room receives (`float`)
* `calculated_host_listings_count` - How many listings the host of the room has (`int`)
* `availability_365` - How many days per year the listing is available for (`int`)

**Note:** Keep in mind while writing your project,
some entries may be missing data for specific columns. Sadly, data in real life
is often messy, and in p6, we will have to deal with missing data.

### Accessing the CSV contents

Try running the following and thinking about the results 
(thinking about the results involves locating the values produced in the `airbnb.csv` dataset):

* `csv_header`
* `len(csv_data)`
* `csv_data[:5]`
* `csv_data[0]`
* `csv_data[0][3]`
* `csv_header.index("neighborhood_group")`
* `csv_data[0][csv_header.index("neighborhood_group")]`

**Note on last two:** You can find the index of a value in a list
by using the `.index(val)` method.
For example, the following prints 2:

```python
letters = ["A", "B", "C", "D"]
print(letters.index("C"))
```

Therefore the final example gets the index of the `neighborhood_group` column,
then uses that to find the value in that column in the 0th row.

```python
csv_data[0][csv_header.index("neighborhood_group")]
```

While looking at the `airbnb.csv` data,
try to complete the following Python expressions to get the specified results:

* `csv_data[0][csv_header.index(????)]` to get "Brooklyn"
* `csv_data[1][csv_header.index(????)]` to get "Jennifer"
* `csv_data[2][csv_header.index(????)]` to get "THE VILLAGE OF HARLEM....NEW YORK !"

Also try using a similar format to extract the following values from an entry:

* `John`
* `Manhattan`
* `Harlem`

You'll use the following function as the basis for accessing data in p6, 
but first you need to fill in some missing pieces (**ignore the option part for now**):

```python
def cell(row_idx, col_name):
    col_idx = csv_header.index(???)
    val = csv_data[???][col_idx]
    if val == "":
        return None
    # optional: convert types based on column name, 
    # ensuring that the float and int values are appropriately converted
    return val
```

Is your implementation correct? Test it with the following:

1. `cell(0, "neighborhood")` should return "Kensington"
2. `cell(1, "name")` should return "Skylit Midtown Castle"
3. `cell(2, "price")` should return "150"
4. `cell(3, "latitude")` should return "40.68514"

**Optional:** It will save you time in the long run 
if `cell(2, "price")` returns an `int` (example 2) 
and `cell(3, "latitude")` returns a `float` (example 3) instead of a String.
Consider improving the `cell` function so it automatically converts the result
to the desired value based on the column name 
(e.g., the value for any price might be cast to an int).

**Important Reminder:** While you and your lab partner (if you have one) 
can collaborate on writing the `cell` function, 
you may not collaborate with your lab partner on other parts of the project,
unless of course the person you're doing the lab with is also your project partner.

## Sorting

There are two major ways to sort lists in Python: 
(1) with the `sorted` function and (2) with the `.sort` method.
You should experiment with both and understand their effects.
More generally, when encountering a new method, 
you should learn (a) how it modifies existing structures, 
and (b) what new values it returns, if any.

Try running the following:

```python
letters = ["B", "C", "A"]

result = letters.sort()

print("Original list: ", letters)
print("Returned value: ", result)
```

You should record your observations in your notes.
What does `.sort` do to existing structures? What does it return?

Now let's try `sorted`:

```python
letters = ["B", "C", "A"]

result = sorted(letters)

print("Original list: ", letters)
print("Returned value: ", result)
```

What does `sorted` do to existing structures?  What does it return?

Let's try `sorted` on a string:

```python
s = "BCA"

result = sorted(s)

print("Original str:", s)
print("Returned value:", result)
```

While `.sort` only works on lists, 
`sorted` works on other sequences, such as strings. 
Can you guess why there's not the equivalent of a `.sort` method for strings? 
Hint: Remember strings are immutable.

Note that `sorted` always returns a list sequence, 
even if the input is a string sequence.

With `.sort` and `sorted()` you can also sort in reverse order
by adding setting the `reverse` parameter to `True` with a keyword argument:

```python
letters = ["B", "C", "A"]

letters.sort(reverse=True)

print("Reverse sorted list: ", letters)
```

```python
letters = ["B", "C", "A"]

result = sorted(letters, reverse=True)

print("Original list: ", letters)
print("Reversed sorted list: ", result)
```

Some methods both change existing structures AND return something. 
Try `pop`:

```python
letters = ["B", "C", "A"]

result = letters.pop(0)

print("Original list:", letters)
print("Returned value:", result)
```

## Sets

In class, we learned about the Python `list` sequence.
Another simpler structure you'll sometimes find useful is the `set`.
A set is NOT a sequence
because it does not keep all the values in any particular order.
You can create sets the same way as lists, 
just replacing the square brackets with curly braces. Try it!

```python
example_list = ["A", "B", "C"]
print(example_list)
example_set = {"A", "B", "C"}
print(example_set)
```

### `in` operator

Some things are similar between lists and sets, 
like checking if they contain something. Try this:

```python
"A" in example_list
```

And this:

```python
"A" in example_set
```

**Note:** If you have a LOT of values, 
the `in` operator is MUCH faster for Python to execute with a `set`
than with a `list`.

### Order (or lack thereof)

Sets have no inherent ordering, so they don't support indexing.
Try and watch it fail:

```python
example_list[0]  # Works
example_set[0]   # Crashes
```

The lack of order also matters for comparisons.
Try evaluating this boolean expression:

```python
["A", "B", "C"] == ["C", "B", "A"]
```

And now try this:

```python
{"A", "B", "C"} == {"C", "B", "A"}
```

### Type Conversions

You can switch back and forth between lists and sets with ease.
Let's try it:

```python
items = [1,2,4]
items_set = set(items)
print(items_set)
```

Or in the other direction:

```python
items = {4,2,1}
items_list = list(items)
print(items_list)
```

Be careful! When going from a set to a list, 
Python has to choose how to order the previously unordered values.
If you run the same code, 
there's no guarantee Python will always choose the same way to order
the set values in the new list.

Sometimes people convert from a more complicated type (like a float)
to a less complicated type (like an int) and back.
Can you think why they might do this?
Run this code and think about it:

```python
x = 3.8
y = float(int(x))
print(y)
```

In the same way,
sometimes people convert from a list (more complicated type)
to a set (simpler type) and back to a list again.
Explore the resulting effect:

```python
list_1 = ["A", "A", "B", "B", "C", "B", "A"] # Try playing with different values here
list_2 = list(set(list_1))
print(list_2)
```

## Project

Hopefully this will help you get off to a good start on the project!
Here's how the lab relates to p6:

1. You should use the `cell` function from the lab to access data in the project
2. Sorting strings will help you detect anagrams
3. Converting a list to a set and then back to a list
   will remove duplicates from your list

Good luck with [p6](https://github.com/msyamkumar/cs220-f21-projects/tree/main/p6)!
