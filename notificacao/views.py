from django.shortcuts import render

from .stuff.constants import HTML


def thanks(request):
    return render(request, HTML.THANKS)
