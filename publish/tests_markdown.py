from probe.tests_django import DjangoTest

from markdown import markdown


# -----------------------
# Pub Data Model

class MarkdownTest(DjangoTest):

    def test_h1(self):
        text = '# Headline'
        self.assertEqual(markdown(text), '<h1>Headline</h1>')

    def test_bullet_list(self):
        text = '* Thing 1\n* Thing 2'
        x = '<ul>\n<li>Thing 1</li>\n<li>Thing 2</li>\n</ul>'
        self.assertEqual(markdown(text), x)

    def test_table(self):
        text = '''
| Column 1 | Column 2 | Column 3 | Column 4 |
|----------|----------|----------|----------|
| Row 1, Col 1 | Row 1, Col 2 | Row 1, Col 3 | Row 1, Col 4 |
| Row 2, Col 1 | Row 2, Col 2 | Row 2, Col 3 | Row 2, Col 4 |
'''
        x = '''<table>
<thead>
<tr>
<th>Column 1</th>
<th>Column 2</th>
<th>Column 3</th>
<th>Column 4</th>
</tr>
</thead>
<tbody>
<tr>
<td>Row 1, Col 1</td>
<td>Row 1, Col 2</td>
<td>Row 1, Col 3</td>
<td>Row 1, Col 4</td>
</tr>
<tr>
<td>Row 2, Col 1</td>
<td>Row 2, Col 2</td>
<td>Row 2, Col 3</td>
<td>Row 2, Col 4</td>
</tr>
</tbody>
</table>'''
        # x = markdown(text, extensions=['tables'])
        # print(x)
        self.assertEqual(markdown(text, extensions=['tables']), x)

    def test_csv(self):
        text = '# CSV Output'
        self.assertEqual(markdown(text), '<h1>CSV Output</h1>')
