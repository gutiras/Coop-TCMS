from django.contrib import admin
from django.urls import path
from . import views 
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView



urlpatterns = [   
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('',views.index, name='index'),
    path('profile/', views.profile, name='profile'),
    path('upload/', views.upload_file, name='upload'),  
    path('test_update/', views.test_update, name='test_update'),
    path('login/', views.login, name='login'),  
    path('testcase_display/<str:group>/<str:filename>', views.testcase_display, name='testcase_display'),
    path('newproject/', views.newproject, name='newproject'),
    path('download/<str:file_name>/<str:group>/', views.download_file, name='download_file'),
    path('search/', views.search_results, name='search_results'),
    path('delete_project/<str:project_name>/', views.delete_project, name='delete_project'),
    path('delete_file/<str:file_name>/', views.delete_file, name='delete_file'),
    path('export-excel/<str:filename>/<str:group>/', views.export_to_excel, name='export_to_excel'),
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)