from django.contrib import admin

from .models import FlashCard


@admin.register(FlashCard)
class FlashCardAdmin(admin.ModelAdmin):
    list_display = ("id", "question", "answer", "created_at")
    search_fields = ("question", "answer")
