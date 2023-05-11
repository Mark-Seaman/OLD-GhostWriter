from django.views.generic import (TemplateView)

from chatterbox.pub_script import pub_path

from .files import read_json
from .pub import doc_html, doc_list, doc_text, list_pubs

class PubView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        pub_js = f"{pub_path(kwargs.get('pub','GhostWriter'))}/pub.json" 
        kwargs.update(read_json('static/js/ghost.json'))
        kwargs.update(read_json(pub_js))
        return kwargs
    
    
class DocumentView(PubView):
    template_name = "document.html"

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        doc = f"{kwargs['pub']}/{kwargs['doc']}"
        kwargs['text'] = doc_html(doc)
        return kwargs    
    

class DocumentListView(PubView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs['docs'] = doc_list(kwargs['pub'])
        return kwargs    
    

class PubListView(PubView):
    template_name = "list.html"

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs['pubs'] = list_pubs()
        return kwargs    
  