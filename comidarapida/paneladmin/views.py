from django.shortcuts import render,redirect
from paneladmin.forms import ProductoForm
from paneladmin.models import Producto

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