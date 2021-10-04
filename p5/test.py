import ast, os, sys, subprocess, json, re, collections, math, warnings

# check the python version
if sys.version[:5] < '3.7.0':
    warnings.warn('Your current python version is {}. Please upgrade your python version to at least 3.7.0.'.format(sys.version[:5]))

################################################################################
REL_TOL = 6e-04 # relative tolerance for floats
ABS_TOL = 15e-03 # absolute tolerance for floats
LINTER = False # set to False if linter should be turned off for project
################################################################################

PASS = "PASS"
TEXT_FORMAT = "text" # question type when expected answer is a str, int, float, or bool
TEXT_FORMAT_UNORDERED_LIST = "text list_unordered" # question type when the expected answer is a list where the order does *not* matter
TEXT_FORMAT_ORDERED_LIST = "text list_ordered" # question type when the expected answer is a list where the order does matter
TEXT_FORMAT_SPECIAL_ORDERED_LIST = "text list_special_ordered" # question type when the expected answer is a list where order does matter, but with possible ties.
TEXT_FORMAT_DICT = "text dict" # question type when the expected answer is a dictionary
TEXT_FORMAT_LIST_DICTS_ORDERED = "text list_dicts_ordered" # question type when the expected answer is a list of dicts where the order does matter
PNG_FORMAT = "png" # use when the expected answer is an image

Question = collections.namedtuple("Question", ["number", "weight", "format"])

questions = [
    Question(number=1, weight=1, format=TEXT_FORMAT),
    Question(number=2, weight=1, format=TEXT_FORMAT),
    Question(number=3, weight=1, format=TEXT_FORMAT),
    Question(number=4, weight=1, format=TEXT_FORMAT),
    Question(number=5, weight=1, format=TEXT_FORMAT),
    Question(number=6, weight=1, format=TEXT_FORMAT),
    Question(number=7, weight=1, format=TEXT_FORMAT),
    Question(number=8, weight=1, format=TEXT_FORMAT),
    Question(number=9, weight=1, format=TEXT_FORMAT),
    Question(number=10, weight=1, format=TEXT_FORMAT),
    Question(number=11, weight=1, format=TEXT_FORMAT),
    Question(number=12, weight=1, format=TEXT_FORMAT),
    Question(number=13, weight=1, format=TEXT_FORMAT),
    Question(number=14, weight=1, format=TEXT_FORMAT),
    Question(number=15, weight=1, format=TEXT_FORMAT),
    Question(number=16, weight=1, format=TEXT_FORMAT),
    Question(number=17, weight=1, format=TEXT_FORMAT),
    Question(number=18, weight=1, format=TEXT_FORMAT),
    Question(number=19, weight=1, format=TEXT_FORMAT),
    Question(number=20, weight=1, format=TEXT_FORMAT),
]
question_nums = set([q.number for q in questions])

# JSON and plaintext values
expected_json = {
    "1": 141,
    "2": "Isaias",
    "3": 1,
    "4": 2,
    "5": 75,
    "6": 115,
    "7": 68700000000,
    "8": "Katrina",
    "9": 175,
    "10": 2704200000,
    "11": "David",
    "12": 1899,
    "13": 91610000000,
    "14": 140,
    "15": 3,
    "16": 22,
    "17": "1991 to 2000",
    "18": 59,
    "19": "Dora",
    "20": "Earl",
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
        #cmd = py_cmd + ' -m ' + cmd
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
            msg = "expected %s"  % (repr(expected))
            if complete_msg:
                msg = msg + " but found %s" % (repr(actual))
    else:
        if expected != actual:
            msg = "expected %s"  % (repr(expected))
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
            val = list_compare_ordered(expected[i], actual[i], "sub"+obj)
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
            msg = "in the %s, missing " % (obj) + val + ", but found un" + list_compare_helper(sort_actual, sort_expected)

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
            actual_item = actual[i: i+j]
            val = list_compare_unordered(expected_item, actual_item)
            if val != PASS:
                if j == 1:
                    msg = "at index %d " % (i) + val
                else:
                    msg = "between indices %d and %d " % (i, i+j-1) + val
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
        msg = "unexpected datatype found in keys of dict; expect a dict with keys of type %s" % (type(expected_keys[0]).__name__)
        return msg
    val = list_compare_unordered(expected_keys, actual_keys, "dict")
    if val != PASS:
        msg = "bad keys in %s: " % (obj) + val
    if msg == PASS:
        for key in expected:
            if type(expected[key]) in [int, float, bool, str]:
                val = simple_compare(expected[key], actual[key])
            elif type(expected[key]) in [list]:
                val = list_compare_ordered(expected[key], actual[key], "value")
            elif type(expected[key]) in [dict]:
                val = dict_compare(expected[key], actual[key], "sub"+obj)
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
        print("\nIf your file is named something other than main.ipynb, you can specify that by replacing '<notebook.ipynb>' with the name you chose:\n")
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
            print ("Q%d is not checked by test.py." % (png_passed[0]))
        else:
            for n in png_passed[:-1]:
                print ("Q%d" % n, end=", ")
            print ("and Q%d are not checked by test.py." % (png_passed[-1]))
        print("Please refer to the corresponding reference png files and the expected output dictionary given in the documentation.\n")

    with open('result.json', 'w') as f:
        f.write(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
