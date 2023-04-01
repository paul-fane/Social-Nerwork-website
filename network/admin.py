from django.contrib import admin
from .models import User, Tweet, Relationship, Comments, images

# Register your models here.
admin.site.register(User)
admin.site.register(Tweet)
admin.site.register(Relationship)
admin.site.register(Comments)
admin.site.register(images)