from django.contrib import admin

# Register your models here.

from .models import Album,Artist,Song

admin.site.register([Artist,Album,Song])