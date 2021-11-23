#!/usr/bin/python

import ast, os, sys, subprocess, json, re, collections, math, warnings
from collections import namedtuple, OrderedDict, defaultdict
from bs4 import BeautifulSoup
from datetime import datetime
import time
import nbconvert
import nbformat

# check the python version
if sys.version[:5] < '3.7.0':
    warnings.warn('Your current python version is {}. Please upgrade your python version to at least 3.7.0.'.format(sys.version[:5]))

################################################################################
REL_TOL = 6e-04  # relative tolerance for floats
ABS_TOL = 15e-03  # absolute tolerance for floats
TIME = 75 # number of seconds before timer times out
LINTER = False  # set to False if linter should be turned off for project
################################################################################

REQUIRED_FILES = ['expected.html']

try:
    from lint import lint
except ImportError:
    err_msg = """Please download lint.py and place it in this directory for
    the tests to run correctly. If you haven't yet looked at the linting module,
    it is designed to help you improve your code so take a look at:
    https://github.com/msyamkumar/cs220-projects/tree/master/linter"""
    raise FileNotFoundError(err_msg)

ALLOWED_LINT_ERRS = {
  "W0703": "broad-except",
  "R1716": "chained-comparison",
  "E0601": "used-before-assignment",
  "W0105": "pointless-string-statement",
  "E1135": "unsupported-membership-test",
  "R1711": "useless-return",
  "W0143": "comparison-with-callable",
  "E1102": "not-callable",
  "W0107": "unnecessary-pass",
  "W0301": "unnecessary-semicolon",
  "W0404": "reimported",
  "W0101": "unreachable",
  "R1714": "consider-using-in",
  "W0311": "bad-indentation",
  "E0102": "function-redefined",
  "E0602": "undefined-variable",
  "W0104": "pointless-statement",
  "W0622": "redefined-builtin",
  "W0702": "bare-except",
  "R1703": "simplifiable-if-statement",
  "W0631": "undefined-loop-variable",
}

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
HTML_FORMAT = "html"
FILE_FORMAT = "file"
FILE_JSON_FORMAT = "file json"

Question = collections.namedtuple("Question", ["number", "weight", "format"])

questions = [
    # stage 1
    Question(number=1, weight=1, format=TEXT_FORMAT),
    Question(number=2, weight=1, format=HTML_FORMAT),
    Question(number=3, weight=1, format=HTML_FORMAT),
    Question(number=4, weight=1, format=TEXT_FORMAT),
    Question(number=5, weight=1, format=TEXT_FORMAT),
    Question(number=6, weight=1, format=HTML_FORMAT),
    Question(number=7, weight=1, format=TEXT_FORMAT),
    Question(number=8, weight=1, format=TEXT_FORMAT_UNORDERED_LIST),
    Question(number=9, weight=1, format=TEXT_FORMAT),
    Question(number=10, weight=1, format=TEXT_FORMAT_ORDERED_LIST),
    Question(number=11, weight=1, format=TEXT_FORMAT),
    Question(number=12, weight=1, format=TEXT_FORMAT_UNORDERED_LIST),
    Question(number=13, weight=1, format=TEXT_FORMAT),
    Question(number=14, weight=1, format=TEXT_FORMAT),
    Question(number=15, weight=1, format=TEXT_FORMAT_UNORDERED_LIST),
    Question(number=16, weight=1, format=TEXT_FORMAT_UNORDERED_LIST),
    Question(number=17, weight=1, format=TEXT_FORMAT_UNORDERED_LIST),
    Question(number=18, weight=1, format=TEXT_FORMAT_ORDERED_LIST),
    Question(number=19, weight=1, format=TEXT_FORMAT_LIST_DICTS_ORDERED),
    Question(number=20, weight=1, format=FILE_JSON_FORMAT)
]
question_nums = set([q.number for q in questions])

# JSON and plaintext values
expected_json = {
    "1": 103,
    "2": ['Harvard University', 'Harvard University', 'Harvard University'],
    "4": 19,
    "5": 87.26666666666667,
    "7": 'Ludwig Maximilian University of Munich',
    "8": ['Harvard University',
            'Massachusetts Institute of Technology',
            'Stanford University',
            'Columbia University',
            'Princeton University',
            'University of California, Berkeley',
            'University of Pennsylvania',
            'University of Chicago',
            'California Institute of Technology',
            'Yale University',
            'Cornell University',
            'Northwestern University',
            'University of California, Los Angeles',
            'University of Michigan, Ann Arbor',
            'Johns Hopkins University',
            'University of Washington - Seattle',
            'University of Illinois at Urbana–Champaign',
            'Duke University',
            'University of Wisconsin–Madison',
            'New York University',
            'University of California San Diego',
            'University of Texas at Austin',
            'University of California, San Francisco',
            'University of North Carolina at Chapel Hill',
            'University of Minnesota - Twin Cities',
            'University of Texas Southwestern Medical Center',
            'Washington University in St. Louis',
            'University of Southern California',
            'Brown University',
            'Vanderbilt University',
            'Pennsylvania State University',
            'Rutgers University–New Brunswick',
            'Dartmouth College',
            'University of California, Davis'],
    "9": 'Fudan University',
    "10": ['Indian Institute of Science',
             'Tata Institute of Fundamental Research',
             'Indian Institute of Technology Bombay',
             'University of Delhi',
             'Indian Institute of Technology Madras'],
    "11": 1856,
    "12": ['Academy of Scientific & Innovative Research',
            'International Institute for Management Development',
            'Tôn Đức Thắng University',
            'SOAS University of London',
            'Antioch College',
            'École nationale supérieure de chimie de Montpellier',
            'USI - University of Italian Speaking Switzerland',
            'Federal University of Mato Grosso do Sul',
            'Haverford College'],
    "13": 'USI - University of Italian Speaking Switzerland',
    "14": 451,
    "15": ["École nationale d'administration",
             'INSEAD',
             'HEC Paris',
             'Institut Polytechnique de Paris',
             'University of Tokyo',
             'International Institute for Management Development',
             'China Europe International Business School'],
    "16": ['École Polytechnique Fédérale de Lausanne',
             'Emory University',
             'University of Utah',
             'École Polytechnique',
             'University of Texas MD Anderson Cancer Center',
             'University of Groningen',
             'Tufts University',
             'Paris-Sud University',
             'Paris Diderot University',
             'University of California San Diego',
             'Aarhus University',
             'École normale supérieure'],
    "17": ['USA', 'United Kingdom'],
    "18": ['World Rank',
            'Institution',
            'Country',
            'National Rank',
            'Quality of Education Rank',
            'Alumni Employment Rank',
            'Quality of Faculty Rank',
            'Research Performance Rank',
            'Score'],
    "19": [{'World Rank': 1,
              'Year': '2019-2020',
              'Institution': 'Harvard University',
              'Country': 'USA',
              'National Rank': 1,
              'Quality of Education Rank': 2,
              'Alumni Employment Rank': 1,
              'Quality of Faculty Rank': 1,
              'Research Performance Rank': 1,
              'Score': 100.0},
             {'World Rank': 2,
              'Year': '2019-2020',
              'Institution': 'Massachusetts Institute of Technology',
              'Country': 'USA',
              'National Rank': 2,
              'Quality of Education Rank': 1,
              'Alumni Employment Rank': 10,
              'Quality of Faculty Rank': 2,
              'Research Performance Rank': 5,
              'Score': 96.7},
             {'World Rank': 3,
              'Year': '2019-2020',
              'Institution': 'Stanford University',
              'Country': 'USA',
              'National Rank': 3,
              'Quality of Education Rank': 9,
              'Alumni Employment Rank': 3,
              'Quality of Faculty Rank': 3,
              'Research Performance Rank': 2,
              'Score': 95.2},
             {'World Rank': 4,
              'Year': '2019-2020',
              'Institution': 'University of Cambridge',
              'Country': 'United Kingdom',
              'National Rank': 1,
              'Quality of Education Rank': 4,
              'Alumni Employment Rank': 19,
              'Quality of Faculty Rank': 5,
              'Research Performance Rank': 11,
              'Score': 94.1},
             {'World Rank': 5,
              'Year': '2019-2020',
              'Institution': 'University of Oxford',
              'Country': 'United Kingdom',
              'National Rank': 2,
              'Quality of Education Rank': 10,
              'Alumni Employment Rank': 24,
              'Quality of Faculty Rank': 10,
              'Research Performance Rank': 4,
              'Score': 93.3}],
    "20": {'rankings.json': 'my_rankings.json'}
}
expected_files = ['expected.html']

def parse_df_html_table(html, question=None):
    soup = BeautifulSoup(html, 'html.parser')

    if question == None:
        tables = soup.find_all('table')
        assert(len(tables) == 1)
        table = tables[0]
    else:
        # find a table that looks like this:
        # <table data-question="6"> ...
        table = soup.find('table', {"data-question": str(question)})

    rows = []
    for tr in table.find_all('tr'):
        rows.append([])
        for cell in tr.find_all(['td', 'th']):
            rows[-1].append(cell.get_text())

    cells = {}
    for r in range(1, len(rows)):
        for c in range(1, len(rows[0])):
            rname = rows[r][0]
            cname = rows[0][c]
            cells[(rname,cname)] = rows[r][c]
    return cells


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
    cmds = ['python3', 'python', 'py']
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
    elif question.format == HTML_FORMAT:
        return check_cell_html(question.number, cell)
    elif question.format.split()[0] == FILE_FORMAT:
            return check_cell_file(question.number, question.format)
    raise Exception("invalid question type")

def check_cell_file(question, format):
    msg = PASS
    if format == FILE_JSON_FORMAT:
        expected, actual = list(expected_json[str(question)].items())[0]
        if expected not in os.listdir("."):
            return "file %s not found" % expected
        elif actual not in os.listdir("."):
            return "file %s not found" % actual
        e = open(expected, encoding='utf-8')
        expected_data = json.load(e)
        e.close()
        a = open(actual, encoding='utf-8')
        actual_data = json.load(a)
        a.close()
        msg = list_compare_ordered(expected_data, actual_data, 'file ' + actual)
    return msg

def check_files(files=REQUIRED_FILES):
    print('Checking if files are present: ', end='')
    missing_files = []
    for file in files:
        if not os.path.exists(file):
            missing_files.append(file)
    return missing_files


def check_cell_html(qnum, cell):
    outputs = cell.get('outputs', [])
    if len(outputs) == 0:
        return 'no outputs in an Out[N] cell'
    actual_lines = outputs[0].get('data', {}).get('text/html', [])
    try:
        actual_cells = parse_df_html_table(''.join(actual_lines))
    except Exception as e:
        print("ERROR!  Could not find table in notebook")
        raise e

    try:
        with open('expected.html', encoding='utf-8') as f:
            expected_cells = parse_df_html_table(f.read(), qnum)
    except Exception as e:
        print("ERROR!  Could not find table in expected.html")
        raise e

    return diff_df_cells(actual_cells, expected_cells)


def diff_df_cells(actual_cells, expected_cells):
    for location, expected in expected_cells.items():
        location_name = "column {} at index {}".format(location[1], location[0])
        actual = actual_cells.get(location, None)
        if actual == None:
            return 'value missing for ' + location_name
        try:
            actual_float = float(actual)
            expected_float = float(expected)
            if math.isnan(actual_float) and math.isnan(expected_float):
                return PASS
            if not math.isclose(actual_float, expected_float, rel_tol=1e-02, abs_tol=1e-02):
                print(type(actual_float), actual_float)
                return "found {} in {} but it was not close to expected {}".format(actual, location_name, expected)
        except Exception as e:
            if actual != expected:
                return "found '{}' in {} but expected '{}'".format(actual, location_name, expected)
    return PASS

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

def obfuscate1():
    return 'namedtuple'

def obfuscate2():
    return ['list', 'of', 'attributes']


def main():
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
        print("\nIf your file is named something other than main.ipynb, you can specify that by replacing '<notebook.ipynb>' with the name you chose:\n")
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

    lint_msgs = lint(orig_notebook, verbose=1, show=False)
    lint_msgs = filter(lambda msg: msg.msg_id in ALLOWED_LINT_ERRS, lint_msgs)
    lint_msgs = list(lint_msgs)
    results["lint"] = [str(l) for l in lint_msgs]

    functionality_score = 100.0 * passing / total
    linting_score = min(10.0, len(lint_msgs))
    results['score'] = max(functionality_score - linting_score, 0.0)

    print("\nSummary:")
    for test in results["tests"]:
        print("  Test %d: %s" % (test["test"], test["result"]))

    if len(lint_msgs) > 0:
        msg_types = defaultdict(list)
        for msg in lint_msgs:
            msg_types[msg.category].append(msg)
        print("\nLinting Summary:")
        for msg_type, msgs in msg_types.items():
            print('  ' + msg_type.title() + ' Messages:')
            for msg in msgs:
                print('    ' + str(msg))

    print('\nTOTAL SCORE: %.2f%%' % results['score'])
    with open('result.json', 'w') as f:
        f.write(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
