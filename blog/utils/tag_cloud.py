class TagCloud(object):
    MIN_FONT_SIZE = 1.0

    MAX_FONT_SIZE = 2.3

    FONT_SIZES = [MIN_FONT_SIZE, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, MAX_FONT_SIZE]

    COLORS = ['#ccc', "#adadad", '#8e8e8e', '#6f6f6f', '#4f4f4f', '#303030', '#111', '#000']

    def __init__(self, min_ref_count, max_ref_count):
        self.min_ref_count = min_ref_count
        self.max_ref_count = max_ref_count

        # 如果最大标签和最小标签相等, 那么认为两者的步长为 0, 所有标签取同样的 font-size.
        if max_ref_count == min_ref_count:
            self.step = 0
        else:
            self.step = (self.MAX_FONT_SIZE - self.MIN_FONT_SIZE) / (max_ref_count - min_ref_count)

    def get_tag_font_size(self, tag_ref_count):
        font_size = self.MIN_FONT_SIZE + (tag_ref_count - self.min_ref_count) * self.step

        # 上面计算出来的 font_size 并不一定刚好是 FONT_SIZES 中的某个元素, 可以能某两个元素之间的某个值

        # 因此要取最接近 FONT_SIZES 中某个元素
        font_size = min(self.FONT_SIZES, key=lambda x: abs(font_size - x))
        return font_size

    def get_tag_color(self, tag_ref_count):
        return self.COLORS[(self.FONT_SIZES.index(self.get_tag_font_size(tag_ref_count)))]
