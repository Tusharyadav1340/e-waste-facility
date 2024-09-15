app_name = 'base'

from django.urls import path
from base.api.views import CustomUserView, BlacklistTokenView, CustomUserDetailView, CustomUserProductView,CustomUserProductSellerView, LoginView, EducationView, TransactionsView, FacilityView, CouponView, CouponRedemptionView, user_transactions
from base.register.views import *
from django.conf import settings
from django.conf.urls.static import static
from base.register import views

urlpatterns = [
    path('register/', CustomUserView.as_view(), name='register'),
    path('details/', CustomUserDetailView.as_view(), name='userdetail'),
    path('products/', CustomUserProductView.as_view(), name='products'),
    path('products/seller/', CustomUserProductSellerView.as_view(), name='seller'),
    path('logout/blacklist/', BlacklistTokenView.as_view(), name='blacklist'),
    path('login/', LoginView.as_view(), name='token_login'),
    # path('logout/', LogoutView.as_view(), name='token_login'),
    path('education/', EducationView.as_view(), name='education'),
    path('events/', EventCardView.as_view(), name='eventcard'),
    path('events_register/', EventRegistrationView.as_view(), name='events_register'),
    path('get_events/', views.get_event, name='get_events'),
    path('get_transactions/', TransactionsView.as_view(), name='get_transactions'),
    path('user_transactions/', user_transactions, name='user_transactions'),
    path('facility/', FacilityView.as_view(), name='facility'),
    path('reg/', views.register, name='register'),
    path('coupons/', CouponView.as_view(), name='coupons'),
    path('claim_coupon/', CouponRedemptionView.as_view(), name='clain_coupon'),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL ,document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL ,document_root = settings.MEDIA_ROOT)