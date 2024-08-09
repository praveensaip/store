from django.urls import path
from.import views

urlpatterns = [
    path('',views.snack_list,name='snacks_list'),
    path('store_list',views.store_list,name='store_list'),
    path('add_snacks',views.add_snacks,name='add_snacks'),
    path('add_store',views.add_store,name='add_store'),
    path('delete_store/<int:store_id>/',views.delete_store,name='delete_store'),
    path('update_store/<int:store_id>/',views.update_store,name='update_store')
    
    
]
