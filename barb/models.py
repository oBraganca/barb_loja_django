from django.db import models


class Category(models.Model):

    CATEGORY = (
        ('tenis','Tenis'),
        ('moletom','Moletom'),
        ('Jeans','Jeans'),
    )
    
    category = models.CharField(max_length=255)

    def __str__(self):
        return self.category
        


class Gender(models.Model):
 
    GENDER = (
        ('F', 'Feminine'),
        ('M', 'Male'),
        ('U', 'Unisex')
    )

    gender = models.CharField( 
        max_length=10, 
        choices=GENDER,
    )

    def __str__(self):
        return self.gender

class product(models.Model):


    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    amount = models.IntegerField(default=False)
    upload = models.ImageField(upload_to ='uploads/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    vendido = models.IntegerField(default=False)
    


    def __str__(self):
        return self.title


