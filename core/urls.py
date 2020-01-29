from django.urls import path
from .views import home, NuevaCategoria, NuevoProducto, NuevoProducto2, Indice, inventario, Productos, Productos2, Kardex, EliminarProducto, EditarProducto, EditarProducto2
from .views import NuevaEntrada, NuevaEntrada2, NuevaSalida, NuevaSalida2, EliminarEntrada, EliminarEntrada2, Confirmacion, EliminarSalida, EliminarSalida2, EditarEntrada, EditarEntrada2
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', home, name="home"),
]

core_patterns = ([
    path('nuevacategoria', NuevaCategoria.as_view(), name = 'nuevacategoria'),
    
    #Producto
    path('nuevoproducto', NuevoProducto.as_view(), name = 'nuevoproducto'),
    path('nuevoproducto2', NuevoProducto2.as_view(), name = 'nuevoproducto2'),
    path('editarproducto/<int:pk>', EditarProducto.as_view(), name = 'editarproducto'),
    path('editarproducto2/<int:pk>', EditarProducto2.as_view(), name = 'editarproducto2'),
    path('eliminarproducto/<int:pk>', EliminarProducto.as_view(), name = 'eliminarproducto'),
    path('indice/<int:categoria>', Indice, name = 'indice'),
    path('productos/<int:categoria>', Productos, name = 'productos'),
    path('productos2/<int:categoria>', Productos2, name = 'productos2'),
    
    #Entradas
    path('nuevaentrada/<int:pk>', NuevaEntrada, name = 'nuevaentrada'),
    path('nuevaentrada2/<int:pk>', NuevaEntrada2, name = 'nuevaentrada2'),
    path('eliminarentrada/<int:pk>', EliminarEntrada, name = 'eliminarentrada'),
    path('eliminarentrada2/<int:pk>', EliminarEntrada2, name = 'eliminarentrada2'),
    path('confirmacion/<int:pk>', Confirmacion, name = 'confirmacion'),
    path('editarentrada/<int:pk>', EditarEntrada, name = 'editarentrada'),
    path('editarentrada2/<int:pk>', EditarEntrada2, name = 'editarentrada2'),
    
    #Salidas
    path('nuevasalida/<int:pk>', NuevaSalida, name = 'nuevasalida'),
    path('nuevasalida2/<int:pk>', NuevaSalida2, name = 'nuevasalida2'),
    path('eliminarsalida/<int:pk>', EliminarSalida, name = 'eliminarsalida'),
    path('eliminarsalida2/<int:pk>', EliminarSalida2, name = 'eliminarsalida2'),
    
    #Inventario
    path('kardex/<int:pk>', Kardex, name = 'kardex'),
    path('inventario/<int:categoria>', inventario, name = 'inventario'),
    
    
    
], 'core')