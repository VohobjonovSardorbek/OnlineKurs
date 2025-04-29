from django.urls import path

from main.views import CourseListCreateAPIView, CourseRetrieveUpdateDestroyAPIView, LessonListCreateAPIView, \
    LessonRetrieveUpdateDestroyAPIView, CourseEnrollView, CourseStudentsView, PaymentsAPIView, CourseReviewAPIView, \
    CoursePayAPIView

urlpatterns = [
    path('courses/', CourseListCreateAPIView.as_view()),
    path('courses/<int:pk>/', CourseRetrieveUpdateDestroyAPIView.as_view()),
    path('courses/<int:pk>/enroll/', CourseEnrollView.as_view()),
    path('courses/<int:pk>/students/', CourseStudentsView.as_view()),
    path('courses/<int:pk>/reviews/', CourseReviewAPIView.as_view()),
    path('courses/<int:pk>/pay/', CoursePayAPIView.as_view()),
    path('lessons/', LessonListCreateAPIView.as_view()),
    path('lessons/<int:pk>/', LessonRetrieveUpdateDestroyAPIView.as_view()),
    path('payments/', PaymentsAPIView.as_view()),
]
