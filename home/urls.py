from django.urls import path
from . import views

urlpatterns = [
    path('', views.index , name='home'),
    path('login/' , views.login_view , name='login'),
    path('signup/' ,views.signup, name='signup'),
    path('<str:username>/addblog/' ,views.addblog , name='addblog'),
    path('<int:blog_id>/seeblog/' ,views.seeblog , name='seeblog'),
    path('profile/<str:username>/' , views.profile , name='profile'),
    path('logout/' , views.logout_view , name='logout'),
    path('deleteblog/<int:blog_id>/' , views.delete , name='delete'),
    path('suggestion/' , views.suggestions , name='suggestion'),
    path('<int:blog_id>/update' , views.update , name='update')
]