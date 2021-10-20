# Project 6: Airbnb

## Corrections/ Clarifications

* (10/14/2021 - 8:20 pm): Added code snippet for Q1 

**Find any issues?** Report to us:

- Brian Huang ([thuang273@wisc.edu](mailto:thuang273@wisc.edu))
- Parker Lougheed ([plougheed@wisc.edu](mailto:plougheed@wisc.edu))

## Announcements

* Remember you must begin each cell with the comment #Q1, #Q2, etc. 
  This comment is read by test.py to identify which question is being answered. 
  **We recommend copying the entire question line as a comment into your notebook.**
* To view grader comments for previous projects
  go to the project submission page and
  select the graded project and click view submission.
* For regrade requests, 
  please fill in the Grading Issues form which can he found [here](https://www.msyamkumar.com/cs220/f21/surveys.html).

## Learning Objectives

In this project, you will learn how to

* Access and utilize data in CSV files
* Deal with messy real world datasets
* Use string functions and sorting to order data

**Please go through [lab-p6](https://github.com/msyamkumar/cs220-f21-projects/tree/main/lab-p6) before working on this project.** 
The lab introduces some useful techniques related to this project.

## Introduction

Data Science can help us understand user behavior on online platform services. 
This project is about the rooms in Airbnb. 
Since 2008, guests and hosts have used Airbnb
to expand on traveling possibilities and present more unique, 
personalized way of experiencing the world. 
has data about nearly 50,000 listings on Airbnb
from New York City, NY from the year 2019. 
This file includes all a lot of information about the hosts, 
geographical availability of the listings, and other necessary
metrics to make predictions and draw conclusions.
You will be using various string manipulation functions that come with Python
as well as creating some of your own to solve the problems posed. Happy coding!

## Directions

Be sure to do [lab-p6](https://github.com/msyamkumar/cs220-f21-projects/tree/main/lab-p6) 
before starting this project; 
otherwise you probably won't get very far. 
Begin by downloading `airbnb.csv` and `test.py`. 
Create a `main.ipynb` file to start answering the following questions, 
and remember to run `test.py` often. 
There is no `project.py` this week, use the code from the lab to access the data. 
Remember to use the `#qN` format as you have for previous projects, and don't forget
to add details about the submitter and partner just like in previous projects.

**Important:** You are expected to use the `cell` function
you wrote in lab-p6 for all data accesses. You will **lose points** if you
access data through other means.


---

### #Q1: What neighborhood groups are present in the airbnb dataset?

Generate a Python list containing
the different neighborhood groups (`neighborhood_group`). 

**Important**: The order doesn't matter
but make sure that your answer doesn't contain duplicate entries.

Here's a code snippet for you to start with:

```python
neighborhood_groups = []
for idx in range(???):
    neighborhood_groups.append(cell(???, ???))
    
#TODO: remove duplicates from `neighborhood_groups`
```

Now is a good time to run the tests with `python test.py`. 
If you did Q1 correctly, it should look like this:

```
Summary:
  Test 1: PASS
  Test 2: not found
  Test 3: not found
  Test 4: not found
  Test 5: not found
  Test 6: not found
  Test 7: not found
  Test 8: not found
  Test 9: not found
  Test 10: not found
  Test 11: not found
  Test 12: not found
  Test 13: not found
  Test 14: not found
  Test 15: not found
  Test 16: not found
  Test 17: not found
  Test 18: not found
  Test 19: not found
  Test 20: not found

TOTAL SCORE: 5.00%
```

---

### #Q2: What is the average number of reviews among all the reviews?

The number of reviews for each listing can be found in the `number_of_reviews` column.

**Note:** Your answer should be rounded down and returned as an integer.

### #Q3: Count the number of rooms located in neighborhood "SoHo"?

You can find the value "SoHo" in the `neighborhood` column.

---

### Function Suggestion:

We require you to complete a function like the following to answer the 
next several questions (this is a requirement, and you will **lose points** if
you do not implement this function):

This function should return a list of all the room names that contain the
substring denoted by the variable `contained` inside them.

```python
def find_room_names(contained):
    pass
    # TODO: create a list
    # TODO: check if the room contains the `contained` parameter (case insensitive)
    # TODO: add every unmodified room name to the return list
    # TODO: return your list of room names
```

### #Q4: Find the room names containing "MSG"

**Note:** All words are case insensitive. Your answer should be in the form of a Python list.


### #Q5: Find the room names containing "cinema" or "film"

**Note:** All words are case insensitive. Your answer should be in the form of a Python list.

**Important:** If there are entries that contain both "cinema" and "film",
make sure to include it only once in your answer. 
If the room name has a word which contains "film", such as "filming", 
include it in your answer.

---

### #Q6: Which host names are anagrams of the word "aisle"?

An anagram is a word or phrase formed by
rearranging the letters of a different word or phrase,
using all the original letters exactly once.
(Read more here: https://en.wikipedia.org/wiki/Anagram). 
For our purposes, 
we'll ignore case when considering
whether two words are anagrams of each other.

**Hint:** Although you'll need to loop over all the names to check for anagrams, 
checking whether a single word is an anagram of another word
does not require writing a loop. 
So if you're writing something complicated, 
review the string methods and sequence operations to see
if there is a short, clever solution.

**Note:** Your answer should be in the form of a Python list. 
Make sure to remove duplicate entries if present in the list.

---

### #Q7: List all room ids that receive more than 15 reviews per month (`reviews_per_month > 15`).

**Note:** Your answer should be in the form of a Python list of strings.

**Important:** Ignore room ids that do not have an entry for `reviews_per_month`
as indicated by a value of `None`.


### #Q8: What percentage of rooms are entire homes or apartments? (`room_type == "Entire home/apt"`)

**Note:** Your answer should be a float value between 0 and 100.


### #Q9: Which room ids in Staten Island (`neighborhood_group == "Staten Island"`) received their last review in the year 2017 or earlier?

**Note:** Your answer should be in the form of a Python list of strings.

**Important:** Ignore room ids that do not have an entry for `last_review`
as indicated by a value of `None`.

---

### Function Suggestion:

We require you to complete a function like the following to answer the 
next several questions (this is a requirement, and you will **lose points** if
you do not implement this function):

For the next two questions you should create and use a function which
finds a list of availabilities (`availability_365`) 
for the rooms with the specified `host_name` 
and within in the specified `neighborhood_group`.

**Note:** Checking for a matching host name should be case insensitive. You should
ignore rooms for which `availability_365` data is missing.

**Note:** If `neighborhood_group` is `None` you should consider rooms
within every neighborhood group.

```python
def availability_per_host_name(host_name, neighborhood_group=None):
    pass
    # TODO: create a list
    # TODO: add every availability matching the host_name and neighborhood_group to the list as an int
    # TODO: return your list of availabilities
```

### #Q10: What are the different availabilities of all rooms in the neighborhood group "Brooklyn" whose host name is "Stanley"?

**Note:** You should remove duplicate availabilities
and the list should be in descending order.

**Important:** You should use your previously written 
`availability_per_host_name` function to implement this logic.


### #Q11: What is the difference between the most and least availability among all rooms whose host name is "Helena" (`host_name == "Helena"`)?

**Note:** Your answer should be in the form of an integer.

**Important:** You should use your previously written 
`availability_per_host_name` function to implement this logic.

---

### Function Suggestion:

We require you to complete a function like the following to answer the 
next several questions (this is a requirement, and you will **lose points** if
you do not implement this function):

This function should return a list of prices of all the rooms within the geographical
location between latitudes `lat_min` and `lat_max` and longitudes `long_min` and
`long_max`.

```python
def find_prices_within(lat_min, lat_max, long_min, long_max):
    pass
    # TODO: create a list
    # TODO: add every price of rooms that locate in the given area to the list
    # TODO: return the filled list of prices
```

### #Q12: What is the average price among rooms within (40.50 <= latitude <= 40.75, -74.00 <= longitude <= -73.95)?

**Note:** Your answer should be a float value.

**Important:** You should use the `find_prices_within`
function to implement this logic.


### #Q13: What is the highest price among rooms within (40.75 <= latitude <= 41.00, -73.95 <= longitude <= -73.85)?

**Note:** Your answer should be an integer.

**Important:** You should use the `find_prices_within`
function to implement this logic.


### #Q14: What percentage of rooms within (40.50 <= latitude <= 41.00, -74.00 <= longitude <= -73.85) have a price less than 100?

**Note:** Your answer should be a float value between 0 and 100.

**Important:** You should use the `find_prices_within`
function to implement this logic.

**Hint:** Find the number of rooms in this area, and the number of rooms in the area that cost less than 100 (`price < 100`).

---

### #Q15: What is the average ratio of the number of reviews to availability in the neighborhood Manhattan Beach?

**Important:** You should ignore rooms that have `availability_365`== 0. You
should also ignore rooms for which the ratio cannot be computed due to missing data.


**Hints:**
1. The denominator is the availability of a room (`availability_365` column). 
   The numerator is the number of reviews of a room (`number_of_reviews` column).
2. Be careful! You need to compute the ratio for each room in the given neighborhood, 
   then take the average of those ratios. 
   Simply dividing the sum of reviews by the sum of availability
   will calculate the wrong answer.
   
### #Q16: What is the average ratio of the number of reviews to availability in the neighborhood Riverdale?

**Hint:** Instead of rewriting the same code or copy/pasting it, it would be easier for you to
go back to your answer for Q15 and make a function out of it. You will **not** lose
points for not implementing a function here, but it is highly recommended that you do so.

### #Q17: Which neighborhood in the neighborhood group Queens has the highest average ratio of the number of reviews to availability?

**Hint:** First make a list of all the neighborhoods in Queens, and find which of these neighborhoods has the highest average ratio.

**Hint:** If the program is taking too long to execute, 
make sure you're not running the logic on duplicate neighborhoods. 

---

### Function Suggestion:

We require you to complete a function to answer the 
next two questions (this is a requirement, and you will **lose points** if
you do not implement this function):

For the next two questions you should create a new function
and use it to find the percentage of names containing one word (`find_room_word`)
that also contain another word (`secondary_word`).


```python
def secondary_word_in_found_rooms(find_room_word, secondary_word):
    pass
```

### #Q18: What percentage of rooms whose name contains the word "cozy" also contain the word "home" in its name?

**Note:** All words are case insensitive.
Your answer should be a float value. You are expected to use the function 
`secondary_word_in_found_rooms` here.

**Hints:** 
1. The denominator is the number of rooms with 'cozy' in their name. The numerator is the number of rooms that have both 'cozy' and 'home' in their name.
2. You may find the function `find_room_names` useful for solving this 

### #Q19: What percentage of rooms whose name contains the word "pool" also contain the word "gym" in its name?

**Note:** All words are case insensitive.
Your answer should be a float value. You are expected to use the function 
`secondary_word_in_found_rooms` here.

---
### #Q20: What is the minimum amount of money one needs to spend to stay for 10 days in Manhattan, and then 5 days in Staten Island?

**Note:** Your answer should be in the form of type int. You may assume
that you will stay in exactly one room per `neighborhood_group`
throughout this trip. You should ignore rooms with missing `availability_365` or 
`minimum_nights` data. You don't have to worry about the exact dates of the availability.
You may assume that if the room is available for the required number of days, it will be available
whenever you want it.

**Hints:** 

1. Note that you need to check the `availability_365` as well as the `minimum_nights` of the rooms.
You can only stay in a room for 5 days if `availability_365 >= 5` and `minimum_nights <= 5`.
2. total cost = (lowest price in Manhattan) * 10 + (lowest price in Staten Island) * 5

---

#### READ ME

**Please remember** to `Kernel->Restart and Run All` to check for errors,
save your notebook, then run the `test.py` script
one more time before submitting the project.
To keep your code concise,
please remove your own testing code
that does not influence the correctness of answers.

**Finally,** if you are unable to solve a question and have partial code
that is causing an error when running `test.py`,
please comment out the lines in the cell for that question
before submitting your file.
Failing to do so will cause the auto-grader to fail when you submit your file
and give you 0 points even if you have some questions correctly answered.

Good luck and have fun navigating and understanding the Airbnb data!
