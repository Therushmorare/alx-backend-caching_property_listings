from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from .models import Property  # assuming you have a Property model

@cache_page(60 * 15)  # Cache for 15 minutes
def property_list(request):
    properties = list(Property.objects.values())  # get all properties as dicts
    return JsonResponse(properties, safe=False)

