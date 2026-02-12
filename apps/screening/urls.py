from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ScreeningResultViewSet, ScreeningView, InstantScreeningView

router = DefaultRouter()
router.register(r'results', ScreeningResultViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('screen/<int:pk>/', ScreeningView.as_view(), name='screen_job'),
    path('instant/', InstantScreeningView.as_view(), name='instant_screen'),
]
