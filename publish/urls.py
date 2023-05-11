from django.urls import path

from publish.views import DocumentListView, DocumentView, PubListView, PubView

urlpatterns = [
    # Pub Views
    path("", PubListView.as_view()),
    path("<str:pub>", DocumentListView.as_view()),

    # Document Views
    path("<str:pub>/<str:doc>", DocumentView.as_view()),
]
