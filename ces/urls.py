"""ces URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url
from student import views as studentView
from users import views as userView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', userView.login),
    url(r'^api/students/(?P<pk>[0-9]+)$', studentView.getStudent),
    url(r'^api/enrollments/$', studentView.enrollment_list),
    url(r'^api/enrollments/(?P<pk>[0-9]+)$', studentView.getEnrollment),
    url(r'^api/getCourses/(?P<pk>[0-9]+)$', studentView.getCourses)
]
