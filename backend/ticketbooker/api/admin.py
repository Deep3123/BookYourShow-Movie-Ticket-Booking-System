from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Movie)
admin.site.register(Theatre)
admin.site.register(ShowTiming)
admin.site.register(Contact_us)
admin.site.register(Payment)
admin.site.register(BookedSeat)