from django.contrib import admin
from blog.models import *


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'create_time', 'update_time')  # 指定要显示的字段
    search_fields = ('title',)  # 指定要搜索的字段，将会出现一个搜索框让管理员搜索关键词
    list_filter = ('create_time',)  # 指定列表过滤器，右边将会出现一个快捷的日期过滤选项，
    # 以方便开发人员快速地定位到想要的数据，同样你也可以指定非日期型类型的字段

    # fields = ('title', 'content', 'tutorial', 'tag', 'views', 'create_time', 'is_delete')  # 自定义编辑表单，在编辑表单的时候 显示哪些字段，显示的属性
    # 分组表单
    fieldsets = (
        ('文章内容', {'fields': ('title', 'content')}),
        ('基本信息', {'fields': ('tutorial', 'tag', 'views', 'create_time', 'is_delete')}),
    )


# Register your models here.
admin.site.register(Tutorial)
admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
