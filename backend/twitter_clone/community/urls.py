from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
router = DefaultRouter()

router.register(r"", views.PostViewSet, basename="community")

urlpatterns = [
    path("", include(router.urls)),
    path("comments/list/<str:pk>", views.PostComentView.as_view()),
    path("detail/<str:uuid>", views.PostDetailsView.as_view())
]
