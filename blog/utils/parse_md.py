import copy
import os.path
import re
import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html


class HighlightRenderer(mistune.HTMLRenderer):
    def block_code(self, code, lang=None):
        if lang:
            lexer = get_lexer_by_name(lang, stripall=True)
            formatter = html.HtmlFormatter()
            return highlight(code, lexer, formatter)
        return '<div class="codehilite"><pre><code>' + mistune.escape(code) + '</code></pre></div>'


def get_toc_list(content):
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
                title = re.sub(r'`', '', title)
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


def toc_list2html(toc_list, n=0, parent_toc_number=None):
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
            temp = toc_list2html(children, n + 1, toc_number)
            tag += f'<li class="toc-item toc-level-{level}"><a class="toc-link" href="#{toc_id}"><span class="toc-number">{toc_number}</span> <span class="toc-text">{title}</span></a>{temp}</li>'

        return s.format(tag)
    else:
        return ''


def get_content(filename):
    with open(filename, 'r') as f:
        content = f.read()

    return content


def parse_content(content):
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


def get_file_list(path):
    file_list = []
    if os.path.isdir(path):
        file_name_list = os.listdir(path)
        file_list = [os.path.join(path, name) for name in file_name_list if name.endswith('.md')]

    return file_list
