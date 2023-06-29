from pathlib import Path
from publish.files import concatonate
from publish.publication import all_pubs, build_pubs, get_pub_info, save_pub_info, show_pub_json, show_pubs
from publish.text import line_count


def test_pub_import():
    return build_pubs()


def test_pub_json():
    return show_pub_json()


def test_pub_info():
    return 'OK'
#     save_pub_info()
#     text = concatonate('probe/pubs/*')
#     return f'All Pub Info: {line_count(text)}'


def test_show_pubs():
    return show_pubs()
