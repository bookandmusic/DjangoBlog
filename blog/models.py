from django.db import models
from mdeditor.fields import MDTextField
from django.db.models import signals

from blog.utils.parse_md import MarkdownParse


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
    create_time = models.DateTimeField(verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')
    title = models.CharField(max_length=50, verbose_name='标题')
    views = models.IntegerField(default=0, verbose_name='阅读量')
    content = MDTextField(verbose_name='内容')
    tutorial = models.ForeignKey(to=Tutorial, on_delete=models.CASCADE, null=True, blank=True, verbose_name='教程')
    tag = models.ManyToManyField(to=Tag, verbose_name='标签')

    html = models.TextField(blank=True, null=True, verbose_name='HTML')
    toc = models.TextField(blank=True, null=True, verbose_name='目录')

    class Meta:
        db_table = 'tb_post'
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    # @classmethod
    # def update_post(cls, instance, *args, **kwargs):
    #     instance.html = MarkdownParse.markdown_to_html(instance.content)
    #     instance.toc = MarkdownParse.markdown_to_toc_list(instance.content)

    @classmethod
    def save_old_content(cls, instance, *args, **kwargs):
        instance.old_content = instance.content

    @classmethod
    def parse_content(cls, instance, created, *args, **kwargs):
        if created or instance.old_content != instance.content:
            instance.html = MarkdownParse.markdown_to_html(instance.content)
            instance.toc = MarkdownParse.markdown_to_toc_list(instance.content)
            instance.old_content = instance.content
            instance.save()


# signals.pre_save.connect(Post.update_post, sender=Post)
signals.post_init.connect(Post.save_old_content, sender=Post)
signals.post_save.connect(Post.parse_content, sender=Post)
