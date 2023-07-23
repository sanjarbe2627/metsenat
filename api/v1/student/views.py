from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from api.v1.base.utils.filters import CreatedRangeFilter
from api.v1.student import serializers
from senat.models import Student, University


# Student view
class StudentListCreateView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = serializers.StudentSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_class = CreatedRangeFilter
    search_fields = ['fullname', 'phone_number', 'university__name']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        serializer = serializers.StudentDetailUpdateSerializer(
            serializer.instance, many=False
        )
        return Response({'result': serializer.data}, status=status.HTTP_201_CREATED)


class StudentDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = serializers.StudentDetailUpdateSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            student = self.queryset.get(pk=kwargs['pk'])
            serializer = self.get_serializer(student)
            return Response({'result': serializer.data}, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            pass
        return Response({'result': {}}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        try:
            instance = self.queryset.get(pk=kwargs['pk'])
            serializer = self.get_serializer(data=request.data, instance=instance)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            return Response({'result': serializer.data}, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            pass

        return Response({'result': {}}, status=status.HTTP_404_NOT_FOUND)


# University view

class UniversityListCreateView(generics.ListCreateAPIView):
    queryset = University.objects.all()
    serializer_class = serializers.StudentUniversitySerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({'result': serializer.data}, status=status.HTTP_201_CREATED)


class UniversityDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = University.objects.all()
    serializer_class = serializers.StudentUniversitySerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            university = self.queryset.get(pk=kwargs['pk'])
            serializer = self.get_serializer(university)
            return Response({'result': serializer.data}, status=status.HTTP_200_OK)
        except University.DoesNotExist:
            pass
        return Response({'result': {}}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        try:
            instance = self.queryset.get(pk=kwargs['pk'])
            serializer = self.get_serializer(data=request.data, insntance=instance)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            return Response({'result': serializer.data}, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            pass

        return Response({'result': {}}, status=status.HTTP_404_NOT_FOUND)
