from django.shortcuts import render
from .models import Article
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.utils import timezone


def index(request):
    article_list = Article.objects.all()
    top_list = article_list.order_by('-pub_time')[:5]
    # 每页显示3条记录
    paginator = Paginator(article_list, 3)
    page_num = paginator.num_pages

    # 根据GET获取页数参数
    if request.method == 'GET':
        # 处理删除
        delete_id = request.GET.get('delete_id')
        if delete_id:
            Article.objects.filter(pk=delete_id).delete()
        # 处理分页跳转
        page = request.GET.get('page')
        if page:
            current_page = int(page)
        else:
            current_page = 1
        try:
            # 获取某一页的内容
            articles = paginator.page(current_page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except InvalidPage:
            return HttpResponse('找不到网页的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            articles = paginator.page(page_num)
        if articles.has_next():
            next_page = current_page + 1
        else:
            next_page = current_page
        if articles.has_previous():
            previous_page = current_page - 1
        else:
            previous_page = current_page

    return render(request,
                  'blog/index.html',
                  {'articles': articles,
                   'page_num': range(1, page_num + 1),
                   'current_page': current_page,
                   'previous_page': previous_page,
                   'next_page': next_page,
                   'top_list': top_list
                   }
                  )


def detail(request, article_id):
    if request.method == 'POST':
        article_id = request.POST['article_id']
        title = request.POST.get('title', 'TITLE')
        content = request.POST['content']
        if str(article_id) != '0':
            article = Article.objects.get(pk=article_id)
            article.title = title
            article.content = content
            article.pub_time = timezone.now()
            article.save()
        else:
            article = Article.objects.create(title=title, content=content, pub_time=timezone.now())

    else:
        article = Article.objects.get(pk=article_id)
    content_list = article.content.split('\n')
    previous_article = Article.objects.filter(id__lt=article.id).order_by('-id')[:1]
    next_article = Article.objects.filter(id__gt=article.id).order_by('id')[:1]

    if previous_article:
        previous_article = previous_article[0]
    else:
        previous_article = None
    if next_article:
        next_article = next_article[0]
    else:
        next_article = None

    return render(request,
                  'blog/detail.html',
                  {
                      'article': article,
                      'content_list': content_list,
                      'previous_article': previous_article,
                      'next_article': next_article
                  })


def edit(request, article_id):
    if str(article_id) == '0':
        article = None
    else:
        article = Article.objects.get(pk=article_id)
    return render(request, 'blog/edit.html', {'article': article})
