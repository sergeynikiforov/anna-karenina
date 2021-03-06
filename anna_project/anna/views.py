from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.http import HttpResponse
from .models import Paragraph, Word
from .forms import QueryForm

# parser imports
from .lexer import anna_lexer
from .parser import parse


def index(request):
    """
    view for the index page of the apps
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
    print('User query: {q}'.format(q=query))
    context['query'] = query

    form = QueryForm(request.GET)
    context['form'] = form

    if len(query) > 0:
        # search in db
        try:
            paragraphs = None

            # parse the query
            tokens = anna_lexer(query)
            print('Query tokens: {t}'.format(t=tokens))
            parse_result = parse(tokens)

            if not parse_result:
                print('Parsing error')
                context['error'] = 'Parsing error'
            else:
                # get AST and print to console
                ast = parse_result.value
                print('AST: {ast}'.format(ast=ast))

                # get list from evaluated AST for paginator
                res = [i for i in ast.eval()]
                context['num_paragraphs'] = len(res)
                paginator = Paginator(res, 10)
                page = request.GET.get('page')
                try:
                    paragraphs = paginator.page(page)
                except PageNotAnInteger:
                    # If page is not an integer, deliver first page
                    paragraphs = paginator.page(1)
                except EmptyPage:
                    # If page is out of range, deliver last page of results
                    paragraphs = paginator.page(paginator.num_pages)
            context['paragraphs'] = paragraphs
        except Word.DoesNotExist:
            print('Err: obj Word does not exist')
    return render(request, 'anna/results.html', context)
