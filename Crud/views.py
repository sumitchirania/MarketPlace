import json
import ast
from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse
from models import User, Item
from django.contrib.auth import authenticate
# Create your views here.

def user_create(request):
    try:
        user_data = request.GET
        name = user_data.get('name')
        email = user_data.get('email')
        password = user_data.get('password')
        user_name = user_data.get('user_name')
        is_seller_str = user_data.get('is_seller', 'false')
        if is_seller_str == 'true':
            is_seller = True
        else:
            is_seller = False
        User(name=name, email=email, user_name=user_name, password=password, is_seller=is_seller).save()
        retval = {'success': True, 'msg': 'User %s created successfully' % name}
    except Exception as e:
        retval = {'success': False, 'msg': str(e)}
    return JsonResponse(retval)

def user_update(request,username):
    try:
        user_data = request.GET
        curr_user = User.objects.get(user_name=username)
        name = user_data.get('name',curr_user)
        curr_user.name=name
        print curr_user
        print name
        curr_email = User.objects.get(user_name=username).email
        email = user_data.get('email',curr_email)
        curr_user.email=email
        print curr_user.email
        print email
        curr_password = User.objects.get(user_name=username).password
        password = user_data.get('password',curr_password)
        curr_user.password=password
        print curr_user.password
        print password
        curr_contact = User.objects.get(user_name=username).contact_no
        contact_no = user_data.get('contact_no',curr_contact)
        curr_user.contact_no = contact_no
        print curr_user.contact_no
        print contact_no
        is_seller_str = user_data.get('is_seller')
        if is_seller_str == 'true':
            is_seller = True
        elif is_seller_str == 'false':
            is_seller = False
        else:
            is_seller = User.objects.get(user_name=username).is_seller
        curr_user.is_seller=is_seller
        print curr_user.is_seller
        print is_seller
        curr_user.save()
        retval = {'success': True, 'msg': 'User with USERNAME = %s  successfully updated' % username}
    except Exception as e:
        retval = {'success': False, 'msg': str(e)}
    return JsonResponse(retval)


def user_read(request,username):
    try:
        this_user = User.objects.filter(user_name=username)
        this_user_string = serializers.serialize('json', this_user)
        this_user_json = json.loads(this_user_string)
        return JsonResponse(this_user_json, safe=False)
    except Exception as e:
        retval = {'success': False, 'msg': str(e)}
        return JsonResponse(retval)

def user_get(request,p_key):
    try:
        this_user_name = User.objects.get(pk=p_key).name
        print this_user_name
        return JsonResponse(this_user_name, safe=False)
    except Exception as e:
            retval = {'success': False, 'msg': str(e)}
            return JsonResponse(retval)
    

def user_delete(request,username):
    user = User.objects.filter(user_name=username)
    print user
    if user:
        try:
            User.objects.filter(user_name=username).delete() 
            retval = {'success': True, 'msg': 'User with USERNAME = %s deleted successfully' %username}
        except Exception as e:
            retval = {'success': False, 'msg': str(e)}
        return JsonResponse(retval)
    else:
        retval = {'success': False, 'msg' : 'There is no registered user with username = %s' %username}
        return JsonResponse(retval)

def item_add(request,username):
    user = User.objects.get(user_name=username)
    user_status = user.is_seller
    print user_status
    print type(user_status)
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
        return JsonResponse(retval)
    
    else:
        retval = {'success':False, 'msg':'You are not authorized to add items'}
        return JsonResponse(retval)

        
def item_edit(request,username,product_name):
    user = User.objects.get(user_name=username)
    user_status = user.is_seller
    if user_status == True:
        try:
            print user
            item_data = request.GET
            description = item_data.get('description',
                    Item.objects.get(seller=user,title=product_name).description)
            print description
            price = item_data.get('price',Item.objects.get(seller=user,title=product_name).price)
            print price
            quantity =item_data.get('quantity',Item.objects.get(seller=user,title=product_name).quantity)
            print quantity
            image_uri =item_data.get('image_uri',Item.objects.get(seller=user,title=product_name).image_uri)
            print image_uri
            Item.objects.get(seller=user,title=product_name).delete()    
            Item(title=product_name, description=description, price=price, quantity=quantity, 
                 seller=user, image_uri=image_uri).save()
            retval = {'success': True, 'msg': 'Item %s updated successfully' % product_name}
        except Exception as e:
            retval = {'success': False, 'msg': str(e)}
        return JsonResponse(retval)
    
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
                print user_status
                this_seller_items = Item.objects.filter(seller=user)
                this_seller_items_string = serializers.serialize('json', this_seller_items)
                this_seller_json = json.loads(this_seller_items_string)
                final_response = JsonResponse(this_seller_json, safe=False)
            except Exception as e:
                final_response = JsonResponse({'success': False, 'msg': str(e)})
        else:
            all_items = Item.objects.values()
            all_items = [entry for entry in all_items] 
            #all_items_string = serializers.serialize('json',all_items)
            #all_items_map = ast.literal_eval(all_items_string)
            all_items_map = {'success': True, 'data':all_items}
            print all_items_map
            final_response = JsonResponse(all_items_map, safe=False)
    else:
        final_response = JsonResponse({'success': False, 'msg' : 'There is no registered user with username = %s' %username})
    return final_response




def user_login(request,username,password):
    user = User.objects.filter(user_name=username)
    if user:
        try:
            passwd = {'password':User.objects.get(user_name=username).password}
            if passwd == password:
                pass_word_string = '{"match":"True"}'
                pass_word_json = json.loads(pass_word_string)
                print pass_word_json
                return JsonResponse(pass_word_json, safe=False)
            else:
                pass_word_string = '{"match":"False"}'
                pass_word_json = json.loads(pass_word_string)
                print pass_word_json
                return JsonResponse(pass_word_json, safe=False)


        except Exception as e:
            retval = {'success': False, 'msg': str(e)}
            return JsonResponse(retval)
    else:
        retval = {'success': False, 'msg':'User with username = %s doesnot exist' %username}
        return JsonResponse(retval)
