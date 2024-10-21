from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import City, Region, Parent, Child, ChildLevels


class CityAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


class RegionAdmin(admin.ModelAdmin):
    list_display = ("name", "city")
    search_fields = ("name", "city__name")


class ParentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "region", "paid")
    search_fields = ("name", "region__name")
    list_filter = (
        "paid",
        "region",
    )


class ChildAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "gender", "age", "parent")
    search_fields = ("name", "parent__name")
    list_filter = ("gender", "parent")


class ChildLevelsAdmin(admin.ModelAdmin):
    list_display = ("child", "level", "stars", "complete")
    search_fields = ("child__name", "level__name")
    list_filter = ("stars", "complete")


admin.site.register(City, CityAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Parent, ParentAdmin)
admin.site.register(Child, ChildAdmin)
admin.site.register(ChildLevels, ChildLevelsAdmin)
admin.site.register(get_user_model())
