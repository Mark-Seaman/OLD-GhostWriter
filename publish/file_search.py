from posixpath import join
from re import findall

from publish.files import file_search, recursive_dirs, recursive_files
from publish.text import match_pattern, text_join, transform_matches


def application_files(path='.'):
    def exclude(p):
        f = str(p)
        return (f.startswith('env') or
                f.startswith('.git') or
                f.startswith('Temp') or
                f.startswith('Github') or
                f.startswith('Documents') or
                f.startswith('.cache') or
                '.pyc' in f or
                '/migrations/' in f)

    return recursive_files('.', '', exclude)


def code_directories(path='.'):
    return recursive_dirs('.')


def code_search(word):
    return file_text_search('code', [word])


def doc_files():
    files = recursive_files(
        'Documents', ['/history/', 'info/Test', '.DS_Store', '.git'])
    return [join('Documents', f) for f in files]


def doc_search(word):
    return file_text_search('doc', [word])


def find_classes(text):
    pattern = r'class (.*)\(.*\)'
    return match_pattern(text, pattern).split('\n')


def find_functions(text):
    pattern = r'\ndef (.*)\(.*\)'
    return findall(pattern, text)


def find_signatures(text):
    pattern = r'def(.*\(.*\)):'
    return transform_matches(text, pattern, r'\1').split('\n')


def html_files():
    all_files = recursive_files('.', ['env/', '.git'])
    return [f for f in all_files if f.endswith('.html')] + [f for f in all_files if f.endswith('.css')]

    # exclude = ['env', '.venv']
    # files = text_lines(shell_file_list('.', 'html', exclude))
    # files += text_lines(shell_file_list('.', 'css', exclude))
    # return files


def html_search(words):
    files = html_files()
    return file_search(files, words)


def list_functions():
    functions = []
    files = code_files()
    for code in files:
        text = open(code).read()
        functions.append(code + ':')
        functions.append('    ' + '\n    '.join(find_functions(text)))
    return text_join(functions)


def file_text_search(file_selector='all', words=[]):
    if file_selector == 'code':
        files = code_files()
    elif file_selector == 'doc':
        files = doc_files()
    elif file_selector == 'html':
        files = html_files()
    else:
        files = code_files() + html_files() + doc_files()
    # print(selector + 'search:')
    return file_search(files, words)


def probe_files():
    return [f for f in python_code_files() if 'probe/probe_' in f]


def python_code_files(path='.'):

    def exclude(p):
        f = str(p)
        return (f.startswith('.venv') or
                f.startswith('.git') or
                f.startswith('Temp') or
                f.startswith('Github') or
                f.startswith('Documents') or
                f.startswith('.cache') or
                '/migrations/' in f)

    return recursive_files('.', '.py', exclude)


def source_code():
    return '\n'.join([open(code).read() for code in python_code_files()])


def template_files(path='.'):

    def exclude(p):
        f = str(p)
        return (f.startswith('.venv') or
                f.startswith('.git') or
                f.startswith('.Documents/') or
                f.startswith('Temp') or
                f.startswith('probe/pages') or
                f.startswith('Github') or
                f.startswith('Documents') or
                f.startswith('.cache') or
                f.startswith('static/reveal.js/'))

    return recursive_files('.', '.html', exclude)
