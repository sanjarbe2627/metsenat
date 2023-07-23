from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from api.v1.base.utils.filters import CreatedRangeFilter
from api.v1.base.utils.permissions import IsAdminOrCreateOnly
from api.v1.sponsor import serializers
from senat.models import Sponsor, Sponsorship


class SponsorListCreateView(generics.ListCreateAPIView):
    permission_classes = (IsAdminOrCreateOnly,)
    queryset = Sponsor.objects.all()
    serializer_class = serializers.SponsorListCreateSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_class = CreatedRangeFilter
    search_fields = ['fullname', 'phone_number', 'company_name']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        serializer = serializers.SponsorDetailUpdateSerializer(serializer.instance, many=False)
        return Response({'result': serializer.data}, status=status.HTTP_201_CREATED)


class SponsorDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = serializers.SponsorDetailUpdateSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            sponsor = self.queryset.get(pk=kwargs['pk'])
            serializer = self.get_serializer(sponsor)
            return Response({'result': serializer.data}, status=status.HTTP_200_OK)
        except Sponsor.DoesNotExist:
            pass
        return Response({'result': {}}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        try:
            instance = self.queryset.get(pk=kwargs['pk'])
            serializer = self.get_serializer(data=request.data, instance=instance)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            return Response({'result': serializer.data}, status=status.HTTP_200_OK)
        except Sponsor.DoesNotExist:
            pass

        return Response({'result': {}}, status=status.HTTP_404_NOT_FOUND)


# Sponsorship view
class SponsorshipListCreateView(generics.ListCreateAPIView):
    queryset = Sponsorship.objects.all()
    serializer_class = serializers.SponsorshipSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = [
        'sponsor__fullname', 'sponsor__phone_number', 'sponsor__company_name',
        'student__fullname', 'student__phone_number', 'student__university__name',
    ]
    filter_fields = ["sponsor", "student"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({"result": serializer.data}, status=status.HTTP_201_CREATED)


class SponsorshipDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sponsorship.objects.all()
    serializer_class = serializers.SponsorshipSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            sponsorship = self.queryset.get(pk=kwargs['pk'])
            serializer = self.get_serializer(sponsorship)
            return Response({'result': serializer.data}, status=status.HTTP_200_OK)
        except Sponsorship.DoesNotExist:
            pass

        return Response({'result': {}}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        try:
            instance = self.queryset.get(pk=kwargs['pk'])
            serializer = self.get_serializer(
                data=request.data, instance=instance, context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            return Response({'result': serializer.data}, status=status.HTTP_200_OK)
        except Sponsorship.DoesNotExist:
            pass
        return Response({'result': {}}, status=status.HTTP_404_NOT_FOUND)
