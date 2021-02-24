from django.contrib import admin
from .models import Announcement


class AnnouncementAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "author",
        "published",
        "created_at",
        "updated_at",
        "expiry",
    )

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()


admin.site.register(Announcement, AnnouncementAdmin)
