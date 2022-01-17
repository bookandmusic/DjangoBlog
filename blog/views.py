from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from haystack.views import SearchView

from DjangoBlog.settings import CONSTANT
from blog.models import Post, Tag, Tutorial
from blog.utils.page import get_page_range, get_year_posts, get_tutorial_posts
from blog.utils.tag_cloud import get_tags


class IndexView(View):
    @staticmethod
    def get(request):
        post_list = Post.objects.order_by('-create_time')
        paginator = Paginator(post_list, CONSTANT["page_size"])  # 得到分页器对象
        page = paginator.get_page(1)  # 得到当前页码对象
        # 最后处理过的页码列表
        page_range = get_page_range(paginator, page)
        return render(request, 'blog/index.html', context={'post_list': page, 'page_range': page_range})


class PageView(View):
    @staticmethod
    def get(request, page_number):
        if page_number == 1:
            return redirect(reverse('blog:index'))
        post_list = Post.objects.order_by('-create_time')
        paginator = Paginator(post_list, CONSTANT["page_size"])  # 得到分页器对象
        page = paginator.get_page(page_number)  # 得到当前页码对象

        # 最后处理过的页码列表
        page_range = get_page_range(paginator, page)
        return render(request, 'blog/page.html', context={'post_list': page, 'page_range': page_range})


class PostView(View):
    @staticmethod
    def get(request, pk):
        post = Post.objects.filter(pk=pk).first()
        post.views += 1
        post.save()
        previous = Post.objects.filter(pk__lt=pk).order_by("-id").first()
        next = Post.objects.filter(pk__gt=pk).order_by("id").first()
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
        data = get_tags()
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

# class AddPostView(View):
#     def get(self, request):
#         file_list = get_file_list('/Users/lsf/Documents/hexo/source/_posts')
#
#         for file in file_list:
#             content = get_content(file)
#             data = parse_markdown_content(content)
#             tags = data.pop('tags')
#             data.setdefault('views', random.randint(500, 600))
#             tag_list = [Tag.objects.get_or_create(name=tag.strip())[0].pk for tag in tags]
#             post = Post.objects.create(**data)
#             post.tag.add(*tag_list)
#
#         return HttpResponse("ok")
