# Lab-P8: Lists and Dictionaries

This lab is designed to help you prepare for p8 and provide you opportunities to practice concepts that we've seen a lot of students struggling with. We will focus on dictionaries, mutating lists, optimizing, copying, and binning.

## Exercises

### Type Conversion: Version 1

Complete the following code so that it prints `total: 600`

```python
values = ["100", "200", "300"]
total = 0

for ???? in values:
    print("looping over value:", x)
    ???? += int(x)
print("total:", total)
```

### Type Conversion: Version 2

Complete the following code so that it prints `total: 600`

```python
values = ["100", "200", "300"]

for ???? in range(len(????)):
    print("looping over index:", i)
    values[i] = int(values[i])

print("total:", sum(values))
```

Notice how converting the original data in-place (i.e., we modified
the list itself) lets us just use the `sum` function at the end?



### Convert a List of Lists to a Dictionary

Given the following list of lists:
```python
player_csv = [ ['Ada', 'Lovelace', 'England', 'Defender, Goalie, Midfield', '12' ], 
                ['Rose', 'Lavelle', 'USA', 'Midfield', '16' ], 
                 ['Marta', 'Vieira da Silva', 'Brazil', 'Midfield, Forward', '10' ],  ]
```
Create a list of dictionaries that looks like this (notice that the jerseys are type int). 
```python
[{'first': 'Ada',
  'last': 'Lovelace',
  'country': 'England',
  'positions': 'Defender, Goalie, Midfield',
  'jersey': 12},
 {'first': 'Rose',
  'last': 'Lavelle',
  'country': 'USA',
  'positions': 'Midfield',
  'jersey': 16},
 {'first': 'Marta',
  'last': 'Vieira da Silva',
  'country': 'Brazil',
  'positions': 'Midfield, Forward',
  'jersey': 10}]
```

Start with this code:
```python
player_dict_list = []
for player in player_csv:
    player_dict = {}
    player_dict['first'] = player[0]
    # code for other keys
player_dict_list
```

### Splitting a String into a List

Now, modify one line of your code so that the value for the key positions is a list of strings, like this:
```python
[{'first': 'Ada',
  'last': 'Lovelace',
  'country': 'England',
  'positions': ['Defender', 'Goalie', 'Midfield'],
  'jersey': 12},
 {'first': 'Rose',
  'last': 'Lavelle',
  'country': 'USA',
  'positions': ['Midfield'],
  'jersey': 16},
 {'first': 'Marta',
  'last': 'Vieira da Silva',
  'country': 'Brazil',
  'positions': ['Midfield', 'Forward'],
  'jersey': 10}]
```
Notice that the strings inside the list do not have spaces in them.  You can accomplish this by a careful use of the .split() method. 


### Iterating through a List of Dictionaries that Contain Lists

Let's practice iterating through the list of dictionaries.  Go to a new cell in your Notebook.  Write a for loop that iterates through your list of dictionaries  to print out only the country names.  You should get this result: 
```python
for i in range(len(player_dict_list)):
    print(???)


England
USA
Brazil
```

Next, instead of printing the country names, modify your loop to print out all the positions, one per line.   You should get this result:
```python
Defender
Goalie
Midfield
Midfield
Midfield
Forward
```
To do this, you will need an inner loop that iterates through the indices in each positions list.  Remember to use a different name for the index in your inner loop.

```python
for i in range(len(player_dict_list)):
    positions = ???
    for j in range(len(positions)):
        print(???)
player_dict_list
```

Finally, change the line that prints out the positions, to instead change each item in positions to uppercase.  When you are done, display the entire dictionary. 
```python
[{'first': 'Ada',
  'last': 'Lovelace',
  'country': 'England',
  'positions': ['DEFENDER', 'GOALIE', 'MIDFIELD'],
  'jersey': 12},
 {'first': 'Rose',
  'last': 'Lavelle',
  'country': 'USA',
  'positions': ['MIDFIELD'],
  'jersey': 16},
 {'first': 'Marta',
  'last': 'Vieira da Silva',
  'country': 'Brazil',
  'positions': ['MIDFIELD', 'FORWARD'],
  'jersey': 10}]
```

Be extra certain that all your answers are correct...you will be using this logic in your project.  Ask your TA or Peer Mentor for help if you need it. 


### Optimizing

As we start dealing with bigger datasets, our programs might start
taking a long time to run if we aren't careful. You have likely already
run into such issues in p6 and p7. In such cases, we
might need to optimize our code, to make it run more quickly.

Optimization often involves avoiding doing the same work more than
once, especially when the repeated work is slow.  Try running the
following code in a cell.  It should take about 20 seconds to run.

```python
import time

# don't change this
def get_winners():
    # make this function slow, for the sake of the exercise
    time.sleep(0.1)
    return [999, 100, 150, 11, 555]

# can you make this function faster?
def count_winners(nums):
    count = 0
    for num in nums:
        if num in get_winners():
            count += 1
    return count

# don't change this either
nums = []
for i in range(200):
    nums.append(i)

print("Winners:", count_winners(nums))
```

The code repeatedly calls a slow function, `get_winners` (it wouldn't
be slow normally, but we made it slow on purpose).  Your job is to
modify the `count_winners` function so that it does produces the same
result while calling the slow function less often.




### Copying Lists to Avoid Side Effects

Try running the following code:

```python
import copy

def median(nums):
    nums.sort()
    if len(nums) % 2 == 1:
        return nums[len(nums) // 2]
    else:
        v1 = nums[len(nums) // 2]
        v2 = nums[len(nums) // 2 - 1]
        return (v1+v2) / 2

values = [33,22,11,44,55]
print("The values before the function call are", values)
print("The median is", median(values)) # change this below
print("The values after  the function call are", values)
```

It currently prints this:

```
The values before the function call are [33, 22, 11, 44, 55]
The median is 33
The values after  the function call are [11, 22, 33, 44, 55]
```

But it should print this:

```
The values before the function call are [33, 22, 11, 44, 55]
The median is 33
The values after  the function call are [33, 22, 11, 44, 55]
```

Change your call to the `median` function. Instead of sending the list, send a copy of the list.  Use one of the functions in the
copy module to make a copy. 


## Binning

Start by pasting the following code in a cell to setup the data:

```python
names = ["Ada", "Caitlin", "Abe", "Bobby", "Alice", "Britney", "Cindy", "Caleb"]
```


Your job is to determine, for each letter, the average length of names
starting with that letter.  This is a two-part task: (1) bucketize the
names based on the first letter, and (2) run a function over each
bucket of data to get a summary.

### Step 1: Bucketize

Try completing the following:

```python
buckets = {}

for name in names:
    first = name[????]
    if not first in ????:
        buckets[first] = [] # empty list
    buckets[????].append(????)

buckets
```

If you complete the above correctly, `buckets` will contain the following dict of lists:

```python
{'A': ['Ada', 'Abe', 'Alice'],
 'C': ['Caitlin', 'Cindy', 'Caleb'],
 'B': ['Bobby', 'Britney']}
```

### Step 2: Stats per Bucket

Now complete the following:

```python
def avg_len(names):
    total = 0
    for name in names:
        ???? += len(name)
    return total / len(????)

summary = {}
for k in buckets:
    summary[k] = avg_len(buckets[????])

summary
```

Your goal is for `summary` to be a dictionary where a key is the first
letter of a name, and the corresponding value is the average length of
the names starting with that letter, like this:

```python
{'A': 3.6666666666666665, 'C': 5.666666666666667, 'B': 6.0}
```

## Project Hints

You'll need to do some conversions very similar to what we ask you to
do in the section *Type Conversion: Version 2*.  We also create a
scenario in the project where you'll need to create a copy of your
data, somewhat similar to what you need to do in the *Copying*
section. You will also be iterating through lists of dictionaries that contain lists.
Finally, you will have to implement a function that borrows heavily
from the *Binning* section. 

Good luck on p8!  We encourage you to stay in lab and ask the TA and Peer Mentor questions. 

