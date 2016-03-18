from django.db import models


class Paragraph(models.Model):
    text = models.TextField()

    def __str__(self):
        return "Paragraph " + str(self.id)


class Word(models.Model):
    word = models.CharField(max_length=100, db_index=True)
    paragraphs = models.ManyToManyField(Paragraph)

    def __str__(self):
        return self.word
