from os.path import exists
from pathlib import Path
from re import compile, findall, search, split, sub


def text_command(options):
    if options:
        cmd = options[0]
        args = options[1:]
        if cmd == "match":
            m = text_match(args[0], args[1])
            print("\n".join(m))
        elif cmd == "no-match":
            text_no_match(args[0], args[1])
        elif cmd == "replace":
            text_replace(args[0], args[1], args[2])
        else:
            text_help(args)
    else:
        text_help()


def text_help(args=None):
    print(
        """
        text Command

        usage: x text COMMAND

        COMMAND:

            match - show lines that match
            no_match - show lines that don't match
            replace - replace lines
            select - pattern matching in doc

        """
    )


# ------------------------------
# Functions


def as_text(query):
    return text_join([str(x) for x in query])


def capture_ideas(options):
    f = "Documents/info/Index.md"
    with open(f, "a") as x:
        x.write("* " + " ".join(options["command"][1:]) + "\n\n")


def count_lines(text):
    return len(text_lines(text))


def delete_lines(text, match_pattern):
    text = text.split("\n")
    text = [t for t in text if match_pattern not in t]
    return "\n".join(text)


def doc_filter(doc, match_pattern, replace_pattern):
    text = open(doc).read()
    return text_replace(text, match_pattern, replace_pattern)


def find_anchors(text):
    return findall('<a href="(https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+)">(.*)</a>', text)


def find_images(html):
    return findall('<img .*src="(.*?)".*/>', html)


def find_links(text):
    def link(anchor):
        return findall('(https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+)">(.*)</a>', anchor)[0]

    results = []
    for anchor in text.split(r"<a ")[1:]:
        anchor = r"<a " + anchor
        results.append(link(anchor))
    return str(results)


# Look for links in markdown text
def find_markdown_links(text):
    pattern = r"\[(.*)\]\((.*)\)"
    return [(match[0], match[1]) for match in findall(pattern, text)]


def find_quotes(text):
    return findall("<div class='noteText'>(.*?)</div>", text)


def find_urls(text):
    return findall("https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+", text)


def first_line(text):
    if text:
        return text_lines(text)[0].strip()


def char_fix(text):
    text2 = (
        text.replace(" ", " ")
        .replace("’", "'")
        .replace("“", '"')
        .replace("‘", "'")
        .replace("&#x27;", "'")
    )
    # text2 = sub("\[.\]", "", text2)
    return text2


def char_fix_file(path):
    text = Path(path).read_text()
    text2 = char_fix(text)
    if text != text2:
        Path(path).write_text(text2)
        return f"Rewrite {path}\n"


def char_fix_files(directory):
    changed = ["Files Changed"]
    for p in Path(directory).rglob("*.md"):
        x = char_fix_file(p)
        if x:
            changed.append(x)
    return text_join(changed)


def include_files(text, dir=None):
    pattern = r"\[\[(.+)\]\]"
    matches = findall(pattern, text)
    for filename in matches:
        try:
            include = (dir/filename).read_text()
            text = text.replace(f"[[{filename}]]", include)
        except FileNotFoundError:
            print(f"File '{filename}' not found.")
    return text


def get_link(text):
    link = find_markdown_links(text)
    if link:
        return link[0][0], link[0][1]


def markdown_list_links(host, lines):
    return markdown_list_string([f"[{x}]({host}/{x})" for x in lines])


def markdown_list_string(mylist):
    return "* " + "\n* ".join(mylist)


def match_lines(text, pattern):
    text = text.split("\n")
    text = [line for line in text if search(pattern, line)]
    return "\n".join(text)


def match_pattern(text, pattern):
    text = text.split("\n")
    text = [search(pattern, line) for line in text]
    text = [x.string for x in text if x]
    return "\n".join(text)


def no_blank_lines(text):
    text = text_lines(text)
    text = [x for x in text if x.strip() != ""]
    text = text_join(text)
    return text


def number_lines(text):
    lines = text_lines(text)
    lines = [("%s - %s" % (x, i)) for i, x in enumerate(lines) if x.strip()]
    return text_join(lines)


def text_join(text):
    return "\n".join(text)


def text_lines(text):
    return text.split("\n")


def text_markdown(outline, depth=1):
    def text_body(lines):
        if lines and len(lines[0].strip()) == 0:
            return text_body(lines[1:])
        elif lines and len(lines[-1].strip()) == 0:
            return text_body(lines[:-1])
        else:
            return lines

    results = []
    for n in outline:
        results.append("#" * depth + " " + n[0] + "\n")
        t = text_body(n[2])
        if t:
            for t in text_body(n[2]):
                results.append(t)
            results.append("")
        children = text_markdown(n[1], depth + 1)
        if children:
            results.append(children)
    return "\n".join(results)


def text_match(match_pattern, doc):
    matches = []
    if doc and exists(doc):
        text = open(doc).read()
        if text:
            for line in text.split("\n"):
                match = search(r"^.*(%s).*$" % match_pattern, line)
                if match:
                    matches.append(match.string)
            return "\n".join([("%s: %s" % (doc, m)) for m in matches])


def text_no_match(match_pattern, doc):
    text = open(doc).read()
    for line in text_lines(text):
        match = search(r"^.*(%s).*$" % match_pattern, line)
        if not match:
            print(line)


def text_outline(text):
    lines = text_lines(text)
    root = []
    active = None
    for line in lines:
        if line.startswith("# "):
            active = [line[2:], [], []]
            root.append(active)
            h1 = active
        elif line.startswith("## "):
            active = [line[3:], [], []]
            h1[1].append(active)
            h2 = active
        elif line.startswith("### "):
            active = [line[4:], [], []]
            h2[1].append(active)
            h3 = active
        elif line.startswith("#### "):
            active = [line[5:], [], []]
            h3[1].append(active)
        else:
            if active:
                active[2].append(line)
    return root


def text_outline_string(outline, depth=0):
    results = []
    for n in outline:
        results.append("    " * depth + n[0])
        for t in n[2]:
            if t.strip():
                results.append("    " * (depth + 1) + "* " + t)
        results.append(text_outline_string(n[1], depth + 1))
    return "\n".join(results)


def text_remove(text, delete_pattern):
    return text_replace(text, delete_pattern, "")


def text_replace(text, match_pattern, replace_pattern):
    return compile(match_pattern).sub(replace_pattern, text)


def text_title(text):
    return text_lines(text)[0]


def text_body(text):
    return text_join(text_lines(text)[1:])


def transform_matches(text, match_pattern, select_pattern):
    results = []
    for line in text_lines(text):
        match = compile(match_pattern).sub(select_pattern, line)
        if match != line:
            results.append(match)
    return text_join(results)


def transform_text(text, pattern, replacement):
    return compile(pattern).sub(replacement, text)


def words(text):
    return split("\s+", text)


def word_count(text):
    return len(words(text))
