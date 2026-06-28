from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('nuevo/', views.crear_producto, name='crear_producto'),
    path('editar/<int:pk>/', views.editar_producto, name='editar_producto'),
    path('eliminar/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),

    # Rutas del carrito
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/restar/<int:producto_id>/', views.restar_del_carrito, name='restar_del_carrito'),
    path('carrito/eliminar/<int:producto_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('carrito/limpiar/', views.limpiar_carrito, name='limpiar_carrito'),
    path('carrito/pagar/', views.procesar_pago, name='procesar_pago'),
]