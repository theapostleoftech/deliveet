from django import template

register = template.Library()


@register.filter
def get_initials(full_name):
    """
    This functions takes in a first name
    and a last name and returns the initials
    :param full_name:
    :return: Returns the first letter of the first and last name
    """
    names = full_name.split()
    if len(names) >= 2:
        return (names[0][0] + names[-1][0]).upper()
    elif len(names) == 1:
        return names[0][0].upper()
    else:
        return ""
