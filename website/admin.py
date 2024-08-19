from django.contrib import admin
from .models import companies,users, notices, placedrecord, reviews

# Register your models here.
admin.site.register(companies)
admin.site.register(users)
admin.site.register(notices)
admin.site.register(placedrecord)
admin.site.register(reviews)