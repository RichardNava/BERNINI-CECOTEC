import json
import datetime
from django.contrib.auth.models import User, Group
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from rest_framework import viewsets
from rest_framework import permissions
from .forms import CreateUserForm
from .models import *
from .utils import *
from .serializers import *

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('store')
        else:
            messages.info(request, 'Nombre de Usuario o Contraseña incorrectas.')
            context = {}
            return render(request, 'login/login.html',context)    
    context = {}
    return render(request, 'login/login.html',context)

def register_user(request):
    if request.user.is_authenticated:
        return redirect('store')
    else:   
        form = CreateUserForm
        if request.method == 'POST':
            form= CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = User.objects.filter().last()        
                username = form.cleaned_data.get('username')
                email = form.cleaned_data.get('email')
                Cliente.objects.create(usuario=user,nombre=username,email=email)
                messages.success(request, "Cuenta creada por " + username)

    context = {'form': form}
    return render(request, 'login/register.html',context)

def logout_user(request):
    logout(request)
    return redirect('/')

def store(request):
    data = cart_data(request)
    art_carrito = data['art_carrito']

    productos = Producto.objects.all()
    context = {'productos': productos, 'art_carrito':art_carrito}
    return render(request, 'store/store.html', context)

def cart(request):
    data = cart_data(request)
    art_carrito = data['art_carrito']
    orden = data['orden']
    articulos = data['articulos']

    context = {'articulos':articulos, 'orden':orden, 'art_carrito': art_carrito} 
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = cart_data(request)
    art_carrito = data['art_carrito']
    orden = data['orden']
    articulos = data['articulos']

    context = {'articulos': articulos, 'orden': orden, 'art_carrito': art_carrito}
    return render(request, 'store/checkout.html', context)

def update_item(request):
    data = json.loads(request.body)
    producto_id = data['productoId']
    accion = data['action']

    cliente = request.user.cliente
    producto = Producto.objects.get(id=producto_id)
    orden, creado = Orden.objects.get_or_create(cliente=cliente, completo=False)
    art_ordenado, creado = ArticuloOrdenado.objects.get_or_create(orden=orden, producto=producto)

    if accion == 'add':
        art_ordenado.cantidad = (art_ordenado.cantidad+1)
    elif accion == 'remove':
        art_ordenado.cantidad = (art_ordenado.cantidad-1)
    
    art_ordenado.save()

    if art_ordenado.cantidad <= 0:
        art_ordenado.delete()
    
    return JsonResponse('El articulo fue añadido', safe= False)

def procesar_orden(request):
    data = json.loads(request.body)
    transaccion_id = datetime.datetime.now().timestamp()
    pedido = cart_data(request)
    orden = pedido['orden']
    cliente = request.user.cliente
    articulos = ArticuloOrdenado.objects.filter(orden=orden)
    csv_path, csv_file = record_csv(articulos,orden)
    total = float(data['form']['total'])
    orden.transaccion_id = transaccion_id

    if total == float(orden.get_cart_total):
        orden.completo = True
    orden.save()

    if orden.envio == True:
        direccion_envio = DireccionEnvio.objects.create(
            cliente=cliente,
            orden=orden,
            direccion=data['shipping']['address'],
            ciudad=data['shipping']['city'],
            estado=data['shipping']['state'],
            codigo_postal= data['shipping']['zipcode'],
        )
        send_email(cliente.email,csv_path,csv_file,orden,direccion_envio)
    
    return JsonResponse('¡Pedido solicitado!', safe=False)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [permissions.IsAuthenticated]

class OrdenViewSet(viewsets.ModelViewSet):
    queryset = Orden.objects.all()
    serializer_class = OrdenSerializer
    permission_classes = [permissions.IsAuthenticated]

class ArticuloOrdenadoViewSet(viewsets.ModelViewSet):
    queryset = ArticuloOrdenado.objects.all()
    serializer_class = ArticuloOrdenadoSerializer
    permission_classes = [permissions.IsAuthenticated]

class DireccionEnvioViewSet(viewsets.ModelViewSet):
    queryset = DireccionEnvio.objects.all()
    serializer_class = DireccionEnvioSerializer
    permission_classes = [permissions.IsAuthenticated]