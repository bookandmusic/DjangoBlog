from django.db import models


# Create your models here.
class BlogSiteInfo(models.Model):
    site_name = models.CharField(max_length=50, verbose_name='站点名称')
    blog_title = models.CharField(max_length=50, verbose_name='首页标题')
    url = models.URLField(verbose_name='站点网址')
    background = models.URLField(verbose_name='背景图片')

    image = models.URLField(verbose_name='头像链接')
    author = models.CharField(max_length=50, verbose_name='作者名称')

    ICP = models.CharField(max_length=20, verbose_name='ICP备案号')
    copyright = models.CharField(max_length=20, verbose_name='版权')

    visitors = models.IntegerField(default=0, verbose_name='访客数')
    views = models.IntegerField(default=0, verbose_name='访问量')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'tb_site_info'
        verbose_name = '站点信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.site_name
