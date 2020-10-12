from django.contrib import admin

from .models import *

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

class ListingAdmin(admin.ModelAdmin):
    list_display = ("title", "starting", "user", "opened")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", 'get_title')

    def get_title(self, obj):
        return obj.listing.title

    get_title.short_description = "listing"

class BidAdmin(admin.ModelAdmin):
    list_display = ("user", "value", "get_listing")

    def get_listing(self, obj):
        return Listing.objects.get(bid=obj).title

    get_listing.short_description = "listing"

# Register your models here.
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(User)
admin.site.register(Comment,CommentAdmin)