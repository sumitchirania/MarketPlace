import json
from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse
from models import User, Item
# Create your views here.

def user_detail_view(request):
    detailView_user = User.objects.all()	
    serialized_obj = serializers.serialize('json', [ detailView_user, ])
    return serialized_obj
    #json_detailViewUser = serializers.serialize('json','detailView_user')
    #return HttpResponse(json_detailViewUser, content_type='application/json')



def item_detail_view(request):
    all_items = Item.objects.all()
    all_items_string = serializers.serialize('json',all_items)
    #all_items_json = json.loads(all_items_string)
    return JsonResponse(all_items_string, safe=False)
