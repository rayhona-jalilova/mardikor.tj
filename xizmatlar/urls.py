from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import signup_view
from .views import chat_room


urlpatterns = [
    path('', views.xizmatlar_royxati, name='xizmatlar_royxati'),
    path('add/', views.add_service, name='add_service'),
    path('delete/<int:pk>/', views.delete_service, name='delete_service'),
    path('delete/<int:pk>/', views.delete_santexnik_service, name='delete_service'),
    path('xizmat/<int:pk>/', views.service_detail, name='service_detail'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='xizmatlar/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('send-message/', views.send_message, name='send_message'),
    path('about/', views.about, name='about'),
    path('home/', views.home, name='home'),
    path('contact/<int:provider_id>/', views.contact_provider, name='contact_provider'),
    path('chat/<str:room_name>/', chat_room, name='chat_room'),
    path('xasharchi/', views.xasharchilar, name='xasharchi'),
    path('santextiklar/', views.santexniklar, name='santexniklar'),
    path('qassob/', views.qassoblar, name='qassob'),
    path('barqchi/', views.barqchilar, name='barqchi'),
    path('cleaner/', views.cleaners, name='cleaner'),
    path('add_santexnik_service', views.add_santexnik_service, name='add_santexnik_service'),
    path('delete/<int:pk>/', views.delete_santexnik_service, name='delete_santexnik_service'),
    path('xizmatlar/<str:category>/', views.service_by_category, name='services_by_category'),
    path('skidka/', views.skidka_xizmatlar, name='skidka'),
    path('skidka/add/', views.chegirmali_xizmat_qoshish, name='chegirmali_xizmat_qoshish'),
    path('book/<int:xizmat_id>/', views.book_service, name='book_service'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
