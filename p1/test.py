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
TIME = 60 # number of seconds before timer times out
LINTER = False  # set to False if linter should be turned off for project
################################################################################

REQUIRED_FILES = []

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
    Question(number=1, weight=1, format=TEXT_FORMAT),
    Question(number=2, weight=1, format=TEXT_FORMAT),
]
question_nums = set([q.number for q in questions])
png_question_nums = [q.number for q in questions if q.format == PNG_FORMAT]


# JSON and plaintext values
def get_expected_json():
    expected_json = {"1": "Hello World!", "2": 2021}
    return expected_json

def get_special_ordered(): # For questions of type TEXT_FORMAT_SPECIAL_ORDERED_LIST, there can be ties in the list. This function returns the actual values by which they are sorted, so ties can be taken care of.
    special_order = {}
    return special_order

# find a comment something like this: #q10
def extract_question_num(cell):
    for line in cell.get('source', []):
        line = line.strip().replace(' ', '').lower()
        m = re.match(r'\#q(\d+).(\d+)', line)
        if m:
            return float(m.group(1) + "." + m.group(2))
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
    os.remove(new_notebook)
    return nb


def normalize_json(orig):
    try:
        return json.dumps(json.loads(orig.strip("'")), indent=2, sort_keys=True)
    except:
        return 'not JSON'


def obfuscate1():
    return 'namedtuple'


def check_cell_text(qnum, cell, format):
    outputs = cell.get('outputs', [])
    expected = expected_json[str(qnum)]
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
            return "CANNOT PARSE CELL!"
        except IndentationError:
            return "expected to find type %s but found a DataFrame" %(type(expected).__name__)

    try:
        if format in [TEXT_FORMAT, TEXT_FORMAT_NAMEDTUPLE]:
            return simple_compare(expected, actual)
        elif format in [TEXT_FORMAT_ORDERED_LIST, TEXT_FORMAT_ORDERED_LIST_NAMEDTUPLE]:
            return list_compare_ordered(expected, actual)
        elif format == TEXT_FORMAT_UNORDERED_LIST:
            return list_compare_unordered(expected, actual)
        elif format == TEXT_FORMAT_SPECIAL_ORDERED_LIST:
            return list_compare_special(expected, actual, special_order_json[str(qnum)])
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
        msg = "unexpected datatype found in %s; expected entries of type %s" % (obj, obj, type(expected[0]).__name__)
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

def list_compare_special_init(expected, special_order):
    real_expected = []
    for i in range(len(expected)):
        if real_expected == [] or special_order[i-1] != special_order[i]:
            real_expected.append([])
        real_expected[-1].append(expected[i])
    return real_expected


def list_compare_special(expected, actual, special_order):
    expected = list_compare_special_init(expected, special_order)
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


def check_cell_file(question, format):
    msg = PASS
    if format == FILE_JSON_FORMAT:
        expected, actual = list(expected_json[str(question)].items())[0]
        if expected not in os.listdir("."):
            return "file %s not found" % expected
        elif actual not in os.listdir("."):
            return "file %s not found" % actual
        try:
            e = open(expected, encoding='utf-8')
            expected_data = json.load(e)
            e.close()
        except json.JSONDecodeError:
            return "file %s is broken and cannot be parsed; please redownload the file" % expected
        try:
            a = open(actual, encoding='utf-8')
            actual_data = json.load(a)
            a.close()
        except json.JSONDecodeError:
            return "file %s is broken and cannot be parsed" % actual
        if type(expected_data) == list:
            msg = list_compare_ordered(expected_data, actual_data, 'file ' + actual)
        elif type(expected_data) == dict:
            msg = dict_compare(expected_data, actual_data)
    return msg


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


def check_cell_html(qnum, cell):
    outputs = cell.get('outputs', [])
    if len(outputs) == 0:
        return 'no outputs in an Out[N] cell'
    actual_lines = outputs[0].get('data', {}).get('text/html', [])
    try:
        actual_cells = parse_df_html_table(''.join(actual_lines))
    except Exception as e:
        print("ERROR! Could not find table in notebook. Please make sure you have answered with a DataFrame and do not have any other output in this cell.")

    try:
        with open('expected.html', encoding='utf-8') as f:
            expected_cells = parse_df_html_table(f.read(), qnum)
    except Exception as e:
        print("ERROR! Could not find table in expected.html. Please make sure you have downloaded expected.html correctly.")

    return diff_df_cells(actual_cells, expected_cells)


def diff_df_cells(actual_cells, expected_cells):
    for location, expected in expected_cells.items():
        location_name = "column {} at index {}".format(location[1], location[0])
        actual = actual_cells.get(location, None)
        if actual == None:
            return "in location %s, expected to find %s" % (location_name, repr(expected))
        try:
            actual_ans = float(actual)
            expected_ans = float(expected)
            if math.isnan(actual_ans) and math.isnan(expected_ans):
                continue
        except Exception as e:
            actual_ans, expected_ans = actual, expected
        msg = simple_compare(expected_ans, actual_ans)
        if msg != PASS:
            return "in location %s, " % location_name + msg
    expected_cols = list(set(["column %s" %loc[1] for loc in expected_cells]))
    actual_cols = list(set(["column %s" %loc[1] for loc in actual_cells]))
    msg = list_compare_unordered(expected_cols, actual_cols, "DataFrame")
    if msg != PASS:
        return msg
    expected_rows = list(set(["row at index %s" %loc[0] for loc in expected_cells]))
    actual_rows = list(set(["row at index %s" %loc[0] for loc in actual_cells]))
    msg = list_compare_unordered(expected_rows, actual_rows, "DataFrame")
    if msg != PASS:
        return msg

    return PASS


def check_cell(question, cell, visible=True):
    if visible:
        if int(question.number) == question.number:
            print('Checking question: %d' % question.number)
        else:
            print('Checking question: %.1f' % question.number)
    if question.format.split()[0] == TEXT_FORMAT:
        return check_cell_text(question.number, cell, question.format)
    elif question.format == PNG_FORMAT:
        return check_cell_png(question.number, cell)
    elif question.format == HTML_FORMAT:
        return check_cell_html(question.number, cell)
    elif question.format.split()[0] == FILE_FORMAT:
            return check_cell_file(question.number, question.format)
    raise Exception("invalid question type")


def check_files(files=REQUIRED_FILES):
    msg = PASS
    raw_all_files = list(os.walk(".", topdown=True))
    all_files = []
    for f in raw_all_files:
        dir_name_path = f[0].split(os.sep)
        dir_name_path.remove(".")
        if dir_name_path == []:
            dir_name_path = [""]
        dir_name = os.path.join(*dir_name_path)
        for file in f[2]:
            all_files.append(os.path.join(dir_name, file))

    missing_files = []
    for file in files:
        if file not in all_files:
            missing_files.append(file)
        else:
            all_files.remove(file)

    extra_files = {}
    all_file_names = {os.path.split(f)[-1]: f for f in all_files}
    for file in files:
        file_name = os.path.split(file)[-1]
        if file_name in all_file_names:
            extra_files[file] = all_file_names[file_name]

    if missing_files != []:
        missing_files_msg = []
        count = 0
        for f in missing_files:
            count += 1
            missing_msg = str(count) + ") " + f
            if f in extra_files:
                missing_msg += " (file is instead present at " + extra_files[f] + ")"
            missing_files_msg.append(missing_msg)
        msg = ('The following files were not found:%s\n\nPlease make sure your files are stored as per the project requirements.\n' % '\n\t'.join(['']+missing_files_msg))
    elif extra_files != {}:
        extra_files_msg = []
        count = 0
        for f in extra_files:
            count += 1
            extra_files_msg.append(str(count) + ") " + extra_files[f] + " (file already present at " + f + ")")
        msg = ('The following files were found in unexpected directories:%s\n\nDelete these files and use the correct files as per the project requirements.\n' % '\n\t'.join(['']+extra_files_msg))
    return msg


def grade_answers(cells, visible=True):
    results = {'score':0, 'tests': []}

    for question in questions:
        cell = cells.get(question.number, None)
        status = "not found"

        if question.number in cells:
            status = check_cell(question, cells[question.number], visible)

        row = {"test": question.number, "result": status, "weight": question.weight}
        results['tests'].append(row)

    passing = sum(t['weight'] for t in results['tests'] if t['result'] == PASS)
    total = sum(t['weight'] for t in results['tests'])
    results['score'] = 100.0 * passing / total

    return results

def verify_new_notebook(old_cells, new_cells):
    FAIL = "Your answers do not match when the notebook is rerun. Please Restart and Run All cells before saving your notebook."
    old_nb_grading = grade_answers(old_cells, False)
    new_nb_grading = grade_answers(new_cells, False)
    old_new_nb_match = {}
    for t in old_nb_grading["tests"]:
        old_new_nb_match[t['test']] = [t['result']]
    for t in new_nb_grading["tests"]:
        if t['test'] not in old_new_nb_match:
            return FAIL
        old_new_nb_match[t['test']].append(t['result'])
    for q in old_new_nb_match:
        if len(old_new_nb_match[q]) != 2:
            return FAIL
        if old_new_nb_match[q][0] != old_new_nb_match[q][1]:
            return FAIL
    return PASS


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


def obfuscate2():
    return ['list', 'of', 'attributes']

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


expected_json = get_expected_json()
special_order_json = get_special_ordered()
def main():
    print()
    if (sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith("win")):
        import asyncio
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    if LINTER:
        try:
            from lint import lint
        except ImportError:
            err_msg = """Please download lint.py and place it in this directory for
            the tests to run correctly. If you haven't yet looked at the linting module,
            it is designed to help you improve your code so take a look at:
            https://github.com/msyamkumar/cs220-projects/tree/master/linter"""
            raise FileNotFoundError(err_msg)

    # check if files are present
    if REQUIRED_FILES != []:
        print('Checking if files are present as per project requirements: ', end='')
        file_check = check_files()
        if file_check == PASS:
            print("All files found in the correct directories.\n")
        else:
            msg_length = max([len(line) for line in file_check.split("\n")]) + 4
            print("\n" + "*"*msg_length)
            print(file_check)
            print('*'*msg_length + '\n')
            sys.exit(1)

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
    new_nb = rerun_notebook(orig_notebook)
    print()
    with open(orig_notebook, encoding='utf-8') as f:
        old_nb = json.load(f)

    # extract cells that have answers
    new_answer_cells = {}
    for cell in new_nb['cells']:
        q = extract_question_num(cell)
        if q == None:
            continue
        if not q in question_nums:
            print('no question %d' % q)
            continue
        new_answer_cells[q] = cell
    old_answer_cells = {}
    for cell in old_nb['cells']:
        q = extract_question_num(cell)
        if q == None:
            continue
        if not q in question_nums:
            continue
        old_answer_cells[q] = cell

    # check if answers match in old and rerun notebook
    verify_match_msg = verify_new_notebook(old_answer_cells, new_answer_cells)
    if verify_match_msg != PASS:
        print()
        print('*'*len(verify_match_msg))
        print(verify_match_msg)
        print('*'*len(verify_match_msg) + '\n')
        sys.exit(1)

    # do grading on extracted answers and produce results.json
    answer_cells = {}
    for q in new_answer_cells:
        if q not in png_question_nums:
            answer_cells[q] = new_answer_cells[q]
    for q in old_answer_cells:
        if q in png_question_nums:
            answer_cells[q] = old_answer_cells[q]
    results = grade_answers(answer_cells)


    if LINTER:
        print("\nRunning linter: results will be displayed at the end.\n")
        linting_score = 0.0
        lint_msgs = lint(orig_notebook, verbose=1, show=False)
        lint_msgs = filter(lambda msg: msg.msg_id in ALLOWED_LINT_ERRS, lint_msgs)
        lint_msgs = list(lint_msgs)
        results["lint"] = [str(l) for l in lint_msgs]
        linting_score = min(10.0, len(lint_msgs))
        results['score'] = max(results['score'] - linting_score, 0.0)

    end_time = time.time()

    # check if notebook takes too long to run
    if end_time - start_time > TIME:
        time_out_msg1 = "TIME OUT: Your code takes far too long to run, and will time out on the autograder!"
        time_out_msg2 = "Please make your code run in less than %s seconds. Otherwise, you will receive a 0 score on this project!" % TIME
        print()
        print('*'*max(len(time_out_msg1), len(time_out_msg2)))
        print(time_out_msg1)
        print(time_out_msg2)
        print('*'*max(len(time_out_msg1), len(time_out_msg2)) + '\n')
        sys.exit(1)

    print("\nSummary:")
    for test in results["tests"]:
        if int(test['test']) == test['test']:
            print("  Test %d: %s" % (test["test"], test["result"]))
        elif test['result'] != 'not found':
            print("  Test %.1f (optional): %s" % (test["test"], test["result"]))

    png_passed = [q for q in png_question_nums if q in answer_cells]
    if len(png_passed) > 0:
        print("\nWARNING: ", end="")
        if len(png_passed) == 1:
            print("Q%d is not checked by test.py." % (png_passed[0]))
        else:
            for n in png_passed[:-1]:
                print("Q%d" % n, end=", ")
            print("and Q%d are not checked by test.py." % (png_passed[-1]))
        print("Please refer to the corresponding reference png files and the expected output dictionary given in the documentation.\n")

    if LINTER:
        print("\nLinting Summary:")
        if len(lint_msgs) > 0:
            msg_types = defaultdict(list)
            for msg in lint_msgs:
                msg_types[msg.category].append(msg)
            for msg_type, msgs in msg_types.items():
                print('  ' + msg_type.title() + ' Messages:')
                for msg in msgs:
                    print('    ' + str(msg))
        else:
            print('  No major linting errors!')
            print('  Run lint.py with the -v and -vv tags to see minor linting errors')


    print('\nTOTAL SCORE: %.2f%%' % results['score'])
    with open('result.json', 'w') as f:
        f.write(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
