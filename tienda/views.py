from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Producto
from .carrito import Carrito
from .forms import ProductoForm

# 1. LEER (Listar todos los productos en el catálogo)
def index(request):
    productos = Producto.objects.all()
    return render(request, 'index.html', {'productos': productos})

# 2. CREAR (Registrar un nuevo producto mediante el formulario)
@login_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ProductoForm()
    return render(request, 'formulario.html', {'form': form, 'titulo': 'Añadir Producto Nuevo'})

# 3. ACTUALIZAR (Editar un producto existente buscando su ID)
@login_required
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'formulario.html', {'form': form, 'titulo': 'Editar Producto'})

# 4. ELIMINAR (Borrar un producto del catálogo de forma inmediata)
@login_required
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    producto.delete()
    return redirect('index')


#CARRITO-----------------------------------------------------------------
def ver_carrito(request):
    carrito_session = request.session.get("carrito", {})
    # Sumar el total de todos los productos en el carrito
    total_pago = sum(item["total"] for item in carrito_session.values())
    return render(request, 'carrito.html', {'total_pago': total_pago})

def agregar_al_carrito(request, producto_id):
    carrito = Carrito(request)
    producto = get_object_or_404(Producto, id=producto_id)
    carrito.agregar(producto)
    return redirect('ver_carrito')

def restar_del_carrito(request, producto_id):
    carrito = Carrito(request)
    producto = get_object_or_404(Producto, id=producto_id)
    carrito.restar(producto)
    return redirect('ver_carrito')

def eliminar_del_carrito(request, producto_id):
    carrito = Carrito(request)
    producto = get_object_or_404(Producto, id=producto_id)
    carrito.eliminar(producto)
    return redirect('ver_carrito')

def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return redirect('ver_carrito')


#PROCESAR PAGO-----------------------------------------------------------------
def procesar_pago(request):
    carrito_session = request.session.get("carrito", {})
    if not carrito_session:
        messages.error(request, "El carrito está vacío. No se puede procesar el pago.")
        return redirect('index')
    
    #Recorremos cada producto guardado en la sesión del carrito.
    for key, item in carrito_session.items():
        producto_db = get_object_or_404(Producto, id=item["producto_id"])
        # Verificamos si hay suficiente stock antes de procesar el pago
        if producto_db.stock >= item["cantidad"]:
            producto_db.stock -= item["cantidad"]
            producto_db.save()
        else:
            messages.error(request, f"No hay suficiente stock para el producto {producto_db.nombre}.")
            return redirect('ver_carrito')
    #Si todo sale bien, se vacía el carrito y se muestra un mensaje de éxito.
    carrito = Carrito(request)
    carrito.limpiar()
    messages.success(request, "Pago procesado con éxito. Gracias por su compra.")
    return redirect('index')