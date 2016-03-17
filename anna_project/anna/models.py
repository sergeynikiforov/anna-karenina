from django.db import models


class Paragraph(models.Model):
    text = models.TextField()


class Word(models.Model):
    word = models.TextField()
    paragraphs = models.ManyToManyField(Paragraph)
