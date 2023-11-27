from django import template


register = template.Library()

cens_words = ['Редиска', 'Гадкий', 'Байден']

@register.filter()
def currency(value):
   """
   value: значение, к которому нужно применить фильтр
   """
   # Возвращаемое функцией значение подставится в шаблон.
   return f'{value} Р'

@register.filter()
def censor(word):
    if isinstance(word, str):
        for i in word.split():
            if i.capitalize() in cens_words:
                word = word.replace(i, i[0] + '*' * len(i))
    else:
        raise ValueError('custom_filters -> censor -> A string is expected, but a different data type has been entered')
    return word