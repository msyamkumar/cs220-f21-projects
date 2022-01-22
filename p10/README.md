# Project 10: Twitter Data

# WARNING: Unless you took a time portal to become my student in the past, this is not the correct repository :) Please go to the correct github repository for the current semester. If you are a Fall'21 semester student though, you are in the right place.

<h2> Corrections/Clarifications
</h2>

 **(11/10/2021) - 4:20 pm**: Warning to not use DictReader, due to autograder errors.

**Find any issues?** Report to us:

- Saurabh Kulkarni <skulkarni27@wisc.edu>
- Hardik Chauhan <hchauhan2@wisc.edu>
- Dyah Adila <adila@wisc.edu>

## Learning Objectives

In this project, you will demonstrate your ability to:

- Read and write files
- Using dictionaries to map information
- Handle errors in parsing data
- Use Nametuples

## Coding Style Requirements

Remember that coding style matters! **We might deduct points for bad coding style.** Here are a list of coding style requirements:

- Do not use meaningless names for variables or functions (e.g. uuu = "my name").
- Do not write the exact same code in multiple places. Instead, wrap this code into a function and call that function whenever the code should be used.
- Do not call unnecessary functions.
- Avoid using slow functions multiple times within a loop.
- Avoid inappropriate use of data structures. A bad example: use for loop to search for a corresponding value in a dictionary with a given key instead of use `dictname[key]` directly.
- Don't name variables or functions as python keywords or built-in functions. Bad example: str = "23".
- Don't define multiple functions with the same name or define multiple versions of one function with different names. Just keep the best version.
- Put all `import` commands together at the second cell of `main.ipynb`, the first cell should be submission information (netid and etc). Only use `import` commands that are expressly allowed in the instructions.
- Think twice before creating a function without any parameters. Defining a new functions is unnecessary sometimes. The advantage of writing functions is that we can reuse the same code. If we only use this function once, there is no need to create a new function.
- Don't use absolute path such as `C://Desktop//220`. **You may only use relative path**. When we test your work on a different operating system, all of the test will fail and you will get a 0. Don't panic when you see this, please fix the error and resubmit your assignment.

**Warning:** Do **not** use `csv.DictReader` to read the csv files. It may cause errors with the autograder
due to version compatibility issues. It would be safest for you to use a function like `process_csv` that we
have been working with in the past, to parse csv files.

## Setup

**Step 1:** Download [`tweets.zip`](https://github.com/msyamkumar/cs220-f21-projects/tree/main/p10/tweets.zip ) and extract it to a directory on your computer (using [Mac directions](http://osxdaily.com/2017/11/05/how-open-zip-file-mac/) or [Windows directions](https://support.microsoft.com/en-us/help/4028088/windows-zip-and-unzip-files)). After extracting, you will find the following directories - `full_data`, `play`, `sample_data`.

**Step 2:** Download [`test.py`](https://github.com/msyamkumar/cs220-f21-projects/tree/main/p10/test.py)  to a directory that contains the uncompressed directories from Step 1 (`test.py` should be in the same directory as `full_data`,`play`, `sample_data`).

**Step 3:** Create a `main.ipynb` in the same location, which contains your P10 solutions.

## **Notes**:

 **Make sure `full_data`, `sample_data`, `main.ipynb` and `test.py` are in same directory**.

**Make sure your answers ignore files that begins with a "." . This is especially important on a Mac which might create a file called .DS_Store. You are expected to explicitly check and disregard files beginning with a "." in your answers.**

## Introduction

In this project, you'll be analyzing a collection of actual tweets.
This data is messy!  You'll face the following challenges:

* Data is spread across multiple files
* Some files will be CSVs, others JSONs
* The files may be missing values or may be too corrupt to parse.
* Some integer values may be represented as strings with a suffix of "M", "K", or similar

In p10, you'll write code to cleanup the data, representing everything as Tweet objects (you'll create a new type for these).  In p11, you'll analyze your clean data.

For this project, you'll create a new `main.ipynb` and answer questions in the usual format. **Please go through the [lab-p10](https://github.com/msyamkumar/cs220-f21-projects/tree/main/lab-p10) before working on this project.** In the lab, you will make helper functions and learn some useful techniques related to this project.

## Questions

For the first 6 questions, we'll ask you to list files where the order does not matter.

However, these aspects of the questions might vary:

* The directory being considered
* The contents of the list - file names or paths
* Filtering the contents of the directory, and only looking for certain file extensions. For eg Q5 and Q6 requires you to consider only csv files.

You may consider writing a single function to answer several questions
(Hint: things that change for different questions can often be
represented with parameters).

#### #Q1: How many files are present in the `sample_data` directory?

Hint: Look into the `os.listdir` function. Your answer should be an int.

#### #Q2: How many files are present in the `full_data` directory?

#### #Q3: What are the paths of all the files in the `sample_data` directory?

In order to achieve this, you need to use the `os.path.join()` function. Please do not hardcode "/" or "\\" because doing so will cause your function to fail on a computer that's not using the same operating system as yours. Again, remember to **use relative path instead of absolute path**.

#### #Q4: What are the paths of all the files in the `full_data` directory?
 Again, remember to **use relative path instead of absolute path**.

#### #Q5: What are the paths of the CSV files present in the `sample_data` directory?

#### #Q6: What are the paths of the json files present in the `full_data` directory?

----

For the following questions, you'll need to create a new Tweet type
(using namedtuple).  It will have the following attributes:

* tweet_id (string)
* username (string)
* num_liked (int)
* length (int)

Please ensure you define your namedtuple exactly according to the
specifications above, or you will be unable to pass the tests.  The length is the number of characters in `tweet_text`. You
should be able to use your Tweet type to create new Tweet objects, like this:

```python
t = Tweet("id123", "user456", 100, 140)
t
```

Running the above in a cell should produce output like this:

```python
Tweet(tweet_id='id123', username='user456', num_liked=100, length=140)
```

Notice that we're ignoring a few fields from the CSV, such as `date`
and `is_retweet`.

Note: Some Tweets have num_liked as String, e.g.
```python
Tweet(tweet_id='1467894593', username='USERID_2', num_liked='869M', length=136)
```
 Your code is expected to convert these string values that end with an 'M' or a 'K', to their respective integer values.

----

#### #Q7: What are the tweets present in the CSV file `2.csv` in `sample_data`?

The expected output format is a list of the Tweet namedtuples, where the order does not matter

```python
[Tweet(tweet_id='1467812799', username='USERID_7', num_liked=3340, length=103),
 Tweet(tweet_id='1467812964', username='USERID_10', num_liked=3684, length=93),
 Tweet(tweet_id='1467813137', username='USERID_5', num_liked=6816, length=20),
 Tweet(tweet_id='1467813579', username='USERID_1', num_liked=1348, length=64),
 Tweet(tweet_id='1467813782', username='USERID_1', num_liked=4770, length=79)]
```
You are expected to write a function to solve this question.
#### #Q8: What are the tweets present in the CSV file `3.csv` in `full_data`?

Use the same function as Q7 to solve this question.

#### #Q9: What are the tweets present in the CSV file `2.csv` in `full_data`?

Use the same function as Q7 to solve this question.

There is a chance that running the Q7 function for Q9 resulted in a crash, or you had missing data. This is because some of the
rows in this file, are incomplete or inconsistent in some way. You
must now go back and modify your Q7 function to deal with
situations like this.

In short, whenever you see a row in the CSV file which does not have
all **6** fields present, even `date` and `is_retweet`, just skip that row and move on to the next
one, parsing what remains.

#### #Q10: What are the tweets present in the JSON file `1.json` in `sample_data`?

Same output format as q7 is expected here.

Just like before with the CSV files, we're going to now parse a JSON
file and convert it to a list of Tweets, so that all of our data
from different files is going into one common format that's easy for
us to work with.

The JSON files have the data saved as one big dictionary. The keys in the dictionary are the tweet_id, and the values are a smaller dictionary, containing all the details of the tweet with that tweet_id. Feel free to open up a JSON file and take a look at it to get a sense of how it's structured (this is always a great first step when you're trying to parse data you're unfamiliar with).

Your task here is to convert each JSON file to a **list of Tweet
objects** (similar to what we did when parsing the CSVs).  Each
key-value pair in our big dictionary therefore corresponds to one
namedtuple in the list.

Here's the first tweet in the JSON file, `1.json` in `sample_data`

```json
{
  "1467810369": {
    "date": "Mon Apr 06 22:19:45 PDT 2009",
    "username": "USERID_4",
    "tweet_text": "@switchfoot http://twitpic.com/2y1zl - Awww, that's a bummer.  You shoulda got David Carr of Third Day to do it. ;D",
    "is_retweet": false,
    "num_liked": 315
},
```

And here's the corresponding namedtuple:

`Tweet(tweet_id='1467810369', username='USERID_4', num_liked=315, length=115)`

If there are any tweets where `num_liked` is `unknown` or `unkown` or throws an error,  treat it as 0. Remember to convert `num_liked` values that end with a 'K' or 'M' to int.

The expected output format is:

```python
[Tweet(tweet_id='1467810369', username='USERID_4', num_liked=315, length=115),
 Tweet(tweet_id='1467810672', username='USERID_8', num_liked=5298, length=111),
 Tweet(tweet_id='1467810917', username='USERID_8', num_liked=533, length=89),
 Tweet(tweet_id='1467811184', username='USERID_6', num_liked=2650, length=47),
 Tweet(tweet_id='1467811193', username='USERID_8', num_liked=2101, length=111)]
```

You are expected to write a function to solve this question.
#### #Q11: What are the tweets present in the JSON file `2.json` in `sample_data`?

You are expected to use the function from Q10 to solve this  question.

#### #Q12: What are the tweets present in the JSON file `3.json` in `full_data`?

You are expected to use the function from Q10 to solve this  question.

#### #Q13: What are the tweets present in the JSON file `1.json` in `full_data`?
You are expected to use the function from Q10 to solve this  question.

There is a good chance that you encountered an error while reading `1.json`. This is because the `1.json` file is broken. Unfortunately, unlike CSV files, broken JSON files are much more complicated to fix, we can't just skip over one tweet and salvage the rest.  Instead, your Q10 function should skip any file it cannot parse using `json.load` and just return an empty list. Modify your Q10 function with `try` and `except` to skip the broken file.



#### #Q14: Return all the tweet objects with a length greater than 140 in `full_data`.

Create a function whose inputs are an integer `textLength`, and a string `directory`  that returns a list containing all the tweets with  text greater than `textLength` in the `directory`. It should read all the files in the `directory` and combine the tweets into one list. Remember to deal with broken json files by skipping them.

```python
def tweets_greater_than(textLength,directory):
  	#TODO: obtain tweets from all files in directory and filter by greater than textLength
```




#### #Q15: Return a list of all the tweet objects with a length greater than 100 in `sample_data`.

Use the function from Q14

#### #Q16: Return a list of all the tweet objects in `full_data`.
Use the function from Q14

#### #Q17: Which file in the directory `sample_data` contains the tweet with tweet_id '1467812723'?

Be sure to produce a **list of relative paths** (even if it's just 1 path)


Hint: Use the functions you've written to help you accomplish this task, as it involves a combination of looking through all the files in a folder, parsing them, and then looking through the parsed list.

#### #Q18: Which file in the directory `full_data` contains the tweet with tweet_id '1467916700'?

Be sure to produce a **list of paths** (even if it's just 1 path)


#### #Q19: Which files in the directory `full_data` contain tweets by the user "USERID_3"?

Be sure to produce a **list of paths** (even if it's just 1 path)

#### #Q20: What are the first 20 tweets present in all the files in the `full_data` directory and the `sample_data` directory, sorted by num_liked?

Produce a single **list of Tweets** of length 20 containing the first 20 tweets sorted in **descending order by num_liked**.
Recall that you learnt how to sort various nested data structures in "Function References" and "Iterators and comprehensions" lectures. 

The first 5 tweets of the expected output are:

```python
[Tweet(tweet_id='1467894593', username='USERID_2', num_liked=869000000, length=136),
 Tweet(tweet_id='1467894600', username='USERID_8', num_liked=915000, length=67),
 Tweet(tweet_id='1467853431', username='USERID_10', num_liked=9936, length=30),
 Tweet(tweet_id='1467875163', username='USERID_2', num_liked=9891, length=69),
 Tweet(tweet_id='1467860904', username='USERID_7', num_liked=9851, length=30)]
```



That's it for p10. In the next project, we'll begin using the data structures we've set up to do some analysis that spans across multiple files!

### Before turning in:
Be sure to run test.py and make sure there are no errors. If you turn in a version of your code which fails on test.py (i.e. you can't see which questions you got right or not), **we will deduct 5 points**. If the autograder is failing but you still want to turn in, you can see which question it is failing on and comment out the code for that question, essentially leaving it out. 

After you add your name and the name of your partner to the notebook, please remember to **Kernel->Restart and Run All** to check for errors then run the test.py script one more time before submission.  To keep your code concise, please **remove your own testing code that does not influence the correctness of answers.** 
