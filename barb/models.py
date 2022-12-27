from django.db import models


class category(models.Model):
    name = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    modifed_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
        


class gender(models.Model):
    name = models.CharField(max_length=200)
    desc = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    modifed_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class discount(models.Model):
    name = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    discount_decimal = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modifed_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class product(models.Model):
    name = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    SKU = models.CharField(max_length=255)
    price = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    product_category_id = models.ForeignKey(category, on_delete=models.CASCADE)
    product_gender_id = models.ForeignKey(gender, on_delete=models.CASCADE)
    discount_id = models.ForeignKey(discount, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modifed_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name


