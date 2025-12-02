from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import DetailView
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth import logout
from django.utils import timezone
import random

from rest_framework import filters, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Articles, Comments
from .forms import CommentForm, ArticleForm, ChangePasswordForm
from .serializers import ArticlesSerializer, CommentsSerializer
from .filters import CommentsFilter

def index(request):
    articles = Articles.objects.order_by('-date')
    all_articles = list(articles)
    popular_articles = random.sample(all_articles, min(3, len(all_articles)))
    paginator = Paginator(articles, 4)  
    page_number = request.GET.get('page')
    news = paginator.get_page(page_number)
    return render(request, 'main/index.html', {'news': news, 'popular_articles': popular_articles})

class NewsDetailView(DetailView):
    model = Articles
    template_name = 'main/details_view.html'
    context_object_name = 'article'

    def get_queryset(self):
        return Articles.objects.prefetch_related('comments')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all().order_by('-id')
        all_articles = list(Articles.objects.exclude(id=self.object.id))
        context['recommended_articles'] = random.sample(all_articles, min(3, len(all_articles)))
        if self.request.user.is_authenticated:
            context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if not request.user.is_authenticated:
            return redirect('login')

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = self.object
            comment.author = request.user.username
            if comment.date is None:
                comment.date = timezone.now()
            comment.save()
            return redirect('news-detail', pk=self.object.pk)

        context = self.get_context_data()
        context['comment_form'] = form
        return render(request, self.template_name, context)

def about(request):
    return render(request, 'main/about.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  
    else:
        form = UserCreationForm()
    return render(request, 'main/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == "POST":
        new_email = request.POST.get("email", "").strip()
        new_username = request.POST.get("username", "").strip()
        new_first_name = request.POST.get("first_name", "").strip()
        new_last_name = request.POST.get("last_name", "").strip()
        updated = False

        if new_first_name and new_first_name != request.user.first_name:
            request.user.first_name = new_first_name
            updated = True
        if new_last_name and new_last_name != request.user.last_name:
            request.user.last_name = new_last_name
            updated = True
        if new_email and new_email != request.user.email:
            request.user.email = new_email
            updated = True
        if new_username and new_username != request.user.username:
            request.user.username = new_username
            updated = True
            
        if updated:
            request.user.save()
            messages.success(request, "Profile updated successfully.")
        else:
            messages.info(request, "Nothing to update.")

        return redirect("profile")

    user_articles = Articles.objects.filter(author=request.user.username).order_by('-date')
    user_comments = Comments.objects.filter(author=request.user.username).order_by('-date')
    articles_count = user_articles.count()
    comments_count = user_comments.count()
    return render(
        request,
        'main/profile.html',
        {
            'articles': user_articles,
            'comments': user_comments,
            'articles_count': articles_count,
            'comments_count': comments_count,
        })

@login_required
def change_password(request):
    if request.method == "POST":
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password changed successfully.")
            return redirect("profile")
    else:
        form = ChangePasswordForm(user=request.user)

    return render(request, "main/change_password.html", {"form": form})

@login_required
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user.username
            article.date = timezone.now()
            article.save()
            return redirect('profile') 
    else:
        form = ArticleForm()
    return render(request, 'main/create_article.html', {'form': form})

def login(request):
    return render(request, 'main/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

class ArticlesViewSet(viewsets.ModelViewSet):
    queryset = Articles.objects.all()
    serializer_class = ArticlesSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CommentsFilter
    search_fields = ['author', 'content']
    ordering_fields = ['author', 'content']
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]


    
    
