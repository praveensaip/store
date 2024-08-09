from django.urls import path
from .import views

urlpatterns = [
    path('add_store',views.add_store,name='add_store'),
    path('',views.store_list,name='store_list'),
    path('delete_list/<int:id>/',views.delete_list,name='delete_list'),
    path('productadd/',views.productadd,name='productadd'),
    path('deleteproduct/<int:id>/',views.deleteproduct,name='deleteproduct'),
    path('updateproduct/<int:id>/',views.updateproduct,name='updateproduct'),
    path('addstore/',views.addstore,name='addstore'),
    path('export_products_to_excel',views.export_products_to_excel,name='export_products_to_excel'),
    path('deletestore/<str:storename>/',views.deletestore,name='deletestore'),
    path('updatestore/<str:storename>/',views.updatestore,name='updatestore'),
    path('storing/',views.storing,name='storing'),
    path('deletestoring/<str:storename>',views.deletestoring,name='deletestoring'),
    path('demo/',views.demoving,name='demoving')
    
    
    
    
    

    
    # path('productlist',views.productlist,name='productlist')

    
    
    
    # path('delete_confirm',views.delete_confirm,name='delete_confirm'),
    
    
]
