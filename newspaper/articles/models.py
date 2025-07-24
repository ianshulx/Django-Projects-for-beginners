from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class Article(models.Model):

    title = models.CharField(max_length=100)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)  # Add Date Automatically

    def __str__(self):
        return self.title


class Comment(models.Model):

    article = models.ForeignKey(
        Article,
        null=True,
        blank=False,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)

    illegal_words = ["Fuck", "Ugly", "Bad"]

    def filter_illegal_words(self, text):
        for word in self.illegal_words:
            if word.lower() in text.lower():
                masked = "*" * len(word)
                text = text.replace(word.lower(), masked).replace(
                    word.capitalize(), masked
                )
        return text

    def save(self, *args, **kwargs):
        self.content = self.filter_illegal_words(self.content)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse("article_details", kwargs={"pk": self.article.pk})
