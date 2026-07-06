# task1: Implementing a Course Management System with Django REST Framework
# from django.urls import path
# from .views import CourseListView, CourseDetailView

# urlpatterns = [
#     path('courses/', CourseListView.as_view(), name='course-list'),
#     path('courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
# ]

# task2: Refactoring views to use DRF ViewSets and automatic URL routing

from rest_framework.routers import DefaultRouter
from .views import (
    CourseViewSet,
    StudentViewSet,
    EnrollmentViewSet
)

router = DefaultRouter()

router.register(r'courses', CourseViewSet)
router.register(r'students', StudentViewSet)
router.register(r'enrollments', EnrollmentViewSet)

urlpatterns = router.urls