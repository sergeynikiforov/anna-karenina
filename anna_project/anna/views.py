from django.shortcuts import render
from django.http import HttpResponse
from .models import Paragraph, Word
from .forms import QueryForm


def index(request):
    """
    view for the index page of the app
    """
    form = QueryForm()
    context = {'form': form}
    return render(request, 'anna/index.html', context)


def searchResults(request):
    """
    view for the results page
    """
    context = {}
    query = request.GET.get('query')
    form = QueryForm(request.GET)
    context['form'] = form
    if len(query) > 0:
        # search in db
        try:
            obj = Word.objects.get(word=query.lower())
            par_list =  obj.paragraphs #Paragraph.objects.order_by('id')[:5]
            context['paragraphs'] = par_list
        except Word.DoesNotExist:
            print('Err: obj Word("{q}") does not exist'.format(q=query))

    context['query'] = query

    return render(request, 'anna/results.html', context)
