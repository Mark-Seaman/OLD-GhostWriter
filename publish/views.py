from os import getenv
from pathlib import Path
from django.views.generic import (CreateView, DeleteView, RedirectView,
                                  TemplateView, UpdateView)

from publish.files import read_json
from chatterbox.pub_script import pub_path

class PubView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        name = kwargs.get('pub', "ghost")
        kwargs.update(read_json(f"static/js/{name}.json"))
        return kwargs
    
class DocumentView(PubView):
    template_name = "document.html"

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        return kwargs    
    

class PubListView(PubView):
    template_name = "list.html"

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs['pubs'] = list_pubs()
        return kwargs    
    

def list_pubs():
    path = Path(f'{getenv("SHRINKING_WORLD_PUBS")}')
    return [pub.name for pub in path.iterdir() if pub.is_dir()]

# pub_root = pub_path(pub)
    # pub_root = pub_path(pub)
#     pub_script = read_file(pub_root / f'AI/Script/{pub}.ai')
#     lines = text_lines(pub_script)