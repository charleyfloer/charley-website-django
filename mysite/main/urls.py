from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from .views import ArticlesViewSet, CommentsViewSet
from . import views

router = DefaultRouter()
router.register(r'articles', ArticlesViewSet, basename='articles')
router.register(r'comments', CommentsViewSet, basename='comments')

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path("profile/change-password/", views.change_password, name="change-password"),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='main/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('news/<int:pk>/', views.NewsDetailView.as_view(), name='news-detail'),
    path('create-article/', views.create_article, name='create-article'),
    path('api/', include(router.urls)),
]

