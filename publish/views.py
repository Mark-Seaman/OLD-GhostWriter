from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.timezone import localtime
from django.views.generic import (CreateView, DeleteView, RedirectView,
                                  TemplateView, UpdateView)

from .files import read_csv_file, read_json
from .import_export import refresh_pub_from_git
from .models import Pub
from .publication import (bouncer_redirect, doc_view_context, get_host, pub_redirect,
                          select_blog_doc)
from .slides import slides_view_context


class BlogTodayView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return self.request.path.replace("today", localtime().strftime("%m-%d"))


class PubRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        x = bouncer_redirect(kwargs.get('id'))
        if x:
            return x
        host = get_host(self.request)
        pub = kwargs.get("pub")
        doc = kwargs.get("doc", 'Index.md')
        return pub_redirect(host, pub, doc)



class PubView(TemplateView):
    template_name = "pub/blog.html"

    def get_context_data(self, **kwargs):
        host = get_host(self.request)
        blog = kwargs.get("pub")
        doc = kwargs.get("doc", "Index.md")
        kwargs = select_blog_doc(host, blog, doc)
        return kwargs


class PubListView(TemplateView):

    template_name = "blog/list.html"
    model = Pub
    context_object_name = "pubs"

    def get_context_data(self, **kwargs):
        host = get_host(self.request)
        pub = self.kwargs.get('pub')
        kwargs['pubs'] = Pub.objects.filter(pub_type=pub)
        kwargs["menu"] = read_json("static/js/nav_blog.json")["menu"]
        # if Path('Documents/Shrinking-World-Pubs/setup.py').exists():
        #     exec()
        # kwargs = super().get_context_data(**kwargs)
        return kwargs


class PubDetailView(TemplateView):
    template_name = "pub/cover.html"

    def get_context_data(self, **kwargs):
        refresh_pub_from_git()
        host = get_host(self.request)
        blog = kwargs.get("pub")
        doc = kwargs.get("doc", "Index.md")
        kwargs = select_blog_doc(host, blog, doc)
        return kwargs


class PubCreateView(LoginRequiredMixin, CreateView):
    template_name = "blog/add.html"
    model = Pub
    fields = "__all__"


class PubUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "blog/edit.html"
    model = Pub
    fields = "__all__"


class PubDeleteView(LoginRequiredMixin, DeleteView):
    model = Pub
    template_name = "blog/delete.html"
    success_url = reverse_lazy("blog_list")


class RandomTweetView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        template_name = "tweet.html"

    def get_context_data(self, **kwargs):
        host = get_host(self.request)
        host = "shrinking-world.com"
        blog = "tweet"
        doc = str(kwargs.get("tweet"))
        return select_blog_doc(host, blog, doc)


class SlideShowView(TemplateView):
    template_name = 'course_slides.html'

    def get_context_data(self, **kwargs):
        return slides_view_context(**kwargs)


# class TweetView(TemplateView):
#     host = get_host(self.request)
#     host = "shrinking-world.com"
#     blog = "tweet"
#     page = "random"
#     return pub_redirect(host, blog, page)

class WorkshopRedirectView(RedirectView):
    url = '/workshop/publish/Publish-1.md'
    # def get_redirect_url(self, *args, **kwargs):
    #     host = get_host(self.request)
    #     pub = kwargs.get("pub")
    #     doc = kwargs.get("doc", 'Index.md')
    #     return pub_redirect(host, pub, doc)


class WorkshopView(TemplateView):
    template_name = "pub/blog.html"

    def get_context_data(self, **kwargs):
        # path = 'Documents/shrinking-world.com/workshop/publish/Publish-slides.md'
        doc = kwargs.get('doc', 'Publish-1.md')
        path = f'Documents/shrinking-world.com/workshop/publish/{doc}'
        kwargs = doc_view_context(path=path)
        return kwargs
