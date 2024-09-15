from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser,UserProducts, Education, Transaction, Facility, Coupon, CouponRedemption
from base.register.models import EventRegistration
from base.register.models import EventCard, CastImage

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('username','email', 'phone', 'password','house','area','landmark','pincode','town','state','country', 'user_image','user_choices','total_coins', 'total_recycle')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','email', 'phone', 'password1', 'password2','house','area','landmark','pincode','town','state','country','user_image','user_choices', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)



admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProducts)
admin.site.register(Education)
admin.site.register(EventCard)
admin.site.register(EventRegistration)
admin.site.register(CastImage)
admin.site.register(Transaction)
admin.site.register(Facility)
admin.site.register(Coupon)
admin.site.register(CouponRedemption)