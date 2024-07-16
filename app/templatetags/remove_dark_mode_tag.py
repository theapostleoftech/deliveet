from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.tag(name="process_all_classes")
def do_process_all_classes(parser, token):
    nodelist = parser.parse(('endprocess_all_classes',))
    parser.delete_first_token()
    return ProcessAllClassesNode(nodelist)


class ProcessAllClassesNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        output = self.nodelist.render(context)
        process_classes = context['process_classes']
        return mark_safe(process_classes(output))
