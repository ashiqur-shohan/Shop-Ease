# shop template a jeno ei data dhorte pari tai custom context processor banacchi
# eita pore setting.py context processor a define kore dite hbe

from .models import Category

def categories(request):
    # dictonary formata a return korte hbe
    return {'categories': Category.objects.all()}