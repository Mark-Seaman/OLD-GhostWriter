from django.views.generic import (CreateView, DeleteView, RedirectView,
                                  TemplateView, UpdateView)

from chatterbox.files import read_json

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