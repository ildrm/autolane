from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


@admin.register(models.User)
class MarketplaceUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Marketplace grants", {"fields": ("roles", "contact_verified", "security_epoch")}),
    )


@admin.register(models.Audit)
class AuditAdmin(admin.ModelAdmin):
    list_display = ("occurred_at", "actor", "action", "object_type", "outcome")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


# Domain writes go through commands, not a bypassing generic model editor.
@admin.register(models.Branch, models.Taxonomy)
class ConfigurationAdmin(admin.ModelAdmin):
    pass
