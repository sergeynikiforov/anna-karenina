from django.db import models


class Paragraph(models.Model):
    text = models.TextField()

    def __str__(self):
        return "Paragraph " + str(self.id)


class Word(models.Model):
    word = models.TextField()
    paragraphs = models.ManyToManyField(Paragraph)

    def __str__(self):
        return self.word
