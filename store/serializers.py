from django.contrib.auth.models import User, Group
from .models import *
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class ClienteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cliente
        fields = ['usuario', 'nombre', 'email']

class ProductoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Producto
        fields = ['nombre', 'precio', 'digital', 'imagen']

    def create(self, validated_data):
        return Producto.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.precio = validated_data.get('precio', instance.precio)
        instance.digital = validated_data.get('digital', instance.digital)
        instance.imagen = validated_data.get('imagen', instance.imagen)
        instance.save()
        return instance

class OrdenSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Orden
        fields = ['cliente', 'fecha_orden', 'completo', 'transaccion_id']

class ArticuloOrdenadoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ArticuloOrdenado
        fields = ['producto', 'orden', 'cantidad', 'fecha_orden']

class DireccionEnvioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DireccionEnvio
        fields = ['cliente', 'orden', 'direccion', 'ciudad', 'estado', 'codigo_postal', 'fecha_agreagdo']