from django.utils.timezone import localdate

from probe.probe import check_file_count, show_files
from publish.file_search import probe_files, python_code_files, template_files
from publish.files import read_file
from publish.text import text_join


def test_coder_app_spec():
    return read_file("config/app.yaml")


def test_coder_date():
    return localdate().strftime("%Y-%m-%d")


def test_coder_probe_source():
    return show_files("Probe Code ", probe_files, 250, 305)


def test_coder_python_source():
    return show_files("Python Code ", python_code_files, 5600, 7000)


def test_coder_templates():
    text = "test_template_files: Templates " + \
        check_file_count(template_files(), 30, 35)
    return text + text_join(template_files())
