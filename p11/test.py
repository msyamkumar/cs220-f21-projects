import ast, os, sys, subprocess, json, re, collections, math, warnings, time

# check the python version
if sys.version[:5] < '3.7.0':
    warnings.warn('Your current python version is {}. Please upgrade your python version to at least 3.7.0.'.format(
        sys.version[:5]))

################################################################################
REL_TOL = 6e-04  # relative tolerance for floats
ABS_TOL = 15e-03  # absolute tolerance for floats
TIME = 75 # number of seconds before timer times out
LINTER = False  # set to False if linter should be turned off for project
################################################################################

REQUIRED_FILES = [os.path.join('sample_data', '1.json'),
         os.path.join('sample_data', '2.json'),
         os.path.join('sample_data', '1.csv'),
         os.path.join('sample_data', '2.csv'),
         os.path.join('full_data', '1.json'),
         os.path.join('full_data', '2.json'),
         os.path.join('full_data', '3.json'),
         os.path.join('full_data', '4.json'),
         os.path.join('full_data', '5.json'),
         os.path.join('full_data', '1.csv'),
         os.path.join('full_data', '2.csv'),
         os.path.join('full_data', '3.csv'),
         os.path.join('full_data', '4.csv'),
         os.path.join('full_data', '5.csv'),
         os.path.join('recursive', 'others', 'USERID_5.json'),
         os.path.join('recursive', 'others', 'USERID_6.json'),
         os.path.join('recursive', 'others', 'USERID_7.json'),
         os.path.join('recursive', 'others', 'USERID_8.json'),
         os.path.join('recursive', 'others', 'USERID_9.json'),
         os.path.join('recursive', 'others', 'USERID_10.json'),
         os.path.join('recursive', 'USERID_1', 'tweets.json'),
         os.path.join('recursive', 'USERID_2', 'tweets.json'),
         os.path.join('recursive', 'USERID_3', 'tweets.json'),
         os.path.join('recursive', 'USERID_4', '1.json'),
         os.path.join('recursive', 'USERID_4', '2.json'),
         os.path.join('recursive', 'USERID_4', '1.csv'),
         os.path.join('recursive', 'USERID_4', '2.csv'),
         os.path.join('recursive', 'USERID_4', 'false', 'tweets.json'),
         os.path.join('recursive', 'USERID_4', 'true', 'tweets.json'),
         os.path.join('play', 'ls', 'lu.txt'),
         os.path.join('play', 'ls', 'mf.py'),
         os.path.join('play', 'ls', 'qwe', 'iuqwe.json'),
         os.path.join('play', 'ls', 'qwe', 'usun.pdf'),
         os.path.join('play', 'ou', 'a'),
         os.path.join('play', 'ou', 'b'),
         os.path.join('play', 'ou', 'quap', 'aoq', 'aqnsa'),
         os.path.join('play', 'ou', 'quap', 'aoq', 'qsonj'),
         os.path.join('play', 'ou', 'quap', 'qonxu.txt'),
         os.path.join('play', 'ou', 'quap', 'uikwe'),
         os.path.join('play', 'ou', 'v'),
         os.path.join('play', 'rb', 'ppt.ppt'),
         os.path.join('play', 'rb', 'rb9', '12.xls'),
         os.path.join('play', 'rb', 'rb9', '89.csv')]

PASS = "PASS"
TEXT_FORMAT = "text"  # question type when expected answer is a str, int, float, or bool
TEXT_FORMAT_NAMEDTUPLE = "text namedtuple"  # question type when expected answer is a namedtuple
TEXT_FORMAT_UNORDERED_LIST = "text list_unordered"  # question type when the expected answer is a list where the order does *not* matter
TEXT_FORMAT_ORDERED_LIST = "text list_ordered"  # question type when the expected answer is a list where the order does matter
TEXT_FORMAT_ORDERED_LIST_NAMEDTUPLE = "text list_ordered namedtuple"  # question type when the expected answer is a list of namedtuples where the order does matter
TEXT_FORMAT_SPECIAL_ORDERED_LIST = "text list_special_ordered"  # question type when the expected answer is a list where order does matter, but with possible ties. All tied elements are put in a list, where internal order does not matter.
TEXT_FORMAT_DICT = "text dict"  # question type when the expected answer is a dictionary
TEXT_FORMAT_LIST_DICTS_ORDERED = "text list_dicts_ordered"  # question type when the expected answer is a list of dicts where the order does matter
PNG_FORMAT = "png"  # use when the expected answer is an image

Question = collections.namedtuple("Question", ["number", "weight", "format"])

questions = [
    Question(number=1, weight=1, format=TEXT_FORMAT),
    Question(number=2, weight=1, format=TEXT_FORMAT_UNORDERED_LIST),
    Question(number=3, weight=1, format=TEXT_FORMAT_DICT),
    Question(number=4, weight=1, format=TEXT_FORMAT_DICT),
    Question(number=5, weight=1, format=TEXT_FORMAT_DICT),
    Question(number=6, weight=1, format=PNG_FORMAT),
    Question(number=7, weight=1, format=PNG_FORMAT),
    Question(number=8, weight=1, format=PNG_FORMAT),
    Question(number=9, weight=1, format=TEXT_FORMAT),
    Question(number=10, weight=1, format=TEXT_FORMAT_ORDERED_LIST_NAMEDTUPLE),
    Question(number=11, weight=1, format=TEXT_FORMAT),
    Question(number=12, weight=1, format=PNG_FORMAT),
    Question(number=13, weight=1, format=PNG_FORMAT),
    Question(number=14, weight=1, format=TEXT_FORMAT_ORDERED_LIST),
    Question(number=15, weight=1, format=TEXT_FORMAT_ORDERED_LIST),
    Question(number=16, weight=1, format=TEXT_FORMAT_ORDERED_LIST),
    Question(number=17, weight=1, format=TEXT_FORMAT_ORDERED_LIST),
    Question(number=18, weight=1, format=TEXT_FORMAT_ORDERED_LIST),
    Question(number=19, weight=1, format=TEXT_FORMAT),
    Question(number=20, weight=1, format=TEXT_FORMAT),
]
question_nums = set([q.number for q in questions])

def get_expected_json():
    # JSON and plaintext values
    expected_json = {
        "1": 131,
        "2": ['USERID_1',
                'USERID_9',
                'USERID_4',
                'USERID_7',
                'USERID_6',
                'USERID_2',
                'USERID_10',
                'USERID_8',
                'USERID_3',
                'USERID_5'],
        "3": {'USERID_1': 52,
               'USERID_7': 55,
               'USERID_10': 45,
               'USERID_9': 44,
               'USERID_4': 35,
               'USERID_6': 51,
               'USERID_3': 39,
               'USERID_2': 47,
               'USERID_5': 46,
               'USERID_8': 31},
        "4": {'USERID_1': 150,
               'USERID_7': 144,
               'USERID_10': 136,
               'USERID_9': 137,
               'USERID_4': 138,
               'USERID_6': 145,
               'USERID_3': 138,
               'USERID_2': 138,
               'USERID_5': 146,
               'USERID_8': 145},
        "5": {'USERID_1': 9393,
               'USERID_7': 9851,
               'USERID_10': 9936,
               'USERID_9': 9728,
               'USERID_4': 9618,
               'USERID_6': 9149,
               'USERID_3': 9678,
               'USERID_2': 869000000,
               'USERID_5': 9608,
               'USERID_8': 915000},
        "9": 'USERID_2',
        "10": [Tweet(tweet_id='1467894593', username='USERID_2', num_liked=869000000, length=136),
                Tweet(tweet_id='1467875163', username='USERID_2', num_liked=9891, length=69),
                Tweet(tweet_id='1467862806', username='USERID_2', num_liked=9465, length=68),
                Tweet(tweet_id='1467907751', username='USERID_2', num_liked=9048, length=110),
                Tweet(tweet_id='1467928764', username='USERID_2', num_liked=9026, length=41),
                Tweet(tweet_id='1467943007', username='USERID_2', num_liked=9000, length=130),
                Tweet(tweet_id='1467918682', username='USERID_2', num_liked=8884, length=102),
                Tweet(tweet_id='1467935121', username='USERID_2', num_liked=8740, length=37),
                Tweet(tweet_id='1467947913', username='USERID_2', num_liked=8578, length=36),
                Tweet(tweet_id='1467892667', username='USERID_2', num_liked=8270, length=20),
                Tweet(tweet_id='1467897316', username='USERID_2', num_liked=7890, length=64),
                Tweet(tweet_id='1467854917', username='USERID_2', num_liked=7741, length=30),
                Tweet(tweet_id='1467961106', username='USERID_2', num_liked=7552, length=65),
                Tweet(tweet_id='1467951252', username='USERID_2', num_liked=7515, length=48),
                Tweet(tweet_id='1467889988', username='USERID_2', num_liked=7394, length=51),
                Tweet(tweet_id='1467916959', username='USERID_2', num_liked=7081, length=69),
                Tweet(tweet_id='1467874916', username='USERID_2', num_liked=6935, length=23),
                Tweet(tweet_id='1467855981', username='USERID_2', num_liked=6455, length=92),
                Tweet(tweet_id='1467872247', username='USERID_2', num_liked=6316, length=137),
                Tweet(tweet_id='1467918850', username='USERID_2', num_liked=5383, length=103),
                Tweet(tweet_id='1467919055', username='USERID_2', num_liked=5370, length=68),
                Tweet(tweet_id='1467915670', username='USERID_2', num_liked=5287, length=138),
                Tweet(tweet_id='1467880442', username='USERID_2', num_liked=5125, length=96),
                Tweet(tweet_id='1467896253', username='USERID_2', num_liked=4906, length=91),
                Tweet(tweet_id='1467962897', username='USERID_2', num_liked=4898, length=98),
                Tweet(tweet_id='1467855812', username='USERID_2', num_liked=4806, length=28),
                Tweet(tweet_id='1467930220', username='USERID_2', num_liked=4770, length=94),
                Tweet(tweet_id='1467852031', username='USERID_2', num_liked=4565, length=63),
                Tweet(tweet_id='1467905378', username='USERID_2', num_liked=4420, length=111),
                Tweet(tweet_id='1467877833', username='USERID_2', num_liked=4270, length=89),
                Tweet(tweet_id='1467870866', username='USERID_2', num_liked=4166, length=82),
                Tweet(tweet_id='1467879984', username='USERID_2', num_liked=3694, length=69),
                Tweet(tweet_id='1467898511', username='USERID_2', num_liked=3477, length=99),
                Tweet(tweet_id='1467926632', username='USERID_2', num_liked=2602, length=98),
                Tweet(tweet_id='1467862213', username='USERID_2', num_liked=2455, length=138),
                Tweet(tweet_id='1467878633', username='USERID_2', num_liked=2351, length=33),
                Tweet(tweet_id='1467878971', username='USERID_2', num_liked=2238, length=27),
                Tweet(tweet_id='1467953090', username='USERID_2', num_liked=1896, length=64),
                Tweet(tweet_id='1467908798', username='USERID_2', num_liked=1659, length=51),
                Tweet(tweet_id='1467918015', username='USERID_2', num_liked=1508, length=97),
                Tweet(tweet_id='1467926444', username='USERID_2', num_liked=1394, length=61),
                Tweet(tweet_id='1467914499', username='USERID_2', num_liked=910, length=138),
                Tweet(tweet_id='1467968584', username='USERID_2', num_liked=777, length=132),
                Tweet(tweet_id='1467933102', username='USERID_2', num_liked=625, length=135),
                Tweet(tweet_id='1467953277', username='USERID_2', num_liked=494, length=31),
                Tweet(tweet_id='1467890222', username='USERID_2', num_liked=227, length=107),
                Tweet(tweet_id='1467871956', username='USERID_2', num_liked=110, length=68)],
        "11": 5003.565217391304,
        "14": [os.path.join('play', 'rb', 'ppt.ppt'),
                os.path.join('play', 'rb', 'rb9', '12.xls'),
                os.path.join('play', 'rb', 'rb9', '89.csv')],
        "15": [os.path.join('play', 'ls', 'qwe', 'iuqwe.json'),
                os.path.join('play', 'ls', 'qwe', 'usun.pdf')],
        "16": [os.path.join('play', 'ls', 'lu.txt'),
                os.path.join('play', 'ls', 'mf.py'),
                os.path.join('play', 'ls', 'qwe', 'iuqwe.json'),
                os.path.join('play', 'ls', 'qwe', 'usun.pdf'),
                os.path.join('play', 'ou', 'a'),
                os.path.join('play', 'ou', 'b'),
                os.path.join('play', 'ou', 'quap', 'aoq', 'aqnsa'),
                os.path.join('play', 'ou', 'quap', 'aoq', 'qsonj'),
                os.path.join('play', 'ou', 'quap', 'qonxu.txt'),
                os.path.join('play', 'ou', 'quap', 'uikwe'),
                os.path.join('play', 'ou', 'v'),
                os.path.join('play', 'rb', 'ppt.ppt'),
                os.path.join('play', 'rb', 'rb9', '12.xls'),
                os.path.join('play', 'rb', 'rb9', '89.csv')],
        "17": [os.path.join('recursive', 'others', 'USERID_10.json'),
                os.path.join('recursive', 'others', 'USERID_5.json'),
                os.path.join('recursive', 'others', 'USERID_6.json'),
                os.path.join('recursive', 'others', 'USERID_7.json'),
                os.path.join('recursive', 'others', 'USERID_8.json'),
                os.path.join('recursive', 'others', 'USERID_9.json')],
        "18": [os.path.join('recursive', 'USERID_1', 'tweets.json'),
                os.path.join('recursive', 'USERID_2', 'tweets.json'),
                os.path.join('recursive', 'USERID_3', 'tweets.json'),
                os.path.join('recursive', 'USERID_4', '1.csv'),
                os.path.join('recursive', 'USERID_4', '1.json'),
                os.path.join('recursive', 'USERID_4', '2.csv'),
                os.path.join('recursive', 'USERID_4', '2.json'),
                os.path.join('recursive', 'USERID_4', 'false', 'tweets.json'),
                os.path.join('recursive', 'USERID_4', 'true', 'tweets.json'),
                os.path.join('recursive', 'others', 'USERID_10.json'),
                os.path.join('recursive', 'others', 'USERID_5.json'),
                os.path.join('recursive', 'others', 'USERID_6.json'),
                os.path.join('recursive', 'others', 'USERID_7.json'),
                os.path.join('recursive', 'others', 'USERID_8.json'),
                os.path.join('recursive', 'others', 'USERID_9.json')],
        "19": 37,
        "20": 220,
    }
    return expected_json

def obfuscate1():
    return "Tweet"


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

def obfuscate2():
    return ['tweet_id', 'username', 'num_liked', 'length']


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
    if 'namedtuple' in format:
        try:
            actual = (eval(compile(ast.parse(actual, mode='eval'), '', 'eval')))
        except NameError:
            obfuscate3 = actual.split('(')[0]
            return "expected to find namedtuple object of type %s but found type %s" % (type(expected_json[str(qnum)]).__name__, obfuscate3)
        except TypeError:
            return "expected to find attributes: %s in namedtuple %s" % (str(expected_json[str(qnum)]._fields), type(expected_json[str(qnum)]).__name__)
    else:
        try:
            actual = ast.literal_eval(actual)
        except ValueError:
            pass
    expected = expected_json[str(qnum)]

    # try:
    if format in [TEXT_FORMAT, TEXT_FORMAT_NAMEDTUPLE]:
        return simple_compare(expected, actual)
    elif format in [TEXT_FORMAT_ORDERED_LIST, TEXT_FORMAT_ORDERED_LIST_NAMEDTUPLE]:
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
    # except:
    #     if expected != actual:
    #         return "expected %s" % (repr(expected))
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
    elif type(expected).__name__ == obfuscate1():
        msg = namedtuple_compare(expected, actual)
    else:
        if expected != actual:
            msg = "expected %s" % (repr(expected))
            if complete_msg:
                msg = msg + " but found %s" % (repr(actual))
    return msg

def namedtuple_compare(expected, actual):
    msg = PASS
    for field in expected._fields:
        val = simple_compare(getattr(expected, field), getattr(actual, field))
        if val != PASS:
            msg = "at attribute %s of namedtuple %s, " % (field, type(expected).__name__) + val
            return msg
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
        elif type(expected[i]).__name__ == obfuscate1():
            val = simple_compare(expected[i], actual[i])
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
    print('Checking question: %d' % question.number)
    if question.format.split()[0] == TEXT_FORMAT:
        return check_cell_text(question.number, cell, question.format)
    elif question.format == PNG_FORMAT:
        return check_cell_png(question.number, cell)
    raise Exception("invalid question type")

def check_files(files=REQUIRED_FILES):
    print('Checking if files are present: ', end='')
    missing_files = []
    for file in files:
        if not os.path.exists(file):
            missing_files.append(file)
    return missing_files

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

Tweet = collections.namedtuple(obfuscate1(), obfuscate2())
expected_json = get_expected_json()

def main():
    print()
    if (sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith("win")):
        import asyncio
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # check if files are present
    file_check = check_files()
    if file_check != []:
        for i in range(len(file_check)):
            file_check[i] = str(i+1) + ") " + file_check[i]
        print('The following files were not found:\n%s\n\nPlease make sure your files are stored as per the project requirements.\n' % '\n\t'.join(['']+file_check))
        sys.exit(1)
    else:
        print('All files found.\n')

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

    start_time = time.time()
    print('Running notebook:\n')
    nb = rerun_notebook(orig_notebook)
    print()
    end_time = time.time()

    # check if notebook takes too long to run
    if end_time - start_time > TIME:
        print('*'*108)
        print("TIME OUT: Your code takes far too long to run, and will time out on the autograder!")
        print("Please make your code run in less than %s seconds. Otherwise, you will receive a 0 score on this project!" % TIME)
        print('*'*108 + '\n')
        sys.exit(1)

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
        print("Please refer to the corresponding reference png files given in the documentation.\n")

    with open('result.json', 'w') as f:
        f.write(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
