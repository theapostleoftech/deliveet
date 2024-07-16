import re


def remove_dark_classes(value):
    classes = value.split()
    filtered_classes = [cls for cls in classes if not cls.startswith('dark:')]
    return ' '.join(filtered_classes)


def dark_mode_processor(request):
    def process_classes(content):
        pattern = r'class="([^"]*)"'
        return re.sub(pattern, lambda m: f'class="{remove_dark_classes(m.group(1))}"', content)

    return {
        'process_classes': process_classes,
    }
