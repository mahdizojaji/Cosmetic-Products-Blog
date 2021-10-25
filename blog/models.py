from django.db import models
from django.template.defaultfilters import slugify


class Article(models.Model):
    title = models.CharField(max_length=50, unique=True)
    slug_title = models.SlugField(unique=True)
    content = models.TextField()

    image = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Slugify the title before save."""
        self.slug_title = slugify(self.title)
        super(Article, self).save(*args, **kwargs)