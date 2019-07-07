from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=32)
    content = models.TextField()
    pub_time = models.DateTimeField(null=True)
    objects = models.Manager()
    def __str__(self):
        return self.title