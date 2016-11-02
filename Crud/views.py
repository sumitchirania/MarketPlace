import json
import ast
import base64
from django.shortcuts import render
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
        if str(e).startswith('invalid literal for int() with base 10'):
            message = "Contact No. Invalid, Enter a Valid one"
        elif str(e).startswith('(1062, "Duplicate entry'):
            message = "Username already taken.Enter a new username"
        else:
            message = str(e)
        retval = {'success': False, 'msg': message}
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
        this_user_name = User.objects.get(pk=p_key).user_name
        this_user_contact = User.objects.get(pk=p_key).contact_no
        this_user_map = {'success': True, 'name': this_user_name, 'contact': this_user_contact}
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
            if str(e).startswith('invalid literal for int() with base 10'):
                message = "Quantity and Price has to be a number. Check again"
            elif str(e).startswith('(1062, "Duplicate entry'):
                message = "Item with title = %s already listed. Try another title" %title
            else:
                message = str(e)
            retval = {'success': False, 'msg': message}
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
            desc = item_data.get('description')
            status = bool(desc)
            if status:
                item.description = item_data.get('description')
            else:
                item.description = item.description
            price = item_data.get('price')
            status = bool(price)
            if status:
                item.price = item_data.get('price')
            else:
                item.price = item.price
            quan = item_data.get('quantity')
            status = bool(quan)
            if status:
                item.quantity = item_data.get('quantity')
            else:
                item.quantity = item.quantity
            img = item_data.get('image_uri')
            print img
            if img == "alpha/beta":
                item.image_uri = item.image_uri
            else:
                item.image_uri =item_data.get('image_uri')
            item.save()
            retval = {'success': True, 'msg': 'Item %s updated successfully' % product_name}
        except Exception as e:
            retval = {'success': False, 'msg': str(e)}
    else:
        retval = {'success':False, 'msg':'You are not authorized to add items'}
    return JsonResponse(retval)

        
def item_delete(request,username,title):
    user = User.objects.get(user_name=username)
    user_status = user.is_seller
    if user_status == True:
        try:
            item = Item.objects.get(title=title)
            if item is not None:
                Item.objects.filter(title=title).delete()
                retval = {'success': True, 'msg': 'Item deleted successfully'}
            else:
                retval = {'success': False, 'msg': 'Item doesnot exist'}
        except Exception as e:
            retval = {'success': False, 'msg': str(e)}
    else:
        retval = {'success':False, 'msg': 'Not Authorized to delete Items'}
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
                response = JsonResponse(this_seller_items_map, safe = False)
            except Exception as e:
                response = JsonResponse({'success': False, 'msg': str(e)})
        else:
            all_items = Item.objects.values()
            all_items = [entry for entry in all_items] 
            all_items_map = {'success': True, 'data':all_items}
            response = JsonResponse(all_items_map, safe=False)
    else:
        response = JsonResponse({'success': False, 'msg' : 'No registered user with username = %s' %username})
    return response


def user_login(request,username,password):
    user = User.objects.filter(user_name=username)
    if user:
        try:
            passwd = User.objects.get(user_name=username).password
            if passwd == password:
                pass_word_map = {'success': True, 'match' : 'True', 'msg' : 'Login Success'}
                retval =  JsonResponse(pass_word_map, safe=False)
            else:
                pass_word_map = {'success': True, 'match': 'False', 'msg': 'Login failed'}
                retval =  JsonResponse(pass_word_map, safe=False)
        except Exception as e:
            retval = JsonResponse({'success': False, 'match': 'False', 'msg': str(e)})
    else:
        retval = JsonResponse({'success': False, 'match': 'False', 'msg':'User with username = %s doesnot exist' %username})
    return retval

@csrf_exempt
def save_image(request):
    if request.method == 'POST':
        print request.POST
        print request.FILES
        #file_data = request.FILES
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
        retval = JsonResponse({'success' : True, 'url' : '/static/images/'+ image_name})
    else:
        print 'Wrong request sent from client'
        retval = JsonResponse({'success' : False})
    return retval

def forgot_password(request,username):
    user_data = request.GET
    user = User.objects.filter(user_name=username)
    if user:
        try:
            curr_user = User.objects.get(user_name=username)
            if user_data.get('email') == curr_user.email:
                curr_user.password = user_data.get('password')
                curr_user.save()
                retval =  JsonResponse({'success': True, 'msg': 'Password Updated'})
            else:
                retval =  JsonResponse({'success': False, 'msg': 'Email linked to User is incorrect'})
        except Exception as e:
            retval = JsonResponse({'success': False, 'msg': str(e)})
    else:
        retval = JsonResponse({'success': False, 'msg':'User with username = %s doesnot exist' %username})
    return retval

