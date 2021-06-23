from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from store import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'clientes', views.ClienteViewSet)
router.register(r'productos', views.ProductoViewSet)
router.register(r'ordenes', views.OrdenViewSet)
router.register(r'articulos_ordenados', views.ArticuloOrdenadoViewSet)
router.register(r'direccion_envio', views.DireccionEnvioViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='api-rest')),
    path('', include('store.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)