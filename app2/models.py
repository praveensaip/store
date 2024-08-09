from django.db import models

class Store(models.Model):
    storename = models.CharField(max_length=100)

    def __str__(self):
        return self.storename

class Snack(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class StoreSnack(models.Model):
    store = models.ForeignKey(Store, related_name='store_snacks', on_delete=models.CASCADE)
    snack = models.ForeignKey(Snack, on_delete=models.CASCADE)
    qty = models.IntegerField()
    rate = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.store.storename} - {self.snack.name}"
    
class Product(models.Model):
    productname = models.CharField(max_length=200)
    productcode = models.CharField(max_length=100)
    cost = models.IntegerField()

    def __str__(self):
        return self.productname
class Supremarket(models.Model):
    storename = models.CharField(max_length=100,null=True)
    invoiceno = models.CharField(max_length=100,null=True)
    date = models.DateField( null=True)
    product = models.ForeignKey(Product,related_name="product",on_delete=models.CASCADE)
    pieces = models.IntegerField(null=True)
    units = models.CharField(max_length=100,null=True)
    amount = models.IntegerField(null=True)
    
    def __str__(self):
        return self.storename


class Producting(models.Model):
    productname = models.CharField(max_length=100)
    productcode = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.productname
class demo(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()

    def __str__(self):
        return self.name


    
    
    

    
    

