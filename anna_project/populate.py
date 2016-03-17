# set django config
import os
import sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'anna_project.settings')

import re

import django
django.setup()

# import models
from anna.models import Word, Paragraph


def populate(filepath):
    """
    Populates Paragraph and Word databases from a text file located at `filepath`

    filepath: str representing a path to a text file
    return: None
    """

    # store all words
    all_words = set([])
    counter = 0

    # start reading from file
    with open(filepath) as f:

        # clear all tables
        Word.objects.all().delete()
        Paragraph.objects.all().delete()

        # regex to get words from the string
        reg_obj = re.compile(r'\w+\-\w+|\w+')

        for line in f:
            # create paragraph
            cur_papagraph = Paragraph.objects.create(text=line)
            cur_papagraph.save()
            counter += 1

            # get words from the line
            word_list = [w.lower() for w in reg_obj.findall(line)]

            # add words to DB
            for word in word_list:
                obj, created = Word.objects.get_or_create(word=word)
                obj.paragraphs.add(cur_papagraph)
                all_words.add(word)

    print('{} words were added to the Word table\n{} paragraphs were added to the Paragraph table'.format(len(all_words), counter))
    return


def main():
    if len(sys.argv) != 2:
        print('usage: python3 populate.py file_path')
        return 1
    else:
        try:
            print('Starting populate.py...')
            populate(sys.argv[1])
        except FileNotFoundError as e:
            print(e)
            return 2
        else:
            return 0


if __name__ == '__main__':
    sys.exit(main())
