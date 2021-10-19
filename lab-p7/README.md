# Lab 7: Dictionaries

In this lab, we'll practice using dictionaries to help you get ready for p7. 
Start these exercises in a new Jupyter notebook.

## Exercises

### Counting Characters in a String

Fill in the blanks so that `counts` becomes a dictionary where each
key is a character and the corresponding value is how many times it
appears in the string `PI`.

*Question:  Before beginning, which character
do you think will occur the most often?*


```python
# counting characters in a string
PI = "three, dot, one, four, one, five, nine, two, six, five, three, five, nine"
counts = {}
for char in ????:
    if not char in counts:
        counts[????] = ????
    else:
        ????[char] += ????
counts
```

If done correctly, your code output should be similar to something like this:

```python
{'t': 4, 'h': 2, 'r': 3, 'e': 11, ',': 12, ' ': 12, 'd': 1, 'o': 5, 'n': 6, 'f': 4, 'u': 1, 'i': 6, 'v': 3, 'w': 1, 's': 1, 'x': 1}
```

### Counting Words in a String by using .split()

Fill in the blanks such that counts becomes a dictionary where each key is a word in a list generated from the string `PI` and the corresponding value is how many times it occured in `PI`.


```python
# counting words in a string
PI = "three, dot, one, four, one, five, nine, two, six, five, three, five, nine"
counts = {}
for word in PI.????(????):
    if ????:
        ????
    else:
        ????
counts
```

If done correctly, your code output should be smilar to something like this:

```python
{'three': 2, 'dot': 1, 'one': 2, 'four': 1, 'five': 3, 'nine': 2, 'two': 1, 'six': 1}
```

### Dictionary from a list of Keys and a list of Values

Fill in the blanks to create a dictionary that maps the English words in list `keys` to their corresponding Spanish translations in list `vals`:

*Question: Before you write the code, ask yourself...what is this code trying to do?*


```python
# dict from list of keys and values
keys = ["two", "zero"]
vals = ["dos", "cero"]
english_to_spanish = ???? # empty dictionary
for i in range(len(????)):
    english_to_spanish[keys[????]] = ????
english_to_spanish
```

The resulting dictionary containing the mapping from English to Spanish
words, should look like this:

```python
{'two': 'dos', 'zero': 'cero'}
```

Now lets try using your `english_to_spanish` dictionary to partially translate the following English sentence.
Not exactly a replacement for Google translate just yet, but it's
a good start...

```python
words = "I love Comp Sci two two zero".split(" ")
for i in range(len(words)):
    default = words[i] # default is to not translate it
    words[i] = english_to_spanish.get(words[i], default)
" ".join(words)
```
*Question: What is the purpose of the 'default' variable?*

*Question: What is the purpose of the line words[i] = english_to_spanish.get(words[i], default)?*



### Flipping Keys and Values

What if we want a dictionary to convert from Spanish back to English?


```python
# flipping keys and values
sp2en = {}
for en in english_to_spanish:
    sp = ????
    sp2en[sp] = ????
sp2en
```

You should get this:

```python
{ 'dos': 'two', 'cero': 'zero'}
```

### Dictionary Division

What if we want to do multiple division operations, but we have all our
numerators in one dictionary and all our denominators in another. 
Can you fill in the missing code to help do these divisions correctly?

```python
numerators = {"A": 1, "B": 2, "C": 3}
denominators = {"A": 2, "B": 4, "C": 4}
result = {}
for key in ????:
    result[????] = ????[key] / ????[key]
result
````

If done correctly, you should get `{'A': 0.5, 'B': 0.5, 'C': 0.75}`.


### Print a Dictionary by sorted keys

Imagine that a dorm kept statistics on the number of noise complaint incidents in different years.
Complete the code so it prints the incidents per year, with earliest year first.


```python
# print a dictionary sorted by keys
incidents = {2017: 14, 2020: 18, 2018: 13, 2019: 16, 2021: 25, 2016: 10}
keys = sorted(list(????.keys()))
for k in ????:
    print(k, incidents[????])
```

``` your result should look like this:
2016 10
2017 14
2018 13
2019 16
2020 18
2021 25
```

### Histogram

Modify the above code so it prints a yearly value histogram using the '*' character, like this:

```
2016 **********
2017 **************
2018 *************
2019 ****************
2020 ******************
2021 *************************
```

### Dictionary Max

Complete the following code to find the year with the highest number of incidents:

```python
# find the best key
incidents = {2017: 14, 2020: 18, 2018: 13, 2019: 16, 2021: 25, 2016: 10}
best_key = None
for key in incidents:
    if best_key == None or incidents[????] > incidents[????]:
        best_key = ????
print("Year", best_key, "had", incidents[????], "incidents (the max)")
```

## Project 7

Hopefully, this lab helped you get familiar with dictionaries! Now you're ready to start p7. If you have time left in lab, go ahead and start p7 now, so you can ask your lab TA questions. Remember to only work with at most one partner on p7 from this point on. Have fun!


