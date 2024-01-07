from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Admin site URL
# URL for handling user authentication (login, signup, etc.)
# URL for the home application
# URL for the dashboard (admin home) application


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("", include("home.urls")),
    path("adminhome/", include("dashboard.urls")),
    path("store/", include("store.urls")),
    path("user_profile/", include("userprofile.urls")),
    path("cart/", include("cart.urls")),
    path("wishlist/", include("wishlist.urls")),
]

# if settings.DEBUG:
# urlpatterns += static(settings.STATIC_URL,documents_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Uncomment the following lines only for development environment
# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
