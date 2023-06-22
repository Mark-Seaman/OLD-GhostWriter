from django.db import models
from django.urls import reverse_lazy


class Pub(models.Model):
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(default="None", null=True, blank=True)
    doc_path = models.CharField(max_length=200, default="Documents")
    image_path = models.CharField(max_length=200, null=True)
    css = models.CharField(max_length=200, null=True)
    domain = models.URLField(max_length=200, null=True)
    url = models.URLField(max_length=200)
    logo = models.CharField(max_length=200, null=True)
    words = models.IntegerField(default=0)
    cover_image = models.CharField(max_length=200, null=True, blank=True)
    menu = models.TextField(null=True, blank=True)
    pub_type = models.CharField(max_length=20, default="blog")
    auto_remove = models.BooleanField(default=False)
    auto_contents = models.BooleanField(default=False)
    auto_index = models.BooleanField(default=False)
    index_folders = models.BooleanField(default=False)
    index_months = models.BooleanField(default=False)
    simple_index = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.title}"

    def get_absolute_url(self):
        return reverse_lazy("blog_detail", args=[str(self.id)])


class Content(models.Model):
    blog = models.ForeignKey("Pub", on_delete=models.CASCADE, editable=False)
    order = models.IntegerField()
    title = models.CharField(max_length=200, default="No title")
    doctype = models.CharField(max_length=200)
    path = models.CharField(max_length=200, null=True)
    folder = models.IntegerField(default=0)
    words = models.IntegerField(default=0)
    retain_object = models.BooleanField(default=False)

    def __str__(self):
        doc = self.path.replace(self.blog.doc_path, "")[1:]
        if self.folder:
            return f"{doc},{self.folder},{self.order}"
        else:
            return f"{doc},{self.order}"
