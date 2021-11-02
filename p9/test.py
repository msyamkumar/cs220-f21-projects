import ast, os, sys, subprocess, json, re, collections, math, warnings

# check the python version
if sys.version[:5] < '3.7.0':
    warnings.warn('Your current python version is {}. Please upgrade your python version to at least 3.7.0.'.format(
        sys.version[:5]))

################################################################################
REL_TOL = 6e-04  # relative tolerance for floats
ABS_TOL = 15e-03  # absolute tolerance for floats
LINTER = False  # set to False if linter should be turned off for project
################################################################################

PASS = "PASS"
TEXT_FORMAT = "text"  # question type when expected answer is a str, int, float, or bool
TEXT_FORMAT_UNORDERED_LIST = "text list_unordered"  # question type when the expected answer is a list where the order does *not* matter
TEXT_FORMAT_ORDERED_LIST = "text list_ordered"  # question type when the expected answer is a list where the order does matter
TEXT_FORMAT_SPECIAL_ORDERED_LIST = "text list_special_ordered"  # question type when the expected answer is a list where order does matter, but with possible ties. All tied elements are put in a list, where internal order does not matter.
TEXT_FORMAT_DICT = "text dict"  # question type when the expected answer is a dictionary
TEXT_FORMAT_LIST_DICTS_ORDERED = "text list_dicts_ordered"  # question type when the expected answer is a list of dicts where the order does matter
PNG_FORMAT = "png"  # use when the expected answer is an image

Question = collections.namedtuple("Question", ["number", "weight", "format"])

questions = [
    Question(number=1, weight=1, format=TEXT_FORMAT),
    Question(number=2, weight=1, format=TEXT_FORMAT),
    Question(number=3, weight=1, format=TEXT_FORMAT_LIST_DICTS_ORDERED),
    Question(number=4, weight=1, format=TEXT_FORMAT_LIST_DICTS_ORDERED),
    Question(number=5, weight=1, format=TEXT_FORMAT_LIST_DICTS_ORDERED),
    Question(number=6, weight=1, format=TEXT_FORMAT_LIST_DICTS_ORDERED),
    Question(number=7, weight=1, format=TEXT_FORMAT_DICT),
    Question(number=8, weight=1, format=PNG_FORMAT),
    Question(number=9, weight=1, format=TEXT_FORMAT_DICT),
    Question(number=10, weight=1, format=PNG_FORMAT),
    Question(number=11, weight=1, format=TEXT_FORMAT_DICT),
    Question(number=12, weight=1, format=TEXT_FORMAT_DICT),
    Question(number=13, weight=1, format=PNG_FORMAT),
    Question(number=14, weight=1, format=TEXT_FORMAT_SPECIAL_ORDERED_LIST), # DO NOT check answer by manual lookup of the test file. The answer is stored in a different format here. Run test.py 
    Question(number=15, weight=1, format=TEXT_FORMAT_LIST_DICTS_ORDERED),
    Question(number=16, weight=1, format=TEXT_FORMAT_LIST_DICTS_ORDERED),
    Question(number=17, weight=1, format=TEXT_FORMAT_SPECIAL_ORDERED_LIST), # DO NOT check answer by manual lookup of the test file. The answer is stored in a different format here. Run test.py to check if your answer is correct.
    Question(number=18, weight=1, format=TEXT_FORMAT_SPECIAL_ORDERED_LIST), # DO NOT check answer by manual lookup of the test file. The answer is stored in a different format here. Run test.py to check if your answer is correct.
    Question(number=19, weight=1, format=TEXT_FORMAT_SPECIAL_ORDERED_LIST), # DO NOT check answer by manual lookup of the test file. The answer is stored in a different format here. Run test.py to check if your answer is correct.
    Question(number=20, weight=1, format=TEXT_FORMAT_SPECIAL_ORDERED_LIST), # DO NOT check answer by manual lookup of the test file. The answer is stored in a different format here. Run test.py to check if your answer is correct.
]
question_nums = set([q.number for q in questions])

# JSON and plaintext values
expected_json = {
    "1": 8.8,
    "2": 7.25,
    "3": [{'title': 'Proud American',
              'year': 2008,
              'genres': ['Drama'],
              'duration': 115,
              'directors': ['Fred Ashman'],
              'actors': ['Michael G. Davis',
               'Cecelia Antoinette',
               'Marie Antoinette',
               'Michelle Ashman'],
              'rating': 1.1},
             {'title': 'Troy: The Resurrection of Aeneas',
              'year': 2018,
              'genres': ['Animation', 'Action', 'Adventure'],
              'duration': 60,
              'directors': ['Aeneas Middleton'],
              'actors': ['Aeneas Middleton', 'Hardley Davidson'],
              'rating': 1.1},
             {'title': 'Browncoats: Independence War',
              'year': 2015,
              'genres': ['Action', 'Sci-Fi', 'War'],
              'duration': 98,
              'directors': ['Francis Hamada'],
              'actors': ['Beth Bemis',
               'Richard Martinsen',
               'Will James Johnson',
               'Nathan Cosmo Rahn'],
              'rating': 1.1},
             {'title': 'The Time Machine (I Found at a Yardsale)',
              'year': 2011,
              'genres': ['Sci-Fi'],
              'duration': 84,
              'directors': ['Steven A. Sandt'],
              'actors': ['George Abdelmalak', 'Steven Ronald Brattman', 'Elise Caloca'],
              'rating': 1.1},
             {'title': 'A Moment of Youth',
              'year': 2011,
              'genres': ['Adventure', 'Biography', 'Comedy'],
              'duration': 143,
              'directors': ['Matthew C. Anderson', 'Nicola Barbour'],
              'actors': ['Isaac Bonillo Alcaina',
               'Gustavo Dettler',
               'Yohanna Farrell-Knight',
               'Luke Heaney'],
              'rating': 1.1}],
    "4": [{'title': 'Toy Story 3',
              'year': 2010,
              'genres': ['Animation', 'Adventure', 'Comedy'],
              'duration': 103,
              'directors': ['Lee Unkrich'],
              'actors': ['Tom Hanks', 'Tim Allen'],
              'rating': 8.3},
             {'title': 'Toy Story',
              'year': 1995,
              'genres': ['Animation', 'Adventure', 'Comedy'],
              'duration': 81,
              'directors': ['John Lasseter'],
              'actors': ['Tom Hanks', 'Tim Allen', 'Don Rickles'],
              'rating': 8.3}],
    "5": [{'title': 'Message from the King',
              'year': 2016,
              'genres': ['Action', 'Crime', 'Drama'],
              'duration': 102,
              'directors': ['Fabrice du Welz'],
              'actors': ['Chadwick Boseman', 'Luke Evans'],
              'rating': 6.4},
             {'title': 'Black Panther',
              'year': 2018,
              'genres': ['Action', 'Adventure', 'Sci-Fi'],
              'duration': 134,
              'directors': ['Ryan Coogler'],
              'actors': ['Chadwick Boseman', 'Michael B. Jordan', "Lupita Nyong'o"],
              'rating': 7.3},
             {'title': 'Get on Up',
              'year': 2014,
              'genres': ['Biography', 'Drama', 'Music'],
              'duration': 139,
              'directors': ['Tate Taylor'],
              'actors': ['Chadwick Boseman', 'Nelsan Ellis', 'Dan Aykroyd'],
              'rating': 6.9},
             {'title': '21 Bridges',
              'year': 2019,
              'genres': ['Action', 'Crime', 'Drama'],
              'duration': 99,
              'directors': ['Brian Kirk'],
              'actors': ['Chadwick Boseman', 'Sienna Miller', 'J.K. Simmons'],
              'rating': 6.6},
             {'title': '42',
              'year': 2013,
              'genres': ['Biography', 'Drama', 'Sport'],
              'duration': 128,
              'directors': ['Brian Helgeland'],
              'actors': ['Chadwick Boseman', 'Harrison Ford'],
              'rating': 7.5},
             {'title': 'Marshall',
              'year': 2017,
              'genres': ['Biography', 'Crime', 'Drama'],
              'duration': 118,
              'directors': ['Reginald Hudlin'],
              'actors': ['Chadwick Boseman', 'Josh Gad', 'Kate Hudson'],
              'rating': 7.2}],
    "6": [{'title': 'The Croods',
              'year': 2013,
              'genres': ['Animation', 'Action', 'Adventure'],
              'duration': 98,
              'directors': ['Kirk DeMicco', 'Chris Sanders'],
              'actors': ['Nicolas Cage', 'Emma Stone'],
              'rating': 7.2},
             {'title': 'Marmaduke',
              'year': 2010,
              'genres': ['Comedy', 'Family'],
              'duration': 99,
              'directors': ['Tom Dey'],
              'actors': ['Owen Wilson',
               'Emma Stone',
               'George Lopez',
               'Christopher Mintz-Plasse'],
              'rating': 4.3},
             {'title': 'The Help',
              'year': 2011,
              'genres': ['Drama'],
              'duration': 146,
              'directors': ['Tate Taylor'],
              'actors': ['Emma Stone', 'Viola Davis', 'Bryce Dallas Howard'],
              'rating': 8.0},
             {'title': 'Easy A',
              'year': 2010,
              'genres': ['Comedy', 'Drama', 'Romance'],
              'duration': 92,
              'directors': ['Will Gluck'],
              'actors': ['Emma Stone', 'Penn Badgley', 'Amanda Bynes', 'Dan Byrd'],
              'rating': 7.0},
             {'title': 'Irrational Man',
              'year': 2015,
              'genres': ['Comedy', 'Drama', 'Romance'],
              'duration': 95,
              'directors': ['Woody Allen'],
              'actors': ['Joaquin Phoenix', 'Emma Stone', 'Joe Stapleton'],
              'rating': 6.6},
             {'title': 'Zombieland: Double Tap',
              'year': 2019,
              'genres': ['Action', 'Adventure', 'Comedy'],
              'duration': 99,
              'directors': ['Ruben Fleischer'],
              'actors': ['Woody Harrelson', 'Jesse Eisenberg', 'Emma Stone'],
              'rating': 6.7},
             {'title': 'The Amazing Spider-Man 2',
              'year': 2014,
              'genres': ['Action', 'Adventure', 'Sci-Fi'],
              'duration': 142,
              'directors': ['Marc Webb'],
              'actors': ['Andrew Garfield', 'Emma Stone', 'Jamie Foxx', 'Dane DeHaan'],
              'rating': 6.6},
             {'title': 'Battle of the Sexes',
              'year': 2017,
              'genres': ['Biography', 'Comedy', 'Drama'],
              'duration': 121,
              'directors': ['Jonathan Dayton', 'Valerie Faris'],
              'actors': ['Emma Stone', 'Steve Carell'],
              'rating': 6.7},
             {'title': 'Zombieland',
              'year': 2009,
              'genres': ['Adventure', 'Comedy', 'Fantasy'],
              'duration': 88,
              'directors': ['Ruben Fleischer'],
              'actors': ['Jesse Eisenberg', 'Woody Harrelson', 'Emma Stone'],
              'rating': 7.6},
             {'title': 'Aloha',
              'year': 2015,
              'genres': ['Comedy', 'Drama', 'Romance'],
              'duration': 105,
              'directors': ['Cameron Crowe'],
              'actors': ['Bradley Cooper', 'Emma Stone', 'Rachel McAdams'],
              'rating': 5.4},
             {'title': 'La La Land',
              'year': 2016,
              'genres': ['Comedy', 'Drama', 'Music'],
              'duration': 128,
              'directors': ['Damien Chazelle'],
              'actors': ['Ryan Gosling', 'Emma Stone'],
              'rating': 8.0},
             {'title': 'The Amazing Spider-Man',
              'year': 2012,
              'genres': ['Action', 'Adventure', 'Sci-Fi'],
              'duration': 136,
              'directors': ['Marc Webb'],
              'actors': ['Andrew Garfield', 'Emma Stone', 'Rhys Ifans'],
              'rating': 6.9},
             {'title': 'Birdman or (The Unexpected Virtue of Ignorance)',
              'year': 2014,
              'genres': ['Comedy', 'Drama'],
              'duration': 119,
              'directors': ['Alejandro G. Iñárritu'],
              'actors': ['Michael Keaton',
               'Emma Stone',
               'Zach Galifianakis',
               'Naomi Watts'],
              'rating': 7.7}],
    "7": {'Action': 5611,
             'Horror': 5175,
             'Sci-Fi': 2148,
             'Crime': 5078,
             'Thriller': 5340,
             'Comedy': 11130,
             'Drama': 16410,
             'Romance': 5753,
             'History': 627,
             'Adventure': 3849,
             'Western': 1177,
             'Family': 1585,
             'Fantasy': 1537,
             'War': 779,
             'Sport': 565,
             'Biography': 1009,
             'Mystery': 2479,
             'Film-Noir': 647,
             'Music': 908,
             'Animation': 676,
             'Musical': 941,
             'Reality-TV': 1,
             'Documentary': 1,
             'News': 1},
    "9": {'1981 to 1990': 2840,
             '2011 to 2020': 8884,
             '2001 to 2010': 6271,
             '1941 to 1950': 2256,
             '1971 to 1980': 1889,
             '1951 to 1960': 2201,
             '1931 to 1940': 2256,
             '1961 to 1970': 1609,
             '1991 to 2000': 4280,
             '1911 to 1920': 120,
             '1921 to 1930': 496},
    "11": {'Action': [{'title': 'The Dark Knight',
               'year': 2008,
               'genres': ['Action', 'Crime', 'Drama'],
               'duration': 152,
               'directors': ['Christopher Nolan'],
               'actors': ['Christian Bale',
                'Heath Ledger',
                'Aaron Eckhart',
                'Michael Caine'],
               'rating': 9.0}],
             'Horror': [{'title': 'Psycho',
               'year': 1960,
               'genres': ['Horror', 'Mystery', 'Thriller'],
               'duration': 109,
               'directors': ['Alfred Hitchcock'],
               'actors': ['Anthony Perkins', 'Vera Miles', 'John Gavin'],
               'rating': 8.5}],
             'Sci-Fi': [{'title': 'Inception',
               'year': 2010,
               'genres': ['Action', 'Adventure', 'Sci-Fi'],
               'duration': 148,
               'directors': ['Christopher Nolan'],
               'actors': ['Leonardo DiCaprio',
                'Joseph Gordon-Levitt',
                'Ellen Page',
                'Tom Hardy'],
               'rating': 8.8}],
             'Crime': [{'title': 'The Godfather',
               'year': 1972,
               'genres': ['Crime', 'Drama'],
               'duration': 175,
               'directors': ['Francis Ford Coppola'],
               'actors': ['Marlon Brando', 'Al Pacino'],
               'rating': 9.2}],
             'Thriller': [{'title': 'The Transcendents',
               'year': 2018,
               'genres': ['Music', 'Mystery', 'Thriller'],
               'duration': 96,
               'directors': ['Derek Ahonen'],
               'actors': ['Rob Franco',
                'Savannah Welch',
                'Kathy Valentine',
                'William Leroy',
                'Derek Ahonen'],
               'rating': 9.2}],
             'Comedy': [{'title': 'The Moving on Phase',
               'year': 2020,
               'genres': ['Comedy'],
               'duration': 85,
               'directors': ['Don Tjernagel'],
               'actors': ['Matt Anderson',
                'Clint Boevers',
                'Jillian Brown',
                'Cody Croskrey',
                'Skott Green'],
               'rating': 9.5}],
             'Drama': [{'title': 'Hopeful Notes',
               'year': 2010,
               'genres': ['Drama'],
               'duration': 94,
               'directors': ['Valerio Zanoli'],
               'actors': ['Walter Nudo', 'Colin Ross', 'Ian Poland'],
               'rating': 9.7}],
             'Romance': [{'title': 'As I Am',
               'year': 2019,
               'genres': ['Drama', 'Fantasy', 'Romance'],
               'duration': 62,
               'directors': ['Anthony Bawn'],
               'actors': ['Andre Myers', 'Jerimiyah Dunbar'],
               'rating': 9.3}],
             'History': [{'title': "Schindler's List",
               'year': 1993,
               'genres': ['Biography', 'Drama', 'History'],
               'duration': 195,
               'directors': ['Steven Spielberg'],
               'actors': ['Liam Neeson',
                'Ben Kingsley',
                'Ralph Fiennes',
                'Caroline Goodall',
                'Jonathan Sagall'],
               'rating': 8.9}],
             'Adventure': [{'title': 'The Lord of the Rings: The Return of the King',
               'year': 2003,
               'genres': ['Action', 'Adventure', 'Drama'],
               'duration': 201,
               'directors': ['Peter Jackson'],
               'actors': ['Sean Astin', 'John Bach', 'Sean Bean', 'Cate Blanchett'],
               'rating': 8.9}],
             'Western': [{'title': "C'era una volta il West",
               'year': 1968,
               'genres': ['Western'],
               'duration': 165,
               'directors': ['Sergio Leone'],
               'actors': ['Claudia Cardinale', 'Henry Fonda', 'Jason Robards'],
               'rating': 8.5}],
             'Family': [{'title': 'All You Can Dream',
               'year': 2012,
               'genres': ['Comedy', 'Drama', 'Family'],
               'duration': 79,
               'directors': ['Valerio Zanoli'],
               'actors': ['Anastacia', 'Hali Mason'],
               'rating': 8.8}],
             'Fantasy': [{'title': 'As I Am',
               'year': 2019,
               'genres': ['Drama', 'Fantasy', 'Romance'],
               'duration': 62,
               'directors': ['Anthony Bawn'],
               'actors': ['Andre Myers', 'Jerimiyah Dunbar'],
               'rating': 9.3}],
             'War': [{'title': 'Saving Private Ryan',
               'year': 1998,
               'genres': ['Drama', 'War'],
               'duration': 169,
               'directors': ['Steven Spielberg'],
               'actors': ['Tom Hanks',
                'Tom Sizemore',
                'Edward Burns',
                'Barry Pepper',
                'Adam Goldberg'],
               'rating': 8.6}],
             'Sport': [{'title': 'The Nomads',
               'year': 2019,
               'genres': ['Drama', 'Sport'],
               'duration': 97,
               'directors': ['Brandon Eric Kamin'],
               'actors': ['Andrea Barnes', 'Erik Blachford', 'Jennifer Butler'],
               'rating': 8.2},
              {'title': 'Raging Bull',
               'year': 1980,
               'genres': ['Biography', 'Drama', 'Sport'],
               'duration': 129,
               'directors': ['Martin Scorsese'],
               'actors': ['Robert De Niro', 'Cathy Moriarty'],
               'rating': 8.2},
              {'title': 'Warrior',
               'year': 2011,
               'genres': ['Action', 'Drama', 'Sport'],
               'duration': 140,
               'directors': ["Gavin O'Connor"],
               'actors': ['Joel Edgerton', 'Tom Hardy', 'Nick Nolte'],
               'rating': 8.2}],
             'Biography': [{'title': "Schindler's List",
               'year': 1993,
               'genres': ['Biography', 'Drama', 'History'],
               'duration': 195,
               'directors': ['Steven Spielberg'],
               'actors': ['Liam Neeson',
                'Ben Kingsley',
                'Ralph Fiennes',
                'Caroline Goodall',
                'Jonathan Sagall'],
               'rating': 8.9}],
             'Mystery': [{'title': 'The Transcendents',
               'year': 2018,
               'genres': ['Music', 'Mystery', 'Thriller'],
               'duration': 96,
               'directors': ['Derek Ahonen'],
               'actors': ['Rob Franco',
                'Savannah Welch',
                'Kathy Valentine',
                'William Leroy',
                'Derek Ahonen'],
               'rating': 9.2}],
             'Film-Noir': [{'title': 'Sunset Blvd.',
               'year': 1950,
               'genres': ['Drama', 'Film-Noir'],
               'duration': 110,
               'directors': ['Billy Wilder'],
               'actors': ['William Holden', 'Gloria Swanson', 'Erich von Stroheim'],
               'rating': 8.4}],
             'Music': [{'title': 'The Transcendents',
               'year': 2018,
               'genres': ['Music', 'Mystery', 'Thriller'],
               'duration': 96,
               'directors': ['Derek Ahonen'],
               'actors': ['Rob Franco',
                'Savannah Welch',
                'Kathy Valentine',
                'William Leroy',
                'Derek Ahonen'],
               'rating': 9.2}],
             'Animation': [{'title': 'Doraleous and Associates',
               'year': 2010,
               'genres': ['Animation'],
               'duration': 100,
               'directors': ['Brent Triplett'],
               'actors': ['Jon Etheridge', 'Bryan Mahoney', 'Nate Panning', 'Tony Schnur'],
               'rating': 8.6}],
             'Musical': [{'title': 'Spies Are Forever',
               'year': 2016,
               'genres': ['Musical'],
               'duration': 159,
               'directors': ['Corey Lubowich'],
               'actors': ['Curt Mega',
                'Mary Kate Wiles',
                'Joey Richter',
                'Brian Rosenthal'],
               'rating': 8.7},
              {'title': "The Guy Who Didn't Like Musicals",
               'year': 2018,
               'genres': ['Comedy', 'Musical'],
               'duration': 112,
               'directors': ['Nick Lang'],
               'actors': ['Jon Matteson', 'Lauren Lopez', 'Joey Richter'],
               'rating': 8.7}],
             'Reality-TV': [{'title': 'Human Zoo',
               'year': 2020,
               'genres': ['Horror', 'Reality-TV', 'Thriller'],
               'duration': 109,
               'directors': ['John E Seymore'],
               'actors': ['Robert Carradine', 'Jose Rosete', 'Rachel Amanda Bryant'],
               'rating': 2.1}],
             'Documentary': [{'title': 'This Is Elvis',
               'year': 1981,
               'genres': ['Documentary', 'Biography', 'Music'],
               'duration': 101,
               'directors': ['Malcolm Leo', 'Andrew Solt'],
               'actors': ['David Scott',
                'Paul Boensch III',
                'Johnny Harra',
                'Larry Raspberry'],
               'rating': 7.5}],
             'News': [{'title': 'A Fighting Season',
               'year': 2015,
               'genres': ['Drama', 'News', 'War'],
               'duration': 82,
               'directors': ['Oden Roberts'],
               'actors': ['Clayne Crawford', 'Lew Temple'],
               'rating': 6.4}]},
    "12": {'Action': 5.5,
             'Horror': 4.6,
             'Sci-Fi': 4.9,
             'Crime': 6.0,
             'Thriller': 5.1,
             'Comedy': 5.9,
             'Drama': 6.1,
             'Romance': 6.2,
             'History': 6.5,
             'Adventure': 6.0,
             'Western': 6.2,
             'Family': 5.9,
             'Fantasy': 5.7,
             'War': 6.4,
             'Sport': 6.1,
             'Biography': 6.7,
             'Mystery': 5.8,
             'Film-Noir': 6.6,
             'Music': 6.2,
             'Animation': 6.4,
             'Musical': 6.2,
             'Reality-TV': 2.1,
             'Documentary': 7.5,
             'News': 6.4},
    "14": [['Documentary'], # DO NOT check this answer by manual lookup. Expected answer is a list of strs. Run test.py to check if your answer is correct.
             ['Biography'],
             ['Film-Noir'],
             ['History'],
             ['War', 'Animation', 'News'],
             ['Romance', 'Western', 'Music', 'Musical'],
             ['Drama', 'Sport'],
             ['Crime', 'Adventure'],
             ['Comedy', 'Family'],
             ['Mystery'],
             ['Fantasy'],
             ['Action'],
             ['Thriller'],
             ['Sci-Fi'],
             ['Horror'],
             ['Reality-TV']],
    "15": [{'title': 'Star Wars',
              'year': 1977,
              'genres': ['Action', 'Adventure', 'Fantasy'],
              'duration': 121,
              'directors': ['George Lucas'],
              'actors': ['Mark Hamill', 'Harrison Ford', 'Carrie Fisher'],
              'rating': 8.6},
             {'title': 'Star Wars: Episode V - The Empire Strikes Back',
              'year': 1980,
              'genres': ['Action', 'Adventure', 'Fantasy'],
              'duration': 124,
              'directors': ['Irvin Kershner'],
              'actors': ['Mark Hamill', 'Harrison Ford'],
              'rating': 8.7},
             {'title': 'Star Wars: Episode VI - Return of the Jedi',
              'year': 1983,
              'genres': ['Action', 'Adventure', 'Fantasy'],
              'duration': 131,
              'directors': ['Richard Marquand'],
              'actors': ['Mark Hamill',
               'Harrison Ford',
               'Carrie Fisher',
               'Billy Dee Williams',
               'Anthony Daniels'],
              'rating': 8.3},
             {'title': 'Star Wars: Episode I - The Phantom Menace',
              'year': 1999,
              'genres': ['Action', 'Adventure', 'Fantasy'],
              'duration': 136,
              'directors': ['George Lucas'],
              'actors': ['Liam Neeson', 'Ewan McGregor', 'Natalie Portman'],
              'rating': 6.5},
             {'title': 'Star Wars: Episode II - Attack of the Clones',
              'year': 2002,
              'genres': ['Action', 'Adventure', 'Fantasy'],
              'duration': 142,
              'directors': ['George Lucas'],
              'actors': ['Ewan McGregor', 'Natalie Portman', 'Hayden Christensen'],
              'rating': 6.5},
             {'title': 'Star Wars: Episode III - Revenge of the Sith',
              'year': 2005,
              'genres': ['Action', 'Adventure', 'Fantasy'],
              'duration': 140,
              'directors': ['George Lucas'],
              'actors': ['Ewan McGregor', 'Natalie Portman', 'Hayden Christensen'],
              'rating': 7.5},
             {'title': 'Star Wars: The Clone Wars',
              'year': 2008,
              'genres': ['Animation', 'Action', 'Adventure'],
              'duration': 98,
              'directors': ['Dave Filoni'],
              'actors': ['Matt Lanter', 'Ashley Eckstein', 'James Arnold Taylor'],
              'rating': 5.9},
             {'title': 'Star Wars: Episode VII - The Force Awakens',
              'year': 2015,
              'genres': ['Action', 'Adventure', 'Sci-Fi'],
              'duration': 138,
              'directors': ['J.J. Abrams'],
              'actors': ['Harrison Ford', 'Mark Hamill', 'Carrie Fisher'],
              'rating': 7.9},
             {'title': 'Star Wars: Episode VIII - The Last Jedi',
              'year': 2017,
              'genres': ['Action', 'Adventure', 'Fantasy'],
              'duration': 152,
              'directors': ['Rian Johnson'],
              'actors': ['Mark Hamill', 'Carrie Fisher', 'Adam Driver', 'Daisy Ridley'],
              'rating': 7.0},
             {'title': 'Solo: A Star Wars Story',
              'year': 2018,
              'genres': ['Action', 'Adventure', 'Sci-Fi'],
              'duration': 135,
              'directors': ['Ron Howard'],
              'actors': ['Alden Ehrenreich', 'Woody Harrelson', 'Emilia Clarke'],
              'rating': 6.9},
             {'title': 'Star Wars: Episode IX - The Rise of Skywalker',
              'year': 2019,
              'genres': ['Action', 'Adventure', 'Fantasy'],
              'duration': 141,
              'directors': ['J.J. Abrams'],
              'actors': ['Carrie Fisher', 'Mark Hamill', 'Adam Driver'],
              'rating': 6.6}],
    "16": [{'title': 'Space Cowboys',
              'year': 2000,
              'genres': ['Action', 'Adventure', 'Thriller'],
              'duration': 130,
              'directors': ['Clint Eastwood'],
              'actors': ['Clint Eastwood',
               'Tommy Lee Jones',
               'Donald Sutherland',
               'James Garner',
               'James Cromwell'],
              'rating': 6.4},
             {'title': 'Heartbreak Ridge',
              'year': 1986,
              'genres': ['Drama', 'War'],
              'duration': 130,
              'directors': ['Clint Eastwood'],
              'actors': ['Clint Eastwood', 'Marsha Mason', 'Everett McGill', 'Moses Gunn'],
              'rating': 6.9},
             {'title': 'Firefox',
              'year': 1982,
              'genres': ['Action', 'Adventure', 'Thriller'],
              'duration': 136,
              'directors': ['Clint Eastwood'],
              'actors': ['Clint Eastwood', 'Freddie Jones', 'David Huffman'],
              'rating': 6.0},
             {'title': 'The Rookie',
              'year': 1990,
              'genres': ['Action', 'Crime', 'Drama'],
              'duration': 120,
              'directors': ['Clint Eastwood'],
              'actors': ['Clint Eastwood', 'Charlie Sheen'],
              'rating': 5.9},
             {'title': 'Pale Rider',
              'year': 1985,
              'genres': ['Drama', 'Western'],
              'duration': 115,
              'directors': ['Clint Eastwood'],
              'actors': ['Clint Eastwood',
               'Michael Moriarty',
               'Carrie Snodgress',
               'Chris Penn',
               'Richard Dysart'],
              'rating': 7.3},
             {'title': 'A Perfect World',
              'year': 1993,
              'genres': ['Crime', 'Drama', 'Thriller'],
              'duration': 138,
              'directors': ['Clint Eastwood'],
              'actors': ['Kevin Costner', 'Clint Eastwood', 'Laura Dern'],
              'rating': 7.6},
             {'title': 'Absolute Power',
              'year': 1997,
              'genres': ['Action', 'Crime', 'Drama'],
              'duration': 121,
              'directors': ['Clint Eastwood'],
              'actors': ['Clint Eastwood', 'Gene Hackman'],
              'rating': 6.7},
             {'title': 'The Gauntlet',
              'year': 1977,
              'genres': ['Action', 'Crime', 'Thriller'],
              'duration': 109,
              'directors': ['Clint Eastwood'],
              'actors': ['Clint Eastwood', 'Sondra Locke', 'Pat Hingle', 'William Prince'],
              'rating': 6.4},
             {'title': 'White Hunter Black Heart',
              'year': 1990,
              'genres': ['Adventure', 'Drama'],
              'duration': 112,
              'directors': ['Clint Eastwood'],
              'actors': ['Clint Eastwood', 'Jeff Fahey', 'Charlotte Cornwell'],
              'rating': 6.6},
             {'title': 'Gran Torino',
              'year': 2008,
              'genres': ['Drama'],
              'duration': 116,
              'directors': ['Clint Eastwood'],
              'actors': ['Clint Eastwood', 'Christopher Carley', 'Bee Vang'],
              'rating': 8.1},
             {'title': 'Play Misty for Me',
              'year': 1971,
              'genres': ['Drama', 'Thriller'],
              'duration': 102,
              'directors': ['Clint Eastwood'],
              'actors': ['Clint Eastwood', 'Jessica Walter', 'Donna Mills', 'John Larch'],
              'rating': 7.0},
             {'title': 'The Eiger Sanction',
              'year': 1975,
              'genres': ['Action', 'Crime', 'Thriller'],
              'duration': 129,
              'directors': ['Clint Eastwood'],
              'actors': ['Clint Eastwood', 'George Kennedy', 'Vonetta McGee'],
              'rating': 6.4},
             {'title': 'The Mule',
              'year': 2018,
              'genres': ['Crime', 'Drama', 'Thriller'],
              'duration': 116,
              'directors': ['Clint Eastwood'],
              'actors': ['Clint Eastwood', 'Patrick L. Reyes', 'Cesar De León'],
              'rating': 7.0},
             {'title': 'The Bridges of Madison County',
              'year': 1995,
              'genres': ['Drama', 'Romance'],
              'duration': 135,
              'directors': ['Clint Eastwood'],
              'actors': ['Clint Eastwood', 'Meryl Streep', 'Annie Corley'],
              'rating': 7.6},
             {'title': 'Honkytonk Man',
              'year': 1982,
              'genres': ['Comedy', 'Drama', 'Music'],
              'duration': 122,
              'directors': ['Clint Eastwood'],
              'actors': ['Clint Eastwood',
               'Kyle Eastwood',
               'John McIntire',
               'Alexa Kenin'],
              'rating': 6.6},
             {'title': 'High Plains Drifter',
              'year': 1973,
              'genres': ['Drama', 'Mystery', 'Western'],
              'duration': 105,
              'directors': ['Clint Eastwood'],
              'actors': ['Clint Eastwood', 'Verna Bloom', 'Marianna Hill'],
              'rating': 7.5},
             {'title': 'True Crime',
              'year': 1999,
              'genres': ['Crime', 'Drama', 'Mystery'],
              'duration': 127,
              'directors': ['Clint Eastwood'],
              'actors': ['Clint Eastwood', 'Isaiah Washington', 'LisaGay Hamilton'],
              'rating': 6.6},
             {'title': 'Sudden Impact',
              'year': 1983,
              'genres': ['Action', 'Crime', 'Thriller'],
              'duration': 117,
              'directors': ['Clint Eastwood'],
              'actors': ['Clint Eastwood',
               'Sondra Locke',
               'Pat Hingle',
               'Bradford Dillman',
               'Jack Thibeau'],
              'rating': 6.7},
             {'title': 'Bronco Billy',
              'year': 1980,
              'genres': ['Action', 'Adventure', 'Comedy'],
              'duration': 116,
              'directors': ['Clint Eastwood'],
              'actors': ['Clint Eastwood', 'Sondra Locke', 'Geoffrey Lewis'],
              'rating': 6.1},
             {'title': 'The Outlaw Josey Wales',
              'year': 1976,
              'genres': ['Western'],
              'duration': 135,
              'directors': ['Clint Eastwood'],
              'actors': ['Clint Eastwood', 'Chief Dan George'],
              'rating': 7.8},
             {'title': 'Blood Work',
              'year': 2002,
              'genres': ['Action', 'Crime', 'Drama'],
              'duration': 110,
              'directors': ['Clint Eastwood'],
              'actors': ['Clint Eastwood', 'Jeff Daniels', 'Anjelica Huston'],
              'rating': 6.4},
             {'title': 'Unforgiven',
              'year': 1992,
              'genres': ['Drama', 'Western'],
              'duration': 130,
              'directors': ['Clint Eastwood'],
              'actors': ['Clint Eastwood', 'Gene Hackman', 'Morgan Freeman'],
              'rating': 8.2},
             {'title': 'Million Dollar Baby',
              'year': 2004,
              'genres': ['Drama', 'Sport'],
              'duration': 132,
              'directors': ['Clint Eastwood'],
              'actors': ['Clint Eastwood', 'Hilary Swank', 'Morgan Freeman'],
              'rating': 8.1}],
    "17": [['Play Misty for Me'],
             ['High Plains Drifter'],
             ['The Gauntlet'],
             ['Blood Work'],
             ['White Hunter Black Heart'],
             ['Pale Rider'],
             ['Gran Torino', 'The Mule', 'Bronco Billy'],
             ['Sudden Impact'],
             ['The Rookie'],
             ['Absolute Power'],
             ['Honkytonk Man'],
             ['True Crime'],
             ['The Eiger Sanction'],
             ['Space Cowboys', 'Heartbreak Ridge', 'Unforgiven'],
             ['Million Dollar Baby'],
             ['The Bridges of Madison County', 'The Outlaw Josey Wales'],
             ['Firefox'],
             ['A Perfect World']],
    "18": [['Welcome to Collinwood'],
             ['You, Me and Dupree'],
             ['Captain America: The Winter Soldier'],
             ['Captain America: Civil War'],
             ['Avengers: Infinity War'],
             ['Avengers: Endgame']],
    "19": [['Hibakusha'],
             ['King Candy'],
             ['Amy Winehouse: Fallen Star'],
             ['Steve Jobs: Visionary Genius'],
             ['The Road to Hollywood'],
             ['Danny Greene: The Rise and Fall of the Irishman',
              'From the Manger to the Cross; or, Jesus of Nazareth',
              'Joseph Smith: Prophet of the Restoration',
              'The Trade'],
             ['Blondes at Work'],
             ['Spirit of Youth'],
             ['The Loves of Edgar Allan Poe'],
             ['Alexander Hamilton', 'Dillinger', 'Memoria']],
    "20": [['Audrey Hepburn'],
             ['Leonardo DiCaprio'],
             ['Woody Allen', 'Ryan Gosling'],
             ['Harold Lloyd'],
             ['Brad Pitt', 'Philip Seymour Hoffman', 'Ralph Fiennes', 'Laurence Olivier'],
             ['Groucho Marx',
              'Humphrey Bogart',
              'Amy Adams',
              'Jake Gyllenhaal',
              'Judy Garland',
              'Bette Davis',
              'Albert Brooks',
              'Bill Murray',
              'Russell Crowe',
              'Christian Bale',
              'Buster Keaton',
              'Tom Cruise'],
             ['Fred Astaire', 'Chris Cooper', 'Matt Damon', 'Donald Crisp']]
}


# find a comment something like this: #q10
def extract_question_num(cell):
    for line in cell.get('source', []):
        line = line.strip().replace(' ', '').lower()
        m = re.match(r'\#q(\d+)', line)
        if m:
            return int(m.group(1))
    return None


# find correct python command based on version
def get_python_cmd():
    cmds = ['py', 'python3', 'python']
    for cmd in cmds:
        try:
            out = subprocess.check_output(cmd + ' -V', shell=True, universal_newlines=True)
            m = re.match(r'Python\s+(\d+\.\d+)\.*\d*', out)
            if m:
                if float(m.group(1)) >= 3.6:
                    return cmd
        except subprocess.CalledProcessError:
            pass
    else:
        return ''


# rerun notebook and return parsed JSON
def rerun_notebook(orig_notebook):
    new_notebook = 'cs-220-test.ipynb'

    # re-execute it from the beginning
    py_cmd = get_python_cmd()
    cmd = 'jupyter nbconvert --execute "{orig}" --to notebook --output="{new}" --ExecutePreprocessor.timeout=120'
    cmd = cmd.format(orig=os.path.abspath(orig_notebook), new=os.path.abspath(new_notebook))
    if py_cmd:
        # cmd = py_cmd + ' -m ' + cmd
        pass
    subprocess.check_output(cmd, shell=True)

    # parse notebook
    with open(new_notebook, encoding='utf-8') as f:
        nb = json.load(f)
    return nb


def normalize_json(orig):
    try:
        return json.dumps(json.loads(orig.strip("'")), indent=2, sort_keys=True)
    except:
        return 'not JSON'


def check_cell_text(qnum, cell, format):
    outputs = cell.get('outputs', [])
    if len(outputs) == 0:
        return 'no outputs in an Out[N] cell'
    actual_lines = None
    for out in outputs:
        lines = out.get('data', {}).get('text/plain', [])
        if lines:
            actual_lines = lines
            break
    if actual_lines == None:
        return 'no Out[N] output found for cell (note: printing the output does not work)'
    actual = ''.join(actual_lines)
    try:
        actual = ast.literal_eval(actual)
    except ValueError:
        pass
    expected = expected_json[str(qnum)]

    try:
        if format == TEXT_FORMAT:
            return simple_compare(expected, actual)
        elif format == TEXT_FORMAT_ORDERED_LIST:
            return list_compare_ordered(expected, actual)
        elif format == TEXT_FORMAT_UNORDERED_LIST:
            return list_compare_unordered(expected, actual)
        elif format == TEXT_FORMAT_SPECIAL_ORDERED_LIST:
            return list_compare_special(expected, actual)
        elif format == TEXT_FORMAT_DICT:
            return dict_compare(expected, actual)
        elif format == TEXT_FORMAT_LIST_DICTS_ORDERED:
            return list_compare_ordered(expected, actual)
        else:
            if expected != actual:
                return "found %s but expected %s" % (repr(actual), repr(expected))
    except:
        if expected != actual:
            return "expected %s" % (repr(expected))
    return PASS


def simple_compare(expected, actual, complete_msg=True):
    msg = PASS
    if type(expected) != type(actual) and not (type(expected) in [float, int] and type(actual) in [float, int]):
        msg = "expected to find type %s but found type %s" % (type(expected).__name__, type(actual).__name__)
    elif type(expected) == float:
        if not math.isclose(actual, expected, rel_tol=REL_TOL, abs_tol=ABS_TOL):
            msg = "expected %s" % (repr(expected))
            if complete_msg:
                msg = msg + " but found %s" % (repr(actual))
    else:
        if expected != actual:
            msg = "expected %s" % (repr(expected))
            if complete_msg:
                msg = msg + " but found %s" % (repr(actual))
    return msg


def list_compare_ordered(expected, actual, obj="list"):
    msg = PASS
    if type(expected) != type(actual):
        msg = "expected to find type %s but found type %s" % (type(expected).__name__, type(actual).__name__)
        return msg
    for i in range(len(expected)):
        if i >= len(actual):
            msg = "expected missing %s in %s" % (repr(expected[i]), obj)
            break
        if type(expected[i]) in [int, float, bool, str]:
            val = simple_compare(expected[i], actual[i])
        elif type(expected[i]) in [list]:
            val = list_compare_ordered(expected[i], actual[i], "sub" + obj)
        elif type(expected[i]) in [dict]:
            val = dict_compare(expected[i], actual[i])
        if val != PASS:
            msg = "at index %d of the %s, " % (i, obj) + val
            break
    if len(actual) > len(expected) and msg == PASS:
        msg = "found unexpected %s in %s" % (repr(actual[len(expected)]), obj)
    if len(expected) != len(actual):
        msg = msg + " (found %d entries in %s, but expected %d)" % (len(actual), obj, len(expected))

    if len(expected) > 0 and type(expected[0]) in [int, float, bool, str]:
        if msg != PASS and list_compare_unordered(expected, actual, obj) == PASS:
            try:
                msg = msg + " (list may not be ordered as required)"
            except:
                pass
    return msg


def list_compare_helper(larger, smaller):
    msg = PASS
    j = 0
    for i in range(len(larger)):
        if i == len(smaller):
            msg = "expected %s" % (repr(larger[i]))
            break
        found = False
        while not found:
            if j == len(smaller):
                val = simple_compare(larger[i], smaller[j - 1], False)
                break
            val = simple_compare(larger[i], smaller[j], False)
            j += 1
            if val == PASS:
                found = True
                break
        if not found:
            msg = val
            break
    return msg


def list_compare_unordered(expected, actual, obj="list"):
    msg = PASS
    if type(expected) != type(actual):
        msg = "expected to find type %s but found type %s" % (type(expected).__name__, type(actual).__name__)
        return msg
    try:
        sort_expected = sorted(expected)
        sort_actual = sorted(actual)
    except:
        msg = "unexpected datatype found in list; expect a list of entries of type %s" % (type(expected[0]).__name__)
        return msg

    if len(actual) == 0 and len(expected) > 0:
        msg = "in the %s, missing" % (obj) + expected[0]
    elif len(actual) > 0 and len(expected) > 0:
        val = simple_compare(sort_expected[0], sort_actual[0])
        if val.startswith("expected to find type"):
            msg = "in the %s, " % (obj) + simple_compare(sort_expected[0], sort_actual[0])
        else:
            if len(expected) > len(actual):
                msg = "in the %s, missing " % (obj) + list_compare_helper(sort_expected, sort_actual)
            elif len(expected) < len(actual):
                msg = "in the %s, found un" % (obj) + list_compare_helper(sort_actual, sort_expected)
            if len(expected) != len(actual):
                msg = msg + " (found %d entries in %s, but expected %d)" % (len(actual), obj, len(expected))
                return msg
            else:
                val = list_compare_helper(sort_expected, sort_actual)
                if val != PASS:
                    msg = "in the %s, missing " % (obj) + val + ", but found un" + list_compare_helper(sort_actual,
                                                                                               sort_expected)
    return msg


def list_compare_special(expected, actual):
    msg = PASS
    expected_list = []
    for expected_item in expected:
        expected_list.extend(expected_item)
    val = list_compare_unordered(expected_list, actual)
    if val != PASS:
        msg = val
    else:
        i = 0
        for expected_item in expected:
            j = len(expected_item)
            actual_item = actual[i: i + j]
            val = list_compare_unordered(expected_item, actual_item)
            if val != PASS:
                if j == 1:
                    msg = "at index %d " % (i) + val
                else:
                    msg = "between indices %d and %d " % (i, i + j - 1) + val
                msg = msg + " (list may not be ordered as required)"
                break
            i += j

    return msg


def dict_compare(expected, actual, obj="dict"):
    msg = PASS
    if type(expected) != type(actual):
        msg = "expected to find type %s but found type %s" % (type(expected).__name__, type(actual).__name__)
        return msg
    try:
        expected_keys = sorted(list(expected.keys()))
        actual_keys = sorted(list(actual.keys()))
    except:
        msg = "unexpected datatype found in keys of dict; expect a dict with keys of type %s" % (
            type(expected_keys[0]).__name__)
        return msg
    val = list_compare_unordered(expected_keys, actual_keys, "dict")
    if val != PASS:
        msg = "bad keys in %s: " % (obj) + val
    if msg == PASS:
        for key in expected:
            if expected[key] == None or type(expected[key]) in [int, float, bool, str]:
                val = simple_compare(expected[key], actual[key])
            elif type(expected[key]) in [list]:
                val = list_compare_ordered(expected[key], actual[key], "value")
            elif type(expected[key]) in [dict]:
                val = dict_compare(expected[key], actual[key], "sub" + obj)
            if val != PASS:
                msg = "incorrect val for key %s in %s: " % (repr(key), obj) + val
    return msg


def check_cell_png(qnum, cell):
    for output in cell.get('outputs', []):
        if 'image/png' in output.get('data', {}):
            return PASS
    return 'no plot found'


def check_cell(question, cell):
    print('Checking question %d' % question.number)
    if question.format.split()[0] == TEXT_FORMAT:
        return check_cell_text(question.number, cell, question.format)
    elif question.format == PNG_FORMAT:
        return check_cell_png(question.number, cell)
    raise Exception("invalid question type")


def grade_answers(cells):
    results = {'score': 0, 'tests': []}

    for question in questions:
        cell = cells.get(question.number, None)
        status = "not found"

        if question.number in cells:
            status = check_cell(question, cells[question.number])

        row = {"test": question.number, "result": status, "weight": question.weight}
        results['tests'].append(row)

    return results


def linter_severe_check(nb):
    issues = []
    func_names = set()
    for cell in nb['cells']:
        if cell['cell_type'] != 'code':
            continue
        code = "\n".join(cell.get('source', []))
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    name = node.name
                    if name in func_names:
                        issues.append('name <%s> reused for multiple functions' % name)
                    func_names.add(name)
        except Exception as e:
            print('Linter error: ' + str(e))

    return issues


def main():
    if (sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith("win")):
        import asyncio
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # rerun everything
    orig_notebook = 'main.ipynb'
    if len(sys.argv) > 2:
        print("Usage: test.py main.ipynb")
        return
    elif len(sys.argv) == 2:
        orig_notebook = sys.argv[1]
    if not os.path.exists(orig_notebook):
        print("File not found: " + orig_notebook)
        print(
            "\nIf your file is named something other than main.ipynb, you can specify that by replacing '<notebook.ipynb>' with the name you chose:\n")
        print("python test.py <notebook.ipynb>")
        sys.exit(1)

    nb = rerun_notebook(orig_notebook)

    if LINTER:
        # check for sever linter errors
        issues = linter_severe_check(nb)
        if issues:
            print("\nPlease fix the following, then rerun the tests:")
            for issue in issues:
                print(' - ' + issue)
            print("")
            sys.exit(1)

    # extract qnums with png expected answer
    png_expected = [q.number for q in questions if q.format == PNG_FORMAT]

    # extract cells that have answers
    answer_cells = {}
    for cell in nb['cells']:
        q = extract_question_num(cell)
        if q == None:
            continue
        if not q in question_nums:
            print('no question %d' % q)
            continue
        answer_cells[q] = cell

    # do grading on extracted answers and produce results.json
    results = grade_answers(answer_cells)
    passing = sum(t['weight'] for t in results['tests'] if t['result'] == PASS)
    total = sum(t['weight'] for t in results['tests'])
    results['score'] = 100.0 * passing / total
    png_passed = [t['test'] for t in results['tests'] if t['result'] == PASS and t['test'] in png_expected]

    print("\nSummary:")
    for test in results["tests"]:
        print("  Test %d: %s" % (test["test"], test["result"]))

    print('\nTOTAL SCORE: %.2f%%' % results['score'])

    if len(png_passed) > 0:
        print("\nWARNING: ", end="")
        if len(png_passed) == 1:
            print("Q%d is not checked by test.py." % (png_passed[0]))
        else:
            for n in png_passed[:-1]:
                print("Q%d" % n, end=", ")
            print("and Q%d are not checked by test.py." % (png_passed[-1]))
        print(
            "Please refer to the corresponding reference png files given in the documentation.\n")

    with open('result.json', 'w') as f:
        f.write(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
