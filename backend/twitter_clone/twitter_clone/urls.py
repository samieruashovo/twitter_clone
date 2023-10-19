from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from tweets import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('tweets/', include('tweets.urls')),
    path('posts/', include('community.urls')),

    path('notify/', include('notifications.urls')),
    path('chats/', include('chat.urls')),
    path('community/', include('community.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/token/',  include('djoser.urls.jwt')),
    path("create/", views.TweetViewSet.as_view({'post': 'create_tweet'}), name="create-tweet"),
    path('media/<str:image_filename>', views.serve_image, name='serve_image'),
] 
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)