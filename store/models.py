from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    usuario = models.OneToOneField(User,on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=200, null=True)
    precio = models.DecimalField(max_digits=7, decimal_places=2)
    digital = models.BooleanField(default=False, null=True,blank=False)
    imagen = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.nombre

    @property
    def imagenURL(self):
        try:
            url = self.imagen.url
        except:
            url = ''
        return url

class Orden(models.Model):        
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, blank=True, null= True)
    fecha_orden = models.DateTimeField(auto_now_add=True)
    completo = models.BooleanField(default=False, null=True,blank=False)
    transaccion_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def envio(self):
        envio = False
        art_ordenados = self.articuloordenado_set.all()
        for art in art_ordenados:
            if art.producto.digital == False:
                envio = True
        return envio

    @property
    def get_cart_total(self):
        art_ordenados = self.articuloordenado_set.all()
        total = sum([articulo.get_total for articulo in art_ordenados])
        return total

    @property
    def get_cart_qty(self):
        art_ordenados = self.articuloordenado_set.all()
        total = sum([articulo.cantidad for articulo in art_ordenados])
        return total

class ArticuloOrdenado(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, blank=True, null=True)
    orden = models.ForeignKey(Orden, on_delete=models.SET_NULL, blank=True, null=True)
    cantidad = models.IntegerField(default=0, null=True, blank=True)
    fecha_orden = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_total(self):
        total = self.producto.precio * self.cantidad
        return total

class DireccionEnvio(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, blank=True, null=True)
    orden = models.ForeignKey(Orden, on_delete= models.SET_NULL, blank=True, null=True)
    direccion = models.CharField(max_length=200, null=True)
    ciudad = models.CharField(max_length=200, null=True)
    estado = models.CharField(max_length=200, null=True)
    codigo_postal = models.CharField(max_length=200, null=True)
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.direccion