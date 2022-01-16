from django.db.models import Count
from django.db.models.functions import TruncMonth

from blog.models import Post, Tag, Tutorial
from siteinfo.models import BlogSiteInfo


def site_info_context(request):
    """
    父模板中的公共数据
    :param request:
    :return:
    """
    site_info = BlogSiteInfo.objects.first()
    posts = Post.objects.count()
    tags = Tag.objects.count()
    tutorials = Tutorial.objects.count()
    recent_posts = Post.objects.order_by('-create_time')[:10]

    archive_list = Post.objects.annotate(month=TruncMonth('create_time')).values('month').annotate(
        total=Count('id')).values('month', 'total').order_by('-month')[:10]
    tag_list = Tag.objects.all()

    if site_info:
        context = {
            'site_name': site_info.site_name,
            'blog_title': site_info.blog_title,
            'url': site_info.url,
            'background': site_info.background,
            'author': site_info.author,
            'image': site_info.image,
            'icp': site_info.ICP,
            'copyright': site_info.copyright,
            'posts': posts,
            'tags': tags,
            'tutorials': tutorials,
            'visitors': site_info.visitors,
            'views': site_info.views,
            'update_time': site_info.update_time.strftime('%Y/%m/%d'),
            'recent_posts': recent_posts,
            'archive_list': archive_list,
            'tag_list': tag_list,
        }
    else:
        context = {
            'site_name': "DjangoBlog",
            'blog_title': "DjangoBlog",
            'url': 'https://bookandmusic.cn',
            'background': 'https://gitee.com/bookandmusic/imgs/raw/master/uPic/2022/01/A1.jpg',
            'author': "佚名",
            'image': 'https://gitee.com/bookandmusic/imgs/raw/master/uPic/2020%2005/me.gif',
            'icp': '',
            'copyright': '佚名',
            'posts': 0,
            'categories': 0,
            'tags': 0,
            'tutorials': 0,
            'visitors': 0,
            'views': 0,
            'update_time': '2022/01/01',
            'recent_posts': recent_posts,
            'archive_list': archive_list,
            'tag_list': tag_list,
        }
    return context
