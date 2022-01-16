def get_page_range(paginator, page):
    # 获取页码列表
    index = page.number - 1  # 当前页码对应的索引
    max_index = paginator.num_pages - 1  # 最大索引
    # 为了得到显示7个页码的列表，从当前索引向前数3个，向后数3个，加上本身，即7个页码
    start_index = index - 3 if index >= 3 else 0
    end_index = index + 3 if index <= max_index - 3 else max_index
    # 最后处理过的页码列表
    page_range = paginator.page_range[start_index:end_index + 1]

    return page_range


def get_year_posts(page):
    data = {}
    for post in page.object_list:
        year = post.create_time.strftime('%Y')
        if data.get(year):
            data[year].append(post)
        else:
            data[year] = [post]
    return data


def get_tutorial_posts(page):
    data = {}
    for post in page.object_list:
        tutorial = post.tutorial
        tutorial_name = tutorial.name
        if data.get(tutorial_name):
            data[tutorial_name]['post_list'].append(post)
        else:
            data[tutorial_name] = {
                'post_list': [post],
                'tutorial': tutorial
            }
    return data
