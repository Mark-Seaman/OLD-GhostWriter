from csv import reader, writer
from genericpath import getmtime
from glob import glob
from io import StringIO
from json import dump, loads
import os
from os import W_OK, access, getcwd, listdir, remove, walk
from os.path import dirname, exists, isdir, isfile, join
from pathlib import Path
from re import search
import shutil
from subprocess import PIPE, Popen

from publish.text import text_join, text_lines, word_count


def content_word_summary(path):
    filetype = '.md'
    files = file_tree_list(path, filetype)
    text = ''
    counts = [path]
    for f in files:
        counts.append(words_in_file(f))
        text += read_file(f)
    words = word_count(text)
    counts.append(f'Total Words = {words}\n\n')
    return text_join(counts)


def copy_files(source, dest):
    dest = Path(dest)
    dest.mkdir(parents=True, exist_ok=True)
    for f in Path(source).glob('*'):
        if not (dest/f.name).exists():
            shutil.copy2(f, dest/f.name)


# Print the count and directory name
def count_files(directory):
    return len(recursive_files(directory))


# Create the directory if needed
def create_directory(path):
    """Handles creating any number of directories when necessary"""
    # Converts to absolute path if relative
    path = Path(path).resolve()
    # Create the directory if it doesn't exist, ignoring errors if it already exists
    os.makedirs(path, exist_ok=True)
    return path

# Delete a relative path name
def delete_file(filename):
    remove(filename)


# Return a list of directories in the directory
def dir_list(path):
    if not exists(path):
        return ['No directory exists']
    return [d for d in listdir(path) if isdir(join(path, d))]


# Return a list of dirs in the directory tree
def dir_tree_list(path):
    dirs = []
    if not exists(path):
        return ['No directory exists']
    for root, dirnames, filenames in walk(path):
        if not '.git' in root:
            for filename in dirnames:
                dirs.append(join(root, filename))
    return dirs


# Remove strange character encodings and convert from utf to ascii
def encode_text(text, encoding='utf-8'):
    text = fix_chars(text)
    return text.decode(encoding).encode('ascii', 'ignore')


# Ignore files in directories
def exclude_files():
    return ['.DS_Store', '/migrations/']


# Ignore directories in file list
def exclude_directories():
    return ['.git', '.cache/', '.idea/', '.venv/', '__pycache__', 'env/', 'Documents/', 'static/']


# Return a list of files in the directory tree (ignoring .git)
def file_tree_list(path, filetype=None):
    files = []
    if not exists(path):
        return ['No directory exists']
    for root, dirnames, filenames in walk(path):
        if not '.git/' in root:
            for filename in filenames:
                files.append(join(root, filename))
    return filter_types(files, filetype)


# Return a list of files in the directory
def file_list(path, filetype=None):
    if not exists(path):
        return ['No directory exists']
    files = listdir(file_path(path))
    if filetype:
        files = [f for f in files if f.endswith(filetype)]
    return files


# Form a file path
def file_path(d='', f=''):
    path = d
    if f:
        return join(path, f)
    return path


def filter_types(files, filetype=None):
    '''Select files of a certain type'''
    if filetype:
        files = [f for f in files if f.endswith(filetype)]
    return files


def line_match(word, text):
    '''Find lines that contain text pattern'''
    return '\n'.join([x for x in text.split('\n') if word in x])


def line_exclude(word, text):
    '''Remove lines that contain a text pattern'''
    return '\n'.join([x for x in text.split('\n') if not word in x])


def line_count(path):
    '''Read a file and count the lines of text'''
    return len(text_lines(read_file(path)))


# Search for words in file list
def file_search(files, words):
    matches = []
    for f in files:
        text = text_lines(read_file(f))
        text = [('%s: %s' % (f, line)) for line in text]
        for pattern in words:
            text = [line for line in text if search(pattern, line)]
        if text:
            matches += text
    return text_join(matches)


# Remove strange character encodings
def fix_chars(text):
    text = text.replace('\xe2\x80\x94', "-")
    text = text.replace('\xe2\x80\x98', "'")
    text = text.replace('\xe2\x80\x99', "'")
    text = text.replace('\xe2\x80\x9c', '"')
    text = text.replace('\xe2\x80\x9d', '"')
    return text


# Run a grep command and capture output
def grep(pattern, file):
    p = Popen(["grep", pattern, file], stdout=PIPE)
    return p.stdout.read().decode('utf-8')


# Check if this file is writable
def is_writable(path):
    return access(dirname(path), W_OK) and (not exists(path) or access(path, W_OK))


# def join_files(file_list):
#     return text_join([read_file(f) for f in file_list])


def join_files(files):
    return text_join([Path(f).read_text() for f in files])


# Return the files as a list
def list_files(directory):
    return sorted([f for f in listdir(directory) if isfile(join(directory, f))])


# Return the files as a list
def list_dirs(directory):
    return sorted([f for f in listdir(directory) if isdir(join(directory, f))])


# Absolute path name from a relative path name
def path_name(relative_filename):
    return join(getcwd(), relative_filename)


def not_excluded(path, exclude):
    for x in exclude:
        if x in path:
            return
    return path


def read_csv_file(path):
    assert exists(path)
    with open(path) as f:
        return [row for row in reader(f)]


# Return the text from the file
def read_file(f):
    try:
        if exists(f):
            return open(f).read()
        return 'No file found, ' + f
    except:
        print('**CORRUPT FILE, %s**' % f)
        return '**CORRUPT FILE, %s**' % f


# Read JSON from a file
def read_json(filename):
    f = Path(filename)
    if f.exists():
        return loads(f.read_text())
    return {}


# Read lines from a file and strip off the tailing newline
def read_lines(path):
    if not exists(path):
        return []
    return text_lines(read_file(path))


# Recursive directory list
def recursive_dirs(d, exclude=[]):
    matches = []
    if not exclude:
        exclude = exclude_directories()
    for root, dirnames, filenames in walk(d):
        for dirname in dirnames:
            path = join(root, dirname).replace(d + '/', '')
            if not_excluded(path, exclude):
                matches.append(path)
    return matches


# Recursive list
def recursive_files(path='.', suffix='', exclude=None):
    files = [str(p) for p in Path(path).rglob(f'*{suffix}')]
    if exclude:
        files = [f for f in files if not exclude(f)]
    return sorted(files)


# Extra a table from a CSV string
def table_data(csv_data):
    return list(reader(StringIO(csv_data)))


# Get a file list sorted by time (recent last)
def time_sort_file(d):
    files = filter(isfile, glob(d + "/*"))
    files.sort(key=lambda x: getmtime(x))
    files = map(lambda p: p.replace(d + '/', ''), files)
    return files


# Show the number of words in all the files in a directory
def words_in_directory(path):
    return text_join([words_in_file(join(path, b)) for b in sorted(listdir(path)) if isfile(join(path, b))])


# Show the number of words in the file
def words_in_file(path):
    return f'{word_count(read_file(path)):-4} words in {path}'


# Count all the words in a file
def word_count_in_file(path):
    return word_count(read_file(path))


# Count all the words in the files in a directory
def word_count_in_directory(path):
    total_words = 0
    for f in file_list(path):
        if isfile(f'{path}/{f}'):
            total_words += word_count(read_file(f'{path}/{f}'))
    return total_words


# Write data to a CSV file
def write_csv_file(path, table):
    assert (exists(dirname(path)))
    with open(path, 'w', newline='') as f:
        writer(f).writerows(table)


# Return the text from the file
def write_file(filename, text, append=None):
    create_directory(dirname(filename))
    with open(filename, 'a' if append else 'w') as f:
        f.write(text)


# Write JSON to a file
def write_json(filename, data):
    with open(filename, "w") as f:
        dump(data, f, indent=4)


# # Print a flat list
# def print_list(lst):
#     for f in lst:
#         print (f)
#

# # Print a list two levels deep
# def print_list2(lst):
#     for v in lst:
#         for f in v:
#             print (f,)
#         print ()


# # Read the input as lines of text
# def read_input():
#     text = stdin.read().split('\n')
#     return filter(lambda x: len(x.rstrip()) > 0, text)
#
