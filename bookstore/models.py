from django.db import models
from django.db.models.fields.related import ForeignKey

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=190,null=True)
    def __str__(self):
        return self.name


class Customer(models.Model):
    name =models.CharField(max_length=190,null=True) 
    email = models.CharField(max_length=190,null=True)
    phone = models.CharField(max_length=190,null=True)
    age = models.CharField(max_length=190,null=True)
    date_created = models.DateTimeField(auto_now_add=True, null = True)


    def __str__(self):
        return self.name

class Book(models.Model):
    CATEGORY = (
        ('Classics.','Classics.'),
        ('Comic Book','Comic Book'),
        ('Fantasy','Fantasy'),
        ('Horror.','Horror.'),
    )
    name = models.CharField(max_length=190,null=True)
    author  = models.CharField(max_length=190,null=True)
    price  = models.FloatField(null=True)
    categorey = models.CharField(max_length=190,null=True,choices=CATEGORY)
    tags = models.ManyToManyField(Tag)
    description = models.CharField(max_length=200,null=True)
    date_created = models.DateTimeField(auto_now_add=True, null = True)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS = (
        ('Pending','Pending'),
        ('Delivered','Delivered'),
        ('in Progress','in Progress'),
        ('Out of Oreder','Out of Order'),
    )
    customer = models.ForeignKey(Customer, null = True,on_delete=models.SET_NULL)
    book = models.ForeignKey(Book, null = True,on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag)
    date_created = models.DateTimeField(auto_now_add=True, null = True)
    status = models.CharField(max_length=200,null = True,choices = STATUS)
    # def __str__(self):
    #     return self.customer