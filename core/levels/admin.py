from django.contrib import admin
from .models import TrainingMainCategory, Level, Images
from django.utils.html import format_html


class ImagesInline(admin.TabularInline):
    model = Images
    extra = 1  # How many extra forms to display by default
    fields = ["image", "image_preview"]
    readonly_fields = ["image_preview"]

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 100px; height: auto;" />', obj.image
            )
        return "No Image"

    image_preview.short_description = "Image Preview"


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ["text", "category", "paid", "voice", "video"]
    list_filter = ["paid", "category"]
    search_fields = ["text", "category__name"]

    # Display Images inline
    inlines = [ImagesInline]

    fieldsets = (
        (None, {"fields": ("category", "paid", "text")}),
        ("Media", {"fields": ("voice", "video")}),
    )


@admin.register(TrainingMainCategory)
class TrainingMainCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "age_min", "age_max"]
    search_fields = ["name"]
    list_filter = ["age_min", "age_max"]
    ordering = ["name"]

    fieldsets = (
        (None, {"fields": ("name",)}),
        ("Age Limits", {"fields": ("age_min", "age_max")}),
    )


@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    list_display = ["level", "image", "image_preview"]
    search_fields = ["level__text"]
    list_filter = ["level__category"]

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 100px; height: auto;" />', obj.image
            )
        return "No Image"

    image_preview.short_description = "Image Preview"
