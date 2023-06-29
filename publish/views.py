from django.views.generic import RedirectView, TemplateView

from .files import read_json
from .import_export import refresh_pub_from_git
from .models import Pub
from .publication import bouncer_redirect, pub_redirect, select_blog_doc


class BouncerRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        x = bouncer_redirect(kwargs.get('id'))
        if x:
            return x
        host = self.request.get_host()
        pub = kwargs.get("pub")
        doc = kwargs.get("doc", 'Index.md')
        return pub_redirect(host, pub, doc)

class PubRedirectView(RedirectView):
    url = '/pubs/book'


class PubView(TemplateView):
    template_name = "pub/blog.html"

    def get_context_data(self, **kwargs):
        # host = get_host(self.request)
        pub = kwargs.get("pub")
        doc = kwargs.get("doc", "Index.md")
        kwargs = select_blog_doc(pub, doc)
        return kwargs


class PubLibraryView(TemplateView):
    template_name = "pub/library.html"

    def get_context_data(self, **kwargs):
        collections = [
            get_collection('textbook', 'Textbooks'),
            get_collection('book', 'Books about Life'),
            get_collection('blog', 'Blogs'),
            get_collection('private', 'Private Blogs'),
            ]
        menu = read_json("static/js/nav_blog.json")["menu"]
        kwargs = dict(collections=collections, menu=menu, site_title="Shrinking Word Publication Library", site_subtitle="All Publications")
        return kwargs

def get_collection(pub_type, title):
    return {'type': title, 'pubs': Pub.objects.filter(pub_type=pub_type)}

class PubListView(TemplateView):

    template_name = "pub/list.html"
    model = Pub
    context_object_name = "pubs"

    def get_context_data(self, **kwargs):
        pub_type = self.kwargs.get('pub_type')
        pubs = Pub.objects.filter(pub_type=pub_type)
        menu = read_json("static/js/nav_blog.json")["menu"]
        kwargs = dict(pubs=pubs, menu=menu, site_title="Shrinking Word Publication Library", site_subtitle="A Seaman's Guides")
        return kwargs

class PubDetailView(TemplateView):
    template_name = "pub/cover.html"

    def get_context_data(self, **kwargs):
        refresh_pub_from_git()
        # host = get_host(self.request)
        pub = kwargs.get("pub")
        doc = kwargs.get("doc", "Index.md")
        kwargs = select_blog_doc(pub, doc)
        return kwargs


# class PubCreateView(LoginRequiredMixin, CreateView):
#     template_name = "blog/add.html"
#     model = Pub
#     fields = "__all__"


# class PubUpdateView(LoginRequiredMixin, UpdateView):
#     template_name = "blog/edit.html"
#     model = Pub
#     fields = "__all__"


# class PubDeleteView(LoginRequiredMixin, DeleteView):
#     model = Pub
#     template_name = "blog/delete.html"
#     success_url = reverse_lazy("blog_list")


# class SlideShowView(TemplateView):
#     template_name = 'course_slides.html'

#     def get_context_data(self, **kwargs):
#         return slides_view_context(**kwargs)

