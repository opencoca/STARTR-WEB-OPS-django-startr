from django.urls import path
from .views import load_lazy_inline

urlpatterns = [
    # URL pattern for lazy loading admin inlines
    path('lazy-inline/<str:app_label>/<str:model_name>/<str:object_id>/', 
         load_lazy_inline, 
         name='admin_lazy_inline'),
]
