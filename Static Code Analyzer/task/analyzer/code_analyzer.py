import glob
import re
import sys


def S001(line):
    return len(line) > 79


def S002(line):
    return (len(line) - len(line.lstrip())) % 4 != 0


def S003(line):
    return line.strip()[-1] == ';' and '# ' not in line or ';  #' in line or '; #' in line


def S004(line):
    return '#' in line and '  #' not in line and line[0] != '#'


def S005(line):
    line = line.lower()
    return 'todo' in line and -1 < line.find('#') < line.find('todo')


def S007(line):
    if re.search(r'class\s\s', line):
        return 'class'
    elif re.search(r'def\s\s', line):
        return 'def'


def S008(line):
    result = re.search(r'(class\s)(.*?)[(:]', line)
    if result:
        s = result.group(2)
        if s == s.lower() or s == s.upper() or "_" in s:
            return s


def S009(line):
    result = re.search(r'(def\s)(.*?)[(:]', line)
    if result:
        s = result.group(2)
        if re.search(r'[A-Z-]', s):
            return s


def S010(line):
    result = re.findall(r'\((\w*?)[=,)]|,\s(\w*?)[=,)]', line)
    if result:
        for set_ in result:
            for entry in set_:
                if re.search(r'[A-Z-]', entry):
                    return entry



def S011(line):
    result = re.search(r'(\w*?)\s=', line)
    if result:
        s = result.group(1)
        if re.search(r'[A-Z-]', s):
            return s


def S012(line):
    return re.search(r'[A-Za-z0-9]\(.*?=\[]', line)


def code_analyzer(file):
    blank_lines = 0
    positives = []
    with open(file, 'r') as check_file:
        for num, line in enumerate(check_file, start=1):
            if not line.strip():
                blank_lines += 1
                continue
            if S001(line):
                print(f'{file}: Line {num}: S001 Line too long')
            if S002(line):
                print(f'{file}: Line {num}: S002 Indentation not a multiple of four')
            if S003(line):
                print(f'{file}: Line {num}: S003 Unnecessary semicolon after statement')
            if S004(line):
                print(f'{file}: Line {num}: S004 Less than two spaces before inline comment')
            if S005(line):
                print(f'{file}: Line {num}: S005 TODO found')
            if blank_lines > 2:
                print(f'{file}: Line {num}: S006 More than two blank lines preceding code line')
            blank_lines = 0
            S007_comp = S007(line)
            if S007_comp:
                print(f'{file}: Line {num}: S007 Too many spaces after "{S007_comp}"')
            S008_comp = S008(line)
            if S008_comp:
                print(f'{file}: Line {num}: S008 Class name "{S008_comp}" should use CamelCase')
            S009_comp = S009(line)
            if S009_comp:
                print(f'{file}: Line {num}: S009 Function name "{S009_comp}" should use snake_case')
            S010_comp = S010(line)
            if S010_comp and S010_comp not in positives:
                positives.append(S010_comp)
                print(f'{file}: Line {num}: S010 Argument name "{S010_comp}" should use snake_case')
            S011_comp = S011(line)
            if S011_comp and S011_comp not in positives:
                positives.append(S011_comp)
                print(f'{file}: Line {num}: S011 Variable "{S011_comp}" should use snake_case')
            if S012(line):
                print(f'{file}: Line {num}: S012 The default argument value is mutable')


def main(link):
    if link[-3:] == '.py':
        code_analyzer(link)
    else:
        for filename in glob.iglob(link + '**/*.py', recursive=True):
            code_analyzer(filename)


main(sys.argv[1])
