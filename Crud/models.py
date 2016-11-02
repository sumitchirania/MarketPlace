from __future__ import unicode_literals
from django.core.validators import MaxValueValidator
from django.db import models

from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class User(models.Model):
    name 	= models.CharField(max_length = 50)
    email 	= models.EmailField(max_length = 50, unique = True)
    user_name   = models.CharField(max_length = 50, unique = True)
    password 	= models.CharField(max_length = 20)
<<<<<<< HEAD
    contact_no  = models.IntegerField(null = True)
    is_seller = models.BooleanField(default = False)
=======
    contact_no  = models.BigIntegerField(null = True,  validators=[MaxValueValidator(9999999999)])
    is_seller   = models.BooleanField(default = False)
>>>>>>> 64aacf93901d4242c6b4eb6f45b630d7e617ea07
    def __str__(self):
        return str(self.name)


@python_2_unicode_compatible
class Item(models.Model):
    title 	= models.CharField(max_length = 50, unique = True)
    description = models.CharField(max_length = 200)
    price 	= models.IntegerField()
    quantity 	= models.IntegerField()
    image_uri 	= models.URLField()
    seller	= models.ForeignKey(User, on_delete = models.CASCADE)
    def __str__(self):
	return str(self.title)

