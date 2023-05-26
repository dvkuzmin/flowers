from django.contrib.auth.hashers import make_password
from django.db import models


class User(models.Model):
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    is_seller = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)    
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class FlowerLot(models.Model):

    FLOWER_CHOICES = (
        ('romashka', 'Ромашка'),
        ('tulipan', 'Тюльпан'),
        ('roza', 'Роза'),
        ('liliya', 'Лилия'),
    )

    SHADE_CHOICES = (
        ('Red', 'Красный'),
        ('Yellow', 'Желтый'),
        ('Blue', 'Синий'),
    )

    seller = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_seller': True})
    flower_type = models.CharField(choices=FLOWER_CHOICES, max_length=100)
    shade = models.CharField(choices=SHADE_CHOICES, max_length=100)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    display_to_buyers = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.seller.is_seller:
            return
        super().save(*args, **kwargs)

    def __str__(self):
        return self.flower_type


class SellerReview(models.Model):
    RATING_CHOICES = (
        (1, '1 звезда'),
        (2, '2 звезды'),
        (3, '3 звезды'),
        (4, '4 звезды'),
        (5, '5 звезд'),
    )

    buyer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_seller': False})
    seller = models.ForeignKey(User, related_name='buyer_reviews', on_delete=models.CASCADE, limit_choices_to={'is_seller': True})
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()


class LotReview(models.Model):
    RATING_CHOICES = (
        (1, '1 звезда'),
        (2, '2 звезды'),
        (3, '3 звезды'),
        (4, '4 звезды'),
        (5, '5 звезд'),
    )
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_seller': False})
    lot = models.ForeignKey(FlowerLot,  related_name='lot_reviews', on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()

    def __str__(self):
        return f"Отзыв от {self.buyer.name} на {self.lot.flower_type}"


class Transaction(models.Model):
    buyer = models.ForeignKey(User, related_name='buyer_transactions', on_delete=models.CASCADE, limit_choices_to={'is_seller': False})
    lot = models.ForeignKey(FlowerLot, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.buyer} купил {self.lot.flower_type}"
