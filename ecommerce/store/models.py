from django.db import models
from django.contrib.auth.models import User

# Клиент
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.name

# Товар
class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    digital = models.BooleanField(default=False, blank=False, null=True) # Логическое поле модели по умолчанию каждый предмет будет физ.предметом
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageUrl(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

# Заказ - Корзина
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True) # У клиента может быть несколько заказов
    data_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)  # Если complete явл. ложным, то это открытая корзина и можно добавлять товары туда. Статус корзины
    transaction_id = models.CharField(max_length=100, null=True)  # id транзакции

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

# Это элемент в Корзине. В Корзине может быть несколько элементов заказа
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)            
    data_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

# Модель-доставки
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True) # Инфо. о клиенте
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)       # Инфо. о заказе
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state= models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)             # Почтовый индекс
    data_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address