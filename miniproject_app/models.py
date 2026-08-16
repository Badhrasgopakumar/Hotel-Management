from django.db import models

# Create your models here.
class RoomCategory(models.Model):
    name = models.CharField(max_length=100)
    base_price = models.DecimalField(max_digits=8,decimal_places=2)
    def __str__(self):
        return self.name

class Room(models.Model):
    room_number = models.CharField(max_length=10,unique=True,blank=True)
    category = models.ForeignKey(RoomCategory,max_length=10,on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.room_number} ({self.category.name})"

class SpecialRate(models.Model):
    room_category = models.ForeignKey(RoomCategory,on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    rate_multiplier = models.FloatField(default=1.0)
    def __str__(self):
        return f"{self.room_category.name} {self.start_date} {self.end_date}"

class Reservation(models.Model):
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    customer_name = models.CharField(max_length=100)
    total_price = models.DecimalField(max_digits=15,decimal_places=2,default=0)


