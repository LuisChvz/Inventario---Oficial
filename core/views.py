from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from braces.views import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import NuevaCategoriaForm, NuevoProductoForm, NuevoProductoForm2, NuevaEntradaForm, NuevaEntradaForm2, NuevaSalidaForm, NuevaSalidaForm2, EditarSalidaForm, EditarSalidaForm2, NuevoUserForm
from .models import Categoria, Producto, Movimiento
from django.contrib.auth.models import User
from django import forms





class NuevaCategoria(LoginRequiredMixin, CreateView):
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

    #Crear
    
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
                
                
            return redirect('core:kardex', producto.id)
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
                
            return redirect('core:kardex', producto.id)
    else:
        form = NuevaEntradaForm2()
        form.initial['producto'] = pk
    
    return render(request, 'core/entrada_form.html', {'form':form, 'producto':producto})


    #Editar
    
@login_required
def EditarEntrada(request, pk):
    movimiento = Movimiento.objects.get(id = pk)
    producto = Producto.objects.get(id = movimiento.producto.id)
    
    if request.method == 'POST':
        form = NuevaEntradaForm(request.POST)
        if form.is_valid():
            
            #Restaurando valores
            if movimiento.medida:
                        
                producto.existencias = producto.existencias - movimiento.unidades
                producto.save()
                        
                producto.paquetes = producto.existencias / producto.unidadPaquete
                producto.sueltas = producto.existencias % producto.unidadPaquete
                producto.save()
                        
            else:
                        
                producto.existencias = producto.existencias - movimiento.unidades
                producto.save()
                        
                producto.paquetes = producto.paquetes - movimiento.paquetes
                producto.sueltas = producto.existencias % producto.unidadPaquete
                producto.save()
            

            #Guardando movimiento
            
            movimiento.medida = form.cleaned_data['medida']
            movimiento.cantidad = form.cleaned_data['cantidad']
            movimiento.save()
            
            
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
                
                
            return redirect('core:kardex', producto.id)
    else:
        form = NuevaEntradaForm()
        form.initial['producto'] = movimiento.producto
        form.initial['medida'] = movimiento.medida
        form.initial['cantidad'] = movimiento.cantidad
    
    return render(request, 'core/entrada_form.html', {'form':form, 'producto':producto})


@login_required
def EditarEntrada2(request, pk):
    movimiento = Movimiento.objects.get(id = pk)
    producto = Producto.objects.get(id = movimiento.producto.id)
    
    if request.method == 'POST':
        form = NuevaEntradaForm2(request.POST)
        if form.is_valid():
            
            #Restaurando valores
            producto.existencias = producto.existencias - movimiento.unidades
            producto.sueltas = producto.sueltas - movimiento.unidadesSueltas
            producto.save()

            #Guardando movimiento
            
            movimiento.cantidad = form.cleaned_data['cantidad']
            movimiento.save()
            

            movimiento.unidades = movimiento.cantidad
            movimiento.unidadesSueltas = movimiento.cantidad
            movimiento.save()
            
            producto.existencias = producto.existencias + movimiento.unidades
            producto.sueltas = producto.sueltas + movimiento.unidadesSueltas
            producto.save()
            
            movimiento.existencias = producto.existencias
            movimiento.save()
                
            return redirect('core:kardex', producto.id)
    else:
        form = NuevaEntradaForm2()
        form.initial['producto'] = movimiento.producto
        form.initial['cantidad'] = movimiento.cantidad
        
    
    return render(request, 'core/entrada_form.html', {'form':form, 'producto':producto})

    #Eliminar

def Confirmacion(request, pk):
    movimiento = Movimiento.objects.get(id=pk)
    return render(request, "core/confirmacion.html", {'movimiento':movimiento})
    

@login_required
def EliminarEntrada(request, pk):
    movimiento = Movimiento.objects.get(id = pk)
    producto = Producto.objects.get(id = movimiento.producto.id)
            
    if movimiento.medida:
                
        producto.existencias = producto.existencias - movimiento.unidades
        producto.save()
                
        producto.paquetes = producto.existencias / producto.unidadPaquete
        producto.sueltas = producto.existencias % producto.unidadPaquete
        producto.save()
                
    else:
                
        producto.existencias = producto.existencias - movimiento.unidades
        producto.save()
                
        producto.paquetes = producto.paquetes - movimiento.paquetes
        producto.sueltas = producto.existencias % producto.unidadPaquete
        producto.save()
        
    movimiento.delete()
                         
    return redirect('core:kardex', producto.id)


@login_required
def EliminarEntrada2(request, pk):
    movimiento = Movimiento.objects.get(id = pk)
    producto = Producto.objects.get(id = movimiento.producto.id)
            
    producto.existencias = producto.existencias - movimiento.unidades
    producto.sueltas = producto.sueltas - movimiento.unidadesSueltas
    producto.save()
            
    movimiento.delete()
                
    return redirect('core:kardex', producto.id)
    
    
    
#Salidas

    #Crear

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
                
                
            return redirect('core:kardex', producto.id)
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
                
            return redirect('core:kardex', producto.id)
    else:
        form = NuevaSalidaForm2()
        form.initial['producto'] = producto.id
        form.initial['tipo'] = True
    
    return render(request, 'core/salida_form.html', {'form':form, 'producto':producto})


    #Editar
    
@login_required
def EditarSalida(request, pk):
    movimiento = Movimiento.objects.get(id = pk)
    producto = Producto.objects.get(id = movimiento.producto.id)
    
    if request.method == 'POST':
        form = EditarSalidaForm(request.POST)
        if form.is_valid():
            
            #Restaurando valores
            if movimiento.medida:
                
                producto.existencias = producto.existencias + movimiento.unidades
                producto.save()
                        
                producto.paquetes = producto.existencias / producto.unidadPaquete
                producto.sueltas = producto.existencias % producto.unidadPaquete
                producto.save()
                        
            else:
            
                producto.existencias = producto.existencias + movimiento.unidades
                producto.save()
                        
                producto.paquetes = producto.paquetes + movimiento.paquetes
                producto.sueltas = producto.existencias % producto.unidadPaquete
                producto.save()
            
            #Guardando valores
            
            movimiento.medida = form.cleaned_data['medida']
            movimiento.cantidad = form.cleaned_data['cantidad']
            movimiento.save()
            
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
                
                
            return redirect('core:kardex', producto.id)
    else:
        form = EditarSalidaForm()
        form.initial['producto'] = producto.id
        form.initial['tipo'] = True
        form.initial['cantidad'] = movimiento.cantidad
        form.initial['medida'] = movimiento.medida
    
    return render(request, 'core/salida_form.html', {'form':form, 'producto':producto})


@login_required
def EditarSalida2(request, pk):
    movimiento = Movimiento.objects.get(id = pk)
    producto = Producto.objects.get(id = movimiento.producto.id)
    
    if request.method == 'POST':
        form = EditarSalidaForm2(request.POST)
        if form.is_valid():
            form.save()
            
            #Restaurando valores
            producto.existencias = producto.existencias + movimiento.unidades
            producto.sueltas = producto.sueltas + movimiento.unidadesSueltas
            producto.save()
            
            #Guardando valores
            movimiento.cantidad = form.cleaned_data['cantidad']
            movimiento.save()
            

            movimiento.unidades = movimiento.cantidad
            movimiento.unidadesSueltas = movimiento.cantidad
            movimiento.save()
            
            producto.existencias = producto.existencias - movimiento.unidades
            producto.sueltas = producto.sueltas - movimiento.unidadesSueltas
            producto.save()
            
            movimiento.existencias = producto.existencias
            movimiento.save()
                
            return redirect('core:kardex', producto.id)
    else:
        form = EditarSalidaForm2()
        form.initial['producto'] = producto.id
        form.initial['tipo'] = True
        form.initial['cantidad'] = movimiento.cantidad
    
    return render(request, 'core/salida_form.html', {'form':form, 'producto':producto})
    

    #Eliminar

@login_required
def EliminarSalida(request, pk):
    movimiento = Movimiento.objects.get(id = pk)       
    producto = Producto.objects.get(id = movimiento.producto.id)

    if movimiento.medida:
                
        producto.existencias = producto.existencias + movimiento.unidades
        producto.save()
                
        producto.paquetes = producto.existencias / producto.unidadPaquete
        producto.sueltas = producto.existencias % producto.unidadPaquete
        producto.save()
                
    else:
     
        producto.existencias = producto.existencias + movimiento.unidades
        producto.save()
                
        producto.paquetes = producto.paquetes + movimiento.paquetes
        producto.sueltas = producto.existencias % producto.unidadPaquete
        producto.save()
        
    movimiento.delete()        
                
    return redirect('core:kardex', producto.id)


@login_required
def EliminarSalida2(request, pk):
    movimiento = Movimiento.objects.get(id = pk)    
    producto = Producto.objects.get(id = movimiento.producto.id)
            
    producto.existencias = producto.existencias + movimiento.unidades
    producto.sueltas = producto.sueltas + movimiento.unidadesSueltas
    producto.save()
            
    movimiento.delete()
                
    return redirect('core:kardex', producto.id)
    


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


#Usuarios
class NuevoUsuario(LoginRequiredMixin, CreateView):
    model = User
    form_class = NuevoUserForm
    template_name = 'core/user_form.html'
    success_url = reverse_lazy('home')
    
    def get_form(self, form_class = None):
        form = super(NuevoUsuario, self).get_form()

        form.fields['password1'].widget = forms.PasswordInput(attrs={'class':'form-control mb-2', 'placeholder':'Contraseña: '})
        form.fields['password2'].widget = forms.PasswordInput(attrs={'class':'form-control mb-2', 'placeholder':'Confirmar contraseña: '})
        return form
    
class UpdateUsuario(LoginRequiredMixin, UpdateView):
    model = User
    form_class = NuevoUserForm
    template_name = 'core/user_update.html'
    success_url = reverse_lazy('home')
    
    def get_form(self, form_class = None):
        form = super(UpdateUsuario, self).get_form()

        form.fields['password1'].widget = forms.PasswordInput(attrs={'class':'form-control mb-2', 'placeholder':'Contraseña: '})
        form.fields['password2'].widget = forms.PasswordInput(attrs={'class':'form-control mb-2', 'placeholder':'Confirmar contraseña: '})
        return form
    

@login_required
def home(request):
    categorias = Categoria.objects.all()
    productos = Producto.objects.all()
    i=0
    cantidades = []
    nombres = []
    cantidad = Categoria.objects.filter().count
    
    for c in categorias:
        nombres.append(c.nombre)
        cuenta = 0
        for p in productos:
            if p.categoria == c:
                cuenta = cuenta + p.existencias
        
        cantidades.append(cuenta)
                
        i = i + 1
    
    return render(request, 'core/home.html', {'categorias': categorias, 'productos': productos, 'nombres':nombres, 'cantidad':cantidad, 'cantidades':cantidades})