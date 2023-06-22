from django.contrib import admin
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    
    # Writer
    path("writer/", include("writer.urls")),

    # Book & Blogs
    path("", include("publish.urls")),
]
