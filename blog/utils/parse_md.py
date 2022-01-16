import os.path
import re


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
