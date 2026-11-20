from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from store.views import product_list, product_detail, add_to_cart, cart_detail, checkout

# Create a simple view for referrals on the fly
from django.shortcuts import render

def referral_view(request):
    return render(request, 'store/referral.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', product_list, name='product_list'),
    path('product/<int:pk>/', product_detail, name='product_detail'),
    path('add-to-cart/<int:variant_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_detail, name='cart_detail'),
    path('checkout/', checkout, name='checkout'),
    path('referrals/', referral_view, name='referrals'), # <-- NEW REFERRAL ROUTE
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)