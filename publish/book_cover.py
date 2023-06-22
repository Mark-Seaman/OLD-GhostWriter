from pathlib import Path

from django.views.generic import TemplateView

from publish.files import read_json


class BookCoverView(TemplateView):
    template_name = 'book_cover.html'

    def get_context_data(self, **kwargs):
        json = Path('static/js/today.json')
        kwargs = read_json(json)
        kwargs['cover_title'] = True
        kwargs['css'] = '/static/css/shrinking-world.css'
        return kwargs
