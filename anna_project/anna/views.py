from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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
    context['query'] = query
    form = QueryForm(request.GET)
    context['form'] = form
    if len(query) > 0:
        # search in db
        try:
            paragraphs = None
            obj = Word.objects.get(word=query.lower())
            par_list =  obj.paragraphs.all() #Paragraph.objects.order_by('id')[:5]
            paginator = Paginator(par_list, 10)
            page = request.GET.get('page')
            try:
                paragraphs = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                paragraphs = paginator.page(1)
            except EmptyPage:
                # If page is out of range, deliver last page of results
                paragraphs = paginator.page(paginator.num_pages)
            context['paragraphs'] = paragraphs
        except Word.DoesNotExist:
            print('Err: obj Word("{q}") does not exist'.format(q=query))
    return render(request, 'anna/results.html', context)
