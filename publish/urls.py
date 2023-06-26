from django.urls import path

from .views import BouncerRedirectView, PubDetailView, PubListView, PubRedirectView, PubView

urlpatterns = [

    # Publish Books & Pubs
    # path("publish/", PubListView.as_view(), name="blog_list"),
    # path("publish/add", PubCreateView.as_view(), name="blog_add"),
    # path("publish/<int:pk>/", PubUpdateView.as_view(), name="blog_edit"),
    # path("publish/<int:pk>/delete", PubDeleteView.as_view(), name="blog_delete"),

    # Slides
    # path('slides', SlideShowView.as_view(), name='slideshow'),
    # path('slides/<str:pub>/<str:doc>', SlideShowView.as_view()),

    # # Book Cover
    # path('cover', BookCoverView.as_view()),


    # Pub Redirect
    path("", PubRedirectView.as_view()),
    path("pubs", PubListView.as_view(), name="pub_list"),
    path("pubs/<str:pub_type>", PubListView.as_view(), name="pub_list"),
    path("<int:id>", BouncerRedirectView.as_view()),

    # Display a pub document
    path("<str:pub>", PubDetailView.as_view(), name="blog_detail"),
    path("<str:pub>/<str:doc>", PubView.as_view(), name="pub"),
]
