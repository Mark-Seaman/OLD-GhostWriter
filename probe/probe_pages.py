from pathlib import Path

from requests import get

from publish.files import read_csv_file
from publish.text import text_join

from .probe import check_webpage, check_line_count, save_page


# def test_web_pages():
#     urls = '''https://shrinking-world.com
# https://markseaman.org
# https://seamanslog.com/publish/
# https://seamanslog.com/book/
# https://seamanslog.com/book/journey
# https://seamanslog.com/book/journey/Part0
# https://seamanslog.com
# https://seamanslog.com/sampler/Index
# https://seamanslog.com/write/Index
# '''

#     results = [f'{url} - {get(url)}' for url in text_lines(urls) if url]
#     return text_join(results)


def test_pages_bouncer():
    bounce_table = read_csv_file('Documents/Shrinking-World-Pubs/_bouncer.csv')
    d = Path('probe/pages')
    d.mkdir(exist_ok=True)
    output = 'Page Tester:\n'
    for p in bounce_table:
        if p[1:]:
            path = d / f'{p[0]}.html'
            text = save_page(path, p[1])
            output += f'{p[0]} -- {p[1]} -- {len(text)} characters\n'
    return output


def test_pages_web():
    pages = read_csv_file('probe/pages.csv')
    d = Path('probe/pages')
    d.mkdir(exist_ok=True)
    output = 'Page Tester:\n'
    for i,p in enumerate(pages):
        if p[2:]:
            path = d / f'web-{i}.html'
            text = save_page(path, p[0])
            text = check_line_count(f'Lines in {p[0]}', text, int(p[1]), int(p[2]))
            output += f'{path} -- {text}\n'
    return output


def test_website_pages():
    return 'OK'
