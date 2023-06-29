from django.urls import path

from .views import BouncerRedirectView, PubDetailView, PubLibraryView, PubListView, PubRedirectView, PubView

urlpatterns = [

    # Pub Redirect
    path("", PubRedirectView.as_view()),
    path("pubs", PubLibraryView.as_view(), name="pub_list"),
    path("pubs/<str:pub_type>", PubListView.as_view(), name="pub_list"),
    path("<int:id>", BouncerRedirectView.as_view()),

    # Display a pub document
    path("<str:pub>", PubDetailView.as_view(), name="pub_detail"),
    path("<str:pub>/<str:doc>", PubView.as_view(), name="pub"),
    
]
