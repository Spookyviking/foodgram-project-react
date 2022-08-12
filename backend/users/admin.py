from django.contrib import admin

from users.models import Follower, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = (
        "first_name",
        "last_name",
        "username",
        "email",
        "role",
        "blocked",
    )
    list_display = (
        "pk",
        "first_name",
        "last_name",
        "username",
        "email",
        "role",
        "is_staff",
        "is_blocked",
    )
    list_display_links = (
        "pk",
        "username",
    )
    list_filter = (
        "username",
        "email",
        ("is_staff", admin.BooleanFieldListFilter),
    )
    search_fields = (
        "first_name",
        "last_name",
        "username",
    )
    empty_value_display = "-пусто-"
    list_editable = ("role",)
    list_per_page = 10
    list_max_show_all = 100
    readonly_fields = ("id",)

    def is_blocked(self, obj):
        return obj.is_blocked

    is_blocked.boolean = True


@admin.register(Follower)
class FollowAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "user",
        "author",
    )
    search_fields = ("author",)
