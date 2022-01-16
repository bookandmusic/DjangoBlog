import markdown
from django.core.paginator import Paginator
from django.db.models import Count, Max, Min
from django.shortcuts import render, redirect, reverse
from django.views import View
from haystack.views import SearchView

from DjangoBlog.settings import CONSTANT
from blog.models import Post, Tag, Tutorial
from blog.utils.page import get_page_range, get_year_posts, get_tutorial_posts
from blog.utils.tag_cloud import TagCloud


class IndexView(View):
    @staticmethod
    def get(request):
        return redirect(reverse('blog:page', kwargs={"page_number": 1}))


class PageView(View):
    @staticmethod
    def get(request, page_number):
        post_list = Post.objects.order_by('-create_time')
        paginator = Paginator(post_list, CONSTANT["page_size"])  # 得到分页器对象
        page = paginator.get_page(page_number)  # 得到当前页码对象

        # 最后处理过的页码列表
        page_range = get_page_range(paginator, page)
        return render(request, 'blog/index.html', context={'post_list': page, 'page_range': page_range})


class PostView(View):
    @staticmethod
    def get(request, pk):
        post = Post.objects.filter(pk=pk).first()
        post.views += 1
        post.save()

        previous = Post.objects.filter(pk=pk - 1).first()
        next = Post.objects.filter(pk=pk + 1).first()
        return render(request, 'blog/post.html', {'post': post, 'previous': previous, 'next': next})


class ArchivesView(View):
    @staticmethod
    def get(request, page_number):
        post_list = Post.objects.order_by('-create_time')
        paginator = Paginator(post_list, CONSTANT["page_size"])  # 得到分页器对象
        page = paginator.get_page(page_number)  # 得到当前页码对象
        # 按照年份组合文章
        data = get_year_posts(page)
        # 页码列表
        page_range = get_page_range(paginator, page)
        return render(request, 'blog/archives.html',
                      context={'post_dict': data, 'post_list': page, 'page_range': page_range})


class ArchivesYearMonthView(View):
    @staticmethod
    def get(request, year, month, page_number):
        post_list = Post.objects.filter(create_time__year=year, create_time__month=month).order_by('-create_time')
        paginator = Paginator(post_list, CONSTANT["page_size"])  # 得到分页器对象
        page = paginator.get_page(page_number)  # 得到当前页码对象
        # 按照年份组合文章
        data = get_year_posts(page)
        # 页码列表
        page_range = get_page_range(paginator, page)
        return render(request, 'blog/archives_year_month.html',
                      context={'post_dict': data, 'post_list': page, 'year': year, 'month': month,
                               'page_range': page_range, 'count': post_list.count()})


class TagView(View):
    @staticmethod
    def get(request):
        tags = Tag.objects.annotate(post_num=Count('post')).order_by('-post_num')
        result = tags.aggregate(max=Max('post_num'), min=Min('post_num'))
        tag_cloud = TagCloud(result['min'], result['min'])
        data = []
        for tag in tags:
            data.append({
                'pk': tag.pk,
                'name': tag.name,
                'font_size': tag_cloud.get_tag_font_size(tag.post_num),
                'font_color': tag_cloud.get_tag_color(tag.post_num)
            })
        return render(request, 'blog/tags.html', {'tag_list': data})


class TagPostView(View):
    @staticmethod
    def get(request, pk, page_number):
        tag = Tag.objects.filter(pk=pk).first()
        post_list = tag.post_set.order_by('-create_time')

        paginator = Paginator(post_list, CONSTANT["page_size"])  # 得到分页器对象
        page = paginator.get_page(page_number)  # 得到当前页码对象

        # 按照年份组合文章
        data = get_year_posts(page)

        # 页码列表
        page_range = get_page_range(paginator, page)
        return render(request, 'blog/tag_post.html',
                      context={'post_dict': data, 'post_list': page, 'tag': tag, 'page_range': page_range})


class TutorialsView(View):
    @staticmethod
    def get(request, page_number):
        post_list = Post.objects.filter(tutorial__isnull=False).order_by('-tutorial_id')
        paginator = Paginator(post_list, CONSTANT["page_size"])  # 得到分页器对象
        page = paginator.get_page(page_number)  # 得到当前页码对象
        # 按照教程名组合文章
        data = get_tutorial_posts(page)
        # 页码列表
        page_range = get_page_range(paginator, page)
        return render(request, 'blog/tutorials.html',
                      context={'post_dict': data, 'post_list': page,
                               'page_range': page_range, 'count': post_list.count()})


class TutorialPostView(View):
    @staticmethod
    def get(request, pk, page_number):
        tutorial = Tutorial.objects.filter(pk=pk).first()
        post_list = tutorial.post_set.order_by('-create_time')

        paginator = Paginator(post_list, CONSTANT["page_size"])  # 得到分页器对象
        page = paginator.get_page(page_number)  # 得到当前页码对象

        # 按照年份组合文章
        data = get_year_posts(page)

        # 页码列表
        page_range = get_page_range(paginator, page)
        return render(request, 'blog/tutorial_post.html',
                      context={'post_dict': data, 'post_list': page, 'tutorial': tutorial, 'page_range': page_range})


class KeyWordSearch(SearchView):
    # 用户覆盖默认的search/search.html
    template = 'blog/search.html'

    def get_context(self):
        (paginator, page) = self.build_page()
        page_range = get_page_range(paginator, page)
        context = {
            "query": self.query,
            "form": self.form,
            "page": page,
            "paginator": paginator,
            "suggestion": None,
            "page_range": page_range
        }

        if (
                hasattr(self.results, "query")
                and self.results.query.backend.include_spelling
        ):
            context["suggestion"] = self.form.get_suggestion()

        context.update(self.extra_context())

        return context
