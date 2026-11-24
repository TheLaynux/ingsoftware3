from django.shortcuts import render,redirect
from paneladmin.forms import ProductoForm
from paneladmin.models import Producto, Perfil, DetalleVenta, Venta
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import get_object_or_404
from django.contrib import messages


def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('lista_productos')

        return render(
            request,
            'login.html',
            {'error': 'Credenciales incorrectas'}
        )

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# Create your views here.
def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm()

    return render(request, 'agregar_producto.html', {
        'form': form
    })

def lista_productos(request):
    productos = Producto.objects.all()

    return render(request, 'lista_productos.html', {
        'productos': productos
    })

@login_required
def agregar_carrito(request, producto_id):

    producto = Producto.objects.get(id=producto_id)

    carrito = request.session.get('carrito', {})

    if str(producto_id) in carrito:
        carrito[str(producto_id)] += 1
    else:
        carrito[str(producto_id)] = 1

    request.session['carrito'] = carrito

    messages.success(
        request,
        f'{producto.nombre} agregado al carrito'
    )

    return redirect('lista_productos')

@login_required
def ver_carrito(request):

    carrito = request.session.get('carrito', {})

    productos = []
    total = 0

    for producto_id, cantidad in carrito.items():

        producto = Producto.objects.get(id=producto_id)

        subtotal = producto.precio * cantidad

        total += subtotal

        productos.append({
            'producto': producto,
            'cantidad': cantidad,
            'subtotal': subtotal
        })

    return render(
        request,
        'productos/carrito.html',
        {
            'productos': productos,
            'total': total
        }
    )

@login_required
def confirmar_venta(request):

    carrito = request.session.get('carrito', {})

    if not carrito:
        return redirect('ver_carrito')

    venta = Venta.objects.create(
        vendedor=request.user
    )

    total = 0

    for producto_id, cantidad in carrito.items():

        producto = Producto.objects.get(id=producto_id)

        subtotal = producto.precio * cantidad

        DetalleVenta.objects.create(
            venta=venta,
            producto=producto,
            cantidad=cantidad,
            subtotal=subtotal
        )

        producto.stock -= cantidad
        producto.save()

        total += subtotal

    venta.total = total
    venta.save()

    request.session['carrito'] = {}

    return redirect('lista_productos')

@login_required
def eliminar_del_carrito(request, producto_id):

    carrito = request.session.get('carrito', {})

    if str(producto_id) in carrito:
        del carrito[str(producto_id)]

    request.session['carrito'] = carrito

    return redirect('ver_carrito')


@login_required
def vaciar_carrito(request):

    request.session['carrito'] = {}

    return redirect('ver_carrito')


@login_required
def editar_producto(request, id):

    if request.user.perfil.rol != 'administrador':
        return redirect('lista_productos')

    producto = get_object_or_404(
        Producto,
        id=id
    )

    if request.method == 'POST':

        form = ProductoForm(
            request.POST,
            request.FILES,
            instance=producto
        )

        if form.is_valid():
            form.save()
            return redirect('lista_productos')

    else:
        form = ProductoForm(instance=producto)

    return render(
        request,
        'editar_producto.html',
        {'form': form}
    )

@login_required
def eliminar_producto(request, id):

    if request.user.perfil.rol != 'administrador':
        return redirect('lista_productos')

    producto = get_object_or_404(
        Producto,
        id=id
    )

    producto.delete()

    return redirect('lista_productos')

@login_required
def lista_ventas(request):

    ventas = Venta.objects.all().order_by('-fecha')

    return render(
        request,
        'lista_ventas.html',
        {
            'ventas': ventas
        }
    )