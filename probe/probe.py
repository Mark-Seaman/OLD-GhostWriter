from inspect import getmembers, isfunction
from os import listdir
from requests import get
from traceback import format_exc

from publish.files import join_files, recursive_files
from publish.shell import banner
from publish.text import text_join, text_lines
from probe.models import Probe, TestResult


# Global Variables
m = ''   # Needed for test_map()
all_probes = {}


def approve_result(result):
    probe = result.probe
    probe.expected = result.output
    probe.passed = True
    probe.save()
    result.passed = True
    result.save()


def accept_results():
    for t in Probe.objects.all():
        r = TestResult.objects.filter(probe=t).order_by('date').last()
        approve_result(r)


def check_files(path, min, max):
    return f"Document files: {path}  - {check_file_count(recursive_files(path), min, max)}"


def check_range(label, num, min, max):
    if min > num or num > max:
        return f"{label}: {num} is not in range (min {min} and max {max})"
    return f"{label}: min {min} -- max {max}"


def check_file_count(files, min, max):
    num_files = len(files)
    return check_range('Files', num_files, min, max)
    # if min > num_files or num_files > max:
    #     return f": {num_files} is not in range (min {min} and max {max})"
    # return f"Files: min {min} -- max {max}"


def check_line_count(label, text, min, max):
    lines = len(text_lines(text))
    return check_range(label, lines, min, max)

    # if min > lines or lines > max:
    #     return f"{label} lines: {lines} is not in range (min {min} and max {max})"
    # return f"{label}: min {min} -- max {max}"


def check_webpage(url):
    try:
        response = get(url)
        assert(response.status_code == 200)
        return response.text
    except:
        return f'Error in getting web page: {url} (status code = {response.status_code})\n'


def clear_probe_history(probe_pk=None):
    if probe_pk:
        TestResult.objects.filter(probe__pk=probe_pk).delete()
    else:
        TestResult.objects.all().delete()


def count_files(label, file_function):
    files = file_function()
    print(f'\nFiles in {label} - {len(files)}')
    for f in files:
        print(' '*4, f)


def execute_probe(probe):

    def get_test_function(name):
        global all_probes
        if not all_probes:
            find_tests()
        return all_probes[name]

    def execute_test(source):
        try:
            return get_test_function(source)()
        except:
            return f'Test Failed to execute:  {source}() \n {format_exc()}'

    def save_results(probe):
        # print(f'\nRun Test: {probe.name}')
        output = execute_test(probe.name)
        passed = (output == probe.expected)
        probe.passed = passed
        probe.save()
        # print(f'OUTPUT:\n{output}')
        if not output:
            output = 'None'

        # Update the result for this probe
        result = TestResult.objects.get_or_create(probe=probe)[0]
        result.output=output
        result.passed=passed
        result.save()

        # print(result.probe.name, result.probe.expected, result.output, result.passed)
        return result
    
    # clear_probe_history(probe.pk)
    return save_results(probe)


def find_tests():

    def module_list(directory):
        return [f.replace('.py', '') for f in listdir(directory) if f.startswith('probe_')]

    def get_module(module_name):
        global m
        exec(f'import probe.{module_name}; global m; m = probe.{module_name}')
        return m

    def test_functions(module_name):
        module = get_module(module_name)
        functions = getmembers(module, isfunction)
        return [f for f in functions if f[0].startswith('test_')]

    global all_probes

    for module_name in module_list('probe'):
        for f in test_functions(module_name):
            source = '.'.join(['probe', module_name, f[0]])
            all_probes[f[0]] = f[1]
            t = Probe.create(name=f[0], source=source)


def list_tests():
    return dict(passing=Probe.objects.filter(passed=True), failing=Probe.objects.filter(passed=False))


def result_list(probe):
    results = TestResult.objects.filter(probe=probe)
    for r in results:
        r.passed = (r.output == probe.expected)
        r.save()
    return results


def reset_tests():
    global all_probes
    Probe.objects.all().delete()
    all_probes = {}
    find_tests()


def run_tests():
    # TestResult.objects.all().delete()
    find_tests()
    for probe in Probe.objects.all():
        print(probe.name)
        result = execute_probe(probe)


def save_page(path, url):
    if not path.exists():
        text = get(url).text
        path.write_text(text)
    else:
        text = path.read_text()
    return text


def show_files(label, files, min, max):
    f = files()
    text = text_join(f) + '\n'
    code = join_files(f)
    # text += code + '\n'
    text += check_line_count(label, code, min, max)
    return text


def test_results():
    for t in Probe.objects.all():
        if not t.passed:
            r = TestResult.objects.filter(probe=t).order_by('date').last()
            print(banner(r.probe.source))
            # print(f'\n\nTest Results: {r.probe.source}\n')
            print(f'\nDifferences:\n    {r.difference}')
            # print('    PASS' if r.passed else '    FAIL')
            # print(f'\n    Expected:\n    {r.probe.expected}')
            # print(f'\n    OUTPUT:\n    {r.output}')


# find_tests()
