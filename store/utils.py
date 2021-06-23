import csv, os
from .models import *
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

def cart_data(request):
    if request.user.is_staff:
        cliente, crea_cl = Cliente.objects.get_or_create(usuario=request.user, nombre=request.user.username, email=request.user.email)
    else:
        cliente = request.user.cliente
    orden, creado = Orden.objects.get_or_create(cliente=cliente, completo=False)
    articulos = orden.articuloordenado_set.all()
    art_carrito = orden.get_cart_qty
    return {'art_carrito': art_carrito, 'orden': orden, 'articulos': articulos}

def record_csv(articulos,orden):
    di_path = os.path.realpath(__file__)[0:-8]
    for art in articulos:
        try:
            with open(f"{di_path}pedido{orden}.csv","r", encoding='utf8',newline="") as file:
                with open(f"{di_path}pedido{orden}.csv","a", encoding='utf8', newline="") as file:
                    writer = csv.writer(file, delimiter=",")
                    data = [art.producto.id,art.producto.nombre,art.producto.precio,art.cantidad,float(art.producto.precio*art.cantidad)]
                    writer.writerow(data)
        except FileNotFoundError:
            with open(f"{di_path}pedido{orden}.csv","w", encoding='utf8',newline="") as file:
                writer = csv.writer(file, delimiter=",")
                data = ["ID","ARTICULO","PRECIO","CANTIDAD","TOTAL"]
                writer.writerow(data)
                data = [art.producto.id,art.producto.nombre,art.producto.precio,art.cantidad,float(art.producto.precio*art.cantidad)]
                writer.writerow(data)
        return f"{di_path}pedido{orden}.csv", f"pedido{orden}.csv"     


def send_email(mail,csv_path,csv_file,orden,direccion_envio):
    context = {
        'mail': mail, 
        'direccion_envio': direccion_envio,
        'orden': orden, 
    }
    template = get_template('email/correo.html')
    content = template.render(context)

    email = EmailMultiAlternatives(
        f'Pedido de Bernini Nº{orden}',
        'EMAIL',
        settings.EMAIL_HOST_USER,
        [mail],
    )
    attachment = open(csv_path, 'rb')
    email.attach(csv_file,attachment.read(),'text/csv')
    email.attach_alternative(content, 'text/html')
    email.send()