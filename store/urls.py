from django.urls import path
from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views



urlpatterns = [
    path('store/',login_required(views.store), name='store'),
    path('cart/', login_required(views.cart), name='cart'),
    path('checkout/', login_required(views.checkout), name='checkout'),
    path('update_item/', login_required(views.update_item), name='update_item'),
    path('procesar_orden/', login_required(views.procesar_orden), name='procesar_orden'),
    path('', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', login_required(views.logout_user), name='logout'),
]