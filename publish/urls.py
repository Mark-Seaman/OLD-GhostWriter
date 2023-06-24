from django.urls import path

from .views import PubDetailView, PubListView, PubRedirectView, PubView

urlpatterns = [

    # Pub Redirect
    path("", PubRedirectView.as_view()),
    path("<int:id>", PubRedirectView.as_view()),

    # Publish Books & Pubs
    # path("publish/", PubListView.as_view(), name="blog_list"),
    # path("publish/add", PubCreateView.as_view(), name="blog_add"),
    # path("publish/<int:pk>/", PubUpdateView.as_view(), name="blog_edit"),
    # path("publish/<int:pk>/delete", PubDeleteView.as_view(), name="blog_delete"),
    path("publish/<str:pub>", PubListView.as_view(), name="pub_list"),

    # Slides
    # path('slides', SlideShowView.as_view(), name='slideshow'),
    # path('slides/<str:pub>/<str:doc>', SlideShowView.as_view()),

    # # Book Cover
    # path('cover', BookCoverView.as_view()),

    # Display a pub document
    path("<str:pub>", PubDetailView.as_view(), name="blog_detail"),
    path("<str:pub>/<str:doc>", PubView.as_view(), name="pub"),
]
