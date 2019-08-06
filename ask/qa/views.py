# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_GET
from django.core.paginator import Paginator
from .models import *
from .forms import *

def test(request, *args, **kwargs):
    return HttpResponse('OK')

# {% include "_form.html" %}
def ask(request):
    if request.method == "POST":
        form = AskForm(request.POST)
        if form.is_valid():
            form._user = request.user
            question = form.save()
            url = question.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AskForm()
    return render(request, 'ask.html', {'form':form})


def question(request, id):
    # try:
    #     question = Question.objects.get(id=id)
    # except Question.DoesNotExist:
    #     raise Http404
    question = get_object_or_404(Question, id=id)
    answers = question.answer_set.order_by('added_at')
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            form._user = request.user
            _ = form.save()
            #question = form.question
            url = question.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AnswerForm(initial = {'question': question.id})
    context = {'question':question, 'answers': answers, 'form': form}
    return  render(request, 'question.html', context)


def paginate(request, qs):
    try:
        limit = int(request.GET.get('limit', 10))
    except ValueError:
        limit = 10
    if limit > 100:
        limit = 10
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404
    paginator = Paginator(qs, limit)
    try:
        page = paginator.page(page)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return paginator, page

@require_GET
def question_list(request):
    questions = Question.objects.new()
    # limit = request.GET.get('limit', 10)
    # page = request.GET.get('page', 1)
    # paginator = Paginator(questions, limit)
    # paginator.baseurl = '/?page='
    # page = paginator.page(page) #Page object
    paginator, page = paginate(request, questions)
    paginator.baseurl = '/?page='
    context = {
        'questions': page.object_list,
        #'questions': questions,
        'paginator': paginator,
        'page': page,
    }
    return  render(request, 'index.html', context)

@require_GET
def question_by_rating(request):
    questions = Question.objects.popular()
    # limit = request.GET.get('limit', 10)
    # page = request.GET.get('page', 1)
    # paginator = Paginator(questions, limit)
    # paginator.baseurl = '/?page='
    # page = paginator.page(page) #Page object
    paginator, page = paginate(request, questions)
    paginator.baseurl = '/popular/?page='
    context = {
        'questions': page.object_list,
        #'questions': questions,
        'paginator': paginator,
        'page': page,
    }
    return  render(request, 'popular.html', context)





#====================================================================
# /blog/post_text/?id=123
# def post_text(request):
#     try:
#         id = request.GET.get('id')
#         obj = Post.objects.get(pk=id) #вызов модели обращение к БД
#     except Post.DoesNotExist:
#         raise Http404
#     return HttpResponse(obj.text, content_type='text/plain')

"""
url(r'^category/(\d+)/$', 'category_view')
url(r'^(?P<pk>\d+)/$', 'post_detail')

def category_view(request, pk=None):
    # вывести все посты
    
def post_details(request, pk):
    # вывести страницу поста
     
def category_view(request, *args, **kwargs):
    pk = args[0]
    pk = kwargs['pk']
    
    
# создание ответа
response = HttpResponse("<html>Hello world</html>")
# установка заголовков
response['Age'] = 120
# установка всех параметров
response = HttpResponse(
    content = '<html><h1>Ничего</h1></html>',
    content_type = 'text/html',
    status = 404,
)   

# Специальные типы ответов
from django.http import HttpResponseRedirect, \
    HttpResponseNotFound, HttpResponseForbidden, \
    HttpResponsePermanentRedirect
    
redirect = HttpResponseRedirect("/")    # 302
redirect = HttpResponsePermanentRedirect("/")   # 301
redirect = HttpResponseNotFound()    # 404
redirect = HttpResponseForbidden()    # 403


# Получение GET и POST параметров
order = request.GET['sort'] #   опасно! не передавать напрямую значение из запроса, лучше сравнить с известным->
if order == 'rating':
    queryset = queryset.order_by('rating')
page = request.GET.get('page') or 1          # используя метод get если не найдет - None или знач.по умолч.
try:
    page = int(page)                # лучше проверять, что передали число
except ValueError:
    return HttpResponseBadRequest()

# GET и POST - объекты QueryDict
/path/?id=3&id=4&id=5  #например при выборе из списка значений
получение множественных значений
id = request.GET.get('id') # id is 5
id = request.GET.getlist('id') # id is [3,4,5]

серилизация - преобразовать обратно все параметры в строку
qs = request.GET.urlencode()
# qs is 'id=3&id=4&id=5'
"""