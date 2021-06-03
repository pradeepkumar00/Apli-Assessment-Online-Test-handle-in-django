from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sign', views.sign, name='sign'),
    path('login', views.logins, name='logins'),
    path('main', views.main, name='main'),
    path('logout', views.logouts, name='logout'),
    path('test', views.test, name='test'),
    path('add', views.add, name='add'),
    path('admin-panel', views.admin, name='admin'),
    path('email', views.email, name='adm'),
    path('saveemail', views.saveemail, name='saveemail'),
    path('atmtest', views.atmtest, name='atmtest'),
    path('savetest', views.savetest, name='savetest'),
    path('about', views.about, name='about'),
    path('solution', views.solution, name='solution'),
]
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]
