from os.path import join
from platform import node
from subprocess import Popen, PIPE

from publish.files import dir_tree_list, file_tree_list


def banner(name):
    '''Show a banner for this file in the output'''
    return '\n%s\n%s%s\n%s\n' % ('-' * 80, ' ' * 30, name, '-' * 80)


def check_dirs(path, min=0, max=0):
    '''Count directories in a directory and compare to known limits'''
    if max == 0:
        max = min
    dirs = dir_tree_list(path)
    num_dirs = len(dirs)
    if num_dirs < min or num_dirs > max:
        message = 'dirs(%s) --> %d dirs (should be between %d and %d)'
        return (message % (path, num_dirs, min, max))
    return ''


def check_dir_list(path, dir_list):
    '''Count directories in a list of directories and compare to known limits'''
    results = [check_dirs(join(path, d[0]), d[1], d[2] if d[2:] else 0) for d in dir_list]
    return '\n'.join(results)


def check_files(path, min=0, max=0):
    '''Count files in a directory and compare to known limits'''
    files = file_tree_list(path)
    num_files = len(files)
    if max == 0:
        max = min
    if num_files < min or num_files > max:
        message = 'files(%s) --> %d files (should be between %d and %d)'
        return (message % (path, num_files, min, max))
    return ''


def check_file_list(path, dir_list):
    '''Count files in a list of directories and compare to known limits'''
    results = [check_files(join(path, d[0]), d[1], d[2] if d[2:] else 0) for d in dir_list]
    return '\n'.join(results)


def check_lines(label, lines, min=0, max=10):
    '''Verify the number of lines in text'''
    lines = lines.split('\n')
    if len(lines) < min or len(lines) > max:
        return f'{label}: {len(lines)} lines of output (should be between {min} and {max})'


def check_shell_lines(cmd, min=0, max=10):
    '''Check for lines returned by the shell command output'''
    return check_lines(cmd, shell(cmd), min, max)


# def curl_get(url):
#     html = shell('curl -s %s' % url)
#     return redact_css(html)
#
#
# def redact_css(text):
#     from tool.text import text_replace
#     match = r'\.css\?.*">\n*'
#     replacement = r'.css">\n'
#     return text_replace(text, match, replacement)


def differences(answer, correct):
    '''   Calculate the diff of two strings   '''
    if answer != correct:
        t1 = '/tmp/diff1'
        t2 = '/tmp/diff2'
        with open(t1, 'wt') as file1:
            # print (answer)
            file1.write(str(answer) + '\n')
        with open(t2, 'wt') as file2:
            file2.write(str(correct) + '\n')
        diffs = shell('diff %s %s' % (t1, t2))
        if diffs:
            # print('Differences detected:     < actual     > expected')
            # print (diffs)
            return diffs


def hostname():
    '''Get the hostname of this computer'''
    return node()


# def is_imac():
#     return 'imac' in hostname()
#
#
# def is_macbook():
#     return 'macbook' in hostname()
#
#
# def is_server():
#     return hostname() == 'sensei-server'


# def send_email_test():
#     send_mail(
#         'Test Message from webserver',
#         'Here is the message.',
#         'mark.b.seaman@gmail.com',
#         ['mark@seamanfamily.org'],
#         fail_silently=False,
#     )


def shell(command_string):
    p = Popen('bash', stdin=PIPE, stdout=PIPE)
    (out, error) = p.communicate(input=command_string.encode('utf-8'))
    if error:
        return error.decode('utf-8') + out.decode('utf-8')
    return out.decode('utf-8')


def limit_lines(shell_command, min=None, max=None):
    '''Limit the lines to a certain number or echo all the output'''
    text = shell(shell_command)
    violation = check_lines(shell_command, text, min, max)
    if violation:
        text = text.split('\n')
        text = '\n'.join([line[:60] for line in text])
        return violation
    return ''
