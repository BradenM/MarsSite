"""mars URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.urls import path, include, re_path
from django.conf.urls.static import static

urlpatterns = [

    # Admin
    path('admin/manage/', include('staff.urls', namespace='staff')),
    path('admin/', admin.site.urls),

    # Home
    path('', include('repair.urls', namespace="repair")),

    # Accounts

    path('accounts/', include('allauth.urls')),
    path('account/tracker/', include('tracker.urls', namespace="tracker")),
    path('account/', include('users.urls', namespace="users")),

    # Store
    path('store/', include('store.urls')),

    # Payments
    path('payments/', include("pinax.stripe.urls")),
    path('pay/', include('billing.urls'))
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(f"/{settings.STATIC_URL}",
                      document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        re_path(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
