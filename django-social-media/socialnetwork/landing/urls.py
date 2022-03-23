from django.urls import path
from landing.views import PostListView, PostCreateView, PostDetailView, UserPostListView, search_user
from django.conf import settings
from django.conf.urls.static import static

urlpatterns =  [
    path('', PostListView.as_view(), name="home"),
    path('user/<username>/', UserPostListView.as_view(), name='user-post'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('search/users/', search_user, name='search-user'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)