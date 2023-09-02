from django.db import models


# Create your models here.
class New(models.Model):
    id = models.IntegerField(primary_key=True)  # news id
    source = models.TextField(blank=True)  # news source
    title = models.TextField()  # news title
    url = models.TextField()  # news url
    image_url = models.TextField(blank=True)  # news image url
    summary = models.TextField(blank=True)  # news summary
    category = models.TextField(blank=True)  # news category
    date = models.TextField()  # news date
    content = models.TextField(blank=True)  # news content

    def __str__(self):
        return self.title
