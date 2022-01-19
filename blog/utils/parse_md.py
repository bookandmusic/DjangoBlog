import copy
import os
import random
import re
import time

import mistune
from mistune import escape
from mistune.directives import DirectiveToc
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html
from pygments.util import ClassNotFound


class MarkdownToHtmlRenderer(mistune.HTMLRenderer):

    def codespan(self, text):
        if text.startswith('$') and text.endswith('$'):
            return '<span class="math">' + escape(text) + '</span>'
        return '<code>' + escape(text) + '</code>'

    def block_code(self, code, lang=None):
        try:
            lexer = get_lexer_by_name(lang, stripall=True)
        except ClassNotFound:
            lexer = None
        if lexer:
            formatter = html.HtmlFormatter()
            return highlight(code, lexer, formatter)
        return '<pre><code>' + mistune.escape(code.strip()) + '</code></pre>'


class MarkdownParse(object):
    markdown = mistune.create_markdown(
        renderer=MarkdownToHtmlRenderer(escape=False),
        plugins=['table', DirectiveToc()]
    )

    @classmethod
    def get_toc_list(cls, content):
        """
        :param content: 符合markdown语法的文件内容
        :return: 解析markdown内容，得到父子嵌套的目录列表
        """
        lines = content.split('\n')
        n = 0
        i = 0
        tree = {}
        heading = {
            'h1': None,
            'h2': None,
            'h3': None,
            'h4': None,
            'h5': None,
            'h6': None,
        }
        temp = copy.copy(heading)
        for line in lines:
            if re.search(r'```', line):
                n += 1
            if n % 2 == 0:
                tmp = re.search(r'(#+)\s+(.*)', line)
                if tmp:
                    i += 1
                    level = len(tmp.group(1))
                    title = tmp.group(2)
                    title = re.sub(r'[^\w\-_]', '', title)
                    if level == 1:
                        temp = copy.copy(heading)
                        parentId = None
                    else:
                        parentId = temp.get(f'h{level - 1}')
                    temp[f'h{level}'] = i
                    tree[i] = {'id': i, 'title': title, 'parentId': parentId, 'level': level}
        toc = []
        for key in tree:
            obj = tree[key]
            if obj['parentId'] is None:
                root = tree[obj['id']]
                toc.append(root)
            else:
                parentId = obj['parentId']
                if 'children' not in tree[parentId]:
                    tree[parentId]['children'] = []
                tree[parentId]['children'].append(tree[obj['id']])
        return toc

    @classmethod
    def toc_list2html(cls, toc_list, n=0, parent_toc_number=None):
        """
        :param toc_list: 父子嵌套格式的目录列表
        :param n: 判断是否为首次调用的标志
        :param parent_toc_number: 生成的ul嵌套列表中父类的编号
        :return: 生成的嵌套ul列表
        """
        if toc_list:
            if n == 0:
                s = '<ol class="toc">{}</ol>'
            else:
                s = '<ol class="toc-child">{}</ol>'
            tag = ''
            for index, item in enumerate(toc_list):
                id = item.get('id')
                level = item.get('level')
                title = item.get('title')
                children = item.get('children')
                toc_number = f'{parent_toc_number}.{index + 1}' if parent_toc_number else f'{index + 1}'
                toc_id = f'toc_{id}'
                temp = cls.toc_list2html(children, n + 1, toc_number)
                tag += f'<li class="toc-item toc-level-{level}"><a class="toc-link" href="#{toc_id}"><span class="toc-number">{toc_number}</span> <span class="toc-text">{title}</span></a>{temp}</li>'

            return s.format(tag)
        else:
            return ''

    @classmethod
    def markdown_to_toc_list(cls, content):
        """
        :param content: 符合markdown语法的文件内容
        :return: 生成的HTMLul嵌套的目录列表
        """
        toc_list = cls.get_toc_list(content)
        return cls.toc_list2html(toc_list)

    @classmethod
    def markdown_to_html(cls, content):
        """
        :param content: 符合markdown语法的文件内容
        :return: 生成的HTML内容
        """
        return cls.markdown(content)


class HexoBlogToSQL(object):
    @classmethod
    def get_file_list(cls, path):
        """
        :param path: 文件夹路径
        :return: 当前路径下所有的md文件
        """
        file_list = []
        if os.path.isdir(path):
            file_name_list = os.listdir(path)
            file_list = [os.path.join(path, name) for name in file_name_list if name.endswith('.md')]

        return file_list

    @classmethod
    def get_file_content(cls, filename):
        """
        :param filename: 文件名
        :return: 返回当前文件的所有内容
        """
        with open(filename, 'r') as f:
            content = f.read()
        return content

    @classmethod
    def parse_hexo_markdown(cls, content):
        """
        :param content: hexo博客下特殊格式的md文件内容
        :return: 解析之后，得到键值对形式的md文件信息，tag，title，create_time，content
        """
        meta = re.search(r'---([\s\S]+?)---', content).group(1)
        title = re.search(r'title: (.*)', meta).group(1)
        try:
            tags = re.search(r'tags:\s*\[(.*)]', meta).group(1).split(',')
        except:
            tags = re.search(r'tags:([\s\S]+?)\w+:', meta).group(1)
            if tags:
                tags = re.findall(r'-\s+(\w+)', tags)
            else:
                tags = []
        create_time = re.search(r'date: (.*)', meta).group(1)
        temp = re.search(r'---[\s\S]+?---([\s\S]+)', content).group(1)
        post = re.sub(r'<!-- more -->', '', temp)
        return {
            "title": title,
            "tags": tags,
            "create_time": create_time,
            "content": post
        }

    @classmethod
    def start(cls, path):
        from blog.models import Tag, Post

        file_list = cls.get_file_list(path)

        for file in file_list:
            content = cls.get_file_content(file)
            data = cls.parse_hexo_markdown(content)
            tags = data.pop('tags')
            data.setdefault('views', random.randint(500, 600))
            try:
                post, _ = Post.objects.get_or_create(**data)
                tag_list = [Tag.objects.get_or_create(name=tag.strip())[0].pk for tag in tags]
                post.tag.add(*tag_list)
            except Exception as e:
                print(e)
                print(data.get('title'))
