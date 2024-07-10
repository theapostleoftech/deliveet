"""
This contains url routes for the courier app.
"""
from django.urls import path
from . import views
from profiles.views import courier_profile_view
from .apis.apis import delivery_tasks_api, delivery_task_status_api, fcm_token_update_api

app_name = 'couriers'
urlpatterns = [
    path('dashboard/', views.CourierDashboardView.as_view(), name='courier_dashboard'),

    path('apis/deliveries/tasks', delivery_tasks_api, name='courier_delivery_tasks_api'),

    path('apis/deliveries/ongoing/<uuid:id>/status', delivery_task_status_api, name='courier_delivery_tasks_status'),

    path('apis/deliveries/tasks/fcm', delivery_tasks_api, name='courier_delivery_tasks_fcm'),

    path('me/', courier_profile_view, name='courier_profile'),

    path('deliveries/tasks/', views.courier_available_delivery_tasks, name='available_delivery_tasks'),

    path('deliveries/tasks/<id>/', views.courier_available_delivery_task, name='available_delivery_task'),

    path('deliveries/ongoing/', views.courier_delivery_task, name='delivery_task'),

    path('deliveries/ongoing/<id>/take-photo', views.courier_delivery_task_take_photo, name='delivery_task_photo'),

    path('deliveries/tasks/completed', views.courier_delivery_task_completed, name='delivery_task_completed'),

    path('deliveries/tasks/past', views.courier_past_delivery_tasks, name='delivery_task_past'),

]
