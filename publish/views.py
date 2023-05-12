from django.views.generic import (TemplateView)
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy

from .files import read_json
from .pub import pub_path, pub_view_data
from .models import Document

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
        kwargs.update(pub_view_data(**kwargs))
        return kwargs    
    

class DocumentEditView(UpdateView):
    model = Document
    fields = ['pub', 'chapter']
    template_name = 'edit.html'

    def get_success_url(self):
        return super().get_success_url(f'/GhostWriter/Chapter1')


class DocumentAddView(CreateView):
    model = Document
    fields = ['pub', 'chapter', 'doc']
    template_name = 'edit.html'

    def get_success_url(self):
        return super().get_success_url(f'/GhostWriter/Chapter1')

# class DocumentListView(PubView):
#     template_name = "index.html"

#     def get_context_data(self, **kwargs):
#         kwargs = super().get_context_data(**kwargs)
#         kwargs.update(pub_view_data(**kwargs))

#         # kwargs['docs'] = doc_list(kwargs['pub'])
#         return kwargs    
    

# class PubListView(PubView):
#     template_name = "list.html"

#     def get_context_data(self, **kwargs):
#         kwargs = super().get_context_data(**kwargs)
#         kwargs.update(pub_view_data(**kwargs))

#         # kwargs['pubs'] = list_pubs()
#         return kwargs    
  
