from haystack import indexes
from blog.models import Post


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    # 类名必须为需要检索的Model_name+Index，这里需要检索ArticlePost，所以创建ArticlePostIndex类
    text = indexes.CharField(document=True, use_template=True)  # 创建一个text字段

    # 对那张表进行查询
    def get_model(self):  # 重载get_model方法，必须要有！
        # 返回这个model
        return Post

    # 针对哪些数据进行查询
    def index_queryset(self, using=None):  # 重载index_..函数
        """Used when the entire index for model is updated."""
        # return self.get_model().objects.filter(updated__lte=datetime.datetime.now())
        return self.get_model().objects.all()
