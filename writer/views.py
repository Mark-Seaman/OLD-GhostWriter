from django.views.generic import RedirectView, TemplateView

from publish.files import read_json

from .ai import pub_ai
from .pub_dev import pub_edit, pub_path, doc_view_data


# class PubView(TemplateView):
#     template_name = "index.html"

#     def get_context_data(self, **kwargs):
#         return kwargs


class DocumentView(TemplateView):
    template_name = "document.html"

    def get_context_data(self, **kwargs):
        # pub_js = f"{pub_path(kwargs.get('pub','GhostWriter'))}/pub.json"
        # kwargs.update(read_json('static/js/ghost.json'))
        # kwargs.update(read_json(pub_js))
        kwargs.update(doc_view_data(**kwargs))
        return kwargs


class DocumentEditView(RedirectView):

    def get_redirect_url(self, **kwargs):
        return pub_edit(**kwargs)


class ApplyAiView(RedirectView):

    def get_redirect_url(self, **kwargs):
        return pub_ai(**kwargs)
