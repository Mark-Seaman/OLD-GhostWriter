from django.urls import path

from publish.views import DocumentView, PubView

urlpatterns = [
    # Pub Views
    path("", DocumentView.as_view()),
    path("<str:pub>", DocumentView.as_view()),

    # Document Views
    path("<str:pub>/<str:doc>", DocumentView.as_view()),
]
