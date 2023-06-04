import secrets
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from . paystack import PayStack

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200, null =True,blank=True)
    registered = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.full_name

class Banner(models.Model):
    title1 = models.CharField(max_length=200)
    title2 = models.CharField(max_length=200)
    title3 = models.CharField(max_length=200)
    title4 = models.CharField(max_length=200)
    title5 = models.CharField(max_length=200,null =True,blank=True)
    
    def __str__(self):
        return self.title1

class Product(models.Model):
    title =models.CharField(max_length=200)
    slug = models.SlugField(max_length=550,null=True,blank=True)
    image = models.ImageField(default='photo.jpg',null=True,blank=True)
    image_1 = models.ImageField(null=True ,blank=True)
    image_2 = models.ImageField(null=True ,blank=True)
    image_3 = models.ImageField(null=True ,blank=True)
    price = models.PositiveIntegerField()
    discount_price = models.PositiveIntegerField(null=True,blank=True)
    delivery_charge = models.PositiveIntegerField(null=True,blank=True)
    pasentage = models.CharField(max_length=20,null=True, blank=True)
    description = models.TextField()
    warranty = models.CharField(max_length=200, null=True,blank=True)
    return_policy = models.CharField(max_length=200, null=True,blank=True)
    view_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True,blank=True)
    def __str__(self):
        return self.title

    def save(self,*args,**kwargs):
        self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)

    class Meta:
        db_table = 'Products'
        managed = True
        verbose_name = 'Products'
        verbose_name_plural = 'Products'

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,null=True,blank=True)
    total = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'cart ::: {str(self.id)}'

class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,null=True,blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'cart ::: {str(self.cart.id)} - cartproduct ::: {str(self.id)}'

OREDER_STATUS = (
	('Order Received','Order Received'),
	('Order Processing','Order Processing'),
	('On the way','On the way'),
	('Order Completed','Order Completed'),
	('Order Canceled','Order Canceled'),
	('Waitng for Pickup','Waitng for Pickup'),
	('Unable to deliver without Payment','Unable to deliver without Payment'),

	)


METHOD = (
    ('Paystack','Paystack'),
    ('Payment Transfer','Payment Transfer'),
    ('Cash On Delivery','Cash On Delivery'),
    
)

class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.SET_NULL, null=True, blank=True)
    ordered_by =models.CharField(max_length=200)
    shipping_address = models.CharField(max_length=200)
    mobile = models.CharField(max_length=11)
    email = models.EmailField(null=True,blank=True)
    discount = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()
    amount = models.PositiveIntegerField()
    order_status = models.CharField(max_length=200, choices=OREDER_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=20, choices=METHOD,default='Cash On Delivery')
    payment_completed = models.BooleanField(default=False,null=True,blank=True)
    ref = models.CharField(max_length=200,null=True, blank=True)

    def __str__(self):
        return f'{self.order_status} ::: {str(self.id)}'

    # paystack code

    def save(self, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            obj_with_sm_ref = Order.objects.filter(ref=ref)
            if not obj_with_sm_ref:
                self.ref= ref
        super().save(*args, **kwargs)
    
    def amount_value(self) -> int:
        return self.amount * 100

    def verify_payment(self):
        paystack = PayStack()
        status, result = paystack.verify_payment(self.ref, self.amount)
        if status:
            if result['amount'] / 100 == self.amount:
                self.payment_completed=True
            self.save()
        if self.order_status == 'Order Completed':
            self.save()
            self.cart.delete()
        if self.payment_completed:
            return True
        return False

class Blog(models.Model):
    title = models.CharField(max_length=550)
    slug = models.SlugField(max_length=550,null=True,blank=True)
    published = models.BooleanField(default=True,null=True,blank=True)
    flag = models.BooleanField(default=False,null=True,blank=True)
    date_posted = models.DateTimeField(auto_now_add=True, null=True,blank=True)
    leadimg = models.ImageField(default='myleadimg.jpg')
    author = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)

    body = RichTextField()

    def __str__(self):
        return self.title

    def save(self,*args,**kwargs):
        self.slug = slugify(self.title)
        super(Blog, self).save(*args, **kwargs)

    class Meta:
        db_table = 'Blog'
        managed = True
        verbose_name = 'Blog'
        verbose_name_plural = 'Blog'

class Flatdiscount(models.Model):
    title = models.CharField(max_length=550)
    slug = models.SlugField(max_length=550,null=True,blank=True)
    published = models.BooleanField(default=True,null=True,blank=True)
    flag = models.BooleanField(default=False,null=True,blank=True)
    date_posted = models.DateTimeField(auto_now_add=True, null=True,blank=True)
    leadimg = models.ImageField(default='myleadimg.jpg')
    body = RichTextField()

    def __str__(self):
        return self.title

    def save(self,*args,**kwargs):
        self.slug = slugify(self.title)
        super(Flatdiscount, self).save(*args, **kwargs)

    class Meta:
        db_table = 'Flatdiscount'
        managed = True
        verbose_name = 'Flatdiscount'
        verbose_name_plural = 'Flatdiscount'

class Contact(models.Model):
    fullname = models.CharField(max_length=200)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    message = models.TextField()

    def __str__(self):
        return f'{self.fullname}'

    class Meta:
        db_table = 'contact'
        managed = True
        verbose_name = 'Contacts'
        verbose_name_plural = 'Contacts' 
             
class About(models.Model):
    title = models.CharField(max_length=550)
    leadimg = models.ImageField(default='myleadimg.jpg', null=True,blank=True)
    body = RichTextField()

    def __str__(self):
        return self.title

class Terms(models.Model):
    title = models.CharField(max_length=550)
    body = RichTextField()

    def __str__(self):
        return self.title

class Privacy(models.Model):
    title = models.CharField(max_length=550)
    body = RichTextField()

    def __str__(self):
        return self.title

class Moredetail(models.Model):
    title = models.CharField(max_length=550)
    subtitle1 = models.CharField(max_length=550)
    subbody1 = models.TextField()
    subtitle2 = models.CharField(max_length=550)
    subbody2 = models.TextField()
    subtitle3 = models.CharField(max_length=550)
    subbody3 = models.TextField()
    body = RichTextField()

    def __str__(self):
        return self.title

class Option(models.Model):
    title = models.CharField(max_length=550)
    body = models.TextField()
    
    def __str__(self):
        return self.title

class Ourteam(models.Model):
    name = models.CharField(max_length=550)
    position = models.CharField(max_length=550)
    moreimg = models.ImageField()
   
    def __str__(self):
        return self.title

class More(models.Model):
    title = models.CharField(max_length=550)
    subtitle = models.CharField(max_length=550)
    subbody = models.TextField()
    moreimg = models.ImageField()
    
    def __str__(self):
        return self.title

class Whatweoffer(models.Model):
    title = models.CharField(max_length=550)
    subtitle1 = models.CharField(max_length=550)
    subbody1 = models.TextField()
    subtitle2 = models.CharField(max_length=550)
    subbody2 = models.TextField()
    subtitle3 = models.CharField(max_length=550)
    subbody3 = models.TextField()
    subtitle4 = models.CharField(max_length=550)
    subbody4 = models.TextField()
    aboutimg = models.ImageField()
    body = RichTextField()

    def __str__(self):
        return self.title

class Howtooder(models.Model):
    title = models.CharField(max_length=550)
    subtitle1 = models.CharField(max_length=550)
    subbody1 = models.TextField()
    subtitle2 = models.CharField(max_length=550)
    subbody2 = models.TextField()
    subtitle3 = models.CharField(max_length=550)
    subbody3 = models.TextField()
    subtitle4 = models.CharField(max_length=550)
    subbody4 = models.TextField()
    subtitle5 = models.CharField(max_length=550)
    subbody5 = models.TextField()
    subtitle6 = models.CharField(max_length=550)
    subbody6 = models.TextField()

    def __str__(self):
        return self.title

class Wearethebest(models.Model):
    subtitle = models.CharField(max_length=550)
    title = models.CharField(max_length=550)
    subtitle1 = models.CharField(max_length=550)
    subbody1 = models.TextField()
    subtitle2 = models.CharField(max_length=550)
    subbody2 = models.TextField()
    subtitle3 = models.CharField(max_length=550)
    subbody3 = models.TextField()
    subtitle4 = models.CharField(max_length=550)
    subbody4 = models.TextField()

    def __str__(self):
        return self.title




