from django.contrib.gis import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.safestring import mark_safe

from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import *


# admin.site.register(WorldBorder, admin.OSMGeoAdmin)
admin.site.unregister(Group)


@admin.register(Report)
class ReportAdmin(admin.OSMGeoAdmin):
    fields = ['get_image', 'image', 'vehicles', 'convoy', 'comment', 'civilians', 'time', 'location', 'user', 'verified']
    readonly_fields = ('time', 'user', 'get_image')
    search_fields = ['vehicles', 'comment', 'user']
    list_filter = ['civilians', 'verified']
    list_editable = ['convoy', 'verified']
    list_display = ['id', 'get_image', 'vehicles', 'convoy', 'civilians', 'verified', 'time']

    @admin.display(description='Image Preview')
    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="150">')
        else:
            return '–'


@admin.register(Convoy)
class ConvoyAdmin(admin.OSMGeoAdmin):
    fields = ['updated', 'tracking']
    readonly_fields = ('updated',)
    list_filter = ['tracking']
    list_editable = ['tracking']
    list_display = ['id', 'count_reports', 'updated', 'tracking']

    def count_reports(self, obj):
        result = Report.objects.filter(convoy=obj).count()
        return result

    count_reports.short_description = "Reports"


User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ['email', 'first_name', 'last_name', 'admin', 'staff']
    list_editable = ['admin', 'staff']
    list_filter = ['admin', 'staff']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Information', {'fields': ('first_name', 'last_name',)}),
        ('Permissions', {'fields': ('admin', 'staff')}),
        ('Location', {'fields': ('last_location',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password_2')}
         ),
    )
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['email']
    filter_horizontal = ()
