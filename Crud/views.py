import json
import ast
import base64
from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse
from models import User, Item
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
STATIC_DIRECTORY = '/home/ubuntu/MarketPlace/Crud/static/images/'

def user_create(request):
    try:
        user_data = request.GET
        name = user_data.get('name')
        email = user_data.get('email')
        password = user_data.get('password')
        user_name = user_data.get('user_name')
        contact_no = user_data.get('contact_no')
        is_seller_str = user_data.get('is_seller')
        if is_seller_str == 'True':
            is_seller = True
        else:
            is_seller = False
        User(name=name, email=email, user_name=user_name, password=password, contact_no=contact_no, is_seller=is_seller).save()
        retval = {'success': True, 'msg': 'User with Username =  %s created successfully' %user_name}
    except Exception as e:
        retval = {'success': False, 'msg': str(e)}
    return JsonResponse(retval)

def user_update(request,username):
    try:
        user_data = request.GET
        curr_user = User.objects.get(user_name=username)
        curr_user.email = user_data.get('email',User.objects.get(user_name=username).email)
        curr_user.contact_no = user_data.get('contact_no',User.objects.get(user_name=username).contact_no)
        curr_user.contact_no = user_data.get('contact_no',User.objects.get(user_name=username).contact_no)
        is_seller_str = user_data.get('is_seller')
        if is_seller_str == 'true':
            is_seller = True
        elif is_seller_str == 'false':
            is_seller = False
            Item.objects.filter(seller=curr_user).delete()
        else:
            is_seller = User.objects.get(user_name=username).is_seller
        curr_user.is_seller=is_seller
        curr_user.save()
        retval = {'success': True, 'msg': 'User with USERNAME = %s  successfully updated' % username}
    except Exception as e:
        retval = {'success': False, 'msg': str(e)}
    return JsonResponse(retval)


def user_read(request,username):
    try:
        this_user = User.objects.filter(user_name=username)
        this_user = this_user.values()
        this_user = [entry for entry in this_user]
        this_user_map = {'success': True, 'data': this_user}
        response =  JsonResponse(this_user_map, safe=False)
    except Exception as e:
        response = JsonResponse({'success': False, 'msg': str(e)})
    return response

def user_get(request,p_key):
    try:
        this_user_name = User.objects.get(pk=p_key).name
        this_user_map = {'success': True, 'data': this_user_name}
        response =  JsonResponse(this_user_map, safe=False)
    except Exception as e:
        response = JsonResponse({'success': False, 'msg': str(e)})
    return response
    

def user_delete(request,username):
    user = User.objects.filter(user_name=username)
    if user:
        try:
            User.objects.filter(user_name=username).delete() 
            retval = {'success': True, 'msg': 'User with USERNAME = %s deleted successfully' %username}
        except Exception as e:
            retval = {'success': False, 'msg': str(e)}
    else:
        retval = {'success': False, 'msg' : 'There is no registered user with username = %s' %username}
    return JsonResponse(retval)

def item_add(request,username):
    user = User.objects.get(user_name=username)
    user_status = user.is_seller
    if user_status == True:
        try:
            item_data = request.GET
            title = item_data.get('title')
            description = item_data.get('description')
            price = item_data.get('price')
            quantity = item_data.get('quantity')
            image_uri = item_data.get('image_uri')
            seller = User.objects.get(user_name=username)
            Item(title=title, description=description, price=price, quantity=quantity, 
                 seller=seller, image_uri=image_uri).save()
            retval = {'success': True, 'msg': 'Item %s added successfully' % title}
        except Exception as e:
            retval = {'success': False, 'msg': str(e)}
    else:
        retval = {'success':False, 'msg':'You are not authorized to add items'}
    return JsonResponse(retval)

        
def item_edit(request,username,product_name):
    user = User.objects.get(user_name=username)
    user_status = user.is_seller
    if user_status == True:
        try:
            item_data = request.GET
            item = Item.objects.get(seller = user, title = product_name)
            item.description = item_data.get('description',
                    Item.objects.get(seller=user,title=product_name).description)
            item.price = item_data.get('price',Item.objects.get(seller=user,title=product_name).price)
            item.quantity =item_data.get('quantity',Item.objects.get(seller=user,title=product_name).quantity)
            item.image_uri =item_data.get('image_uri',Item.objects.get(seller=user,title=product_name).image_uri)
            item.save()
            retval = {'success': True, 'msg': 'Item %s updated successfully' % product_name}
        except Exception as e:
            retval = {'success': False, 'msg': str(e)}
    else:
        retval = {'success':False, 'msg':'You are not authorized to add items'}
    return JsonResponse(retval)

        
def item_delete(request,username,title):
    try:
        user = User.objects.get(user_name=username)
        Item.objects.filter(seller=user, title=title).delete()
        retval = {'success': True, 'msg': 'Item deleted successfully'}
    except Exception as e:
        retval = {'success': False, 'msg': str(e)}
    return JsonResponse(retval)

              

def item_detail(request,username):
    user = User.objects.filter(user_name=username)
    if user:
        User.objects.get(user_name=username)
        user_status = User.objects.get(user_name=username).is_seller
        if user_status == True:
            try:
                this_seller_items = Item.objects.filter(seller=user)
                this_seller_items = this_seller_items.values()
                this_seller_items = [entry for entry in this_seller_items]
                this_seller_items_map = {'success': True, 'data': this_seller_items}
                final_response = JsonResponse(this_seller_items_map, safe = False)
            except Exception as e:
                final_response = JsonResponse({'success': False, 'msg': str(e)})
        else:
            all_items = Item.objects.values()
            all_items = [entry for entry in all_items] 
            all_items_map = {'success': True, 'data':all_items}
            final_response = JsonResponse(all_items_map, safe=False)
    else:
        final_response = JsonResponse({'success': False, 'msg' : 'There is no registered user with username = %s' %username})
    return final_response


def user_login(request,username,password):
    user = User.objects.filter(user_name=username)
    if user:
        try:
            passwd = User.objects.get(user_name=username).password
            if passwd == password:
                pass_word_map = {'success': True, 'match' : 'True'}
                retval =  JsonResponse(pass_word_map, safe=False)
            else:
                pass_word_map = {'success': False, 'match': 'False'}
                retval =  JsonResponse(pass_word_map, safe=False)
        except Exception as e:
            retval = JsonResponse({'success': False, 'msg': str(e)})
    else:
        retval = JsonResponse({'success': False, 'msg':'User with username = %s doesnot exist' %username})
    return retval

@csrf_exempt
def save_image(request):
    if request.method == 'POST':
        print request.POST
        print request.FILES
        #file_data = request.FILES
        #print file_data
        #profile_pic = file_data['profileImage']
        image_title = request.POST.get('title')
        user_name = request.POST.get('username')
        image_base64 = request.POST.get('image')
        image_jpeg = base64.b64decode(image_base64)
        if user_name:
            image_name = user_name + '_' + image_title + '.jpg'
        else:
            image_name = image_title + '.jpg'
        file_path = STATIC_DIRECTORY + image_name
        with open(file_path, 'wb') as fh:
            fh.write(image_jpeg)
        print image_name
        retval = JsonResponse({'success' : True, 'url' : '/static/image/'+ image_name})
    else:
        print 'Wrong request sent from client'
        retval = JsonResponse({'success' : False})
    return retval

