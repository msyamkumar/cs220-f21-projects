# Project 8: Going to the Movies

## Clarifications/Corrections

None yet.

**Find any issues?** Report to us:  
- Dyah Adila [adila@wisc.edu](mailto:adila@wisc.edu)
- Raj Aryan Singh [rsingh94@wisc.edu](mailto:rsingh94@wisc.edu)

## Learning Objectives

In this project, you will demonstrate how to:
- integrate relevant information from various sources (e.g. multiple csv files)  
- build appropriate data structures for organized and informative presentation (e.g. list of dictionaries)
- practice good coding style

## Coding Style Requirements

Remember that coding style matters! **We may deduct points for bad coding style.** In addition to the [requirements from p7](https://github.com/msyamkumar/cs220-f21-projects/tree/main/p7#coding-style-requirements), here are several other common bad coding habits to avoid:

- Do not use meaningless names for variables or functions (e.g. uuu = "my name").
- Do not write the exact same code in multiple places. Instead, wrap this code into a function and call that function whenever the code should be used.
- Do not call unnecessary functions (i.e. functions with no parameters).
- Avoid calling slow functions multiple times within a loop.
- Avoid calling functions that iterate over the entire dataset within a loop; instead, call the function before the loop and store the result in a variable.

**Warning:** Please do not use the method `csv.DictReader` for p8. Although the required output can be obtained using this method, one of the learning outcomes of this project is to demonstrate your ability to build dictionaries with your own code.

## Introduction

In this project and the next, we will be working on the [IMDb Movies Dataset](https://www.imdb.com/interfaces/). We will use Python  to discover some cool facts about our favorite movies, actors, and directors.

In this project, you will combine the data from the movie and mapping files into a more useful format. As usual, hand in the `main.ipynb` file (use the `#qN` format).  Start by downloading the following files: [`test.py`](https://github.com/msyamkumar/cs220-f21-projects/blob/main/p8/test.py), [`small_mapping.csv`](https://github.com/msyamkumar/cs220-f21-projects/blob/main/p8/small_mapping.csv), [`small_movies.csv`](https://github.com/msyamkumar/cs220-f21-projects/blob/main/p8/small_movies.csv), [`mapping.csv`](https://github.com/msyamkumar/cs220-f21-projects/blob/main/p8/mapping.csv), and [`movies.csv`](https://github.com/msyamkumar/cs220-f21-projects/blob/main/p8/movies.csv).

## The Data

Open `movies.csv` and `mapping.csv` in any Spreadsheet viewer, and see what the data looks like. `movies.csv` has ~33000 rows and `mapping.csv` has ~84000 rows. Before we start working with these very large datasets, let us start with some much smaller datasets. `small_movies.csv` and `small_mapping.csv` have been provided to help you get your core logic right with a smaller dataset. `small_movies.csv` has the same columns as (but fewer rows than) `movies.csv`, and `small_mapping.csv` has the same columns as (but fewer rows than) `mapping.csv`. In the next project (p9), you will be mostly working mainly with `movies.csv` and `mapping.csv`.

`small_movies.csv` and `movies.csv` have 7 columns: `title`, `year`, `genres`, `duration`, `directors`, `actors`, and `rating`.

Here are a few rows from `movies.csv`:
```
title,year,genres,duration,directors,actors,rating
tt1735898,2012,"Action, Adventure, Drama",127,nm2782185,"nm0829576, nm1165110, nm0000234, nm3510471",6.1
tt1210166,2011,"Biography, Drama, Sport",133,nm0587955,"nm0000093, nm1706767, nm0000450, nm0000705",7.6
tt0058079,1964,Horror,60,"nm0554924, nm0692414","nm0001033, nm0067280, nm0593360, nm0388885",3.0
```

The `year` column refers to the year the movie was released in, `duration` refers to the duration of the movie (in minutes), `genres` refers to the genres that the movie belongs to, and `rating` refers to the IMDb rating of that movie. The weird alphanumeric sequences used for the columns `title`, `actors`, and `directors` are the unique identifiers that IMDb uses for identifying either an actor or a director or a movie title. The IDs that begin with `tt` refer to a movie title, and the IDs that begin with `nm` refer to a person's name (either an actor or a director).

`small_mapping.csv` and `mapping.csv` have 2 columns: `id` and `name`, mapping these IDs to their names.

Here are a few rows from `mapping.csv`:

```
tt0110991,Ring of Steel
tt0037244,San Diego I Love You
tt10003008,The Rental
nm0364744,Hank Harris
nm0563220,Zola Maseko
```

If you are ready, let's get started with data plumbing!


# Data Plumbing

A lot of data science work often involves *plumbing*, the process of
getting messy data into a more useful format.  We have already dealt with
it in passing, in p7. Data plumbing is the focus of this project. 
We'll develop and test some functions that will be very
helpful in p9:

1. `get_mapping(path)`: this loads a mapping file that can be used to lookup names from IDs
2. `get_raw_movies(path)`: this loads movie data with info represented using IDs
3. `get_movies(movies_path, mapping_path)`: this uses the other two functions to load movie data, then replace the IDs with names

Note - the variable `path` is of type string

---

Write a function that starts like this:

```python
def get_mapping(path):
    csv_data = process_csv(path) # you can use this function from p7
    # TODO: make a dictionary where keys are the ID's and values are the names
```

When called, the `path` should refer to one of the mapping files
(e.g., "small_mapping.csv").  The function should return a dictionary
that maps IDs (as keys) to names (as values), based on the file
referenced by `path`.  For example, this code:

```python
mapping = get_mapping("small_mapping.csv")
mapping
```

should output this (order doesn't matter):

```python
{'tt1950186': 'Ford v Ferrari',
 'tt2267998': 'Gone Girl',
 'nm0000255': 'Ben Affleck',
 'nm0003506': 'James Mangold',
 'nm0000354': 'Matt Damon',
 'nm1256532': 'Jon Bernthal',
 'nm0683253': 'Rosamund Pike',
 'nm0000288': 'Christian Bale',
 'nm0000399': 'David Fincher'}
```

Note that the mapping files DO NOT have a CSV header.

The following questions pertain to `small_mapping.csv` unless
otherwise specified.

---

### \#Q1: What is returned by your `get_mapping("small_mapping.csv")` function?

You shouldn't be surprised to see the results are exactly the dictionary shown above if your function works correctly. Please (1) store the result in a variable for use in subsequent questions, and (2) display the result in the output area so the grading script can find your answer. By storing the result in a variable, you can avoid having to call this time-consuming function in the future.

### #Q2: What is the value associated with the key "nm0000288"?

Hint: Use the dictionary returned earlier.

### #Q3: What are the values in the mapping (dictionary) associated with keys that begin with "nm"?

The answer should be a Python list. The order does not matter.

### #Q4: List the keys of all the people in the above mapping, whose last name is "Pike".

The answer should be a Python list. The order does not matter.

**Warning**: Make sure that you only consider the people whose **last name** is "Pike". To get full credit for this problem, given a larger dataset, your code should **not** return any of the following:
1. IDs of any movie titles,
2. IDs of people whose last name is not "Pike", but the first or middle name is "Pike"
3. IDs of people whose last name is not "Pike", but starts with the string "Pike" (such as "Piker").

---

Now, let's move on to read movie files! Build a function named `get_raw_movies` that takes the path to a
CSV file (e.g., "small_movies.csv" or "movies.csv") as the only parameter and
returns a list of dictionaries where each dictionary represents a
movie as follows:

```python
{
    'title': "movie-id",
    'year': <the year as an integer>,
    'genres': ["genre1", "genre2", ...],
    'duration': <the duration as an integer>,
    'directors': ["director-id1", "director-id2", ...],
    'actors': ["actor-id1", "actor-id2", ....],
    'rating': <the rating as a float>
}
```

Note that unlike `small_mapping.csv`, the movie files DO have a CSV header.

To be consistent, the values for `directors`, `actors`, and `genres`
are always of type \<list\>, even if some lists might only contain a single item.

---

### #Q5: What does `get_raw_movies("small_movies.csv")` return?

The result should be this (the order of the movies *does* matter):
```python
[{'title': 'tt1950186',
  'year': 2019,
  'genres': ['Action', 'Biography', 'Drama'],
  'duration': 152,
  'directors': ['nm0003506'],
  'actors': ['nm0000354', 'nm0000288', 'nm1256532'],
  'rating': 8.1},
 {'title': 'tt2267998',
  'year': 2014,
  'genres': ['Drama', 'Mystery', 'Thriller'],
  'duration': 149,
  'directors': ['nm0000399'],
  'actors': ['nm0000255', 'nm0683253'],
  'rating': 8.1}]
```
If your answer looks correct, but does not pass `test.py`, make sure that the datatypes are all correct. Also make sure that the actors and directors are in the same order, as here.

As with `get_mapping`, keep the result returned by `get_raw_movies` in a variable for use in answering future questions. Do not call `get_raw_movies` every time you need data from the movies file.



### #Q6: How many actors does the movie at index 1 have?

Hint: Use the dictionary from Q5.

### #Q7: What is the ID of the first actor listed for the movie at index 0?

Hint: use the dictionary from Q5.

---
You may have noticed that `actors`, `directors`, and `title` are represented by IDs instead of actual names. Write a function named
`get_movies(movies_path, mapping_path)` that loads data from the
`movies_path` file using `get_raw_movies` and converts the IDs to
names using a mapping based on the `mapping_path` file, which you
should load using your `get_mapping` function.

Each dictionary in the list should look like this:

```python
{
    'title': "the movie name",
    'year': <the year as an integer>,
    'genres': ["genre1", "genre2", ...],
    'duration': <the duration as an integer>,
    'directors': ["director-name1", "director-name2", ...],
    'actors': ["actor-name1", "actor-name2", ....],
    'rating': <the rating as a float>
}
```

Notice the difference between the previous one and this (IDs are replaced by names). This list of dictionaries is essential for almost all of the following questions.

We recommend you break this down into several steps.  Start with the simple case the `title`: try to translate from the ID code to the name of the movie. Then work on translating for actors and directors after you get the title working. The `actors` and `directors` are more complicated because they are lists.

After you implement your function, call it and store the result as a variable named `small_data`:

```python
small_data = get_movies("small_movies.csv", "small_mapping.csv")
```

### #Q8: What is `small_data`?

The result should look something like this :

```python
[{'title': 'Ford v Ferrari',
  'year': 2019,
  'genres': ['Action', 'Biography', 'Drama'],
  'duration': 152,
  'directors': ['James Mangold'],
  'actors': ['Matt Damon', 'Christian Bale', 'Jon Bernthal'],
  'rating': 8.1},
 {'title': 'Gone Girl',
  'year': 2014,
  'genres': ['Drama', 'Mystery', 'Thriller'],
  'duration': 149,
  'directors': ['David Fincher'],
  'actors': ['Ben Affleck', 'Rosamund Pike'],
  'rating': 8.1}]
```

### #Q9: What is `small_data[1]["title"]`?

Just paste `small_data[1]["title"]` into a cell and run it.  We're doing
this to check that the structures in `small_data` (as returned by
`get_movies` above) contain the correct data.

### #Q10: What is `small_data[0]["actors"]`?

### #Q11: What is `small_data[-1]["directors"]`?

---

If you've gotten this far, your functions must be working pretty well
with small datasets.  So let's try the full dataset!

```python
movies = get_movies("movies.csv", "mapping.csv")
```

**Warning**: You are **not** allowed to call `get_movies` more than once for the
"movies.csv" file in your notebook.  Reuse the `movies` variable
instead, which is more efficient. Otherwise, we will deduct points for bad coding style.

---

### #Q12: What are the 2017th to 2019th (inclusive) rows in movies?

Please return a list of dictionaries whose **format** is like this:

```python
[{'title': 'Ambassador Bill',
  'year': 1931,
  'genres': ['Comedy'],
  'duration': 70,
  'directors': ['Sam Taylor'],
  'actors': ['Will Rogers',
   'Marguerite Churchill',
   'Greta Nissen',
   'Tad Alexander'],
  'rating': 6.2},
 {'title': 'The Etruscan Smile',
  'year': 2018,
  'genres': ['Drama'],
  'duration': 107,
  'directors': ['Oded Binnun', 'Mihal Brezis'],
  'actors': ['Brian Cox', 'JJ Feild', 'Thora Birch', 'Rosanna Arquette'],
  'rating': 6.8},
 {'title': 'In Old Oklahoma',
  'year': 1943,
  'genres': ['Romance', 'Western'],
  'duration': 102,
  'directors': ['Albert S. Rogell'],
  'actors': ['John Wayne',
   'Martha Scott',
   'Albert Dekker',
   "George 'Gabby' Hayes",
   'Marjorie Rambeau'],
  'rating': 6.5}]
```


### #Q13: What are the last 2 rows in movies?

Please return a list of dictionaries whose **format** is like this:

```python
[{'title': 'Battle Bots',
  'year': 2018,
  'genres': ['Action', 'Adventure', 'Sci-Fi'],
  'duration': 67,
  'directors': ['Mark Polonia'],
  'actors': ['Danielle Donahue', 'Jeff Kirkendall', 'Marie DeLorenzo'],
  'rating': 1.9},
 {'title': 'Inescapable',
  'year': 2003,
  'genres': ['Drama'],
  'duration': 82,
  'directors': ['Helen Lesnick'],
  'actors': ['Natalie Anderson', 'Tanna Frederick', 'Athena Demos'],
  'rating': 4.2}]
```

------

Now that we have created this data structure `movies`, we can start doing some fun things with the data!
We will continue working on this data structure for the next project (p9) as well.

Let us now use this data strucutre `movies` to create a search bar like the one in Netflix!
For now, copy the following function to your notebook, **but don't change it in any way**.
This function takes in keywords like a substring of a title, a genre, or the name of a person,
and returns a list of relevant movies with that title, genre, or actor/director.

```python
# You are *not* allowed to change this function

def search_bar(movies, keyword):
    '''given a list of movie dictionaries and a keyword, 
    returns a list of movies that contains the keyword'''
    idx = 0
    while idx < len(movies):
        movie = movies[idx]
        if (keyword not in movie['title']) and (keyword not in movie["genres"]) and  (keyword not in movie["directors"]) and (keyword not in movie["actors"]):
            movies.pop(idx)
        else:
            idx += 1
    return movies
```

The `movies` parameter is for a list of movie dictionaries (similar to what is returned by `get_movies`) and `keyword` is a keyword to filter on. 
The function returns the movies in `movies` that contains `keyword` in either its title, genre, actors, or directors.

------

### #Q14: List all the movies in the dataset, that contain "Harry Potter" in the title.

Note that the `search_bar` function has an **undesirable** side effect that we will fix in q15 and you may need restart the kernel and run all. For this problem you are required to follow these requirements:
1. Answer using `search_bar`
2. Do **not** call `get_movies` on "movies.csv" more than once in your notebook

### #Q15: Which genres of movies did the actor Paul Walker ever play in?

**Hint:** we've set you up a bit to encounter a bug.  Review the copy functions in the `copy` module and see if you can use one of them to overcome the shortcomings of the `search_bar` function we're forcing you to use. You can call one of the copy functions outside of the  `search_bar` function to copy the dataset. You might need to go back and tweak your q14 answer and potentially do a "Restart & Run All" on your notebook after you've fixed the bug. Remember that you need to follow the requirements below:
1. Answer using `search_bar`
2. Do **not** call `get_movies` on "movies.csv" more than once in your notebook
3. Do **not** change `search_bar`


**Extra hint:** remember optimizing in lab-p8. Avoid looping through the whole dataset whenever possible. Instead, you can get a list of movies relevant to the question first, and then loop through this list

Return a list of genres.

---

The function `search_bar` was a good start, but the function has some limitations. For one, it has to 
loop through the entire dataset each time it is called, so it is a little slow. This is perfectly fine, when the
keyword is a substring of a movie title. But for example, when the keyword is a genre,
it will not be efficient to go through the dataset every time. Since there are so few genres to deal with,
in the spirit of optimizing code, it makes sense to just make a list of movies for each genre and
store it in a variable. Then we can simply look up this variable instead of calling `search_bar` each time.

### Function Suggestion:
We suggest you complete a function like the following to answer the next several questions (this is a requirement, and you will **lose points** if you do not implement this function).

This function should return a dictionary that maps each genre to a list of all movies with that genre. For instance:
```python
{'Action': 
    [{'title': 'They Live',
      'year': 1988,
      'genres': ['Action', 'Horror', 'Sci-Fi'],
      'duration': 94,
      'directors': ['John Carpenter'],
      'actors': ['Roddy Piper', 'Keith David', 'Meg Foster'],
      'rating': 7.3},
   ...],
'Romance': [...list of romance movies],
'Horror': [...list of horror movies],
...
}
```
**Note:** Note that if a movie falls under multiple genres, it must appear under *all* of these genres in the dictionary.

If you find it challenging to write this function, you can start with the following code snippet:
```python
def genre_search_bar(movies):
    '''given a list of movie dictionaries, 
    returns a dict in which the key is the genre and 
    the value is a list of all movies that contain that genre'''
    #TODO: initialize a dictionary
    #TODO: loop through all movies
    #TODO: loop through all genres in this movie
    #TODO: if this genre is not a key in our dictionary, set the value associted with this genre to an empty list
    #TODO: if we already have this genre in our dictionary, append the movie to the list associated with this genre
```
**Warning:** You should first call `genre_search_bar` on `movies` and store the result in a variable to avoid calling it on the same list of movies multiple times in these questions. **You will lose points** if you call `genre_search_bar` **on the same list of movies** more than once. 

**Hint:** You can also look up the section on *Bucketizing* from lab-p8 for some help here. You 
implemented a similar function there.

You can create similar functions for actors and directors as well. You will deal more with such functions 
in p9. *Can you figure out why it is **not** a good idea to create a similar function for **substrings** of the title*?

For now, let us see what we can do with `genre_search_bar`.

---

### #Q16: List the unique genres in our dataset.

**Note**: Make sure you return a list

### #Q17: How many Action movies do we have the dataset?

### #Q18: What is the average rating of Comedy movies?

### #Q19: List all the genres of movies that Christopher Nolan has ever acted/directed in.

**Hint**: Notice that this question is nearly identical to q15. However, using `genre_search_bar` 
together with `search_bar`, you can solve this question much quicker now. We expect that you will answer this question **without any explicit control strucures (loops, if statements)**

### #Q20: Which movie genre does the actress Kristen Stewart play the most?

Your answer should be a single genre.  This code will need a control stucture that finds a maximum.

---

**Warning**: Remember that there is a bug in q15! If you skipped that question, and solved it after you solved q16 - q20, you may find 
that your answers for q16 - q20 are incorrect now. If you solve q15 after you solve q16- q20, please verify that this does
not happen.

**Warning:** Recall that in q4, you were supposed to make a list of keys of people whose **last name** is "Pike". Since `small_movies` is 
a small dataset, you might have got the correct answer without the correct code. In that case, you will lose points during code review.
You can check to see if you got the correct code
by running that code in a separate cell on the larger `mapping.csv` dataset. If your code is correct, the answer will not change.

---
Good luck!

### Before turning in:
Be sure to run test.py and make sure there are no errors. If you turn in a version of your code which fails on test.py (i.e. you can't see which questions you got right or not), **we will deduct 5 points** from p8 onwards. If the autograder is failing but you still want to turn in, you can see which question it is failing on and comment out the code for that question, essentially leaving it out. 

After you add your name and the name of your partner to the notebook, please remember to **Kernel->Restart and Run All** to check for errors then run the test.py script one more time before submission.  To keep your code concise, please **remove your own testing code that does not influence the correctness of answers.** In particular, **remove any code that displays large lists such as `movies`**.
