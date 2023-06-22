from django.urls import path

from .book_cover import BookCoverView
from .views import (BlogTodayView, PubCreateView, PubDeleteView, PubDetailView,
                    PubListView, PubRedirectView, PubUpdateView, PubView,
                    SlideShowView, WorkshopRedirectView, WorkshopView)

urlpatterns = [
    #
    # Pub Redirect
    path("", PubRedirectView.as_view()),
    path("<int:id>", PubRedirectView.as_view()),
    path("book/", PubRedirectView.as_view(), name="book_list"),
    path("book/<str:pub>", PubRedirectView.as_view()),
    path("book/<str:pub>/<str:doc>", PubRedirectView.as_view()),
    path("blog/", PubRedirectView.as_view(), name="blog_list"),
    path("blog/<str:pub>", PubRedirectView.as_view()),
    path("blog/<str:pub>/<str:doc>", PubRedirectView.as_view()),
    #
    # Publish Books & Pubs
    path("publish/", PubListView.as_view(), name="blog_list"),
    path("publish/add", PubCreateView.as_view(), name="blog_add"),
    path("publish/<int:pk>/", PubUpdateView.as_view(), name="blog_edit"),
    path("publish/<int:pk>/delete", PubDeleteView.as_view(), name="blog_delete"),
    path("publish/<str:pub>", PubListView.as_view(), name="blog_detail"),
    #
    # Slides
    path('slides', SlideShowView.as_view(), name='slideshow'),
    path('slides/<str:pub>/<str:doc>', SlideShowView.as_view()),
    #
    # Workshop
    path('workshop/<str:pub>', WorkshopRedirectView.as_view()),
    path('workshop/<str:pub>/<str:doc>', WorkshopView.as_view()),
    # Book Cover
    path('cover', BookCoverView.as_view()),
    #
    # Today's Article
    path("<str:pub>/today", BlogTodayView.as_view()),
    #
    # Random
    #   path("blog/random", BlogRandomView.as_view()),
    #   path("blog/<str:blog>/random", BlogRandomView.as_view()),
    #   path("blog/<str:blog>/<str:dir>/random", BlogRandomView.as_view()),
    #
    # Tweet
    #   path("<str:pub>/<int:tweet>", TweetView.as_view()),
    #   path("tweet", RandomTweetView.as_view()),
    #
    # Display a pub document
    # path("<str:pub>", PubRedirectView.as_view()),
    # path('cellbiology', CellBiology.as_view()),
    path("<str:pub>", PubDetailView.as_view(), name="blog_detail"),
    path("<str:pub>/<str:doc>", PubView.as_view(), name="pub"),
]
