from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from api.v1.base.utils.filters import CreatedRangeFilter
from api.v1.base.utils.permissions import IsAdminOrCreateOnly
from api.v1.sponsor import serializers
from senat.models import Sponsor


class SponsorListCreateView(generics.ListCreateAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = serializers.SponsorListCreateSerializer
    permission_classes = (IsAdminOrCreateOnly,)
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['fullname', 'phone_number', 'company_name']
    filter_fields = ['status', 'money', 'company_name']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({'success': True}, status=status.HTTP_201_CREATED)


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
