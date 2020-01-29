from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from braces.views import SuperuserRequiredMixin, LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import NuevaCategoriaForm, NuevoProductoForm, NuevoProductoForm2, NuevaEntradaForm, NuevaEntradaForm2, NuevaSalidaForm, NuevaSalidaForm2
from .models import Categoria, Producto, Movimiento



@login_required
def home(request):
    return render(request, "core/home.html")

class NuevaCategoria(SuperuserRequiredMixin, CreateView):
    model = Categoria
    form_class = NuevaCategoriaForm
    success_url = reverse_lazy('core:indice', args=[0])


#Productos

class NuevoProducto(LoginRequiredMixin, CreateView):
    model = Producto
    form_class = NuevoProductoForm
    success_url = reverse_lazy('core:indice', args=[0])
    
    def get_initial(self):
        return {
            'paquetes':0,
            'empaquetado':True,
        }
    
class NuevoProducto2(LoginRequiredMixin, CreateView):
    model = Producto
    form_class = NuevoProductoForm2
    success_url = reverse_lazy('core:indice', args=[0])
    
    
class EditarProducto(LoginRequiredMixin, UpdateView):
    model = Producto
    form_class = NuevoProductoForm
    success_url = reverse_lazy('core:indice', args=[0])
    
    def get_initial(self):
        return {
            'paquetes':0,
            'empaquetado':True,
        }
    
class EditarProducto2(LoginRequiredMixin, UpdateView):
    model = Producto
    form_class = NuevoProductoForm2
    success_url = reverse_lazy('core:indice', args=[0])
    
    
class EliminarProducto(LoginRequiredMixin, DeleteView):
    model = Producto
    template_name = 'core/producto_delete.html'
    success_url = reverse_lazy('core:indice', args=[0])
 
    
@login_required
def Indice(request, categoria):
    filtro = categoria
    categorias = Categoria.objects.all()
    
    if filtro == 0:
        productos = Producto.objects.all()
    else:
        productos = Producto.objects.filter(categoria = filtro)
        
    return render(request, 'core/indice.html', {'categorias': categorias, 'productos': productos, 'filtro':filtro})


@login_required
def Productos(request, categoria):
    filtro = categoria
    categorias = Categoria.objects.all()
    
    if filtro == 0:
        productos = Producto.objects.all()
    else:
        productos = Producto.objects.filter(categoria = filtro)
        
    return render(request, 'core/productos.html', {'categorias': categorias, 'productos': productos, 'filtro':filtro})


@login_required
def Productos2(request, categoria):
    filtro = categoria
    categorias = Categoria.objects.all()
    
    if filtro == 0:
        productos = Producto.objects.all()
    else:
        productos = Producto.objects.filter(categoria = filtro)
        
    return render(request, 'core/productos2.html', {'categorias': categorias, 'productos': productos, 'filtro':filtro})


#Entradas

@login_required
def NuevaEntrada(request, pk):
    producto = Producto.objects.get(id = pk)
    
    if request.method == 'POST':
        form = NuevaEntradaForm(request.POST)
        if form.is_valid():
            form.save()
            
            movimiento = Movimiento.objects.latest('id')
            producto = Producto.objects.get(id = pk)
            
            if movimiento.medida:
                movimiento.unidades = movimiento.cantidad
                movimiento.paquetes = movimiento.cantidad/producto.unidadPaquete
                movimiento.unidadesSueltas = movimiento.cantidad % producto.unidadPaquete
                movimiento.save()
                
                producto.existencias = producto.existencias + movimiento.unidades
                producto.save()
                
                movimiento.existencias = producto.existencias
                movimiento.save()
                
                producto.paquetes = producto.existencias / producto.unidadPaquete
                producto.sueltas = producto.existencias % producto.unidadPaquete
                producto.save()
                
            else:
                movimiento.paquetes = movimiento.cantidad
                movimiento.unidades = movimiento.cantidad * producto.unidadPaquete
                movimiento.save()
                
                producto.existencias = producto.existencias + movimiento.unidades
                producto.save()
                
                movimiento.existencias = producto.existencias
                movimiento.save()
                
                producto.paquetes = producto.paquetes + movimiento.paquetes
                producto.sueltas = producto.existencias % producto.unidadPaquete
                producto.save()
                
                
            return redirect('core:productos', 0)
    else:
        form = NuevaEntradaForm()
        form.initial['producto'] = pk
    
    return render(request, 'core/entrada_form.html', {'form':form, 'producto':producto})


@login_required
def NuevaEntrada2(request, pk):
    producto = Producto.objects.get(id = pk)
    
    if request.method == 'POST':
        form = NuevaEntradaForm2(request.POST)
        if form.is_valid():
            form.save()
            
            movimiento = Movimiento.objects.latest('id')
            producto = Producto.objects.get(id = pk)
            

            movimiento.unidades = movimiento.cantidad
            movimiento.unidadesSueltas = movimiento.cantidad
            movimiento.save()
            
            producto.existencias = producto.existencias + movimiento.unidades
            producto.sueltas = producto.sueltas + movimiento.unidadesSueltas
            producto.save()
            
            movimiento.existencias = producto.existencias
            movimiento.save()
                
            return redirect('core:productos', 0)
    else:
        form = NuevaEntradaForm2()
        form.initial['producto'] = pk
    
    return render(request, 'core/entrada_form.html', {'form':form, 'producto':producto})



#Salidas

@login_required
def NuevaSalida(request, pk):
    producto = Producto.objects.get(id = pk)
    
    if request.method == 'POST':
        form = NuevaSalidaForm(request.POST)
        if form.is_valid():
            form.save()
            
            movimiento = Movimiento.objects.latest('id')
            producto = Producto.objects.get(id = pk)
            
            if movimiento.medida:
                movimiento.unidades = movimiento.cantidad
                movimiento.paquetes = movimiento.cantidad/producto.unidadPaquete
                movimiento.unidadesSueltas = movimiento.cantidad % producto.unidadPaquete
                movimiento.save()
                
                producto.existencias = producto.existencias - movimiento.unidades
                producto.save()
                
                movimiento.existencias = producto.existencias
                movimiento.save()
                
                producto.paquetes = producto.existencias / producto.unidadPaquete
                producto.sueltas = producto.existencias % producto.unidadPaquete
                producto.save()
                
            else:
                movimiento.paquetes = movimiento.cantidad
                movimiento.unidades = movimiento.cantidad * producto.unidadPaquete
                movimiento.save()
                
                producto.existencias = producto.existencias - movimiento.unidades
                producto.save()
                
                movimiento.existencias = producto.existencias
                movimiento.save()
                
                producto.paquetes = producto.paquetes - movimiento.paquetes
                producto.sueltas = producto.existencias % producto.unidadPaquete
                producto.save()
                
                
            return redirect('core:productos2', 0)
    else:
        form = NuevaSalidaForm()
        form.initial['producto'] = producto.id
        form.initial['tipo'] = True
    
    return render(request, 'core/salida_form.html', {'form':form, 'producto':producto})


@login_required
def NuevaSalida2(request, pk):
    producto = Producto.objects.get(id = pk)
    
    if request.method == 'POST':
        form = NuevaSalidaForm2(request.POST)
        if form.is_valid():
            form.save()
            
            movimiento = Movimiento.objects.latest('id')
            producto = Producto.objects.get(id = pk)
            

            movimiento.unidades = movimiento.cantidad
            movimiento.unidadesSueltas = movimiento.cantidad
            movimiento.save()
            
            producto.existencias = producto.existencias - movimiento.unidades
            producto.sueltas = producto.sueltas - movimiento.unidadesSueltas
            producto.save()
            
            movimiento.existencias = producto.existencias
            movimiento.save()
                
            return redirect('core:productos2', 0)
    else:
        form = NuevaSalidaForm2()
        form.initial['producto'] = producto.id
        form.initial['tipo'] = True
    
    return render(request, 'core/salida_form.html', {'form':form, 'producto':producto})


#Inventario

@login_required
def inventario(request, categoria):
    filtro = categoria
    categorias = Categoria.objects.all()
    
    if filtro == 0:
        productos = Producto.objects.all()
    else:
        productos = Producto.objects.filter(categoria = filtro)
        
    return render(request, 'core/inventario.html', {'categorias': categorias, 'productos': productos, 'filtro':filtro})


def Kardex(request, pk):
    producto = Producto.objects.get(id = pk)
    movimientos = Movimiento.objects.filter(producto = producto)

    return render(request, 'core/kardex.html', {'movimientos':movimientos, 'producto':producto})