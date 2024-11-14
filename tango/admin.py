from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from tango.models import Category, Occupation, Place, Activity, Member, Opinion


admin.site.register(Category)
admin.site.register(Occupation)
admin.site.register(Place)
admin.site.register(Activity)
admin.site.register(Opinion)

@admin.register(Member)
class MemberAdmin(UserAdmin):
    list_display = (UserAdmin.list_display + ("phone_number", "get_occupations"))
    fieldsets = (UserAdmin.fieldsets
                 + (("Additional info", {"fields": ("phone_number", "occupations")}),))

    def get_occupations(self, obj):
        return ", ".join([occupation.name for occupation in obj.occupations.all()])
    get_occupations.short_description = "Occupations"
