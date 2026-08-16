from django.contrib import admin
from . models import RoomCategory,Room,Reservation,SpecialRate
# Register your models here.
admin.site.register(RoomCategory)
admin.site.register(Room)
admin.site.register(Reservation)
admin.site.register(SpecialRate)
