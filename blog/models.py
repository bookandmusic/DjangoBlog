import mistune
from mistune.directives import DirectiveToc

from django.db import models
from mdeditor.fields import MDTextField

from blog.utils.parse_md import get_toc_list, toc_list2html, HighlightRenderer, get_abstract


class Tag(models.Model):
    name = models.CharField(max_length=20, verbose_name='标签')

    class Meta:
        db_table = 'tb_tag'
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Tutorial(models.Model):
    name = models.CharField(max_length=50, verbose_name='教程名')

    class Meta:
        db_table = 'tb_tutorial'
        verbose_name = '教程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Post(models.Model):
    markdown = mistune.create_markdown(
        renderer=HighlightRenderer(),
        plugins=['table', DirectiveToc()]
    )

    create_time = models.DateTimeField(verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')
    title = models.CharField(max_length=50, verbose_name='标题')
    views = models.IntegerField(default=0, verbose_name='阅读量')
    comments = models.IntegerField(default=0, verbose_name='评论量')
    content = MDTextField(verbose_name='内容')
    tutorial = models.ForeignKey(to=Tutorial, on_delete=models.CASCADE, null=True, blank=True, verbose_name='教程')
    tag = models.ManyToManyField(to=Tag, verbose_name='标签')

    def content_to_markdown(self):
        return self.markdown(self.content)

    def content_to_toc(self):
        toc_list = get_toc_list(self.content)
        toc = toc_list2html(toc_list)
        return toc

    def content_to_abstract(self):
        return get_abstract(self.content)

    class Meta:
        db_table = 'tb_post'
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
