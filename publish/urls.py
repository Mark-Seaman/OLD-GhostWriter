from django.urls import path

from publish.views import DocumentView, PubView

urlpatterns = [
    # Pub Views
    path("", PubView.as_view()),
    path("<str:pub>", PubView.as_view()),

    # Document Views
    path("<str:pub>/<str:doc>", DocumentView.as_view()),
]
