"""question URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from ques import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('welcome/', views.welcome),
    path('random/<chapter>/', views.chapter),
    path('question/<question_id>', views.question),
    path('random/', views.random),
    path('registry/', views.registry),
    path('wrong/', views.wrong),
    path('do/', views.do),
    path('api/changeCategory/<category_id>', views.change_category),
    path('api/changePassword', views.change_password)
]
