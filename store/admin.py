from django.contrib import admin
from .models import *

admin.site.register(Cliente)
admin.site.register(Producto)
admin.site.register(Orden)
admin.site.register(ArticuloOrdenado)
admin.site.register(DireccionEnvio)