from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from .models import Property  # assuming you have a Property model
from .utils import get_all_properties

@cache_page(60 * 15)  # Cache for 15 minutes
def property_list(request):
    properties = list(Property.objects.values())  # get all properties as dicts
    return JsonResponse(properties, safe=False)

def property_list(request):
    """
    View to list all properties using cached queryset
    """
    properties = get_all_properties()
    return render(request, 'properties/property_list.html', {'properties': properties})

