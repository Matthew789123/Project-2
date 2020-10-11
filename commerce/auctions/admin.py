from django.contrib import admin

from .models import *

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

class ListingAdmin(admin.ModelAdmin):
    list_display = ("title", "starting", "user")

# Register your models here.
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid)
admin.site.register(Category, CategoryAdmin)
admin.site.register(User)
admin.site.register(Watchlist)
admin.site.register(Comment)