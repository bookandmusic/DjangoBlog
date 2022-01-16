import mistune
from mistune.directives import DirectiveToc
from mistune.plugins import plugin_table, plugin_url, plugin_task_lists, plugin_def_list, plugin_abbr

from django import template

register = template.Library()


@register.filter(name='markdown2html')
def markdown2html(source):
    renderer = mistune.HTMLRenderer()
    md = mistune.create_markdown(renderer, plugins=[
        plugin_table,
        plugin_url,
        plugin_task_lists,
        plugin_def_list,
        plugin_abbr,
        DirectiveToc()
    ])
    return md(source)
