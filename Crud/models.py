from __future__ import unicode_literals

from django.db import models

from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class User(models.Model):
    name 	= models.CharField(max_length = 50)
    email 	= models.EmailField(max_length = 50)
    user_name   = models.CharField(max_length = 50)
    password 	= models.CharField(max_length = 20)
    contact_no  = models.IntegerField(blank = True, null = True)
    is_seller = models.BooleanField(default = False)
    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Item(models.Model):
    title 	= models.CharField(max_length = 50)
    description = models.CharField(max_length = 200)
    price 	= models.IntegerField()
    quantity 	= models.IntegerField()
    image_uri 	= models.ImageField()
    seller	= models.ForeignKey(User, on_delete = models.CASCADE)
    def __str__(self):
	return self.title