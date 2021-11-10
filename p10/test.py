import ast, os, sys, subprocess, json, re, collections, math, warnings, time

# check the python version
if sys.version[:5] < '3.7.0':
    warnings.warn('Your current python version is {}. Please upgrade your python version to at least 3.7.0.'.format(sys.version[:5]))

################################################################################
REL_TOL = 6e-04  # relative tolerance for floats
ABS_TOL = 15e-03  # absolute tolerance for floats
TIME = 60 # number of seconds before timer times out
LINTER = False  # set to False if linter should be turned off for project
################################################################################

PASS = "PASS"
TEXT_FORMAT = "text" # use when expected answer is a str, int, float, or bool
TEXT_FORMAT_DICT = "text dict" # use when the expected answer is a dictionary
TEXT_FORMAT_UNORDERED_LIST = "text unordered_list" # use when the expected answer is a list where the order does *not* matter
TEXT_FORMAT_ORDERED_LIST = "text ordered_list" # use when the expected answer is a list where the order does matter
TEXT_FORMAT_LIST_DICTS_ORDERED = "text list_dicts_ordered" # use when the expected answer is a list of dicts where the order does matter

obfuscate1 = "Tweet"
obfuscate2 = ['tweet_id', 'username', 'num_liked', 'length']
Tweet = collections.namedtuple(obfuscate1, obfuscate2)
Question = collections.namedtuple("Question", ["number", "weight", "format"])

questions = [
    Question(number=1, weight=1, format=TEXT_FORMAT),
    Question(number=2, weight=1, format=TEXT_FORMAT),
    Question(number=3, weight=1, format=TEXT_FORMAT_UNORDERED_LIST),
    Question(number=4, weight=1, format=TEXT_FORMAT_UNORDERED_LIST),
    Question(number=5, weight=1, format=TEXT_FORMAT_UNORDERED_LIST),
    Question(number=6, weight=1, format=TEXT_FORMAT_UNORDERED_LIST),
    Question(number=7, weight=1, format=TEXT_FORMAT_UNORDERED_LIST),
    Question(number=8, weight=1, format=TEXT_FORMAT_UNORDERED_LIST),
    Question(number=9, weight=1, format=TEXT_FORMAT_UNORDERED_LIST),
    Question(number=10, weight=1, format=TEXT_FORMAT_UNORDERED_LIST),
    Question(number=11, weight=1, format=TEXT_FORMAT_UNORDERED_LIST),
    Question(number=12, weight=1, format=TEXT_FORMAT_UNORDERED_LIST),
    Question(number=13, weight=1, format=TEXT_FORMAT_UNORDERED_LIST),
    Question(number=14, weight=1, format=TEXT_FORMAT_UNORDERED_LIST),
    Question(number=15, weight=1, format=TEXT_FORMAT_UNORDERED_LIST),
    Question(number=16, weight=1, format=TEXT_FORMAT_UNORDERED_LIST),
    Question(number=17, weight=1, format=TEXT_FORMAT_UNORDERED_LIST),
    Question(number=18, weight=1, format=TEXT_FORMAT_UNORDERED_LIST),
    Question(number=19, weight=1, format=TEXT_FORMAT_UNORDERED_LIST),
    Question(number=20, weight=1, format=TEXT_FORMAT_ORDERED_LIST),
]
question_nums = set([q.number for q in questions])

# JSON and plaintext values
expected_json = {
    "1": 4,
    "2": 10,
    "3": [os.path.join('sample_data','1.csv'),
                 os.path.join('sample_data','1.json'),
                 os.path.join('sample_data','2.csv'),
                 os.path.join('sample_data','2.json')],
    "4": [os.path.join('full_data','1.csv'),
             os.path.join('full_data','1.json'),
             os.path.join('full_data','2.csv'),
             os.path.join('full_data','2.json'),
             os.path.join('full_data','3.csv'),
             os.path.join('full_data','3.json'),
             os.path.join('full_data','4.csv'),
             os.path.join('full_data','4.json'),
             os.path.join('full_data','5.csv'),
             os.path.join('full_data','5.json')],
    "5": [os.path.join('sample_data','1.csv'),
                 os.path.join('sample_data','2.csv')],
    "6": [os.path.join('full_data','1.json'),
             os.path.join('full_data','2.json'),
             os.path.join('full_data','3.json'),
             os.path.join('full_data','4.json'),
             os.path.join('full_data','5.json')],
    "7": [Tweet(tweet_id='1467812799', username='USERID_7', num_liked=3340, length=103),
 Tweet(tweet_id='1467812964', username='USERID_10', num_liked=3684, length=93),
 Tweet(tweet_id='1467813137', username='USERID_5', num_liked=6816, length=20),
 Tweet(tweet_id='1467813579', username='USERID_1', num_liked=1348, length=64),
 Tweet(tweet_id='1467813782', username='USERID_1', num_liked=4770, length=79)],
    "8": [Tweet(tweet_id='1467901250', username='USERID_6', num_liked=7790, length=132),
 Tweet(tweet_id='1467901346', username='USERID_1', num_liked=5079, length=137),
 Tweet(tweet_id='1467901437', username='USERID_6', num_liked=5913, length=60),
 Tweet(tweet_id='1467901500', username='USERID_7', num_liked=7376, length=13),
 Tweet(tweet_id='1467901839', username='USERID_7', num_liked=4871, length=101),
 Tweet(tweet_id='1467904302', username='USERID_8', num_liked=1195, length=91),
 Tweet(tweet_id='1467905125', username='USERID_7', num_liked=1738, length=27),
 Tweet(tweet_id='1467905378', username='USERID_2', num_liked=4420, length=111),
 Tweet(tweet_id='1467905653', username='USERID_10', num_liked=8845, length=82),
 Tweet(tweet_id='1467906151', username='USERID_8', num_liked=6711, length=45),
 Tweet(tweet_id='1467906345', username='USERID_3', num_liked=8279, length=46),
 Tweet(tweet_id='1467906723', username='USERID_6', num_liked=7222, length=28),
 Tweet(tweet_id='1467907298', username='USERID_8', num_liked=9005, length=61),
 Tweet(tweet_id='1467907751', username='USERID_2', num_liked=9048, length=110),
 Tweet(tweet_id='1467907876', username='USERID_7', num_liked=1347, length=87),
 Tweet(tweet_id='1467908012', username='USERID_1', num_liked=1809, length=50),
 Tweet(tweet_id='1467908134', username='USERID_7', num_liked=8983, length=66),
 Tweet(tweet_id='1467908456', username='USERID_5', num_liked=2265, length=138),
 Tweet(tweet_id='1467908672', username='USERID_10', num_liked=1692, length=48),
 Tweet(tweet_id='1467908798', username='USERID_2', num_liked=1659, length=51),
 Tweet(tweet_id='1467909124', username='USERID_4', num_liked=9406, length=118),
 Tweet(tweet_id='1467909222', username='USERID_5', num_liked=8887, length=136),
 Tweet(tweet_id='1467909292', username='USERID_10', num_liked=5179, length=45),
 Tweet(tweet_id='1467910531', username='USERID_7', num_liked=6172, length=34),
 Tweet(tweet_id='1467910689', username='USERID_3', num_liked=1529, length=37),
 Tweet(tweet_id='1467910932', username='USERID_8', num_liked=1507, length=68),
 Tweet(tweet_id='1467910986', username='USERID_6', num_liked=836, length=66),
 Tweet(tweet_id='1467910995', username='USERID_4', num_liked=2886, length=57),
 Tweet(tweet_id='1467911036', username='USERID_7', num_liked=6950, length=101),
 Tweet(tweet_id='1467911302', username='USERID_10', num_liked=8562, length=119),
 Tweet(tweet_id='1467911624', username='USERID_5', num_liked=5668, length=77),
 Tweet(tweet_id='1467911846', username='USERID_3', num_liked=1352, length=67),
 Tweet(tweet_id='1467912100', username='USERID_6', num_liked=3394, length=94),
 Tweet(tweet_id='1467912333', username='USERID_7', num_liked=3345, length=49),
 Tweet(tweet_id='1467912572', username='USERID_3', num_liked=36, length=80),
 Tweet(tweet_id='1467912842', username='USERID_4', num_liked=496, length=14),
 Tweet(tweet_id='1467912994', username='USERID_8', num_liked=926, length=57),
 Tweet(tweet_id='1467913111', username='USERID_7', num_liked=5185, length=144),
 Tweet(tweet_id='1467913608', username='USERID_8', num_liked=8262, length=111),
 Tweet(tweet_id='1467914434', username='USERID_1', num_liked=1269, length=49),
 Tweet(tweet_id='1467914499', username='USERID_2', num_liked=910, length=138),
 Tweet(tweet_id='1467914916', username='USERID_4', num_liked=3232, length=91),
 Tweet(tweet_id='1467915140', username='USERID_7', num_liked=1996, length=22),
 Tweet(tweet_id='1467915612', username='USERID_6', num_liked=4014, length=41),
 Tweet(tweet_id='1467915670', username='USERID_2', num_liked=5287, length=138),
 Tweet(tweet_id='1467916510', username='USERID_8', num_liked=8150, length=96),
 Tweet(tweet_id='1467916595', username='USERID_6', num_liked=1178, length=138),
 Tweet(tweet_id='1467916695', username='USERID_10', num_liked=6691, length=54),
 Tweet(tweet_id='1467916700', username='USERID_9', num_liked=2519, length=136),
 Tweet(tweet_id='1467916820', username='USERID_10', num_liked=8557, length=127)],
    "9": [Tweet(tweet_id='1467876711', username='USERID_10', num_liked=1117, length=84),
           Tweet(tweet_id='1467877496', username='USERID_1', num_liked=2062, length=106),
           Tweet(tweet_id='1467877833', username='USERID_2', num_liked=4270, length=89),
           Tweet(tweet_id='1467877865', username='USERID_1', num_liked=5899, length=30),
           Tweet(tweet_id='1467878057', username='USERID_6', num_liked=703, length=42),
           Tweet(tweet_id='1467878557', username='USERID_6', num_liked=5814, length=61),
           Tweet(tweet_id='1467878633', username='USERID_2', num_liked=2351, length=33),
           Tweet(tweet_id='1467878971', username='USERID_2', num_liked=2238, length=27),
           Tweet(tweet_id='1467878983', username='USERID_8', num_liked=4860, length=61),
           Tweet(tweet_id='1467879480', username='USERID_4', num_liked=1345, length=97),
           Tweet(tweet_id='1467879984', username='USERID_2', num_liked=3694, length=69),
           Tweet(tweet_id='1467880085', username='USERID_4', num_liked=2478, length=120),
           Tweet(tweet_id='1467880431', username='USERID_3', num_liked=9407, length=85),
           Tweet(tweet_id='1467880442', username='USERID_2', num_liked=5125, length=96),
           Tweet(tweet_id='1467880463', username='USERID_9', num_liked=1226, length=29),
           Tweet(tweet_id='1467880692', username='USERID_6', num_liked=4989, length=49),
           Tweet(tweet_id='1467881131', username='USERID_10', num_liked=732, length=107),
           Tweet(tweet_id='1467881373', username='USERID_6', num_liked=8615, length=145),
           Tweet(tweet_id='1467881376', username='USERID_4', num_liked=4378, length=49),
           Tweet(tweet_id='1467881457', username='USERID_7', num_liked=119, length=27),
           Tweet(tweet_id='1467881686', username='USERID_5', num_liked=8136, length=46),
           Tweet(tweet_id='1467881809', username='USERID_4', num_liked=1797, length=138),
           Tweet(tweet_id='1467881897', username='USERID_5', num_liked=2314, length=76),
           Tweet(tweet_id='1467881920', username='USERID_3', num_liked=4101, length=112),
           Tweet(tweet_id='1467882140', username='USERID_8', num_liked=5320, length=137),
           Tweet(tweet_id='1467882491', username='USERID_10', num_liked=3512, length=55),
           Tweet(tweet_id='1467882592', username='USERID_10', num_liked=1887, length=67),
           Tweet(tweet_id='1467882902', username='USERID_3', num_liked=4646, length=48),
           Tweet(tweet_id='1467888679', username='USERID_8', num_liked=3089, length=27),
           Tweet(tweet_id='1467888732', username='USERID_7', num_liked=2800, length=48),
           Tweet(tweet_id='1467888953', username='USERID_3', num_liked=3951, length=46),
           Tweet(tweet_id='1467889231', username='USERID_5', num_liked=1320, length=79),
           Tweet(tweet_id='1467889334', username='USERID_5', num_liked=8495, length=42),
           Tweet(tweet_id='1467889574', username='USERID_1', num_liked=4696, length=123),
           Tweet(tweet_id='1467889791', username='USERID_5', num_liked=4027, length=132),
           Tweet(tweet_id='1467889988', username='USERID_2', num_liked=7394, length=51),
           Tweet(tweet_id='1467890079', username='USERID_8', num_liked=2556, length=38),
           Tweet(tweet_id='1467890222', username='USERID_2', num_liked=227, length=107),
           Tweet(tweet_id='1467890723', username='USERID_1', num_liked=96, length=134),
           Tweet(tweet_id='1467891826', username='USERID_9', num_liked=2021, length=113),
           Tweet(tweet_id='1467891880', username='USERID_7', num_liked=6847, length=96),
           Tweet(tweet_id='1467892075', username='USERID_6', num_liked=2816, length=124),
           Tweet(tweet_id='1467892515', username='USERID_5', num_liked=917, length=39),
           Tweet(tweet_id='1467892667', username='USERID_2', num_liked=8270, length=20),
           Tweet(tweet_id='1467892720', username='USERID_3', num_liked=3227, length=128)],
    "10": [Tweet(tweet_id='1467810369', username='USERID_4', num_liked=315, length=115),
        Tweet(tweet_id='1467810672', username='USERID_8', num_liked=5298, length=111),
        Tweet(tweet_id='1467810917', username='USERID_8', num_liked=533, length=89),
        Tweet(tweet_id='1467811184', username='USERID_6', num_liked=2650, length=47),
        Tweet(tweet_id='1467811193', username='USERID_8', num_liked=2101, length=111)],
    "11":[Tweet(tweet_id='1467812416', username='USERID_9', num_liked=5278, length=43),
 Tweet(tweet_id='1467812579', username='USERID_1', num_liked=9700, length=26),
 Tweet(tweet_id='1467812723', username='USERID_3', num_liked=5414, length=94),
 Tweet(tweet_id='1467812771', username='USERID_8', num_liked=2190, length=77),
 Tweet(tweet_id='1467812784', username='USERID_10', num_liked=2667, length=117)] ,
    "12":[Tweet(tweet_id='1467892760', username='USERID_6', num_liked=4443, length=56),
 Tweet(tweet_id='1467892889', username='USERID_1', num_liked=7439, length=91),
 Tweet(tweet_id='1467892945', username='USERID_4', num_liked=8101, length=43),
 Tweet(tweet_id='1467893163', username='USERID_3', num_liked=6754, length=74),
 Tweet(tweet_id='1467893258', username='USERID_7', num_liked=1415, length=74),
 Tweet(tweet_id='1467893275', username='USERID_6', num_liked=9002, length=70),
 Tweet(tweet_id='1467893504', username='USERID_9', num_liked=4940, length=25),
 Tweet(tweet_id='1467893730', username='USERID_4', num_liked=840, length=90),
 Tweet(tweet_id='1467894593', username='USERID_2', num_liked=869000000, length=136),
 Tweet(tweet_id='1467894600', username='USERID_8', num_liked=915000, length=67),
 Tweet(tweet_id='1467894746', username='USERID_4', num_liked=3185, length=107),
 Tweet(tweet_id='1467894749', username='USERID_5', num_liked=6311, length=40),
 Tweet(tweet_id='1467894750', username='USERID_6', num_liked=1046, length=46),
 Tweet(tweet_id='1467894786', username='USERID_7', num_liked=4709, length=136),
 Tweet(tweet_id='1467894841', username='USERID_8', num_liked=803, length=102),
 Tweet(tweet_id='1467894898', username='USERID_7', num_liked=2692, length=76),
 Tweet(tweet_id='1467895048', username='USERID_10', num_liked=9822, length=136),
 Tweet(tweet_id='1467895109', username='USERID_7', num_liked=3255, length=133),
 Tweet(tweet_id='1467895424', username='USERID_10', num_liked=3423, length=41),
 Tweet(tweet_id='1467895478', username='USERID_8', num_liked=926, length=67),
 Tweet(tweet_id='1467895481', username='USERID_5', num_liked=6120, length=49),
 Tweet(tweet_id='1467895712', username='USERID_8', num_liked=8551, length=136),
 Tweet(tweet_id='1467896211', username='USERID_6', num_liked=3966, length=31),
 Tweet(tweet_id='1467896253', username='USERID_2', num_liked=4906, length=91),
 Tweet(tweet_id='1467896463', username='USERID_9', num_liked=1728, length=136),
 Tweet(tweet_id='1467896777', username='USERID_10', num_liked=0, length=92),
 Tweet(tweet_id='1467896778', username='USERID_4', num_liked=886, length=97),
 Tweet(tweet_id='1467896898', username='USERID_7', num_liked=2972, length=58),
 Tweet(tweet_id='1467896911', username='USERID_9', num_liked=5160, length=136),
 Tweet(tweet_id='1467896996', username='USERID_10', num_liked=6540, length=61),
 Tweet(tweet_id='1467897316', username='USERID_2', num_liked=7890, length=64),
 Tweet(tweet_id='1467897981', username='USERID_9', num_liked=3034, length=136),
 Tweet(tweet_id='1467898061', username='USERID_8', num_liked=9271, length=145),
 Tweet(tweet_id='1467898076', username='USERID_7', num_liked=5075, length=136),
 Tweet(tweet_id='1467898078', username='USERID_10', num_liked=9705, length=104),
 Tweet(tweet_id='1467898511', username='USERID_2', num_liked=3477, length=99),
 Tweet(tweet_id='1467898676', username='USERID_9', num_liked=6766, length=58),
 Tweet(tweet_id='1467899025', username='USERID_6', num_liked=4660, length=137),
 Tweet(tweet_id='1467899451', username='USERID_1', num_liked=1861, length=138),
 Tweet(tweet_id='1467899605', username='USERID_9', num_liked=3209, length=90),
 Tweet(tweet_id='1467899707', username='USERID_6', num_liked=1941, length=123),
 Tweet(tweet_id='1467899753', username='USERID_10', num_liked=675, length=32),
 Tweet(tweet_id='1467900033', username='USERID_10', num_liked=9041, length=36),
 Tweet(tweet_id='1467900037', username='USERID_8', num_liked=6640, length=70),
 Tweet(tweet_id='1467900244', username='USERID_10', num_liked=1618, length=45),
 Tweet(tweet_id='1467900431', username='USERID_9', num_liked=3306, length=34),
 Tweet(tweet_id='1467900545', username='USERID_7', num_liked=148, length=13),
 Tweet(tweet_id='1467900898', username='USERID_1', num_liked=1149, length=131),
 Tweet(tweet_id='1467901135', username='USERID_4', num_liked=5825, length=94),
 Tweet(tweet_id='1467901188', username='USERID_1', num_liked=8852, length=138)],
    "13": [],
    "14": [Tweet(tweet_id='1467934004', username='USERID_1', num_liked=6170, length=150),
 Tweet(tweet_id='1467929915', username='USERID_5', num_liked=4550, length=146),
 Tweet(tweet_id='1467898061', username='USERID_8', num_liked=9271, length=145),
 Tweet(tweet_id='1467881373', username='USERID_6', num_liked=8615, length=145),
 Tweet(tweet_id='1467913111', username='USERID_7', num_liked=5185, length=144),
 Tweet(tweet_id='1467863684', username='USERID_1', num_liked=3108, length=142)],
    "15":[Tweet(tweet_id='1467810369', username='USERID_4', num_liked=315, length=115),
 Tweet(tweet_id='1467810672', username='USERID_8', num_liked=5298, length=111),
 Tweet(tweet_id='1467811193', username='USERID_8', num_liked=2101, length=111),
 Tweet(tweet_id='1467812799', username='USERID_7', num_liked=3340, length=103),
 Tweet(tweet_id='1467812784', username='USERID_10', num_liked=2667, length=117)],
    "16": [Tweet(tweet_id='1467953163', username='USERID_1', num_liked=2254, length=105),
 Tweet(tweet_id='1467953277', username='USERID_2', num_liked=494, length=31),
 Tweet(tweet_id='1467953367', username='USERID_6', num_liked=552, length=40),
 Tweet(tweet_id='1467953500', username='USERID_1', num_liked=9035, length=67),
 Tweet(tweet_id='1467953681', username='USERID_7', num_liked=6149, length=75),
 Tweet(tweet_id='1467953733', username='USERID_4', num_liked=9526, length=67),
 Tweet(tweet_id='1467953738', username='USERID_1', num_liked=1544, length=46),
 Tweet(tweet_id='1467954059', username='USERID_1', num_liked=3935, length=63),
 Tweet(tweet_id='1467954070', username='USERID_8', num_liked=9462, length=64),
 Tweet(tweet_id='1467959908', username='USERID_1', num_liked=2241, length=8),
 Tweet(tweet_id='1467960066', username='USERID_8', num_liked=8350, length=28),
 Tweet(tweet_id='1467960388', username='USERID_4', num_liked=964, length=132),
 Tweet(tweet_id='1467960481', username='USERID_1', num_liked=4440, length=106),
 Tweet(tweet_id='1467960735', username='USERID_7', num_liked=8682, length=87),
 Tweet(tweet_id='1467960840', username='USERID_6', num_liked=3367, length=54),
 Tweet(tweet_id='1467961044', username='USERID_5', num_liked=3582, length=75),
 Tweet(tweet_id='1467961091', username='USERID_10', num_liked=9184, length=38),
 Tweet(tweet_id='1467961106', username='USERID_2', num_liked=7552, length=65),
 Tweet(tweet_id='1467961146', username='USERID_6', num_liked=5316, length=120),
 Tweet(tweet_id='1467961817', username='USERID_4', num_liked=3179, length=27),
 Tweet(tweet_id='1467962336', username='USERID_9', num_liked=5680, length=128),
 Tweet(tweet_id='1467962502', username='USERID_5', num_liked=7788, length=32),
 Tweet(tweet_id='1467962634', username='USERID_7', num_liked=7725, length=74),
 Tweet(tweet_id='1467962671', username='USERID_5', num_liked=3448, length=67),
 Tweet(tweet_id='1467962897', username='USERID_2', num_liked=4898, length=98),
 Tweet(tweet_id='1467962938', username='USERID_3', num_liked=8703, length=42),
 Tweet(tweet_id='1467963418', username='USERID_1', num_liked=4274, length=84),
 Tweet(tweet_id='1467963477', username='USERID_6', num_liked=5004, length=47),
 Tweet(tweet_id='1467963715', username='USERID_9', num_liked=8006, length=70),
 Tweet(tweet_id='1467963880', username='USERID_10', num_liked=5313, length=71),
 Tweet(tweet_id='1467964211', username='USERID_4', num_liked=9618, length=79),
 Tweet(tweet_id='1467964229', username='USERID_7', num_liked=6978, length=100),
 Tweet(tweet_id='1467965065', username='USERID_10', num_liked=6004, length=62),
 Tweet(tweet_id='1467965832', username='USERID_1', num_liked=8678, length=129),
 Tweet(tweet_id='1467965873', username='USERID_7', num_liked=2352, length=128),
 Tweet(tweet_id='1467965949', username='USERID_9', num_liked=8308, length=29),
 Tweet(tweet_id='1467965994', username='USERID_8', num_liked=5985, length=88),
 Tweet(tweet_id='1467966187', username='USERID_7', num_liked=7995, length=39),
 Tweet(tweet_id='1467966260', username='USERID_4', num_liked=6040, length=25),
 Tweet(tweet_id='1467966271', username='USERID_1', num_liked=4664, length=38),
 Tweet(tweet_id='1467966560', username='USERID_5', num_liked=767, length=43),
 Tweet(tweet_id='1467966646', username='USERID_7', num_liked=9821, length=47),
 Tweet(tweet_id='1467967089', username='USERID_6', num_liked=7597, length=19),
 Tweet(tweet_id='1467967410', username='USERID_6', num_liked=99, length=73),
 Tweet(tweet_id='1467967432', username='USERID_1', num_liked=4072, length=53),
 Tweet(tweet_id='1467967862', username='USERID_7', num_liked=8710, length=60),
 Tweet(tweet_id='1467968140', username='USERID_7', num_liked=3903, length=123),
 Tweet(tweet_id='1467968155', username='USERID_6', num_liked=4072, length=74),
 Tweet(tweet_id='1467968402', username='USERID_8', num_liked=4272, length=53),
 Tweet(tweet_id='1467968584', username='USERID_2', num_liked=777, length=132),
 Tweet(tweet_id='1467930083', username='USERID_6', num_liked=6650, length=48),
 Tweet(tweet_id='1467930157', username='USERID_7', num_liked=7410, length=138),
 Tweet(tweet_id='1467930220', username='USERID_2', num_liked=4770, length=94),
 Tweet(tweet_id='1467930309', username='USERID_9', num_liked=4910, length=51),
 Tweet(tweet_id='1467930341', username='USERID_10', num_liked=1990, length=79),
 Tweet(tweet_id='1467931027', username='USERID_5', num_liked=1699, length=26),
 Tweet(tweet_id='1467931070', username='USERID_8', num_liked=910, length=135),
 Tweet(tweet_id='1467931396', username='USERID_9', num_liked=2496, length=96),
 Tweet(tweet_id='1467931501', username='USERID_5', num_liked=5807, length=117),
 Tweet(tweet_id='1467931736', username='USERID_6', num_liked=2449, length=91),
 Tweet(tweet_id='1467931839', username='USERID_6', num_liked=1915, length=73),
 Tweet(tweet_id='1467931983', username='USERID_7', num_liked=9292, length=106),
 Tweet(tweet_id='1467932117', username='USERID_5', num_liked=9188, length=50),
 Tweet(tweet_id='1467932208', username='USERID_7', num_liked=9169, length=84),
 Tweet(tweet_id='1467932372', username='USERID_7', num_liked=9065, length=56),
 Tweet(tweet_id='1467932549', username='USERID_6', num_liked=6966, length=53),
 Tweet(tweet_id='1467932979', username='USERID_1', num_liked=6333, length=52),
 Tweet(tweet_id='1467933048', username='USERID_5', num_liked=3184, length=69),
 Tweet(tweet_id='1467933102', username='USERID_2', num_liked=625, length=135),
 Tweet(tweet_id='1467933112', username='USERID_9', num_liked=3523, length=52),
 Tweet(tweet_id='1467933295', username='USERID_1', num_liked=6234, length=14),
 Tweet(tweet_id='1467933494', username='USERID_10', num_liked=6958, length=85),
 Tweet(tweet_id='1467933623', username='USERID_3', num_liked=2239, length=73),
 Tweet(tweet_id='1467933662', username='USERID_5', num_liked=5510, length=39),
 Tweet(tweet_id='1467933685', username='USERID_6', num_liked=8653, length=39),
 Tweet(tweet_id='1467934004', username='USERID_1', num_liked=6170, length=150),
 Tweet(tweet_id='1467934184', username='USERID_9', num_liked=8463, length=31),
 Tweet(tweet_id='1467934481', username='USERID_5', num_liked=7982, length=59),
 Tweet(tweet_id='1467934606', username='USERID_10', num_liked=7842, length=31),
 Tweet(tweet_id='1467935121', username='USERID_2', num_liked=8740, length=37),
 Tweet(tweet_id='1467935189', username='USERID_10', num_liked=4191, length=56),
 Tweet(tweet_id='1467935271', username='USERID_5', num_liked=6982, length=129),
 Tweet(tweet_id='1467935345', username='USERID_9', num_liked=2980, length=45),
 Tweet(tweet_id='1467936498', username='USERID_5', num_liked=313, length=16),
 Tweet(tweet_id='1467936541', username='USERID_5', num_liked=2821, length=47),
 Tweet(tweet_id='1467936901', username='USERID_5', num_liked=9181, length=24),
 Tweet(tweet_id='1467937038', username='USERID_3', num_liked=5684, length=21),
 Tweet(tweet_id='1467937128', username='USERID_8', num_liked=9343, length=125),
 Tweet(tweet_id='1467937189', username='USERID_7', num_liked=3442, length=108),
 Tweet(tweet_id='1467937250', username='USERID_3', num_liked=4415, length=15),
 Tweet(tweet_id='1467937393', username='USERID_10', num_liked=9361, length=129),
 Tweet(tweet_id='1467942658', username='USERID_7', num_liked=615, length=59),
 Tweet(tweet_id='1467943007', username='USERID_2', num_liked=9000, length=130),
 Tweet(tweet_id='1467943375', username='USERID_3', num_liked=3647, length=59),
 Tweet(tweet_id='1467943526', username='USERID_6', num_liked=7674, length=68),
 Tweet(tweet_id='1467943851', username='USERID_6', num_liked=1658, length=42),
 Tweet(tweet_id='1467943966', username='USERID_10', num_liked=6623, length=68),
 Tweet(tweet_id='1467944261', username='USERID_1', num_liked=7023, length=40),
 Tweet(tweet_id='1467944317', username='USERID_3', num_liked=7476, length=54),
 Tweet(tweet_id='1467944552', username='USERID_8', num_liked=6151, length=132),
 Tweet(tweet_id='1467844540', username='USERID_9', num_liked=6366, length=49),
 Tweet(tweet_id='1467844907', username='USERID_3', num_liked=8770, length=42),
 Tweet(tweet_id='1467845095', username='USERID_4', num_liked=8567, length=126),
 Tweet(tweet_id='1467845157', username='USERID_8', num_liked=5761, length=17),
 Tweet(tweet_id='1467852031', username='USERID_2', num_liked=4565, length=63),
 Tweet(tweet_id='1467852067', username='USERID_4', num_liked=9594, length=34),
 Tweet(tweet_id='1467852789', username='USERID_10', num_liked=686, length=44),
 Tweet(tweet_id='1467853135', username='USERID_1', num_liked=6515, length=131),
 Tweet(tweet_id='1467853356', username='USERID_10', num_liked=3192, length=136),
 Tweet(tweet_id='1467853431', username='USERID_10', num_liked=9936, length=30),
 Tweet(tweet_id='1467853479', username='USERID_9', num_liked=4939, length=24),
 Tweet(tweet_id='1467854062', username='USERID_10', num_liked=9346, length=92),
 Tweet(tweet_id='1467854345', username='USERID_9', num_liked=7959, length=72),
 Tweet(tweet_id='1467854706', username='USERID_1', num_liked=8972, length=103),
 Tweet(tweet_id='1467854917', username='USERID_2', num_liked=7741, length=30),
 Tweet(tweet_id='1467855673', username='USERID_9', num_liked=9728, length=72),
 Tweet(tweet_id='1467855812', username='USERID_2', num_liked=4806, length=28),
 Tweet(tweet_id='1467855981', username='USERID_2', num_liked=6455, length=92),
 Tweet(tweet_id='1467856044', username='USERID_7', num_liked=1442, length=49),
 Tweet(tweet_id='1467856352', username='USERID_3', num_liked=523, length=20),
 Tweet(tweet_id='1467856426', username='USERID_6', num_liked=8675, length=99),
 Tweet(tweet_id='1467856497', username='USERID_7', num_liked=3105, length=79),
 Tweet(tweet_id='1467856632', username='USERID_1', num_liked=1724, length=43),
 Tweet(tweet_id='1467856821', username='USERID_6', num_liked=5145, length=80),
 Tweet(tweet_id='1467856919', username='USERID_4', num_liked=3887, length=61),
 Tweet(tweet_id='1467857221', username='USERID_5', num_liked=3589, length=102),
 Tweet(tweet_id='1467857297', username='USERID_1', num_liked=736, length=70),
 Tweet(tweet_id='1467857378', username='USERID_4', num_liked=9459, length=81),
 Tweet(tweet_id='1467857511', username='USERID_7', num_liked=3713, length=127),
 Tweet(tweet_id='1467857722', username='USERID_8', num_liked=9072, length=55),
 Tweet(tweet_id='1467857975', username='USERID_9', num_liked=4893, length=21),
 Tweet(tweet_id='1467858363', username='USERID_10', num_liked=4263, length=119),
 Tweet(tweet_id='1467858627', username='USERID_3', num_liked=8400, length=120),
 Tweet(tweet_id='1467858869', username='USERID_10', num_liked=1609, length=48),
 Tweet(tweet_id='1467859025', username='USERID_4', num_liked=5618, length=81),
 Tweet(tweet_id='1467859066', username='USERID_9', num_liked=99, length=53),
 Tweet(tweet_id='1467859408', username='USERID_5', num_liked=2878, length=128),
 Tweet(tweet_id='1467859436', username='USERID_7', num_liked=8001, length=67),
 Tweet(tweet_id='1467859558', username='USERID_1', num_liked=8732, length=136),
 Tweet(tweet_id='1467859666', username='USERID_9', num_liked=9158, length=16),
 Tweet(tweet_id='1467859820', username='USERID_10', num_liked=7921, length=27),
 Tweet(tweet_id='1467859922', username='USERID_6', num_liked=3955, length=120),
 Tweet(tweet_id='1467860895', username='USERID_1', num_liked=2055, length=18),
 Tweet(tweet_id='1467860904', username='USERID_7', num_liked=9851, length=30),
 Tweet(tweet_id='1467861095', username='USERID_10', num_liked=7191, length=38),
 Tweet(tweet_id='1467861522', username='USERID_1', num_liked=2742, length=70),
 Tweet(tweet_id='1467861571', username='USERID_1', num_liked=7095, length=84),
 Tweet(tweet_id='1467862213', username='USERID_2', num_liked=2455, length=138),
 Tweet(tweet_id='1467862313', username='USERID_10', num_liked=3256, length=127),
 Tweet(tweet_id='1467862355', username='USERID_3', num_liked=4110, length=53),
 Tweet(tweet_id='1467916851', username='USERID_3', num_liked=559, length=58),
 Tweet(tweet_id='1467916959', username='USERID_2', num_liked=7081, length=69),
 Tweet(tweet_id='1467917177', username='USERID_3', num_liked=9678, length=105),
 Tweet(tweet_id='1467917302', username='USERID_5', num_liked=1624, length=35),
 Tweet(tweet_id='1467917484', username='USERID_1', num_liked=4679, length=94),
 Tweet(tweet_id='1467917499', username='USERID_4', num_liked=2851, length=51),
 Tweet(tweet_id='1467917718', username='USERID_1', num_liked=1344, length=84),
 Tweet(tweet_id='1467917800', username='USERID_6', num_liked=7810, length=55),
 Tweet(tweet_id='1467918015', username='USERID_2', num_liked=1508, length=97),
 Tweet(tweet_id='1467918552', username='USERID_3', num_liked=8973, length=44),
 Tweet(tweet_id='1467918560', username='USERID_6', num_liked=6796, length=131),
 Tweet(tweet_id='1467918682', username='USERID_2', num_liked=8884, length=102),
 Tweet(tweet_id='1467918728', username='USERID_6', num_liked=903, length=58),
 Tweet(tweet_id='1467918812', username='USERID_3', num_liked=2835, length=99),
 Tweet(tweet_id='1467918850', username='USERID_2', num_liked=5383, length=103),
 Tweet(tweet_id='1467919055', username='USERID_2', num_liked=5370, length=68),
 Tweet(tweet_id='1467919452', username='USERID_5', num_liked=2839, length=10),
 Tweet(tweet_id='1467919538', username='USERID_10', num_liked=406, length=83),
 Tweet(tweet_id='1467919762', username='USERID_5', num_liked=4035, length=139),
 Tweet(tweet_id='1467919765', username='USERID_7', num_liked=5237, length=124),
 Tweet(tweet_id='1467922983', username='USERID_3', num_liked=8024, length=94),
 Tweet(tweet_id='1467923235', username='USERID_9', num_liked=9662, length=134),
 Tweet(tweet_id='1467923247', username='USERID_1', num_liked=1211, length=44),
 Tweet(tweet_id='1467923370', username='USERID_5', num_liked=2601, length=117),
 Tweet(tweet_id='1467923445', username='USERID_4', num_liked=3462, length=52),
 Tweet(tweet_id='1467923775', username='USERID_9', num_liked=4869, length=33),
 Tweet(tweet_id='1467924273', username='USERID_3', num_liked=825, length=35),
 Tweet(tweet_id='1467924690', username='USERID_9', num_liked=2250, length=41),
 Tweet(tweet_id='1467924823', username='USERID_6', num_liked=7229, length=59),
 Tweet(tweet_id='1467925327', username='USERID_9', num_liked=8401, length=99),
 Tweet(tweet_id='1467925657', username='USERID_5', num_liked=7082, length=69),
 Tweet(tweet_id='1467926153', username='USERID_5', num_liked=2376, length=56),
 Tweet(tweet_id='1467926444', username='USERID_2', num_liked=1394, length=61),
 Tweet(tweet_id='1467926632', username='USERID_2', num_liked=2602, length=98),
 Tweet(tweet_id='1467927016', username='USERID_6', num_liked=48, length=87),
 Tweet(tweet_id='1467927126', username='USERID_5', num_liked=468, length=126),
 Tweet(tweet_id='1467927987', username='USERID_3', num_liked=4156, length=39),
 Tweet(tweet_id='1467928014', username='USERID_7', num_liked=9830, length=18),
 Tweet(tweet_id='1467928037', username='USERID_3', num_liked=4319, length=138),
 Tweet(tweet_id='1467928300', username='USERID_9', num_liked=9681, length=79),
 Tweet(tweet_id='1467928490', username='USERID_7', num_liked=1065, length=57),
 Tweet(tweet_id='1467928676', username='USERID_10', num_liked=9187, length=84),
 Tweet(tweet_id='1467928749', username='USERID_10', num_liked=7504, length=99),
 Tweet(tweet_id='1467928764', username='USERID_2', num_liked=9026, length=41),
 Tweet(tweet_id='1467929184', username='USERID_4', num_liked=1977, length=21),
 Tweet(tweet_id='1467929230', username='USERID_6', num_liked=3724, length=47),
 Tweet(tweet_id='1467929248', username='USERID_7', num_liked=4986, length=66),
 Tweet(tweet_id='1467929601', username='USERID_9', num_liked=366, length=99),
 Tweet(tweet_id='1467929915', username='USERID_5', num_liked=4550, length=146),
 Tweet(tweet_id='1467930017', username='USERID_7', num_liked=2627, length=14),
 Tweet(tweet_id='1467892760', username='USERID_6', num_liked=4443, length=56),
 Tweet(tweet_id='1467892889', username='USERID_1', num_liked=7439, length=91),
 Tweet(tweet_id='1467892945', username='USERID_4', num_liked=8101, length=43),
 Tweet(tweet_id='1467893163', username='USERID_3', num_liked=6754, length=74),
 Tweet(tweet_id='1467893258', username='USERID_7', num_liked=1415, length=74),
 Tweet(tweet_id='1467893275', username='USERID_6', num_liked=9002, length=70),
 Tweet(tweet_id='1467893504', username='USERID_9', num_liked=4940, length=25),
 Tweet(tweet_id='1467893730', username='USERID_4', num_liked=840, length=90),
 Tweet(tweet_id='1467894593', username='USERID_2', num_liked=869000000, length=136),
 Tweet(tweet_id='1467894600', username='USERID_8', num_liked=915000, length=67),
 Tweet(tweet_id='1467894746', username='USERID_4', num_liked=3185, length=107),
 Tweet(tweet_id='1467894749', username='USERID_5', num_liked=6311, length=40),
 Tweet(tweet_id='1467894750', username='USERID_6', num_liked=1046, length=46),
 Tweet(tweet_id='1467894786', username='USERID_7', num_liked=4709, length=136),
 Tweet(tweet_id='1467894841', username='USERID_8', num_liked=803, length=102),
 Tweet(tweet_id='1467894898', username='USERID_7', num_liked=2692, length=76),
 Tweet(tweet_id='1467895048', username='USERID_10', num_liked=9822, length=136),
 Tweet(tweet_id='1467895109', username='USERID_7', num_liked=3255, length=133),
 Tweet(tweet_id='1467895424', username='USERID_10', num_liked=3423, length=41),
 Tweet(tweet_id='1467895478', username='USERID_8', num_liked=926, length=67),
 Tweet(tweet_id='1467895481', username='USERID_5', num_liked=6120, length=49),
 Tweet(tweet_id='1467895712', username='USERID_8', num_liked=8551, length=136),
 Tweet(tweet_id='1467896211', username='USERID_6', num_liked=3966, length=31),
 Tweet(tweet_id='1467896253', username='USERID_2', num_liked=4906, length=91),
 Tweet(tweet_id='1467896463', username='USERID_9', num_liked=1728, length=136),
 Tweet(tweet_id='1467896777', username='USERID_10', num_liked=0, length=92),
 Tweet(tweet_id='1467896778', username='USERID_4', num_liked=886, length=97),
 Tweet(tweet_id='1467896898', username='USERID_7', num_liked=2972, length=58),
 Tweet(tweet_id='1467896911', username='USERID_9', num_liked=5160, length=136),
 Tweet(tweet_id='1467896996', username='USERID_10', num_liked=6540, length=61),
 Tweet(tweet_id='1467897316', username='USERID_2', num_liked=7890, length=64),
 Tweet(tweet_id='1467897981', username='USERID_9', num_liked=3034, length=136),
 Tweet(tweet_id='1467898061', username='USERID_8', num_liked=9271, length=145),
 Tweet(tweet_id='1467898076', username='USERID_7', num_liked=5075, length=136),
 Tweet(tweet_id='1467898078', username='USERID_10', num_liked=9705, length=104),
 Tweet(tweet_id='1467898511', username='USERID_2', num_liked=3477, length=99),
 Tweet(tweet_id='1467898676', username='USERID_9', num_liked=6766, length=58),
 Tweet(tweet_id='1467899025', username='USERID_6', num_liked=4660, length=137),
 Tweet(tweet_id='1467899451', username='USERID_1', num_liked=1861, length=138),
 Tweet(tweet_id='1467899605', username='USERID_9', num_liked=3209, length=90),
 Tweet(tweet_id='1467899707', username='USERID_6', num_liked=1941, length=123),
 Tweet(tweet_id='1467899753', username='USERID_10', num_liked=675, length=32),
 Tweet(tweet_id='1467900033', username='USERID_10', num_liked=9041, length=36),
 Tweet(tweet_id='1467900037', username='USERID_8', num_liked=6640, length=70),
 Tweet(tweet_id='1467900244', username='USERID_10', num_liked=1618, length=45),
 Tweet(tweet_id='1467900431', username='USERID_9', num_liked=3306, length=34),
 Tweet(tweet_id='1467900545', username='USERID_7', num_liked=148, length=13),
 Tweet(tweet_id='1467900898', username='USERID_1', num_liked=1149, length=131),
 Tweet(tweet_id='1467901135', username='USERID_4', num_liked=5825, length=94),
 Tweet(tweet_id='1467901188', username='USERID_1', num_liked=8852, length=138),
 Tweet(tweet_id='1467876711', username='USERID_10', num_liked=1117, length=84),
 Tweet(tweet_id='1467877496', username='USERID_1', num_liked=2062, length=106),
 Tweet(tweet_id='1467877833', username='USERID_2', num_liked=4270, length=89),
 Tweet(tweet_id='1467877865', username='USERID_1', num_liked=5899, length=30),
 Tweet(tweet_id='1467878057', username='USERID_6', num_liked=703, length=42),
 Tweet(tweet_id='1467878557', username='USERID_6', num_liked=5814, length=61),
 Tweet(tweet_id='1467878633', username='USERID_2', num_liked=2351, length=33),
 Tweet(tweet_id='1467878971', username='USERID_2', num_liked=2238, length=27),
 Tweet(tweet_id='1467878983', username='USERID_8', num_liked=4860, length=61),
 Tweet(tweet_id='1467879480', username='USERID_4', num_liked=1345, length=97),
 Tweet(tweet_id='1467879984', username='USERID_2', num_liked=3694, length=69),
 Tweet(tweet_id='1467880085', username='USERID_4', num_liked=2478, length=120),
 Tweet(tweet_id='1467880431', username='USERID_3', num_liked=9407, length=85),
 Tweet(tweet_id='1467880442', username='USERID_2', num_liked=5125, length=96),
 Tweet(tweet_id='1467880463', username='USERID_9', num_liked=1226, length=29),
 Tweet(tweet_id='1467880692', username='USERID_6', num_liked=4989, length=49),
 Tweet(tweet_id='1467881131', username='USERID_10', num_liked=732, length=107),
 Tweet(tweet_id='1467881373', username='USERID_6', num_liked=8615, length=145),
 Tweet(tweet_id='1467881376', username='USERID_4', num_liked=4378, length=49),
 Tweet(tweet_id='1467881457', username='USERID_7', num_liked=119, length=27),
 Tweet(tweet_id='1467881686', username='USERID_5', num_liked=8136, length=46),
 Tweet(tweet_id='1467881809', username='USERID_4', num_liked=1797, length=138),
 Tweet(tweet_id='1467881897', username='USERID_5', num_liked=2314, length=76),
 Tweet(tweet_id='1467881920', username='USERID_3', num_liked=4101, length=112),
 Tweet(tweet_id='1467882140', username='USERID_8', num_liked=5320, length=137),
 Tweet(tweet_id='1467882491', username='USERID_10', num_liked=3512, length=55),
 Tweet(tweet_id='1467882592', username='USERID_10', num_liked=1887, length=67),
 Tweet(tweet_id='1467882902', username='USERID_3', num_liked=4646, length=48),
 Tweet(tweet_id='1467888679', username='USERID_8', num_liked=3089, length=27),
 Tweet(tweet_id='1467888732', username='USERID_7', num_liked=2800, length=48),
 Tweet(tweet_id='1467888953', username='USERID_3', num_liked=3951, length=46),
 Tweet(tweet_id='1467889231', username='USERID_5', num_liked=1320, length=79),
 Tweet(tweet_id='1467889334', username='USERID_5', num_liked=8495, length=42),
 Tweet(tweet_id='1467889574', username='USERID_1', num_liked=4696, length=123),
 Tweet(tweet_id='1467889791', username='USERID_5', num_liked=4027, length=132),
 Tweet(tweet_id='1467889988', username='USERID_2', num_liked=7394, length=51),
 Tweet(tweet_id='1467890079', username='USERID_8', num_liked=2556, length=38),
 Tweet(tweet_id='1467890222', username='USERID_2', num_liked=227, length=107),
 Tweet(tweet_id='1467890723', username='USERID_1', num_liked=96, length=134),
 Tweet(tweet_id='1467891826', username='USERID_9', num_liked=2021, length=113),
 Tweet(tweet_id='1467891880', username='USERID_7', num_liked=6847, length=96),
 Tweet(tweet_id='1467892075', username='USERID_6', num_liked=2816, length=124),
 Tweet(tweet_id='1467892515', username='USERID_5', num_liked=917, length=39),
 Tweet(tweet_id='1467892667', username='USERID_2', num_liked=8270, length=20),
 Tweet(tweet_id='1467892720', username='USERID_3', num_liked=3227, length=128),
 Tweet(tweet_id='1467901250', username='USERID_6', num_liked=7790, length=132),
 Tweet(tweet_id='1467901346', username='USERID_1', num_liked=5079, length=137),
 Tweet(tweet_id='1467901437', username='USERID_6', num_liked=5913, length=60),
 Tweet(tweet_id='1467901500', username='USERID_7', num_liked=7376, length=13),
 Tweet(tweet_id='1467901839', username='USERID_7', num_liked=4871, length=101),
 Tweet(tweet_id='1467904302', username='USERID_8', num_liked=1195, length=91),
 Tweet(tweet_id='1467905125', username='USERID_7', num_liked=1738, length=27),
 Tweet(tweet_id='1467905378', username='USERID_2', num_liked=4420, length=111),
 Tweet(tweet_id='1467905653', username='USERID_10', num_liked=8845, length=82),
 Tweet(tweet_id='1467906151', username='USERID_8', num_liked=6711, length=45),
 Tweet(tweet_id='1467906345', username='USERID_3', num_liked=8279, length=46),
 Tweet(tweet_id='1467906723', username='USERID_6', num_liked=7222, length=28),
 Tweet(tweet_id='1467907298', username='USERID_8', num_liked=9005, length=61),
 Tweet(tweet_id='1467907751', username='USERID_2', num_liked=9048, length=110),
 Tweet(tweet_id='1467907876', username='USERID_7', num_liked=1347, length=87),
 Tweet(tweet_id='1467908012', username='USERID_1', num_liked=1809, length=50),
 Tweet(tweet_id='1467908134', username='USERID_7', num_liked=8983, length=66),
 Tweet(tweet_id='1467908456', username='USERID_5', num_liked=2265, length=138),
 Tweet(tweet_id='1467908672', username='USERID_10', num_liked=1692, length=48),
 Tweet(tweet_id='1467908798', username='USERID_2', num_liked=1659, length=51),
 Tweet(tweet_id='1467909124', username='USERID_4', num_liked=9406, length=118),
 Tweet(tweet_id='1467909222', username='USERID_5', num_liked=8887, length=136),
 Tweet(tweet_id='1467909292', username='USERID_10', num_liked=5179, length=45),
 Tweet(tweet_id='1467910531', username='USERID_7', num_liked=6172, length=34),
 Tweet(tweet_id='1467910689', username='USERID_3', num_liked=1529, length=37),
 Tweet(tweet_id='1467910932', username='USERID_8', num_liked=1507, length=68),
 Tweet(tweet_id='1467910986', username='USERID_6', num_liked=836, length=66),
 Tweet(tweet_id='1467910995', username='USERID_4', num_liked=2886, length=57),
 Tweet(tweet_id='1467911036', username='USERID_7', num_liked=6950, length=101),
 Tweet(tweet_id='1467911302', username='USERID_10', num_liked=8562, length=119),
 Tweet(tweet_id='1467911624', username='USERID_5', num_liked=5668, length=77),
 Tweet(tweet_id='1467911846', username='USERID_3', num_liked=1352, length=67),
 Tweet(tweet_id='1467912100', username='USERID_6', num_liked=3394, length=94),
 Tweet(tweet_id='1467912333', username='USERID_7', num_liked=3345, length=49),
 Tweet(tweet_id='1467912572', username='USERID_3', num_liked=36, length=80),
 Tweet(tweet_id='1467912842', username='USERID_4', num_liked=496, length=14),
 Tweet(tweet_id='1467912994', username='USERID_8', num_liked=926, length=57),
 Tweet(tweet_id='1467913111', username='USERID_7', num_liked=5185, length=144),
 Tweet(tweet_id='1467913608', username='USERID_8', num_liked=8262, length=111),
 Tweet(tweet_id='1467914434', username='USERID_1', num_liked=1269, length=49),
 Tweet(tweet_id='1467914499', username='USERID_2', num_liked=910, length=138),
 Tweet(tweet_id='1467914916', username='USERID_4', num_liked=3232, length=91),
 Tweet(tweet_id='1467915140', username='USERID_7', num_liked=1996, length=22),
 Tweet(tweet_id='1467915612', username='USERID_6', num_liked=4014, length=41),
 Tweet(tweet_id='1467915670', username='USERID_2', num_liked=5287, length=138),
 Tweet(tweet_id='1467916510', username='USERID_8', num_liked=8150, length=96),
 Tweet(tweet_id='1467916595', username='USERID_6', num_liked=1178, length=138),
 Tweet(tweet_id='1467916695', username='USERID_10', num_liked=6691, length=54),
 Tweet(tweet_id='1467916700', username='USERID_9', num_liked=2519, length=136),
 Tweet(tweet_id='1467916820', username='USERID_10', num_liked=8557, length=127),
 Tweet(tweet_id='1467862411', username='USERID_10', num_liked=5740, length=34),
 Tweet(tweet_id='1467862710', username='USERID_1', num_liked=4540, length=100),
 Tweet(tweet_id='1467862806', username='USERID_2', num_liked=9465, length=68),
 Tweet(tweet_id='1467863072', username='USERID_5', num_liked=2574, length=10),
 Tweet(tweet_id='1467863415', username='USERID_7', num_liked=7576, length=79),
 Tweet(tweet_id='1467863507', username='USERID_3', num_liked=1498, length=91),
 Tweet(tweet_id='1467863508', username='USERID_1', num_liked=1650, length=82),
 Tweet(tweet_id='1467863633', username='USERID_9', num_liked=9549, length=95),
 Tweet(tweet_id='1467863684', username='USERID_1', num_liked=3108, length=142),
 Tweet(tweet_id='1467863716', username='USERID_7', num_liked=6088, length=48),
 Tweet(tweet_id='1467864250', username='USERID_7', num_liked=3198, length=111),
 Tweet(tweet_id='1467870864', username='USERID_9', num_liked=7390, length=119),
 Tweet(tweet_id='1467870866', username='USERID_2', num_liked=4166, length=82),
 Tweet(tweet_id='1467871007', username='USERID_6', num_liked=6527, length=81),
 Tweet(tweet_id='1467871040', username='USERID_5', num_liked=1115, length=89),
 Tweet(tweet_id='1467871223', username='USERID_10', num_liked=6506, length=130),
 Tweet(tweet_id='1467871226', username='USERID_9', num_liked=683, length=62),
 Tweet(tweet_id='1467871545', username='USERID_5', num_liked=3342, length=129),
 Tweet(tweet_id='1467871552', username='USERID_3', num_liked=8876, length=52),
 Tweet(tweet_id='1467871661', username='USERID_9', num_liked=8472, length=104),
 Tweet(tweet_id='1467871754', username='USERID_8', num_liked=5203, length=52),
 Tweet(tweet_id='1467871917', username='USERID_9', num_liked=6516, length=48),
 Tweet(tweet_id='1467871956', username='USERID_2', num_liked=110, length=68),
 Tweet(tweet_id='1467872136', username='USERID_9', num_liked=3265, length=84),
 Tweet(tweet_id='1467872175', username='USERID_1', num_liked=1418, length=28),
 Tweet(tweet_id='1467872181', username='USERID_6', num_liked=6938, length=64),
 Tweet(tweet_id='1467872218', username='USERID_5', num_liked=3366, length=37),
 Tweet(tweet_id='1467872247', username='USERID_2', num_liked=6316, length=137),
 Tweet(tweet_id='1467872309', username='USERID_9', num_liked=3512, length=123),
 Tweet(tweet_id='1467872355', username='USERID_6', num_liked=6313, length=106),
 Tweet(tweet_id='1467872594', username='USERID_6', num_liked=3097, length=37),
 Tweet(tweet_id='1467872638', username='USERID_5', num_liked=3310, length=72),
 Tweet(tweet_id='1467872759', username='USERID_1', num_liked=6966, length=49),
 Tweet(tweet_id='1467872940', username='USERID_8', num_liked=5494, length=30),
 Tweet(tweet_id='1467873004', username='USERID_4', num_liked=1976, length=75),
 Tweet(tweet_id='1467873227', username='USERID_10', num_liked=8958, length=75),
 Tweet(tweet_id='1467873256', username='USERID_6', num_liked=6042, length=76),
 Tweet(tweet_id='1467873467', username='USERID_5', num_liked=7632, length=86),
 Tweet(tweet_id='1467873592', username='USERID_1', num_liked=547, length=56),
 Tweet(tweet_id='1467873828', username='USERID_6', num_liked=520, length=34),
 Tweet(tweet_id='1467873980', username='USERID_5', num_liked=9608, length=88),
 Tweet(tweet_id='1467874103', username='USERID_1', num_liked=9177, length=128),
 Tweet(tweet_id='1467874479', username='USERID_6', num_liked=9149, length=102),
 Tweet(tweet_id='1467874569', username='USERID_3', num_liked=3439, length=12),
 Tweet(tweet_id='1467874916', username='USERID_2', num_liked=6935, length=23),
 Tweet(tweet_id='1467875163', username='USERID_2', num_liked=9891, length=69),
 Tweet(tweet_id='1467875208', username='USERID_5', num_liked=2904, length=106),
 Tweet(tweet_id='1467875930', username='USERID_5', num_liked=9106, length=82),
 Tweet(tweet_id='1467876016', username='USERID_9', num_liked=7912, length=131),
 Tweet(tweet_id='1467876133', username='USERID_1', num_liked=2748, length=44),
 Tweet(tweet_id='1467944581', username='USERID_1', num_liked=7216, length=131),
 Tweet(tweet_id='1467944654', username='USERID_7', num_liked=2838, length=59),
 Tweet(tweet_id='1467944871', username='USERID_1', num_liked=9393, length=51),
 Tweet(tweet_id='1467945476', username='USERID_10', num_liked=9246, length=33),
 Tweet(tweet_id='1467945704', username='USERID_1', num_liked=526, length=62),
 Tweet(tweet_id='1467945787', username='USERID_9', num_liked=8850, length=81),
 Tweet(tweet_id='1467945885', username='USERID_4', num_liked=9403, length=67),
 Tweet(tweet_id='1467946026', username='USERID_1', num_liked=2861, length=69),
 Tweet(tweet_id='1467946137', username='USERID_1', num_liked=5470, length=135),
 Tweet(tweet_id='1467946559', username='USERID_6', num_liked=987, length=116),
 Tweet(tweet_id='1467946592', username='USERID_3', num_liked=9085, length=137),
 Tweet(tweet_id='1467946749', username='USERID_4', num_liked=3381, length=42),
 Tweet(tweet_id='1467946810', username='USERID_4', num_liked=5338, length=62),
 Tweet(tweet_id='1467947005', username='USERID_7', num_liked=6974, length=53),
 Tweet(tweet_id='1467947104', username='USERID_6', num_liked=5847, length=24),
 Tweet(tweet_id='1467947557', username='USERID_9', num_liked=8449, length=110),
 Tweet(tweet_id='1467947713', username='USERID_7', num_liked=7444, length=140),
 Tweet(tweet_id='1467947913', username='USERID_2', num_liked=8578, length=36),
 Tweet(tweet_id='1467948169', username='USERID_1', num_liked=4545, length=33),
 Tweet(tweet_id='1467948434', username='USERID_9', num_liked=770, length=53),
 Tweet(tweet_id='1467948521', username='USERID_4', num_liked=8276, length=100),
 Tweet(tweet_id='1467948526', username='USERID_3', num_liked=7010, length=64),
 Tweet(tweet_id='1467948979', username='USERID_10', num_liked=9209, length=93),
 Tweet(tweet_id='1467949047', username='USERID_3', num_liked=7231, length=30),
 Tweet(tweet_id='1467949516', username='USERID_3', num_liked=4787, length=104),
 Tweet(tweet_id='1467949681', username='USERID_5', num_liked=5318, length=36),
 Tweet(tweet_id='1467949746', username='USERID_8', num_liked=4383, length=8),
 Tweet(tweet_id='1467949969', username='USERID_3', num_liked=1177, length=80),
 Tweet(tweet_id='1467950027', username='USERID_10', num_liked=8575, length=26),
 Tweet(tweet_id='1467950029', username='USERID_1', num_liked=7362, length=119),
 Tweet(tweet_id='1467950217', username='USERID_7', num_liked=1241, length=63),
 Tweet(tweet_id='1467950510', username='USERID_7', num_liked=5002, length=34),
 Tweet(tweet_id='1467950588', username='USERID_4', num_liked=589, length=63),
 Tweet(tweet_id='1467950600', username='USERID_3', num_liked=5951, length=71),
 Tweet(tweet_id='1467950649', username='USERID_7', num_liked=9449, length=46),
 Tweet(tweet_id='1467950687', username='USERID_3', num_liked=3464, length=70),
 Tweet(tweet_id='1467950866', username='USERID_4', num_liked=122, length=27),
 Tweet(tweet_id='1467950975', username='USERID_3', num_liked=6793, length=74),
 Tweet(tweet_id='1467951016', username='USERID_5', num_liked=7795, length=80),
 Tweet(tweet_id='1467951035', username='USERID_9', num_liked=3477, length=114),
 Tweet(tweet_id='1467951252', username='USERID_2', num_liked=7515, length=48),
 Tweet(tweet_id='1467951422', username='USERID_6', num_liked=2520, length=98),
 Tweet(tweet_id='1467951568', username='USERID_8', num_liked=39, length=98),
 Tweet(tweet_id='1467951850', username='USERID_8', num_liked=1170, length=29),
 Tweet(tweet_id='1467951931', username='USERID_4', num_liked=5320, length=81),
 Tweet(tweet_id='1467952069', username='USERID_7', num_liked=399, length=24),
 Tweet(tweet_id='1467952100', username='USERID_1', num_liked=2754, length=69),
 Tweet(tweet_id='1467952123', username='USERID_9', num_liked=9222, length=137),
 Tweet(tweet_id='1467952985', username='USERID_4', num_liked=6256, length=118),
 Tweet(tweet_id='1467953090', username='USERID_2', num_liked=1896, length=64)]
,
    "17": [os.path.join('sample_data', '2.json')],
    "18": [os.path.join('full_data', '3.csv')],
    "19": [os.path.join('full_data', '5.csv'),
             os.path.join('full_data', '4.csv'),
             os.path.join('full_data', '3.csv'),
             os.path.join('full_data', '2.csv'),
             os.path.join('full_data', '1.csv'),
             os.path.join('full_data', '5.json'),
             os.path.join('full_data', '4.json'),
             os.path.join('full_data', '3.json'),
             os.path.join('full_data', '2.json')],
    "20": [Tweet(tweet_id='1467894593', username='USERID_2', num_liked=869000000, length=136),
 Tweet(tweet_id='1467894600', username='USERID_8', num_liked=915000, length=67),
 Tweet(tweet_id='1467853431', username='USERID_10', num_liked=9936, length=30),
 Tweet(tweet_id='1467875163', username='USERID_2', num_liked=9891, length=69),
 Tweet(tweet_id='1467860904', username='USERID_7', num_liked=9851, length=30),
 Tweet(tweet_id='1467928014', username='USERID_7', num_liked=9830, length=18),
 Tweet(tweet_id='1467895048', username='USERID_10', num_liked=9822, length=136),
 Tweet(tweet_id='1467966646', username='USERID_7', num_liked=9821, length=47),
 Tweet(tweet_id='1467855673', username='USERID_9', num_liked=9728, length=72),
 Tweet(tweet_id='1467898078', username='USERID_10', num_liked=9705, length=104),
 Tweet(tweet_id='1467812579', username='USERID_1', num_liked=9700, length=26),
 Tweet(tweet_id='1467928300', username='USERID_9', num_liked=9681, length=79),
 Tweet(tweet_id='1467917177', username='USERID_3', num_liked=9678, length=105),
 Tweet(tweet_id='1467923235', username='USERID_9', num_liked=9662, length=134),
 Tweet(tweet_id='1467964211', username='USERID_4', num_liked=9618, length=79),
 Tweet(tweet_id='1467873980', username='USERID_5', num_liked=9608, length=88),
 Tweet(tweet_id='1467852067', username='USERID_4', num_liked=9594, length=34),
 Tweet(tweet_id='1467863633', username='USERID_9', num_liked=9549, length=95),
 Tweet(tweet_id='1467953733', username='USERID_4', num_liked=9526, length=67),
 Tweet(tweet_id='1467862806', username='USERID_2', num_liked=9465, length=68)]
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
        cmd = py_cmd + ' -m ' + cmd
    subprocess.check_output(cmd, shell=True)

    # parse notebook
    with open(new_notebook) as f:
        nb = json.load(f, encoding='utf-8')
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
    actual_lines = outputs[0].get('data', {}).get('text/plain', [])
    actual = ''.join(actual_lines)
    jbn = [7,8,9,10,11,12,13,14,15,16,20]
    if qnum in jbn:
        actual = (eval(compile(ast.parse(actual, mode='eval'), '', 'eval')))
    else:
        try:
            actual = ast.literal_eval(actual)
        except Exception as e:
            print("COULD NOT PARSE THIS CELL:")
            print(actual)
            raise e
    expected = expected_json[str(qnum)]

    if type(expected) != type(actual):
        return "expected an answer of type %s but found one of type %s" % (type(expected), type(actual))

    if format == TEXT_FORMAT:
        if type(expected) == float:
            if not math.isclose(actual, expected, rel_tol=1e-06, abs_tol=15e-05):
                return "expected %s but found %s" % (str(expected), str(actual))
        else:
            if expected != actual:
                return "expected %s but found %s" % (str(expected), repr(actual))
    elif format == TEXT_FORMAT_UNORDERED_LIST:
        try:
            extra = set(actual) - set(expected)
            missing = set(expected) - set(actual)
            if missing:
                return "missing %d entries from list, such as: %s" % (len(missing), repr(list(missing)[0]))
            elif extra:
                return "found unexpected entry in list: %s" % repr(list(extra)[0])
            elif len(actual) != len(expected):
                return "expected %d entries in the list but found %d" % (len(expected), len(actual))
        except TypeError:
            # Just do a simple comparison
            if actual != expected:
                return "expected %s" % repr(expected)
    elif format == TEXT_FORMAT_ORDERED_LIST:
        try:
            extra = set(actual) - set(expected)
            missing = set(expected) - set(actual)
            if missing:
                return "missing %d entries from list, such as: %s" % (len(missing), repr(list(missing)[0]))
            elif extra:
                return "found unexpected entry in list: %s" % repr(list(extra)[0])
            elif len(actual) != len(expected):
                return "expected %d entries in the list but found %d" % (len(expected), len(actual))
            elif expected != actual:
                if sorted(expected) == sorted(actual):
                    return "list not sorted as expected"
                for i in range(len(expected)):
                    if type(expected[i]) != type(actual[i]):
                        return "expected an element of type %s at index %d of the list, but found one of type %s" % (type(expected[i]), i, type(actual[i]))
                    elif expected[i] != actual[i]:
                        return "expected %s at index %d of the list, but found %s" % (repr(expected[i]), i, repr(actual[i]))
        except TypeError:
            # Just do a simple comparison
            if actual != expected:
                return "expected %s" % repr(expected)
    elif format == TEXT_FORMAT_DICT:
        missing_keys = set(expected.keys()) - set(actual.keys())
        extra_keys = set(actual.keys()) - set(expected.keys())
        if missing_keys:
            key = list(missing_keys)[0]
            return "missing %d key value pairs (%s: %s) from dict" % (len(missing_keys), repr(key), repr(expected[key]))
        elif extra_keys:
            key = list(extra_keys)[0]
            return "found unexpected key value pair (%s: %s) in dict" % (repr(key), repr(actual[key]))
        for key in expected:
            if type(expected[key]) != type(actual[key]):
                return "expected a value of type %s for the key %s, but found %s" % (type(expected[key]), repr(key), type(actual[key]))
            elif expected[key] != actual[key]:
                if type(expected[key]) == list:
                    extra = set(actual[key]) - set(expected[key])
                    missing = set(expected[key]) - set(actual[key])
                    if missing:
                        return "missing %d entries from value for key %s, such as: %s" % (len(missing), repr(key), repr(list(missing)[0]))
                    elif extra:
                        return "found unexpected entry %s in the value for key %s" % (repr(list(extra)[0]), repr(key))
                    elif len(actual[key]) != len(expected[key]):
                        return "expected %d entries in the value for key %s, but found %d" % (len(expected[key]), repr(key), len(actual[key]))
                    elif sorted(expected[key]) == sorted(actual[key]):
                        return "value of key %s not sorted as expected" % (repr(key))
                return "expected value %s for the key %s, but found %s" % (repr(expected[key]), repr(key), repr(actual[key]))
    elif format == TEXT_FORMAT_LIST_DICTS_ORDERED:
        try:
            if len(expected) < len(actual):
                for extra in actual:
                    if extra not in expected:
                        return "found unexpected entry in list: %s" % repr(extra)
                return "expected %d entries in the list but found %d" % (len(expected), len(actual))
            elif len(expected) > len(actual):
                for missing in expected:
                    if missing not in actual:
                        return "missing entries from list, such as %s" % repr(missing)
                return "expected %d entries in the list but found %d" % (len(expected), len(actual))
            for i in range(len(expected)):
                expected_dict = expected[i]
                actual_dict = actual[i]
                if type(actual_dict) != type(expected_dict):
                    return "expected a list of %s but found one of type %s at index %d" % (type(expected_dict), type(actual_dict), i)
                missing_keys = set(expected_dict.keys()) - set(actual_dict.keys())
                extra_keys = set(actual_dict.keys()) - set(expected_dict.keys())
                if missing_keys:
                    key = list(missing_keys)[0]
                    return "missing %d key value pairs (%s: %s) from dict at index %d of the list" % (len(missing_keys), repr(key), repr(expected_dict[key]), i)
                elif extra_keys:
                    key = list(extra_keys)[0]
                    return "found unexpected key value pair (%s: %s) in dict at index %d of the list" % (repr(key), repr(actual_dict[key]), i)
                for key in expected_dict:
                    if type(expected_dict[key]) != type(actual_dict[key]):
                        return "expected a value of type %s for the key %s in dict at index %d of the list, but found %s" % (type(expected_dict[key]), repr(key), i, type(actual_dict[key]))
                    if expected_dict[key] != actual_dict[key]:
                        if type(expected_dict[key]) == list:
                            extra = set(actual_dict[key]) - set(expected_dict[key])
                            missing = set(expected_dict[key]) - set(actual_dict[key])
                            if missing:
                                return "missing %d entries from value for key %s, such as %s, at index %d of the list" % (len(missing), repr(key), repr(list(missing)[0]), i)
                            elif extra:
                                return "found unexpected entry %s in the value for key %s at index %d of the list" % (repr(list(extra)[0]), repr(key), i)
                            elif len(actual_dict[key]) != len(expected_dict[key]):
                                return "expected %d entries in the value for key %s but found %d, at index %d of the list" % (len(expected_dict[key]), repr(key), len(actual_dict[key]), i)
                            elif sorted(expected_dict[key]) == sorted(actual_dict[key]):
                                return "value of key %s not sorted as expected" % (repr(key))
                        return "expected value %s for the key %s in dict at index %d of the list, but found %s" % (repr(expected_dict[key]), repr(key), i, repr(actual_dict[key]))
        except:
            # Just do a simple comparison
            if actual != expected:
                return "expected %s" % repr(expected)
    else:
        if expected != actual:
            return "expected %s" % repr(expected)
    return PASS


def check_cell(question, cell):
    print('Checking question %d' % question.number)
    if question.format.split()[0] == TEXT_FORMAT:
        return check_cell_text(question.number, cell, question.format)

    raise Exception("invalid question type")


def grade_answers(cells):
    results = {'score':0, 'tests': []}

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

    if (
        sys.version_info[0] == 3
        and sys.version_info[1] >= 8
        and sys.platform.startswith("win")
        ):
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
        print("\nIf your file is named something other than main.ipynb, you can specify that by replacing '<notebook.ipynb>' with the name you chose:\n")
        print("python test.py <notebook.ipynb>")
        sys.exit(1)

    nb = rerun_notebook(orig_notebook)

    # check for sever linter errors
    issues = linter_severe_check(nb)
    if issues:
        print("\nPlease fix the following, then rerun the tests:")
        for issue in issues:
            print(' - ' + issue)
        print("")
        sys.exit(1)

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

    print("\nSummary:")
    for test in results["tests"]:
        print("  Test %d: %s" % (test["test"], test["result"]))

    print('\nTOTAL SCORE: %.2f%%' % results['score'])
    with open('result.json', 'w') as f:
        f.write(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
