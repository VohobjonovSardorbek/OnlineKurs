from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import SAFE_METHODS, AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import *
from users.permissions import Is_Teacher, Is_Student
from users.serializers import StudentSerializer
from .permissions import IsTeacherOrIsPaid
from .serializers import *
from .models import *
from rest_framework.views import APIView
from rest_framework.generics import *
from .filters import CourseFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100


class CourseListCreateAPIView(ListCreateAPIView):
    queryset = Course.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = CourseFilter
    ordering_fields = ['price', 'rating']
    ordering = ['price']
    pagination_class = CustomPagination

    @swagger_auto_schema(
        request_body=CoursePostSerializer,
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return CourseSerializer
        return CoursePostSerializer

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)


class CoursePayAPIView(APIView):
    permission_classes = [Is_Student]

    @swagger_auto_schema(
        request_body=PaymentSerializer
    )
    def post(self, request, pk):
        course = get_object_or_404(Course, id=pk)
        serializer = PaymentSerializer(data=request.data)
        if not Payment.objects.filter(user=request.user, course=course).exists():
            if serializer.is_valid():
                serializer.save(course=course, user=request.user, status=Payment.COMPLETED)
                return Response({
                    'success': True,
                    'message': "To'lov muvaffaqiyatli amalga oshirildi!"
                },
                    status=HTTP_201_CREATED
                )
            return Response(
                {
                    'success': False,
                    'errors': serializer.errors
                },
                status=HTTP_400_BAD_REQUEST
            )
        return Response(
            data={
                "message": "Siz oldin ushbu kurs uchun to'lov qilgansiz!"
            }
        )


class CourseEnrollView(APIView):
    permission_classes = [Is_Student]

    def post(self, request, pk):
        course = get_object_or_404(Course, id=pk)

        if Payment.objects.filter(user=request.user.student, course=course,
                                  status=Payment.COMPLETED).exists():
            return Response(
                data={
                    'message': "Siz ushbu kurs uchun to'lov qilmagansiz!"
                }
            )

        if course in Student.objects.get(user=request.user).course.all():
            return Response(
                data={
                    "message": "Siz ro'yxatdan allaqachon o'tgansiz!"
                }
            )

        student = Student.objects.get(user=request.user)
        student.course.add(course)


class CourseStudentsView(APIView):
    def get(self, request, pk):
        students = Student.objects.filter(course__id=pk)

        serializers = StudentSerializer(students, many=True)
        return Response(serializers.data)


class CourseRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return CourseSerializer
        return CoursePostSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        return [IsAuthenticated(), Is_Teacher()]

    def perform_update(self, serializer):
        if serializer.instance.instructor != self.request.user:
            raise PermissionDenied("Siz ushbu kursni tahrirlash huquqiga ega emassiz!")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.instructor != self.request.user:
            raise PermissionDenied("Siz ushbu kursni o'chirish huquqiga ega emassiz!")
        instance.delete()


class LessonListCreateAPIView(ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    @swagger_auto_schema(
        request_body=LessonSerializer
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        return [IsTeacherOrIsPaid()]


class LessonRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    @swagger_auto_schema(request_body=LessonSerializer)
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(request_body=LessonSerializer)
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        return [IsAuthenticated(), Is_Teacher()]

    def perform_update(self, serializer):
        if serializer.instance.course.instructor != self.request.user:
            raise PermissionDenied("Siz ushbu lessonni tahrirlash huquqiga ega emassiz!")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.course.instructor != self.request.user:
            raise PermissionDenied("Siz ushbu lessonni o'chirish huquqiga ega emassiz!")
        instance.delete()


class PaymentsAPIView(APIView):
    def get(self, request):
        payments = Payment.objects.filter(user=request.user)
        serializers = PaymentSerializer(payments, many=True)
        return Response(serializers.data)


class CourseReviewAPIView(APIView):

    def get(self, request, pk):
        course = get_object_or_404(Course, id=pk)
        reviews = Review.objects.filter(course=course)
        serializers = ReviewSerializer(reviews, many=True)
        return Response(serializers.data)

    @swagger_auto_schema(
        request_body=ReviewSerializer
    )
    def post(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        student = getattr(request.user, 'student', None)
        is_paid = Payment.objects.filter(
            user=student,
            course=course,
            status=Payment.COMPLETED
        ).exists()

        if student and is_paid:
            serializer = ReviewSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(course=course, user=student)
                return Response(
                    {
                        'success': True,
                        "data": serializer.data
                    },
                    status=HTTP_201_CREATED
                )
            return Response(
                {
                    "success": False,
                    'errors': serializer.errors
                },
                status=HTTP_400_BAD_REQUEST
            )
        raise PermissionDenied(
            "Siz student emassiz yoki siz ushbu kursni ko'rish uchun to'lov qilmagansiz shuning uchun siz sharh qoldira olmaysiz!")
